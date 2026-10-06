Done. I created the required files in the run directory:

- [trace.md]([local file: trace.md]) with the `Mapk8`-specific evidence trail:
  - loaded the focal training `n_degs` table and confirmed the held-out manifest only requests `Mapk8`
  - calibrated the sparse endpoint distribution across 1,674 training perturbations
  - checked exact focal counts for JNK/stress-MAPK/AP-1 comparators such as `Mapk9`, `Map2k6`, `Taok1`, `Map3k7`, `Jund`, `Fosl2`, `Nr4a1`, and `Nr4a3`
  - filtered the DE parquet for the focal cell group to inspect adjusted p-values and matched nucleus counts for those comparators
  - used the Distributed Agents same-experiment corpus plus PubMed literature on JNK1/JNK2/JNK3 biology to separate known stimulus/developmental JNK biology from the basal postnatal snRNA-seq endpoint

- [answer.txt]([local file: answer.txt]) with the exact required single fenced TSV block:
  ```tsv
  target_name	predicted_n_degs
  Mapk8	0
  ```

I also validated that `answer.txt` is exactly one `tsv` fenced block, has one `Mapk8` row, preserves the manifest order, and contains a single non-negative integer prediction.