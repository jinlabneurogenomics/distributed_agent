# Q7b Depletion Evaluation Tables

Ground-truth relevance is constrained to GT top100.

| Framework | Pred cutoff | Hits in GT top100 | Precision | Recall of GT top100 | Prefix overlap with GT topK |
|---|---:|---:|---:|---:|---:|
| 2000agents | 10 | 4 | 0.400 | 0.040 | 0/10 = 0.000 |
| 2000agents | 20 | 7 | 0.350 | 0.070 | 2/20 = 0.100 |
| 2000agents | 50 | 20 | 0.400 | 0.200 | 15/50 = 0.300 |
| 2000agents | 75 | 25 | 0.333 | 0.250 | 24/75 = 0.320 |
| 2000agents | 100 | 28 | 0.280 | 0.280 | 28/100 = 0.280 |
| biomni | 10 | 5 | 0.500 | 0.050 | 1/10 = 0.100 |
| biomni | 20 | 6 | 0.300 | 0.060 | 4/20 = 0.200 |
| biomni | 50 | 8 | 0.160 | 0.080 | 7/50 = 0.140 |
| biomni | 75 | 12 | 0.160 | 0.120 | 11/75 = 0.147 |
| biomni | 100 | 15 | 0.150 | 0.150 | 15/100 = 0.150 |

| Framework | AP | NDCG@100 |
|---|---:|---:|
| 2000agents | 0.103 | 0.299 |
| biomni | 0.066 | 0.278 |

## Top 30 Rank Mapping

| Framework | Pred rank | Pred gene | GT rank | GT rank | GT gene | Pred rank |
|---|---:|---|---:|---:|---|---:|
| 2000agents | 1 | Xpo1 | NA | 1 | Atp6v1b2 | NA |
| 2000agents | 2 | Srsf1 | 136 | 2 | Ddx39b | NA |
| 2000agents | 3 | Uba5 | NA | 3 | Taf1 | NA |
| 2000agents | 4 | U2af2 | 122 | 4 | Ogt | 38 |
| 2000agents | 5 | Tpr | 60 | 5 | Pafah1b1 | NA |
| 2000agents | 6 | Psmb4 | 11 | 6 | Atp6v1e1 | NA |
| 2000agents | 7 | Hspa9 | 41 | 7 | Cltc | NA |
| 2000agents | 8 | Elp1 | NA | 8 | Thoc2 | 36 |
| 2000agents | 9 | Atp1a3 | NA | 9 | Gbf1 | 66 |
| 2000agents | 10 | Ppp2r1a | 69 | 10 | Hspa5 | 40 |
| 2000agents | 11 | Hnrnpu | NA | 11 | Psmb4 | 6 |
| 2000agents | 12 | Rnpc3 | NA | 12 | Hspa8 | NA |
| 2000agents | 13 | Tnpo3 | 33 | 13 | Eef2 | NA |
| 2000agents | 14 | Ufc1 | NA | 14 | Hmgcr | NA |
| 2000agents | 15 | Psmc5 | 20 | 15 | Atp6v1a | 29 |
| 2000agents | 16 | Cdc40 | NA | 16 | Prpf6 | 24 |
| 2000agents | 17 | Naa15 | NA | 17 | Sec31a | 67 |
| 2000agents | 18 | Brd4 | 65 | 18 | Ranbp2 | NA |
| 2000agents | 19 | Huwe1 | NA | 19 | Kansl1 | NA |
| 2000agents | 20 | Opa1 | NA | 20 | Psmc5 | 15 |
| 2000agents | 21 | Dnm1l | NA | 21 | Son | NA |
| 2000agents | 22 | Psmc1 | 22 | 22 | Psmc1 | 22 |
| 2000agents | 23 | Snrnp70 | NA | 23 | Kif1a | NA |
| 2000agents | 24 | Prpf6 | 16 | 24 | Supt16 | NA |
| 2000agents | 25 | Ddx23 | 51 | 25 | Pomp | 41 |
| 2000agents | 26 | Ap2s1 | NA | 26 | Nr2f2 | NA |
| 2000agents | 27 | Sin3a | NA | 27 | Six6 | NA |
| 2000agents | 28 | Wac | NA | 28 | Dhdds | 74 |
| 2000agents | 29 | Atp6v1a | 15 | 29 | Stx5a | NA |
| 2000agents | 30 | Ndufs2 | NA | 30 | Copa | NA |
| biomni | 1 | Psmb4 | 11 | 1 | Atp6v1b2 | NA |
| biomni | 2 | Cltc | 7 | 2 | Ddx39b | NA |
| biomni | 3 | Polr3b | 37 | 3 | Taf1 | NA |
| biomni | 4 | Sec31a | 17 | 4 | Ogt | NA |
| biomni | 5 | Glmn | NA | 5 | Pafah1b1 | 40 |
| biomni | 6 | Usp9x | 62 | 6 | Atp6v1e1 | NA |
| biomni | 7 | Atp6ap1 | NA | 7 | Cltc | 2 |
| biomni | 8 | Nfe2l1 | NA | 8 | Thoc2 | 64 |
| biomni | 9 | Diaph2 | NA | 9 | Gbf1 | NA |
| biomni | 10 | Gabra2 | NA | 10 | Hspa5 | NA |
| biomni | 11 | Safe_target_53 | NA | 11 | Psmb4 | 1 |
| biomni | 12 | Appl1 | NA | 12 | Hspa8 | NA |
| biomni | 13 | Sec63 | 107 | 13 | Eef2 | 18 |
| biomni | 14 | Ndufb8 | NA | 14 | Hmgcr | NA |
| biomni | 15 | Safe_target_26 | NA | 15 | Atp6v1a | NA |
| biomni | 16 | Gp6 | NA | 16 | Prpf6 | NA |
| biomni | 17 | Safe_target_77 | NA | 17 | Sec31a | 4 |
| biomni | 18 | Eef2 | 13 | 18 | Ranbp2 | NA |
| biomni | 19 | Mpdz | NA | 19 | Kansl1 | NA |
| biomni | 20 | Tbce | 139 | 20 | Psmc5 | NA |
| biomni | 21 | Igsf1 | NA | 21 | Son | 86 |
| biomni | 22 | Pcca | NA | 22 | Psmc1 | NA |
| biomni | 23 | Smad4 | NA | 23 | Kif1a | NA |
| biomni | 24 | Srr | NA | 24 | Supt16 | NA |
| biomni | 25 | Thbd | NA | 25 | Pomp | NA |
| biomni | 26 | Slf2 | NA | 26 | Nr2f2 | NA |
| biomni | 27 | Figla | NA | 27 | Six6 | NA |
| biomni | 28 | Stard7 | NA | 28 | Dhdds | NA |
| biomni | 29 | Safe_target_90 | NA | 29 | Stx5a | NA |
| biomni | 30 | Smad9 | NA | 30 | Copa | NA |
