#!/usr/bin/env python3
"""
Ipe Figures Integration for LaTeX Workflow
Dark mode support + auto-export + neovim integration
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

# Optional watchdog for file watching
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

class IpeFigures:
    def __init__(self, dark_mode=True):
        self.dark_mode = dark_mode
        
    def get_template(self):
        """Return Ipe template with proper preamble"""
        # Colors for dark mode
        if self.dark_mode:
            bg_color = "0.161 0.192 0.2"  # #293133 (pag)
            stroke_color = "1 1 1"  # white
            extra_colors = '''
<color name="p1" value="0.792 0.941 0.973"/>
<color name="p2" value="0.678 0.91 0.957"/>
<color name="p3" value="0.565 0.878 0.937"/>
<color name="p4" value="0.282 0.792 0.894"/>
<color name="p5" value="0 0.706 0.847"/>
<color name="p6" value="0 0.588 0.78"/>
<color name="p7" value="0 0.467 0.714"/>
<color name="p8" value="0.008 0.243 0.541"/>
<color name="p9" value="0.012 0.016 0.369"/>
<color name="pag" value="0.161 0.192 0.2"/>
<color name="white" value="1 1 1"/>
<color name="matred" value="0.957 0.263 0.212"/>
<color name="matblue" value="0.129 0.588 0.953"/>
<color name="matgreen" value="0.298 0.686 0.314"/>
<color name="matyellow" value="1 0.922 0.231"/>
<color name="matorange" value="1 0.596 0"/>
<color name="matpurple" value="0.612 0.153 0.69"/>'''
        else:
            bg_color = "1 1 1"
            stroke_color = "0 0 0"
            extra_colors = ""

        return f'''<?xml version="1.0"?>
<!DOCTYPE ipe SYSTEM "ipe.dtd">
<ipe version="70218" creator="Ipe 7.2.24">
<info created="D:20240101000000" modified="D:20240101000000"/>
<preamble>
\\input{{/Users/stephens1/university/preamble.tex}}
{"\\input{/Users/stephens1/university/preamble-darkmode.tex}" if self.dark_mode else ""}
</preamble>
<ipestyle name="custom">
{extra_colors}
<color name="red" value="1 0 0"/>
<color name="green" value="0 1 0"/>
<color name="blue" value="0 0 1"/>
<color name="yellow" value="1 1 0"/>
<color name="orange" value="1 0.647 0"/>
<color name="purple" value="0.627 0.125 0.941"/>
<color name="gray" value="0.745"/>
<color name="darkgray" value="0.4"/>
<color name="lightgray" value="0.9"/>
<dashstyle name="dashed" value="[4] 0"/>
<dashstyle name="dotted" value="[1 3] 0"/>
<dashstyle name="dash dotted" value="[4 2 1 2] 0"/>
<pen name="heavier" value="0.8"/>
<pen name="fat" value="1.2"/>
<pen name="ultrafat" value="2"/>
<textsize name="large" value="\\large"/>
<textsize name="Large" value="\\Large"/>
<textsize name="LARGE" value="\\LARGE"/>
<textsize name="huge" value="\\huge"/>
<textsize name="small" value="\\small"/>
<textsize name="footnote" value="\\footnotesize"/>
<textsize name="tiny" value="\\tiny"/>
<symbolsize name="small" value="2"/>
<symbolsize name="tiny" value="1.1"/>
<symbolsize name="large" value="5"/>
<arrowsize name="small" value="5"/>
<arrowsize name="large" value="10"/>
<gridsize name="4 pts" value="4"/>
<gridsize name="8 pts" value="8"/>
<gridsize name="16 pts" value="16"/>
<opacity name="25%" value="0.25"/>
<opacity name="50%" value="0.5"/>
<opacity name="75%" value="0.75"/>
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
        pdf_file = figures_path / f"{clean_name}.pdf"
        
        # Create Ipe file if it doesn't exist
        if not ipe_file.exists():
            with open(ipe_file, 'w') as f:
                f.write(self.get_template())
            print(f"✅ Created {ipe_file}")
        else:
            print(f"📂 Opening existing {ipe_file}")
        
        # Return info for neovim
        return {
            "name": clean_name,
            "ipe": str(ipe_file),
            "pdf": str(pdf_file),
            "latex": f"\\incipe{{{clean_name}}}"
        }
    
    def open_ipe(self, ipe_file):
        """Open file in Ipe with proper PATH"""
        env = os.environ.copy()
        env['PATH'] = '/Library/TeX/texbin:' + env.get('PATH', '')
        subprocess.Popen(['open', '-a', 'Ipe', str(ipe_file)], env=env)

    def export_pdf(self, ipe_file):
        """Export Ipe file to PDF"""
        ipe_path = Path(ipe_file)
        pdf_path = ipe_path.with_suffix('.pdf')
        
        if not ipe_path.exists():
            print(f"❌ File not found: {ipe_file}")
            return None
        
        env = os.environ.copy()
        env['PATH'] = '/Library/TeX/texbin:' + env.get('PATH', '')
        
        try:
            # Use ipetoipe for conversion
            result = subprocess.run(
                ['ipetoipe', '-pdf', str(ipe_path), str(pdf_path)],
                capture_output=True, text=True, env=env
            )
            if result.returncode == 0:
                print(f"✅ Exported {pdf_path.name}")
                return str(pdf_path)
            else:
                print(f"⚠️  ipetoipe error: {result.stderr}")
                return None
        except FileNotFoundError:
            print("❌ ipetoipe not found. Install with: brew install ipe")
            return None

    def export_svg(self, ipe_file):
        """Export Ipe file to SVG"""
        ipe_path = Path(ipe_file)
        svg_path = ipe_path.with_suffix('.svg')
        
        env = os.environ.copy()
        env['PATH'] = '/Library/TeX/texbin:' + env.get('PATH', '')
        
        try:
            result = subprocess.run(
                ['ipetoipe', '-svg', str(ipe_path), str(svg_path)],
                capture_output=True, text=True, env=env
            )
            if result.returncode == 0:
                print(f"✅ Exported {svg_path.name}")
                return str(svg_path)
        except FileNotFoundError:
            pass
        return None

    def list_figures(self, figures_dir="./figures"):
        """List all Ipe figures in directory"""
        figures_path = Path(figures_dir)
        if not figures_path.exists():
            return []
        
        figures = []
        for ipe_file in sorted(figures_path.glob("*.ipe")):
            pdf_exists = ipe_file.with_suffix('.pdf').exists()
            figures.append({
                "name": ipe_file.stem,
                "ipe": str(ipe_file),
                "pdf": str(ipe_file.with_suffix('.pdf')) if pdf_exists else None,
                "has_pdf": pdf_exists
            })
        return figures

    def edit(self, name, figures_dir="./figures"):
        """Edit existing figure"""
        figures_path = Path(figures_dir)
        clean_name = name.lower().replace(' ', '-')
        ipe_file = figures_path / f"{clean_name}.ipe"
        
        if ipe_file.exists():
            self.open_ipe(ipe_file)
            return {"name": clean_name, "ipe": str(ipe_file)}
        else:
            print(f"❌ Figure not found: {clean_name}")
            return None


if HAS_WATCHDOG:
    class IpeWatcher(FileSystemEventHandler):
        """Watch for Ipe file changes and auto-export"""
        
        def __init__(self, ipe_figures):
            self.ipe = ipe_figures
            self.last_export = {}
        
        def on_modified(self, event):
            if event.is_directory:
                return
            if event.src_path.endswith('.ipe'):
                # Debounce - don't export more than once per second
                now = time.time()
                last = self.last_export.get(event.src_path, 0)
                if now - last < 1:
                    return
                self.last_export[event.src_path] = now
                
                print(f"🔄 Change detected: {Path(event.src_path).name}")
                self.ipe.export_pdf(event.src_path)


def watch_figures(figures_dir, dark_mode=True):
    """Watch directory for Ipe file changes"""
    if not HAS_WATCHDOG:
        print("❌ watchdog not installed. Run: pip3 install watchdog")
        return
        
    figures_path = Path(figures_dir)
    figures_path.mkdir(exist_ok=True)
    
    ipe = IpeFigures(dark_mode=dark_mode)
    handler = IpeWatcher(ipe)
    observer = Observer()
    observer.schedule(handler, str(figures_path), recursive=False)
    observer.start()
    
    print(f"👁️  Watching {figures_path} for changes...")
    print("   Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(description="Ipe Figures for LaTeX")
    parser.add_argument("command", choices=["create", "edit", "list", "export", "watch", "export-all"])
    parser.add_argument("name", nargs="?", help="Figure name")
    parser.add_argument("-d", "--dir", default="./figures", help="Figures directory")
    parser.add_argument("--light", action="store_true", help="Use light mode template")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    ipe = IpeFigures(dark_mode=not args.light)
    
    if args.command == "create":
        if not args.name:
            args.name = input("Figure name: ").strip()
        if args.name:
            result = ipe.create(args.name, args.dir)
            if args.json:
                import json
                print(json.dumps(result))
            else:
                ipe.open_ipe(result["ipe"])
                print(f"📋 LaTeX: {result['latex']}")

    elif args.command == "edit":
        if not args.name:
            # Show list and let user pick
            figures = ipe.list_figures(args.dir)
            if not figures:
                print("No figures found")
                return
            for i, f in enumerate(figures, 1):
                status = "✓" if f["has_pdf"] else "○"
                print(f"  {i}. {status} {f['name']}")
            try:
                choice = int(input("Select figure: ")) - 1
                args.name = figures[choice]["name"]
            except (ValueError, IndexError):
                return
        ipe.edit(args.name, args.dir)
    
    elif args.command == "list":
        figures = ipe.list_figures(args.dir)
        if args.json:
            import json
            print(json.dumps(figures))
        else:
            if not figures:
                print("No figures found")
            else:
                print("📊 Ipe Figures:")
                for f in figures:
                    status = "✓" if f["has_pdf"] else "○"
                    print(f"  {status} {f['name']}")
    
    elif args.command == "export":
        if args.name:
            figures_path = Path(args.dir)
            ipe_file = figures_path / f"{args.name}.ipe"
            ipe.export_pdf(ipe_file)
        else:
            print("Specify figure name")
    
    elif args.command == "export-all":
        figures = ipe.list_figures(args.dir)
        for f in figures:
            ipe.export_pdf(f["ipe"])
    
    elif args.command == "watch":
        watch_figures(args.dir, dark_mode=not args.light)


if __name__ == "__main__":
    main()
