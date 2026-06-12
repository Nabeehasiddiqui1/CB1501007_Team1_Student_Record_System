import json
import os

from academic_error import AcademicError
from student import Student
from course import Course
from record_system import RecordSystem


DATA_FOLDER = "data"
STUDENTS_FILE = os.path.join(DATA_FOLDER, "students.json")
COURSES_FILE = os.path.join(DATA_FOLDER, "courses.json")


# ---------- File I/O ----------

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


# ---------- Bonus: Export Transcript ----------

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


# ---------- Menu Display ----------

def show_menu():
    print("\n===== Student Record System =====")
    print("1. Add Student")
    print("2. Edit Student")
    print("3. Delete Student")
    print("4. Add Course")
    print("5. Edit Course")
    print("6. Delete Course")
    print("7. Enroll Student")
    print("8. Record Grade")
    print("9. Show Transcript")
    print("10. Show Ranking")
    print("11. Show Analytics")
    print("12. Search")
    print("13. Save")
    print("14. Load")
    print("15. Export Transcript to TXT")
    print("0. Exit")


# ---------- Menu Actions ----------

def add_student_action(system):
    name = input("Name: ").strip()
    sid = input("Student ID: ").strip()
    major = input("Major: ").strip()
    year = int(input("Year: "))

    system.add_student(name, sid, major, year)
    auto_save(system)
    print("Student added.")


def edit_student_action(system):
    sid = input("Student ID to edit: ").strip()
    name = input("New name: ").strip()
    major = input("New major: ").strip()
    year = int(input("New year: "))

    system.edit_student(sid, name, major, year)
    auto_save(system)
    print("Student edited.")


def delete_student_action(system):
    sid = input("Student ID to delete: ").strip()

    system.delete_student(sid)
    auto_save(system)
    print("Student deleted.")


def add_course_action(system):
    code = input("Course code: ").strip()
    name = input("Course name: ").strip()
    credits = int(input("Credits: "))
    capacity = int(input("Capacity: "))

    system.add_course(code, name, credits, capacity)
    auto_save(system)
    print("Course added.")


def edit_course_action(system):
    code = input("Course code to edit: ").strip()
    name = input("New course name: ").strip()
    credits = int(input("New credits: "))
    capacity = int(input("New capacity: "))

    system.edit_course(code, name, credits, capacity)
    auto_save(system)
    print("Course edited.")


def delete_course_action(system):
    code = input("Course code to delete: ").strip()

    system.delete_course(code)
    auto_save(system)
    print("Course deleted.")


def enroll_student_action(system):
    sid = input("Student ID: ").strip()
    code = input("Course code: ").strip()

    system.enroll(sid, code)
    auto_save(system)
    print("Student enrolled.")


def record_grade_action(system):
    sid = input("Student ID: ").strip()
    code = input("Course code: ").strip()
    grade = input("Grade A+/A/B+/B/C+/C/D/F: ").strip()

    system.record_grade(sid, code, grade)
    auto_save(system)
    print("Grade recorded.")


def show_transcript_action(system):
    sid = input("Student ID: ").strip()

    if sid not in system.students:
        print("Student not found.")
        return

    print(system.students[sid].transcript(system.courses))


def show_ranking_action(system):
    ranking = system.calculate_ranking()

    print("\n===== Ranking =====")

    if not ranking:
        print("No graded students yet.")
        return

    for rank, student_info in enumerate(ranking, start=1):
        print(rank, student_info)


def show_analytics_action(system):
    analytics = system.analytics()

    print("\n===== Analytics =====")
    print(analytics)


def search_action(system):
    keyword = input("Search keyword: ").strip()
    results = system.find(keyword)

    print("\n===== Search Results =====")

    if not results:
        print("No results found.")
        return

    for result in results:
        print(result)


# ---------- Main Program ----------

def main():
    system = RecordSystem()
    load_data(system)

    while True:
        show_menu()
        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                add_student_action(system)

            elif choice == "2":
                edit_student_action(system)

            elif choice == "3":
                delete_student_action(system)

            elif choice == "4":
                add_course_action(system)

            elif choice == "5":
                edit_course_action(system)

            elif choice == "6":
                delete_course_action(system)

            elif choice == "7":
                enroll_student_action(system)

            elif choice == "8":
                record_grade_action(system)

            elif choice == "9":
                show_transcript_action(system)

            elif choice == "10":
                show_ranking_action(system)

            elif choice == "11":
                show_analytics_action(system)

            elif choice == "12":
                search_action(system)

            elif choice == "13":
                save_data(system)

            elif choice == "14":
                load_data(system)

            elif choice == "15":
                export_transcript(system)

            elif choice == "0":
                save_data(system)
                print("Goodbye.")
                break

            else:
                print("Invalid option. Try again.")

        except AcademicError as error:
            print(f"Academic Error: {error}")

        except ValueError:
            print("Input Error: Please enter a valid number.")

        except Exception as error:
            print(f"Unexpected Error: {error}")


if __name__ == "__main__":
    main()