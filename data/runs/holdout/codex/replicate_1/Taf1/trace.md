# Taf1 DEG-count forecast

## Target and held-out endpoint

- Target: `Taf1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- The target row is absent from the declared count table and the target expression signature is absent from the declared training Parquet.

## Evidence used

**Run-local Taf1 biology bundle**

- `Taf1` is detected in the exact focal non-target population: 19,528 of 23,679 nuclei express it, with 82.47% expressing, mean raw UMI 2.030, mean log1p CP10K 0.733, and pseudobulk CPM 127.23 in `151 TH Prkcd Grin2c Glut`.
- The source card identifies TAF1 as the largest TFIID subunit and a core RNA Pol II promoter-recognition / preinitiation-complex component.
- Functional-stock adjudication was sparse and indeterminate for the P16 to P37-P44 window: a disruptive edit should stop new intact TAF1 synthesis, but it does not directly remove pre-existing TAF1 protein or TFIID assemblies, and no target-specific TAF1/TFIID neuronal persistence measurement was found.
- The mouse loss phenotypes in the bundle were developmental or striatal disease-allele contexts, so I treated them as evidence that TAF1 can matter biologically, not as timing-matched evidence for a large acute thalamic survivor signature.

**Training count table**

The exact FDR<0.05 training counts show that `151 TH Prkcd Grin2c Glut` is sparse overall despite a heavy upper tail:

- 1,674 training perturbations
- 1,205 zeros
- median 0
- 90th percentile 2
- 95th percentile 18

Closest core transcription-initiation analogs were small or flat:

- Native mouse CORUM `TFIID complex` has no available training member besides the held-out `Taf1`.
- Reactome `RNA Polymerase II Transcription Initiation`, `RNA Polymerase II Transcription Pre-Initiation And Promoter Opening`, and `RNA Polymerase II Transcription Initiation And Promoter Clearance` contain only `Taf1` and the trainable `Gtf2h5`; `Gtf2h5` has `n_degs = 0`.
- KEGG `Basal transcription factors` contributes the trainable `Gtf2h5`, `Gtf2i`, and `Gtf2ird1`, with counts `0`, `10`, and `4`.

Broader but still relevant RNA-production or transcription-regulator comparators also argued for a low nonzero count rather than a high-tail response:

- `Taf1b`, a Pol I initiation factor, has `n_degs = 0`.
- Measured Mediator perturbations in or near the shared 151-thalamic module were modest: `Med13 = 11`, `Med13l = 1`, `Med15 = 19`, `Med23 = 13`.
- KAT/chromatin coactivators most relevant to TAF1's acetyltransferase/chromatin annotations were also flat to small: `Crebbp = 8`, `Ep300 = 0`, `Kat6a = 0`, `Kat6b = 0`.

**Same-experiment corpus interpretation**

- The corpus has no `Taf1` Finding, Claim, or explicit comparator record in the selected release.
- The `Gtf2h5` report interpreted its response as a narrow two-gene `191 MB P MY GABA` signal and explicitly as not a broad basal-transcription collapse.
- `Gtf2i` and `Gtf2ird1` reports described compact, non-overlapping thalamic TFII-I-family outputs rather than a shared Williams-region or basal-transcription module.
- `Taf1b` reports described a flat protein-coding mRNA surface despite a core Pol I initiation role and no p53 / UPR / ISR sentinel induction.
- `Med13`, `Med15`, and `Med23` reports supported a real but narrow recurrent thalamic down-module, with `Med13l` and `Cdk8` as boundaries rather than a rule that any transcriptional co-regulator yields that module.

## Synthesis

The direct molecular case pushes above the population median of zero: `Taf1` is expressed in most focal nuclei, has a central non-paralogous TFIID role, and is closer to Pol II initiation than the Pol I/TFII-I/Mediator comparators. The realization prior pushes the other way: the CRISPR edit can leave old TAF1/TFIID stock in place, TFIID turnover is unmeasured, survivor conditioning can erase severely depleted cells, and the closest trainable Pol II-initiation analog `Gtf2h5` is exactly flat in the focal class.

I therefore put `Taf1` in the small-response regime above the many true zeros but below the measured Mediator submodule. A point estimate of **5** matches a sparse signature: slightly larger than `Gtf2ird1` and much larger than `Gtf2h5`/`Taf1b`, but below `Gtf2i`, `Crebbp`, and the `Med13`/`Med15`/`Med23` 151-thalamic module.
