#!/usr/bin/env python3
"""
Ipe Figures Integration for LaTeX Workflow
A simpler alternative to inkscape-figures
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class IpeFigures:
    def __init__(self):
        self.ipe_template = '''<?xml version="1.0"?>
<!DOCTYPE ipe SYSTEM "ipe.dtd">
<ipe version="70218" creator="Ipe 7.2.24">
<info created="D:20240101000000" modified="D:20240101000000"/>
<preamble>
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{amsfonts}
\\usepackage{mathtools}
</preamble>
<ipestyle name="basic">
<symbol name="arrow/arc(spx)">
<path stroke="sym-stroke" fill="sym-stroke" pen="sym-pen">
0 0 m
-1.0 0.333 l
-1.0 -0.333 l
h
</path>
</symbol>
<symbol name="arrow/normal(spx)">
<path stroke="sym-stroke" fill="sym-stroke" pen="sym-pen">
0 0 m
-1.0 0.333 l
-1.0 -0.333 l
h
</path>
</symbol>
</ipestyle>
<page>
<layer name="alpha"/>
<view layers="alpha" active="alpha"/>
</page>
</ipe>'''
    
    def create(self, name, figures_dir="./figures"):
        """Create a new Ipe figure"""
        figures_path = Path(figures_dir)
        figures_path.mkdir(exist_ok=True)
        
        # Clean the name
        clean_name = name.lower().replace(' ', '-')
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c in '-_')
        
        ipe_file = figures_path / f"{clean_name}.ipe"
        
        # Create Ipe file if it doesn't exist
        if not ipe_file.exists():
            with open(ipe_file, 'w') as f:
                f.write(self.ipe_template)
            print(f"Created {ipe_file}")
        else:
            print(f"Opening existing {ipe_file}")
        
        # Open in Ipe
        try:
            subprocess.run(['open', '-a', 'Ipe', str(ipe_file)])
            print(f"Opened {clean_name}.ipe in Ipe")
            return clean_name
        except Exception as e:
            print(f"Error opening Ipe: {e}")
            print("Make sure Ipe is installed: brew install --cask ipe")
            return None
    
    def edit(self, name, figures_dir="./figures"):
        """Edit an existing Ipe figure"""
        figures_path = Path(figures_dir)
        clean_name = name.lower().replace(' ', '-')
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c in '-_')
        
        ipe_file = figures_path / f"{clean_name}.ipe"
        
        if ipe_file.exists():
            subprocess.run(['open', '-a', 'Ipe', str(ipe_file)])
            print(f"Opened {clean_name}.ipe for editing")
        else:
            print(f"Figure {clean_name}.ipe not found. Use 'create' to make a new one.")
    
    def list_figures(self, figures_dir="./figures"):
        """List all Ipe figures in directory"""
        figures_path = Path(figures_dir)
        if not figures_path.exists():
            print("No figures directory found")
            return
        
        ipe_files = list(figures_path.glob("*.ipe"))
        if ipe_files:
            print("Available Ipe figures:")
            for ipe_file in sorted(ipe_files):
                pdf_file = ipe_file.with_suffix('.pdf')
                status = "✓" if pdf_file.exists() else "○"
                print(f"  {status} {ipe_file.stem}")
        else:
            print("No Ipe figures found")
    
    def export_pdf(self, name, figures_dir="./figures"):
        """Export Ipe figure to PDF (if Ipe command line tools available)"""
        figures_path = Path(figures_dir)
        clean_name = name.lower().replace(' ', '-')
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c in '-_')
        
        ipe_file = figures_path / f"{clean_name}.ipe"
        pdf_file = figures_path / f"{clean_name}.pdf"
        
        if not ipe_file.exists():
            print(f"Figure {clean_name}.ipe not found")
            return
        
        try:
            # Try to use ipetoipe command if available
            result = subprocess.run(['ipetoipe', '-pdf', str(ipe_file), str(pdf_file)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Exported {clean_name}.ipe to PDF")
            else:
                print("ipetoipe not available. Export manually from Ipe: File → Export as PDF")
        except FileNotFoundError:
            print("Manual export needed: In Ipe, go to File → Export as PDF")

def main():
    parser = argparse.ArgumentParser(description="Ipe Figures for LaTeX")
    parser.add_argument("command", choices=["create", "edit", "list", "export"])
    parser.add_argument("name", nargs="?", help="Figure name")
    parser.add_argument("figures_dir", nargs="?", default="./figures", help="Figures directory")
    
    args = parser.parse_args()
    ipe = IpeFigures()
    
    if args.command == "create":
        if not args.name:
            args.name = input("Figure name: ").strip()
        if args.name:
            ipe.create(args.name, args.figures_dir)
    
    elif args.command == "edit":
        if not args.name:
            print("Figure name required for editing")
            return
        ipe.edit(args.name, args.figures_dir)
    
    elif args.command == "list":
        ipe.list_figures(args.figures_dir)
    
    elif args.command == "export":
        if not args.name:
            print("Figure name required for export")
            return
        ipe.export_pdf(args.name, args.figures_dir)

if __name__ == "__main__":
    main()
