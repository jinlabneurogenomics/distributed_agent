Created the requested prediction deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Zkscan3	0
```

I validated that `answer.txt`:

- contains only a single fenced `tsv` block
- has the exact required header
- has exactly one data row
- preserves the requested target order from `the single-target request`
- contains no duplicate targets
- uses a non-negative integer prediction

The prediction is driven by the focal training counts and raw focal DE rows for close `Zkscan` relatives and autophagy/lysosome pathway analogs. `Zkscan1` and `Zkscan16` were both complete focal nulls; visible core autophagy perturbations such as `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, and `Rubcn` were also null or nearly null in `151 TH Prkcd Grin2c Glut`. I treated `Tsc2 = 86` as an mTORC1-derepression counterexample rather than as a transferable analog for `Zkscan3`, because loss of an upstream mTORC1 brake is not the same causal intervention as derepressing a context-dependent autophagy transcription factor.