import json
import os

from student import Student
from course import Course


DATA_FOLDER = "data"
STUDENTS_FILE = os.path.join(DATA_FOLDER, "students.json")
COURSES_FILE = os.path.join(DATA_FOLDER, "courses.json")


def save_data(system):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    students_data = {
        sid: student.to_dict()
        for sid, student in system.students.items()
    }

    courses_data = {
        code: course.to_dict()
        for code, course in system.courses.items()
    }

    with open(STUDENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(students_data, file, indent=4)

    with open(COURSES_FILE, "w", encoding="utf-8") as file:
        json.dump(courses_data, file, indent=4)

    print("Data saved successfully.")


def load_data(system):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    system.students = load_students()
    system.courses = load_courses()

    print("Data loaded successfully.")


def load_students():
    try:
        with open(STUDENTS_FILE, "r", encoding="utf-8") as file:
            students_data = json.load(file)

        return {
            sid: Student.from_dict(student_data)
            for sid, student_data in students_data.items()
        }

    except FileNotFoundError:
        print("students.json not found. Starting with empty students.")
        return {}

    except json.JSONDecodeError:
        print("students.json is corrupted. Starting with empty students.")
        return {}


def load_courses():
    try:
        with open(COURSES_FILE, "r", encoding="utf-8") as file:
            courses_data = json.load(file)

        return {
            code: Course.from_dict(course_data)
            for code, course_data in courses_data.items()
        }

    except FileNotFoundError:
        print("courses.json not found. Starting with empty courses.")
        return {}

    except json.JSONDecodeError:
        print("courses.json is corrupted. Starting with empty courses.")
        return {}


def auto_save(system):
    save_data(system)


def export_transcript(system):
    sid = input("Student ID: ").strip()

    if sid not in system.students:
        print("Student not found.")
        return

    transcript = system.students[sid].transcript(system.courses)
    filename = f"transcript_{sid}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(transcript)

    print(f"Transcript exported to {filename}")