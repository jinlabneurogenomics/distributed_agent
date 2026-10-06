# Question and endpoint

I interpreted the task as a scalar prediction for the single requested held-out
target `Ap3b2`: predict how many measured genes would have
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei after acute mosaic CRISPR-Cas9
loss of `Ap3b2`.

The endpoint is directly observed for visible training perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. The held-out `Ap3b2`
signature and DEG count are absent from both supplied inputs, so every
`Ap3b2` value below is a transfer from visible perturbations plus gene-function
priors. I treated the training count CSV as authoritative for visible focal-cell
`n_degs`; I used `training_de_all_cell_groups.parquet` only to inspect the
underlying focal-cell DE patterns and boundary counterexamples.

# Sources used

- Declared input parquet:
  `training differential-expression dataset`.
- Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared requested-target manifest:
  `single-target request for Ap3b2`.
- Run-local measurement registry
  `codex_runtime/pipeline/measurement_registry.json`, which confirmed that the
  parquet contains only differential-expression summaries over recovered nuclei,
  not raw UMI counts, guide-exposure denominators, or pre-assay survival.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used the `Ap3b1` direct
  evidence slice and packaged evidence to check whether the nearest AP-3
  visible perturbation carried a coherent same-experiment AP-3, BLOC, lysosome,
  or synaptic-vesicle signature.
- External literature from PubMed:
  Seong et al. 2004, DOI `10.1091/mbc.e04-10-0892`, PMID `15537701`;
  Newell-Litwa et al. 2009, DOI `10.1091/mbc.e08-05-0456`, PMID `19144828`;
  Evstratova et al. 2014, DOI `10.1038/ncomms6530`, PMID `25410111`; and
  Assoum et al. 2016, DOI `10.1016/j.ajhg.2016.10.009`, PMID `27889060`.

# Quantitative checks

The requested-target CSV contained exactly one target, `Ap3b2`. The focal-cell
training CSV contained 1,674 visible perturbations with a highly zero-inflated
response: median `n_degs = 0`, 75th percentile `= 1`, 95th percentile `= 18`,
and only 469 / 1,674 perturbations had any FDR<0.05 gene in this cell group.
Thus a zero or one-gene prediction is the empirical default for a target whose
nearest visible perturbations are transcriptionally quiet.

I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and counted significant rows among
mechanistically adjacent visible perturbations. The relevant focal-cell
observations were:

| visible target | focal `n_degs` | focal pattern |
| --- | ---: | --- |
| `Ap3b1` | 0 | 85 perturbed nuclei; no gene had `pvals_adj < 0.05`; the smallest adjusted P value in the filtered focal rows was 1.0 |
| `Dtnbp1` | 0 | BLOC-1/Hermansky-Pudlak comparator; no focal FDR<0.05 genes |
| `Slc32a1` | 0 | vesicular GABA transporter and AP-3 cargo context; no focal FDR<0.05 genes |
| `Ap1b1` | 1 | the only focal FDR<0.05 gene was `Ap1b1` itself |
| `Ap1s2` | 0 | related adaptor subunit, no focal FDR<0.05 genes |
| `Ap4s1` | 0 | related adaptor subunit, no focal FDR<0.05 genes |
| `Cplx1`, `Cplx2` | 1, 0 | the `Cplx1` response was self-transcript only; `Cplx2` was null |
| `Syp`, `Syn1`, `Syn2`, `Sv2a`, `Vamp1`, `Stx1b`, `Stxbp1`, `Unc13a`, `Unc13b`, `Unc13c` | 1, 1, 0, 1, 1, 0, 1, 0, 0, 0 | synaptic-vesicle and release perturbations were null or self-only in the same focal group |
| `Becn1`, `Vps41`, `Atp6v1a` | 0, 0, 0 | endolysosomal/autophagy comparators were null in the focal group |
| `Rab7` | 501 | strong counterexample: the same focal assay detects a broad lysosomal/sterol response when late endosome-lysosome trafficking is disrupted |

The internal `Ap3b1` report was concordant with the direct parquet slice:
`Ap3b1` produced 0 FDR<0.10 downstream genes in `151 TH Prkcd Grin2c Glut`,
0 downstream FDR<0.10 genes in all 18 measured `Ap3b1` neuronal groups, no
detectable AP-3 compensation/lysosomal/autophagy/TFEB panel, and no meaningful
score-vector neighbor. The same report noted that `Dtnbp1` and `Slc32a1` were
also flat in the matched neuronal screen. That corpus evidence is an
interpretation of the same experiment, not independent replication.

# Ap3b2 prediction

My causal model was:

`Ap3b2` CRISPR loss -> reduced neuron-specific beta-3B AP-3 adaptor function
on early endosome-derived synaptic-vesicle traffic -> altered synaptic-vesicle
cargo sorting and asynchronous transmitter release -> any propagated stress or
compensation in sparse postnatal thalamic glutamatergic neurons -> recovered
nuclear RNA DE after survivor-conditioned sampling.

External biology supports the first two arrows. `AP3B2` encodes the
neuron-specific beta subunit of the AP-3 complex, and recessive human `AP3B2`
loss causes early-onset epileptic encephalopathy with optic atrophy rather than
the albinism/platelet phenotype characteristic of ubiquitous `AP3B1` deficiency
(Assoum et al. 2016). Mouse genetics showed that beta-3B and beta-3A AP-3
complexes localize differently in neurons and have divergent effects on
synaptic zinc vesicle cargoes (Seong et al. 2004). In synaptic-vesicle
fractions, neuronal `Ap3b2` loss reduced selected cargo proteins whereas
`Ap3b1` or BLOC-1 loss increased AP-3-related cargoes, so `Ap3b1` is not an
obligate same-direction proxy for `Ap3b2` (Newell-Litwa et al. 2009).
`Ap3b2` knockout mice also have a synaptic physiological defect, with reduced
AP-3-dependent asynchronous release during stimulus trains (Evstratova et al.
2014).

Those priors argue that `Ap3b2` perturbation should engage neuronal vesicle
sorting, but they do not imply a large 3-4 week nuclear transcriptional
footprint in the recovered `151 TH Prkcd Grin2c Glut` cells. In the declared
dataset, the nearest AP-3 and BLOC perturbations are null; a measured AP-3
beta isoform, `Ap3b1`, has no focal DE and no hidden AP-3/lysosomal program in
other measured neuronal groups. BLOC-1 loss via `Dtnbp1` is also null. The
larger late-endosome `Rab7` response shows that the focal assay can detect a
lysosomal stress program, but the AP-3B intervention is upstream and more
selective for synaptic-vesicle cargo sorting, so the `Rab7` count is a
counterexample rather than a transferable magnitude. Finally, direct
synaptic-vesicle and release perturbations such as `Syn1`, `Syp`, `Sv2a`,
`Vamp1`, and `Stxbp1` generally registered only loss of their own transcripts,
not a broad downstream response.

I therefore predicted no FDR<0.05 genes for `Ap3b2` in this focal group:

- predicted `n_degs = 0`;
- zero/nonzero call: zero;
- basis: visible AP-3/BLOC and synaptic-vesicle perturbations were almost all
  null or self-only;
- main counterpressure: AP3B2 is the neuronal AP-3 beta subunit and could be
  better expressed than `Ap3b1`, so a one-gene self-transcript hit is plausible;
- reason I did not assign a large value: no visible AP-3/BLOC perturbation
  produced a lysosomal, synaptic, or stress signature in this dataset, and
  AP3B2-associated synaptic-vesicle cargo/physiology phenotypes are not the
  same endpoint as broad single-nucleus RNA DE.

# Limits

The comparison is imperfect because the actual AP-3 delta, mu, sigma, and
beta-3B subunits were held out or absent as visible training perturbations;
`Ap3b1` is the ubiquitous beta-3A isoform and is mechanistically related but
directionally divergent from `Ap3b2` for some neuronal cargoes. The input
parquet has differential-expression summaries only, so I could not inspect
baseline `Ap3b2` expression or raw target-mRNA capture in the focal cells. The
prediction also extrapolates from sparse acute CRISPR loss; published germline
mouse and human loss-of-function phenotypes establish neuronal importance but
not the number of FDR-significant nuclear genes after mosaic AAV editing.
