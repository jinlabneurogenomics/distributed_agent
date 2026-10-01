# Top-six Task-1 response-to-zero misses: STRING support

The six largest observed responses assigned a BioAgents count of zero are:

- Naa20: 1,327 observed, 0 predicted
- Ppp2r1a: 1,292 observed, 0 predicted
- Ap2s1: 1,152 observed, 0 predicted
- Kmt2d: 314 observed, 0 predicted
- Naa15: 306 observed, 0 predicted
- Max: 109 observed, 0 predicted

Across the 18 target-by-network comparisons, the primary STRING analysis assigns **6 to A** (no qualifying training partner), **12 to B** (qualifying partners exist, but none occupy the target's observed seven-level DEG-count range), and **0 to C** (at least one response-matched partner).

This is the target-level version of the aggregate physical, functional, and literature result: response-matched partners are associated with lower count error, whereas proximity without response similarity is not sufficient. Because response similarity uses held-out truth, this is a post-hoc characterization and not causal proof of why the model emitted zero.
