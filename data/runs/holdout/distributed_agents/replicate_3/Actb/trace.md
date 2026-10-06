# Reasoning trace

## Question and resolved ambiguities

The requested readout is the integer number of genes with `pvals_adj < 0.05` in the held-out perturbation signature for `151 TH Prkcd Grin2c Glut`. I used the exact focal cell-group string from the prompt and data, `151 TH Prkcd Grin2c Glut`, and the exact `n_degs` definition from the training CSV: count focal-cell DE rows with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`.

The manifest has a single held-out target:

```tsv
target_name
Actb
```

`Actb` is absent from both supplied training files by construction, so I did not use any measured `Actb` perturbation endpoint. Zero is interpreted as no measured downstream gene passing FDR 0.05, not as no editing, no protein effect, or no morphological phenotype.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene DE results for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact focal-cell DEG counts for the 1,674 training targets.
- `003_Actb.csv`: requested held-out target manifest.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially:
  - `Actg1:F005` and claim `claim:c42462070e20006d1117`, stating that represented actin-network relatives, Rho/WAVE-proximal, myosin, tropomyosin, filamin, and PI3K-AKT comparators were flat or singleton-only and did not phenocopy `Actg1` in this same Perturb-seq corpus.
  - `Specc1l:F003`, anchoring a broader weak-coupling pattern across `Cdc42`, `Cyfip1`, `Cyfip2`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Akt3`, `Rac1`, and `Actg1`.
  - claim `claim:1aeabad1e41e30f971bc`, summarizing the same-corpus buffering of represented Rac/Cdc42-linked actin-cytoskeleton signaling perturbations.
- PubMed literature for outside biological priors:
  - Bunnell et al. 2011, DOI `10.1091/mbc.E11-06-0582`, showing that complete `Actb` loss is embryonic lethal and disrupts primary fibroblast growth, migration, the G-actin pool, and cell-cycle/motility gene expression.
  - Bunnell and Ervasti 2010, DOI `10.1002/cm.20467`, showing that `Actg1` null mice have delayed growth and perinatal lethality but much milder development than `Actb` nulls, consistent with similar but non-identical beta/gamma cytoplasmic actin functions.
  - Perrin et al. 2010, DOI `10.1371/journal.pgen.1001158`, showing overlap and later specialization of beta- and gamma-actin in hair-cell stereocilia.
  - Riviere et al. 2012, DOI `10.1038/ng.1091`, identifying de novo ACTB and ACTG1 missense variants in Baraitser-Winter syndrome.
  - Kim et al. 2013, DOI `10.1523/JNEUROSCI.0035-13.2013`, and Kim et al. 2014, DOI `10.7554/eLife.02839`, showing that Arp2/3 and Cdc42 perturbation can strongly affect dendritic-spine structure and plasticity, phenotypes that need not appear as broad basal nuclear RNA signatures.

## Computation over the supplied data

I first read the focal training-count CSV to calibrate the assay scale. The focal endpoint is extremely zero-heavy:

```text
training targets: 1674
n_degs == 0:     1205
n_degs > 0:       469
median n_degs:      0
75th percentile:    1
95th percentile:   18
maximum:         2677
```

I then used Parquet row-group statistics to read only row groups compatible with `151 TH Prkcd Grin2c Glut` and extracted a manually selected actin/cytoskeleton comparator set. Each comparator had 17,259 measured genes in the focal group. The non-obvious part was avoiding a 616M-row scan:

```python
pf = pyarrow.parquet.ParquetFile(path)
for i in range(pf.num_row_groups):
    stats = pf.metadata.row_group(i).column(group_name_column).statistics
    if stats and stats.min <= "151 TH Prkcd Grin2c Glut" <= stats.max:
        table = pf.read_row_group(i, columns=wanted_columns)
        focal = table.filter(
            pc.and_(
                pc.equal(table["group_name"], "151 TH Prkcd Grin2c Glut"),
                pc.is_in(table["gene_target"], value_set=pa.array(comparators)),
            )
        )
```

For the biologically closest training perturbations:

| training target | focal `n_degs` | strongest focal evidence |
| --- | ---: | --- |
| `Actg1` | 1 | The lone FDR<0.05 gene was `Actg1` itself, log2FC -0.824, adjusted p = `9.85e-16`; no downstream gene reached even FDR 0.10 in the focal slice. |
| `Actn4` | 0 | No focal FDR<0.10 genes. |
| `Add1`, `Add2`, `Add3` | 0, 0, 0 | No focal FDR<0.10 genes for any adducin. |
| `Baiap2` | 0 | No focal FDR<0.10 genes. |
| `Cdc42` | 1 | The lone focal hit was `Cdc42` itself; no downstream gene reached FDR 0.10. |
| `Rac1` | 0 | No focal FDR<0.10 genes. |
| `Cyfip1`, `Cyfip2` | 0, 1 | `Cyfip2` had only its self-transcript as a focal hit; `Cyfip1` had none. |
| `Pak1`, `Pak2`, `Pak3` | 1, 0, 0 | `Pak1` had only its self-transcript as a focal hit; `Pak2/Pak3` had none. |
| `Limk1`, `Cfl2` | 0, 0 | No focal FDR<0.10 genes. |
| `Diaph2`, `Fmn2` | 0, 0 | No focal FDR<0.10 genes. |
| `Mrtfa` | 0 | No focal FDR<0.10 genes. |
| `Myo5a`, `Myo6`, `Myo9a` | 1, 0, 0 | `Myo5a` had only its self-transcript as a focal hit; `Myo6/Myo9a` had none. |
| `Tpm1`, `Tpm3` | 0, 0 | No focal FDR<0.10 genes. |
| `Washc4` | 0 | No focal FDR<0.10 genes. |
| `Specc1l` | 0 | No focal FDR<0.10 genes, consistent with the same-corpus Rho/WAVE/PI3K weak-coupling claim. |
| `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2` | 0, 0, 0, 0 | No focal FDR<0.05 downstream response. `Akt3` itself barely missed the relaxed FDR 0.10 line. |

I also checked structural counterexamples. `Sptan1`, `Tubb4b`, and `Tubb5` were self-transcript-only in this focal group, and `Tuba1a` produced 7 DEGs that were almost entirely a tubulin self/paralog compensation pattern. `Ctnnb1` was the informative counterexample with 383 focal DEGs; I did not transfer this count to `Actb` because beta-catenin has a direct Wnt/nuclear transcriptional role, but it shows that the cell group could mount a broad expression response to a cytoskeleton-adjacent perturbation when the perturbed molecule is wired into transcription.

Finally, I checked whether the measured-gene universe in the focal parquet included `Actb` as a possible self-transcript hit. It did not: there were zero rows with `names == "Actb"` in `151 TH Prkcd Grin2c Glut`. This matters because many one-DEG neighbors are one-DEG only because the targeted transcript itself was counted. A held-out `Actb` signature in this cell group is therefore expected to need a true downstream response, not just a detectable `Actb` row, to make `n_degs` positive.

## Target-specific reasoning

### Actb

The closest in-dataset perturbation is `Actg1`, the other ubiquitous cytoplasmic actin. It is a strong biochemical analog because beta- and gamma-cytoplasmic actin are 99% identical proteins and partly compensate for each other, yet they are not interchangeable developmental alleles: `Actb` knockout is early-embryonic lethal and fibroblasts lacking `Actb` show growth, migration, G-actin, and expression defects, while `Actg1` loss is milder but still affects growth/survival and specialized F-actin maintenance in tissues such as hair cells. Human ACTB/ACTG1 Baraitser-Winter alleles are largely de novo missense developmental actinopathies, which makes them a poor literal model for sparse postnatal frameshift-like CRISPR loss.

The focal expression evidence argues that actin-polymer disruption per se is almost invisible to this readout. `Actg1` produced 1 DEG in the focal cell group, but that gene was `Actg1` itself. The Distributed Agents corpus further reports that across the same screen `Actg1` had only two FDR<0.10 downstream genes across 22 measured cell groups, had no robust data-driven signature neighbor, and was not phenocopied by `Flnb`, `Rac1`, `Cdc42`, `Cyfip1`, `Cyfip2`, `Mrtfa`, or other measured actin regulators. The focal `Cdc42`, `Cyfip2`, `Pak1`, and `Myo5a` singleton calls were also self-transcript calls. Other F-actin crosslinkers and membrane-cortex relatives, including `Actn4`, the adducins, `Sptan1`, `Sptb`, `Dmd`, `Dst`, and `Macf1`, were zero or self/near-threshold only.

The expected upstream actin remodeling pathway is likewise not an expression analog. `Rac1`, `Cdc42`, `Pak1/2/3`, `Limk1`, `Cfl2`, `Cyfip1/2`, `Baiap2`, `Diaph2`, `Fmn2`, `Mrtfa`, the tropomyosins, and `Washc4` all sit on pathways that can regulate Arp2/3, WAVE/WASP, cofilin, formin, or serum-response actin programs. In the same experiment and in this focal group they were 0- or self-only targets. The high-confidence Distributed Agents Rac/Cdc42 claim explicitly bounded these perturbations as transcriptionally buffered in juvenile neuronal snRNA-seq rather than a recurrent shared nuclear mRNA module. This is compatible with the mouse Cdc42 and Arp2/3 literature: the phenotypes can be synaptic/spine structural and plasticity phenotypes, which this single-nucleus expression endpoint is poorly positioned to count.

My point prediction is therefore driven mainly by the within-dataset `Actg1` and Rac/Cdc42/WAVE/PAK/LIMK evidence, with the external literature used only to make sure `Actg1` is the right positive analog and to avoid overinterpreting embryonic or missense actinopathy biology. The likely outcome is no measured downstream gene at FDR 0.05 in `151 TH Prkcd Grin2c Glut`; unlike `Actg1`, even a target-self hit is unavailable because `Actb` was not in the focal measured-gene table.

Prediction: `Actb -> 0`.

## Limits

The main extrapolation is that no direct `Actb` perturbation exists in the supplied data or in the Distributed Agents corpus. `Actg1` is the closest paralog, but `Actb` and `Actg1` have isoform- and nucleotide-dependent functions, and whole-body `Actb` loss is more severe than whole-body `Actg1` loss. The P16 sparse AAV CRISPR assay also measures nuclear RNA 3-4 weeks after perturbation; it cannot see F-actin organization, local translation, spine remodeling, axonal transport, protein abundance, or edited-cell loss. Finally, the direct downstream test is slightly weakened by the absence of `Actb` from the focal measured-gene universe, because the experiment would not count a self-transcript knockdown even if the guides decreased `Actb` RNA.
