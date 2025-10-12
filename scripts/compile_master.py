#!/usr/bin/env python3
"""
Standalone Master Compiler - Works with existing lecture files
Auto-cleans empty theorem brackets and compiles to master.pdf

Usage:
  python3 compile_master.py math55
  python3 compile_master.py math55 --open
  python3 compile_master.py --list
"""

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path

def clean_empty_optional_args(file_path):
    """Remove empty optional arguments from theorem environments"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern matches: \begin{theorem}[], \begin{lemma}[], etc.
    pattern = r'\\begin\{(theorem|lemma|corollary|proposition|definition|example|remark|proof|problem)\}\[\s*\]'
    cleaned = re.sub(pattern, r'\\begin{\1}', content)
    
    with open(file_path, 'w') as f:
        f.write(cleaned)
    
    return content != cleaned  # Return True if changes were made

class MasterCompiler:
    def __init__(self, root_dir="~/university"):
        self.root_dir = Path(root_dir).expanduser()
    
    def find_preamble(self):
        """Find preamble.tex location"""
        locations = [
            self.root_dir / "preamble.tex",
            Path.home() / ".config/latex/preamble.tex",
            Path.cwd() / "preamble.tex",
        ]
        
        for loc in locations:
            if loc.exists():
                return loc
        return None
    
    def extract_content(self, lecture_file):
        """Extract content from standalone lecture file"""
        with open(lecture_file, 'r') as f:
            lines = f.readlines()
        
        content_start = 0
        content_end = len(lines)
        in_document = False
        
        for i, line in enumerate(lines):
            if '\\begin{document}' in line:
                content_start = i + 1
                in_document = True
            elif '\\end{document}' in line and in_document:
                content_end = i
                break
        
        content = ''.join(lines[content_start:content_end])
        return content.strip()
    
    def compile_course(self, course_name, open_pdf=False, preamble_path="../preamble.tex", strip_mode=True):
        """Compile all lectures in a course into master.pdf"""
        course_path = self.root_dir / course_name
        
        if not course_path.exists():
            print(f"❌ Course directory not found: {course_path}")
            print(f"Available courses:")
            self.list_courses()
            return False
        
        preamble_path = self.find_preamble()
        if not preamble_path:
            print(f"⚠️  Warning: preamble.tex not found")
            print(f"   The master.tex will assume ../preamble.tex")
        
        # Find lecture files
        lecture_files = []
        flat_lectures = sorted(course_path.glob("lecture_*.tex"))
        lectures_dir = course_path / "lectures"
        subdir_lectures = []
        if lectures_dir.exists():
            subdir_lectures = sorted(lectures_dir.glob("lecture_*.tex"))
        
        if flat_lectures:
            lecture_files = flat_lectures
            lectures_relative = ""
        elif subdir_lectures:
            lecture_files = subdir_lectures
            lectures_relative = "lectures/"
        else:
            print(f"❌ No lecture files found in {course_path}")
            return False
        
        print(f"📚 Found {len(lecture_files)} lectures in {course_name}")
        
        if strip_mode:
            print(f"📝 Extracting content from standalone lecture files...")
            extracted_lectures = []
            for lecture_file in lecture_files:
                content = self.extract_content(lecture_file)
                extracted_lectures.append({
                    'name': lecture_file.stem,
                    'content': content
                })
            
            master_content = self.generate_master_tex_embedded(
                course_name,
                extracted_lectures,
                preamble_path
            )
        else:
            master_content = self.generate_master_tex(
                course_name, 
                lecture_files, 
                lectures_relative,
                preamble_path
            )
        
        # Write master.tex
        master_file = course_path / "master.tex"
        with open(master_file, 'w') as f:
            f.write(master_content)
        print(f"✓ Generated {master_file}")
        
        # Compile to PDF
        print(f"🔨 Compiling master.pdf...")
        success = self.compile_latex(course_path)
        
        if success:
            print(f"✅ Successfully created master.pdf")
            
            if open_pdf:
                pdf_file = course_path / "master.pdf"
                if pdf_file.exists():
                    self.open_pdf(pdf_file)
            
            return True
        else:
            print(f"❌ Compilation failed. Check master.log for errors.")
            return False
    
    def generate_master_tex(self, course_name, lecture_files, lectures_relative, preamble_path="../preamble.tex"):
        """Generate master.tex content"""
        input_lines = []
        for lecture in lecture_files:
            lecture_name = lecture.stem
            input_lines.append(f"\\input{{{lectures_relative}{lecture_name}.tex}}")
        
        inputs = "\n".join(input_lines)
        
        template = f"""\\documentclass{{report}}

% Load preamble
\\input{{{preamble_path}}}

% Optional: Customize these
\\course{{{course_name}}}
\\me{{Your Name}}

\\title{{\\Huge{{{course_name}}}\\\\XXXX -- Harvard University}}
\\author{{\\huge{{S. D. V. Stephens}}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle
\\newpage
\\pdfbookmark[section]{{\\contentsname}}{{toc}}
\\tableofcontents
\\pagebreak

% All lectures
{inputs}

\\end{{document}}
"""
        return template
    
    def generate_master_tex_embedded(self, course_name, extracted_lectures, preamble_path="../preamble.tex"):
        """Generate master.tex with embedded lecture content"""
        lecture_sections = []
        for lec in extracted_lectures:
            separator = "% " + "="*60
            section = f"{separator}\n% {lec['name']}\n{separator}\n\n{lec['content']}"
            lecture_sections.append(section)
        
        all_content = "\n\n".join(lecture_sections)
        
        template = f"""\\documentclass{{report}}

% Load preamble
\\input{{{preamble_path}}}

% Optional: Customize these
\\course{{{course_name.replace('_', ' ')}}}
\\me{{Your Name}}

\\title{{\\Huge{{{course_name.replace('_', ' ')}}}\\\\XXXX -- Harvard University}}
\\author{{\\huge{{S. D. V. Stephens}}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle
\\newpage
\\pdfbookmark[section]{{\\contentsname}}{{toc}}
\\tableofcontents
\\pagebreak

% ============================================
% ALL LECTURES (content extracted)
% ============================================

{all_content}

\\end{{document}}
"""
        return template
    
    def compile_latex(self, course_path):
        """Compile master.tex to PDF with auto-cleanup"""
        original_dir = os.getcwd()
        os.chdir(course_path)
        
        try:
            # Clean empty optional arguments BEFORE compiling
            master_file = course_path / "master.tex"
            if clean_empty_optional_args(master_file):
                print("✨ Auto-fixed empty theorem brackets")
            
            # Run pdflatex 3 times for TOC
            for i in range(3):
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "master.tex"],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"❌ pdflatex error (run {i+1}/3)")
                    return False
            
            return True
            
        except FileNotFoundError:
            print("❌ pdflatex not found. Make sure LaTeX is installed.")
            return False
        except Exception as e:
            print(f"❌ Error during compilation: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def open_pdf(self, pdf_file):
        """Open PDF in default viewer"""
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", str(pdf_file)])
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", str(pdf_file)])
            elif sys.platform == "win32":
                os.startfile(str(pdf_file))
        except Exception as e:
            print(f"Could not open PDF: {e}")
    
    def list_courses(self):
        """List available courses"""
        if not self.root_dir.exists():
            print(f"❌ Root directory not found: {self.root_dir}")
            return
        
        courses = []
        for item in self.root_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                has_flat = list(item.glob("lecture_*.tex"))
                has_subdir = list((item / "lectures").glob("lecture_*.tex")) if (item / "lectures").exists() else []
                
                if has_flat or has_subdir:
                    lecture_count = len(has_flat or has_subdir)
                    courses.append((item.name, lecture_count))
        
        if courses:
            print("\nAvailable courses:")
            for name, count in sorted(courses):
                print(f"  • {name} ({count} lectures)")
        else:
            print(f"\nNo courses with lecture files found in {self.root_dir}")
    
    def clean(self, course_name):
        """Clean auxiliary LaTeX files"""
        course_path = self.root_dir / course_name
        
        if not course_path.exists():
            print(f"❌ Course not found: {course_name}")
            return
        
        aux_extensions = ['.aux', '.log', '.toc', '.out', '.synctex.gz', '.bcf', '.run.xml', '.bbl', '.blg']
        
        for ext in aux_extensions:
            for file in course_path.glob(f"master{ext}"):
                file.unlink()
                print(f"🗑️  Deleted {file.name}")
        
        print("✓ Cleaned auxiliary files")

def main():
    parser = argparse.ArgumentParser(
        description="Compile lecture notes into master.pdf",
        epilog="Example: python3 compile_master.py math55 --open"
    )
    
    parser.add_argument("course", nargs="?", help="Course name")
    parser.add_argument("--open", "-o", action="store_true", help="Open PDF after compilation")
    parser.add_argument("--list", "-l", action="store_true", help="List available courses")
    parser.add_argument("--clean", "-c", action="store_true", help="Clean auxiliary files")
    parser.add_argument("--root", default="~/university", help="Root directory")
    parser.add_argument("--preamble", "-p", default="../preamble.tex", help="Path to preamble")
    parser.add_argument("--no-strip", action="store_true", help="Don't strip documentclass/preamble")
    
    args = parser.parse_args()
    compiler = MasterCompiler(args.root)
    
    if args.list:
        compiler.list_courses()
        return
    
    if args.clean:
        if not args.course:
            print("❌ Course name required for --clean")
            return
        compiler.clean(args.course)
        return
    
    if not args.course:
        print("❌ Course name required")
        compiler.list_courses()
        return
    
    strip_mode = not args.no_strip
    compiler.compile_course(args.course, args.open, args.preamble, strip_mode)

if __name__ == "__main__":
    main()
