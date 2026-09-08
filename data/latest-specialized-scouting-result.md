# Latest specialized/scouting result

Source: Samuel report in HAI session, 2026-09-09.

## Result

The new run is materially better than the earlier HAI-MCP comparison as an exploratory variance signal.

Both Nemotron runs produced usable candidates, even without finished HTML. The merge still used their candidate evidence where available.

```text
110 evidence items from 6 maps -> 53 verified concepts
```

## Consensus split

| Consensus level | Verified | Unverified |
| --- | ---: | ---: |
| >=3 models | 12 | 0 |
| <=2 models | 41 (77%) | 9 |

Interpretation: most verified substance came from one or two models. A consensus-only method would discard the majority of the useful signal.

## Per-model cluster contribution

| Model | Clusters |
| --- | ---: |
| muse-spark-1.3 | 22 |
| nemotron-3-ultra | 22 |
| ling-3.0-flash-fin | 18 |
| mimo-v2.5 | 17 |
| muse-spark-1.2 | 11 |
| nemotron-3.5-lightning | 0 |

## Research implication

This supports the overlap/variance hypothesis:

- HAI-MCP, smaller repo: 55% of substance came from one or two models.
- New larger run: 77% of verified substance came from one or two models.

The larger the project, the less the model views overlap, and the more value the fan-out can add.

This does not yet prove that specialized scouting is superior overall. It does show that consensus is a bad pruning rule for this setting, because low-overlap findings can carry most of the source-grounded substance.
