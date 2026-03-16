# KBS_Forward_Backward_Chaining_Njoroge_730

**Course Eligibility Expert System** — Demonstrating Forward and Backward Chaining in a Rule-Based Knowledge-Based System (KBS) built entirely in Python.

## Table of Contents

1. [Problem Description](#1-problem-description)
2. [Facts](#2-facts)
3. [Rules](#3-rules)
4. [How Forward Chaining Works](#4-how-forward-chaining-works)
5. [How Backward Chaining Works](#5-how-backward-chaining-works)
6. [How to Run](#6-how-to-run)
7. [Sample Outputs](#7-sample-outputs)
8. [File Structure](#8-file-structure)

## 1. Problem Description

This system determines whether a university student is eligible to enrol in specific courses based on:

- Courses they have already **completed**
- Their current **GPA**
- A set of **inference rules** that model academic prerequisites

Two reasoning strategies are implemented from scratch (no external AI libraries):

| Strategy | Approach | Trigger |
|----------|----------|---------|
| **Forward Chaining** | Data-driven — derive all possible conclusions from known facts | Run automatically for every student |
| **Backward Chaining** | Goal-driven — prove or disprove a specific eligibility goal | Run for specific course queries |


## 2. Facts

Facts are stored using two Python structures:

### `Student` class (custom class)
```python
Student(
    name: str,               # Student's name
    completed_courses: set,  # Courses already passed (stored as a set)
    gpa: float               # Current GPA on a 0.0–4.0 scale
)
```

### Dynamic fact set (`set[str]`)
During inference, a `set` accumulates all known facts — starting from completed courses and growing as rules fire. Examples of facts in the set:

```
"Programming I"
"Mathematics I"
"Eligible for Data Structures"
"Eligible for Algorithms"
"Not eligible for advanced courses"
```

## 3. Rules

Seven rules are defined. Each rule has:
- A unique **ID** and **description**
- A **condition** (a callable that checks student facts)
- A **conclusion** (a new fact string to add if conditions are met)

| Rule | Antecedents | Conclusion |
|------|-------------|------------|
| 1 | Programming I **AND** Mathematics I | Eligible for Data Structures |
| 2 | Eligible for Data Structures **AND** Computer Organization | Eligible for Algorithms |
| 3 | Programming I **AND** Statistics | Eligible for Machine Learning Basics |
| 4 | GPA < 2.5 | Not eligible for advanced courses |
| 5 | Eligible for Algorithms **AND** GPA ≥ 3.0 **AND** no low-GPA flag | Eligible for Advanced AI |
| 6 | Database Systems **AND** Eligible for Algorithms | Eligible for Software Engineering |
| 7 | Eligible for Machine Learning Basics **AND** GPA ≥ 3.0 **AND** no low-GPA flag | Eligible for Deep Learning |

Rules are stored as a list of dictionaries, making the knowledge base easy to extend.

## 4. How Forward Chaining Works

**Algorithm — iterative, data-driven breadth-first derivation:**

```
1. Initialise known_facts with the student's completed courses.
2. Repeat:
   a. For every rule in RULES:
      - If the rule's conclusion is NOT yet in known_facts:
        * Evaluate the rule's conditions against (student, known_facts).
        * If conditions are met → add conclusion to new_facts_this_round
                                  and print which rule fired.
   b. If new_facts_this_round is empty → STOP (fixed point reached).
   c. Otherwise → merge new_facts_this_round into known_facts and loop.
3. Report all facts whose string starts with "Eligible for".
```

Key properties:
- **Automated and iterative** — no manual triggering of individual rules.
- **Monotonic** — facts are only ever added, never removed.
- **Terminates** — stops when no new facts are derivable (fixed point).
- Handles **chained dependencies** (e.g., Rule 2 depends on the conclusion of Rule 1).

## 5. How Backward Chaining Works

**Algorithm — recursive, goal-driven depth-first search:**

```
backward_chain(goal, student, known_facts):
  1. If goal ∈ known_facts → return TRUE  (base case: already known)
  2. If goal ∈ visited    → return FALSE  (cycle guard)
  3. Mark goal as visited.
  4. Find all rules whose conclusion matches goal.
  5. For each such rule:
     a. Collect the rule's prerequisite sub-goals.
     b. For each sub-goal: recursively call backward_chain(sub-goal, …)
        - If proved → treat as known for this branch.
        - If not proved → this rule fails; try next rule.
     c. Evaluate any numeric/GPA conditions for the rule.
     d. If all sub-goals and numeric conditions pass → return TRUE.
  6. If no rule could prove the goal → return FALSE.
```

Key properties:
- **Recursive** — naturally mirrors the depth-first proof search.
- **Traced output** — every attempted rule and sub-goal is printed with indentation showing the reasoning tree.
- **Cycle detection** — a `visited` set prevents infinite loops.
- Returns `PROVED` or `NOT PROVED` with a full explanation trace.

## 6. How to Run

### Requirements
- Python **3.10 or later** (uses `set[str]` and `list[str]` type hints)
- No third-party packages required

### Run the script

```bash
python kbs_chaining.py
```

The program will automatically run **three test cases** and print both Forward and Backward Chaining results for each.

At the end you will be asked:
```
Run interactive mode? (y/n):
```

Type `y` to enter your own student details and query a specific course.

### Interactive mode example

```
Enter student name: Sam
Available courses: 1. Programming I  2. Mathematics I  3. Statistics ...
Enter course numbers: 1, 2, 3
Enter GPA: 3.5
Enter a course to query eligibility for: Data Structures
```

## 7. Sample Outputs

### Alice — GPA 3.2 | Completed: Programming I, Statistics, Mathematics I, Computer Organization

**Forward Chaining:**
```
Rule 1 fired : Programming I + Mathematics I → Data Structures
  → New fact inferred : Eligible for Data Structures
Rule 3 fired : Programming I + Statistics → Machine Learning Basics
  → New fact inferred : Eligible for Machine Learning Basics
Rule 2 fired : Data Structures + Computer Organization → Algorithms
  → New fact inferred : Eligible for Algorithms
Rule 7 fired : Machine Learning Basics + GPA ≥ 3.0 → Deep Learning
  → New fact inferred : Eligible for Deep Learning
Rule 5 fired : Algorithms + GPA ≥ 3.0 → Advanced AI
  → New fact inferred : Eligible for Advanced AI

Final Eligible Courses:
   Eligible for Advanced AI
   Eligible for Algorithms
   Eligible for Data Structures
   Eligible for Deep Learning
   Eligible for Machine Learning Basics
```

**Backward Chaining — "Is Alice eligible for Machine Learning Basics?":**
```
Trying Rule 3 : Programming I + Statistics → Machine Learning Basics
  Sub-goal: prove 'Programming I'  -> already known.
  Sub-goal: prove 'Statistics'     -> already known.
Rule 3 PROVED 'Eligible for Machine Learning Basics'.

RESULT : PROVED – Alice IS eligible for Machine Learning Basics.
```


### Bob — GPA 2.1 | Completed: Programming I, Mathematics I, Computer Organization, Database Systems

**Forward Chaining:**
```
Rule 1 fired → Eligible for Data Structures
Rule 4 fired → Not eligible for advanced courses  (GPA < 2.5)
Rule 2 fired → Eligible for Algorithms
Rule 6 fired → Eligible for Software Engineering

Low GPA flag active – advanced courses blocked.
```

**Backward Chaining — "Is Bob eligible for Advanced AI?":**
```
Trying Rule 5 …
  [sub-goals proved, but numeric GPA check fails]
Rule 5 failed.

RESULT : NOT PROVED – Bob is NOT eligible for Advanced AI.
```


## 8. File Structure

```
KBS_Forward_Backward_Chaining_[LastName]_[ID]/
├── kbs_chaining.py   # Main source file — all logic
└── README.md         # This file
```

---

*Written for the Knowledge-Based Systems practical assignment.
All inference logic is implemented from scratch using only Python built-ins.*
