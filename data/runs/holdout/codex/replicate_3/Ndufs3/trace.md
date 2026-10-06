# Ndufs3 direct forecast

Target from the declared one-row manifest: `Ndufs3` in `151 TH Prkcd Grin2c Glut`.

The selected July same-experiment corpus had no Ndufs3 target report, Finding, explicit comparator, or Claim record, so the target itself contributed only the declared biology bundle. That bundle places NDUFS3 as a core Q-module subunit of assembled respiratory complex I, with broad exact focal-population expression in non-targeting thalamic neurons: 22,000 of 23,679 cells expressed Ndufs3, 92.91%, with mean raw UMI 3.38 and pseudobulk 211.9 cpm. The functional-stock card was the downward timing evidence: a P16 edit stops new NDUFS3 supply but does not directly disable pre-existing complex I, and the closest postnatal neuronal model kept NDUFS3 near control at one month with loss emerging later, so P37-P44 should be at most a leading edge of complex-I stock depletion rather than a fully realized respiratory-chain lesion.

I chose the training comparators from curated complex-I membership rather than from string prefixes alone. The deterministic GO:CC `respiratory chain complex I` set containing Ndufs3 had 20 available training targets in the focal count table after excluding the held-out target and two unavailable members:

`Ndufa10 1`, `Ndufa11 0`, `Ndufa12 0`, `Ndufa6 1`, `Ndufa8 0`, `Ndufa9 0`, `Ndufaf2 0`, `Ndufb10 1`, `Ndufb11 1`, `Ndufb3 0`, `Ndufb7 0`, `Ndufb8 1`, `Ndufb9 1`, `Ndufc2 1`, `Ndufs2 1`, `Ndufs4 0`, `Ndufs7 0`, `Ndufs8 1`, `Ndufv1 0`, `Ndufv2 1`.

That exact focal-class prior is pinned to the origin: 10/20 members had `n_degs = 0`, 10/20 had `n_degs = 1`, and none exceeded 1. The closer NADH-to-ubiquinone/Q- and N-module subunits in the same table were equally sparse: `Ndufs2`, `Ndufs7`, `Ndufs8`, `Ndufv1`, and `Ndufv2` had `1, 0, 1, 0, 1`.

The focal Parquet rows showed why I treated `1` as a minimal/self or singleton count rather than evidence for a downstream module. In `151 TH Prkcd Grin2c Glut`, the significant complex-I/respiratory-chain rows included self-transcript hits for `Ndufs2`, `Ndufs8`, `Ndufa10`, `Ndufa4`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Cox5a`, `Cyc1`, `Sdha`, and `Uqcrc2`; among the queried nuclear OXPHOS targets, the only non-self singletons in this class were `Ndufv2 -> Cdc40` and `Uqcrq -> Gpr180`.

The corpus supports the same interpretation at the whole-screen level. A high-confidence 16-contribution Claim over NDUF/NDUFAF/Timmdc1 reports that represented nuclear complex-I perturbations were broadly buffered and failed to form a shared acute OXPHOS-stress module. Individual `Ndufs2`, `Ndufs4`, `Ndufs8`, `Ndufv1`, and `Ndufv2` Findings were flat or near-flat, and the Opa1 Claim shows that this is not a generic inability of the snRNA/Wilcoxon pipeline to detect mitochondrial stress: Opa1 did activate an ATF4/ISR-like mitochondrial response, while complex-I comparators such as `Ndufs2` and `Ndufv1` did not.

My endpoint expectation for Ndufs3 is therefore zero broad downstream DEGs in this thalamic class. Because the endpoint counts the target transcript itself when it passes FDR, and because Ndufs3 is highly expressed in the exact focal population, I placed the point at the minimal nonzero value rather than at a multi-gene stress response.

Predicted `n_degs`: `1`.
