# Prediction trace

## Question and resolved ambiguities

The held-out perturbation in this run is `Cask`; it is absent from both supplied training tables, so I treated the task as a transfer problem from non-held-out perturbations in the same Perturb-seq experiment to the focal cell group, `151 TH Prkcd Grin2c Glut`.

I used `n_degs` exactly as defined in the prompt: the number of measured genes in this cell group with `pvals_adj < 0.05`. The training endpoint counts the perturbed gene itself when its own transcript is detected as significantly depleted: for example `Dlg4`, `Nrxn1`, `Nlgn3`, `Caskin1`, `Cacna2d1`, and `Camk2b` are one-DEG signatures in this focal group because their self rows pass FDR while downstream genes do not. Thus a prediction of `1` can mean "target transcript only" rather than a propagated transcriptional state.

## Sources

- Input endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest: `[local file: 030_Cask.csv]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, queried for same-experiment findings about CASK-adjacent perturbations. There were no direct `Cask` findings in this held-out release, but the release contained findings for `Caskin1`, `Dlg4`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Magi2`, `Cacna1a`, `Cacna1d`, `Cacna2d1`, `Shank2`, `Shank3`, and `Tbr1`.
- Distributed Agents runtime profile comparison over the focal DE signatures, used to compare selected analogs by their `logfoldchanges` vectors and top signed tails.
- Literature from PubMed:
  - Hata, Butz, and Sudhof 1996, PMID 8786425, DOI 10.1523/JNEUROSCI.16-08-02488.1996: CASK was identified as a neurexin-binding MAGUK with an N-terminal CaM-kinase-like domain.
  - Hsueh 2006, PMID 16842202, DOI 10.2174/092986706777585040: review of CASK interactions with neurexins, calcium-channel proteins, Mint1, Veli/mLIN-7/MALS, SAP97, Caskin, TBR1, and CINAP.
  - Pan et al. 2020, PMID 33090494, DOI 10.1111/jnc.15215: patient missense mutations can disrupt CASK binding to SAP97, neurexin, CINAP, and TBR1, and neurexin can drive CASK oligomerization.
  - Becker et al. 2020, PMID 32929080, DOI 10.1038/s41398-020-00994-0: CASK-deficient human iPSC-derived neurons showed presynaptic gene down-regulation and smaller inhibitory presynapses.
  - Marco de la Cruz et al. 2024, PMID 38472649, DOI 10.1038/s41593-024-01592-9: neurexin/LAR presynaptic adhesion can recruit liprin-alpha through CASK during human presynapse assembly.

## Computation over the supplied tables

I first checked the endpoint distribution for all 1,674 focal-cell training perturbations. It is sparse: median `n_degs` is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. Therefore, for a synaptic scaffold like `Cask`, the relevant question is mostly whether it is one of the rare broad responders or whether it follows the many self-only or null synaptic profiles.

From the parquet I filtered

- `group_name == "151 TH Prkcd Grin2c Glut"`, and
- `gene_target` in a hand-picked CASK-neighborhood set:
  `Caskin1`, `Dlg4`, `Magi2`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Shank2`, `Shank3`, `Cacna1a`, `Cacna1d`, `Cacna2d1`, `Camk2a`, `Camk2b`, `Camk2g`, `Tbr1`, and the mechanistic counterexample `Grin1`.

The relevant observed DEG counts in the focal group were:

| training perturbation | focal `n_degs` | interpretation for `Cask` |
| --- | ---: | --- |
| `Caskin1` | 1 | Direct CASK-interacting family member; its one DEG was self depletion. |
| `Dlg4` | 1 | Postsynaptic MAGUK scaffold; one self-only DEG. |
| `Magi2` | 0 | PSD MAGUK-like scaffold; no focal response. |
| `Nrxn1`, `Nrxn2`, `Nrxn3` | 1, 0, 0 | CASK neurexin-binding axis; null or self-only in this cell group. |
| `Nlgn3` | 1 | Neurexin ligand; self-only. |
| `Shank2`, `Shank3` | 0, 2 | PSD scaffold layer downstream of Nrxn/Nlgn/Dlg; absent or singleton downstream response. |
| `Cacna1a`, `Cacna1d`, `Cacna2d1` | 0, 0, 1 | Ca-channel-related comparators; absent or self-only. |
| `Camk2a`, `Camk2b`, `Camk2g` | 0, 1, 0 | CaM-kinase signaling comparators; absent or self-only. |
| `Tbr1` | 0 | Nuclear CASK/TBR1 transcription-complex partner; no focal response. |
| `Grin1` | 89 | Positive control for a directly active glutamatergic receptor perturbation; too broad to be used as the main CASK template. |

I also compared the `logfoldchanges` profiles for this set with the Distributed Agents runtime profile tools. Among the 17 selected perturbations, nine had no FDR-significant focal features, seven had only one to nine, and only `Grin1` had at least 50. The comparison did not reveal a broad shared CASK-neighborhood signature hidden below the FDR cutoff: the active members were essentially target-only or singleton profiles, and the runtime's top-tail overlaps were driven by weak nonsignificant ranks rather than a coherent set of shared significant genes.

The same-experiment Distributed Agents corpus findings were consistent with that direct focal-cell calculation:

- `Caskin1`: thalamic and midbrain glutamatergic groups buffered `Caskin1` RNA depletion without downstream transcription; known biochemical neighbors did not phenocopy the only `Caskin1` responder.
- `Dlg4`: globally flat downstream profile despite detectable self depletion; PSD scaffold/adhesion perturbations converged mainly by being transcriptionally flat.
- `Magi2`: no FDR < 0.10 downstream response in any recovered neuronal group; NMDAR, beta-catenin, and mTOR perturbations were measurable but did not converge with `Magi2`.
- `Nrxn1`, `Nrxn2`, `Nrxn3`, and `Nlgn3`: neurexin/neuroligin perturbations were null, self-only, or very cell-type-restricted and did not form a common transcriptomic module.
- `Cacna1a`, `Cacna1d`, and `Cacna2d1`: Ca-channel perturbations were largely transcriptionally buffered in acute postmitotic neurons.
- `Shank2` and `Shank3`: SHANK perturbations were absent or singleton surfaces and did not move the canonical SHANK-Homer-GKAP-NMDA/mGluR panel.
- `Tbr1`: the postnatal response was limited to cortical glutamatergic groups and did not recover the canonical embryonic `Reln`/`Grin2b` laminar-fate program.

## Target-specific rationale: `Cask`

Biologically, `Cask` is a plausible perturbation: it is a multidomain neuronal MAGUK, binds neurexins through its PDZ/SH3/GK region, participates in presynaptic scaffold organization with Mint/Veli and liprin-alpha, and can join a nuclear TBR1/CINAP transcriptional complex. Those facts made `Caskin1`, `Dlg4`/`Magi2`, `Nrxn1-3`/`Nlgn3`, Ca-channel subunits, `Camk2a/b/g`, and `Tbr1` the closest measured training analogs.

The within-dataset evidence points away from a broad CASK-induced transcriptional state in `151 TH Prkcd Grin2c Glut` cells:

- The most direct interactor in the table, `Caskin1`, had `n_degs = 1`; its focal hit was just `Caskin1` itself.
- `Dlg4`, another neuronal MAGUK scaffold with a robustly detected target knockdown, had `n_degs = 1` and did not induce PSD, NMDAR, AMPAR, neurexin, or MAGUK paralog transcripts.
- `Nrxn1`, `Nrxn2`, `Nrxn3`, and `Nlgn3`, the presynaptic adhesion lane through which CASK is often discussed, were `1`, `0`, `0`, and `1` DEGs respectively.
- The calcium-channel and CaMK-related comparators were similarly flat: `Cacna1a = 0`, `Cacna1d = 0`, `Cacna2d1 = 1`, `Camk2a = 0`, `Camk2b = 1`, `Camk2g = 0`.
- `Tbr1 = 0` in this cell group, arguing that an acute P16 CASK perturbation should not be assumed to activate the embryonic TBR1 transcriptional program here.
- `Grin1 = 89` shows that the assay could detect a glutamatergic receptor perturbation in this same group, but the NMDAR pore subunit is not a good scaffold analog: direct receptor loss was a boundary/counterexample, not a phenocopy of `Dlg4`, `Caskin1`, `Magi2`, or neurexin-family perturbations.

Given that pattern, I expect essentially no downstream DEGs. I did keep the count nonzero because `Cask` itself is broadly neuronal and several comparably expressed synaptic genes in this focal group registered only their own CRISPR-induced mRNA depletion. The point prediction is therefore:

```text
Cask: 1 DEG, interpreted as likely self-transcript depletion and no confident downstream target.
```

## Limits and extrapolation

There is no measured `Cask` perturbation profile in the supplied tables and no direct held-out `Cask` finding in the Distributed Agents same-experiment corpus, so this is an extrapolation from adjacent proteins. CASK is multifunctional; neurexin binding, Mint/Veli scaffolding, calcium-channel organization, and the TBR1/CINAP nuclear complex are not interchangeable mechanisms. Human iPSC CASK deficiency can down-regulate presynaptic genes, but those cells model development over a long timescale and differ from sparse P16 AAV-CRISPR in postmitotic mouse neurons. Conversely, the focal endpoint includes target self depletion, and self detection depends on expression, guide position, nonsense-mediated decay, and nucleus counts; if `Cask` mRNA is not significantly depleted in the true focal data, the same biological reasoning would collapse the count from 1 to 0.
