# StruView — Methods Note (1 page)

**Author:** Hafiza Muntaha Fatima · BS Biochemistry, Government College Women University Faisalabad

## Purpose
StruView communicates the **structural context** of a plant anti-virulence docking study: it shows
the *Streptococcus pyogenes* virulence-factor targets in 3D and highlights the catalytic site where
plant flavonoids were docked — the entry point of structure-guided inhibitor design.

## Targets (real, published structures)
- **SpeB — PDB 2UZJ**: streptococcal pyrogenic exotoxin B, a cysteine protease. Catalytic dyad
  **Cys47 / His195** (marked by the bound E64 inhibitor) — the docking site.
- **SpeA — PDB 1B1Z**: streptococcal pyrogenic exotoxin A, a superantigen; blind-docked across the surface.

## Methods
1. **Structure rendering** — structures streamed live from the **RCSB PDB** and displayed with
   **3Dmol.js** (cartoon + highlighted active-site residues).
2. **Docking (from thesis pipeline)** — AutoDock Vina 1.2.5, fixed seed 42; best affinity per
   ligand–target pair (EGCG, quercetin, thymoquinone).

## Key result
EGCG is the strongest predicted binder to both virulence factors (best: **EGCG–SpeB, −7.574
kcal/mol**, at the Cys47/His195 catalytic site).

## Honest scope
- Visualises and annotates **published** structures — **no structure was determined here**.
- Does **not** reproduce the exact 3D docked pose; only documented catalytic residues are highlighted.
- Docking gives **relative affinity, not efficacy**; **no synergy** is claimed; wet-lab validation
  (MIC, checkerboard/FICI) is **planned**.

## Relevance to structural biology (StruBE context)
Structure-guided inhibitor design begins with understanding a target's fold and active site.
StruView demonstrates comfort at the **plant–pathogen structural interface** from the computational
side — which I would like to extend with experimental structure determination (X-ray/SAXS/cryo-EM).

*Reproduce: `pip install -r requirements.txt && streamlit run app.py`.*
