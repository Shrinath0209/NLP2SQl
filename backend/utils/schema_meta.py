SCHEMA_META = {
    "students": {
        "description": "contains student information including personal and academic details",
        "columns": {
            "id": "unique student identifier",
            "name": "student full name",
            "department": "department or branch of study like CSE ECE",
            "cgpa": "cumulative grade point average academic score",
            "attendance": "attendance percentage how often student attends class",
            "semester": "current semester number"
        }
    },
    "marks": {
        "description": "contains subject wise marks scores grades for students",
        "columns": {
            "student_id": "references student id",
            "subject": "subject name or course name",
            "marks": "marks obtained score in the subject",
            "semester": "semester number"
        }
    },
    "courses": {
        "description": "contains course information subjects offered",
        "columns": {
            "course_id": "unique course identifier",
            "course_name": "name of the course or subject",
            "faculty": "teacher professor who teaches the course",
            "credits": "credit hours of the course"
        }
    }
}

SYNONYMS = {
    "kids": "students",
    "score": "marks",
    "grade": "marks",
    "grades": "marks",
    "teacher": "faculty",
    "professor": "faculty",
    "branch": "department",
    "gpa": "cgpa",
    "percentage": "attendance",
    "subject": "course_name",
    "top": "ORDER BY DESC LIMIT",
    "bottom": "ORDER BY ASC LIMIT",
    "lowest": "ORDER BY ASC",
    "highest": "ORDER BY DESC",
    "low": "less than",
    "high": "greater than",
    "below": "less than",
    "above": "greater than",
    "pass": "marks >= 50",
    "fail": "marks < 50"
}
