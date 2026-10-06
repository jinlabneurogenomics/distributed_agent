# Trace

## Question and ambiguity resolution

The requested held-out readout is the integer `n_degs` for each target in
`035_Cep164.csv`: the number of measured genes with `pvals_adj < 0.05` after
acute AAV-CRISPR loss of that target in `151 TH Prkcd Grin2c Glut` neurons.
The manifest contains one target, `Cep164`. I treated the DEG count as the
same endpoint represented in the training CSV, i.e. self-transcript hits are
counted when they pass the same adjusted-P threshold, because the training
`n_degs` values match direct counting of all significant rows in the parquet.

The target itself is completely held out from the supplied DE parquet and from
the focal training-count CSV, so I used neighboring non-held-out perturbations
and known CEP164 biology to transfer a count. I did not infer guide success or
failure from target-transcript depletion, in line with the task warning and the
screen documentation.

## Sources used

- Raw same-experiment DE evidence:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoints:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest:
  `[local file: 035_Cep164.csv]`.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, queried through target reports and the target-neighborhood tools. `Cep164` itself was absent, as expected for a held-out target.
- NCBI PubMed E-utilities literature searches for CEP164, distal appendage, SCLT1, and TTBK2 biology.

Key external mechanism references:

- Tanos et al. 2013, Genes & Development, DOI `10.1101/gad.207043.112`, PMID `23348840`: CEP164, CEP89, CEP83, SCLT1, and FBF1 are distal-appendage proteins; CEP83/SCLT1 help recruit CEP164, and distal appendages are needed for ciliary membrane docking, TTBK2 recruitment, and CP110 removal.
- Cajanek and Nigg 2014, PNAS, DOI `10.1073/pnas.1401777111`, PMID `24982133`: CEP164 binds/recruits TTBK2 to the mother centriole and thereby triggers ciliogenesis, CP110 removal, and IFT recruitment.
- Oda et al. 2014, Genes to Cells, DOI `10.1111/gtc.12191`, PMID `25297623`: the CEP164-binding motif of TTBK2 is required for TTBK2 centriolar localization, CP110 removal, and ciliogenesis.
- Ye et al. 2014, PNAS, DOI `10.1073/pnas.1318737111`, PMID `24469809`: C2CD3 acts upstream of distal appendage assembly and is needed to recruit SCLT1, CEP164, CEP89, FBF1, and TTBK2.
- Siller et al. 2017, PLOS Genetics, DOI `10.1371/journal.pgen.1007128`, PMID `29244804`: conditional mouse Cep164 loss disrupts basal-body docking and multiciliated-cell ciliogenesis, reinforcing that CEP164 is a bona fide ciliary assembly factor.
- Lo et al. 2019, Journal of Cell Biology, DOI `10.1083/jcb.201811142`, PMID `31455668`, and Bernatik et al. 2020, Molecular Biology of the Cell, DOI `10.1091/mbc.E19-06-0334`, PMID `32129703`: CEP164-dependent TTBK2 recruitment leads to phosphorylation of distal-appendage/ciliogenesis substrates such as CEP83 and CEP164.

## Computations over the input data

I first read the manifest and focal training CSV. The manifest had exactly one
row, `Cep164`. The 1,674 focal training counts were strongly zero-inflated:
1,205 targets had 0 DEGs, 363 had 1-9, 63 had 10-89, and 43 had at least 100.

I then queried the training counts for ciliary, transition-zone, basal-body, and
ciliopathy-associated perturbations that are biologically close to CEP164 or are
useful counterexamples. In `151 TH Prkcd Grin2c Glut`, the direct and nearby
comparators were almost all zero:

```text
B9d1      0    Cplane1   0    Cspp1      0    Dync2h1   0
Dync2i1   0    Dzip1     0    Ift43      0    Ift81     0
Ift88     0    Iqcb1     0    Kif3b      0    Kiz       0
Lztfl1    0    Pibf1     0    Pkd1       0    Rpgr      0
Rpgrip1l  0    Sclt1     0    Tbc1d32    0    Armc9     0
Bbs5      0    Cep290    0    Gpr161     0    Ocrl      0
Rab18     0    Ttll5     0
```

The few nonzero entries in the broader ciliary/retinal set were still very weak:
`Ttc8` had 1 DEG and `Arl3` had 1 DEG, both the perturbed target transcript
itself; `Pi4kb` had 1 non-self DEG; and `Rp9` had 4 DEGs. These are not distal
appendage proteins and do not define a CEP164-like downstream state.

For the same 31 comparator genes I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"`, producing 535,029 measured-gene
rows, and recounted `pvals_adj < 0.05`. This reproduced the training CSV counts.
I also inspected the smallest adjusted P values per comparator to check whether
the zeros were cutoff-adjacent. The most direct zeros were not near threshold:
`Sclt1` min q was 1.0 across 122 perturbed versus 23,679 control nuclei;
`Kiz` q was 1.0 across 169 versus 23,679; `Cplane1` q was 1.0 across
179 versus 23,679; `Ift88` q was 1.0 across 143 versus 23,679; `Cep290` min q
was 0.650 across 99 versus 23,679; and `Rpgrip1l` min q was 0.184 across
137 versus 23,679. Thus the zero calls for the best analogs were not a cluster
of just-missed q values at 0.05.

I used the Distributed Agents corpus to avoid treating this as a hand-picked family list.
The corpus reports for `Sclt1`, `Cep290`, `Ift88`, `Rpgrip1l`, `Kiz`, `Cplane1`,
`Dzip1`, and `Tbc1d32` repeatedly found that represented ciliary trafficking,
BBSome, IFT, transition-zone, and Hedgehog-adjacent perturbations were flat,
singleton-only, or orthogonal in the postnatal NeuN+ snRNA readout. The strongest
packaged same-experiment claim was `claim:78305cab7c1c7b98458d`: acute
perturbation of represented ciliary trafficking and ciliary signaling genes in
postnatal NeuN+ neurons is largely buffered at basal nuclear RNA rather than
forming a coherent ciliary transcriptional module. `Sclt1` was especially
important because Tanos et al. place SCLT1 immediately upstream of CEP164
recruitment at the distal appendage, and the Distributed Agents `Sclt1` report explicitly
found no Hedgehog, cilium-gene, UPR, or ISR program after Sclt1 perturbation.

## Target-specific prediction

### Cep164

CEP164 is a mother-centriole distal-appendage protein that recruits TTBK2 and
helps initiate ciliogenesis. In a proliferating-cell or developing-tissue
setting, one would expect loss of CEP164 to interfere with ciliary vesicle
docking, CP110 removal, IFT recruitment, and primary-cilium assembly. That prior
establishes that the perturbation is biologically real, but it does not by
itself predict many nuclear DEGs in postmitotic thalamic glutamatergic neurons
3-4 weeks after sparse P16 editing.

The most relevant training perturbation was `Sclt1`, because SCLT1 is a
distal-appendage component needed for normal CEP164 placement. `Sclt1` had
0 DEGs in `151 TH Prkcd Grin2c Glut`, no q<1 row in the focal group, and the
Distributed Agents corpus specifically reported that it did not induce cilium, Hedgehog,
UPR, or ISR transcriptional programs; its weak all-score neighbor `Kiz` was
also a zero. `Kiz`, another distal-appendage/basal-body comparator present in
the screen, had 0 DEGs in the focal group and no FDR-level response across the
postnatal NeuN+ surface.

Downstream cilium-assembly and ciliary-gate perturbations supported the same
decision. `Ift88`, `Ift81`, and `Ift43` represent IFT machinery downstream of
CEP164/TTBK2 recruitment and all had 0 DEGs in the focal group. The dynein-2
genes `Dync2h1` and `Dync2i1`, the kinesin component `Kif3b`, the CPLANE and
BROMI-axis genes `Cplane1` and `Tbc1d32`, transition-zone/ciliopathy genes
`Cep290` and `Rpgrip1l`, and BBSome-related `Bbs5`, `Lztfl1`, and `Ttc8` were
likewise zeros or singleton-only in this exact endpoint. The singleton
exceptions did not nominate a reusable count for `Cep164`: in the focal group
the `Ttc8` and `Arl3` counts were self-transcript hits, while the non-self
`Pi4kb` and `Rp9` effects were outside the distal-appendage initiation complex
and much weaker than a medium response.

I therefore predict that `Cep164` will be transcriptionally buffered in this
cell group and will not pass the BH FDR 0.05 threshold for any measured gene.
The point prediction is 0 rather than 1 because the best direct analogs were
strict zeros, their smallest adjusted P values were far from 0.05, and the
within-dataset ciliary self-transcript hits were sporadic rather than a stable
property of ciliary knockouts.

## Limits and extrapolation

`Cep83`, `Cep89`, `Fbf1`, `Ttbk2`, and `C2cd3` would have been even closer
distal-appendage or CEP164-TTBK2 comparators but were not present in the
non-held-out focal training table I used. The prediction therefore extrapolates
from `Sclt1`, `Kiz`, and downstream IFT/transition-zone/BBSome genes rather than
from a direct TTBK2 loss signature.

The screen measures basal nuclear RNA from recovered NeuN+ nuclei. It does not
image primary cilia, measure ciliary cargo localization, quantify CEP164 protein
at distal appendages, test evoked Hedgehog or GPCR signaling, sequence indels,
or sample the retina, pituitary, olfactory bulb, hindbrain, embryonic
neuroepithelium, or non-neuronal ciliated cells. A zero-DEG prediction is
therefore not a claim that CEP164 protein loss would be phenotypically neutral;
it only predicts that this particular postnatal thalamic neuronal snRNA-seq
endpoint will have no measured gene below FDR 0.05.
