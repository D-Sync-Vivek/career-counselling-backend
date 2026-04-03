import psycopg2
import json
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_formatted_questions():
    """
    Returns the 45 questions for Grade 9-11 formatted with \n 
    to match the Grade 6-8 frontend rendering logic.
    """
    return [
        # === QUANTITATIVE APTITUDE ===
        {
            "document": "Question: A shirt costs ₹800. After a 15% discount, what is the final price?\nA) ₹640\nB) ₹680\nC) ₹700\nD) ₹720\nCorrect Answer: B\nExplanation: Discount = 15% of 800 = 120. Final price = 800 – 120 = ₹680.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Percentage Change", "target_grade": "9-11"}
        },
        {
            "document": "Question: Solve for x: 3x + 7 = 22.\nA) 3\nB) 4\nC) 5\nD) 6\nCorrect Answer: C\nExplanation: 3x = 22 – 7 = 15, so x = 15 / 3 = 5.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Linear Equations", "target_grade": "9-11"}
        },
        {
            "document": "Question: A bag has 4 red and 6 green balls. One ball is drawn at random. What is the probability it is red?\nA) 2/5\nB) 3/5\nC) 1/4\nD) 1/2\nCorrect Answer: A\nExplanation: P(red) = 4 / (4+6) = 4/10 = 2/5.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Basic Probability", "target_grade": "9-11"}
        },
        {
            "document": "Question: The price of a product rose from ₹500 to ₹600. What is the percentage increase?\nA) 15%\nB) 20%\nC) 25%\nD) 10%\nCorrect Answer: B\nExplanation: % increase = (100/500) × 100 = 20%.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Percentage Change", "target_grade": "9-11"}
        },
        {
            "document": "Question: Solve: 2x – 5 = 3x + 1.\nA) x = –6\nB) x = 6\nC) x = –3\nD) x = 3\nCorrect Answer: A\nExplanation: 2x – 3x = 1 + 5 → –x = 6 → x = –6.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Linear Equations", "target_grade": "9-11"}
        },
        {
            "document": "Question: Find the roots of x² – 5x + 6 = 0.\nA) 2 and 3\nB) 1 and 6\nC) –2 and –3\nD) 3 and 4\nCorrect Answer: A\nExplanation: Factorising: (x–2)(x–3) = 0 → x = 2 or x = 3.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Quadratic Equations", "target_grade": "9-11"}
        },
        {
            "document": "Question: The 10th term of an AP is 35 and the first term is 8. What is the common difference?\nA) 2\nB) 3\nC) 4\nD) 5\nCorrect Answer: B\nExplanation: a + 9d = 35 → 8 + 9d = 35 → 9d = 27 → d = 3.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Arithmetic Progressions", "target_grade": "9-11"}
        },
        {
            "document": "Question: A cylinder has radius 7 cm and height 10 cm. What is its volume? (π = 22/7)\nA) 1540 cm³\nB) 1440 cm³\nC) 1320 cm³\nD) 1640 cm³\nCorrect Answer: A\nExplanation: V = πr²h = (22/7) × 49 × 10 = 22 × 7 × 10 = 1540 cm³.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Volume of Shapes", "target_grade": "9-11"}
        },
        {
            "document": "Question: For the AP: 3, 7, 11, …, what is the sum of the first 15 terms?\nA) 465\nB) 480\nC) 495\nD) 510\nCorrect Answer: A\nExplanation: Sn = n/2 × [2a + (n–1)d] = 15/2 × [6 + 56] = 15/2 × 62 = 465.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Arithmetic Progressions", "target_grade": "9-11"}
        },
        {
            "document": "Question: The area of a trapezium is 180 cm². Its parallel sides are 10 cm and 20 cm. Find the height.\nA) 10 cm\nB) 12 cm\nC) 14 cm\nD) 16 cm\nCorrect Answer: B\nExplanation: Area = ½ × (a+b) × h → 180 = ½ × 30 × h → h = 360/30 = 12 cm.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Area of Complex Shapes", "target_grade": "9-11"}
        },
        {
            "document": "Question: If log₂(x) + log₂(4) = 5, find x.\nA) 4\nB) 8\nC) 16\nD) 32\nCorrect Answer: B\nExplanation: log₂(4x) = 5 → 4x = 2⁵ = 32 → x = 8.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Logarithms", "target_grade": "9-11"}
        },
        {
            "document": "Question: If sin θ = 3/5, find tan θ.\nA) 3/4\nB) 4/3\nC) 3/5\nD) 4/5\nCorrect Answer: A\nExplanation: cos θ = 4/5 (using Pythagoras). tan θ = sin θ / cos θ = (3/5)/(4/5) = 3/4.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Trigonometry Basics", "target_grade": "9-11"}
        },
        {
            "document": "Question: In how many ways can 4 students be chosen from a group of 9?\nA) 126\nB) 84\nC) 36\nD) 72\nCorrect Answer: A\nExplanation: C(9,4) = 9! / (4! × 5!) = (9×8×7×6) / (4×3×2×1) = 126.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Combinations", "target_grade": "9-11"}
        },
        {
            "document": "Question: If f(x) = 2x² – 3x + 1, find f(–2).\nA) 15\nB) 11\nC) 13\nD) 9\nCorrect Answer: A\nExplanation: f(–2) = 2(4) – 3(–2) + 1 = 8 + 6 + 1 = 15.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Functions", "target_grade": "9-11"}
        },
        {
            "document": "Question: How many 4-letter words (with repetition allowed) can be formed using letters A, B, C, D, E?\nA) 125\nB) 256\nC) 625\nD) 1024\nCorrect Answer: C\nExplanation: Each position has 5 choices. Total = 5⁴ = 625.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Permutations", "target_grade": "9-11"}
        },

        # === LOGICAL REASONING ===
        {
            "document": "Question: Find the next term: 5, 10, 17, 26, 37, ?\nA) 48\nB) 50\nC) 52\nD) 54\nCorrect Answer: B\nExplanation: Differences are +5, +7, +9, +11, +13. Next term = 37 + 13 = 50.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Number Series", "target_grade": "9-11"}
        },
        {
            "document": "Question: A is the father of B. B is the sister of C. How is A related to C?\nA) Uncle\nB) Father\nC) Grandfather\nD) Brother\nCorrect Answer: B\nExplanation: A is the father of B, and B is the sibling of C, so A is also the father of C.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Blood Relations", "target_grade": "9-11"}
        },
        {
            "document": "Question: Ram walks 10 m north, then 6 m east, then 10 m south. How far is he from the start?\nA) 4 m\nB) 5 m\nC) 6 m\nD) 8 m\nCorrect Answer: C\nExplanation: North and south cancel (10–10=0). He is only 6 m east of start.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Direction Sense", "target_grade": "9-11"}
        },
        {
            "document": "Question: Find the odd one out in the series: 3, 5, 7, 9, 11.\nA) 3\nB) 7\nC) 9\nD) 11\nCorrect Answer: C\nExplanation: 9 is the only composite number (3×3). All others are prime.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Number Series", "target_grade": "9-11"}
        },
        {
            "document": "Question: Pointing to a woman, Ravi says 'She is the daughter of my grandfather's only son.' How is she related to Ravi?\nA) Sister\nB) Cousin\nC) Mother\nD) Aunt\nCorrect Answer: A\nExplanation: Grandfather's only son = Ravi's father. The daughter of Ravi's father = Ravi's sister.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Blood Relations", "target_grade": "9-11"}
        },
        {
            "document": "Question: In a code, MANGO is written as OCPIQ. How is GRAPE coded?\nA) ITCRF\nB) ITCRG\nC) ITCQF\nD) HSCQF\nCorrect Answer: B\nExplanation: Each letter shifts +2. G→I, R→T, A→C, P→R, E→G. Answer = ITCRG.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Coding-Decoding", "target_grade": "9-11"}
        },
        {
            "document": "Question: Statements: All cats are dogs. All dogs are birds. Conclusion I: All cats are birds. II: All birds are cats.\nA) Only I\nB) Only II\nC) Both\nD) Neither\nCorrect Answer: A\nExplanation: By transitivity, all cats are birds. But not all birds need to be cats — the reverse isn't guaranteed.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Syllogisms", "target_grade": "9-11"}
        },
        {
            "document": "Question: Six people A–F sit in a row. A is third from left. B is to the immediate right of A. C is at the far right. Who is second from the right?\nA) D\nB) E\nC) B\nD) F\nCorrect Answer: A\nExplanation: Positions: _ _ A B _ C. Remaining: D, E, F fill positions 1, 2, 5. Second from right = position 5.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Seating Arrangement", "target_grade": "9-11"}
        },
        {
            "document": "Question: If BOOK = 2-15-15-11 (A=1…Z=26), what is DOOR?\nA) 4-15-15-18\nB) 3-15-15-18\nC) 4-14-14-18\nD) 4-15-14-17\nCorrect Answer: A\nExplanation: D=4, O=15, O=15, R=18. So DOOR = 4-15-15-18.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Coding-Decoding", "target_grade": "9-11"}
        },
        {
            "document": "Question: Statements: Some pens are books. No book is a pencil. Conclusion I: Some pens are not pencils. II: No pen is a pencil.\nA) Only I\nB) Only II\nC) Both\nD) Neither\nCorrect Answer: A\nExplanation: Since some pens are books and no book is a pencil, those pens (which are books) are definitely not pencils.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Syllogisms", "target_grade": "9-11"}
        },
        {
            "document": "Question: Is integer n divisible by 6? Statement I: n is divisible by 3. Statement II: n is divisible by 2.\nA) I alone sufficient\nB) II alone sufficient\nC) Both together sufficient\nD) Neither sufficient\nCorrect Answer: C\nExplanation: Divisible by 6 requires divisibility by both 2 and 3. Neither statement alone is sufficient; together they confirm it.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Data Sufficiency", "target_grade": "9-11"}
        },
        {
            "document": "Question: A net is folded into a cube. The net has a cross shape with one square on top, one at bottom, and four in a row. Which face is opposite the top face when folded?\nA) The bottom square\nB) The 3rd square in the row\nC) The 2nd square in the row\nD) The 4th square in the row\nCorrect Answer: A\nExplanation: When a cross-shaped net is folded, the top and bottom extension squares become opposite faces of the cube.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Spatial Folding / Nets", "target_grade": "9-11"}
        },
        {
            "document": "Question: Statement: 'Students who study daily score high.' Assumption I: Daily study improves scores. Assumption II: Students who don't study daily score low.\nA) Only I is implicit\nB) Only II is implicit\nC) Both are implicit\nD) Neither is implicit\nCorrect Answer: A\nExplanation: Assumption I is directly implied by the statement. Assumption II is a stronger claim not necessarily implied.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Statement-Assumption Logic", "target_grade": "9-11"}
        },
        {
            "document": "Question: Is x > y? Statement I: x² > y². Statement II: x and y are both positive.\nA) I alone\nB) II alone\nC) Both together\nD) Neither\nCorrect Answer: C\nExplanation: x²>y² tells us |x|>|y|. Combined with both being positive (Statement II), we can conclude x>y directly.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Data Sufficiency", "target_grade": "9-11"}
        },
        {
            "document": "Question: A cube is painted red on all faces, then cut into 27 equal smaller cubes. How many small cubes have exactly 2 faces painted?\nA) 8\nB) 12\nC) 6\nD) 4\nCorrect Answer: B\nExplanation: Cubes with exactly 2 painted faces sit on edges. A 3×3×3 cube has 12 edges, each contributing 1 such cube. Total = 12.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Spatial Reasoning", "target_grade": "9-11"}
        },

        # === VERBAL ABILITY ===
        {
            "document": "Question: Complete the sentence: 'Despite the heavy rain, she _____ to reach on time.'\nA) managed\nB) manage\nC) has manage\nD) managing\nCorrect Answer: A\nExplanation: Simple past tense 'managed' is correct here as it describes a completed action.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Sentence Completion", "target_grade": "9-11"}
        },
        {
            "document": "Question: What does the idiom 'burn the midnight oil' mean?\nA) Work late into the night\nB) Waste energy\nC) Start a fire\nD) Destroy documents\nCorrect Answer: A\nExplanation: 'Burn the midnight oil' means to work or study late at night.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Common Idioms", "target_grade": "9-11"}
        },
        {
            "document": "Question: Change to passive voice: 'The chef cooked the meal.'\nA) The meal was cooked by the chef.\nB) The meal is cooked by the chef.\nC) The meal has been cooked.\nD) The meal cooked by the chef.\nCorrect Answer: A\nExplanation: Simple past active → simple past passive: 'was cooked by'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Active/Passive Voice", "target_grade": "9-11"}
        },
        {
            "document": "Question: Fill in the blank: 'He is good _____ mathematics.'\nA) in\nB) at\nC) for\nD) with\nCorrect Answer: B\nExplanation: The correct preposition with 'good' when talking about a subject or skill is 'at'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Sentence Completion", "target_grade": "9-11"}
        },
        {
            "document": "Question: What does 'hit the nail on the head' mean?\nA) Do carpentry well\nB) Strike something hard\nC) Be exactly right\nD) Miss the point\nCorrect Answer: C\nExplanation: This idiom means to describe exactly what is causing a situation or problem.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Common Idioms", "target_grade": "9-11"}
        },
        {
            "document": "Question: Spot the error: 'Neither the manager nor the employees was present at the meeting.'\nA) Neither the manager\nB) nor the employees\nC) was present\nD) at the meeting\nCorrect Answer: C\nExplanation: With 'neither…nor', the verb agrees with the noun closest to it — 'employees' (plural). Correct: 'were'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Error Spotting", "target_grade": "9-11"}
        },
        {
            "document": "Question: Analogy — Stethoscope : Doctor :: Gavel : ?\nA) Judge\nB) Lawyer\nC) Jury\nD) Bailiff\nCorrect Answer: A\nExplanation: A stethoscope is the tool of a doctor; a gavel is the tool of a judge.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Analogies", "target_grade": "9-11"}
        },
        {
            "document": "Question: Choose the word closest in meaning to EPHEMERAL.\nA) Eternal\nB) Fleeting\nC) Significant\nD) Robust\nCorrect Answer: B\nExplanation: Ephemeral means lasting for a very short time — synonymous with fleeting.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "GRE/SAT Vocabulary", "target_grade": "9-11"}
        },
        {
            "document": "Question: Spot the error: 'The data clearly shows that the number of cases are increasing.'\nA) The data\nB) clearly shows\nC) the number of cases\nD) are increasing\nCorrect Answer: D\nExplanation: 'The number of' takes a singular verb. Correct: 'is increasing'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Error Spotting", "target_grade": "9-11"}
        },
        {
            "document": "Question: Analogy — Canvas : Painter :: Stage : ?\nA) Audience\nB) Director\nC) Actor\nD) Script\nCorrect Answer: C\nExplanation: A canvas is the medium of a painter; a stage is the medium of an actor.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Analogies", "target_grade": "9-11"}
        },
        {
            "document": "Question: Choose the meaning of TENDENTIOUS as used in a biased report:\nA) Well-researched\nB) Promoting a particular cause\nC) Factually incorrect\nD) Overly long\nCorrect Answer: B\nExplanation: Tendentious means expressing a particular point of view; biased.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Contextual Vocabulary", "target_grade": "9-11"}
        },
        {
            "document": "Question: Rearrange: (P) the committee (Q) after a debate (R) finally approved (S) the policy.\nA) QPRS\nB) PQRS\nC) QRPS\nD) PRQS\nCorrect Answer: A\nExplanation: Logical order: 'After a debate (Q), the committee (P) finally approved (R) the policy (S).'",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Sentence Restructuring", "target_grade": "9-11"}
        },
        {
            "document": "Question: Weakener: 'Banning junk food in schools will improve health.'\nA) Junk food reduces concentration\nB) Students can buy junk food outside school\nC) Healthy food improves energy\nD) Schools have a duty of care\nCorrect Answer: B\nExplanation: If students access it elsewhere, the ban is ineffective, weakening the argument.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Critical Reasoning", "target_grade": "9-11"}
        },
        {
            "document": "Question: Contextual meaning of SANGUINE:\nA) Pessimistic\nB) Confused\nC) Optimistic\nD) Indifferent\nCorrect Answer: C\nExplanation: Sanguine means optimistic, especially in a difficult situation.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Contextual Vocabulary", "target_grade": "9-11"}
        },
        {
            "document": "Question: Strengthener: 'City A has more hospitals, so residents are healthier.'\nA) City A has better roads\nB) Hospital visits in City A are for preventive care\nC) City B has more pharmacies\nD) City A has a younger population\nCorrect Answer: B\nExplanation: Preventive care visits support the claim that residents are proactively healthy.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Critical Reasoning", "target_grade": "9-11"}
        }
    ]

def run_migration():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        print("✅ Connected. Migrating 45 reformatted questions...")

        questions = get_formatted_questions()
        query = "INSERT INTO langchain_pg_embedding (id, document, cmetadata) VALUES (%s, %s, %s)"

        for i, q in enumerate(questions, 1):
            cur.execute(query, (str(uuid.uuid4()), q["document"], json.dumps(q["metadata"])))
        
        conn.commit()
        print(f"✅ Success! {len(questions)} questions migrated in the correct format.")
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    run_migration()