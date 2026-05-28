# Math 55a Audit — Batch 3 (Lectures 13–17)

**Scope.** Representation theory of finite groups: characters, orthogonality, regular rep, S_3/S_4/A_4 tables (L13); orthonormal basis theorem, isotypic projection, representation ring, S_5/A_5 tables, Artin/Brauer (L14); restriction, induction, Frobenius reciprocity, Mackey, S_4↓S_3 (L15); real/quaternionic/complex reps, Frobenius–Schur indicator, Q_8 example (L16); commutative rings (ED/PID/UFD/Noetherian, Hilbert basis, Gauss's lemma), Galois theory (FTGT, cyclotomic, Abel–Ruffini), Lie groups/algebras (exp map, sl₂, Dynkin) (L17).

**Audit depth.** Thorough: every proof re-verified by hand. All character tables (S_3, S_4, A_4, S_5, A_5) recomputed from definitions. All representation inner products checked against orthogonality relations. Induction and restriction formulas cross-checked with Frobenius reciprocity. L16 Q_8 and S_4 Frobenius–Schur indicator computations redone. L17 exercise solutions all re-verified (including [E_1,E_2]=E_3 for so(3), sl_2 bracket relations, and Gal(ℚ(√[4]{2},i)/ℚ)≅D_4).

**Fix policy in force (unchanged from batch 2).**
- Do NOT fix minor errors/issues; only critical + major + LaTeX bugs.
- For major forward references, just add a sentence noting the ref is ahead of its proof.
- Voice / tone / character stays as-is — do not sanitize.
- Keep "kernal/kernel" misspellings (no batch rename this round).
- Fix LaTeX bugs even though the PDF compiles.

Severity legend: **CRIT** mathematically wrong in a way that breaks the statement or proof; **MAJ** wrong example / wrong diagram / wrong scope but recoverable; **MIN** style, forward-ref-within-lecture, or cosmetic.

---

## Lecture 13 — Representations, characters, orthogonality

Clean. Every character-table entry and every inner product ⟨χ_ρ, χ_σ⟩ re-verified against |G|⁻¹ Σ χ_ρ(g) χ_σ(g)̄. Schur's lemma, Maschke's theorem, the column orthogonality derivation, the regular representation decomposition, and the S_3/S_4/A_4 tables all check out.

**Attack plan for L13.** Nothing to apply.

---

## Lecture 14 — Orthonormal basis theorem, representation ring, Artin/Brauer

Clean. S_5 and A_5 character tables re-verified. In particular: A_5 irreducibles of dim 3 with golden-ratio entries a = (1+√5)/2, b = (1−√5)/2 on 5-cycles satisfy a + b = 1, ab = −1, a² + b² = 3 (so ⟨χ_Y, χ_Y⟩ = 1 as required). Artin's theorem (induced characters from cyclics span R(G)⊗ℚ) and Brauer's theorem (from elementary subgroups span R(G)) both correctly stated.

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 14.1 | — | MIN | Generalized averaging/projection proposition appears in both L13 (end) and again in L14 (reframing in the orthogonal-projection language). This is a deliberate pedagogical repeat, not a bug. Leave. |

**Attack plan for L14.** Nothing to apply.

---

## Lecture 15 — Restriction, induction, Frobenius reciprocity, Mackey

Clean. Induced-character formula (χ_Ind(g) = (1/|H|) Σ_{x : x⁻¹gx ∈ H} χ_V(x⁻¹gx)) re-verified. Frobenius reciprocity ⟨Ind^G_H V, W⟩_G = ⟨V, Res^G_H W⟩_H checked on the S_4 ↓ S_3 example and the Ind^{S_5}_{S_4}(V_4) = V ⊕ ∧²V ⊕ W decomposition (which is not a typical formula — recomputed the induced character on each conjugacy class and confirmed the decomposition against ⟨·,·⟩_{S_5}).

**Attack plan for L15.** Nothing to apply.

---

## Lecture 16 — Real, quaternionic, complex representations; Frobenius–Schur indicator

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 16.1 | 118 (approx., the displayed Q_8 matrix block) | **MAJ** | The Q_8 matrices given as a 2-dimensional complex representation do not actually satisfy the quaternion relation ij = k. Displayed: i ↦ diag(i, −i), j ↦ ((0, −1), (1, 0)), k ↦ ((0, i), (i, 0)). Direct computation: i · j = diag(i,−i) · ((0,−1),(1,0)) = ((0, −i), (−i, 0)) = −k (not k). So the displayed matrices fail to define a Q_8 homomorphism (they give a rep of some central extension/twist, but not Q_8 itself as written). The downstream content — the character χ = (2, −2, 0, 0, 0), the computation of the Frobenius–Schur indicator giving −1, and the conclusion that this is the quaternionic-type irreducible — is all **unaffected**, because characters depend only on traces, and the ±g pairings balance in both g and g² regardless of the sign flip. The fix is a local sign change in the displayed matrices; none of the surrounding prose needs to change. Standard Fulton–Harris convention: change j ↦ ((0, 1), (−1, 0)) (flip both off-diagonal signs). Then i·j = ((0, i), (i, 0)) = k as required. |
| 16.2 | — | MIN | The antilinear-involution criterion (a complex rep V is real-type ⟺ it carries a G-equivariant antilinear involution J with J² = +I; quaternionic-type ⟺ J² = −I) is stated slightly before the proof of its full equivalence with the indicator. The local proof sketch is sufficient to make the claim rigorous in-chapter. Leave. |

**Attack plan for L16.**
- 16.1: change the displayed j matrix to `\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}`. Verify by hand that i·j = k, j·k = i, k·i = j after the fix.

---

## Lecture 17 — Commutative rings, Galois theory, Lie algebras

Part I (commutative rings) and Part II (Galois theory) verified end-to-end. Part III (Lie groups / Lie algebras) — matrix Lie group dimension formulas, sl₂ bracket relations, the exp-map counterexample in SL_2(ℝ) (the matrix `((-1, 1), (0, -1))` really is not in exp(sl_2(ℝ)) — verified by case analysis on eigenvalue structure of real 2×2 traceless X), Dynkin classification (A_n for n ≥ 1, B_n for n ≥ 2, C_n for n ≥ 3, D_n for n ≥ 4; exceptional dims 14, 52, 78, 133, 248) all correct. Exercise solutions all verified by hand.

| # | Line | Severity | Issue |
|---|------|----------|-------|
| 17.1 | 97–98 | **MAJ** (LaTeX / style consistency) | `\thm{Every PID is a UFD}{% \n}` — the theorem's body argument is empty (just a `%` comment and a newline). The statement is carried only by the title; every other `\thm{…}{…}` in the file places a sentence of the form "If R is … then R is …" inside the body. As printed, this theorem has a header and then jumps straight into the "Proof (sketch)" block, which looks like a rendering glitch. Fix: put the statement "Every principal ideal domain is a unique factorization domain." (or similar) into the body so the theorem environment has content like every other `\thm` in the lecture series. |
| 17.2 | 211 | MIN | `S_3/{\ZZ}/3 \cong {\ZZ}/2` typesets as "S_3/ℤ/3" with two adjacent slashes. Clearer as `S_3/\langle (123)\rangle` or `S_3/A_3`. Leave per minor-fix policy. |
| 17.3 | 346 | MIN | The Dynkin conventions `B_n (n ≥ 2)`, `C_n (n ≥ 3)`, `D_n (n ≥ 4)` are the "non-overlapping" conventions (chosen to avoid low-rank coincidences: B_2 ≅ C_2, A_3 ≅ D_3, A_1 × A_1 ≅ D_2). Some references use n ≥ 1 for B/C and n ≥ 2 for D. The chosen convention is standard and internally consistent. Leave. |
| 17.4 | 294 | MIN | "Differentiating det(e^{tX}) = e^{t Tr(X)} = 1 gives Tr(X) = 0" elides one step (differentiate at t = 0, getting Tr(X) · 1 = 0). Reasoning correct; leave. |
| 17.5 | 270 | MIN | The dimension computation is stated for O(n), not specifically for SO(n); dim SO(n) = dim O(n) since SO(n) is the identity component. Harmless; leave. |

**Attack plan for L17.**
- 17.1: change `\thm{Every PID is a UFD}{%\n}` to `\thm{Every PID is a UFD}{Every principal ideal domain is a unique factorization domain.%\n}` (or equivalent text). This gives the environment a body consistent with every other `\thm` in the file.

---

## Cross-cutting observations

1. **Forward references.** No cross-lecture forward references in batch 3. Every L13–L17 proof depends only on material already established (character theory builds on L11 group actions; induction/restriction builds on L13–L14; Galois uses S_n/A_n from L11; Lie algebras use linear-algebra preliminaries from L5–L9).
2. **Representation-theory arithmetic.** Every character-table inner product spot-checked. The A_5 golden-ratio entries, the S_5 Sym²V / ∧²V decomposition, and the Ind^{S_5}_{S_4}(V_4) decomposition all verify cleanly against orthogonality.
3. **Q_8 matrix bug is the only real mathematical issue in batch 3** (L16, finding 16.1). It does not propagate into the Frobenius–Schur indicator result or any later computation, because characters only see traces; but the displayed matrices as printed are not a Q_8 representation.
4. **Empty theorem body in L17** (finding 17.1) is the only LaTeX-structural issue found in batch 3 — a real inconsistency with the rest of the document's `\thm` usage.
5. **No LLM-esque prose** detected across L13–L17. The voice throughout these five lectures is more neutral than L7 but consistent.
6. **No new misspellings** introduced in batch 3. L7's "kernal" family does not recur here.

---

## Decisions needed from you

**(D1)** Apply L16 fix 16.1 — change the displayed j matrix in the Q_8 representation from `\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}` to `\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}` so that i · j = k holds. (Character χ = (2,−2,0,0,0) and Frobenius–Schur indicator = −1 are unchanged; no surrounding prose requires editing.) Confirm? [Y/n]

**(D2)** Apply L17 fix 17.1 — add a body to `\thm{Every PID is a UFD}{…}` so it isn't printed as a bodiless theorem environment. Proposed body text: "Every principal ideal domain is a unique factorization domain." Alternative: "If R is a PID, then R is a UFD." Confirm the proposed text, or specify preferred wording. [body text choice]

**(D3)** No action needed on L13, L14, L15. Confirm "no fixes" for these three lectures. [Y/n]

Once you respond, I'll apply the approved fixes and then produce the final consolidated audit report covering all three batches (L1–L17).
