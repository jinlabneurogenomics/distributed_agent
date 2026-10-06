Completed the run-local prediction deliverables:

- [trace.md](./trace.md) records the target-specific reasoning for `Nlgn2`, including the focal training analog counts, the self-vs-downstream DEG distinction, same-experiment corpus context for visible synaptic analogs, and PubMed-cited NL2 mechanism priors.
- [answer.txt](./answer.txt) contains the required single fenced `tsv` block:
  `Nlgn2	1`

I also mechanically verified that `answer.txt` has exactly one data row, preserves the requested-target CSV order, contains no duplicate or extra targets, uses a nonnegative integer prediction, and has no prose outside the fenced TSV block.