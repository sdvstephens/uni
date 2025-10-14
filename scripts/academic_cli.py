#!/usr/bin/env python3
"""
Unified Academic CLI - Complete Academic Life Management System
Integrates course management, grade tracking, task management, and calendar
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class UnifiedAcademicSystem:
    def __init__(self, root_dir="~/university"):
        self.root_dir = Path(root_dir).expanduser()
        self.data_dir = self.root_dir / ".academic_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Data files
        self.courses_file = self.data_dir / "courses.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.schedule_file = self.data_dir / "schedule.json"
        self.settings_file = self.data_dir / "settings.json"
        
        # Load all data
        self.load_data()
    
    def load_data(self):
        """Load all data from JSON files"""
        self.courses = self.load_json(self.courses_file, {})
        self.tasks = self.load_json(self.tasks_file, [])
        self.schedule = self.load_json(self.schedule_file, {})
        self.settings = self.load_json(self.settings_file, {
            "current_semester": "Fall 2024",
            "academic_year": "2024-2025"
        })
    
    def load_json(self, file_path: Path, default):
        """Load JSON data with fallback to default"""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def save_data(self):
        """Save all data to JSON files"""
        self.save_json(self.courses_file, self.courses)
        self.save_json(self.tasks_file, self.tasks)
        self.save_json(self.schedule_file, self.schedule)
        self.save_json(self.settings_file, self.settings)
    
    def save_json(self, file_path: Path, data):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    # COURSE MANAGEMENT
    def add_course(self, name: str, code: str = "", credits: float = 3.0, 
                   instructor: str = "", schedule: str = ""):
        """Add a new course"""
        course_id = name.lower().replace(" ", "_")
        
        self.courses[course_id] = {
            "name": name,
            "code": code,
            "credits": credits,
            "instructor": instructor,
            "schedule": schedule,
            "created": datetime.now().isoformat(),
            "assignments": {},
            "notes_path": str(self.root_dir / name.replace(" ", "_"))
        }
        
        # Create course directory structure
        course_dir = self.root_dir / name.replace(" ", "_")
        course_dir.mkdir(exist_ok=True)
        (course_dir / "figures").mkdir(exist_ok=True)
        (course_dir / "psets").mkdir(exist_ok=True)
        (course_dir / "psets" / "figures").mkdir(exist_ok=True)
        
        # Create .latexmkrc for texlab root detection
        latexmkrc_content = """# LaTeX build configuration
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 %O %S';
$out_dir = '.latexmk/out';
$aux_dir = '.latexmk/aux';
"""
        latexmkrc_file = course_dir / ".latexmkrc"
        with open(latexmkrc_file, 'w') as f:
            f.write(latexmkrc_content)


        self.save_data()
        print(f"✓ Added course: {name} ({code}) - {credits} credits")
        print(f"✓ Created .latexmkrc in {course_dir.name}")
        
    def list_courses(self):
        """List all courses"""
        if not self.courses:
            print("No courses found")
            return
        
        print(f"\n=== Courses ({self.settings['current_semester']}) ===")
        for course_id, course in self.courses.items():
            schedule_info = f" [{course['schedule']}]" if course['schedule'] else ""
            print(f"  {course['name']} ({course['code']}) - {course['credits']} credits{schedule_info}")
            if course['instructor']:
                print(f"    Instructor: {course['instructor']}")
    
    # TASK MANAGEMENT
    def add_task(self, title: str, course: str = "", due_date: str = "", 
                 priority: str = "medium", task_type: str = "assignment"):
        """Add a new task"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "course": course,
            "due_date": due_date,
            "priority": priority,  # low, medium, high, urgent
            "type": task_type,    # assignment, study, exam, project, reading
            "status": "pending",   # pending, in_progress, completed
            "created": datetime.now().isoformat(),
            "completed": None,
            "notes": ""
        }
        
        self.tasks.append(task)
        self.save_data()
        
        due_info = f" (due: {due_date})" if due_date else ""
        course_info = f" [{course}]" if course else ""
        print(f"✓ Added task: {title}{course_info}{due_info}")
    
    def list_tasks(self, status: str = "pending", course: str = ""):
        """List tasks with optional filtering"""
        filtered_tasks = [
            task for task in self.tasks 
            if (not status or task["status"] == status) and
               (not course or task["course"].lower() == course.lower())
        ]
        
        if not filtered_tasks:
            filter_info = f" ({status})" if status else ""
            course_info = f" for {course}" if course else ""
            print(f"No tasks found{filter_info}{course_info}")
            return
        
        # Sort by due date, then priority
        def sort_key(task):
            due_date = task["due_date"] or "9999-12-31"
            priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
            return (due_date, priority_order.get(task["priority"], 2))
        
        filtered_tasks.sort(key=sort_key)
        
        print(f"\n=== Tasks ===")
        for task in filtered_tasks:
            priority_icon = {"urgent": "🔥", "high": "⚡", "medium": "📝", "low": "💭"}
            status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
            
            due_info = f" (due: {task['due_date']})" if task['due_date'] else ""
            course_info = f" [{task['course']}]" if task['course'] else ""
            
            print(f"  {status_icon[task['status']]} {priority_icon[task['priority']]} "
                  f"{task['title']}{course_info}{due_info}")
    
    def complete_task(self, task_id: int):
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed"] = datetime.now().isoformat()
                self.save_data()
                print(f"✅ Completed: {task['title']}")
                return
        print(f"Task {task_id} not found")
    
    def update_task_status(self, task_id: int, status: str):
        """Update task status"""
        valid_statuses = ["pending", "in_progress", "completed"]
        if status not in valid_statuses:
            print(f"Invalid status. Use: {', '.join(valid_statuses)}")
            return
        
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                if status == "completed":
                    task["completed"] = datetime.now().isoformat()
                self.save_data()
                print(f"✓ Updated task {task_id} status to: {status}")
                return
        print(f"Task {task_id} not found")
    
    # SCHEDULE MANAGEMENT
    def add_class_schedule(self, course: str, day: str, time: str, location: str = ""):
        """Add recurring class schedule"""
        if course not in self.schedule:
            self.schedule[course] = {"classes": [], "exams": []}
        
        class_info = {
            "day": day,
            "time": time,
            "location": location,
            "type": "class"
        }
        
        self.schedule[course]["classes"].append(class_info)
        self.save_data()
        print(f"✓ Added class schedule: {course} - {day} {time}")
    
    def add_exam(self, course: str, exam_type: str, date: str, time: str = "", location: str = ""):
        """Add exam to schedule"""
        if course not in self.schedule:
            self.schedule[course] = {"classes": [], "exams": []}
        
        exam_info = {
            "type": exam_type,  # midterm, final, quiz
            "date": date,
            "time": time,
            "location": location
        }
        
        self.schedule[course]["exams"].append(exam_info)
        self.save_data()
        
        # Auto-create study task
        study_task_title = f"Study for {exam_type} - {course}"
        study_due = (datetime.fromisoformat(date) - timedelta(days=3)).strftime("%Y-%m-%d")
        self.add_task(study_task_title, course, study_due, "high", "study")
        
        print(f"✓ Added exam: {course} {exam_type} on {date}")
        print(f"✓ Created study task (due: {study_due})")
    
    def show_schedule(self, days: int = 7):
        """Show upcoming schedule"""
        print(f"\n=== Upcoming Schedule ({days} days) ===")
        
        # Show classes
        today = datetime.now()
        days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        for course, schedule_data in self.schedule.items():
            for class_info in schedule_data["classes"]:
                day = class_info["day"].lower()
                if day in days_of_week:
                    location_info = f" at {class_info['location']}" if class_info['location'] else ""
                    print(f"  📚 {course}: {class_info['day']} {class_info['time']}{location_info}")
        
        # Show upcoming exams
        upcoming_exams = []
        for course, schedule_data in self.schedule.items():
            for exam in schedule_data["exams"]:
                exam_date = datetime.fromisoformat(exam["date"])
                if (exam_date - today).days <= days and exam_date >= today:
                    upcoming_exams.append((exam_date, course, exam))
        
        upcoming_exams.sort()
        for exam_date, course, exam in upcoming_exams:
            days_until = (exam_date - today).days
            time_info = f" at {exam['time']}" if exam['time'] else ""
            location_info = f" ({exam['location']})" if exam['location'] else ""
            print(f"  🎯 {course} {exam['type']} in {days_until} days: {exam['date']}{time_info}{location_info}")
    
    # DASHBOARD
    def show_dashboard(self):
        """Show comprehensive academic dashboard"""
        print("=" * 60)
        print(f"   📚 ACADEMIC DASHBOARD - {datetime.now().strftime('%Y-%m-%d')}")
        print("=" * 60)
        
        # Today's tasks
        today = datetime.now().strftime("%Y-%m-%d")
        urgent_tasks = [t for t in self.tasks if t["due_date"] == today and t["status"] != "completed"]
        
        if urgent_tasks:
            print(f"\n🔥 DUE TODAY ({len(urgent_tasks)} tasks):")
            for task in urgent_tasks:
                course_info = f" [{task['course']}]" if task['course'] else ""
                print(f"   • {task['title']}{course_info}")
        
        # This week's tasks
        week_end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        week_tasks = [t for t in self.tasks 
                     if t["due_date"] and today <= t["due_date"] <= week_end and t["status"] != "completed"]
        
        if week_tasks:
            print(f"\n📅 THIS WEEK ({len(week_tasks)} tasks):")
            for task in sorted(week_tasks, key=lambda x: x["due_date"]):
                course_info = f" [{task['course']}]" if task['course'] else ""
                print(f"   • {task['due_date']}: {task['title']}{course_info}")
        
        # Course overview
        print(f"\n📚 COURSES ({len(self.courses)}):")
        for course_id, course in self.courses.items():
            print(f"   • {course['name']} ({course['code']})")
        
        # Recent activity
        recent_tasks = [t for t in self.tasks if t["status"] == "completed"][-3:]
        if recent_tasks:
            print(f"\n✅ RECENTLY COMPLETED:")
            for task in reversed(recent_tasks):
                course_info = f" [{task['course']}]" if task['course'] else ""
                print(f"   • {task['title']}{course_info}")
        
        print("\n" + "=" * 60)
    
    # INTEGRATION HELPERS
    def create_lecture_with_tasks(self, course: str, lecture_num: int, topic: str):
        """Create lecture and associated tasks"""
        # Use existing alec system
        try:
            result = subprocess.run([
                "alec", "new-lecture", 
                "--course", course, 
                "--number", str(lecture_num),
                "--title", topic
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Created lecture {lecture_num}: {topic}")
                
                # Add review task
                review_due = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
                self.add_task(f"Review Lecture {lecture_num}: {topic}", course, review_due, "low", "study")
                
            else:
                print(f"⚠ Could not create lecture: {result.stderr}")
        except FileNotFoundError:
            print("⚠ alec command not found. Make sure it's in your PATH.")
    
    def export_weekly_report(self):
        """Generate weekly LaTeX report"""
        week_start = datetime.now() - timedelta(days=7)
        completed_tasks = [
            t for t in self.tasks 
            if t["completed"] and datetime.fromisoformat(t["completed"]) >= week_start
        ]
        
        latex_report = f"""\\section{{Weekly Report - {datetime.now().strftime('%Y-%m-%d')}}}

\\subsection{{Completed This Week}}
\\begin{{itemize}}
"""
        for task in completed_tasks:
            course_info = f" ({task['course']})" if task['course'] else ""
            latex_report += f"    \\item {task['title']}{course_info}\n"
        
        latex_report += "\\end{itemize}\n"
        
        # Upcoming deadlines
        upcoming = [t for t in self.tasks if t["due_date"] and t["status"] != "completed"]
        if upcoming:
            latex_report += "\n\\subsection{Upcoming Deadlines}\n\\begin{itemize}\n"
            for task in sorted(upcoming, key=lambda x: x["due_date"])[:5]:
                course_info = f" ({task['course']})" if task['course'] else ""
                latex_report += f"    \\item {task['due_date']}: {task['title']}{course_info}\n"
            latex_report += "\\end{itemize}\n"
        
        return latex_report

def main():
    parser = argparse.ArgumentParser(description="Unified Academic Management System")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Course commands
    course_parser = subparsers.add_parser('course', help='Course management')
    course_subparsers = course_parser.add_subparsers(dest='course_action')
    
    add_course = course_subparsers.add_parser('add', help='Add course')
    add_course.add_argument('--name', required=True, help='Course name')
    add_course.add_argument('--code', default='', help='Course code')
    add_course.add_argument('--credits', type=float, default=3.0, help='Credit hours')
    add_course.add_argument('--instructor', default='', help='Instructor name')
    add_course.add_argument('--schedule', default='', help='Class schedule')
    
    course_subparsers.add_parser('list', help='List courses')
    
    # Task commands
    task_parser = subparsers.add_parser('task', help='Task management')
    task_subparsers = task_parser.add_subparsers(dest='task_action')
    
    add_task = task_subparsers.add_parser('add', help='Add task')
    add_task.add_argument('--title', required=True, help='Task title')
    add_task.add_argument('--course', default='', help='Related course')
    add_task.add_argument('--due', default='', help='Due date (YYYY-MM-DD)')
    add_task.add_argument('--priority', choices=['low', 'medium', 'high', 'urgent'], default='medium')
    add_task.add_argument('--type', choices=['assignment', 'study', 'exam', 'project', 'reading'], default='assignment')
    
    list_tasks = task_subparsers.add_parser('list', help='List tasks')
    list_tasks.add_argument('--status', choices=['pending', 'in_progress', 'completed'], default='pending')
    list_tasks.add_argument('--course', default='', help='Filter by course')
    
    complete_task = task_subparsers.add_parser('complete', help='Complete task')
    complete_task.add_argument('--id', type=int, required=True, help='Task ID')
    
    # Schedule commands
    schedule_parser = subparsers.add_parser('schedule', help='Schedule management')
    schedule_subparsers = schedule_parser.add_subparsers(dest='schedule_action')
    
    add_class = schedule_subparsers.add_parser('add-class', help='Add class schedule')
    add_class.add_argument('--course', required=True, help='Course name')
    add_class.add_argument('--day', required=True, help='Day of week')
    add_class.add_argument('--time', required=True, help='Time')
    add_class.add_argument('--location', default='', help='Location')
    
    add_exam = schedule_subparsers.add_parser('add-exam', help='Add exam')
    add_exam.add_argument('--course', required=True, help='Course name')
    add_exam.add_argument('--type', required=True, help='Exam type')
    add_exam.add_argument('--date', required=True, help='Date (YYYY-MM-DD)')
    add_exam.add_argument('--time', default='', help='Time')
    add_exam.add_argument('--location', default='', help='Location')
    
    schedule_subparsers.add_parser('show', help='Show schedule')
    
    # Dashboard
    subparsers.add_parser('dashboard', help='Show dashboard')
    
    args = parser.parse_args()
    system = UnifiedAcademicSystem()
    
    if args.command == 'course':
        if args.course_action == 'add':
            system.add_course(args.name, args.code, args.credits, args.instructor, args.schedule)
        elif args.course_action == 'list':
            system.list_courses()
    
    elif args.command == 'task':
        if args.task_action == 'add':
            system.add_task(args.title, args.course, args.due, args.priority, args.type)
        elif args.task_action == 'list':
            system.list_tasks(args.status, args.course)
        elif args.task_action == 'complete':
            system.complete_task(args.id)
    
    elif args.command == 'schedule':
        if args.schedule_action == 'add-class':
            system.add_class_schedule(args.course, args.day, args.time, args.location)
        elif args.schedule_action == 'add-exam':
            system.add_exam(args.course, args.type, args.date, args.time, args.location)
        elif args.schedule_action == 'show':
            system.show_schedule()
    
    elif args.command == 'dashboard':
        system.show_dashboard()
    
    else:
        system.show_dashboard()  # Default action

if __name__ == "__main__":
    main()
