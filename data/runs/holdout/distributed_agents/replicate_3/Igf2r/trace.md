# Igf2r prediction trace

## Question

The requested held-out target file contains one perturbation:

```text
Igf2r
```

I interpreted the task as a point prediction of `n_degs`, the number of measured genes with
`pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` cell group after acute sparse
AAV-CRISPR loss of the target. `Igf2r` itself is absent from both supplied training tables, so
the prediction has to be transferred from non-held-out perturbations and biology of the
cation-independent mannose-6-phosphate/IGF-II receptor rather than inferred from an Igf2r
signature.

The main ambiguity I resolved was how to score weak singleton signatures. In this dataset many
one-DEG lysosomal examples are just the perturbed transcript itself passing FDR, not a downstream
lysosomal stress program. I therefore treated `0` and "target self only" as much closer evidence
than the raw difference between 0 and 1 DEGs would imply.

## Sources used

Same-experiment sources:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 111_Igf2r.csv]`
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile comparison over a declared 31-gene Igf2r-relevant cohort in `151 TH Prkcd Grin2c Glut`

External mechanism sources:

- Brown, Jones and Forbes 2009, DOI `10.1016/S0083-6729(08)00625-0`, PMID `19251056`: IGF2R/CI-MPR is a mannose-6-phosphate receptor for trans-Golgi-to-endosome delivery of lysosomal enzymes and a scavenger receptor for IGF-II.
- Takeda et al. 2019, DOI `10.1038/s41419-019-2117-9`, PMID `31748500`: IGF2R depletion can impair cathepsin transport to lysosomes and autophagy/mitophagy in cervical cancer cells.
- Han et al. 2020, DOI `10.1080/15548627.2020.1761742`, PMID `32397873`: retromer VPS35 and SNX-BAR dimers participate in IGF2R/CI-MPR retrograde retrieval from endosomes to the trans-Golgi network.
- Ahn et al. 2023, DOI `10.1126/science.adf6249`, PMID `37856615`: a genome-wide LYTAC screen confirmed that CI-M6PR/IGF2R trafficking depends on endosomal recycling and retromer state.
- Tavares et al. 2024, DOI `10.1016/j.jbc.2024.105700`, PMID `38307383`: an AP-1 gamma2-containing adaptor complex is required for endosome-to-Golgi retrieval of CI-MPR.

## Computational checks

I first read the manifest and confirmed that `Igf2r` was the only requested target and was absent
from the 1,674-row focal training-count table. The focal training endpoint is extremely sparse:
1,205 of 1,674 perturbations, 72.0%, have `n_degs = 0`; 1,481 have `n_degs <= 1`; and the median
is 0. This made it important to ask whether a proposed Igf2r analog belonged to a rare broad
response class or to the common buffered class.

I then queried the large parquet only for `group_name = '151 TH Prkcd Grin2c Glut'` and measured
Igf2r pathway comparators, joining those observations to the focal `n_degs` table. The key
results were:

| comparator class | measured perturbations in focal training data | observed `n_degs` and expression evidence |
| --- | --- | --- |
| M6P synthesis and soluble lysosomal cargo | `Gnptab`, `Gnptg`, `Manba`, `Ppt1`, `Psap`, `Gaa`, `Ctsb` | `Gnptab`, `Gnptg`, and `Manba` had 0 DEGs. `Ppt1`, `Psap`, `Gaa`, and `Ctsb` each had 1 DEG, and in each case the only significant gene was the target transcript itself. |
| Other lysosomal cargo/receptor genes | `Sort1`, `Tmem106b`, `Scarb2`, `Lamp2` | `Sort1` and `Lamp2` had 0 DEGs. `Tmem106b` and `Scarb2` each had 1 DEG, again the target itself. |
| MPR-adjacent endocytic or cargo receptors | `Lrp1`, `Lrp2`, `Sorl1`, `Igf1r`, `Insr` | all had 0 DEGs. |
| TGF-beta signaling controls | `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Smad2`, `Smad3`, `Smad4`, `Smad6` | all had 0 DEGs except `Smad2`, with 1. |
| CI-MPR retrieval / trafficking counterexamples | `Ap1b1`, `Ap1s2`, `Cltc`, `Vps35`, `Vps35l`, `Washc4`, `Vps53`, `Vps54`, `Rab7`, `Vps41` | `Ap1s2`, `Vps35l`, `Washc4`, `Vps53`, and `Vps41` had 0 DEGs; `Ap1b1` had only self as its 1 DEG; `Cltc` had 3 weak non-Igf2r genes; `Vps35` had 17 DEGs including `Atp2a2`, `Brsk1`, `Grin2b`, and `Vps35` itself; `Vps54` had 31; `Rab7` was the strong counterexample with 501 DEGs, including V-ATPase/lysosomal genes such as `Atp6v1b2`, `Dpp7`, and `Lamp2` plus sterol genes such as `Insig1`, `Msmo1`, and `Fdft1`. |
| mTOR/late-lysosome counterexamples | `Mtor`, `Rptor`, `Tsc2` | `Mtor` had 2 DEGs, `Rptor` 0, and `Tsc2` 86, supporting that only selected lysosome-coupled growth-control nodes make a broader 151 TH transcriptomic state. |

The focal parquet also showed that `Sort1` itself was down in the `Sort1` perturbation but did
not pass the FDR 0.05 endpoint in 151 TH (`logfoldchanges = -0.366`, `pvals_adj = 0.094`), while
`Gnptab` self was not significant (`pvals_adj = 1`). Thus the focal zero calls for the closest
M6P-pathway controls are not all guide-count or endpoint-count artifacts: some pathway members
show target RNA movement or target-only depletion without secondary mRNA changes.

Finally, I ran a Distributed Agents runtime `profile_compare` on a 31-node cohort of Igf2r-relevant
training perturbations using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the
significance gate. In that cohort, the inspected anchors had these focal response sizes:

| anchor | significant features |
| --- | ---: |
| `Sort1` | 0 |
| `Gnptab` | 0 |
| `Cltc` | 3 |
| `Vps35` | 17 |
| `Rab7` | 501 |

The point of this profile pass was not to use arbitrary whole-profile correlations between two
FDR-null vectors; the null anchors have many extreme but nonsignificant log-fold-change artifacts.
Instead I used it as a bounded audit that the selected M6P/lysosome comparators really contribute
no significant focal features, whereas `Rab7` and `Vps35` are qualitatively different positive
controls.

## Target-specific reasoning

### Igf2r

`Igf2r` encodes CI-MPR, a multifunctional receptor that binds mannose-6-phosphate tags on soluble
lysosomal enzymes and recycles between the trans-Golgi network, endosomes, and the plasma
membrane. It also binds IGF-II and has literature connections to latent TGF-beta activation.
Those functions made three same-assay neighborhoods relevant.

The closest M6P and lysosomal-cargo neighborhood argues for no FDR-significant downstream program
in this focal neuronal readout. `Gnptab` and `Gnptg`, which synthesize the M6P hydrolase tag,
were both flat in 151 TH: 0 DEGs each. Direct soluble hydrolase or lysosomal cargo perturbations
were also silent or target-only: `Manba` 0, `Ppt1` 1 self DEG, `Psap` 1 self DEG, `Gaa` 1 self
DEG, and `Ctsb` 1 self DEG. The internal Distributed Agents corpus has matching high-level claims:
claim `56e1e77cd2cb9bb6604f` states that acute perturbation of represented lysosomal disease
genes did not elicit a shared TFEB/MiT, ISR/UPR, autophagy, or storage-stress nuclear RNA program;
claim `2ea06b0f0f62f2fef4d7` states that represented soluble hydrolase, cargo, and M6P-pathway
perturbations were buffered in the sparse mosaic neuronal assay. This is the strongest within-
dataset evidence because CI-MPR loss should first perturb trafficking of exactly these M6P-tagged
hydrolases.

The receptor and ligand-scavenger comparisons point the same way. `Sort1`, another lysosomal
cargo receptor, had 0 DEGs in the focal group despite a near-threshold decrease in its own
transcript. `Lrp1`, `Lrp2`, `Sorl1`, `Igf1r`, and `Insr` all had 0 DEGs. TGF-beta pathway
perturbations were likewise almost entirely flat: `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Smad3`,
`Smad4`, and `Smad6` were 0. These are imperfect analogs for CI-MPR biochemistry, but they are
good counterweights against predicting a broad nuclear response solely because Igf2r can influence
IGF-II clearance or TGF-beta activation in other systems.

The main positive counterexamples are later and more disruptive than Igf2r. `Rab7` loss produced
501 DEGs with a clear V-ATPase/lysosome/sterol compensation state, and the Distributed Agents corpus
claim `726468d7afc216bc3be2` summarizes this as a selective Rab7 late-endosomal/lysosomal
compensation program. `Vps35` loss gave a smaller 17-gene signature in this focal group, consistent
with retromer being involved in CI-MPR retrieval, and `Cltc` gave 3 DEGs. However, the same retromer
branch did not generalize to measured relatives: `Vps35l`, `Washc4`, and `Vps41` were 0 in the
focal training counts, and Distributed Agents claim `02de8fcbbda046b67a7b` explicitly separates the modest
151 TH `Vps35` response from flat or divergent Retriever/Commander/WASH perturbations. Since Igf2r
is a cargo receptor whose loss is partially buffered by receptor redundancy, enzyme secretion and
recapture, and mosaic wild-type neighbors, it is closer to `Sort1`/`Gnptab`/hydrolase behavior
than to a core `Rab7` late-endosome collapse.

Putting those observations together, I predict that acute partial Igf2r loss in postnatal
`151 TH Prkcd Grin2c Glut` neurons will not cross the BH-adjusted Wilcoxon 0.05 gate for any
gene. The prediction is primarily driven by within-dataset evidence from `Gnptab`, `Gnptg`,
`Sort1`, and the hydrolase/cargo perturbations; external IGF2R biology was used to choose those
comparators and to demote broader `Rab7` and `Tsc2` stress states as less direct.

Predicted `n_degs`: 0.

## Limits

`Igf2r` itself was not measured as a perturbation in the training parquet, and the closest same
receptor, `M6pr`, was not a training target. None of the measured controls is a perfect same-complex
phenocopy: `Gnptab` and `Gnptg` perturb hydrolase phosphorylation upstream, `Sort1` carries a
different cargo repertoire, and `Vps35`/`Rab7` perturb retrieval or late-endosome identity rather
than the CI-MPR cargo receptor. The assay also measures nuclear RNA only; it does not assay
cathepsin secretion, lysosomal enzyme activity, IGF-II uptake, receptor localization, storage
material, autophagic flux, protein abundance, or chronic effects. Finally, a target-only Igf2r RNA
decrease could have produced a count of 1 even with no downstream program; I assigned 0 because
nearby cargo receptors and M6P-pathway genes often failed to clear the focal FDR gate even when
their biology was directionally perturbed.
