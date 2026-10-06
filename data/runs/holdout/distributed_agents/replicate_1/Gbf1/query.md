Created the requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Gbf1	0`. The trace records the focal training-count calibration, the direct Parquet checks for COPI/ER-Golgi analogs, same-experiment corpus evidence for `Copa`, `Copg1`, `Sec23a`, `Rab7`, and `Sec63`, and PubMed-backed GBF1 mechanism citations.

I also mechanically validated `answer.txt`:

- single fenced `tsv` block
- exact header `target_name	predicted_n_degs`
- exactly 1 data row, matching the requested manifest’s 1 row
- exact requested spelling/order: `Gbf1`
- no duplicates or extra targets
- integer non-negative prediction