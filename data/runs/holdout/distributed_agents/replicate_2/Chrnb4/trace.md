# Chrnb4 held-out DEG-count prediction

## Question and resolved ambiguities

The manifest `[local file: 040_Chrnb4.csv]` contains one requested perturbation, `Chrnb4`. I interpreted the requested readout as the exact focal-cell endpoint in the training count table: for `151 TH Prkcd Grin2c Glut`, count measured genes whose Wilcoxon BH-adjusted `pvals_adj` is below 0.05 after a sparse postnatal AAV-CRISPR loss-of-function perturbation.

The held-out `Chrnb4` perturbation itself is absent as a `gene_target`, so I did not use a `Chrnb4` DE signature. Rows in which `Chrnb4` is a measured transcript under other perturbations are allowed; they are part of the non-held-out DE table and are only weak evidence about basal detectability of `Chrnb4` RNA in this cell group.

## Sources

- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target CSV: `040_Chrnb4.csv`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.
  - `target_context(Chrnb4)` returned no target-specific findings or claims.
  - `target_context(Chrna3)`, `target_context(Chrnb2)`, and `target_context(Chrna4)` recovered a high-confidence claim, `claim:19d81f58855e7218ecbc`: single-subunit nicotinic acetylcholine receptor perturbations represented in this assay do not produce a shared basal neuronal transcriptional state.
- NCBI PubMed literature:
  - Gahring, Persiyanov, and Rogers 2004, J Comp Neurol, DOI `10.1002/cne.10942`, PMID `14681928`.
  - Wang, Orr-Urtreger, Chapman, Rabinowitz, and Korczyn 2003, Mol Pharmacol, DOI `10.1124/mol.63.3.574`, PMID `12606764`.
  - Frahm et al. 2011, Neuron, DOI `10.1016/j.neuron.2011.04.013`, PMID `21555077`.
  - Scholze, Koth, Orr-Urtreger, and Huck 2012, J Neurochem, DOI `10.1111/j.1471-4159.2012.07714.x`, PMID `22380605`.
  - Wills et al. 2022, Pharmacol Rev, DOI `10.1124/pharmrev.121.000299`, PMID `35017179`.

## Computation over the supplied data

I first read the training endpoint CSV and confirmed it has 1,674 non-held-out perturbations for this cell group. Its response breadth is highly zero-inflated:

| range of `n_degs` | training targets |
| --- | ---: |
| 0 | 1205 |
| 1 to 9 | 363 |
| >9 | 106 |

I then row-filtered the all-cell DE parquet to the focal group and a receptor/cholinergic comparator list:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(analogs)
)
```

That yielded 258,885 DE rows: 15 available perturbations x 17,259 measured genes. For each target I counted `pvals_adj < 0.05`, verified the significant genes against the endpoint CSV, and inspected target-transcript rows where the measured gene equaled the perturbation target. I also ran `profile_compare` on the same focal `logfoldchanges` vectors for these 15 perturbations. The profile comparison classified 12/15 receptor-related perturbations as having no significant features and 3/15 as having only 1 to 9 significant features; no matched nicotinic or muscarinic perturbation had a broad response.

As a basal-detectability check, I queried `names == "Chrnb4"` across all 1,674 non-held-out targets in `151 TH Prkcd Grin2c Glut`. It was present in the measured feature set but had `pvals_adj == 1.0` in every non-held-out contrast, consistent with a sparse transcript in this class and giving no evidence for a robust `Chrnb4`-centered RNA state.

## Target-specific reasoning

### Chrnb4

`Chrnb4` encodes the beta4 nicotinic acetylcholine receptor subunit. External biology makes `Chrna3` and `Chrna5` its closest CNS/autonomic partners: alpha3/beta4-containing receptors are prominent in autonomic ganglia, beta4 deficiency alters ganglionic transmission and autonomic cardiac/intestinal function in mice (Wang et al. 2003), the `CHRNA5-CHRNA3-CHRNB4` cluster is tied to nicotine phenotypes, and alpha3/beta4-containing receptors are highly enriched in the medial habenula-interpeduncular pathway (Scholze et al. 2012; Frahm et al. 2011; Wills et al. 2022). Mouse beta4 protein is reported in the medial habenula, fasciculus retroflexus, interpeduncular nucleus, auditory system including medial geniculate, ventral thalamic nucleus, olfactory-associated structures, piriform cortex, and a subset of hippocampal GAD-positive neurons (Gahring et al. 2004).

The focal assay context points the other way for a DEG-count prediction. `Chrna3`, the closest represented alpha partner for beta4 receptors, produced zero DEGs in `151 TH Prkcd Grin2c Glut` from 148 perturbed nuclei. `Chrnb3`, another neuronal beta subunit and a beta-family counterexample, was also flat from 120 nuclei. The canonical alpha4/beta2 brain receptor pair was barely above the endpoint floor: `Chrnb2` had exactly one hit, its own transcript, from 222 perturbed nuclei, and `Chrna4` had two hits, `Chrna4` itself and `Cyp46a1`, from 293 perturbed nuclei. Other represented neuronal alpha subunits were similarly silent: `Chrna6` 0/133 nuclei and `Chrna7` 0/212 nuclei. The cholinergic comparator `Ache` had one DEG, only the depleted `Ache` self-transcript, from 117 nuclei; `Chrm2` and `Chrm3` were 0. Muscle nAChR subunits were useful negative controls for family membership without focal-cell expression: `Chrna1`, `Chrnb1`, `Chrnd`, `Chrne`, and `Chrng` each had 0 DEGs.

Within the Distributed Agents corpus, the available same-experiment interpretations of `Chrna3`, `Chrnb2`, `Chrna4`, `Chrna6`, `Chrna7`, `Chrnb3`, and `Ache` all argue against a family-wide cholinergic or nAChR transcriptional module. The `Chrna3` finding explicitly noted that the untested closest partners `Chrnb4` and `Chrna5` limit direct inference, but among measurable receptor relatives `Chrna3` was flat and did not converge with the rest of the family. The `Chrnb2` finding was an even cleaner counterexample: target RNA was depleted, yet no downstream FDR program appeared, indicating that loss of a functional nicotinic channel subunit need not become a snRNA-seq state in this basal P37-P44 assay.

This makes a nonzero broad response unlikely for `Chrnb4`. The only plausible nonzero mode would be a self-transcript hit analogous to `Chrnb2`, `Chrna4`, or `Ache`, but the measured `Chrnb4` row is uniformly nonsignificant across the training focal table and the focal nuclei are thalamic/glutamatergic rather than an isolated medial-habenula or autonomic ganglion population. I therefore predict no genes passing BH FDR 0.05.

Predicted `n_degs` for `Chrnb4`: **0**.

## Limits

The strongest missing comparator is `Chrnb4`'s direct alpha3/beta4/alpha5 partner `Chrna5`; it was not in the training count CSV, and `Chrnb4` itself was held out. The focal class may contain thalamic neurons near regions where beta4 protein has been reported, but the screen did not isolate the medial habenula-interpeduncular pathway and did not assay nicotine challenge, membrane receptor trafficking, ligand-gated currents, or behavior. A sparse self-transcript hit of size 1 is hard to exclude in this endpoint, but the within-dataset nAChR evidence is concentrated at 0 and the external biology mainly predicts circuit/channel phenotypes, not a large persistent basal nuclear RNA program.
