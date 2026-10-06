Done. I created both required artifacts in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I predicted `Uqcrc1` as a singleton response:

```tsv
target_name	predicted_n_degs
Uqcrc1	1
```

The trace anchors that estimate in the focal training counts for native complex III analogs: `Cyc1:1`, `Uqcrb:0`, `Uqcrc2:1`, `Uqcrfs1:0`, `Uqcrh:0`, `Uqcrq:1`, plus the complex III assembly comparators `Lyrm4:0`, `Nfs1:0`, and `Ttc19:1`. The closest core-complex analog, `Uqcrc2`, had only a self-transcript hit in `151 TH Prkcd Grin2c Glut`, and the Distributed Agents same-experiment corpus supported treating represented complex III components as transcriptionally buffered singleton/null profiles rather than a shared mitochondrial-stress module.

I also verified that [answer.txt]([local file: answer.txt]) contains only a single fenced `tsv` block, the exact header, and exactly one `Uqcrc1` row.