from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

# import existing logic
from .roadmap import RoadmapResponse, generate_roadmap, _GOLD_SYSTEM_PROMPT
from models.mentorship import MentorFeedback, ParentFeedback
from models.roadmaps import Roadmap, RoadmapPhase, RoadmapTask
from models.users import User
from core.database import get_db
from api.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/roadmaps", tags=["Roadmap Pivot"])

@router.post("/adjust", status_code=201, response_model=RoadmapResponse)
async def adjust_student_path(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    """
    Analyzes Mentor and Parent feedback to pivot the existing active roadmap.
    """
    # 1. Fetch the Current Active roadmap.
    active_roadmap = db.query(Roadmap).filter(
        Roadmap.student_id == current_user.id,
        Roadmap.is_active == True
    ).first()

    if not active_roadmap:
        raise HTTPException(status_code=404, detail="No active roadmap found to adjust. Generate one first.")
    

    # 2. Extract Phase and Task details into a string for the LLM

    plan_details = []
    for phase in active_roadmap.phases:
        task_titles = [f"- {t.title}" for t in phase.tasks]
        tasks_str = "\n".join(task_titles)
        plan_details.append(f"Phase {phase.sequence}: {phase.title}\nTasks:\n{tasks_str}")

    current_plan_summary =  f"CURRENT PLAN BEING ADJUSTED:\n" + "\n\n".join(plan_details)

    # 3. Fetch Latest Mentor and Parent Feedback
    mentor_feedback = db.query(MentorFeedback).filter(
        MentorFeedback.student_id == current_user.id
    ).order_by(MentorFeedback.submitted_at.desc()).first()

    parent_feedback = db.query(ParentFeedback).filter(
        ParentFeedback.student_id == current_user.id
    ).order_by(ParentFeedback.logged_at.desc()).first()

    vision = ""
    if isinstance(current_user.aspiration_data, dict):
        vision = (
            current_user.aspiration_data.get("ten_year_vision")
            or current_user.aspiration_data.get("five_year_goal")
            or ""
        )

    # 4. Generate the adjusted roadmap using your existing function
    adjusted_data = await generate_roadmap(
        career_goal=active_roadmap.title,
        current_class=current_user.academic_data.get("current_class", "9th"),
        past_summary=current_plan_summary,
        vision=vision,
        academic_summary=current_user.academic_data,
        aptitude_summary=current_user.apti_data,
        personality_summary=current_user.personality_data,
        study_hours=current_user.lifestyle_data,
        financial_context=current_user.financial_data,
        mentor_action_items=mentor_feedback.action_items if mentor_feedback else "None",
        parent_observations=f"Habits: {parent_feedback.study_habits}" if parent_feedback else "None",
    )

    # 5. Handle DB
    active_roadmap.is_active = False
    db.flush()

    # 6. Create New Roadmap
    new_roadmap = Roadmap(
        student_id=current_user.id,
        title=adjusted_data.career_title,
        description=f"Level: {adjusted_data.student_level} | Difficulty: {adjusted_data.difficulty_level}",
        phase_number=active_roadmap.phase_number,
        is_active=True,
        status="Active"
    )
    db.add(new_roadmap)
    db.flush() # This gets us the new_roadmap.id without committing yet.

    # 7. Create New Phases and Tasks
    # Assuming adjust_data.phases is the list from AI response.
    for phase_in in adjusted_data.phases:
        # Convert the WeeklyTask objects into a serializable dictionary for JSONB
        serializable_weeks = [week.model_dump() for week in phase_in.weekly_breakdown]

        new_phase = RoadmapPhase(
            roadmap_id=new_roadmap.id,
            sequence=phase_in.phase_number,
            title=phase_in.phase_title,
            status="Active" if phase_in.phase_number == 1 else "Not Started",
            # Store the deep weekly nesting here
            tasks_data=serializable_weeks,
            completion_summary=f"Milestone: {phase_in.milestone_project}, Criteria: {phase_in.success_criteria}"
        )
        db.add(new_phase)
        db.flush()

        # create RoadmapTasks for tracking
        # Since the AI gives us weeks, we can create one DB task per week 
        # or one DB task for the Milestone Project.
        for week in phase_in.weekly_breakdown:
            new_task = RoadmapTask(
                phase_id=new_phase.id,
                sequence=week.week_number,
                title=week.topic,
                description=", ".join(week.tasks),
                status="Not Started"
            )
            db.add(new_task)
    
    # 8. Commit
    try:
        db.commit()
        db.refresh(new_roadmap)
        # Return the structured RoadmapResponse for the frontend
        return new_roadmap
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to persist adjusted roadmap: {e}")
        raise HTTPException(status_code=500, detail="Database error during roadmap pivot.")
