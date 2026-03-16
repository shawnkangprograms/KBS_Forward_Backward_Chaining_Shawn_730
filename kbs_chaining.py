"""
Course Eligibility Expert System
Forward & Backward Chaining — Knowledge-Based Systems
"""

# ── Knowledge Base ─────────────────────────────────────────

class Student:
    def __init__(self, name, courses, gpa):
        self.name = name
        self.courses = set(courses)
        self.gpa = gpa

RULES = [
    {"id": 1, "desc": "Prog I + Math I → Data Structures",
     "prereqs": ["Programming I", "Mathematics I"],
     "conclusion": "Eligible: Data Structures"},

    {"id": 2, "desc": "Data Structures + Comp Org → Algorithms",
     "prereqs": ["Eligible: Data Structures", "Computer Organization"],
     "conclusion": "Eligible: Algorithms"},

    {"id": 3, "desc": "Prog I + Statistics → Machine Learning",
     "prereqs": ["Programming I", "Statistics"],
     "conclusion": "Eligible: Machine Learning"},

    {"id": 4, "desc": "GPA < 2.5 → Advanced courses blocked",
     "prereqs": [],
     "gpa_check": lambda g: g < 2.5,
     "conclusion": "BLOCKED: Advanced Courses"},

    {"id": 5, "desc": "Algorithms + GPA ≥ 3.0 → Advanced AI",
     "prereqs": ["Eligible: Algorithms"],
     "gpa_check": lambda g: g >= 3.0,
     "conclusion": "Eligible: Advanced AI"},

    {"id": 6, "desc": "Machine Learning + GPA ≥ 3.0 → Deep Learning",
     "prereqs": ["Eligible: Machine Learning"],
     "gpa_check": lambda g: g >= 3.0,
     "conclusion": "Eligible: Deep Learning"},

    {"id": 7, "desc": "Database Systems + Algorithms → Software Eng",
     "prereqs": ["Database Systems", "Eligible: Algorithms"],
     "conclusion": "Eligible: Software Engineering"},
]

def conditions_met(rule, student, facts):
    blocked = "BLOCKED: Advanced Courses" in facts
    if blocked and rule["conclusion"] in ("Eligible: Advanced AI", "Eligible: Deep Learning"):
        return False
    prereqs_ok = all(p in facts for p in rule["prereqs"])
    gpa_ok = rule["gpa_check"](student.gpa) if "gpa_check" in rule else True
    return prereqs_ok and gpa_ok


# ── Forward Chaining ───────────────────────────────────────

def forward_chain(student):
    facts = set(student.courses)
    print(f"\n{'='*55}")
    print(f"FORWARD CHAINING — {student.name}")
    print(f"Courses: {', '.join(sorted(student.courses))}  |  GPA: {student.gpa}")
    print("-" * 55)

    while True:
        new = set()
        for rule in RULES:
            if rule["conclusion"] not in facts and conditions_met(rule, student, facts):
                new.add(rule["conclusion"])
                print(f"  Rule {rule['id']} fired → {rule['conclusion']}")
        if not new:
            break
        facts |= new

    eligible = sorted(f for f in facts if f.startswith("Eligible:"))
    print(f"\nFinal: {', '.join(eligible) or 'None'}")
    if "BLOCKED: Advanced Courses" in facts:
        print("  Low GPA — advanced courses blocked.")
    print("=" * 55)
    return facts


# ── Backward Chaining ──────────────────────────────────────

def backward_chain(goal, student, facts, depth=0, visited=None):
    visited = visited or set()
    pad = "  " * depth

    if goal in facts:
        print(f"{pad} '{goal}' already known.")
        return True
    if goal in visited:
        return False
    visited.add(goal)

    for rule in [r for r in RULES if r["conclusion"] == goal]:
        print(f"{pad}? Rule {rule['id']}: {rule['desc']}")
        temp = set(facts)
        ok = all(
            backward_chain(p, student, temp, depth + 1, visited) or temp.add(p) or p in temp
            for p in rule["prereqs"]
        )
        gpa_ok = rule["gpa_check"](student.gpa) if "gpa_check" in rule else True
        if ok and gpa_ok:
            print(f"{pad} PROVED '{goal}'")
            return True

    print(f"{pad} Cannot prove '{goal}'")
    return False

def query(goal, student, facts):
    full_goal = f"Eligible: {goal}"
    print(f"\n{'='*55}")
    print(f"BACKWARD CHAINING — Is {student.name} eligible for {goal}?")
    print("-" * 55)
    result = backward_chain(full_goal, student, set(student.courses))
    print("-" * 55)
    print(f"RESULT: {'PROVED' if result else 'NOT PROVED'}")
    print("=" * 55)


# ── Test Cases ─────────────────────────────────────────────

test_data = [
    (Student("Alice", ["Programming I", "Statistics", "Mathematics I", "Computer Organization"], 3.2),
     ["Machine Learning", "Algorithms", "Advanced AI"]),
    (Student("Bob",   ["Programming I", "Mathematics I", "Computer Organization", "Database Systems"], 2.1),
     ["Data Structures", "Algorithms", "Advanced AI"]),
    (Student("Carol", ["Programming I", "Statistics", "Mathematics I", "Computer Organization", "Database Systems"], 3.7),
     ["Deep Learning", "Software Engineering", "Advanced AI"]),
]

for student, qs in test_data:
    facts = forward_chain(student)
    for q in qs:
        query(q, student, facts)


# ── Interactive Mode (Bonus) ───────────────────────────────

print("\n" + "-" * 55)
if input("Run interactive mode? (y/n): ").strip().lower() == "y":
    name = input("Name: ").strip()
    courses = [c.strip() for c in input("Completed courses (comma-separated): ").split(",")]
    gpa = float(input("GPA: ").strip())
    s = Student(name, courses, gpa)
    f = forward_chain(s)
    query(input("Query course: ").strip(), s, f)
