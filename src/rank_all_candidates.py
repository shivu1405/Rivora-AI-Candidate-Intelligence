import json
import csv
import os
import time
from tqdm import tqdm
from ranker import score_candidate # Assuming ranker.py is in the same directory

def run_ranking(input_file='data/candidates.jsonl', output_dir='output'):
    """
    Reads candidates, calculates scores, and outputs ranked results.
    """
    start_time = time.time()
    ranked_candidates = []

    # 1. Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Count lines for tqdm (optional, but good for progress bars)
    print("Counting candidates...")
    with open(input_file, 'r') as f:
        total_candidates = sum(1 for _ in f)

    # 3. Process candidates line-by-line to maintain low memory usage
    print(f"Processing {total_candidates} candidates...")
    with open(input_file, 'r') as f:
        for line in tqdm(f, total=total_candidates, desc="Scoring"):
            candidate = json.loads(line)
            # Calculate score using the imported logic
            result = score_candidate(candidate)
            ranked_candidates.append(result)

    # 4. Sort candidates by score descending
    ranked_candidates.sort(key=lambda x: x['score'], reverse=True)

    # 5. Print Top 20 to console
    print("\n--- TOP 20 CANDIDATES ---")
    print(f"{'Rank':<6} | {'Candidate ID':<15} | {'Score':<8} | {'Reasoning'}")
    for i, cand in enumerate(ranked_candidates[:20], 1):
        print(f"{i:<6} | {cand['candidate_id']:<15} | {cand['score']:<8} | {cand['reasoning'][:60]}...")

    # 6. Save Top 100 to CSV
    output_path = os.path.join(output_dir, 'top100.csv')
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['candidate_id', 'rank', 'score', 'reasoning'])
        for i, cand in enumerate(ranked_candidates[:100], 1):
            writer.writerow([cand['candidate_id'], i, cand['score'], cand['reasoning']])

    # 7. Final timing
    end_time = time.time()
    print(f"\nProcessing complete. Total time: {end_time - start_time:.2f} seconds.")
    print(f"Top 100 candidates saved to {output_path}")

if __name__ == "__main__":
    run_ranking()