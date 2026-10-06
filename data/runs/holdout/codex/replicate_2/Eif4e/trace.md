# Eif4e DEG-count forecast

Target: `Eif4e`

Focal population: `151 TH Prkcd Grin2c Glut`

Point forecast: `1`

## Evidence used

- The declared holdout manifest contains the single target `Eif4e`; `Eif4e` is absent from the focal training-count table, so no target outcome was available.
- The outcome-blind biology bundle places Eif4e in cap-dependent translation initiation as the cap-binding eIF4F subunit. It is measured in the focal non-target nuclei with high reach, 20,346 / 23,679 nuclei expressing and mean log1p CP10K 0.810, so the target transcript is observable in this thalamic class.
- The same bundle adjudicates the functional stock as `likely_substantially_depleted`: a disruptive P16 edit stops new canonical Eif4e production, the operative pool is a renewable dynamic translation factor, and the 21-28 day P16 to P37-P44 interval should greatly exceed available non-neural half-life proxies. It leaves the actual postnatal thalamic-neuron consequence unresolved; systemic half dose can be tolerated and the paralogs `Eif4e2` and `Eif4e1b` are a buffering uncertainty rather than a same-context compensation result.
- The selected same-experiment corpus has no `Eif4e` Findings or Claims, but it does have a cap-initiation claim centered on the represented eIF4F and mTOR-side perturbations. Its strongest local boundary is `Eif4g1`: loss of this core eIF4F scaffold produced no downstream FDR < 0.10 response in any recovered postnatal neuronal class, did not engage the ATF4/amino-acid stress program that was readily detected after `Opa1` and `Elp1`, and had no strong full-universe profile neighbor.
- In the declared `151 TH Prkcd Grin2c Glut` count table, 1,205 / 1,674 training perturbations had `n_degs = 0`; the median was 0 and the 75th percentile was 1. Mechanistic neighbors on the cap-initiation/mTOR-loss side were also at the floor: `Eif2ak4 = 0`, `Eif5a = 0`, `Rptor = 0`, `Eif4g1 = 1`, `Eif4h = 1`, `Eif4a2 = 2`, and `Mtor = 2`.
- Direct Parquet inspection of those focal rows showed that the lone `Eif4g1` call was the `Eif4g1` transcript itself, `Eif4a2` had the self transcript plus one additional gene, and `Eif4h`/`Mtor` each had only one to two isolated features. The broader responses in adjacent biology came from less direct or oppositely signed states: `Eef2 = 9`, `Ddx3x = 8`, and `Tsc2 = 86`, with `Tsc2` representing mTORC1 disinhibition rather than eIF4F component loss.

## Reasoning

The biology card argues that the perturbation should be realized in the assay window and should not be dismissed as unexpressed or as a durable pre-edit stock. It does not, however, provide a reason to expect a large secondary nuclear-RNA program in recovered juvenile thalamic neurons.

The closest measured loss-of-function analog is `Eif4g1`, another core eIF4F component. Its only focal FDR < 0.05 feature is self RNA, and the packaged report layer interprets it as globally flat for downstream transcription despite the assay's ability to detect ATF4-like and mTOR/SREBP-like states in the same screen. `Eif4a2`, `Eif4h`, `Eif2ak4`, `Eif5a`, `Rptor`, and `Mtor` keep the same local picture: simple postnatal cap-initiation or positive mTOR-arm loss usually lands between 0 and 2 focal DEGs, not in the tens or hundreds.

I therefore forecast a near-floor outcome for `Eif4e`. Because `Eif4e` is well measured in the focal population and the closest expressed eIF4F factors often contribute a self-transcript call without a downstream program, I kept the point at one significant measured gene rather than an absolute zero. The number is not meant to imply strong target-mRNA knockdown or broad biological failure; it is a one-DEG forecast for a likely flat survivor nuclear-RNA signature.
