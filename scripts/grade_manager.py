#!/usr/bin/env python3
"""
Custom Grade Manager - Integrates with existing academic workflow
Designed to work with the alec course management system
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class GradeManager:
    def __init__(self, root_dir="~/university"):
        self.root_dir = Path(root_dir).expanduser()
        self.grades_file = self.root_dir / ".grades.json"
        self.load_grades()
    
    def load_grades(self):
        """Load grades from JSON file"""
        if self.grades_file.exists():
            with open(self.grades_file, 'r') as f:
                self.grades = json.load(f)
        else:
            self.grades = {}
    
    def save_grades(self):
        """Save grades to JSON file"""
        with open(self.grades_file, 'w') as f:
            json.dump(self.grades, f, indent=2)
    
    def add_course(self, course_name: str, credit_hours: float = 3.0):
        """Add a new course"""
        if course_name not in self.grades:
            self.grades[course_name] = {
                "credit_hours": credit_hours,
                "assignments": {},
                "categories": {},
                "final_grade": None,
                "created": datetime.now().isoformat()
            }
            self.save_grades()
            print(f"Added course: {course_name} ({credit_hours} credit hours)")
        else:
            print(f"Course {course_name} already exists")
    
    def add_category(self, course_name: str, category: str, weight: float):
        """Add a grade category (e.g., Homework: 30%, Exams: 70%)"""
        if course_name not in self.grades:
            print(f"Course {course_name} doesn't exist. Add it first.")
            return
        
        self.grades[course_name]["categories"][category] = {
            "weight": weight,
            "assignments": []
        }
        self.save_grades()
        print(f"Added category '{category}' with {weight}% weight to {course_name}")
    
    def add_grade(self, course_name: str, assignment: str, grade: float, 
                  category: str = "General", max_points: float = 100.0):
        """Add a grade for an assignment"""
        if course_name not in self.grades:
            print(f"Course {course_name} doesn't exist. Add it first.")
            return
        
        # Ensure category exists
        if category not in self.grades[course_name]["categories"]:
            # Auto-create category with default weight
            self.add_category(course_name, category, 100.0)
        
        assignment_data = {
            "grade": grade,
            "max_points": max_points,
            "percentage": (grade / max_points) * 100,
            "date": datetime.now().isoformat(),
            "category": category
        }
        
        self.grades[course_name]["assignments"][assignment] = assignment_data
        self.grades[course_name]["categories"][category]["assignments"].append(assignment)
        self.save_grades()
        
        print(f"Added grade: {assignment} = {grade}/{max_points} ({assignment_data['percentage']:.1f}%)")
    
    def calculate_course_grade(self, course_name: str) -> Optional[float]:
        """Calculate current grade for a course"""
        if course_name not in self.grades:
            return None
        
        course = self.grades[course_name]
        categories = course["categories"]
        assignments = course["assignments"]
        
        if not categories or not assignments:
            return None
        
        total_weighted_grade = 0.0
        total_weight = 0.0
        
        for category, cat_data in categories.items():
            if not cat_data["assignments"]:
                continue
            
            # Calculate average for this category
            category_total = 0.0
            category_count = 0
            
            for assignment_name in cat_data["assignments"]:
                if assignment_name in assignments:
                    category_total += assignments[assignment_name]["percentage"]
                    category_count += 1
            
            if category_count > 0:
                category_average = category_total / category_count
                weight = cat_data["weight"] / 100.0
                total_weighted_grade += category_average * weight
                total_weight += weight
        
        if total_weight > 0:
            return total_weighted_grade / total_weight
        return None
    
    def show_course_grades(self, course_name: str):
        """Display grades for a specific course"""
        if course_name not in self.grades:
            print(f"Course {course_name} not found")
            return
        
        course = self.grades[course_name]
        print(f"\n=== {course_name} ===")
        print(f"Credit Hours: {course['credit_hours']}")
        
        current_grade = self.calculate_course_grade(course_name)
        if current_grade:
            print(f"Current Grade: {current_grade:.1f}%")
        
        print("\nAssignments:")
        for assignment, data in course["assignments"].items():
            date = datetime.fromisoformat(data["date"]).strftime("%Y-%m-%d")
            print(f"  {assignment}: {data['grade']}/{data['max_points']} ({data['percentage']:.1f}%) [{data['category']}] ({date})")
        
        print("\nCategories:")
        for category, cat_data in course["categories"].items():
            print(f"  {category}: {cat_data['weight']}% weight")
    
    def show_all_grades(self):
        """Display grades for all courses"""
        if not self.grades:
            print("No courses found")
            return
        
        print("\n=== Grade Summary ===")
        total_credits = 0.0
        total_grade_points = 0.0
        
        for course_name, course_data in self.grades.items():
            current_grade = self.calculate_course_grade(course_name)
            credits = course_data["credit_hours"]
            
            print(f"{course_name}: ", end="")
            if current_grade:
                grade_letter = self.percentage_to_letter(current_grade)
                print(f"{current_grade:.1f}% ({grade_letter}) [{credits} credits]")
                
                # Calculate GPA contribution
                grade_points = self.letter_to_points(grade_letter)
                total_credits += credits
                total_grade_points += grade_points * credits
            else:
                print(f"No grades yet [{credits} credits]")
        
        if total_credits > 0:
            gpa = total_grade_points / total_credits
            print(f"\nOverall GPA: {gpa:.2f}")
    
    def percentage_to_letter(self, percentage: float) -> str:
        """Convert percentage to letter grade"""
        if percentage >= 97: return "A+"
        elif percentage >= 93: return "A"
        elif percentage >= 90: return "A-"
        elif percentage >= 87: return "B+"
        elif percentage >= 83: return "B"
        elif percentage >= 80: return "B-"
        elif percentage >= 77: return "C+"
        elif percentage >= 73: return "C"
        elif percentage >= 70: return "C-"
        elif percentage >= 67: return "D+"
        elif percentage >= 65: return "D"
        else: return "F"
    
    def letter_to_points(self, letter: str) -> float:
        """Convert letter grade to GPA points"""
        grade_points = {
            "A+": 4.0, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "F": 0.0
        }
        return grade_points.get(letter, 0.0)
    
    def export_latex_table(self, course_name: str) -> str:
        """Generate LaTeX table for grades"""
        if course_name not in self.grades:
            return ""
        
        course = self.grades[course_name]
        assignments = course["assignments"]
        
        latex = "\\begin{table}[ht]\n"
        latex += "\\centering\n"
        latex += "\\begin{tabular}{|l|c|c|c|l|}\n"
        latex += "\\hline\n"
        latex += "Assignment & Grade & Max & Percentage & Category \\\\\n"
        latex += "\\hline\n"
        
        for assignment, data in assignments.items():
            latex += f"{assignment} & {data['grade']} & {data['max_points']} & {data['percentage']:.1f}\\% & {data['category']} \\\\\n"
        
        latex += "\\hline\n"
        current_grade = self.calculate_course_grade(course_name)
        if current_grade:
            latex += f"\\multicolumn{{4}}{{|c|}}{{Current Grade}} & {current_grade:.1f}\\% \\\\\n"
            latex += "\\hline\n"
        
        latex += "\\end{tabular}\n"
        latex += f"\\caption{{Grades for {course_name}}}\n"
        latex += "\\end{table}\n"
        
        return latex
    
    def list_courses(self):
        """List all courses"""
        if not self.grades:
            print("No courses found")
            return
        
        print("Available courses:")
        for course_name, course_data in self.grades.items():
            assignment_count = len(course_data["assignments"])
            print(f"  {course_name} ({course_data['credit_hours']} credits, {assignment_count} assignments)")

def main():
    parser = argparse.ArgumentParser(description="Custom Grade Manager")
    parser.add_argument("action", choices=[
        "add-course", "add-category", "add-grade", 
        "show", "show-all", "list", "export-latex"
    ])
    parser.add_argument("--course", "-c", help="Course name")
    parser.add_argument("--assignment", "-a", help="Assignment name")
    parser.add_argument("--grade", "-g", type=float, help="Grade received")
    parser.add_argument("--max", "-m", type=float, default=100.0, help="Maximum points")
    parser.add_argument("--category", "--cat", default="General", help="Grade category")
    parser.add_argument("--weight", "-w", type=float, help="Category weight percentage")
    parser.add_argument("--credits", type=float, default=3.0, help="Credit hours for course")
    
    args = parser.parse_args()
    manager = GradeManager()
    
    if args.action == "add-course":
        if not args.course:
            print("Course name required")
            return
        manager.add_course(args.course, args.credits)
    
    elif args.action == "add-category":
        if not args.course or not args.weight:
            print("Course name and weight required")
            return
        manager.add_category(args.course, args.category, args.weight)
    
    elif args.action == "add-grade":
        if not args.course or not args.assignment or args.grade is None:
            print("Course, assignment, and grade required")
            return
        manager.add_grade(args.course, args.assignment, args.grade, args.category, args.max)
    
    elif args.action == "show":
        if not args.course:
            print("Course name required")
            return
        manager.show_course_grades(args.course)
    
    elif args.action == "show-all":
        manager.show_all_grades()
    
    elif args.action == "list":
        manager.list_courses()
    
    elif args.action == "export-latex":
        if not args.course:
            print("Course name required")
            return
        latex_table = manager.export_latex_table(args.course)
        print(latex_table)

if __name__ == "__main__":
    main()
