#!/usr/bin/env python3
"""
Master Compiler - Simplified
Uses docmute package for clean inclusion of standalone lectures

Usage:
  python3 compile_master.py Studies-in-Algebra
  python3 compile_master.py Studies-in-Algebra --open
  python3 compile_master.py --list
"""

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path


def clean_empty_optional_args(content):
    """Remove empty optional arguments from theorem environments"""
    pattern = r'\\begin\{(theorem|lemma|corollary|proposition|definition|example|remark|proof|problem)\}\[\s*\]'
    return re.sub(pattern, r'\\begin{\1}', content)


class MasterCompiler:
    def __init__(self, root_dir="~/university"):
        self.root_dir = Path(root_dir).expanduser()
    
    def find_lectures(self, course_path):
        """Find lecture files in course directory"""
        # Check flat structure first
        flat = sorted(course_path.glob("lecture_*.tex"))
        if flat:
            return flat, ""
        
        # Check lectures/ subdirectory
        lectures_dir = course_path / "lectures"
        if lectures_dir.exists():
            subdir = sorted(lectures_dir.glob("lecture_*.tex"))
            if subdir:
                return subdir, "lectures/"
        
        return [], ""

    def generate_master(self, course_name, lectures, rel_path):
        """Generate master.tex using docmute package"""
        
        # Build include lines
        includes = []
        for lec in lectures:
            name = lec.stem
            includes.append(f"\\input{{{rel_path}{name}}}")
        
        includes_str = "\n".join(includes)
        
        return f"""\\documentclass{{report}}

% Load preamble
\\input{{~/university/preamble.tex}}
\\input{{~/university/preamble-darkmode.tex}}

% docmute: allows \\input of standalone documents (ignores their preamble)
\\usepackage{{docmute}}

\\course{{{course_name.replace('-', ' ')}}}

\\title{{\\Huge{{{course_name.replace('-', ' ')}}}\\\\Harvard University}}
\\author{{\\huge{{S. D. V. Stephens}}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle
\\newpage
\\pdfbookmark[section]{{\\contentsname}}{{toc}}
\\tableofcontents
\\pagebreak

% Include all lectures (docmute strips their preambles)
{includes_str}

\\end{{document}}
"""

    def compile(self, course_name, open_pdf=False):
        """Compile course to master.pdf"""
        course_path = self.root_dir / course_name
        
        if not course_path.exists():
            print(f"❌ Course not found: {course_name}")
            self.list_courses()
            return False
        
        lectures, rel_path = self.find_lectures(course_path)
        if not lectures:
            print(f"❌ No lectures found in {course_name}")
            return False
        
        print(f"📚 Found {len(lectures)} lectures")
        
        # Generate master.tex
        master_content = self.generate_master(course_name, lectures, rel_path)
        master_content = clean_empty_optional_args(master_content)
        
        master_file = course_path / "master.tex"
        master_file.write_text(master_content)
        print(f"✓ Generated master.tex")

        # Compile
        print(f"🔨 Compiling...")
        
        original_dir = os.getcwd()
        os.chdir(course_path)
        
        try:
            # Create output directories
            (course_path / ".latexmk").mkdir(exist_ok=True)
            
            # Run latexmk (handles multiple passes automatically)
            result = subprocess.run([
                "latexmk", "-pdf", "-interaction=nonstopmode",
                "-shell-escape", "-synctex=1",
                "master.tex"
            ], capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            if result.returncode != 0:
                print(f"❌ Compilation failed")
                print(result.stderr[-500:] if result.stderr else "No error output")
                return False
            
            print(f"✅ Created master.pdf")
            
            if open_pdf:
                subprocess.run(["zathura", "master.pdf"], start_new_session=True)
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Command not found: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def list_courses(self):
        """List available courses"""
        print("\n📚 Available courses:\n")
        for item in sorted(self.root_dir.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                lectures, _ = self.find_lectures(item)
                if lectures:
                    print(f"  • {item.name} ({len(lectures)} lectures)")


def main():
    parser = argparse.ArgumentParser(description="Compile lectures to master.pdf")
    parser.add_argument("course", nargs="?", help="Course name")
    parser.add_argument("--open", "-o", action="store_true", help="Open PDF after")
    parser.add_argument("--list", "-l", action="store_true", help="List courses")
    
    args = parser.parse_args()
    compiler = MasterCompiler()
    
    if args.list:
        compiler.list_courses()
        return
    
    if not args.course:
        print("Usage: compile_master.py COURSE [--open]")
        compiler.list_courses()
        return
    
    compiler.compile(args.course, args.open)


if __name__ == "__main__":
    main()
