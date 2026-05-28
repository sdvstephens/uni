# Math 55a — Audit Report, Batch 1 (Lectures 1–6)

**Scope:** `lecture_01.tex` through `lecture_06.tex` in `Studies-in-Algebra-and-Group-Theory/`.
**Depth:** Thorough — every definition, theorem statement, and proof re-verified line-by-line.
**Deliverable status:** Interim. Please review the attack plan in each section and flag any findings you disagree with (or any proposed fixes you'd like changed) before I start applying edits or move on to Batch 2.

**Legend for severity:**
- **CRITICAL** — mathematically wrong; will mislead the reader.
- **MAJOR** — logically wrong or structurally broken (e.g., forward references that cannot be recovered, internally inconsistent examples).
- **MINOR** — typo, LaTeX rendering bug, stylistic/"LLM-ism" issue, light informal aside.

---

## 0. Top-level summary across Batch 1

The lectures are mostly in good shape mathematically, but there are **seven substantive errors** (CRITICAL or MAJOR) and several **forward-reference chains** that break the "no forward references" criterion. The main things I want you to look at before I touch anything:

1. **Lecture 2, line 340** (CRITICAL): the parenthetical aside gets the *direction* of the First Isomorphism Theorem backward. It says surjectivity is equivalent to trivial kernel; the correct statement is **injectivity** is equivalent to trivial kernel.
2. **Lecture 3, line 62** (CRITICAL): Cantor's diagonal has a type error — the set $A$ is defined using $s \neq \alpha(s)$, but $\alpha(s) \in \mathcal{P}(S)$ is a *subset* of $S$, not an element, so the comparison should be $s \notin \alpha(s)$. The proof prose (correctly) uses "$\notin$".
3. **Lecture 3, lines 116 & 118** (CRITICAL): The equivalence relation $a \sim b \iff ab^{-1} \in H$ has equivalence classes that are **right cosets** $Hg$, not **left cosets**. The text asserts left cosets. The entire subsequent discussion is then presented using left cosets, so the relation and the claim of what its equivalence classes are don't match.
4. **Lecture 3, lines 155–165** (MAJOR): The $S_3$ coset example silently switches composition conventions mid-example — the coset listing requires **left-to-right** composition, but the computation $(13)(23) = (132)$ uses **right-to-left**. I verified both by hand.
5. **Lecture 3, line 1005** (MAJOR): The $Q_8$ presentation verification claims $iji^{-1}j = e \Rightarrow ij = j^{-1}i^{-1}$. The correct conclusion is $ij = j^{-1}i$. The subsequent manipulation $(j^{-1}i^{-1} = (ji)^{-1})$ is also wrong ($(ji)^{-1} = i^{-1}j^{-1}$).
6. **Lecture 5, line 204** (CRITICAL): "we have $Q = P$" — this is wrong; $Q = P^{-1}$, as the next line (210) correctly states. The contradictory sentence should be deleted.
7. **Lecture 6, line 386** (MAJOR): Proposition setup says "Let $S : V \to W$ and $T : W \to U$" and then item (1) states $(S+T)^* = S^* + T^*$ "when both are defined" — but $S + T$ is never defined when $S, T$ have different codomains. Either the hypotheses or the statement needs to change.

There are also forward-reference issues in lectures 2, 3, 5, 6 (Euclid, Bézout, Lagrange, FIT, eigenvalues) — details below.

---

## 1. Lecture 1 — Set Theory (`lecture_01.tex`, 210 lines)

### 1.1 Findings

| Line(s) | Severity | Issue |
|---|---|---|
| 99 | MINOR | `"f(x,y)=x; similarly, if if f(x,y)=x"` — doubled word "if if". |
| 104 | MINOR | `"universially"` — typo, should be "universally". |
| 135 | MINOR | Trailing literal `\}` at end of the proof item `"Thus, by definition, the set must be empty.\}"` — looks like a stray escape artifact. |
| 134 | CONCEPTUAL (MINOR) | The sentence concludes "the only element that can be in $Y^\emptyset$ is the singleton $\{\emptyset\}$" — but the claim being proved is that $Y^\emptyset = \{\emptyset\}$, i.e., it contains the empty function $\emptyset$ as a single element. Writing the element as "the singleton $\{\emptyset\}$" conflates the element (empty function) with the containing set. Prose is loose, but not outright wrong. |
| 142 | MINOR | `"\ran (\{A_i\}= \bigcup_{i \in I} A_i )"` — the paren grouping is off; $\ran$ is supposed to apply to the family, not to the equation. Should be `\ran(\{A_i\}) = \bigcup_{i \in I} A_i`. |
| 152–155 | MINOR | Theorem statement "Let $\{I_j\} : J \to K \mid K = \bigcup_{j \in I}$" — the condition is cut off (what is being unioned?), and the index on the union is wrong ($j \in I$ should be $j \in J$ to match the domain just introduced). |
| 161 | MINOR (tone) | `"Sorry! I am leaving this one as an exercise for the reader (sorrryyyyyy:) )"` — informal, not obviously "LLM-ese" but reads as filler/stalling in a technical document. |
| 166 | MINOR (tone) | `"these are so disgusting as to induce spontaneous retching in even the most tough-stomached mathematicians"` — colorful prose; keep or tone down per taste. |
| 169 | MINOR (tone) | Long parenthetical about "toiling and languishing over my incorrectness and stupidity, suffering immensely" — this is a "LLM-esque" self-deprecating aside; consider cutting. |
| 183–185 | MINOR | The note conflates the two meanings of $f^{-1}$ in a way that reads slightly confused: "$f^{-1} : \ran(f) \to X \implies f^{-1}(y) = x \iff f(x) = y$" — the implication arrow is wrong here; this should be a definition, not an implication. |
| 204 | MINOR | `"Congrats! You made a \textbf\{\textit{composite relation}\}"` — `\textbf\{` is an escaped brace (prints literally as `{...}`). Same issue at "\textbf\{\textit{relative product}\}(??)". Should be `\textbf{\textit{...}}`. |
| 188 | MINOR | "Let $f$ be a function such that $f : X \to A$ for each of the following" — but then item (1) talks about $B \subset Y$, meaning the codomain should be $Y$, not $A$. Inconsistent naming. |
| 90 | MINOR (clarity) | `"we call this the \textbf{\emph{inclusion map} embedding/ injection/} or we say $f$ is \textbf{\emph{one-to-one}}"` — the inclusion map is a specific map $X \hookrightarrow Y$ when $X \subset Y$, not synonymous with "injection" or "one-to-one"; any injection is not automatically an inclusion. Definitions are being run together. |

No forward references, no mathematical errors, no proof errors.

### 1.2 Attack plan (Lecture 1)

Proposed fixes, in order of increasing invasiveness:

1. **Typos / LaTeX (safe):** fix "if if" (line 99), "universially" → "universally" (104), stray `\}` (135), escaped braces in `\textbf\{...\}` (204), paren on `\ran` (142), $X \to A$ → $X \to Y$ in the list intro (188), the $\implies$/$\iff$ muddle in the inverse-function note (183).
2. **Theorem 152–155 (Associative law of unions):** restore the cut-off hypothesis and fix the index mismatch. I'll propose: "Let $J$ be an index set and let $\{I_j\}_{j \in J}$ be a family of sets with $K = \bigcup_{j \in J} I_j$, and let $\{A_k\}_{k \in K}$ be a family of subsets of $X$." Leaving the "exercise for the reader" prose as-is unless you want me to touch the voice.
3. **Prose (needs your call):** the "suffering immensely" aside (169), the "retching" line (166), the "sorrryyyyyy:)" aside (161), the "enby (slay)" bit I flagged earlier, and the $\mathcal{X}y / \mathfrak{c}y$ notation question — these are *voice* choices. I'd like your preference:
   - (a) Leave all voice alone; fix only technical issues.
   - (b) Soften egregious asides (the three above) but keep personality.
   - (c) Strip all informal asides.
4. **Definition at line 90 (inclusion/injection conflation):** rewrite to disentangle "inclusion map" (a specific map $X \hookrightarrow Y$ with $X \subset Y$) from "injection" (any one-to-one map). Small rewrite, two sentences.

---

## 2. Lecture 2 — Group Theory Basics (`lecture_02.tex`, 570 lines)

### 2.1 Findings

| Line(s) | Severity | Issue |
|---|---|---|
| **340** | **CRITICAL** | *Proof of cyclic group structure, end of Case 2.* The parenthetical reads: "this will be introduced later but to oversimplify: surjectivity is guaranteed iff the kernal only contains the identity". This is the **wrong direction**: injectivity is equivalent to trivial kernel; surjectivity is unrelated to the kernel. Also `"kernal"` → `"kernel"`. |
| 121–125 | MAJOR (forward reference) | Uses Euclid's lemma at line ~121 and Bézout's identity at ~125 before either is introduced. Bézout is proved later in this lecture at line 295. If you want no forward refs, these need either (a) a sentence acknowledging they're being cited ahead of their proof, or (b) reorganization so Bézout comes first. |
| 383 | MAJOR (forward reference) | Solution "(2)" cites Lagrange's theorem to prove $\mathbb{Z}/p\mathbb{Z}$ has no proper nontrivial subgroups — but Lagrange is proved in Lecture 3. Either move the exercise to after Lagrange, give a direct proof (easy: any subgroup of $\langle a \rangle$ is cyclic, and $\langle a^k \rangle$ for $a^k \neq 0$ has order $p/\gcd(k,p) = p$ since $p$ prime), or flag the forward ref. |
| 340 | MINOR (forward reference) | The same parenthetical also cites FIT ahead of its proof in Lecture 3. |
| General | MINOR | Throughout lectures 1–3, "kernal" is used in several places where "kernel" is correct. I'll flag every instance during the fix. |

All proofs I checked in this lecture are otherwise correct. Matrix work in $\mathbb{Z}/n$ subgroup-lattice derivation is fine; $Z(D_4)$ solution is fine.

### 2.2 Attack plan (Lecture 2)

1. **Line 340 (CRITICAL):** replace the parenthetical with a correct informal gloss. Proposed replacement text:

   > "...so $G \cong \mathbb{Z}/n\mathbb{Z}$ by the First Isomorphism Theorem (introduced in the next lecture; informally: once we quotient by the kernel, the induced map is automatically injective, and we already have surjectivity)."

   Alternative (more minimal): just delete the parenthetical entirely — the FIT is cited, which is enough.

2. **Forward reference to Euclid/Bézout (121, 125):** two options:
   - (a) Add a `\nt{...}` at first use: "We'll use Euclid's lemma / Bézout here; a proof appears below at Proposition X."
   - (b) Reorganize: prove Bézout first (it's the prerequisite for Euclid), then proceed. (a) is much less invasive.
3. **Lagrange forward reference in solution (383):** I'd suggest replacing with a direct argument. Proposed rewrite:

   > "Any subgroup of $\mathbb{Z}/p\mathbb{Z}$ is cyclic (subgroups of cyclic groups are cyclic, proven above), so is generated by some $a^k$. If $a^k \neq e$, then $\gcd(k, p) = 1$ since $p$ is prime, so $\langle a^k \rangle = \mathbb{Z}/p\mathbb{Z}$."

4. **"kernal" → "kernel":** mechanical global fix within this lecture. I'll do a replace_all pass scoped per-file.

---

## 3. Lecture 3 — Group Relations (`lecture_03.tex`, 1016 lines)

This is the lecture with the most issues, both conceptual and mechanical.

### 3.1 Findings

| Line(s) | Severity | Issue |
|---|---|---|
| 14 | MINOR | Starts with `".We say"` — stray leading period. |
| 16, 19 | MINOR | "Schröder-Berstein" misspelled — should be "Schröder-Bernstein". |
| 24 | MINOR | `\|N \times N\| = \|N\| = N^n` is a type error — last term should be `\|N^n\|`. Also "$(k, 1)$" appears where "$(k, l)$" (lowercase ell) was meant. |
| **62** | **CRITICAL** | Cantor's diagonal: $A := \{s \in S \mid s \neq \alpha(s)\}$. Since $\alpha(s) \in \mathcal{P}(S)$ is a *subset* of $S$, not an element, the comparison $s \neq \alpha(s)$ is a type error. The correct definition is $A := \{s \in S \mid s \notin \alpha(s)\}$. The prose *immediately after* correctly uses "$t \notin \alpha(t)$", so this is a set-builder typo, but it's the central construction of the proof. |
| **116** | **CRITICAL** | Defines $a \sim b \iff ab^{-1} \in H$ and adds "this is to say that $a \in bH$". But $ab^{-1} \in H$ means $a = hb$ for some $h \in H$, i.e., $a \in Hb$ (**right coset**), not $a \in bH$. |
| **118** | **CRITICAL** | Definition says "The equivalence classes under congruence mod $H$ are precisely the left cosets of $H$." Given the relation at line 116, they're right cosets. The whole partition-by-left-cosets development that follows is fine if the relation is changed to $a^{-1}b \in H$ (the standard "left congruence"); the cleanest fix is to change the relation to match the later left-coset discussion. |
| 121, 124, 126 | Follow-on | The Proposition "Cosets partition $G$" and its proof are stated and proved for **left** cosets; this is internally consistent with line 118's claim but not with line 116's relation. |
| **155–165** | **MAJOR (MIXED CONVENTIONS)** | The $S_3$ example has a **composition-order inconsistency**: <br> • Coset listing $(13)H = \{(13),\ (132)\}$ and $(23)H = \{(23),\ (123)\}$ — these require **left-to-right** composition (apply leftmost permutation first). <br> • But the computation $(13)(23) = (132)$ at line 157 requires **right-to-left** composition (standard math convention). <br> Verified by hand: under right-to-left, $(13)(12) = (123)$, so $(13)H = \{(13), (123)\}$. Under left-to-right, $(13)(23) = (123)$, not $(132)$. No single convention makes both parts correct. |
| 201 | MINOR | In the well-definedness proof of quotient groups: "Since $N$ is normal, $n_1 b = b n_3$ for some $n_3 \in N$. We have $n_1 b \in Nb = bN$, so $n_1 b = b n_3$ for some $n_3 \in N$." The same conclusion is drawn twice back-to-back; one of the two sentences should be deleted. |
| 317 | MAJOR (forward reference) | Cayley's theorem proof cites the First Isomorphism Theorem, but FIT is stated/proved in the same lecture at line 389 — so Cayley appears before its tool. Either (a) move FIT above Cayley, (b) give a direct kernel-trivial argument without invoking FIT (very short: $\rho$ is a group homomorphism with trivial kernel, hence $G \cong \rho(G) \subset \operatorname{Sym}(G)$ by general nonsense — but "general nonsense" *is* FIT, so this is circular unless we just say "injective homomorphism gives an isomorphism with its image", which is fine as a bare statement). |
| 978 | MINOR | `"in facct"` → `"in fact"`. |
| **1005** | **MAJOR** | $Q_8$ solution: "$iji^{-1}j = e$ means $ij = j^{-1}i^{-1}$". <br> Correct: $iji^{-1}j = e \Rightarrow iji^{-1} = j^{-1} \Rightarrow ij = j^{-1}i$ (right-multiply both sides by $i$). The exponent on the second $i$ is wrong. <br> The follow-on "$= j^{-1}i^3 = j^{-1}(i^{-1}) = (ji)^{-1}$" is also wrong: $(ji)^{-1} = i^{-1}j^{-1}$, not $j^{-1}i^{-1}$ (those agree only if $i, j$ commute, which they don't in $Q_8$). |

### 3.2 Attack plan (Lecture 3)

1. **Line 62 (CRITICAL — Cantor):** change `s \neq \alpha(s)` to `s \notin \alpha(s)`. One-character class fix ($\neq$ → $\notin$). No downstream changes needed.
2. **Lines 116 & 118 (CRITICAL — coset relation):** two options, I want your call:
   - **(A) Keep left cosets throughout; change the relation.** Rewrite line 116 as: "$a \sim b \iff a^{-1} b \in H$, which is the same as $b \in aH$." This is the standard "left congruence mod $H$" whose classes are left cosets, matching line 118 and everything that follows. This is the cleanest fix; only line 116 changes.
   - **(B) Keep the relation; switch all the subsequent discussion to right cosets.** Much more invasive — the Lagrange proof, the $S_3$ example, the normality definitions (which use $gN = Ng$) all stay OK by symmetry, but the stated theorems / definitions would need "left coset" → "right coset" in ~10 places.

   **Recommendation: (A).**
3. **Lines 155–165 (MAJOR — $S_3$ cosets):** pick one convention and redo the example. Under **right-to-left** (standard), the cosets are:
   - $H = \{e, (12)\}$
   - $(13)H = \{(13),\ (13)(12)\} = \{(13),\ (123)\}$
   - $(23)H = \{(23),\ (23)(12)\} = \{(23),\ (132)\}$

   Then the "it worked!" and "disaster!" demonstrations need to be redone with fresh representatives. I can regenerate the whole example using right-to-left; net change ~10 lines. I'll draft it and send for review before applying.

4. **Line 201:** delete the redundant second sentence.
5. **Line 317 (Cayley uses FIT):** simplest fix is to rephrase to "An injective homomorphism $\rho : G \to \Sym(G)$ gives an isomorphism $G \cong \rho(G)$" — this is a statement independent of FIT per se, so no forward reference. Alternatively, reorder: move FIT before Cayley.
6. **Line 1005 ($Q_8$ algebra):** rewrite the verification. Draft:

   > $i^4 = 1$ gives $i$ order dividing 4. $i^2 = j^2$ gives a common square. The relation $iji^{-1}j = e$ rearranges to $ij = j^{-1}i$, which combined with $i^2 = j^2$ encodes the full quaternion multiplication (one can verify that $ij$ satisfies the defining relations of $k$).

   I'll write out the full verification if you want a longer version.
7. **Typos:** leading period at 14; "Berstein" → "Bernstein" (16, 19); $\lvert N^n \rvert$ at 24; $(k, l)$ at 24; "facct" → "fact" (978). All mechanical.

---

## 4. Lecture 4 — Vector Spaces (`lecture_04.tex`, 630 lines)

This lecture is the cleanest of the batch.

### 4.1 Findings

| Line(s) | Severity | Issue |
|---|---|---|
| ~16 | MINOR (tone) | Opening framing has some "motivating chatter" that reads slightly LLM-ish; not a must-fix. |
| ~369 | MINOR (tone) | "if that doesn't make sense right now, don't worry" — informal aside; optional to remove. |

No mathematical or proof errors identified. Definitions of $k$-vector space, subspace, internal/external direct sum, span, linear independence, basis, and dimension are all correct and well-ordered. The proof that dimension is well-defined (Steinitz exchange flavor) is correct.

### 4.2 Attack plan (Lecture 4)

Minor prose polish if you want it (see voice question under Lecture 1 attack plan item 3). Otherwise, **no changes recommended**.

---

## 5. Lecture 5 — Linear Maps (`lecture_05.tex`, 318 lines)

### 5.1 Findings

| Line(s) | Severity | Issue |
|---|---|---|
| 189 | MINOR (tone) | `"what makes linear algebra, well linear algebra (duh)"` — filler; should be cut in a serious course doc. |
| 194 | LaTeX BUG | `\sum_{n}^{i=1}` — bounds are swapped. Should be `\sum_{i=1}^{n}`. |
| 199 | LaTeX BUG | `\mcM (\text{id}_W,(w_i)(w_i'))` — missing comma between `(w_i)` and `(w_i')`, should be `\mcM(\text{id}_W, (w_i), (w_i'))`. |
| 199 | LaTeX BUG | `\varphi ((v_i'))X'` — misplaced close paren; should be `\varphi((v_i'))X'` or `\varphi((v_i') X')` depending on intent. |
| 202 | MINOR | `"pp^{-1}"` — lowercase; should be `PP^{-1}` to match notation. |
| **204** | **CRITICAL** | "with $P = \mcM(\id_V, (v_i'), (v_i))$ as above, and using the *same* basis change for both domain and codomain, **we have $Q = P$**" — this is wrong. $Q$ was defined on $W$-side as $\mcM(\id_W, (w_i), (w_i'))$; when $V = W$ and both bases are $(v_i), (v_i')$, we get $Q = \mcM(\id_V, (v_i), (v_i'))$. That's the **inverse** of $P$, not $P$ itself. The very next sentence (line 210) correctly states $Q = P^{-1}$. Need to delete or fix the "$Q = P$" claim. |
| throughout | LaTeX RENDERING | `Tr` in math mode renders as variables ($T \cdot r$). Should be `\operatorname{Tr}` or a `\Tr` macro (check preamble — if absent, I can add it). |
| 269+ | FORWARD REFERENCE | Propositions about eigenvalues as similarity invariants (and the surrounding example) use "eigenvalue" without a formal definition, which arrives later. Either define eigenvalues when first used, or defer the proposition to after the definition. |

### 5.2 Attack plan (Lecture 5)

1. **Line 204 (CRITICAL):** delete the sentence "we have $Q = P$" and rewrite the transition as:

   > "With $V = W$ and using the same basis change for both domain and codomain, $Q$ is the change-of-basis matrix from $(v_i')$ back to $(v_i)$, i.e., $Q = P^{-1}$. The formula $\mathcal{M}(\varphi, (v'), (w')) = QAP$ therefore becomes $A' = P^{-1} A P$."

2. **LaTeX bugs (194, 199, 202):** mechanical fixes.
3. **`Tr` rendering:** check if preamble has `\Tr`. If not, add `\DeclareMathOperator{\Tr}{Tr}`, then replace `Tr` with `\Tr` throughout (I'd run this scoped to the lecture, not the whole book, so the change is auditable).
4. **Forward reference to eigenvalues:** two options:
   - (a) Add a brief inline definition at first use ("an *eigenvalue* of $A$ is a scalar $\lambda$ such that $Av = \lambda v$ for some nonzero $v$").
   - (b) Move the "eigenvalues are similarity invariants" proposition to the lecture where eigenvalues are formally introduced.

   **Recommendation: (a)**, since the proof of similarity invariance is clean and short, and deferring breaks the thematic arc of lecture 5 (similarity → invariants).
5. **Line 189 tone:** cut per voice policy.

---

## 6. Lecture 6 — Kernel, Images, Duality (`lecture_06.tex`, 519 lines)

### 6.1 Findings

| Line(s) | Severity | Issue |
|---|---|---|
| 1, 14 | MINOR | Title/comment use `"Kernals"` — misspelling, should be `"Kernels"`. |
| 18 | MINOR (tone) | `"(what a fun word)"` — informal aside. |
| 31, 75 | MINOR | `"kernal"` → `"kernel"`. |
| 75 | MINOR | `"more that merely"` → `"more than merely"`. |
| 40, 307 | LaTeX RENDERING | Same `Tr` in math mode issue as Lecture 5. |
| 229 | FORWARD REFERENCE | Note references eigenvalues, algebraic/geometric multiplicity, and Jordan normal form — all appearing in later lectures. Since this is in a `\nt{}` (note), it's the least harmful kind of forward reference, but still worth flagging. |
| **386** | **MAJOR (structural)** | Proposition setup: "Let $S : V \to W$ and $T : W \to U$ be linear maps." Then item (1) states "$(S + T)^* = S^* + T^*$ (when both are defined)." But $S + T$ is only defined when $S, T$ share both domain and codomain, which the hypothesis explicitly violates. This proposition is conflating two different propositions: (a) additivity of dualization on $\Hom(V, W)$ — where both maps have the same domain/codomain — and (b) contravariance/composition (item 3, $(T \circ S)^* = S^* \circ T^*$). |
| 431 | MINOR (forward reference, flagged) | Corollary's proof says "By a result we'll see shortly" pointing to line 438. Acceptable style with disclaimer, but still a forward ref. |
| 451–481 vs 485–511 | MAJOR (organization) | Exercise 4 asks about $V^{**}$ and the solution is given *before* the subsection "The Double Dual and Natural Isomorphisms" (lines 485+). The content order is: exercises/solutions that presuppose a concept → formal introduction of that concept. Reader encounters $V^{**}$ cold. |

### 6.2 Attack plan (Lecture 6)

1. **Line 386 (MAJOR):** split the proposition into two, or fix the hypotheses. Cleanest fix — restate as two propositions:

   **Proposition A (additivity).** For $S, T : V \to W$ and $\lambda \in k$: $(S+T)^* = S^* + T^*$ and $(\lambda T)^* = \lambda T^*$.
   **Proposition B (contravariance).** For $S : V \to W$ and $T : W \to U$: $(T \circ S)^* = S^* \circ T^*$.

   Plus: $(\id_V)^* = \id_{V^*}$ as a standalone line.

2. **Lines 451–511 (MAJOR organization):** two options:
   - (a) Move the double dual subsection (485–511) to appear *before* the exercises, then the exercise solution references previously-introduced material.
   - (b) Move Exercise 4 and its solution to after the double dual subsection.

   Both are clean; **(a)** preserves exercise numbering.

3. **Spelling:** "Kernals" → "Kernels", "kernal" → "kernel", "more that merely" → "more than merely".
4. **`Tr` rendering:** same fix as Lecture 5.
5. **Line 229 forward references:** add a line acknowledging "concepts introduced in a later lecture" or defer the note.
6. **Line 18 tone:** cut per voice policy.

---

## 7. Cross-cutting (all of Batch 1)

These are patterns that span multiple lectures — I'd like you to confirm the policy before I apply anything:

### 7.1 "kernel" / "kernal"
Misspelled `kernal` appears in lectures 2, 3, and 6 (and possibly elsewhere; I'll grep the full batch during the fix pass). Mechanical global replace within scope.

### 7.2 `Tr` as operator
`\operatorname{Tr}` (or a `\Tr` macro declared once in the preamble) should be used consistently. Preamble check pending — if `\Tr` isn't defined I'd add one line rather than scatter `\operatorname` everywhere.

### 7.3 Forward references
Per your original criterion "no forward references unless specifically noted", several places cite later material implicitly. Options for each forward reference:
- **Explicit disclaimer**, e.g., `\nt{Citing X, which is proven in Lecture Y below.}` (lowest-cost).
- **Reorder** the material so the citation is backward-looking.
- **Inline-define** the missing concept (e.g., eigenvalues in Lecture 5).

I'll pick per-location based on your preference. Default I'd use: disclaim if a single line, reorder if the concept is central.

### 7.4 "LLM-esque" / informal voice
There are scattered informal asides I've flagged as MINOR (tone). These are a matter of editorial taste — I don't want to strip personality from your notes. Please pick a policy:
- (a) Leave all voice as-is (fix only technical/mathematical issues).
- (b) Remove only the most egregious asides (the "suffering immensely" parenthetical, the "sorrryyyyyy:)", the "retching" line, "(duh)" filler, "(what a fun word)").
- (c) Strict professional voice — strip all informal asides.

**Recommendation: (b).**

---

## 8. What I have NOT done yet

- Run LaTeX compilation to catch any additional rendering bugs (the `\textbf\{`, `\sum_{n}^{i=1}`, etc., would definitely fail visual inspection; the rest are semantic).
- Audited the preamble `preamble.tex` for macros actually used vs. defined.
- Batch 2 (Lectures 7–12) or Batch 3 (Lectures 13–17).

---

## 9. Your decisions before I proceed

Please confirm (or amend) on each:

1. **Lecture 3, lines 116/118 (coset relation):** go with fix **(A)** (change the relation to $a^{-1}b \in H$)? Or prefer **(B)** (switch the text to right cosets)?
2. **Lecture 3, lines 155–165 ($S_3$ example):** okay for me to draft a replacement using right-to-left composition and send for review?
3. **Lecture 3, line 317 (Cayley uses FIT):** rephrase to avoid FIT, or reorder so FIT precedes Cayley?
4. **Lecture 5, eigenvalue forward refs:** inline-define (a) or move the proposition (b)?
5. **Lecture 6, Proposition at 386:** split into two propositions as proposed?
6. **Lecture 6, double dual ordering:** move subsection before exercise?
7. **Voice policy (7.4):** (a), (b), or (c)?
8. **Forward-reference policy (7.3):** default to disclaim-when-short, reorder-when-central?

Once you confirm, I'll make the edits in a single pass per lecture and produce a cleaned version for you to review, then start Batch 2.
