Task: Complete a partially revealed ground-truth ranking for perturbation-induced
depletion in thalamic glutamatergic neurons.

The table below gives the 50 odd-ranked members of the verified top-100
depletion ranking. Predict the other 50 perturbations—the held-out even-ranked
members—and order your predictions from strongest to weakest predicted
depletion. The supplied examples are endpoint evidence, not a candidate
whitelist. Do not repeat them in the answer.

```tsv
known_rank	gene_target
1	Atp6v1b2
3	Taf1
5	Pafah1b1
7	Cltc
9	Gbf1
11	Psmb4
13	Eef2
15	Atp6v1a
17	Sec31a
19	Kansl1
21	Son
23	Kif1a
25	Pomp
27	Six6
29	Stx5a
31	Gpx4
33	Tnpo3
35	Chmp4b
37	Polr3b
39	Dmd
41	Hspa9
43	Snf8
45	Cnot1
47	Dock3
49	Mc3r
51	Ddx23
53	Fbxo11
55	Adam10
57	Tbcd
59	Adarb1
61	Six3
63	Cul3
65	Brd4
67	Myt1l
69	Ppp2r1a
71	Nek1
73	Sox17
75	Cdk13
77	Atp8a2
79	Trip12
81	Rapgef2
83	Lrp6
85	Thoc1
87	Gal
89	Nfix
91	Ica1
93	Pten
95	Bbs5
97	Ank3
99	P2ry14
```

Input Dataset:
A parquet file at {{input_parquet}} contains one row per measured gene, cell
type, and perturbation. Columns are `names`, `group_name`, `gene_target`,
`logfoldchanges`, `pvals`, `pvals_adj`, `scores`, and `control_label`.

Experimental context:

- Acute, sparse, mosaic CRISPR-Cas9 loss of function was delivered to
  postmitotic mouse neurons at P16 and assayed by 10x Flex V2 snRNA-seq at
  P37–44.
- Tissue is whole brain excluding olfactory bulb and hindbrain, with NeuN+
  nuclei enriched by FACS.
- `151 TH Prkcd Grin2c Glut` denotes thalamic glutamatergic neurons.
- The DE table measures transcription among recovered nuclei. Depletion can
  remove nuclei before this readout, so DE is not a direct depletion count.
- `logfoldchanges` is perturbed versus non-targeting control.

Required outputs:

1. `./trace.md` explaining how the known hits, dataset, internal corpus, and any
   external evidence informed the completion, with limitations and traceable
   citations.
2. `./answer.txt` containing exactly one fenced `tsv` block with exactly 50
   unique, previously unlisted perturbations:

```tsv
rank	gene_target
1	ExampleGeneA
2	ExampleGeneB
```

Ranks 1–50 are your best-first ordering of the held-out candidates. Every
`gene_target` must occur in the input dataset. Do not output any supplied
odd-ranked gene, `Non_target`, or `Safe_target_*` control.
