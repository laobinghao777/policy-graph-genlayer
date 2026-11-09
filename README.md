# PolicyGraph

A reusable GenLayer primitive for identifying conflicting obligations in a committed policy set. Teams can publish individually reasonable rules that become incompatible in an overlapping scenario. This contract produces an auditable **pairwise conflict graph**, with a concrete scenario for every conflict, so reviewers can prioritize the rules involved in the most clashes.

## Design

The creator commits 2–6 rules and their shared applicability scope. The contract derives every unordered pair; the model cannot omit a pair or invent rule IDs. GenLayer consensus requires the same relation for every pair: conflict, compatible or unknown. A conflict requires a concrete witness within the supplied scope. Unknown remains unresolved rather than being counted as compatibility.

The contract attaches exact original rules and computes conflict edges, degrees, unresolved pairs and a stable review-priority ordering deterministically. The assessment binds to a SHA-256 of the immutable scope and rules. Only the creator can analyze; the final result cannot be overwritten. Revised policies must be committed as a new case.

## Meaning of the result

`no_pairwise_conflicts_identified` is deliberately **not a global consistency proof**. Higher-order conflicts involving three or more rules may exist even if all pairs appear compatible. Witnesses are natural-language evidence reviewed through AI consensus, not formal proofs. The primitive does not interpret legal authority, decide rights, execute governance or guarantee correctness. It is a review aid for small explicit policy sets, not a legal decision engine. No production users or rewards are claimed.

## Reproduce

Requires Node.js 20+ and Python 3.12+. Run `npm install --ignore-scripts` and `python tests.py`. Place a dedicated test key in ignored local `pk.txt`. Call `node scripts/run.mjs create_case <scope> <JSON-array-of-rules>`, then `node scripts/run.mjs analyze <case-id>`. Use `get_case` or `list_cases` for reads; `node scripts/run.mjs` prints a read-only snapshot. Writes wait for finalization, guard network identity and record actual settled test-GEN costs. Never upload keys or logs.

Deployment and finalized interaction evidence will be documented after verification. No Portal approval or points are claimed.
