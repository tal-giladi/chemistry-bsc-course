"""Canonical lesson manifest: module titles, stages and lesson titles.
Single source of truth for _sidebar.md, lesson ids and H1s. Run `py scripts/manifest.py` to regenerate _sidebar.md.
Paths are stable ids: never rename, reorder or remove a lesson once published; add new lessons at the end of a module."""
from pathlib import Path

STAGES = {
    1: "Year 1 — Toolkit and foundations",
    12: "Year 2 — The chemistry core",
    25: "Year 3 — Advanced core, labs and research",
}

MODULES = [
    # ---------------- Year 1 ----------------
    ("Orientation, Units and Safe Practice", [
        "How this course works and what it cannot train",
        "Units, significant figures and dimensional analysis",
        "The lab notebook and the lab report",
        "Chemical safety: hazards, SDS and Israeli law",
        "Your home kit and first measurement"]),
    ("Calculus for Chemists", [
        "Functions chemists meet: power, exponential and logarithm",
        "Derivatives as rates of change",
        "Integrals as accumulated change",
        "Series and approximations",
        "Functions of several variables and partial derivatives"]),
    ("Linear Algebra and Differential Equations", [
        "Vectors, matrices and solving linear systems",
        "Eigenvalues and eigenvectors",
        "First-order differential equations and rate laws",
        "Second-order equations and oscillators",
        "Coupled systems: consecutive reactions"]),
    ("Physics for Chemists", [
        "Forces, energy and momentum",
        "Oscillations and waves",
        "Electrostatics: charge, field and potential",
        "Circuits, current and resistance",
        "Light as an electromagnetic wave and as photons"]),
    ("Python for Scientists", [
        "Python setup and the scientific stack",
        "Arrays, vectorised maths and plotting",
        "Fitting models to data with uncertainty",
        "Reading real instrument data",
        "Reproducible analysis notebooks"]),
    ("Biology for Chemists", [
        "Cells, membranes and compartments",
        "Proteins: from amino acids to folds",
        "Nucleic acids and the flow of information",
        "Metabolism and energy currency"]),
    ("Foundations of Chemistry A: Atoms, Bonds and Amounts", [
        "Atoms, isotopes and the mole",
        "Electron configuration and periodic trends",
        "Ionic and covalent bonding, Lewis structures",
        "VSEPR, polarity and intermolecular forces",
        "Stoichiometry and limiting reagents",
        "Gases: ideal and real",
        "Lab: weighing, glassware and making solutions"]),
    ("Foundations of Chemistry B: Energy, Equilibrium and Electrons", [
        "Thermochemistry and Hess's law",
        "Entropy, free energy and spontaneity",
        "Chemical equilibrium and Le Chatelier",
        "Acids, bases and pH",
        "Redox reactions and balancing",
        "Electrochemical cells and the Nernst equation",
        "Lab: coffee-cup calorimetry and a first titration"]),
    ("Analytical Chemistry 1: Measurement and Error", [
        "Types of error, accuracy and precision",
        "Statistics: mean, standard deviation and confidence intervals",
        "Propagation of uncertainty",
        "Calibration, linear regression and detection limits",
        "Titration theory and titration curves",
        "Buffers and gravimetric analysis"]),
    ("Analytical Chemistry Lab 1", [
        "The titration bench: indicators, burettes and endpoints",
        "Potentiometric and redox titrations",
        "Precipitation and complexometric titrations",
        "Gravimetry, electrogravimetry and coulometry",
        "Ion-selective electrodes and water testing",
        "Project: home vinegar titration with full error analysis"]),
    ("Scientific English: Reading and Writing Chemistry", [
        "Reading a research paper efficiently",
        "Finding and judging sources and data",
        "Writing a lab report and a figure that tells the story"]),
    # ---------------- Year 2 ----------------
    ("Quantum Theory in Chemistry", [
        "Why classical physics fails: photons, spectra and waves",
        "The Schrödinger equation and the particle in a box",
        "Tunnelling",
        "The harmonic oscillator and molecular vibrations",
        "Rotors, angular momentum and the hydrogen atom",
        "Many-electron atoms, molecular orbitals and selection rules"]),
    ("Chemical Thermodynamics", [
        "Systems, state functions and the first law",
        "Enthalpy, heat capacity and calorimetry",
        "The second law and entropy",
        "Free energy and chemical potential",
        "Phase equilibria and phase diagrams",
        "Solutions, activity and equilibrium constants"]),
    ("Chemical Physics Lab: Oscillators and Signals", [
        "Measuring a spring with your phone",
        "Damping, anharmonicity and the Q factor",
        "Normal modes of three coupled masses",
        "From coupled masses to the vibrations of CO2",
        "Signals, sampling and the Fourier transform",
        "Project: RLC resonance curve and Q factor"]),
    ("Organic Chemistry 1: Structure and Reactions", [
        "Bonding, hybridisation and functional groups",
        "Conformations and strain",
        "Stereochemistry and chirality",
        "Curved arrows, acids and bases in organic chemistry",
        "Nucleophilic substitution: SN1 and SN2",
        "Elimination: E1 and E2",
        "Alkenes and alkynes"]),
    ("Organic Chemistry 2: Carbonyls, Aromatics and Synthesis", [
        "Alcohols, ethers and oxidation",
        "Aldehydes, ketones and nucleophilic addition",
        "Carboxylic acids and their derivatives",
        "Enolates and the aldol reaction",
        "Aromaticity and electrophilic aromatic substitution",
        "Amines, sugars and heterocycles",
        "Retrosynthesis and multi-step planning"]),
    ("Identifying Compounds from Spectra", [
        "Mass spectrometry: molecular ion and fragments",
        "Infrared spectroscopy: functional groups",
        "Proton NMR: shift, integration and splitting",
        "Carbon NMR and 2D NMR basics",
        "Putting it together: solving unknowns",
        "Project: 50 unknowns from real SDBS spectra"]),
    ("Inorganic Chemistry", [
        "Periodic trends in depth and the main-group elements",
        "Solid structures and lattice energy",
        "Coordination compounds: geometry and isomers",
        "Crystal field and ligand field theory",
        "Colour and magnetism of transition-metal complexes"]),
    ("Analytical Chemistry 2: Instrumental Methods", [
        "UV-Vis spectrophotometry and Beer-Lambert",
        "Fluorescence and atomic spectroscopy",
        "Extraction and the theory of chromatography",
        "Gas and liquid chromatography",
        "Electroanalysis and cyclic voltammetry"]),
    ("Molecular Spectroscopy and Symmetry", [
        "Light-matter interaction and selection rules",
        "Rotational spectra",
        "Vibrational spectra and Raman",
        "Electronic spectra and Franck-Condon",
        "Symmetry elements and point groups",
        "Character tables and predicting IR and Raman bands"]),
    ("Statistical Thermodynamics", [
        "Microstates, the Boltzmann distribution and temperature",
        "The partition function",
        "Molecular partition functions: translation, rotation, vibration",
        "From partition functions to equilibrium constants"]),
    ("Chemical Kinetics", [
        "Rate laws and integrated rate laws",
        "Measuring rates: methods and data analysis",
        "Mechanisms and the steady-state approximation",
        "Temperature dependence: Arrhenius and transition-state theory",
        "Catalysis and enzyme kinetics"]),
    ("Physical Chemistry Lab 1", [
        "Gas laws and kinetic theory in the lab",
        "Thermochemistry: enthalpy of neutralisation and solution",
        "Equilibrium constant by spectrophotometry",
        "Kinetics: dye fading tracked with a phone camera",
        "Electrochemistry: cells, potentials and a lemon battery",
        "Surface tension and detergents"]),
    ("Organic Chemistry Lab 1", [
        "Lab techniques: reflux, extraction and drying",
        "Purification: recrystallisation and distillation",
        "Checking purity: TLC and melting point",
        "Virtual synthesis: aspirin",
        "Virtual synthesis: substitution, Grignard and aldol",
        "Multi-step synthesis with spectra at every step"]),
    # ---------------- Year 3 ----------------
    ("Analytical Chemistry Lab 2", [
        "Spectrophotometry of mixtures and a phone spectrometer",
        "Fluorescence: quinine in tonic water",
        "Atomic absorption and emission",
        "Gas chromatography and GC-MS",
        "HPLC method thinking",
        "Cyclic voltammetry in practice"]),
    ("Bio-inorganic Chemistry", [
        "Metals in biology: why these elements",
        "Bonding in transition-metal complexes revisited",
        "Oxygen transport: haemoglobin and myoglobin",
        "Metalloenzymes, electron transfer and respiration"]),
    ("Electromagnetism and Matter", [
        "Maxwell's equations for chemists",
        "Multipoles and molecular charge distributions",
        "Polarisability and dielectrics",
        "Intermolecular forces from electrostatics"]),
    ("Structure and Reactivity in Organic Chemistry", [
        "Potential energy surfaces and reaction coordinates",
        "The Hammond postulate and selectivity",
        "Linear free-energy relationships: Hammett",
        "Reactive intermediates: carbocations, radicals, carbenes",
        "Probing mechanisms: isotope effects and trapping"]),
    ("Biochemistry and Enzymology", [
        "Protein structure and stability",
        "Enzyme kinetics: Michaelis-Menten in depth",
        "Inhibition and regulation",
        "Enzyme mechanisms: catalytic strategies",
        "Metabolic pathways as chemistry"]),
    ("Physical Chemistry Lab 2", [
        "IR spectroscopy from first principles: HCl rotation-vibration",
        "Electron spin resonance and hyperfine splitting",
        "Speed of sound and the heat-capacity ratio of air",
        "Electronic spectra of conjugated dyes: particle in a box"]),
    ("Computational Chemistry Lab", [
        "Setting up Avogadro, xtb and ORCA",
        "Molecular mechanics and conformer search",
        "Hartree-Fock and DFT: geometry optimisation",
        "Calculated IR and NMR spectra versus experiment",
        "Transition states and reaction barriers",
        "Excited states with time-dependent DFT"]),
    ("Electives: Electrochemistry and Solid State", [
        "Electrode kinetics and the Butler-Volmer equation",
        "Batteries, fuel cells and corrosion",
        "Crystals, lattices and X-ray diffraction",
        "Band theory: metals, semiconductors and insulators",
        "Choosing your further electives"]),
    ("Research Project", [
        "Choosing a question you can answer at home",
        "Designing the study and managing the data",
        "Writing the report and the poster",
        "Getting feedback and what comes next"]),
]


def lessons():
    """Yield (module_no, lesson_no, global_no, id, title, path)."""
    g = 0
    for m, (_, ls) in enumerate(MODULES, 1):
        for l, t in enumerate(ls, 1):
            g += 1
            yield m, l, g, f"{m:02d}.{l}", t, f"lessons/module-{m:02d}/lesson-{l:02d}.md"


def sidebar():
    out = ["- [Home](/)", "- [Course map](COURSE-MAP.md)", "- [Glossary](glossary.md)",
           "- [Templates](templates/README.md)", "- [Simulations](simulations/README.md)",
           "- [References](references/README.md)", ""]
    all_ls = list(lessons())
    for m, (title, _) in enumerate(MODULES, 1):
        if m in STAGES:
            out += ["", f"- {STAGES[m]}"]
        out.append(f"- **Module {m} — {title}**")
        for mm, l, g, lid, t, p in all_ls:
            if mm == m:
                out.append(f"  - [{g:02d} · {t}]({p})")
        out.append(f"  - [Module {m} quiz](assessments/module-{m:02d}-quiz.md)")
    return "\n".join(out).replace("\n\n\n", "\n\n") + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    (root / "_sidebar.md").write_text(sidebar(), encoding="utf-8", newline="\n")
    # The GitHub Pages preview (docsify) needs root-absolute links; the Academy reads _sidebar.md.
    import re
    (root / "preview/_sidebar.md").write_text(re.sub(r"\]\(([a-zA-Z])", r"](/\1", sidebar()), encoding="utf-8", newline="\n")
    print(f"{len(list(lessons()))} lessons, {len(MODULES)} modules")
