# Q3 literature-agreement methods

## Eligibility

The manifest was read without truncation from `[local file: n0500.targets.json]` and all primary
phenotype calls were restricted to its 500 assigned targets. The
screen-wide parquet was filtered to exact `gene_target` matches from that
manifest and `pvals_adj < 0.10`; eligibility was then computed after removing
rows where `lower(names) == lower(gene_target)`. This yielded 1604
eligible perturbation x cell-type pairs, and the output emits 1604
rows.

## Phenotype characterization

For every eligible pair, significant downstream genes were sorted by adjusted
p-value with absolute log fold change as a tiebreaker. The evidence row records
the number of downstream FDR hits, the up/down split, the minimum adjusted
p-value, the largest absolute log fold change, the matched perturbed/control
cell counts, and up to eight leading genes from that ordered list. Recurrent
modules were called when the leading significant genes matched a coherent set:
SREBP-2/sterol transcripts (`Dhcr24`, `Insig1`, `Msmo1`, `Cyp51`, `Hmgcr`,
`Hmgcs1`, `Ldlr`, `Fdps`, `Fdft1`, `Lss`, `Mvk`, `Sqle`, or `Acaca`),
canonical Wnt feedback genes (`Axin2`, `Nkd1`, `Serpine2`, `Atrnl1`), unfolded
protein response genes (`Hspa5`, `Hyou1`, `Pdia6`, `Sdf2l1`, `Dnajb9`, `Rpn1`,
`Sec11c`, `Txndc5`), actin-network compensation (`Actg1`, `Flna`), ADAR2-Flnb
editing, or TSC/mTORC1-adjacent lysosomal and sterol outputs.

## Literature search and flagging

I first searched PubMed for the recurring target-module relationships with
queries combining the perturbed target, its mouse/human aliases, and the
central measured module genes. Papers were retained only when the abstract
documented a target-specific relationship to the measured gene or module:
`Srebf2` to sterol-gene transcription, `Apc` to beta-catenin target genes,
`Manf` to ER-stress chaperones, `Adarb1` to `Flnb` RNA editing, `Actb` to
actin-isoform compensation and actin reprogramming, and TSC1/TSC2 loss to
mTORC1/SREBP signaling. For the remaining rows I searched the target against
the leading FDR genes named in the evidence row and screened for direct or
specific partial target-to-response bridges; broad disease associations,
family membership, and generic transcriptional dysregulation were not counted.

Context differences were recorded but did not by themselves downgrade a
directionally interpretable relationship. Relationships were marked `Agree`
when the cited mechanism predicted the sign of the central response, and
`Inferred` when the literature supplied a biologically specific but incomplete
bridge, such as ADARB1-to-Flnb editing without an established Flnb abundance
prediction or TSC loss to mTORC1/SREBP signaling without a complete neuronal
sterol-gene prediction. Rows with no retained bridge were assigned
`No Literature`.

## Multi-module pairs

When a pair contained more than one module, the pair-level flag was assigned
from the most central FDR-supported module that had target-specific literature:
`Srebf2` rows were reduced to the sterol-gene module, `Apc` rows to Wnt
feedback targets, `Manf` rows to the ER-stress chaperone module, `Actb` rows
to actin isoform or FLNA actin-network compensation, and `Tsc1`/`Tsc2`/`Depdc5`
rows to mTORC1-adjacent sterol/lysosomal outputs. Incidental significant
transcripts from the same pair were kept in the evidence record rather than
used to assign a separate row-level flag.

## Difficult or low-confidence pairs

Most eligible pairs were isolated one-gene or few-gene effects with no
published target-specific link to the observed transcript, so they are
reported as `No Literature` after target-plus-gene searches rather than being
merged into a broad pathway claim. `Actb` pairs led by `Flna` and `Adarb1`
pairs led by `Flnb` were deliberately kept at `Inferred`: the searches found
specific bridges to cytoskeletal remodeling or Flnb RNA editing, but not a
directly documented loss-of-function prediction for FLNA/FLNB abundance in
these juvenile brain cell groups. No pair was left incompletely reviewed.

## Totals

- Eligible pairs: 1604
- Emitted pair rows: 1604
- Incompletely reviewed pairs: 0
- Flag counts: {"Agree": 26, "Inferred": 43, "No Literature": 1535}
