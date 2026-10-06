Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1]) with the dataset calibration, Hox-family comparator counts/signatures, Hoxc13-specific biology, citations, and limitations.
- [answer.txt]([local file: answer.txt:1]) with exactly the required single fenced TSV block.

I also validated that `answer.txt`:

- starts with ```tsv and has no prose outside the fence
- has the required `target_name	predicted_n_degs` header
- includes exactly the manifest target, in order
- uses a single non-negative integer prediction

Final point prediction: `Hoxc13	0`.