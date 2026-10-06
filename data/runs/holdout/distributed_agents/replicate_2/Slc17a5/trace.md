# DEG-count prediction trace

## Question and interpretation

The task is to predict the held-out value of `n_degs` for each requested perturbation in `151 TH Prkcd Grin2c Glut` neurons.  Here the manifest contained one target:

| target_name |
| --- |
| Slc17a5 |

I treated the endpoint exactly as defined in the prompt: the number of measured mouse genes with `pvals_adj < 0.05` in the focal cell group, including the perturbed target transcript itself if that row would pass FDR.  I did not treat target-mRNA reduction as an editing-efficiency score; it can contribute one counted DEG, but downstream response breadth has to come from other genes.

## Sources used

Internal same-experiment sources:

* `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* `[local file: training_de_all_cell_groups.parquet]`
* Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`
  * `target_context(Slc17a5)` returned no packaged claims or findings for `Slc17a5`.
  * `target_context(Rab7)`, `target_context(Gaa)`, `target_context(Asah1)`, `target_context(Atp6v0a1)`, `target_context(Lamp2)`, and `target_context(Vps41)` were used to check the curated same-experiment interpretation of lysosomal, HOPS/Rab7, V-ATPase, storage-enzyme, and sphingolipid controls.

External biological sources:

* Huizing and Gahl, 2020, DOI `10.1016/j.bbamem.2020.183336`: lysosomal membrane transporter diseases, including the distinction between transporter defects and hydrolytic enzyme defects.
* Huizing et al., 2021, PMID `33862140`, DOI `10.1016/j.neulet.2021.135896`: `SLC17A5`/sialin defects cause free sialic acid storage disorder by blocking lysosomal export of free sialic acid and lead to neurodevelopmental and hypomyelinating disease on a chronic organismal timescale.

## Computation over the supplied data

I first checked the focal training-count table.  It has 1,674 non-held-out targets; 1,205 of them have `n_degs = 0`, 276 have exactly one DEG, 63 lie between 10 and 99 DEGs, and 43 have at least 100 DEGs.  Thus the focal class is the most responsive class in the atlas but still has a zero-dominated count distribution.

I queried the Parquet only for `group_name = '151 TH Prkcd Grin2c Glut'` and mechanistically selected comparator genes.  The focal cell group has 17,259 measured genes per perturbation and 23,679 matched controls in the rows I inspected.  For the key comparator query I used:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj, scores,
       n_pert_matched, n_ctrl_matched
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
  AND pvals_adj < 0.05
ORDER BY gene_target, pvals_adj;
```

The relevant focal DEG counts and expression-pattern evidence were:

| training perturbation | focal `n_degs` | focal expression evidence | relevance to `Slc17a5` |
| --- | ---: | --- | --- |
| `Gaa` | 1 | The only FDR row was `Gaa` itself, log2FC -0.709, adjusted P `8.97e-16`. | Lysosomal hydrolase whose loss causes a storage disease; appropriate as an acute sparse lysosomal-storage counterexample.  Distributed Agents `Gaa:F001-F005` also reports pan-neuronal absence of non-`Gaa` downstream FDR genes despite self-detection in some classes. |
| `Psap` | 1 | The only FDR row was `Psap` itself, log2FC -1.277, adjusted P `1.70e-28`. | Lysosomal sphingolipid activator/cofactor; a storage-neighbor counterexample showing that a lysosomal lipid-cargo defect did not create a broad secondary RNA program here. |
| `Ppt1` | 1 | The only FDR row was `Ppt1` itself, log2FC -0.536, adjusted P `1.34e-5`. | Lysosomal enzyme and neuronal ceroid lipofuscinosis gene; another self-only lysosomal disease comparator. |
| `Scarb2` | 1 | The only FDR row was `Scarb2` itself, log2FC -0.811, adjusted P `0.00246`. | Lysosomal membrane protein and glucocerebrosidase trafficking receptor; relevant because it is a membrane protein rather than a soluble hydrolase, but it still behaved as a singleton. |
| `Ctsb` | 1 | The only FDR row was `Ctsb` itself, log2FC -1.480, adjusted P `8.54e-43`. | Lysosomal protease; useful as another case where a lysosomal transcript was readily self-detected without a downstream storage-stress module. |
| `Grn` | 1 | The only FDR row was `Grn` itself, log2FC -0.770, adjusted P `5.3e-5`. | Lysosomal progranulin biology; same singleton behavior. |
| `Lamp2` | 0 | No focal FDR<0.05 rows.  The Distributed Agents corpus reports only two corrected downstream hits across the wider screen and absence of lysosome, autophagy, proteasome, UPR/ISR, or redox programs after `Lamp2` loss. | Direct lysosome/autophagy membrane counterexample; this makes a broad `Slc17a5` response less likely. |
| `Asah1` | 0 | No focal FDR<0.05 rows.  Distributed Agents `Asah1:F001-F003` found no robust downstream DE and no convergence with `Psap`, `Scarb2`, `Lamp2`, `Ctsb`, or `Gaa`. | Acid ceramidase deficiency is a lysosomal sphingolipidosis; the null argues against automatically transferring chronic lysosomal storage disease priors to this acute neuronal endpoint. |
| `Atp6v0a1` | 1 | The only FDR row was `Atp6v0a1` itself, log2FC -0.640, adjusted P `4.52e-12`. | A V-ATPase a-subunit is a stronger lysosomal-acidification perturbation than `Slc17a5`; Distributed Agents `Atp6v0a1:F001-F005` found no TFEB/CLEAR, autophagy, ISR/UPR, or proteasome response. |
| `Atp6v1a` | 0 | No focal FDR<0.05 rows. | Same V-ATPase complex; the absence supports the same acidification-axis boundary. |
| `Slc9a7` | 1 | The only FDR row was `Slc9a7` itself, log2FC -0.693, adjusted P `5.0e-5`. | Endomembrane pH/ion-homeostasis transporter; useful as a transporter singleton rather than a Slc17 paralog. |
| `St3gal5` | 1 | The only FDR row was `St3gal5` itself, log2FC -0.788, adjusted P `1.96e-14`. | Ganglioside/sialylation pathway control; biochemically upstream of sialoglycoconjugate turnover but not lysosomal free-sialic-acid export. |
| `Vps41` | 0 | No focal FDR<0.05 rows in this cell class.  Distributed Agents reports weak Rab7-shared lysosomal compensation only outside the focal class. | HOPS/late-endosome fusion is closer to the strong `Rab7` axis than `Slc17a5`, but was still silent in the focal endpoint. |
| `Rab7` | 501 | Broad response: top rows included up-regulation of `Atp6v1b2`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, `Msmo1`, `Lamp2`, `Atp6ap1`, plus many sterol, V-ATPase, lysosomal, ISR/UPR, and synaptic changes. | Positive control proving that this same cell class can report a late-endosomal/lysosomal collapse when the perturbation reaches that level.  It is not the closest quantitative analog for `Slc17a5` because RAB7 controls late endosome maturation, lysosomal positioning, and HOPS recruitment rather than one exported catabolite. |
| `Depdc5` | 13 | Shared a much weaker sterol branch with `Rab7`: `Ldlr`, `Insig1`, `Hmgcs1`, and `Msmo1` were among its few hits. | Lysosome-proximal mTOR/GATOR biology, included as a mechanistic counterexample; it shows that lysosomal nutrient signaling can be visible without implying that each lysosomal transporter is visible. |

No `Slc17` paralog was present in the focal training-count table, so family transfer from `Slc17a6`, `Slc17a7`, `Slc17a8`, or `Slc17a9` was not possible and would in any case have been superficial because those paralogs are vesicular glutamate/nucleotide transporters rather than the lysosomal sialic-acid exporter.

## Target-specific prediction

### `Slc17a5`

`Slc17a5` encodes sialin, the lysosomal membrane exporter for free sialic acid.  Pathogenic loss of human `SLC17A5` causes free sialic acid storage disorder, with free sialic acid accumulating in lysosomes and a clinical spectrum that includes severe infantile disease and Salla disease.  That places it in the lysosomal storage neighborhood, but as a transporter for one acidic sugar rather than a late-endosome fusion factor, V-ATPase subunit, generic autophagy gene, or sterol/mTOR hub.

The strongest positive lysosomal training example, `Rab7`, is therefore a poor point analog: its 501 focal DEGs include a broad V-ATPase/lysosomal hydrolase/sterol and stress state, and Distributed Agents explicitly interprets it as a selective late-endosomal/lysosomal compensation program.  Removing sialin should not acutely phenocopy the full RAB7 trafficking defect in surviving NeuN+ nuclei.

The closer storage and lysosomal-membrane examples were much quieter.  `Gaa`, `Psap`, `Ppt1`, `Scarb2`, `Ctsb`, `Grn`, `Atp6v0a1`, `Slc9a7`, and `St3gal5` each had either zero downstream genes or only the target transcript itself in the focal class; `Lamp2`, `Asah1`, `Atp6v1a`, and `Vps41` were focal zeros.  The curated Distributed Agents corpus makes the same point from the broader expression surfaces: acute sparse loss of multiple lysosomal enzymes, sphingolipid-storage nodes, V-ATPase components, HOPS/retromer relatives, and autophagy genes did not form one recurrent multi-gene storage-stress program in this postnatal neuronal snRNA-seq assay.

My zero/nonzero decision is therefore driven mostly by same-dataset evidence.  External SLC17A5 biology says that the target is real and disease-relevant, but the expected defect is catabolite export and chronic lysosomal free-sialic-acid storage; it is an extrapolation to expect that three to four weeks of mosaic postmitotic editing would generate a nuclear RNA stress response in this thalamic class.  I predict no secondary FDR-significant genes.  The only reason to predict a singleton would be direct self-transcript depletion, as seen for several hydrolases.  I resolved that ambiguity toward zero because direct self-detection is target-specific and `Slc17a5` itself has no same-family calibrator in the training set.

**Predicted `n_degs`: 0**

## Limits and weak points

* `Slc17a5` has no direct Distributed Agents corpus claim and no assayed `Slc17` paralog, so the prediction is transferred from lysosomal-storage and transporter neighbors, not from a true same-family perturbation.
* The represented lysosomal controls are imperfect: many are soluble hydrolases or acidification/trafficking factors, whereas sialin is a lysosomal membrane exporter for free sialic acid.
* A zero prediction is a statement about the FDR<0.05 snRNA endpoint in recovered focal nuclei, not about absence of sialic-acid accumulation, lysosomal morphology, neuronal physiology, developmental glial phenotypes, or edited-cell depletion.
* Sparse AAV CRISPR differs sharply from biallelic human disease and germline mouse models.  Cross-correction, residual protein, long lysosomal protein half-life, survival conditioning, and under-sampling of glia can all hide a biochemical defect from this endpoint.
* The exact `0` versus `1` choice is less certain than the downstream-null prediction, because a self-transcript row can push an otherwise silent perturbation from zero to one DEG.
