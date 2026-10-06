Created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1])
- [answer.txt]([local file: answer.txt:1])

The held-out manifest contained only `Tubb4a`, and I predicted:

```tsv
target_name	predicted_n_degs
Tubb4a	1
```

Key basis for the call:

- The focal training endpoint is highly sparse: `1205 / 1674` training perturbations have `0` DEGs, and direct tubulin/cytoskeletal perturbations were almost all weak or null.
- Closest direct focal tubulin analogs:
  - `Tuba1a`: `7` DEGs, with a small multi-tubulin compensation module.
  - `Tuba4a`: `2` DEGs, self plus `Mast1`.
  - `Tubb4b`: `1` DEG, the `Tubb4b` self row.
  - `Tubb5`: `1` DEG, the `Tubb5` self row.
- `Tubb4a` itself is measurable in the focal class: it was significantly up after `Tuba1a` loss.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1` had no held-out `Tubb4a` card, but its same-experiment `Tubb4b`/`Tubb5`/`Tuba4a` reports explicitly bounded the `Tuba1a` response as an isotype-specific exception rather than a generic beta-tubulin or microtubule-stress program.
- External TUBB4A literature supports real tubulin disease biology, but mostly through dominant missense / H-ABC / dystonia mechanisms rather than this sparse postnatal CRISPR-LoF NeuN+ nuclear RNA endpoint.

I also validated [answer.txt]([local file: answer.txt:1]): it contains exactly one `tsv` fenced block, the manifest target appears once in order, and the prediction is a non-negative integer.