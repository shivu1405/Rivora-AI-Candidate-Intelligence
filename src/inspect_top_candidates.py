import json
import csv

def inspect_top_candidates(csv_path='output/top100.csv', jsonl_path='data/candidates.jsonl'):
    """
    Reads the top 100 CSV, extracts the top 20 IDs, and retrieves 
    their full profile details from the source JSONL file.
    """
    
    # 1. Get the top 20 Candidate IDs from the CSV
    top_20_ids = []
    try:
        with open(csv_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Rank is 1-indexed, take first 20
                if int(row['rank']) <= 20:
                    top_20_ids.append(row['candidate_id'])
    except FileNotFoundError:
        print(f"Error: {csv_path} not found. Run rank_all_candidates.py first.")
        return

    # 2. Build a map of candidates to search for
    # Using a dictionary for O(1) lookup after one pass through the large file
    found_candidates = {}
    
    print(f"Searching for {len(top_20_ids)} candidates in {jsonl_path}...")
    with open(jsonl_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            cid = data.get("candidate_id")
            if cid in top_20_ids:
                found_candidates[cid] = data
                
    # 3. Print the formatted output for validation
    print("\n" + "="*60)
    print("MANUAL VALIDATION: TOP 20 CANDIDATES")
    print("="*60)
    
    for cid in top_20_ids:
        c = found_candidates.get(cid)
        if not c:
            continue
            
        profile = c.get("profile", {})
        signals = c.get("redrob_signals", {})
        skills = [s.get("name") for s in c.get("skills", [])[:5]] # Top 5 skills
        
        print(f"Candidate ID:   {cid}")
        print(f"Current Title:  {profile.get('current_title')}")
        print(f"Experience:     {profile.get('years_of_experience')} years")
        print(f"Top Skills:     {', '.join(skills)}")
        print(f"GitHub Score:   {signals.get('github_activity_score')}")
        print(f"Response Rate:  {signals.get('recruiter_response_rate'):.0%}")
        print("-" * 60)

if __name__ == "__main__":
    inspect_top_candidates()