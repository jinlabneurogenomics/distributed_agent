# Ndufs1 DEG-count prediction

## Question interpreted

The held-out manifest for this run contains one perturbation, `Ndufs1`. I treated the required prediction as:

- cell group: `151 TH Prkcd Grin2c Glut`
- endpoint: the count of measured genes with `pvals_adj < 0.05` in the Wilcoxon differential-expression result for the `Ndufs1` perturbation
- output scale: one non-negative integer point estimate

`Ndufs1` was absent from both supplied training inputs, so I did not use any `Ndufs1` DE signature. The only target-specific signal transferred from the parquet is from non-held-out complex I and mitochondrial perturbations.

The main ambiguity I resolved is that the endpoint counts the perturbed target transcript itself if it passes FDR. In this assay, many one-DEG respiratory-chain perturbations are exactly on-target mRNA decreases, so the target RNA is a legitimate part of `n_degs`; I therefore predicted whether `Ndufs1` is a null call or a singleton, not whether it will induce a broad downstream state.

## Sources

- Input DEG parquet: `[local file: training_de_all_cell_groups.parquet]`
- Input focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out target manifest: `[local file: 146_Ndufs1.csv]`
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`
- PubMed literature
- MitoCarta 3.0 mitochondrial protein and pathway annotations, described by Rath et al. 2021, Nucleic Acids Research, DOI: `10.1093/nar/gkaa1011`, PMID: `33174596`

External biological citations used below:

- Fiedorczuk et al. 2016, Nature, DOI: `10.1038/nature19794`, PMID: `27595392`: atomic structure of mammalian mitochondrial complex I, placing the conserved core subunits in the matrix and membrane arms.
- Sazanov 2014, Journal of Bioenergetics and Biomembranes, DOI: `10.1007/s10863-014-9554-z`, PMID: `24943718`: review of complex I electron transfer from NADH to ubiquinone coupled to proton pumping.
- Benit et al. 2001, American Journal of Human Genetics, DOI: `10.1086/320603`, PMID: `11349233`: nuclear `NDUFS1` and `NDUFV1` mutations causing human isolated complex I deficiency.
- Martin et al. 2005, Archives of Neurology, DOI: `10.1001/archneur.62.4.659`, PMID: `15824269`: `NDUFS1` mutation in Leigh syndrome with biochemical complex I deficiency.
- Kruse et al. 2008, Cell Metabolism, DOI: `10.1016/j.cmet.2008.02.004`, PMID: `18396137`: germline mouse `Ndufs4` loss compromises complex I and causes fatal encephalomyopathy.
- Adjobo-Hermans et al. 2020, BBA Bioenergetics, DOI: `10.1016/j.bbabio.2020.148213`, PMID: `32335026`: `Ndufs4` loss destabilizes complex I subunits including `NDUFA12`, with `NDUFAF2`-associated subcomplexes.

## Computation over the supplied data

I first verified that `Ndufs1` occurs only in the held-out manifest and not in the training endpoint CSV. I then used the endpoint CSV to inspect the focal-cell response sizes for every represented `Nduf*`, `Cox*`, `Uqcr*`, `Sdha`, `Timmdc1`, and several mitochondrial-stress comparators.

The full parquet is 7.8 GB, so I inspected row-group metadata and found the focal cell group in row groups 546-580. I then used a predicate scan, with `group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target` in the complex I / respiratory-chain comparator set, and retained `names`, `gene_target`, `scores`, `logfoldchanges`, `pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`. The nontrivial operation was:

```python
scanner = ds.dataset(parquet_path, format="parquet").scanner(
    columns=[
        "names", "gene_target", "scores", "logfoldchanges",
        "pvals_adj", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(complex_i_targets)
    ),
)
df = scanner.to_table().to_pandas()
```

From those rows I computed:

- `sum(pvals_adj < 0.05)` by perturbation as a check against the training-count CSV.
- Significant focal genes for each same-complex perturbation.
- The focal self-logFC and self-adjusted p value where the perturbed gene was itself measured.
- Pearson correlations between focal Wilcoxon `scores` vectors for represented `Nduf*`, `Ndufaf*`, and `Timmdc1` perturbations, to check for a hidden shared complex I state below the FDR threshold.

The focal training distribution as a whole is very sparse: across 1,674 non-held-out perturbations, 72.0% had `n_degs = 0`, 88.5% had `n_degs <= 1`, and the median was `0`. The complex I panel was even more concentrated at 0 or 1 in this cell group.

## Same-complex and pathway evidence

`Ndufs1` encodes the 75 kDa nuclear core subunit of mitochondrial complex I, a matrix-arm Fe-S protein in the NADH-to-ubiquinone electron-transfer chain. MitoCarta 3.0 assigns it to mitochondrial complex I/OXPHOS, and complex I structures place it next to the `NDUFV1` flavin site and the `NDUFS2`/`NDUFS7`/`NDUFS8` Q-module core. Thus the closest represented training perturbations are the core N/Q-module genes `Ndufv1`, `Ndufv2`, `Ndufs2`, `Ndufs7`, and `Ndufs8`; `Ndufs4` is slightly less direct because it is an accessory subunit, but it is a strong disease-model comparator in mouse.

Focal endpoint and expression evidence for direct analogs:

| perturbation | `151 TH...` n_degs | focal expression evidence | interpretation for `Ndufs1` |
| --- | ---: | --- | --- |
| `Ndufs2` | 1 | the only FDR gene was the target itself, `Ndufs2` log2FC `-0.728`, adjusted p `8.26e-12` | closest core Q-module evidence that a complex I catalytic subunit can yield a singleton on-target call but no downstream program |
| `Ndufs8` | 1 | the only FDR gene was `Ndufs8` log2FC `-0.650`, adjusted p `3.06e-08` | same pattern as `Ndufs2`: real target-mRNA depletion without a secondary OXPHOS/ISR response |
| `Ndufs4` | 0 | self row was negative but not significant, log2FC `-0.623`, adjusted p `0.502`; no gene passed FDR | Leigh-model complex I perturbation showing that even a pathogenic complex I gene can be transcriptionally silent under sparse P16 CRISPR |
| `Ndufs7` | 0 | no FDR genes; top adjusted p was `0.534` | core Q-module counterexample to a guaranteed singleton |
| `Ndufv1` | 0 | no FDR genes; self log2FC `-0.292`, adjusted p `1.0` | closest N-module comparator; argues against a broad stress state from weakening the NADH dehydrogenase module |
| `Ndufv2` | 1 | one FDR gene, `Cdc40`, log2FC `0.785`, adjusted p `0.0279`; the self row did not pass | isolated, likely idiosyncratic singleton rather than a complex I response |

Additional complex I subunits and assembly factors in the focal cell group were also 0 or 1 DEG: `Ndufa11` 0, `Ndufa12` 0, `Ndufa6` 1, `Ndufaf2` 0, `Ndufaf4` 0, `Ndufaf5` 0, `Ndufb3` 0, `Ndufb8` 1, `Ndufb10` 1, and `Timmdc1` 0. Where the one-DEG calls were interpretable, they were almost all self-transcript decreases: for example `Ndufb10` itself was down with log2FC `-0.843`, adjusted p `6.79e-19`, and `Ndufb8` itself was down with log2FC `-0.591`, adjusted p `0.00131`.

The focal score-vector correlations among the closest core comparators were effectively zero:

| pair set | observed score-correlation range |
| --- | ---: |
| all pairs among `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2` | `-0.0346` to `0.0443` |

This matters because if acute single-gene complex I disruption were inducing a common nuclear OXPHOS or ATF4/integrated-stress module, these same-complex signatures should have become positively correlated even when only a few genes crossed FDR. They did not.

Broader respiratory-chain comparators were similarly sparse in the focal class: `Cox11` 0, `Cox4i1` 0, `Cox5a` 1, `Cox6a1` 0, `Cox7b` 0, `Cox8a` 0, `Uqcrfs1` 0, `Uqcrc2` 1, `Uqcrb` 0, `Uqcrh` 0, `Uqcrq` 1, and `Sdha` 1. These are not as mechanistically close to `Ndufs1` as the complex I genes, but they reinforce that P16 mosaic disruption of a single nuclear respiratory-chain component usually did not produce many nuclear DEGs in this endpoint.

`Opa1` is the key counterexample rather than a same-complex analog. In the same focal cell group, `Opa1` produced 37 DEGs, including the mitochondrial stress / amino-acid response genes `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, `Aars`, `Sars`, `Herpud1`, `Lars`, and `Nars`. The same scanner found very small correlations between `Opa1` and the `Nduf*`/`Ndufaf*` panel, from `-0.0257` to `0.0913`. So the assay could detect a mitochondrial-stress-like state in `151 TH Prkcd Grin2c Glut`, but represented complex I subunit perturbations mostly stayed below that state.

## Distributed Agents corpus evidence

The Distributed Agents corpus had no direct `Ndufs1` target context in this held-out run, as expected. It did contain a high-confidence, same-experiment claim over the represented nuclear complex I panel: "Represented nuclear-encoded Complex-I subunit and assembly-factor perturbations are broadly buffered at the postnatal neuronal nuclear transcriptome level, failing to produce a shared acute OXPHOS-stress transcriptional module." The claim covered `Ndufa11`, `Ndufa12`, `Ndufa6`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Ndufb10`, `Ndufb7`, `Ndufb8`, `Ndufb9`, `Ndufs2`, `Ndufs4`, `Ndufs8`, `Ndufv1`, `Ndufv2`, and `Timmdc1`.

Corpus `Ndufs2` findings reported that P16 mosaic `Ndufs2` CRISPR produced only three FDR<0.10 downstream genes across all measured neuronal groups despite significant `Ndufs2` self-decreases in six groups; the `Ndufs2` profile did not activate `Asns`, `Chac1`, `Ddit3`, `Shmt2`, `Slc7a5`, aminoacyl-tRNA synthetases, `Herpud1`, `Lonp1`, `Mthfd2`, `mt-Co2`, or `mt-Cytb` while `Opa1` did. Corpus `Ndufv1` findings similarly described 0 FDR<0.10 downstream genes in every recovered neuronal group and absence of the `Opa1`-like mitochondrial ISR.

I also audited corpus common-neighbor candidates from `Ndufs2`, `Ndufs4`, `Ndufs8`, `Ndufv1`, and `Ndufv2`:

| candidate | focal `n_degs` | disposition |
| --- | ---: | --- |
| `Ndufb3` | 0 | keep as a complex I subunit with a near-null focal surface |
| `Ndufb8` | 1 | keep as a complex I subunit with a singleton self-decrease |
| `Ndufa11` | 0 | keep as a complex I subunit with no focal FDR genes |
| `Ndufs7` | 0 | keep as a close core Q-module subunit with no focal FDR genes |
| `Ndufb10` | 1 | keep as a complex I subunit with a singleton self-decrease |
| `Ndufaf5` | 0 | keep as an assembly-factor boundary showing near-null behavior beyond structural subunits |
| `Opa1` | 37 | keep only as a positive mitochondrial-stress counterexample |
| `Npy1r` | 0 | reject as a mechanistically unrelated near-neighbor of sparse null signatures |

## Target-specific prediction for Ndufs1

External biology says `Ndufs1` is not a dispensable or off-pathway target: it is a core complex I Fe-S subunit, and inherited `NDUFS1` defects cause human complex I deficiency. If this were a germline or highly penetrant protein-null experiment, I would expect impaired respiration and potentially severe neuronal phenotypes. The supplied experiment, however, is a sparse postnatal AAV-CRISPR screen with modest average on-target mRNA loss and a nuclear snRNA endpoint at 3-4 weeks, and the training perturbations show that this setup generally buffers nuclear complex I subunit loss at the transcriptional level.

The most appropriate transfer is therefore:

- Do not transfer a broad `Opa1`-like 37-DEG stress program to `Ndufs1`; `Opa1` is detectable in this cell group but the core complex I genes `Ndufs2`, `Ndufs8`, `Ndufs7`, `Ndufv1`, and `Ndufv2` do not correlate with it or induce its ISR genes.
- Bound the downstream expectation near zero because no direct complex I analog had more than one FDR<0.05 DEG in the focal class.
- Allow one DEG because `Ndufs2` and `Ndufs8`, two core subunits closest to `Ndufs1`, each produced exactly one FDR gene and that gene was the depleted target transcript itself.

I predict `Ndufs1` will behave like the singleton on-target subset of the complex I panel: enough target mRNA reduction to call `Ndufs1` itself, but no separate OXPHOS, mitochondrial ISR, mitophagy, or neuronal-identity transcriptional response. Final point prediction: `1`.

## Limits

- The prediction hinges on the unobserved `Ndufs1` guide set and matched perturbed-cell count. The training data show both strong self calls (`Ndufs2`, `Ndufs8`) and zero self calls (`Ndufs4`, `Ndufs7`, `Ndufv1`) among mechanistically valid complex I comparators.
- The parquet measures RNA only. It does not measure DNA indels, NDUFS1 protein, complex I assembly, oxygen consumption, NADH/NAD+ state, or cell loss.
- `Opa1` is a useful positive mitochondrial-stress benchmark in this assay, but it perturbs inner-membrane fusion and cristae structure rather than complex I catalysis, so it is a counterexample to readout failure rather than a phenocopy.
- The broader `Cox*`, `Uqcr*`, and `Sdha` perturbations support a respiratory-chain buffering pattern but are less specific than the `Ndufs*` and `Ndufv*` core subunits.
- A zero prediction would also be plausible if the `Ndufs1` target transcript fails to pass FDR; I chose `1` because the likely effect, if any, is exactly a self-transcript singleton and the closest represented core subunits include strong self-singleton cases.
