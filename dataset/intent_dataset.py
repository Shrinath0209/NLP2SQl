"""
Labeled NL→SQL Intent Dataset
56 examples, 8 per intent class (7 classes)
Used to fine-tune MiniLM classification head.
"""

INTENT_LABELS = ["COUNT", "AVERAGE", "TOP_N", "BOTTOM_N", "FILTER_LT", "FILTER_GT", "SELECT"]

LABEL2ID = {label: idx for idx, label in enumerate(INTENT_LABELS)}
ID2LABEL = {idx: label for idx, label in enumerate(INTENT_LABELS)}

DATASET = [
    # ── COUNT (0) ──
    ("how many students are there", "COUNT"),
    ("count all students in the database", "COUNT"),
    ("what is the total number of students", "COUNT"),
    ("how many courses are available", "COUNT"),
    ("give me a count of all marks records", "COUNT"),
    ("total number of students enrolled", "COUNT"),
    ("how many students are in CSE", "COUNT"),
    ("count students in semester 6", "COUNT"),

    # ── AVERAGE (1) ──
    ("what is the average cgpa of students", "AVERAGE"),
    ("find the mean attendance of all students", "AVERAGE"),
    ("average marks in maths", "AVERAGE"),
    ("what is the avg score across all subjects", "AVERAGE"),
    ("calculate average cgpa for ECE students", "AVERAGE"),
    ("mean marks obtained in semester 5", "AVERAGE"),
    ("average attendance percentage", "AVERAGE"),
    ("what is the average credits per course", "AVERAGE"),

    # ── TOP_N (2) ──
    ("show top 5 students by cgpa", "TOP_N"),
    ("list highest scoring students", "TOP_N"),
    ("who are the best students by attendance", "TOP_N"),
    ("top 10 students ranked by marks", "TOP_N"),
    ("show maximum cgpa students", "TOP_N"),
    ("best 3 courses by credits", "TOP_N"),
    ("highest attendance students", "TOP_N"),
    ("top performers in the database", "TOP_N"),

    # ── BOTTOM_N (3) ──
    ("show bottom 5 students by cgpa", "BOTTOM_N"),
    ("list lowest scoring students", "BOTTOM_N"),
    ("who has the worst attendance", "BOTTOM_N"),
    ("bottom 10 students by marks", "BOTTOM_N"),
    ("minimum cgpa students", "BOTTOM_N"),
    ("lowest 3 performers", "BOTTOM_N"),
    ("worst attendance in the class", "BOTTOM_N"),
    ("students with the least marks", "BOTTOM_N"),

    # ── FILTER_LT (4) ──
    ("students with attendance below 75", "FILTER_LT"),
    ("show students with cgpa less than 6", "FILTER_LT"),
    ("students under 7 cgpa", "FILTER_LT"),
    ("marks less than 50", "FILTER_LT"),
    ("students with low attendance", "FILTER_LT"),
    ("find students below average cgpa", "FILTER_LT"),
    ("students with marks under 40", "FILTER_LT"),
    ("attendance below 60 percent", "FILTER_LT"),

    # ── FILTER_GT (5) ──
    ("students with cgpa above 8", "FILTER_GT"),
    ("show students with attendance more than 90", "FILTER_GT"),
    ("marks greater than 80", "FILTER_GT"),
    ("students over 9 cgpa", "FILTER_GT"),
    ("high attendance students above 85", "FILTER_GT"),
    ("students with marks above 70", "FILTER_GT"),
    ("cgpa greater than 7.5", "FILTER_GT"),
    ("attendance more than 80 percent", "FILTER_GT"),

    # ── SELECT (6) ──
    ("show all CSE students", "SELECT"),
    ("list students in ECE department", "SELECT"),
    ("get all courses", "SELECT"),
    ("show me all students", "SELECT"),
    ("display student details", "SELECT"),
    ("fetch all marks records", "SELECT"),
    ("show students in semester 3", "SELECT"),
    ("list all courses offered", "SELECT"),
]
