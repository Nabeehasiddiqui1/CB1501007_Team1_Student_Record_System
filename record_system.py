# record_system.py
from academic_error import AcademicError
from collections import Counter
from typing import List, Tuple, Dict, Any
import json
import os


class RecordSystem:
    """
    Main system class that manages students, courses, and all operations.
    """
    
    def __init__(self, filename: str = "data/students_courses.json"):
        """
        Initialize the record system with empty data structures.
        
        Args:
            filename: Path to the JSON file for persistence
        """
        self.students = {}  # dictionary: student_id -> Student object
        self.courses = {}   # dictionary: course_code -> Course object
        self.filename = filename
        self.load()
    
    # ============================================================
    # YOUR ANALYTICS METHODS
    # ============================================================
    
    def calculate_ranking(self) -> List[Tuple[Any, float]]:
        """
        Calculate ranking of all students who have at least one graded course.
        
        Returns:
            List of tuples (student, gpa) sorted by GPA descending.
            Only students with at least one completed (graded) course are included.
        """
        ranked_students = []
        
        for student in self.students.values():
            # Check if student has any graded courses (grade is not None)
            graded_courses = [grade for grade in student.enrollments.values() if grade is not None]
            if len(graded_courses) > 0:
                gpa = student.gpa(self.courses)
                ranked_students.append((student, gpa))
        
        # Sort by GPA descending (highest first)
        ranked_students.sort(key=lambda x: x[1], reverse=True)
        
        return ranked_students
    
    def average_gpa_by_major(self) -> Dict[str, float]:
        """
        Calculate average GPA for each major.
        
        Returns:
            Dictionary mapping major name to average GPA.
            Only students with at least one graded course are included.
        """
        major_gpas = {}  # major -> list of GPAs
        
        for student in self.students.values():
            # Check if student has any graded courses
            graded_courses = [grade for grade in student.enrollments.values() if grade is not None]
            if len(graded_courses) == 0:
                continue  # Skip students with no grades
            
            gpa = student.gpa(self.courses)
            major = student.major
            
            if major not in major_gpas:
                major_gpas[major] = []
            
            major_gpas[major].append(gpa)
        
        # Calculate averages
        avg_by_major = {}
        for major, gpa_list in major_gpas.items():
            avg_by_major[major] = round(sum(gpa_list) / len(gpa_list), 2)
        
        return avg_by_major
    
    def grade_distribution(self) -> Counter:
        """
        Calculate distribution of all letter grades across all students.
        
        Returns:
            Counter object with letter grades as keys and counts as values.
        """
        all_grades = []
        
        for student in self.students.values():
            for grade in student.enrollments.values():
                if grade is not None:  # Only include actual grades, not None
                    all_grades.append(grade)
        
        return Counter(all_grades)
    
    def honor_roll(self) -> List[Tuple[Any, float]]:
        """
        Identify students on the honor roll (GPA >= 3.5).
        
        Returns:
            List of tuples (student, gpa) for students with GPA >= 3.5.
            Only includes students with at least one graded course.
            Sorted by GPA descending.
        """
        honor_students = []
        
        for student in self.students.values():
            # Check if student has any graded courses
            graded_courses = [grade for grade in student.enrollments.values() if grade is not None]
            if len(graded_courses) == 0:
                continue
            
            gpa = student.gpa(self.courses)
            if gpa >= 3.5:
                honor_students.append((student, gpa))
        
        # Sort by GPA descending
        honor_students.sort(key=lambda x: x[1], reverse=True)
        
        return honor_students
    
    def at_risk_students(self) -> List[Tuple[Any, float]]:
        """
        Identify at-risk students (GPA < 2.0).
        
        Returns:
            List of tuples (student, gpa) for students with GPA < 2.0.
            Only includes students with at least one graded course.
            Sorted by GPA ascending (lowest first).
        """
        at_risk = []
        
        for student in self.students.values():
            # Check if student has any graded courses
            graded_courses = [grade for grade in student.enrollments.values() if grade is not None]
            if len(graded_courses) == 0:
                continue
            
            gpa = student.gpa(self.courses)
            if gpa < 2.0:
                at_risk.append((student, gpa))
        
        # Sort by GPA ascending (lowest GPAs first)
        at_risk.sort(key=lambda x: x[1])
        
        return at_risk
    
    def print_analytics_report(self) -> None:
        """
        Print a formatted analytics report showing all statistics.
        This method is called from the menu interface.
        """
        print("\n" + "=" * 60)
        print("ACADEMIC ANALYTICS REPORT")
        print("=" * 60)
        
        # 1. Grade Distribution
        print("\nGRADE DISTRIBUTION:")
        print("-" * 30)
        grade_counts = self.grade_distribution()
        if grade_counts:
            for grade in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
                count = grade_counts.get(grade, 0)
                print(f"  {grade}: {count}")
        else:
            print("  No grades recorded yet.")
        
        # 2. Average GPA by Major
        print("\nAVERAGE GPA BY MAJOR:")
        print("-" * 30)
        avg_by_major = self.average_gpa_by_major()
        if avg_by_major:
            for major, avg_gpa in sorted(avg_by_major.items()):
                print(f"  {major}: {avg_gpa}")
        else:
            print("  No data available.")
        
        # 3. Class Ranking (Top 5)
        print("\nCLASS RANKING (Top 5):")
        print("-" * 30)
        ranking = self.calculate_ranking()
        if ranking:
            for i, (student, gpa) in enumerate(ranking[:5], 1):
                print(f"  {i}. {student.name} (ID: {student.sid}) - GPA: {gpa}")
            if len(ranking) > 5:
                print(f"  ... and {len(ranking) - 5} more students")
        else:
            print("  No students with completed courses.")
        
        # 4. Honor Roll
        print("\nHONOR ROLL (GPA >= 3.5):")
        print("-" * 30)
        honor = self.honor_roll()
        if honor:
            for student, gpa in honor:
                print(f"  * {student.name} (ID: {student.sid}) - GPA: {gpa}")
        else:
            print("  No students on honor roll.")
        
        # 5. At-Risk Students
        print("\nAT-RISK STUDENTS (GPA < 2.0):")
        print("-" * 30)
        at_risk = self.at_risk_students()
        if at_risk:
            for student, gpa in at_risk:
                print(f"  * {student.name} (ID: {student.sid}) - GPA: {gpa}")
        else:
            print("  No at-risk students.")
        
        print("\n" + "=" * 60)
    
    # ============================================================
    # PLACEHOLDER METHODS (Your teammates will implement these)
    # ============================================================
    
    def enroll_student(self, student_id: str, course_code: str) -> None:
        if student_id not in self.students:
            raise AcademicError(f"Student with ID {student_id} not found")
        if course_code not in self.courses:
            raise AcademicError(f"Course with code {course_code} not found")
        
        student = self.students[student_id]
        course = self.courses[course_code]
        
        if course_code in student.enrollments:
            raise AcademicError(f"Student {student_id} is already enrolled in {course_code}")
        if course.is_full():
            raise AcademicError(f"Course {course_code} has reached maximum capacity")
        
        student.enrollments[course_code] = None
        course.enroll(student_id)
        print(f"Student {student.name} enrolled in {course.name} successfully")
        self.save()
    
    def record_grade(self, student_id: str, course_code: str, grade: str) -> None:
        valid_grades = {'A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F'}
        if grade not in valid_grades:
            raise AcademicError(f"Invalid grade. Must be one of: {', '.join(valid_grades)}")
        if student_id not in self.students:
            raise AcademicError(f"Student with ID {student_id} not found")
        if course_code not in self.courses:
            raise AcademicError(f"Course with code {course_code} not found")
        
        student = self.students[student_id]
        if course_code not in student.enrollments:
            raise AcademicError(f"Student {student_id} is not enrolled in {course_code}")
        
        student.enrollments[course_code] = grade
        print(f"Grade {grade} recorded for {student.name} in {self.courses[course_code].name}")
        self.save()
    
    def validate_year(self, year: str) -> bool:
        valid_years = {'Freshman', 'Sophomore', 'Junior', 'Senior'}
        if year not in valid_years:
            raise AcademicError(f"Invalid year. Must be one of: {', '.join(valid_years)}")
        return True
    
    def validate_major(self, major: str) -> bool:
        if not major or len(major.strip()) == 0:
            raise AcademicError("Major cannot be empty")
        if len(major) < 2:
            raise AcademicError("Major must be at least 2 characters")
        return True
        # ============================================================
    # CRUD METHODS FOR STUDENTS AND COURSES (Member 3)
    # ============================================================
    
    def add_student(self, name: str, student_id: str, major: str, year: str) -> None:
        """
        Add a new student to the system.
        """
        from student import Student
        from academic_error import AcademicError
        
        # Validate inputs
        self.validate_major(major)
        self.validate_year(year)
        
        # Check for duplicate ID
        if student_id in self.students:
            raise AcademicError(f"Student with ID {student_id} already exists")
        
        # Create and add student
        student = Student(name, student_id, major, year)
        self.students[student_id] = student
        self.save()
        print(f"Student {name} added successfully")
    
    def edit_student(self, student_id: str, name: str = None, major: str = None, year: str = None) -> None:
        """
        Edit an existing student's information.
        """
        from academic_error import AcademicError
        
        if student_id not in self.students:
            raise AcademicError(f"Student with ID {student_id} not found")
        
        student = self.students[student_id]
        
        if name:
            student.name = name
        if major:
            self.validate_major(major)
            student.major = major
        if year:
            self.validate_year(year)
            student.year = year
        
        self.save()
        print(f"Student {student_id} updated successfully")
    
    def delete_student(self, student_id: str) -> None:
        """
        Delete a student from the system and remove from all course rosters.
        """
        from academic_error import AcademicError
        
        if student_id not in self.students:
            raise AcademicError(f"Student with ID {student_id} not found")
        
        # Remove student from all course rosters
        for course in self.courses.values():
            course.remove(student_id)
        
        # Delete student
        del self.students[student_id]
        self.save()
        print(f"Student {student_id} deleted successfully")
    
    def add_course(self, code: str, name: str, credits: int, capacity: int) -> None:
        """
        Add a new course to the system.
        """
        from course import Course
        from academic_error import AcademicError
        
        # Validate credits
        if credits < 1 or credits > 6:
            raise AcademicError("Credits must be between 1 and 6")
        
        # Validate capacity
        if capacity < 1:
            raise AcademicError("Capacity must be at least 1")
        
        # Check for duplicate code
        if code in self.courses:
            raise AcademicError(f"Course with code {code} already exists")
        
        # Create and add course
        course = Course(code, name, credits, capacity)
        self.courses[code] = course
        self.save()
        print(f"Course {name} added successfully")
    
    def edit_course(self, code: str, name: str = None, credits: int = None, capacity: int = None) -> None:
        """
        Edit an existing course's information.
        """
        from academic_error import AcademicError
        
        if code not in self.courses:
            raise AcademicError(f"Course with code {code} not found")
        
        course = self.courses[code]
        
        if name:
            course.name = name
        if credits:
            if credits < 1 or credits > 6:
                raise AcademicError("Credits must be between 1 and 6")
            course.credits = credits
        if capacity:
            if capacity < 1:
                raise AcademicError("Capacity must be at least 1")
            course.capacity = capacity
        
        self.save()
        print(f"Course {code} updated successfully")
    
    def delete_course(self, code: str) -> None:
        """
        Delete a course from the system and remove from all student enrollments.
        """
        from academic_error import AcademicError
        
        if code not in self.courses:
            raise AcademicError(f"Course with code {code} not found")
        
        # Remove course from all student enrollments
        for student in self.students.values():
            if code in student.enrollments:
                del student.enrollments[code]
        
        # Delete course
        del self.courses[code]
        self.save()
        print(f"Course {code} deleted successfully")
    
    def search_students(self, keyword: str, search_by: str = 'name') -> list:
        """
        Search for students by name, ID, or major (case-insensitive).
        """
        keyword_lower = keyword.lower()
        results = []
        
        for student in self.students.values():
            if search_by == 'name' and keyword_lower in student.name.lower():
                results.append(student)
            elif search_by == 'id' and keyword_lower in student.sid.lower():
                results.append(student)
            elif search_by == 'major' and keyword_lower in student.major.lower():
                results.append(student)
        
        return results
    def add_student(self):
        """To be implemented by teammate"""
        pass
    
    def add_course(self):
        """To be implemented by teammate"""
        pass
    
    def save(self):
        """To be implemented by teammate"""
        pass
    
    def load(self):
        """To be implemented by teammate"""
        pass