# Task-1 category-3 overpredictions and cell-depletion rank

The figure contains the six largest strict category-3 calls (observed zero, BioAgents predicted response) plus Pomp as a marked near-null reference. Pomp is not category 3: it has 4 observed and 600 predicted DEGs.

- Pomp: observed 4, predicted 600, depletion rank 25/1,948
- Thoc2: observed 0, predicted 303, depletion rank 8/1,948
- Pafah1b1: observed 0, predicted 40, depletion rank 5/1,948
- Smc3: observed 0, predicted 31, depletion rank 1,620/1,948
- Hnrnpa1: observed 0, predicted 14, depletion rank 1,057/1,948
- Med12: observed 0, predicted 14, depletion rank 218/1,948
- Taf1: observed 0, predicted 14, depletion rank 3/1,948

## STRING pattern

Across the 18 strict-category-3 target-by-network comparisons, there are 3 A cells, 2 B cells, and 13 C cells. Thus most of these overpredictions have at least one response-matched (zero-response) STRING training neighbor—the opposite of the top underprediction misses, which had no C cells.

## Depletion pattern

Taf1, Pafah1b1, and Thoc2 occupy depletion ranks 3, 5, and 8, respectively. Pomp is rank 25. Med12, Hnrnpa1, and Smc3 are ranks 218, 1,057, and 1,620. Across all 30 strict category-3 targets, 4 are in the top 100 cell-depletion ranks.

This supports an endpoint-mismatch interpretation for a subset: a target can be strongly depleted from the recovered population yet have zero downstream DEGs among surviving cells. It does not show that depletion caused the model prediction, and the weak depletion ranks of several other overpredictions show that depletion is not a universal explanation.
