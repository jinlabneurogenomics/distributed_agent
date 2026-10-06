# Trace

## Local data checks

The run directory only contained the prompt and execution logs, so I treated
the declared Parquet file as the sole local assay table.  Its schema matched
the prompt:

- `names`
- `scores`
- `logfoldchanges`
- `pvals`
- `pvals_adj`
- `group_name`
- `gene_target`
- `control_label`

The file has 745,758,369 DE rows in 712 row groups.  Row-group metadata showed
that `151 TH Prkcd Grin2c Glut` occupies row groups 547-580, and streaming
those row groups gave 2,046 measured perturbation targets in this thalamic
subclass.  I used that target set only as a whitelist and explicitly removed:

- the 50 supplied odd-ranked endpoints
- `Non_target`
- all `Safe_target_*` controls

## Ranking evidence

The odd-ranked list has several mechanistic blocks rather than a single cell
marker program.

- Core proteostasis and organelle-acidification hits are strongest:
  `Atp6v1b2`, `Atp6v1a`, `Psmb4`, and `Pomp`.
- Membrane trafficking and endolysosomal hits recur:
  `Cltc`, `Gbf1`, `Sec31a`, `Stx5a`, `Chmp4b`, `Snf8`, and `Adam10`.
- RNA processing, transcription, and nuclear transport hits recur:
  `Taf1`, `Son`, `Ddx23`, `Polr3b`, `Tnpo3`, `Cnot1`, `Brd4`, `Cdk13`, and
  `Thoc1`.
- A later tier mixes neuronal structural and identity/signaling genes:
  `Kif1a`, `Dmd`, `Dock3`, `Tbcd`, `Adarb1`, `Six6`, `Six3`, `Myt1l`, `Nek1`,
  `Atp8a2`, `Rapgef2`, `Lrp6`, `Gal`, `Nfix`, `Ica1`, `Pten`, `Bbs5`, `Ank3`,
  and `P2ry14`.

I then computed a weighted average DE signature from the 50 known endpoints in
the thalamic slice and scored all non-supplied perturbations by cosine
similarity to that signature.  The highest non-supplied perturbations by this
data-derived score included `Psmc5`, `Psmc1`, `Atp6v0c`, `Hspa5`, `Prpf6`,
`Uba5`, `Tpr`, `U2af2`, `Snrnp70`, `Xpo1`, `Bdp1`, `Copa`, `Dync1h1`,
`Vps54`, `Vps37a`, `Nsf`, and `Ranbp2`.  I used those scores to break ties
inside pathway-level guesses, not as a direct depletion metric.

Independent literature supported the main neighborhoods used to fill the even
ranks:

- V-ATPase subunits and accessory factors control endosomal/lysosomal
  acidification, and V-ATPase dysfunction is linked to developmental
  encephalopathy, epilepsy, and neurodegeneration in the nervous system
  (Falace et al., 2024, PMID:39273013).
- Proteasome and ubiquitin-dependent protein quality control are central to
  neuronal proteostasis and the clearance of damaged or unwanted proteins
  (Rogers et al., 2010, PMID:20202119; Schmidt et al., 2021,
  PMID:33414510).
- `GBF1` activates ARF-family GTPases for COPI vesicle formation and Golgi
  maintenance; pathogenic `GBF1` variants cause axonal neuropathy with Golgi
  fragmentation, supporting the ER/Golgi trafficking block around `Copa`,
  `Sec23a`, `Nsf`, and Vps-family candidates (Mendoza-Ferreira et al., 2020,
  PMID:32937143).
- `PAFAH1B1`/LIS1 and the dynein pathway regulate microtubule- and
  dynein-based nuclear and cargo movement in neurons; the linked Miller-Dieker
  region also implicates `YWHAE`, which is in the measured perturbation set
  (Tanaka et al., 2004, PMID:15173193; Liu et al., 2021, PMID:35053800).
- `UBA5` encodes the E1 enzyme for UFM1 conjugation; biallelic `UBA5`
  variants disrupt ufmylation, alter ER structure, and cause early-onset
  encephalopathy, supporting `Uba5` and `Ufc1` as strong candidates from the
  expression-signature scan (Colin et al., 2016, PMID:27545681).
- SON-mediated splicing controls genes needed for brain development and
  metabolism, and broader hnRNP/splicing-factor dosage changes are linked to
  neurodevelopmental phenotypes; this supports the spliceosome/RNA-processing
  candidates near `Son`, `Ddx23`, and `Thoc1` (Kim et al., 2016,
  PMID:27545680; Niggl et al., 2023, PMID:37541189; Tilliole et al., 2024,
  PMID:39086926).
- `GPX4` is the key lipid-peroxide repair enzyme whose inactivation drives
  ferroptosis, so I kept the oxidative-stress and quality-control candidates
  adjacent to this part of the known list rather than interpreting `Gpx4` as a
  thalamus-specific marker (Yang and Stockwell, 2015, PMID:26653790).

## Limitations

The Parquet table measures differential transcription among recovered nuclei.
It does not contain guide abundance, cell-count depletion scores, replicate
level counts, or a direct estimate of how many perturbed thalamic nuclei were
lost before sequencing.  Therefore the DE signature was useful for identifying
perturbations that phenocopy the supplied endpoints but could not reproduce the
held-out ranking by itself.

I also did not find a permitted PubMed record matching the exact experimental
phrasing or the exact top-hit set, so the citations above are independent
mechanistic support rather than citations to the hidden ground-truth screen.
