#!/usr/bin/env python3
"""
Setup Anki note types with MathJax support for custom LaTeX macros.
Requires: Anki running with AnkiConnect addon (2055492159)

Usage: python3 anki-mathjax-setup.py
"""

import json
import urllib.request

ANKI_CONNECT_URL = "http://localhost:8765"

def anki_request(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload.encode())
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    if result.get("error"):
        raise Exception(f"AnkiConnect error: {result['error']}")
    return result.get("result")

# MathJax 3 config with all custom macros from preamble.tex
MATHJAX_SCRIPT = r"""
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    macros: {
      // Number sets
      RR: ['\\mathbb{R}^{#1}', 1, ''],
      NN: ['\\mathbb{N}^{#1}', 1, ''],
      ZZ: ['\\mathbb{Z}^{#1}', 1, ''],
      QQ: ['\\mathbb{Q}^{#1}', 1, ''],
      CC: ['\\mathbb{C}^{#1}', 1, ''],
      PP: ['\\mathbb{P}^{#1}', 1, ''],
      HH: ['\\mathbb{H}^{#1}', 1, ''],
      FF: ['\\mathbb{F}^{#1}', 1, ''],
      EE: '\\mathbb{E}',

      // Calligraphic
      mcA: '\\mathcal{A}', mcB: '\\mathcal{B}', mcC: '\\mathcal{C}',
      mcD: '\\mathcal{D}', mcE: '\\mathcal{E}', mcF: '\\mathcal{F}',
      mcG: '\\mathcal{G}', mcH: '\\mathcal{H}', mcI: '\\mathcal{I}',
      mcJ: '\\mathcal{J}', mcK: '\\mathcal{K}', mcL: '\\mathcal{L}',
      mcM: '\\mathcal{M}', mcN: '\\mathcal{N}', mcO: '\\mathcal{O}',
      mcP: '\\mathcal{P}', mcQ: '\\mathcal{Q}', mcR: '\\mathcal{R}',
      mcS: '\\mathcal{S}', mcT: '\\mathcal{T}', mcU: '\\mathcal{U}',
      mcV: '\\mathcal{V}', mcW: '\\mathcal{W}', mcX: '\\mathcal{X}',
      mcY: '\\mathcal{Y}', mcZ: '\\mathcal{Z}',

      // Fraktur (Lie algebras & primes)
      kg: '\\mathfrak{g}', kh: '\\mathfrak{h}', kn: '\\mathfrak{n}',
      kb: '\\mathfrak{b}', ku: '\\mathfrak{u}', kz: '\\mathfrak{z}',
      kp: '\\mathfrak{p}', kq: '\\mathfrak{q}', km: '\\mathfrak{m}',
      gl: '{\\operatorname{\\mathfrak{gl}}}',
      slie: '{\\operatorname{\\mathfrak{sl}}}',

      // Script
      sA: '\\mathscr{A}', sB: '\\mathscr{B}', sC: '\\mathscr{C}',
      sD: '\\mathscr{D}', sE: '\\mathscr{E}', sF: '\\mathscr{F}',
      sG: '\\mathscr{G}', sH: '\\mathscr{H}',

      // Operators
      Hom: '\\operatorname{Hom}',
      End: '\\operatorname{End}',
      Aut: '\\operatorname{Aut}',
      Inn: '\\operatorname{Inn}',
      Mor: '\\operatorname{Mor}',
      Ext: '\\operatorname{Ext}',
      Tor: '\\operatorname{Tor}',
      Ker: '\\operatorname{Ker}',
      Img: '\\operatorname{Im}',
      coker: '\\operatorname{coker}',
      Coker: '\\operatorname{Coker}',
      rank: '\\operatorname{rank}',
      Spec: '\\operatorname{Spec}',
      Tr: '\\operatorname{Tr}',
      Gal: '\\operatorname{Gal}',
      Syl: '\\operatorname{Syl}',
      Sym: '\\operatorname{Sym}',
      Stab: '\\operatorname{Stab}',
      sgn: '\\operatorname{sgn}',
      diag: '\\operatorname{diag}',
      img: '\\operatorname{im}',
      ord: '\\operatorname{ord}',
      diam: '\\operatorname{diam}',
      GL: '\\operatorname{GL}',
      SL: '\\operatorname{SL}',

      // Arrows & maps
      injto: '\\hookrightarrow',
      surjto: '\\twoheadrightarrow',
      taking: ['\\xrightarrow{#1}', 1],
      inv: '^{-1}',

      // Derivatives
      od: ['\\frac{\\mathrm{d} #1}{\\mathrm{d} #2}', 2],
      odd: ['\\dfrac{\\mathrm{d} #1}{\\mathrm{d} #2}', 2],
      pd: ['\\frac{\\partial #1}{\\partial #2}', 2],
      pdd: ['\\dfrac{\\partial #1}{\\partial #2}', 2],
      del: '\\partial',

      // Formatting
      ol: ['\\overline{#1}', 1],
      ul: ['\\underline{#1}', 1],
      wt: ['\\widetilde{#1}', 1],
      wh: ['\\widehat{#1}', 1],
      dboxed: ['\\boxed{#1}', 1],
      vocab: ['\\textbf{\\color{blue}{#1}}', 1],

      // Misc
      defeq: '\\overset{\\mathrm{def}}{=}',
      eps: '\\epsilon',
      veps: '\\varepsilon',
      lm: '\\lambda',
      id: '\\text{id}',
      half: '\\frac{1}{2}',
      bs: ['\\boldsymbol{#1}', 1],
    }
  }
};
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
"""

CARD_CSS = """
.card {
  font-family: 'Iowan Old Style', 'Palatino', Georgia, serif;
  font-size: 18px;
  text-align: left;
  color: #1a1a2e;
  background-color: #fafafa;
  padding: 20px 30px;
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto;
}
.card.nightMode {
  color: #e0e0e0;
  background-color: #1a1a2e;
}
mjx-container {
  font-size: 110% !important;
}
hr { border: 1px solid #ccc; margin: 15px 0; }
"""

FRONT_TEMPLATE = MATHJAX_SCRIPT + """
{{Front}}
"""

BACK_TEMPLATE = MATHJAX_SCRIPT + """
{{FrontSide}}
<hr id=answer>
{{Back}}
"""

CLOZE_FRONT = MATHJAX_SCRIPT + """
{{cloze:Text}}
"""

CLOZE_BACK = MATHJAX_SCRIPT + """
{{cloze:Text}}
<br><br>
{{Back Extra}}
"""

def create_latex_basic_model():
    """Create 'LaTeX Basic' note type with MathJax macros."""
    existing = anki_request("modelNames")

    if "LaTeX Basic" in existing:
        print("✅ 'LaTeX Basic' note type already exists")
        # Update templates to ensure macros are current
        anki_request("updateModelTemplates", model={
            "name": "LaTeX Basic",
            "templates": {
                "Card 1": {
                    "Front": FRONT_TEMPLATE,
                    "Back": BACK_TEMPLATE,
                }
            }
        })
        anki_request("updateModelStyling", model={
            "name": "LaTeX Basic",
            "css": CARD_CSS,
        })
        print("   → Updated templates with latest macros")
        return

    anki_request("createModel",
        modelName="LaTeX Basic",
        inOrderFields=["Front", "Back"],
        css=CARD_CSS,
        cardTemplates=[{
            "Name": "Card 1",
            "Front": FRONT_TEMPLATE,
            "Back": BACK_TEMPLATE,
        }],
    )
    print("✅ Created 'LaTeX Basic' note type")


def update_existing_models():
    """Inject MathJax macros into existing Basic and Cloze models."""
    models_to_update = {
        "Basic": {
            "Card 1": {"Front": FRONT_TEMPLATE.replace("{{Front}}", "{{Front}}"),
                       "Back": BACK_TEMPLATE}
        },
    }

    for model_name, templates in models_to_update.items():
        try:
            anki_request("updateModelTemplates", model={
                "name": model_name,
                "templates": templates,
            })
            anki_request("updateModelStyling", model={
                "name": model_name,
                "css": CARD_CSS,
            })
            print(f"✅ Updated '{model_name}' with MathJax macros")
        except Exception as e:
            print(f"⚠️  Could not update '{model_name}': {e}")


def list_decks():
    """Show available decks."""
    decks = anki_request("deckNames")
    print("\n📚 Available decks:")
    for d in sorted(decks):
        print(f"   • {d}")


def main():
    try:
        version = anki_request("version")
        print(f"🔌 AnkiConnect v{version} is running\n")
    except Exception:
        print("❌ Cannot connect to AnkiConnect.")
        print("   Make sure Anki is running and AnkiConnect addon is installed.")
        print("   Restart Anki after installing the addon (ID: 2055492159)")
        return

    create_latex_basic_model()
    update_existing_models()
    list_decks()

    print("\n✨ Setup complete! In neovim:")
    print("   1. Open any .anki file")
    print("   2. :Anki LaTeX Basic   (or <leader>km)")
    print("   3. Write LaTeX math as usual (snippets work!)")
    print("   4. :AnkiSend           (or <leader>ks)")


if __name__ == "__main__":
    main()
