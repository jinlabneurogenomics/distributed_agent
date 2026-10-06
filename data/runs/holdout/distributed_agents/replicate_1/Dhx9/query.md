Created the two requested deliverables:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Dhx9` as a small nonzero response in `151 TH Prkcd Grin2c Glut` cells:

```tsv
target_name	predicted_n_degs
Dhx9	12
```

Validation passed: `answer.txt` contains exactly one `tsv` fenced block, the required `target_name` / `predicted_n_degs` header, exactly the requested target in manifest order, no duplicates, and a non-negative integer prediction.