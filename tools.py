"""
tools.py - all the CGPA Guider tools (plain python functions).
FastMCP reads the docstring + type hints of each function and shows them to the model.
"""

# credit hours of every semester of the BS Software Engineering degree
CREDIT_HOURS = {1: 17, 2: 18, 3: 18, 4: 18, 5: 19, 6: 18, 7: 16, 8: 15}

# grade -> grade points (4.0 scale)
GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.67,
    "B+": 3.33, "B": 3.0, "B-": 2.67,
    "C+": 2.33, "C": 2.0, "C-": 1.67,
    "D+": 1.33, "D": 1.0, "F": 0.0,
}


def get_credit_hours(semesters: list[int]) -> float:
    """Return the total credit hours of the given semesters.
    Example: semesters=[5, 6] gives 37.0. Semester numbers go from 1 to 8."""
    total = 0.0
    for s in semesters:
        if s not in CREDIT_HOURS:
            raise ValueError(f"Semester {s} does not exist. Use numbers from 1 to 8.")
        total += CREDIT_HOURS[s]
    return total


def grade_to_points(grade: str) -> float:
    """Convert a letter grade (like A, B+, C-) into grade points on the 4.0 scale."""
    g = grade.strip().upper()
    if g not in GRADE_POINTS:
        raise ValueError(f"Unknown grade '{grade}'. Valid grades: {', '.join(GRADE_POINTS)}")
    return GRADE_POINTS[g]


def calculate_cgpa(completed_credits: float, current_cgpa: float,
                   semester_credits: float, semester_gpa: float) -> float:
    """Calculate the new CGPA after adding one more semester.
    completed_credits = credit hours done so far, current_cgpa = CGPA so far,
    semester_credits = credit hours of the new semester, semester_gpa = GPA got in it."""
    if completed_credits < 0 or semester_credits <= 0:
        raise ValueError("Credit hours must be positive.")
    total_points = completed_credits * current_cgpa + semester_credits * semester_gpa
    total_credits = completed_credits + semester_credits
    return round(total_points / total_credits, 2)


def required_gpa(completed_credits: float, current_cgpa: float,
                 target_cgpa: float, upcoming_credits: float) -> float:
    """GPA the student must score in the upcoming credit hours to reach target_cgpa.
    If the answer is more than 4.0 then the target cannot be reached in that window."""
    if upcoming_credits <= 0:
        raise ValueError("Upcoming credits must be more than 0.")
    needed_points = target_cgpa * (completed_credits + upcoming_credits)
    have_points = completed_credits * current_cgpa
    return round((needed_points - have_points) / upcoming_credits, 2)


def check_target(completed_credits: float, current_cgpa: float,
                 target_cgpa: float, current_semester: int) -> dict:
    """Check if target_cgpa is possible. It starts with only the next semester, then
    widens the window to the next 2 and then 3 semesters (max 3 tries) and tells
    the required GPA for each window. current_semester = semesters already finished."""
    results = []
    for window in (1, 2, 3):
        sems = [s for s in range(current_semester + 1, current_semester + 1 + window) if s <= 8]
        if not sems:
            break
        credits = get_credit_hours(sems)
        need = required_gpa(completed_credits, current_cgpa, target_cgpa, credits)
        results.append({
            "semesters": sems,
            "credit_hours": credits,
            "required_gpa": need,
            "possible": need <= 4.0,
        })
        if need <= 4.0:
            break  # found a window that works, no need to widen more
    return {"target_cgpa": target_cgpa, "tries": results}
