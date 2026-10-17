# Instructor notes — 15.1 Bonding, hybridisation and functional groups

- Objective: the learner assigns sp³/sp²/sp from electron domains, counts σ and π bonds, reads skeletal formulas and SMILES, and names the functional groups of a drug-sized molecule by eye and with RDKit.
- Likely confusion: counting a double bond as two domains; whether lone pairs count; the conjugated O and N that RDKit calls sp² while many textbooks say sp³.
- Misconception: "hybridisation causes the shape". It is a description chosen to fit a shape fixed by electron repulsion and the full MO picture (12.6). Also: "a double bond is twice a single bond".
- Analogy: functional groups are like the tools on a Swiss army knife; the handle (carbon skeleton) is similar in every knife, the tool decides what it can do.
- Expected hands-on result: C–C 153–154 pm, C=C 133–134 pm, C≡C 120–121 pm; angles 109.5°, 120°, 180°. Script: ethane 7/0, ethene 5/1, ethyne 3/2, benzene 12/3, aspirin 21/5, paracetamol 20/4; aspirin arene + carboxylic acid + ester; paracetamol arene + phenol + amide; carvone alkene ×2 + ketone. Drill: allene central C sp (2 π), trimethylamine N sp³, CO₂ C sp, acetone O sp².
- Extension: write SMARTS for an acid chloride and an anhydride and test them on PubChem SMILES of acetyl chloride and acetic anhydride; or use the rule σ = N − 1 + r to count σ bonds in caffeine and check with RDKit.
