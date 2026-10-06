# Q3 Methods

## Eligibility

The manifest at `[local file: n0001.targets.json]` assigned one required perturbation, `Psmb4`. I filtered the full parquet to that target and the 23 allowed `group_name` values, then called a pair eligible when it had at least one row satisfying:

```sql
gene_target = 'Psmb4'
AND group_name IN (<allowed cell groups>)
AND pvals_adj < 0.10
AND lower(names) <> lower(gene_target)
```

This produced 18 eligible target x cell-type pairs. `012 MEA LA CA1 DG Glut` and `017 CA3 CA2-FC DG Glut` had recovered Psmb4 rows but no FDR < 0.10 downstream gene after target-transcript exclusion; `001 L5-6 IT Glut`, `215 MB Dopa`, and `217 P MY Pineal Glut` had no recovered Psmb4 rows. The output therefore emits 18 of 18 eligible pairs.

## Phenotype Characterization

For each eligible pair I counted all downstream FDR < 0.10 genes, separated positive and negative log-fold changes, recorded `n_pert_matched` and `n_ctrl_matched`, and inspected the top significant genes ranked by adjusted p-value. Recurrent upregulated genes included proteasome or proteostasis genes such as `Psme4`, `Psmc6`, `Psmd4`, `Ubc`, `Hsph1`, `Ddit3`, `Hmox1`, `Bax`, and `Sqstm1`; recurrent downregulated genes included synaptic or neuronal markers such as `Syt1`, `Syp`, `Gria2`, `Grin2b`, `Atp1a3`, `Slc17a6`, and `Slc32a1`.

Large mixed pairs were reduced to a single pair-level call by using the coherent upregulated proteasome or integrated-stress arm when it was supported by multiple FDR-significant genes. The summaries explicitly disclose the parallel downregulated synaptic/neuronal module, because the cited target-specific literature supports PSMB4 loss to proteasome dysfunction and recovery/stress transcription more directly than it supports cell-type marker loss.

## Literature Search

Searches used PubMed through the filtered literature gateway. The common target-level queries were `PSMB4 proteasome beta 4 knockdown`, `PSMB4 neuron synapse brain proteasome`, `PSMB4 neuronal apoptosis proteasome spinal cord injury RIP3`, `Nrf1 proteasome recovery proteasome subunit genes`, and proteasome-inhibition CHOP/DDIT3 queries. For sparse or borderline pairs I also searched for `PSMB4` together with the observed genes or module, including `Cacnb3 Kcnj9 Rangap1 Pkm Syt1`, `Sort1 Uchl1 Pkm`, `Erbb4 Pnoc Syt1 cortical GABA`, and `Syt7 proteasome striatal GABA`.

The `PSMB4` knockdown search returned nine PubMed records; the neuronal `PSMB4` searches returned either zero records or the rat spinal-cord-injury necroptosis paper, which was reviewed but not cited because it did not connect Psmb4 loss to the measured modules. The no-literature searches for the sparse 007, 022, 046, and 059 responses returned no target-to-response paper. The Nrf1 search returned the Radhakrishnan et al. proteasome-recovery paper, and the CHOP/DDIT3 search returned multiple proteasome-inhibitor stress papers, of which Teske et al. was cited for a mechanistic CHOP/ISR connection.

## Flag Rules

`Agree` was assigned when a pair contained multiple increased proteasome-recovery or ISR genes. The directional prior was a complete but indirect chain: human PSMB4 loss or siRNA depletion impairs proteasome assembly/activity; mammalian proteasome inhibition induces Nrf1-dependent proteasome-subunit transcription; proteasome inhibition also activates a CHOP/DDIT3 integrated-stress and apoptosis program. Context tags therefore include `species`, `cell_type`, `stage`, `modality`, and `indirect`.

`Inferred` was assigned to `009 L2-3 IT PIR AON ENT Glut` because only a small subset of its 51-gene response, `Psmd4`, `Psme4`, and `H2-K1`, fit the documented proteasome-recovery or type-I-IFN consequences of PSMB4/proteasome loss. The literature did not bridge PSMB4 to the remaining Pcbp1/Bex2/Chn1/Homer1-like mixed response.

`No Literature` was assigned only after pair-specific target/module searches failed. `007 L2-3 IT CTX Glut` was a sparse calcium-channel and metabolic response, `022 L5 ET CTX Glut` contained only `Pkm`, `Sort1`, and `Uchl1`, `046 CTX-CGE GABA` was dominated by `Erbb4`/`Pnoc`/`Syt1` decreases despite one `Psme4` hit, and `059 CNU-LGE LSX GABA` contained only decreased `Syt7`. These searches found no biologically specific PSMB4-to-effect bridge beyond general proteasome biology or shared pathway membership.

## Review Completeness

All 18 eligible pairs were characterized against their FDR-significant downstream genes and reviewed against the target-level and module-level literature. Four pairs were low-confidence `No Literature` calls because the DE signal was sparse or did not resemble the canonical PSMB4/proteasome stress response. No eligible pair was left incompletely reviewed.

Totals: eligible pairs = 18; emitted pairs = 18; incompletely reviewed pairs = 0.
