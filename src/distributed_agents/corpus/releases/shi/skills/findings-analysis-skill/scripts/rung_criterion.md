You are grading ONE perturbation finding for how much it reveals about biology — its
"so what" — from the downstream readout genes it moved. Grade to the LOWEST rung it can
truthfully reach. Do not let a gene's disease fame, or the surprise that two genes differ,
lift the rung: only the functional content of the readout genes can.

RUNG 0 — regulatory bookkeeping. The finding states a relationship (A≠B, A regulates B,
A and B are non-interchangeable / do not phenocopy / are uncoupled, "engaged but the
readout was silent," "the expected program was absent") but says nothing about what the
cell can now DO. A silent or absent readout is rung 0 no matter how clean or surprising.

RUNG 1 — a named program with no capability consequence. The readout is labeled as a
pathway/module (sterol/SREBP, UPR/ISR, spliceosome, clock, RAS-MAPK, Wnt, proteostasis)
but no specific effector genes are named that change what the cell does. A generic
"synaptic module" with no named effectors stays at rung 1.

RUNG 2 — the readout switches a capability or identity on or off. Specific EFFECTOR genes
carry it: ion channels, neurotransmitter receptors, transporters/pumps, synaptic-release
or adhesion machinery, or cell-fate/identity transcription factors — such that the cell
plausibly GAINS, LOSES, or aberrantly RUNS a concrete capability (excitability, a receptor
complement, transmitter release, identity), OR the readout is ECTOPIC (an out-of-lineage
program the cell should not run, e.g. a germline/meiotic or cell-cycle/replication program
in a postmitotic neuron). You must be able to name the effector genes that carry it.

RUNG 3 — that capability/identity change maps to a concrete phenotype, circuit, or
vulnerability (a mechanism you could state and test), not just a capability list.

How to weigh: (1) the FUNCTIONAL WEIGHT of the named readout genes — what those specific
genes do — not their count or their pathway label; (2) ECTOPY — an out-of-lineage program
is a strong up-rung signal. Down-rank: disease-gene fame with no effector readout;
non-interchangeability / uncoupling / "does not phenocopy" with no effector readout; a
generic program label with no specific effector named.

SET `interest` (0-1) BY CAPABILITY SHARPNESS — this is the ranking signal, so make it
discriminate:
  - 0.85-1.00: an ECTOPIC out-of-lineage program, OR a SPECIFIC coherent capability switch
    you can name in a phrase (a defined ion-channel complement; a receptor-identity swap with
    one class down and another up; an inhibitory- or excitatory-transmission set; a fate
    change). The named genes together constitute the capability.
  - 0.50-0.70: effector genes are present but form a GENERIC or loose synaptic / plasticity /
    activity module with no single specific capability named. (Recognize the effectors — do
    not deny them — but rank below the sharp cases.)
  - 0.20-0.40: only a named pathway/program label (sterol, UPR, spliceosome, clock, …) with
    no effector genes.
  - 0.00-0.15: regulatory bookkeeping — non-interchangeability / uncoupling / "engaged but
    silent" / expected-program-absent — no capability claim.
Keep `rung` as defined above (recognize effector content generously); `interest` is what
ranks the list, so let capability sharpness spread the scores.

Output ONLY a compact JSON object on one line:
{"rung": <0|1|2|3>, "interest": <float 0-1>, "carrying_genes": ["..."], "why": "<= 20 words"}
where `interest` is your overall ranking score (higher = more worth a human's attention),
monotonic with rung but allowed to break ties within a rung by how sharp the capability
change is. `carrying_genes` are the specific readout genes that justify the rung (empty for
rung 0/1). Emit the JSON and nothing else.
