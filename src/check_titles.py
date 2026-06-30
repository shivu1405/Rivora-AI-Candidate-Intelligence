import json

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        if i >= 20:
            break

        candidate = json.loads(line)

        print(
            candidate["candidate_id"],
            "->",
            candidate["profile"]["current_title"]
        )