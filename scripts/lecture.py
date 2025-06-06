#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

class LectureManager:
    def __init__(self, root_dir="~/university"):
        self.root_dir = Path(root_dir).expanduser()
        self.courses_file = self.root_dir / "courses.txt"
        
    def get_courses(self):
        """Get list of available courses"""
        if not self.courses_file.exists():
            return []
        with open(self.courses_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    def add_course(self, course_name):
        """Add a new course"""
        courses = self.get_courses()
        if course_name not in courses:
            courses.append(course_name)
            with open(self.courses_file, 'w') as f:
                for course in sorted(courses):
                    f.write(f"{course}\n")
            
            # Create course directory
            course_dir = self.root_dir / course_name
            course_dir.mkdir(exist_ok=True)
            (course_dir / "figures").mkdir(exist_ok=True)
            
            print(f"Added course: {course_name}")
        else:
            print(f"Course {course_name} already exists")
    
    def create_lecture(self, course_name, lecture_number, title=""):
        """Create a new lecture file"""
        if course_name not in self.get_courses():
            print(f"Course {course_name} doesn't exist. Add it first.")
            return
        
        course_dir = self.root_dir / course_name
        filename = f"lecture_{lecture_number:02d}.tex"
        filepath = course_dir / filename
        
        if filepath.exists():
            print(f"Lecture {lecture_number} already exists")
            return filepath
        
        # Create lecture content from template
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""\\documentclass{{article}}
\\input{{../preamble}}

\\begin{{document}}

\\lecture{{{lecture_number}}}{{{title or f"Lecture {lecture_number}"}}}{{{{\\today}}}}

% Your notes here

\\end{{document}}
"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Created: {filepath}")
        return filepath

def main():
    parser = argparse.ArgumentParser(description="Manage lectures and courses")
    parser.add_argument("action", choices=["add-course", "new-lecture", "list-courses"])
    parser.add_argument("--course", "-c", help="Course name")
    parser.add_argument("--number", "-n", type=int, help="Lecture number")
    parser.add_argument("--title", "-t", help="Lecture title")
    
    args = parser.parse_args()
    manager = LectureManager()
    
    if args.action == "add-course":
        if not args.course:
            print("Course name required")
            return
        manager.add_course(args.course)
    
    elif args.action == "new-lecture":
        if not args.course or not args.number:
            print("Course name and lecture number required")
            return
        filepath = manager.create_lecture(args.course, args.number, args.title)
        
        # Optionally open in editor
        if filepath:
            subprocess.run(["nvim", str(filepath)])
    
    elif args.action == "list-courses":
        courses = manager.get_courses()
        if courses:
            print("Available courses:")
            for course in courses:
                print(f"  - {course}")
        else:
            print("No courses found")

if __name__ == "__main__":
    main()
