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
    parser.add_argument("action", choices=["new", "recent", "info"])
    parser.add_argument("--course", "-c", help="Course name")
    parser.add_argument("--topic", "-t", help="Lecture topic")
    parser.add_argument("--days", "-d", type=int, default=7, help="Days for recent lectures")
    
    args = parser.parse_args()
    manager = AdvancedLectureManager()
    
    if args.action == "new":
        filepath = manager.new_lecture(args.course, args.topic)
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
            if data.get('lectures'):
                latest = data['lectures'][-1]
                print(f"Latest: {latest['topic']} ({latest['date'][:10]})")
        else:
            print("No course information found")

if __name__ == "__main__":
    main()
