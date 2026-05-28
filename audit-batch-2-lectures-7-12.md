# Math 55a Audit — Batch 2 (Lectures 7–12)

**Scope.** Generalized eigenspaces & Jordan form (L7); categories, automorphism groups, universal properties (L8); inner product spaces & the spectral theorem (L9); modules over PIDs & finitely generated abelian groups (L10); group actions, Sylow theorems, finite subgroups of SO(3), semidirect products (L11); free groups, presentations, Cayley graphs, braid group, SL₂(ℤ) / PSL₂(ℤ) (L12).

**Audit depth.** Thorough: every proof re-verified by hand; diagrams inspected at tikz-level; statements cross-checked with their claimed generality. All matrix computations in L12 re-done (Euclidean reduction, R³ = −I, (TT′)⁶ = I, worked example, entry-sum argument).

**Fix policy in force (from user, verbatim).**
- Do NOT fix minor errors/issues; only critical + major + LaTeX bugs.
- For major forward references, just add a sentence noting the ref is ahead of its proof.
- Voice / tone / character stays as-is — do not sanitize.
- Keep "kernal/kernel" misspellings (no batch rename this round).
- Fix LaTeX bugs even though the PDF compiles (they may still be real bugs).

Severity legend: **CRIT** mathematically wrong in a way that breaks the statement or proof; **MAJ** wrong example / wrong diagram / wrong scope but recoverable; **MIN** style, forward-ref-within-lecture, or cosmetic.

---

## Lecture 07 — Generalized eigenspaces & Jordan form

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 7.1 | 420 | **CRIT** | Kernel chain printed as `\Ker(\varphi) \subset \Ker(\varphi^2) \subset \Ker\varphi \subset \ldots`. The third term repeats φ¹; should be `\Ker \varphi^3`. This makes the displayed chain mathematically meaningless. |
| 7.2 | 423 | **CRIT** | Stabilization proof has two defects in one line. (a) `\varphi^{m+1}(\varphi(V))` — capital V is a typo for lowercase v (the vector chosen at the start of the line). (b) `\varphi(v) = \Ker \varphi^m` is a type error: a vector cannot equal a subspace. Should be `\varphi(v) \in \Ker \varphi^m`. The intended chain of equivalences is fine — both are typos in the logical glue — but as printed the proof does not parse. |
| 7.3 | 348 | MIN | "The eigenfairy doesn't visit ℝ (sad)" — leave as-is per voice policy. |
| 7.4 | 412, 415 | MIN | Typos "Generalized Kernals", "vecrtors", "evnetually", "itterative" — leave per kernal/kernel policy and minor-fix policy. |
| 7.5 | 537 (approx.) | MIN | Corollary references the characteristic polynomial slightly before it is fully deployed; stays within the chapter so this is an intra-lecture forward ref, not cross-lecture. |

**Attack plan for L7.**
- 7.1: change `\Ker \varphi \subset \ldots` to `\Ker \varphi^3 \subset \ldots` in the displayed chain.
- 7.2: change `\varphi(V)` → `\varphi(v)` and `\varphi(v) = \Ker\varphi^m` → `\varphi(v) \in \Ker\varphi^m`.
- Everything else: leave.

---

## Lecture 08 — Categories, automorphism groups, universal properties

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 8.1 | 187 | **MAJ** | Note claims "non-isomorphic objects can have isomorphic automorphism groups" and backs it with "in Set, any two 3-element sets have Aut = S₃, but they are only isomorphic if we consider them as abstract sets (which they always are)". In **Set**, two 3-element sets are *always* isomorphic — the example does not exhibit the stated phenomenon. A correct example: Aut(ℤ/2 × ℤ/2) ≅ S₃ ≅ Aut(S₃), but ℤ/2 × ℤ/2 is abelian of order 4 while S₃ is non-abelian of order 6; they are non-isomorphic groups. Or: in **Grp**, Aut(ℤ) ≅ ℤ/2 ≅ Aut(ℤ/3), and ℤ ≇ ℤ/3. |
| 8.2 | 213–216 | **MAJ** | tikzcd bug in the product diagram. The line reads `P \ar[r, "\pi_1"'] \& A \& B \ar[l, "\pi_2"]`. The `\ar[l, ...]` from B draws an arrow B → A (one cell left of B is A), so the rendered diagram shows π₂ : B → A — which is nonsense for a product. The intended arrow is π₂ : P → B. The coproduct diagram on line 228 is correct; this one appears to have been copy-pasted and the arrow direction was not reconsidered. |
| 8.3 | 269 (approx.) | MIN | "Finite-dimensional" qualifier on the product/coproduct existence result is stronger than needed (binary products/coproducts exist in all of **Vect**). Leave per minor-fix policy. |
| 8.4 | 193 | MIN | "Fundamental groupoid" name-drop is a forward reference to algebraic topology, but it's flagged as "a key example" rather than used, so no disclaimer needed. |

**Attack plan for L8.**
- 8.1: replace the Set example with a correct one. Proposed text: "For instance, in **Grp**, the cyclic group ℤ and the cyclic group ℤ/3 both have automorphism group ℤ/2 (inversion, and the nontrivial automorphism respectively), but ℤ ≇ ℤ/3."
- 8.2: rewrite the product tikzcd so that π₂ points from P to B. Simplest layout-preserving fix is to change `B \ar[l, "\pi_2"]` to something that draws P → B, e.g. move B into a position where a straight arrow from P works, or add `\ar[rr, bend right, "\pi_2"']` from P. Concrete proposed replacement (keeps the three-column row):
  ```
  T \ar[dr, "\alpha"'] \ar[drr, "\beta", bend left=15] \ar[d, dashed, "\exists!\, \varphi"'] \& \& \\
  P \ar[r, "\pi_1"'] \ar[rr, bend right=20, "\pi_2"'] \& A \& B
  ```

---

## Lecture 09 — Inner product spaces & the spectral theorem

Clean. Every proof re-verified (Cauchy–Schwarz, Gram–Schmidt, adjoint identities, real and complex spectral theorems, reflections, Cayley transform, orthogonal decompositions).

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 9.1 | 386 | MIN | `\pi_S^* = \pi_S` with "see §9.3" — an intra-lecture forward ref (§9.3 comes later in the same file). Leave. |
| 9.2 | 606 | MIN | Real skew-adjoint derivation writes an `\overline{\cdot}` that does nothing in the real case. Harmless; leave. |

**Attack plan for L9.** Nothing to apply.

---

## Lecture 10 — Modules & finitely generated abelian groups

Clean. Smith Normal Form reduction and the classification theorem proof verified end-to-end.

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 10.1 | 65 | MIN | Notation `k[x] / (p(x)) \cdot k[x]` is clunky; standard `k[x]/(p(x))` suffices. Leave. |
| 10.2 | 112 | MIN | "Analogous to Maschke's theorem" comparison for PID splitting is loose (PID splitting is really a projectivity / short-exact-sequence fact, not representation-theoretic averaging). Leave. |

**Attack plan for L10.** Nothing to apply.

---

## Lecture 11 — Group actions, Sylow, SO(3) subgroups, semidirect products

Clean. Orbit–stabilizer, Burnside, class equation, all three Sylow theorems (via combinatorial lemma + subset action), A_n simplicity for n ≥ 5, finite subgroups of SO(3) all verified. No findings to tag.

**Attack plan for L11.** Nothing to apply.

---

## Lecture 12 — Presentations, Cayley graphs, braid group, SL₂(ℤ) / PSL₂(ℤ)

Clean. All matrix computations re-done by hand: S² = R³ = −I, (TT′)⁶ = I, TT′T = T′TT′ = S, worked example M = T³ S T² verified by direct multiplication, entry-sum argument for the free-product proof checked (T and SR⁻¹ both have entry sum 3, and (a+c)(e+f) + (b+d)(g+h) stays ≥ 3 under multiplication of Ts and Us).

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 12.1 | 77–93 | MIN | The S₃ Cayley graph is drawn with single directed arrows, though s_i are involutions (each edge should be bidirectional or undirected). Standard pedagogical simplification; leave. |
| 12.2 | 135 | MIN | Calling the braid relation "the Yang–Baxter equation" is a colloquial stretch — Y–B is a parameter-dependent generalization — but widely used in this loose sense. Leave. |

**Attack plan for L12.** Nothing to apply.

---

## Cross-cutting observations

1. **No cross-lecture forward references found in batch 2.** Every proof in L7–L12 depends only on material already established. (L9's §9.3 pointer is intra-file.)
2. **Diagram integrity.** Only one tikzcd bug (L8 product diagram). L8 coproduct, L11 SO(3) diagrams, L12 Cayley graphs and fundamental-domain picture, L12 braid diagrams all check out.
3. **Tone / voice.** L7 contains the densest voice ("eigenfairy", "what in tarnation", "Auroux likes it though, so that is what we are going with") — leaving intact per policy. L8–L12 are tonally more neutral.
4. **No LLM-esque tells.** No "it's worth noting", "let's delve", "in this section we will explore" patterns observed in batch 2.
5. **Misspellings.** L7's "kernal", "vecrtors", "evnetually", "itterative" left alone per policy. No new misspellings introduced elsewhere in batch 2.

---

## Decisions needed from you

To proceed to fix application for batch 2, please confirm or amend:

**(D1)** Apply L7 fix 7.1 (kernel chain `\Ker\varphi` → `\Ker\varphi^3`). Confirm? [Y/n]

**(D2)** Apply L7 fix 7.2 (φ(V) → φ(v), and `=` → `\in`). Confirm? [Y/n]

**(D3)** Apply L8 fix 8.1 — replace the wrong Set example in the note with a correct one. My proposed replacement is Aut(ℤ) ≅ ℤ/2 ≅ Aut(ℤ/3) with ℤ ≇ ℤ/3. Alternatives include the S₃ / ℤ/2 × ℤ/2 pair, or keep the Set framing but switch to "two sets of *different* cardinality with the same Aut group" (doesn't work — Aut distinguishes cardinality in Set). Choose preferred example, or approve my proposal. [example choice]

**(D4)** Apply L8 fix 8.2 — rewrite the product tikzcd so π₂ : P → B. Propose the `\ar[rr, bend right=20, "\pi_2"']` form shown above. Confirm? [Y/n]

**(D5)** No action needed on L9–L12; confirm "no fixes" for those lectures. [Y/n]

Once you respond, I'll apply the approved fixes and then move to batch 3 (L13–L17).
