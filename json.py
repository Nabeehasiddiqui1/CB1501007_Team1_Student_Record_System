import json
from academic_error import AcademicError
from student import Student
from course import Course
from record_system import RecordSystem


# ---------- Member 6: File I/O Helper ----------

def save_data(system, filename="record_system.json"):
    data = {
        "students": {
            sid: student.to_dict()
            for sid, student in system.students.items()
        },
        "courses": {
            code: course.to_dict()
            for code, course in system.courses.items()
        }
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully.")


def load_data(system, filename="record_system.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        system.students = {
            sid: Student.from_dict(student_data)
            for sid, student_data in data.get("students", {}).items()
        }

        system.courses = {
            code: Course.from_dict(course_data)
            for code, course_data in data.get("courses", {}).items()
        }

        print("Data loaded successfully.")

    except FileNotFoundError:
        print("No saved file found. Starting with empty data.")
        system.students = {}
        system.courses = {}

    except json.JSONDecodeError:
        print("Saved file is corrupted. Starting with empty data.")
        system.students = {}
        system.courses = {}


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


# ---------- Menu System ----------

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


def main():
    system = RecordSystem()
    load_data(system)

    while True:
        show_menu()
        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                name = input("Name: ").strip()
                sid = input("Student ID: ").strip()
                major = input("Major: ").strip()
                year = int(input("Year: "))

                system.add_student(name, sid, major, year)
                auto_save(system)
                print("Student added.")

            elif choice == "2":
                sid = input("Student ID to edit: ").strip()
                name = input("New name: ").strip()
                major = input("New major: ").strip()
                year = int(input("New year: "))

                system.edit_student(sid, name, major, year)
                auto_save(system)
                print("Student edited.")

            elif choice == "3":
                sid = input("Student ID to delete: ").strip()

                system.delete_student(sid)
                auto_save(system)
                print("Student deleted.")

            elif choice == "4":
                code = input("Course code: ").strip()
                name = input("Course name: ").strip()
                credits = int(input("Credits: "))
                capacity = int(input("Capacity: "))

                system.add_course(code, name, credits, capacity)
                auto_save(system)
                print("Course added.")

            elif choice == "5":
                code = input("Course code to edit: ").strip()
                name = input("New course name: ").strip()
                credits = int(input("New credits: "))
                capacity = int(input("New capacity: "))

                system.edit_course(code, name, credits, capacity)
                auto_save(system)
                print("Course edited.")

            elif choice == "6":
                code = input("Course code to delete: ").strip()

                system.delete_course(code)
                auto_save(system)
                print("Course deleted.")

            elif choice == "7":
                sid = input("Student ID: ").strip()
                code = input("Course code: ").strip()

                system.enroll(sid, code)
                auto_save(system)
                print("Student enrolled.")

            elif choice == "8":
                sid = input("Student ID: ").strip()
                code = input("Course code: ").strip()
                grade = input("Grade A+/A/B+/B/C+/C/D/F: ").strip()

                system.record_grade(sid, code, grade)
                auto_save(system)
                print("Grade recorded.")

            elif choice == "9":
                sid = input("Student ID: ").strip()

                if sid in system.students:
                    print(system.students[sid].transcript(system.courses))
                else:
                    print("Student not found.")

            elif choice == "10":
                ranking = system.calculate_ranking()

                print("\n===== Ranking =====")
                for rank, student_info in enumerate(ranking, start=1):
                    print(rank, student_info)

            elif choice == "11":
                analytics = system.analytics()

                print("\n===== Analytics =====")
                print(analytics)

            elif choice == "12":
                keyword = input("Search keyword: ").strip()
                results = system.find(keyword)

                print("\n===== Search Results =====")
                if not results:
                    print("No results found.")
                else:
                    for result in results:
                        print(result)

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