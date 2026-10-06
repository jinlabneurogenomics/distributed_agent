Created the required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Uqcc2	1`, based on the directly observed focal counts for the represented complex III analogs and `Ttc19`, all of which were essentially flat in `151 TH Prkcd Grin2c Glut` cells: `Cyc1`, `Ttc19`, `Uqcrc2`, and `Uqcrq` had 1 DEG each, while `Uqcrb`, `Uqcrfs1`, and `Uqcrh` had 0. The reasoning trace distinguishes that same-experiment near-null complex III pattern from the external evidence that complete UQCC2 loss can severely disrupt cytochrome-b biogenesis and complex III assembly.

I also mechanically validated `answer.txt`: it is exactly one fenced `tsv` block, has the required header, preserves the requested target order, contains exactly one row, contains no duplicate or extra targets, and has a non-negative integer prediction.