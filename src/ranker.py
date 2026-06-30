def score_candidate(candidate: dict) -> dict:
    """
    Scores a candidate for the Senior AI Engineer role at Redrob,
    returning a recruiter-style professional summary.
    """
    
    score = 0.0
    
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    career_history = candidate.get("career_history", [])
    skills = candidate.get("skills", [])
    
    # --- Scoring Logic (Maintained as requested) ---
    
    # 1. Title Scoring
    title = profile.get("current_title", "").lower()
    strong_ai_titles = ['ai engineer', 'machine learning engineer', 'ml engineer', 'data scientist', 
                        'applied scientist', 'nlp engineer', 'search engineer', 'recommendation engineer']
    related_titles = ['backend engineer', 'software engineer', 'data engineer', 'platform engineer']
    weak_titles = ['accountant', 'hr manager', 'sales executive', 'marketing manager', 
                   'customer support', 'operations manager']
    
    if any(t in title for t in strong_ai_titles):
        score += 25
    elif any(t in title for t in related_titles):
        score += 10
    elif any(t in title for t in weak_titles):
        score -= 15

    # 2. Skill Scoring (Weighted)
    high_value_skills = [
        'embeddings', 'retrieval', 'vector search', 'semantic search', 'ranking systems', 
        'recommendation systems', 'faiss', 'pinecone', 'qdrant', 'weaviate', 'milvus', 'rag', 'mlops', 'nlp', 'llm'
    ]
    proficiency_map = {'expert': 1.5, 'advanced': 1.2, 'intermediate': 1.0, 'beginner': 0.5}
    
    total_skill_score = 0
    detected_skills = []
    for skill in skills:
        s_name = skill.get("name", "").lower()
        if s_name in high_value_skills:
            detected_skills.append(s_name)
            mult = proficiency_map.get(skill.get("proficiency"), 0.5)
            total_skill_score += (10 * mult)
            
    skill_bonus = min(total_skill_score, 50)
    score += skill_bonus

    # 3. Career History Analysis
    career_text = " ".join([job.get("description", "").lower() for job in career_history])
    keywords = ["retrieval", "search", "ranking", "recommendation", "embeddings", "vector", 
                "semantic", "rag", "mlops", "production ml", "model serving", "recommendation engine"]
    matches = [kw for kw in keywords if kw in career_text]
    career_bonus = min(len(matches) * 5, 25)
    score += career_bonus

    # 4. Experience Years
    yoe = profile.get("years_of_experience", 0)
    if 5 <= yoe <= 9: score += 20
    elif 3 <= yoe < 5 or 10 <= yoe <= 12: score += 10

    # 5. GitHub Activity
    gh_score = signals.get("github_activity_score", -1)
    if gh_score >= 70: score += 15
    elif gh_score >= 40: score += 10
    elif gh_score == 0: score += 3

    # 6. Notice Period & Behavioral
    notice = signals.get("notice_period_days", 90)
    if notice <= 30: score += 15
    elif notice <= 60: score += 5
    elif notice >= 120: score -= 10
    
    resp_rate = signals.get("recruiter_response_rate", 0)
    if resp_rate >= 0.7: score += 10
    elif resp_rate >= 0.4: score += 5
    elif resp_rate < 0.2: score -= 10
    
    if signals.get("interview_completion_rate", 0) >= 0.8: score += 10
    if signals.get("open_to_work_flag"): score += 5
    
    # --- Recruiter-Style Reasoning Construction ---
    
    top_skill_str = ", ".join([s.title() for s in detected_skills[:3]])
    yoe_str = f"{yoe:.1f} years"
    gh_status = "High GitHub activity" if gh_score >= 40 else "Active engagement"
    
    reasoning = (
        f"{profile.get('current_title', 'Professional')} with {yoe_str} of experience. "
        f"Demonstrates strong background in {top_skill_str if top_skill_str else 'system architecture'}. "
        f"{gh_status} and high recruiter responsiveness. "
        f"{'Excellent fit for production AI search and ranking systems.' if score > 50 else 'Potential fit for specific technical requirements.'}"
    )

    return {
        "candidate_id": candidate.get("candidate_id"),
        "score": round(score, 2),
        "reasoning": reasoning
    }