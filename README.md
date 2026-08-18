# 🧫 StruView

**Interactive 3D structural explorer of the *Streptococcus pyogenes* virulence factors** targeted
by a plant anti-virulence docking study.

Built by **Hafiza Muntaha Fatima** (BS Biochemistry, GCWUF) · [github.com/hafizamuntaha-fatima](https://github.com/hafizamuntaha-fatima)

StruView streams the real experimental structures from the **RCSB PDB** (SpeB = 2UZJ, SpeA = 1B1Z),
renders them in 3D with **3Dmol.js**, and highlights the **catalytic dyad (Cys47/His195)** where the
plant flavonoids were docked. It communicates a target's structure and active site — the starting
point of structure-guided inhibitor design.

## What it does
- **3D structure viewer** — rotate/zoom the target; catalytic residues highlighted in orange.
- **Docking data** — real AutoDock Vina affinity ranking (EGCG, quercetin, thymoquinone vs SpeB/SpeA).
- **Methods & honesty** — states clearly what the tool is and is not.

## Data provenance (everything is real)
- **Structures:** RCSB PDB 2UZJ (SpeB), 1B1Z (SpeA) — streamed live at runtime.
- **Docking affinities:** AutoDock Vina 1.2.5, seed 42, from
  [spyogenes-docking](https://github.com/hafizamuntaha-fatima/spyogenes-docking).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Push to GitHub (can be private).
2. https://share.streamlit.io → New app → this repo → main file `app.py`.
3. Advanced settings → Python 3.11 → Deploy. You get a public URL.
   *(No heavy dependencies; the 3D viewer loads 3Dmol.js from a CDN and structures from RCSB.)*

## Honest limitations
Visualises and annotates **published** structures — no structure was determined here, and the exact
3D docked pose is not reproduced (only documented catalytic residues are shown). Docking predicts
relative affinity, not efficacy; no synergy is claimed; wet-lab validation is planned.
