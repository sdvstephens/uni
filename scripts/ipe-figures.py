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
\\input{/Users/stephens1/university/preamble.tex}
</preamble>
<ipestyle name="basic">
<color name="red" value="1 0 0"/>
<color name="green" value="0 1 0"/>
<color name="blue" value="0 0 1"/>
<color name="yellow" value="1 1 0"/>
<color name="orange" value="1 0.647 0"/>
<color name="gold" value="1 0.843 0"/>
<color name="purple" value="0.627 0.125 0.941"/>
<color name="gray" value="0.745 0.745 0.745"/>
<color name="brown" value="0.647 0.165 0.165"/>
<color name="navy" value="0 0 0.502"/>
<color name="pink" value="1 0.753 0.796"/>
<color name="seagreen" value="0.18 0.545 0.341"/>
<color name="turquoise" value="0.251 0.878 0.816"/>
<color name="violet" value="0.933 0.51 0.933"/>
<color name="darkblue" value="0 0 0.545"/>
<color name="darkcyan" value="0 0.545 0.545"/>
<color name="darkgray" value="0.663 0.663 0.663"/>
<color name="darkgreen" value="0 0.392 0"/>
<color name="darkmagenta" value="0.545 0 0.545"/>
<color name="darkorange" value="1 0.549 0"/>
<color name="darkred" value="0.545 0 0"/>
<color name="lightblue" value="0.678 0.847 0.902"/>
<color name="lightcyan" value="0.878 1 1"/>
<color name="lightgray" value="0.827 0.827 0.827"/>
<color name="lightgreen" value="0.565 0.933 0.565"/>
<color name="lightyellow" value="1 1 0.878"/>
<dashstyle name="dashed" value="[4] 0"/>
<dashstyle name="dotted" value="[1 3] 0"/>
<dashstyle name="dash dotted" value="[4 2 1 2] 0"/>
<dashstyle name="dash dot dotted" value="[4 2 1 2 1 2] 0"/>
<pen name="heavier" value="0.8"/>
<pen name="fat" value="1.2"/>
<pen name="ultrafat" value="2"/>
<textsize name="large" value="\large"/>
<textsize name="Large" value="\Large"/>
<textsize name="LARGE" value="\LARGE"/>
<textsize name="huge" value="\huge"/>
<textsize name="Huge" value="\Huge"/>
<textsize name="small" value="\small"/>
<textsize name="footnote" value="\footnotesize"/>
<textsize name="script" value="\scriptsize"/>
<textsize name="tiny" value="\tiny"/>
<symbolsize name="small" value="2"/>
<symbolsize name="tiny" value="1.1"/>
<symbolsize name="large" value="5"/>
<arrowsize name="small" value="5"/>
<arrowsize name="tiny" value="3"/>
<arrowsize name="large" value="10"/>
<gridsize name="4 pts" value="4"/>
<gridsize name="8 pts (~3 mm)" value="8"/>
<gridsize name="16 pts (~6 mm)" value="16"/>
<gridsize name="32 pts (~12 mm)" value="32"/>
<gridsize name="10 pts (~3.5 mm)" value="10"/>
<gridsize name="20 pts (~7 mm)" value="20"/>
<gridsize name="14 pts (~5 mm)" value="14"/>
<gridsize name="28 pts (~10 mm)" value="28"/>
<gridsize name="56 pts (~20 mm)" value="56"/>
<anglesize name="90 deg" value="90"/>
<anglesize name="60 deg" value="60"/>
<anglesize name="45 deg" value="45"/>
<anglesize name="30 deg" value="30"/>
<anglesize name="22.5 deg" value="22.5"/>
<symbol name="mark/circle(sx)" transformations="translations">
<path fill="sym-stroke">
0.6 0 0 0.6 0 0 e 0.4 0 0 0.4 0 0 e
</path></symbol>
<symbol name="mark/disk(sx)" transformations="translations">
<path fill="sym-stroke">
0.6 0 0 0.6 0 0 e
</path></symbol>
<symbol name="mark/fdisk(sfx)" transformations="translations">
<group><path fill="sym-fill">
0.5 0 0 0.5 0 0 e
</path><path fill="sym-stroke" fillrule="eofill">
0.6 0 0 0.6 0 0 e 0.4 0 0 0.4 0 0 e
</path></group></symbol>
<symbol name="mark/box(sx)" transformations="translations">
<path fill="sym-stroke" fillrule="eofill">
-0.6 -0.6 m 0.6 -0.6 l 0.6 0.6 l -0.6 0.6 l h
-0.4 -0.4 m 0.4 -0.4 l 0.4 0.4 l -0.4 0.4 l h</path></symbol>
<symbol name="mark/square(sx)" transformations="translations">
<path fill="sym-stroke">
-0.6 -0.6 m 0.6 -0.6 l 0.6 0.6 l -0.6 0.6 l h</path></symbol>
<symbol name="mark/fsquare(sfx)" transformations="translations">
<group><path fill="sym-fill">
-0.5 -0.5 m 0.5 -0.5 l 0.5 0.5 l -0.5 0.5 l h</path>
<path fill="sym-stroke" fillrule="eofill">
-0.6 -0.6 m 0.6 -0.6 l 0.6 0.6 l -0.6 0.6 l h
-0.4 -0.4 m 0.4 -0.4 l 0.4 0.4 l -0.4 0.4 l h</path></group></symbol>
<symbol name="mark/cross(sx)" transformations="translations">
<group><path fill="sym-stroke">
-0.43 -0.57 m 0.57 0.43 l 0.43 0.57 l -0.57 -0.43 l h</path>
<path fill="sym-stroke">
-0.43 0.57 m 0.57 -0.43 l 0.43 -0.57 l -0.57 0.43 l h</path>
</group></symbol>
<symbol name="arrow/arc(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
0 0 m -1.0 0.333 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/farc(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0 0 m -1.0 0.333 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/ptarc(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
0 0 m -1.0 0.333 l -0.8 0 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/fptarc(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0 0 m -1.0 0.333 l -0.8 0 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/fnormal(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0 0 m -1.0 0.333 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/pointed(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
0 0 m -1.0 0.333 l -0.8 0 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/fpointed(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0 0 m -1.0 0.333 l -0.8 0 l -1.0 -0.333 l h</path></symbol>
<symbol name="arrow/linear(spx)">
<path pen="sym-pen" stroke="sym-stroke">
-1.0 0.333 m 0 0 l -1.0 -0.333 l</path></symbol>
<symbol name="arrow/fdouble(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0 0 m -1.0 0.333 l -1.0 -0.333 l h
-1 0 m -2.0 0.333 l -2.0 -0.333 l h
</path></symbol>
<symbol name="arrow/double(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
0 0 m -1.0 0.333 l -1.0 -0.333 l h
-1 0 m -2.0 0.333 l -2.0 -0.333 l h
</path></symbol>
<symbol name="arrow/mid-normal(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
0.5 0 m -0.5 0.333 l -0.5 -0.333 l h
</path></symbol>
<symbol name="arrow/mid-fnormal(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0.5 0 m -0.5 0.333 l -0.5 -0.333 l h
</path></symbol>
<symbol name="arrow/mid-pointed(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
0.5 0 m -0.5 0.333 l -0.3 0 l -0.5 -0.333 l h</path></symbol>
<symbol name="arrow/mid-fpointed(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
0.5 0 m -0.5 0.333 l -0.3 0 l -0.5 -0.333 l h</path></symbol>
<symbol name="arrow/mid-double(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="sym-stroke">
1 0 m -0 0.333 l 0 -0.333 l h
0 0 m -1 0.333 l -1 -0.333 l h
</path></symbol>
<symbol name="arrow/mid-fdouble(spx)">
<path pen="sym-pen" stroke="sym-stroke" fill="white">
1 0 m -0 0.333 l 0 -0.333 l h
0 0 m -1 0.333 l -1 -0.333 l h
</path></symbol>
<opacity name="10%" value="0.1"/>
<opacity name="30%" value="0.3"/>
<opacity name="50%" value="0.5"/>
<opacity name="75%" value="0.75"/>
<tiling name="falling" angle="-60" width="1" step="4"/>
<tiling name="rising" angle="30" width="1" step="4"/>
<textstyle name="center" begin="\begin{center}"
end="\end{center}"/>
<textstyle name="itemize" begin="\begin{itemize}"
end="\end{itemize}"/>
<textstyle name="item" begin="\begin{itemize}\item{}"
end="\end{itemize}"/>
</ipestyle> '''


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
# Open in Ipe
        try:
            env = os.environ.copy()
            env['PATH'] = '/Library/TeX/texbin:' + env['PATH']
            subprocess.run(['open', '-a', 'Ipe', str(ipe_file)], env=env)
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
