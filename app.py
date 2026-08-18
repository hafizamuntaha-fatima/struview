"""
StruView — interactive 3D structural explorer of the Streptococcus pyogenes
virulence-factor targets used in a plant anti-virulence docking study.

It loads the real experimental structures from the RCSB PDB (SpeB = 2UZJ,
SpeA = 1B1Z), renders them in 3D (3Dmol.js), and highlights the catalytic site
where the plant compounds were docked. It sits at the plant-pathogen structural
interface from the computational side.

Honesty: these are PUBLISHED structures viewed and annotated — no structure was
determined here, and the exact docked pose coordinates are not reproduced (only
the documented catalytic residues are highlighted). Docking affinities are real
AutoDock Vina output from the thesis pipeline.

Author: Hafiza Muntaha Fatima  ·  github.com/hafizamuntaha-fatima
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

DATA = Path(__file__).parent / "data"

st.set_page_config(page_title="StruView", page_icon="🧫", layout="wide")


@st.cache_data
def load_data():
    docking = pd.read_csv(DATA / "docking_results.csv")
    targets = pd.read_csv(DATA / "targets.csv")
    return docking, targets


docking, targets = load_data()


def structure_view(pdb_id: str, resi: list[str], height: int = 520) -> str:
    """Build a 3Dmol.js HTML block that downloads a PDB structure from RCSB and
    highlights the given residues (the catalytic site)."""
    resi_js = str(resi) if resi else "[]"
    highlight = ""
    if resi:
        highlight = f"""
        v.setStyle({{resi:{resi_js}}},
                   {{stick:{{colorscheme:'orangeCarbon', radius:0.35}},
                     cartoon:{{color:'spectrum'}}}});
        v.addStyle({{resi:{resi_js}}}, {{sphere:{{radius:0.5, color:'orange'}}}});
        v.addResLabels({{resi:{resi_js}}}, {{fontSize:12, showBackground:true}});
        """
    return f"""
    <div id="viewer" style="width:100%;height:{height}px;position:relative;
         border:1px solid #ddd;border-radius:8px;"></div>
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <script>
      let v = $3Dmol.createViewer(document.getElementById('viewer'),
                                  {{backgroundColor:'white'}});
      $3Dmol.download('pdb:{pdb_id}', v, {{}}, function() {{
        v.setStyle({{}}, {{cartoon:{{color:'spectrum'}}}});
        {highlight}
        v.zoomTo();
        v.render();
      }});
    </script>
    """


# ---------- header ----------
st.title("🧫 StruView")
st.caption(
    "Interactive 3D structural explorer of the *Streptococcus pyogenes* virulence "
    "factors (SpeB, SpeA) targeted by a plant anti-virulence docking study."
)

tab_view, tab_data, tab_methods = st.tabs(
    ["🧬 3D structure viewer", "📊 Docking data", "📖 Methods & honesty"]
)

# ================= TAB 1: 3D VIEWER =================
with tab_view:
    names = {r["receptor"]: f'{r["receptor"]} — {r["full_name"]}' for _, r in targets.iterrows()}
    pick = st.selectbox("Choose a target", list(names.keys()),
                        format_func=lambda k: names[k])
    trow = targets[targets["receptor"] == pick].iloc[0]
    resi = [] if pd.isna(trow["site_resi"]) else str(trow["site_resi"]).split(";")

    c1, c2 = st.columns([2, 1])
    with c1:
        components.html(structure_view(trow["pdb_id"], resi), height=545)
        st.caption("Drag to rotate · scroll to zoom · structure streamed live from the RCSB PDB.")
    with c2:
        st.markdown(f"**Target:** {trow['full_name']}")
        st.markdown(f"**PDB:** `{trow['pdb_id']}`  ·  [RCSB entry](https://www.rcsb.org/structure/{trow['pdb_id']})")
        st.markdown(f"**Docking site:** {trow['site_label']}")
        st.info(trow["note"])
        best = docking[docking["receptor"] == pick].sort_values("best_affinity_kcal_mol").iloc[0]
        st.metric(f"Strongest predicted binder — {pick}",
                  f"{best['ligand']}  {best['best_affinity_kcal_mol']} kcal/mol")
        if resi:
            st.caption("Highlighted (orange sticks/spheres): the catalytic dyad where the "
                       "plant flavonoids were docked.")

# ================= TAB 2: DOCKING DATA =================
with tab_data:
    st.subheader("Binding-affinity ranking (real AutoDock Vina output)")
    ranked = docking.sort_values("best_affinity_kcal_mol").reset_index(drop=True)
    ranked.index += 1
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(ranked.rename(columns={
            "receptor": "Target", "pdb_id": "PDB", "ligand": "Ligand",
            "best_affinity_kcal_mol": "Best affinity (kcal/mol)"}),
            use_container_width=True)
    with col2:
        fig = px.bar(docking, x="ligand", y="best_affinity_kcal_mol", color="receptor",
                     barmode="group",
                     labels={"best_affinity_kcal_mol": "Affinity (kcal/mol)",
                             "ligand": "Ligand", "receptor": "Target"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    st.info("EGCG (green tea) is the strongest predicted binder to both virulence factors "
            "(best: EGCG–SpeB, −7.574 kcal/mol, at the Cys47/His195 catalytic site).")

# ================= TAB 3: METHODS & HONESTY =================
with tab_methods:
    st.subheader("Methods & honest limitations")
    st.markdown("""
**Structures.** Streamed live from the **RCSB PDB**: SpeB = **2UZJ** (cysteine protease),
SpeA = **1B1Z** (superantigen). Rendered with **3Dmol.js**. For SpeB, the **Cys47/His195**
catalytic dyad (marked by the bound E64 inhibitor) is highlighted — this is where the plant
flavonoids were docked.

**Docking.** AutoDock Vina 1.2.5, fixed seed 42; best affinity per ligand–target pair, from the
thesis pipeline ([spyogenes-docking](https://github.com/hafizamuntaha-fatima/spyogenes-docking)).

**What this tool is — and is not:**
- It **visualises and annotates published structures**; no structure was determined here.
- It does **not** reproduce the exact 3D docked pose (only the documented catalytic residues are
  shown). The pose figure lives in the docking repo.
- Docking predicts **relative affinity, not efficacy**; **no synergy is claimed**; wet-lab
  validation (MIC, checkerboard/FICI) is **planned**.

**Why this tool.** It communicates a target's structure and active site — the starting point of
structure-guided inhibitor design — and shows I can work at the plant–pathogen structural interface
computationally, which I would like to extend with experimental structure determination.

*Built by Hafiza Muntaha Fatima · BS Biochemistry, GCWUF · github.com/hafizamuntaha-fatima*
""")
