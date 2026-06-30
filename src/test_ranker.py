import json
from ranker import score_candidate
import json
from ranker import score_candidate

results = []

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= 20:
            break

        candidate = json.loads(line)

        result = score_candidate(candidate)

        results.append(result)
results.sort(
    key=lambda x: x["score"],
    reverse=True
)
print("\nTOP 20 TEST RESULTS\n")

for rank, candidate in enumerate(results, start=1):
    print(
        f"{rank}. "
        f"{candidate['candidate_id']} "
        f"Score={candidate['score']}"
    )

    print(
        f"Reason: {candidate['reasoning']}"
    )

    print("-" * 50)