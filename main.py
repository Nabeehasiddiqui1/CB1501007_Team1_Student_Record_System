import sys
from record_system import RecordSystem
from academic_error import AcademicError


def print_menu():
    print("\n" + "=" * 60)
    print("STUDENT RECORD SYSTEM")
    print("=" * 60)
    print("1. Add Student")
    print("2. Add Course")
    print("3. Enroll Student in Course")
    print("4. Record Grade")
    print("5. View Transcript")
    print("6. View Class Ranking")
    print("7. View Academic Analytics Report")
    print("8. Search Students")
    print("9. Search Courses")
    print("10. Delete Student")
    print("11. Delete Course")
    print("12. List All Students")
    print("13. List All Courses")
    print("14. Save Data")
    print("15. Load Data")
    print("0. Exit")
    print("-" * 60)


def add_student(system):
    print("\n--- ADD NEW STUDENT ---")
    try:
        name = input("Enter student name: ").strip().title()
        student_id = input("Enter student ID: ").strip()
        major = input("Enter major: ").strip().title()
        year = input("Enter year (Freshman/Sophomore/Junior/Senior): ").strip().capitalize()
        system.add_student(name, student_id, major, year)
    except AcademicError as e:
        print(f"Error: {e}")


def add_course(system):
    print("\n--- ADD NEW COURSE ---")
    try:
        code = input("Enter course code: ").strip().upper()
        name = input("Enter course name: ").strip().title()
        credits = int(input("Enter credits (1-6): "))
        capacity = int(input("Enter maximum capacity: "))
        system.add_course(code, name, credits, capacity)
    except AcademicError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: Credits and capacity must be numbers")


def enroll_student(system):
    print("\n--- ENROLL STUDENT IN COURSE ---")
    try:
        student_id = input("Enter student ID: ").strip()
        course_code = input("Enter course code: ").strip().upper()
        system.enroll_student(student_id, course_code)
    except AcademicError as e:
        print(f"Error: {e}")


def record_grade(system):
    print("\n--- RECORD GRADE ---")
    try:
        student_id = input("Enter student ID: ").strip()
        course_code = input("Enter course code: ").strip().upper()
        print("Valid grades: A+, A, B+, B, C+, C, D, F")
        grade = input("Enter grade: ").strip().upper()
        system.record_grade(student_id, course_code, grade)
    except AcademicError as e:
        print(f"Error: {e}")


def view_transcript(system):
    print("\n--- VIEW TRANSCRIPT ---")
    try:
        student_id = input("Enter student ID: ").strip()
        student = system.get_student_by_id(student_id)
        if not student:
            print("Student not found.")
            return
        print(student.transcript(system.courses))
    except Exception as e:
        print(f"Error: {e}")


def view_ranking(system):
    print("\n--- CLASS RANKING ---")
    ranking = system.calculate_ranking()
    if not ranking:
        print("No students with completed courses yet.")
        return
    print("\n" + "-" * 50)
    print(f"{'Rank':<6} {'Name':<20} {'ID':<12} {'GPA':<6}")
    print("-" * 50)
    for i, (student, gpa) in enumerate(ranking, 1):
        print(f"{i:<6} {student.name:<20} {student.sid:<12} {gpa:<6.2f}")
    print("-" * 50)


def view_analytics(system):
    system.print_analytics_report()


def search_students(system):
    print("\n--- SEARCH STUDENTS ---")
    print("Search by: 1. Name  2. ID  3. Major")
    try:
        choice = input("Enter choice: ").strip()
        search_map = {'1': 'name', '2': 'id', '3': 'major'}
        if choice not in search_map:
            print("Invalid choice")
            return
        keyword = input("Enter keyword: ").strip()
        results = system.search_students(keyword, search_map[choice])
        if not results:
            print("No students found.")
            return
        print(f"\nFound {len(results)} student(s):")
        for student in results:
            print(f"  {student.name} (ID: {student.sid}) - {student.major}")
    except Exception as e:
        print(f"Error: {e}")


def search_courses(system):
    print("\n--- SEARCH COURSES ---")
    print("Search by: 1. Name  2. Code")
    try:
        choice = input("Enter choice: ").strip()
        search_map = {'1': 'name', '2': 'code'}
        if choice not in search_map:
            print("Invalid choice")
            return
        keyword = input("Enter keyword: ").strip()
        results = system.search_courses(keyword, search_map[choice])
        if not results:
            print("No courses found.")
            return
        print(f"\nFound {len(results)} course(s):")
        for course in results:
            print(f"  {course.code}: {course.name} ({course.credits} credits)")
    except Exception as e:
        print(f"Error: {e}")


def delete_student(system):
    print("\n--- DELETE STUDENT ---")
    try:
        student_id = input("Enter student ID to delete: ").strip()
        confirm = input(f"Delete student {student_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            system.delete_student(student_id)
    except AcademicError as e:
        print(f"Error: {e}")


def delete_course(system):
    print("\n--- DELETE COURSE ---")
    try:
        course_code = input("Enter course code to delete: ").strip().upper()
        confirm = input(f"Delete course {course_code}? (y/n): ").strip().lower()
        if confirm == 'y':
            system.delete_course(course_code)
    except AcademicError as e:
        print(f"Error: {e}")


def list_all_students(system):
    print("\n--- ALL STUDENTS ---")
    if not system.students:
        print("No students in the system.")
        return
    print("-" * 60)
    print(f"{'ID':<12} {'Name':<20} {'Major':<15} {'Year':<10}")
    print("-" * 60)
    for student in system.students.values():
        print(f"{student.sid:<12} {student.name:<20} {student.major:<15} {student.year:<10}")
    print("-" * 60)
    print(f"Total: {len(system.students)} students")


def list_all_courses(system):
    print("\n--- ALL COURSES ---")
    if not system.courses:
        print("No courses in the system.")
        return
    print("-" * 60)
    print(f"{'Code':<10} {'Name':<25} {'Credits':<8} {'Seats':<10}")
    print("-" * 60)
    for course in system.courses.values():
        available = course.capacity - len(course.enrolled_students)
        print(f"{course.code:<10} {course.name:<25} {course.credits:<8} {available}/{course.capacity}")
    print("-" * 60)
    print(f"Total: {len(system.courses)} courses")


def save_data(system):
    try:
        system.save()
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data(system):
    try:
        system.load()
    except Exception as e:
        print(f"Error loading data: {e}")


def main():
    try:
        system = RecordSystem()
    except Exception as e:
        print(f"Error: {e}")
        system = RecordSystem()
    
    print("\nWelcome to the Student Record System!")
    
    menu_actions = {
        '1': add_student, '2': add_course, '3': enroll_student,
        '4': record_grade, '5': view_transcript, '6': view_ranking,
        '7': view_analytics, '8': search_students, '9': search_courses,
        '10': delete_student, '11': delete_course, '12': list_all_students,
        '13': list_all_courses, '14': save_data, '15': load_data,
    }
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '0':
            print("\nGoodbye!")
            system.save()
            sys.exit(0)
        
        if choice in menu_actions:
            menu_actions[choice](system)
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()