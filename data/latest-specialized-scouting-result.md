# Latest specialized/scouting result

Source: Samuel report in HAI session, 2026-09-09.

## Result

The new run is encouraging for fan-out scouting and is stronger than the earlier HAI-MCP comparison as an exploratory variance signal. It should not be described as "hypothesis confirmed" yet.

Candidates without finished HTML can still be useful when their source references survive into the merge. That is important because the harness should not require every model to finish the presentation step before its analysis can help the aggregator.

```text
110 evidence items from 6 maps -> 53 verified concepts
```

## Consensus split

| Consensus level | Verified | Unverified |
| --- | ---: | ---: |
| >=3 models | 12 | 0 |
| <=2 models | 41 (77%) | 9 |

Interpretation: most verified clusters came from one or two models. A consensus-only method requiring at least three agreeing models would discard about 77% of the verified clusters in this run.

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

The cautious version is: the larger run shows lower overlap than the smaller HAI-MCP run. It supports the idea that larger projects may reduce overlap between model views, but it does not confirm the general rule because the projects also differ in structure and assignment content.

Two caveats matter:

- 77% of found clusters is not automatically 77% of all important project information.
- "Both Nemotrons were usable" conflicts with `nemotron-3.5-lightning` contributing 0 clusters unless the report distinguishes formal candidate usability from merge-usable source evidence.

Also, in this merge, "verified" means first that the referenced code location exists. It does not by itself prove that the model's architectural interpretation of that code location is semantically correct.

This does not yet prove that specialized scouting is superior overall. It does show that consensus is a bad pruning rule for this setting, because low-overlap findings can carry most of the source-grounded substance. The next decisive step is whether the composer can translate those extra findings into a map that Samuel actually understands better.
