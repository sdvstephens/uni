#!/usr/bin/env python3
"""
Academic CLI v2 - Modern Academic Workflow Management
Integrates with taskwarrior, auto-detects courses, supports both org and tex output
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum
import shutil


class OutputFormat(Enum):
    ORG = "org"
    TEX = "tex"


@dataclass
class CourseInfo:
    name: str
    code: str
    instructor: str
    schedule: str
    lecture_count: int
    pset_count: int
    path: Path
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d['path'] = str(d['path'])
        return d


class TaskWarrior:
    """Wrapper for taskwarrior CLI"""
    
    @staticmethod
    def available() -> bool:
        return shutil.which("task") is not None
    
    @staticmethod
    def run(args: List[str], capture: bool = True) -> str:
        """Run task command and return output"""
        cmd = ["task", "rc.verbose=nothing", "rc.confirmation=off"] + args
        if capture:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd)
            return ""
    
    @classmethod
    def add(cls, description: str, project: str = "", due: str = "", 
            priority: str = "", tags: List[str] = None) -> str:
        """Add a task"""
        args = ["add", description]
        if project:
            args.append(f"project:{project}")
        if due:
            args.append(f"due:{due}")
        if priority:
            args.append(f"priority:{priority}")
        for tag in (tags or []):
            args.append(f"+{tag}")
        return cls.run(args)

    @classmethod
    def list_tasks(cls, filter_args: List[str] = None, json_output: bool = True) -> List[Dict]:
        """List tasks with optional filters"""
        args = (filter_args or []) + ["export"] if json_output else (filter_args or [])
        output = cls.run(args)
        if json_output and output:
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                return []
        return []
    
    @classmethod
    def get_pending(cls, project: str = "") -> List[Dict]:
        """Get pending tasks, optionally filtered by project"""
        filters = ["status:pending"]
        if project:
            filters.append(f"project:{project}")
        return cls.list_tasks(filters)
    
    @classmethod
    def get_due_soon(cls, days: int = 7) -> List[Dict]:
        """Get tasks due within N days"""
        return cls.list_tasks([f"due.before:{days}d", "status:pending"])
    
    @classmethod
    def complete(cls, task_id: int) -> str:
        """Mark task as done"""
        return cls.run([str(task_id), "done"])


class AcademicManager:
    """Main academic workflow manager"""
    
    def __init__(self, root_dir: str = "~/university"):
        self.root = Path(root_dir).expanduser()
        self.config_dir = self.root / ".academic"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self._load_config()
        self.tw = TaskWarrior()

    def _load_config(self) -> dict:
        """Load config, creating defaults if needed"""
        defaults = {
            "semester": "Spring 2025",
            "default_format": "org",  # or "tex"
            "author": "S. D. V. Stephens",
            "excluded_dirs": ["scripts", "tester", ".academic", "__pycache__"],
            "courses": {}  # course_id -> {code, instructor, schedule}
        }
        if self.config_file.exists():
            with open(self.config_file) as f:
                saved = json.load(f)
                defaults.update(saved)
        return defaults
    
    def _save_config(self):
        """Persist config"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _get_current_course(self) -> Optional[str]:
        """Get current course from symlink"""
        link = Path.home() / "current-course"
        if link.is_symlink():
            return link.resolve().name
        return None
    
    def _set_current_course(self, course: str):
        """Set current course symlink"""
        link = Path.home() / "current-course"
        target = self.root / course
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(target)

    def scan_courses(self) -> List[CourseInfo]:
        """Auto-detect courses from filesystem"""
        courses = []
        excluded = set(self.config["excluded_dirs"])
        
        for item in self.root.iterdir():
            if not item.is_dir() or item.name.startswith('.') or item.name in excluded:
                continue
            
            # Count lectures and psets
            lectures = list(item.glob("lecture_*.*"))
            psets_dir = item / "psets"
            psets = list(psets_dir.glob("hw_*.*")) if psets_dir.exists() else []
            
            # Get saved metadata or defaults
            meta = self.config["courses"].get(item.name, {})
            
            courses.append(CourseInfo(
                name=item.name,
                code=meta.get("code", ""),
                instructor=meta.get("instructor", ""),
                schedule=meta.get("schedule", ""),
                lecture_count=len(lectures),
                pset_count=len(psets),
                path=item
            ))
        
        return sorted(courses, key=lambda c: c.name)
    
    def update_course_meta(self, course: str, code: str = None, 
                           instructor: str = None, schedule: str = None):
        """Update course metadata"""
        if course not in self.config["courses"]:
            self.config["courses"][course] = {}
        if code is not None:
            self.config["courses"][course]["code"] = code
        if instructor is not None:
            self.config["courses"][course]["instructor"] = instructor
        if schedule is not None:
            self.config["courses"][course]["schedule"] = schedule
        self._save_config()

    def _get_next_number(self, course_path: Path, pattern: str) -> int:
        """Get next lecture/pset number"""
        existing = list(course_path.glob(pattern))
        return len(existing) + 1
    
    def create_lecture(self, course: str = None, topic: str = None, 
                       fmt: OutputFormat = None) -> Optional[Path]:
        """Create a new lecture file"""
        course = course or self._get_current_course()
        if not course:
            print("❌ No course specified. Use --course or set current course.")
            return None
        
        course_path = self.root / course
        if not course_path.exists():
            print(f"❌ Course directory not found: {course}")
            return None
        
        fmt = fmt or OutputFormat(self.config["default_format"])
        num = self._get_next_number(course_path, "lecture_*.*")
        
        if not topic:
            topic = input(f"Lecture {num} topic: ").strip() or f"Lecture {num}"
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"lecture_{num:02d}.{fmt.value}"
        filepath = course_path / filename
        
        if fmt == OutputFormat.ORG:
            content = self._org_lecture_template(course, num, topic, date_str)
        else:
            content = self._tex_lecture_template(course, num, topic, date_str)
        
        filepath.write_text(content)
        print(f"✅ Created: {filepath.relative_to(self.root)}")
        return filepath

    def _org_lecture_template(self, course: str, num: int, topic: str, date: str) -> str:
        author = self.config["author"]
        return f"""#+title: {course} - Lecture {num}: {topic}
#+author: {author}
#+date: {date}
#+setupfile: ../org-preamble.setup
#+latex_header_extra: \\course{{{course}}}

#+begin_export latex
\\lecture{{{num}}}{{{topic}}}
#+end_export

* {topic}

"""

    def _tex_lecture_template(self, course: str, num: int, topic: str, date: str) -> str:
        author = self.config["author"]
        return f"""% {course} - Lecture {num}: {topic}
% Author: {author}
% Date: {date}
% Compile with: pdflatex -shell-escape

\\documentclass{{report}}
\\input{{~/university/preamble.tex}}
\\input{{~/university/preamble-darkmode.tex}}

\\course{{{course}}}

\\begin{{document}}

\\lecture{{{num}}}{{{topic}}}



\\end{{document}}
"""

    def create_pset(self, course: str = None, title: str = None,
                    fmt: OutputFormat = None) -> Optional[Path]:
        """Create a new problem set"""
        course = course or self._get_current_course()
        if not course:
            print("❌ No course specified.")
            return None
        
        course_path = self.root / course
        psets_dir = course_path / "psets"
        psets_dir.mkdir(exist_ok=True)
        (psets_dir / "figures").mkdir(exist_ok=True)
        
        fmt = fmt or OutputFormat(self.config["default_format"])
        num = self._get_next_number(psets_dir, "hw_*.*")
        
        if not title:
            title = input(f"Problem set {num} title (enter for default): ").strip()
            title = title or f"Problem Set {num}"
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"hw_{num:02d}.{fmt.value}"
        filepath = psets_dir / filename
        
        if fmt == OutputFormat.ORG:
            content = self._org_pset_template(course, num, title, date_str)
        else:
            content = self._tex_pset_template(course, num, title, date_str)
        
        filepath.write_text(content)
        
        # Create taskwarrior task for the pset
        if TaskWarrior.available():
            due = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            TaskWarrior.add(
                f"{course} Problem Set {num}",
                project=course.replace("-", "_"),
                due=due,
                priority="M",
                tags=["pset", "academic"]
            )
            print(f"📋 Created task in taskwarrior (due: {due})")
        
        print(f"✅ Created: {filepath.relative_to(self.root)}")
        return filepath

    def _org_pset_template(self, course: str, num: int, title: str, date: str) -> str:
        author = self.config["author"]
        return f"""#+title: {course} - {title}
#+author: {author}
#+date: {date}
#+setupfile: ../../org-preamble.setup

#+begin_export latex
\\begin{{titlebox}}{{{course}}}
    \\textbf{{Name:}} {author}\\\\[2mm]
    \\textbf{{Date:}} \\today
\\tcblower
    \\begin{{center}}
    \\vspace{{4mm}}
    {{\\Huge\\bfseries PSET {num}}}
    \\end{{center}}
\\end{{titlebox}}
\\vspace{{10mm}}
#+end_export

* Problem 1

** Solution

* Problem 2

** Solution

"""

    def _tex_pset_template(self, course: str, num: int, title: str, date: str) -> str:
        author = self.config["author"]
        return f"""% {course} - {title}
% Author: {author}
% Date: {date}

\\documentclass{{report}}
\\input{{~/university/preamble.tex}}
\\input{{~/university/preamble-darkmode.tex}}
\\begin{{document}}

\\begin{{titlebox}}{{{course}}}
    \\textbf{{Name:}} S. D. V. Stephens\\\\[2mm]
    \\textbf{{Professor:}} Prof. Denis Auroux\\\\[2mm]
    \\textbf{{Date:}}\\today 
\\tcblower
    \\begin{{center}}
    \\vspace{{4mm}}
    {{\\Huge\\bfseries PSET {num}}}
    \\end{{center}}
\\end{{titlebox}}
\\vspace{{10mm}}

\\qs{{}}{{}}

\\sol{{}}

\\qs{{}}{{}}

\\sol{{}}

\\end{{document}}
"""

    def add_course(self, name: str, code: str = "", instructor: str = "", schedule: str = ""):
        """Create a new course directory structure"""
        course_dir = self.root / name
        if course_dir.exists():
            print(f"⚠️  Course directory already exists: {name}")
            return
        
        course_dir.mkdir()
        (course_dir / "figures").mkdir()
        (course_dir / "psets").mkdir()
        (course_dir / "psets" / "figures").mkdir()
        
        # Create .latexmkrc for texlab
        latexmkrc = """$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 %O %S';
$aux_dir = '.latexmk/aux';
"""
        (course_dir / ".latexmkrc").write_text(latexmkrc)
        
        # Save metadata
        self.update_course_meta(name, code, instructor, schedule)
        
        # Create taskwarrior project
        if TaskWarrior.available():
            project = name.replace("-", "_")
            TaskWarrior.add(f"Set up {name} course materials", project=project, tags=["setup"])
        
        print(f"✅ Created course: {name}")
        if code: print(f"   Code: {code}")
        if instructor: print(f"   Instructor: {instructor}")

    def dashboard(self, compact: bool = False):
        """Display aesthetic academic dashboard with taskwarrior integration"""
        import shutil
        import os
        
        courses = self.scan_courses()
        current = self._get_current_course()
        today = datetime.now()
        
        # Get terminal width, default to 70
        term_width = min(shutil.get_terminal_size().columns, 80)
        w = term_width - 4  # inner width
        
        # Only use colors if we're in a real TTY
        use_colors = sys.stdout.isatty()
        
        if use_colors:
            RESET = "\033[0m"
            BOLD = "\033[1m"
            DIM = "\033[2m"
            CYAN = "\033[36m"
            GREEN = "\033[32m"
            YELLOW = "\033[33m"
            RED = "\033[31m"
            MAGENTA = "\033[35m"
            BLUE = "\033[34m"
        else:
            RESET = BOLD = DIM = CYAN = GREEN = YELLOW = RED = MAGENTA = BLUE = ""
        
        def box_line(content: str, align: str = "left") -> str:
            """Create a properly aligned box line"""
            # Strip ANSI codes for length calculation
            import re
            visible = re.sub(r'\033\[[0-9;]*m', '', content)
            padding = w - len(visible)
            if align == "center":
                left_pad = padding // 2
                right_pad = padding - left_pad
                return f"  {' ' * left_pad}{content}{' ' * right_pad}  "
            elif align == "right":
                return f"  {' ' * padding}{content}  "
            else:
                return f"  {content}{' ' * padding}  "
        
        def separator(char: str = "─") -> str:
            return f"  {char * w}  "
        
        # Header
        print()
        print(f"{CYAN}{BOLD}" + separator("━") + RESET)
        print(box_line(f"{BOLD}ACADEMIC DASHBOARD{RESET}", "center"))
        print(box_line(f"{DIM}{today.strftime('%A, %B %d, %Y')}{RESET}", "center"))
        print(separator("─"))
        
        # Current course
        if current:
            print(box_line(f"{GREEN}▶{RESET} Current: {BOLD}{current}{RESET}"))
            print(separator("─"))
        
        # Courses section
        print(box_line(f"{CYAN}{BOLD}COURSES{RESET}"))
        print()
        
        if courses:
            for c in courses:
                marker = f"{GREEN}→{RESET}" if c.name == current else " "
                code_str = f" {DIM}({c.code}){RESET}" if c.code else ""
                stats = f"{DIM}{c.lecture_count}L {c.pset_count}P{RESET}"
                name_display = c.name[:35] + "..." if len(c.name) > 38 else c.name
                
                # Calculate spacing
                import re
                visible_left = re.sub(r'\033\[[0-9;]*m', '', f"{marker} {name_display}{code_str}")
                visible_right = re.sub(r'\033\[[0-9;]*m', '', stats)
                space = w - len(visible_left) - len(visible_right)
                
                print(f"  {marker} {name_display}{code_str}{' ' * max(1, space)}{stats}  ")
        else:
            print(box_line(f"{DIM}No courses found{RESET}"))
        
        print()
        print(separator("─"))
        
        # Tasks section
        print(box_line(f"{YELLOW}{BOLD}TASKS{RESET}"))
        print()
        
        if TaskWarrior.available():
            # Due today
            due_today = [t for t in TaskWarrior.get_due_soon(1) 
                        if "academic" in t.get("tags", []) or 
                           any(c.name.replace("-","_") in t.get("project","") for c in courses)]
            
            # Due this week
            due_week = [t for t in TaskWarrior.get_due_soon(7)
                       if "academic" in t.get("tags", []) or
                          any(c.name.replace("-","_") in t.get("project","") for c in courses)]
            due_week = [t for t in due_week if t not in due_today]
            
            if due_today:
                print(box_line(f"{RED}{BOLD}DUE TODAY{RESET}"))
                for t in due_today[:3]:
                    desc = t.get("description", "")[:w-6]
                    print(box_line(f"  {RED}•{RESET} {desc}"))
                print()
            
            if due_week:
                print(box_line(f"{YELLOW}This Week{RESET}"))
                for t in due_week[:5]:
                    desc = t.get("description", "")[:w-18]
                    due = t.get("due", "")[:10] if t.get("due") else ""
                    print(box_line(f"  • {desc}  {DIM}{due}{RESET}"))
                print()
            
            if not due_today and not due_week:
                print(box_line(f"{GREEN}✓ No upcoming academic tasks{RESET}"))
                print()
        else:
            print(box_line(f"{DIM}taskwarrior not available{RESET}"))
            print()
        
        print(separator("─"))
        
        # Recent files section
        print(box_line(f"{MAGENTA}{BOLD}RECENT{RESET}"))
        print()
        
        recent_files = []
        for c in courses:
            for f in c.path.glob("lecture_*.*"):
                if f.suffix in ['.tex', '.org', '.pdf']:
                    recent_files.append((f.stat().st_mtime, f, c.name))
            psets_dir = c.path / "psets"
            if psets_dir.exists():
                for f in psets_dir.glob("hw_*.*"):
                    if f.suffix in ['.tex', '.org', '.pdf']:
                        recent_files.append((f.stat().st_mtime, f, c.name))
        
        recent_files.sort(reverse=True)
        seen = set()
        count = 0
        for mtime, f, cname in recent_files:
            # Dedupe by base name (show only one of .tex/.org/.pdf)
            base = f.stem
            if base in seen:
                continue
            seen.add(base)
            count += 1
            if count > 5:
                break
            
            age = today - datetime.fromtimestamp(mtime)
            if age.days == 0:
                age_str = f"{GREEN}today{RESET}"
            elif age.days == 1:
                age_str = f"{YELLOW}yesterday{RESET}"
            elif age.days < 7:
                age_str = f"{DIM}{age.days}d ago{RESET}"
            else:
                age_str = f"{DIM}{age.days}d{RESET}"
            
            # Shorten course name for display
            short_course = cname[:20] + ".." if len(cname) > 22 else cname
            file_display = f"{DIM}{short_course}/{RESET}{f.name}"
            
            import re
            visible_left = re.sub(r'\033\[[0-9;]*m', '', file_display)
            visible_right = re.sub(r'\033\[[0-9;]*m', '', age_str)
            space = w - len(visible_left) - len(visible_right)
            
            print(f"  {file_display}{' ' * max(1, space)}{age_str}  ")
        
        if not recent_files:
            print(box_line(f"{DIM}No files yet{RESET}"))
        
        print()
        
        # Footer
        print(separator("─"))
        sem = self.config.get("semester", "")
        print(box_line(f"{DIM}{sem}{RESET}                              {DIM}v2.1{RESET}"))
        print(f"{CYAN}" + separator("━") + RESET)
        print()

    def dashboard_json(self):
        """Output dashboard data as JSON for nvim integration"""
        courses = self.scan_courses()
        current = self._get_current_course()
        today = datetime.now()
        
        # Build courses list
        courses_data = []
        for c in courses:
            courses_data.append({
                "name": c.name,
                "code": c.code,
                "lectures": c.lecture_count,
                "psets": c.pset_count,
                "current": c.name == current
            })
        
        # Build tasks
        tasks_today = []
        tasks_week = []
        tasks_backlog = []
        if TaskWarrior.available():
            # Get all pending tasks
            all_pending = TaskWarrior.get_pending()
            
            # Filter for academic-related tasks (with tags or projects)
            course_projects = [c.name.replace("-","_") for c in courses]
            
            for t in all_pending:
                is_academic = ("academic" in t.get("tags", []) or 
                              "pset" in t.get("tags", []) or
                              any(proj in t.get("project","") for proj in course_projects))
                
                due = t.get("due")
                desc = t.get("description", "")
                task_data = {"description": desc, "due": due or "", "id": t.get("id", 0)}
                
                if due:
                    # Parse due date - only show tasks with due dates
                    try:
                        due_date = datetime.strptime(due[:8], "%Y%m%d")
                        days_until = (due_date - today.replace(hour=0, minute=0, second=0, microsecond=0)).days
                        if days_until <= 0:
                            tasks_today.append(task_data)
                        elif days_until <= 7:
                            tasks_week.append(task_data)
                    except:
                        pass
                elif is_academic:
                    # Only show unscheduled tasks if they're academic-related
                    tasks_backlog.append(task_data)
            
            # Limit each category
            tasks_today = tasks_today[:5]
            tasks_week = tasks_week[:5]
            tasks_backlog = tasks_backlog[:5]
        
        # Build recent files
        recent = []
        recent_files = []
        for c in courses:
            for f in c.path.glob("lecture_*.*"):
                if f.suffix in ['.tex', '.org']:
                    recent_files.append((f.stat().st_mtime, f, c.name))
            psets_dir = c.path / "psets"
            if psets_dir.exists():
                for f in psets_dir.glob("hw_*.*"):
                    if f.suffix in ['.tex', '.org']:
                        recent_files.append((f.stat().st_mtime, f, c.name))
        
        recent_files.sort(reverse=True)
        seen = set()
        for mtime, f, cname in recent_files[:5]:
            if f.stem in seen:
                continue
            seen.add(f.stem)
            age = today - datetime.fromtimestamp(mtime)
            if age.days == 0:
                age_str = "today"
            elif age.days == 1:
                age_str = "yesterday"
            else:
                age_str = f"{age.days}d ago"
            recent.append({"course": cname, "file": f.name, "age": age_str})
        
        output = {
            "current": current,
            "semester": self.config.get("semester", ""),
            "courses": courses_data,
            "tasks_today": tasks_today,
            "tasks_week": tasks_week,
            "tasks_backlog": tasks_backlog,
            "recent": recent
        }
        
        print(json.dumps(output))

    def list_courses(self):
        """List all courses"""
        courses = self.scan_courses()
        current = self._get_current_course()
        
        print(f"\n📚 Courses ({self.config.get('semester', '')}):\n")
        for c in courses:
            marker = "→" if c.name == current else " "
            code = f" [{c.code}]" if c.code else ""
            print(f"  {marker} {c.name}{code}")
            if c.instructor:
                print(f"      Instructor: {c.instructor}")
            if c.schedule:
                print(f"      Schedule: {c.schedule}")
            print(f"      Lectures: {c.lecture_count} | PSets: {c.pset_count}")
            print()
    
    def select_course(self, course: str = None):
        """Interactively select or set current course"""
        courses = self.scan_courses()
        
        if course:
            if any(c.name == course for c in courses):
                self._set_current_course(course)
                print(f"✅ Current course set to: {course}")
            else:
                print(f"❌ Course not found: {course}")
            return
        
        print("\nSelect a course:\n")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name}")
        
        try:
            choice = int(input("\nEnter number: ")) - 1
            if 0 <= choice < len(courses):
                self._set_current_course(courses[choice].name)
                print(f"✅ Current course set to: {courses[choice].name}")
        except (ValueError, IndexError):
            print("Invalid selection")

    def set_format(self, fmt: str):
        """Set default output format"""
        if fmt not in ("org", "tex"):
            print("❌ Format must be 'org' or 'tex'")
            return
        self.config["default_format"] = fmt
        self._save_config()
        print(f"✅ Default format set to: {fmt}")

    def cleanup_course(self, name: str = None, dry_run: bool = False):
        """Remove LaTeX auxiliary files from a course directory"""
        course = name or self._get_current_course()
        if not course:
            # Fall back to the current directory if it's a course under the root
            cwd = Path.cwd().resolve()
            if cwd.parent == self.root.resolve():
                course = cwd.name
        if not course:
            print("No course specified (run from inside a course, pass a name, or set a current course)")
            return
        course_dir = self.root / course
        if not course_dir.is_dir():
            print(f"Course directory not found: {course_dir}")
            return
        exts = ("aux", "log", "toc", "out", "synctex.gz", "bcf",
                "run.xml", "bbl", "blg", "fls", "fdb_latexmk", "nav", "snm")
        targets = [p for ext in exts for p in course_dir.rglob(f"*.{ext}")]
        if not targets:
            print(f"No auxiliary files to clean in {course}")
            return
        for p in targets:
            if dry_run:
                print(f"  would remove: {p.relative_to(self.root)}")
            else:
                try:
                    p.unlink()
                except OSError as e:
                    print(f"  failed: {p} ({e})")
        action = "Would remove" if dry_run else "Removed"
        print(f"✅ {action} {len(targets)} auxiliary file(s) in {course}")
    
    def info(self, course: str = None):
        """Show info about a course"""
        course = course or self._get_current_course()
        if not course:
            print("No course specified")
            return
        
        courses = self.scan_courses()
        c = next((x for x in courses if x.name == course), None)
        if not c:
            print(f"Course not found: {course}")
            return
        
        print(f"\n📖 {c.name}")
        if c.code: print(f"   Code: {c.code}")
        if c.instructor: print(f"   Instructor: {c.instructor}")
        if c.schedule: print(f"   Schedule: {c.schedule}")
        print(f"   Lectures: {c.lecture_count}")
        print(f"   Problem Sets: {c.pset_count}")
        print(f"   Path: {c.path}")
        
        # Show related tasks
        if TaskWarrior.available():
            project = course.replace("-", "_")
            tasks = TaskWarrior.get_pending(project)
            if tasks:
                print(f"\n   📋 Pending tasks:")
                for t in tasks[:5]:
                    desc = t.get("description", "")
                    print(f"      • {desc}")


# ----- Grades (folded in from grade_manager.py) -----
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
    parser = argparse.ArgumentParser(
        description="Academic CLI v2 - Modern Academic Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     Show dashboard
  %(prog)s new                 Create new lecture
  %(prog)s new --tex           Create new .tex lecture
  %(prog)s pset                Create new problem set
  %(prog)s course add Math-101 Add new course
  %(prog)s select              Select current course
  %(prog)s list                List all courses
  %(prog)s format tex          Set default format to tex
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # New lecture
    new_p = subparsers.add_parser("new", help="Create new lecture")
    new_p.add_argument("-c", "--course", help="Course name")
    new_p.add_argument("-t", "--topic", help="Lecture topic")
    new_p.add_argument("--tex", action="store_true", help="Create .tex file")
    new_p.add_argument("--org", action="store_true", help="Create .org file")
    
    # New pset
    pset_p = subparsers.add_parser("pset", help="Create new problem set")
    pset_p.add_argument("-c", "--course", help="Course name")
    pset_p.add_argument("-t", "--title", help="Problem set title")
    pset_p.add_argument("--tex", action="store_true", help="Create .tex file")
    pset_p.add_argument("--org", action="store_true", help="Create .org file")

    # Course management
    course_p = subparsers.add_parser("course", help="Course management")
    course_sub = course_p.add_subparsers(dest="course_action")
    
    add_c = course_sub.add_parser("add", help="Add new course")
    add_c.add_argument("name", help="Course name")
    add_c.add_argument("--code", default="", help="Course code")
    add_c.add_argument("--instructor", default="", help="Instructor")
    add_c.add_argument("--schedule", default="", help="Schedule")
    
    edit_c = course_sub.add_parser("edit", help="Edit course metadata")
    edit_c.add_argument("name", help="Course name")
    edit_c.add_argument("--code", help="Course code")
    edit_c.add_argument("--instructor", help="Instructor")
    edit_c.add_argument("--schedule", help="Schedule")

    clean_c = course_sub.add_parser("cleanup", help="Remove LaTeX aux files from a course")
    clean_c.add_argument("name", nargs="?", help="Course name (default: current)")
    clean_c.add_argument("--name", dest="name_opt", help="Course name (alternative to positional)")
    clean_c.add_argument("--dry-run", action="store_true", help="List files without deleting")
    
    # Other commands
    subparsers.add_parser("list", help="List all courses")
    dash_p = subparsers.add_parser("dashboard", aliases=["d"], help="Show dashboard")
    dash_p.add_argument("--json", action="store_true", help="Output as JSON")
    
    select_p = subparsers.add_parser("select", help="Select current course")
    select_p.add_argument("course", nargs="?", help="Course name")
    
    info_p = subparsers.add_parser("info", help="Show course info")
    info_p.add_argument("course", nargs="?", help="Course name")
    
    format_p = subparsers.add_parser("format", help="Set default format")
    format_p.add_argument("fmt", choices=["org", "tex"], help="Format")
    
    # Grades (folded in from grade_manager.py)
    grades_p = subparsers.add_parser("grades", help="Manage grades")
    grades_p.add_argument("action", choices=[
        "add-course", "add-category", "add-grade",
        "show", "show-all", "list", "export-latex"
    ])
    grades_p.add_argument("--course", "-c", help="Course name")
    grades_p.add_argument("--assignment", "-a", help="Assignment name")
    grades_p.add_argument("--grade", "-g", type=float, help="Grade received")
    grades_p.add_argument("--max", "-m", type=float, default=100.0, help="Maximum points")
    grades_p.add_argument("--category", "--cat", default="General", help="Grade category")
    grades_p.add_argument("--weight", "-w", type=float, help="Category weight percentage")
    grades_p.add_argument("--credits", type=float, default=3.0, help="Credit hours for course")

    args = parser.parse_args()
    mgr = AcademicManager()

    # Dispatch commands
    if args.command == "new":
        fmt = OutputFormat.TEX if args.tex else (OutputFormat.ORG if args.org else None)
        mgr.create_lecture(args.course, args.topic, fmt)
    
    elif args.command == "pset":
        fmt = OutputFormat.TEX if args.tex else (OutputFormat.ORG if args.org else None)
        mgr.create_pset(args.course, args.title, fmt)
    
    elif args.command == "course":
        if args.course_action == "add":
            mgr.add_course(args.name, args.code, args.instructor, args.schedule)
        elif args.course_action == "edit":
            mgr.update_course_meta(args.name, args.code, args.instructor, args.schedule)
            print(f"✅ Updated {args.name}")
        elif args.course_action == "cleanup":
            mgr.cleanup_course(args.name_opt or args.name, args.dry_run)
    
    elif args.command == "list":
        mgr.list_courses()
    
    elif args.command == "select":
        mgr.select_course(args.course)
    
    elif args.command == "info":
        mgr.info(args.course)
    
    elif args.command == "format":
        mgr.set_format(args.fmt)
    
    elif args.command == "grades":
        gm_inst = GradeManager()
        if args.action == "add-course":
            if not args.course:
                print("Course name required"); return
            gm_inst.add_course(args.course, args.credits)
        elif args.action == "add-category":
            if not args.course or not args.weight:
                print("Course name and weight required"); return
            gm_inst.add_category(args.course, args.category, args.weight)
        elif args.action == "add-grade":
            if not args.course or not args.assignment or args.grade is None:
                print("Course, assignment, and grade required"); return
            gm_inst.add_grade(args.course, args.assignment, args.grade, args.category, args.max)
        elif args.action == "show":
            if not args.course:
                print("Course name required"); return
            gm_inst.show_course_grades(args.course)
        elif args.action == "show-all":
            gm_inst.show_all_grades()
        elif args.action == "list":
            gm_inst.list_courses()
        elif args.action == "export-latex":
            if not args.course:
                print("Course name required"); return
            print(gm_inst.export_latex_table(args.course))

    elif args.command in ("dashboard", "d") or args.command is None:
        if hasattr(args, 'json') and args.json:
            mgr.dashboard_json()
        else:
            mgr.dashboard()


if __name__ == "__main__":
    main()
