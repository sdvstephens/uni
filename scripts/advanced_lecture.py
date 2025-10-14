#!/usr/bin/env python3

import os
import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class AdvancedLectureManager:
    def __init__(self, root_dir="~/university"):
        self.root_dir = Path(root_dir).expanduser()
        self.metadata_file = self.root_dir / ".course_metadata.json"
        self.load_metadata()
        
    def load_metadata(self):
        """Load course metadata with attendance, topics, etc."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def save_metadata(self):
        """Save course metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_current_course(self):
        """Get current course from the symlink we set up"""
        current_link = Path.home() / "current-course"
        if current_link.is_symlink():
            return current_link.readlink().name
        return None
    
    def new_lecture(self, course_name=None, topic=None):
        """Create new lecture with metadata tracking"""
        if not course_name:
            course_name = self.get_current_course()
            if not course_name:
                print("No current course set. Use 'cs' to select a course first.")
                return
        
        course_path = self.root_dir / course_name
        
        # Find existing lectures and determine next number
        lectures = list(course_path.glob("lecture_*.tex"))
        next_num = len(lectures) + 1
        
        if not topic:
            topic = input(f"Lecture {next_num} topic: ").strip()
            if not topic:
                topic = f"Lecture {next_num}"
        
        # Create lecture content with better template
        date_str = datetime.now().strftime("%B %d, %Y")
        lecture_content = f"""\\documentclass{{report}}
\\input{{../preamble}}

\\course{{{course_name}}}

\\begin{{document}}

\\lecture{{{next_num}}}{{{topic}}}

\\section{{{topic}}}

% Your notes here...

\\end{{document}}
"""
        
        lecture_file = course_path / f"lecture_{next_num:02d}.tex"
        with open(lecture_file, 'w') as f:
            f.write(lecture_content)
        
        # Update metadata
        if course_name not in self.metadata:
            self.metadata[course_name] = {"lectures": [], "created": datetime.now().isoformat()}
        
        lecture_meta = {
            "number": next_num,
            "date": datetime.now().isoformat(),
            "topic": topic,
            "filename": f"lecture_{next_num:02d}.tex"
        }
        
        self.metadata[course_name]["lectures"].append(lecture_meta)
        self.save_metadata()
        
        print(f"Created {course_name}/lecture_{next_num:02d}.tex: {topic}")
        return lecture_file
    def new_homework(self, course_name=None, hw_num=None, title=None):
        """Create new homework file with template"""
        if not course_name:
            course_name = self.get_current_course()
            if not course_name:
                print("No current course set.")
                return
        
        course_path = self.root_dir / course_name
        psets_dir = course_path / "psets"
        
        # Create psets directory if it doesn't exist
        psets_dir.mkdir(exist_ok=True)
        (psets_dir / "figures").mkdir(exist_ok=True)
        
        # Find existing homework files and determine next number
        if hw_num is None:
            hw_files = list(psets_dir.glob("hw_*.tex"))
            hw_num = len(hw_files) + 1
        
        if not title:
            title = input(f"Homework {hw_num} title (or press enter): ").strip()
            if not title:
                title = f"Problem Set {hw_num}"
        
        # Create homework template
        hw_content = f"""\\documentclass{{report}}
\\input{{~/university/preamble.tex}}

\\begin{{document}}

\\begin{{titlebox}}[Math 55a]
    \\textbf{{Name:}} S. D. V. Stephens\\\\[2mm]
    \\textbf{{Professor:}} Prof. Denis Auroux\\\\[2mm]
    \\textbf{{Date:}}\\today 
\\tcblower
    \\begin{{center}}
    \\vspace{{4mm}}
    {{\\Huge\\bfseries PSET {hw_num}}}
    \\end{{center}}
\\end{{titlebox}}
\\vspace{{10mm}}

\\qs{{}}{{}}
\\sol 

\\qs{{}}{{}}
\\sol 

\\qs{{}}{{}}
\\sol

\\end{{document}}
"""
        
        hw_file = psets_dir / f"hw_{hw_num:02d}.tex"
        with open(hw_file, 'w') as f:
            f.write(hw_content)
        
        # Update metadata
        if course_name not in self.metadata:
            self.metadata[course_name] = {"lectures": [], "homework": [], "created": datetime.now().isoformat()}
        
        if "homework" not in self.metadata[course_name]:
            self.metadata[course_name]["homework"] = []
        
        hw_meta = {
            "number": hw_num,
            "date": datetime.now().isoformat(),
            "title": title,
            "filename": f"hw_{hw_num:02d}.tex"
        }
        
        self.metadata[course_name]["homework"].append(hw_meta)
        self.save_metadata()
        
        print(f"Created {course_name}/psets/hw_{hw_num:02d}.tex: {title}")
        return hw_file
    def list_recent(self, days=7):
        """List recent lectures across all courses"""
        cutoff = datetime.now() - timedelta(days=days)
        recent = []
        
        for course, data in self.metadata.items():
            for lecture in data.get("lectures", []):
                lecture_date = datetime.fromisoformat(lecture["date"])
                if lecture_date > cutoff:
                    recent.append({
                        "course": course,
                        "lecture": lecture,
                        "date": lecture_date
                    })
        
        recent.sort(key=lambda x: x["date"], reverse=True)
        
        if recent:
            print(f"Recent lectures (last {days} days):")
            for item in recent:
                date_str = item["date"].strftime("%Y-%m-%d %H:%M")
                print(f"  {item['course']}: {item['lecture']['topic']} ({date_str})")
        else:
            print(f"No lectures in the last {days} days")
def main():
    parser = argparse.ArgumentParser(description="Advanced lecture management")
    parser.add_argument("action", choices=["new", "psets", "recent", "info"])
    parser.add_argument("--course", "-c", help="Course name")
    parser.add_argument("--topic", "-t", help="Lecture topic")
    parser.add_argument("--title", help="Problem set title")
    parser.add_argument("--number", "-n", type=int, help="Problem set/Lecture number")
    parser.add_argument("--days", "-d", type=int, default=7, help="Days for recent lectures")
    
    args = parser.parse_args()
    manager = AdvancedLectureManager()
    
    if args.action == "new":
        filepath = manager.new_lecture(args.course, args.topic)
        if filepath:
            # Open in nvim automatically
            subprocess.run(["nvim", str(filepath)])
    
    elif args.action == "psets":
        filepath = manager.new_homework(args.course, args.number, args.title)
        if filepath:
            # Open in nvim automatically
            subprocess.run(["nvim", str(filepath)])
    
    elif args.action == "recent":
        manager.list_recent(args.days)
    
    elif args.action == "info":
        course = args.course or manager.get_current_course()
        if course and course in manager.metadata:
            data = manager.metadata[course]
            print(f"Course: {course}")
            print(f"Total lectures: {len(data.get('lectures', []))}")
            print(f"Total problem sets: {len(data.get('homework', []))}")
            if data.get('lectures'):
                latest = data['lectures'][-1]
                print(f"Latest lecture: {latest['topic']} ({latest['date'][:10]})")
            if data.get('homework'):
                latest_pset = data['homework'][-1]
                print(f"Latest pset: {latest_pset['title']} ({latest_pset['date'][:10]})")
        else:
            print("No course information found")
if __name__ == "__main__":
    main()
