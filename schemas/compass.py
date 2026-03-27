from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BasicProfileUpdate(BaseModel):
    full_name: str
    dob: date
    gender: Optional[str] = None
    current_class: str = Field(..., description="e.g., 9, 10, 11, 12")
    school_type: Optional[str] = None
    state: Optional[str] = None
    area_type: Optional[str] = Field(None, description="Urban, Semi-Urban, Rural, Tribal")
    medium_of_learning: Optional[str] = None

class AcademicProfileUpdate(BaseModel):
    overall_percentage_band: str = Field(..., description="e.g., 80-90%, Below 60%")
    strongest_subject: str
    weakest_subject: str
    favorite_subject: str
    learning_style: Optional[str] = None
    study_hours_home: Optional[int] = None
    homework_completion: Optional[str] = None
    achievements: Optional[str] = None

class PsychometricProfileUpdate(BaseModel):
    riasec_code: Optional[str] = None
    work_environment: Optional[str] = None
    work_style: Optional[str] = None
    biggest_strength: str
    biggest_weakness: str
    motivation_driver: str

class LifestyleProfileUpdate(BaseModel):
    screen_time: int = Field(..., description="Daily screen time in hours")
    sleep_quality: str = Field(..., description="Good, Average, Poor")
    stress_level: str = Field(..., description="High, Medium, Low")
    # Notice: We do NOT ask the frontend for focus_score. The backend calculates it!

class FinancialProfileUpdate(BaseModel):
    family_structure: Optional[str] = None
    income_band: str = Field(..., description="e.g., Below 3L, 3L-8L, Above 8L")
    father_education: Optional[str] = None
    mother_education: Optional[str] = None
    affordability_level: str
    coaching_access: bool

class AspirationProfileUpdate(BaseModel):
    dream_career: str
    life_direction: Optional[str] = None
    ten_year_vision: Optional[str] = None