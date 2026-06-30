"""
explore_candidates.py
Redrob India Runs — Data & AI Challenge
Dataset Exploration Script

Usage:
    python explore_candidates.py                        # expects candidates.jsonl in same folder
    python explore_candidates.py --file path/to/file    # custom path
    python explore_candidates.py --sample 5             # show N sample records (default: 1)
"""

import json
import sys
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, date


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def load_jsonl(filepath: str) -> list[dict]:
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  [WARN] Line {i} failed to parse: {e}")
    return records


def separator(title: str = "", width: int = 72):
    if title:
        pad = width - len(title) - 4
        print(f"\n{'─' * 2}  {title}  {'─' * pad}")
    else:
        print("─" * width)


def pct(n, total):
    return f"{n:>6,}  ({100 * n / total:.1f}%)" if total else f"{n:>6,}  (N/A)"


# ─────────────────────────────────────────────
#  SECTION 1 — AVAILABLE FIELDS
# ─────────────────────────────────────────────

def print_fields(records: list[dict]):
    separator("1.  ALL AVAILABLE TOP-LEVEL FIELDS")

    top_keys = set()
    for r in records:
        top_keys.update(r.keys())

    print(f"\n  {'Field':<35} {'Present in N records':>22}  {'Coverage %':>10}")
    print(f"  {'─'*35} {'─'*22}  {'─'*10}")

    for k in sorted(top_keys):
        n = sum(1 for r in records if k in r)
        print(f"  {k:<35} {n:>22,}  {100*n/len(records):>9.1f}%")

    # Nested keys
    separator("  Nested keys inside  'profile'")
    profile_keys = set()
    for r in records:
        profile_keys.update(r.get("profile", {}).keys())
    for k in sorted(profile_keys):
        n = sum(1 for r in records if k in r.get("profile", {}))
        print(f"    profile.{k:<30} {n:>18,}  {100*n/len(records):>9.1f}%")

    separator("  Nested keys inside  'redrob_signals'")
    sig_keys = set()
    for r in records:
        sig_keys.update(r.get("redrob_signals", {}).keys())
    for k in sorted(sig_keys):
        n = sum(1 for r in records if k in r.get("redrob_signals", {}))
        print(f"    redrob_signals.{k:<25} {n:>18,}  {100*n/len(records):>9.1f}%")

    separator("  Array fields (career_history / education / skills / certifications / languages)")
    for array_field in ["career_history", "education", "skills", "certifications", "languages"]:
        lengths = [len(r.get(array_field, [])) for r in records]
        print(f"\n  {array_field}")
        print(f"    min items : {min(lengths)}")
        print(f"    max items : {max(lengths)}")
        print(f"    avg items : {sum(lengths)/len(lengths):.1f}")
        print(f"    empty (0) : {pct(sum(1 for l in lengths if l == 0), len(records))}")


# ─────────────────────────────────────────────
#  SECTION 2 — STRUCTURE OF ONE RECORD
# ─────────────────────────────────────────────

def print_one_record(records: list[dict], n_samples: int = 1):
    separator("2.  STRUCTURE OF ONE CANDIDATE RECORD")
    for idx in range(min(n_samples, len(records))):
        r = records[idx]
        print(f"\n  ── Sample {idx + 1}: {r.get('candidate_id', 'N/A')} ──")

        p = r.get("profile", {})
        print(f"\n  [profile]")
        print(f"    headline    : {p.get('headline', '')[:80]}")
        print(f"    location    : {p.get('location')}  |  country: {p.get('country')}")
        print(f"    current     : {p.get('current_title')} @ {p.get('current_company')}")
        print(f"    company_sz  : {p.get('current_company_size')}")
        print(f"    industry    : {p.get('current_industry')}")
        print(f"    yoe         : {p.get('years_of_experience')} years")
        print(f"    summary     : {str(p.get('summary', ''))[:120]}...")

        print(f"\n  [career_history]  ({len(r.get('career_history', []))} roles)")
        for job in r.get("career_history", [])[:2]:
            current_tag = "← CURRENT" if job.get("is_current") else ""
            print(f"    • {job['title']} @ {job['company']}  "
                  f"({job['start_date']} → {job['end_date'] or 'present'}, "
                  f"{job['duration_months']}mo)  {current_tag}")
            print(f"      {str(job.get('description', ''))[:100]}...")

        print(f"\n  [education]  ({len(r.get('education', []))} entries)")
        for edu in r.get("education", []):
            print(f"    • {edu.get('degree')} in {edu.get('field_of_study')}  "
                  f"@ {edu.get('institution')}  [{edu.get('tier', 'unknown')}]")

        print(f"\n  [skills]  ({len(r.get('skills', []))} skills)")
        for s in r.get("skills", [])[:6]:
            dur = f"  {s.get('duration_months')}mo" if s.get('duration_months') else ""
            print(f"    • {s['name']:<30} {s['proficiency']:<14} {s['endorsements']} endorsements{dur}")
        if len(r.get("skills", [])) > 6:
            print(f"    ... and {len(r['skills']) - 6} more")

        certs = r.get("certifications", [])
        if certs:
            print(f"\n  [certifications]  ({len(certs)})")
            for c in certs[:3]:
                print(f"    • {c['name']}  ({c['issuer']}, {c['year']})")

        sig = r.get("redrob_signals", {})
        print(f"\n  [redrob_signals]")
        print(f"    open_to_work         : {sig.get('open_to_work_flag')}")
        print(f"    last_active          : {sig.get('last_active_date')}")
        print(f"    profile_completeness : {sig.get('profile_completeness_score')}")
        print(f"    recruiter_resp_rate  : {sig.get('recruiter_response_rate')}")
        print(f"    notice_period_days   : {sig.get('notice_period_days')}")
        print(f"    salary_range (LPA)   : {sig.get('expected_salary_range_inr_lpa')}")
        print(f"    github_activity      : {sig.get('github_activity_score')}")
        print(f"    willing_to_relocate  : {sig.get('willing_to_relocate')}")
        print(f"    preferred_work_mode  : {sig.get('preferred_work_mode')}")
        print(f"    skill_assessments    : {sig.get('skill_assessment_scores')}")


# ─────────────────────────────────────────────
#  SECTION 3 — DATA TYPES
# ─────────────────────────────────────────────

def print_data_types(records: list[dict]):
    separator("3.  DATA TYPES (from first non-null value in dataset)")

    schema_map = {
        "candidate_id":                         ("top-level",  "str"),
        "profile.anonymized_name":              ("profile",    "str"),
        "profile.headline":                     ("profile",    "str"),
        "profile.summary":                      ("profile",    "str"),
        "profile.location":                     ("profile",    "str"),
        "profile.country":                      ("profile",    "str"),
        "profile.years_of_experience":          ("profile",    "float"),
        "profile.current_title":                ("profile",    "str"),
        "profile.current_company":              ("profile",    "str"),
        "profile.current_company_size":         ("profile",    "str (enum)"),
        "profile.current_industry":             ("profile",    "str"),
        "career_history[*].company":            ("array item", "str"),
        "career_history[*].title":              ("array item", "str"),
        "career_history[*].start_date":         ("array item", "str (YYYY-MM-DD)"),
        "career_history[*].end_date":           ("array item", "str | null"),
        "career_history[*].duration_months":    ("array item", "int"),
        "career_history[*].is_current":         ("array item", "bool"),
        "career_history[*].industry":           ("array item", "str"),
        "career_history[*].company_size":       ("array item", "str (enum)"),
        "career_history[*].description":        ("array item", "str"),
        "education[*].institution":             ("array item", "str"),
        "education[*].degree":                  ("array item", "str"),
        "education[*].field_of_study":          ("array item", "str"),
        "education[*].start_year":              ("array item", "int"),
        "education[*].end_year":                ("array item", "int"),
        "education[*].grade":                   ("array item", "str | null"),
        "education[*].tier":                    ("array item", "str (enum)"),
        "skills[*].name":                       ("array item", "str"),
        "skills[*].proficiency":                ("array item", "str (enum)"),
        "skills[*].endorsements":               ("array item", "int"),
        "skills[*].duration_months":            ("array item", "int"),
        "certifications[*].name":               ("array item", "str"),
        "certifications[*].issuer":             ("array item", "str"),
        "certifications[*].year":               ("array item", "int"),
        "languages[*].language":                ("array item", "str"),
        "languages[*].proficiency":             ("array item", "str (enum)"),
        "redrob_signals.profile_completeness_score":  ("signals", "float 0–100"),
        "redrob_signals.signup_date":                 ("signals", "str (YYYY-MM-DD)"),
        "redrob_signals.last_active_date":            ("signals", "str (YYYY-MM-DD)"),
        "redrob_signals.open_to_work_flag":           ("signals", "bool"),
        "redrob_signals.profile_views_received_30d":  ("signals", "int"),
        "redrob_signals.applications_submitted_30d":  ("signals", "int"),
        "redrob_signals.recruiter_response_rate":     ("signals", "float 0–1"),
        "redrob_signals.avg_response_time_hours":     ("signals", "float"),
        "redrob_signals.skill_assessment_scores":     ("signals", "dict[str, float 0–100]"),
        "redrob_signals.connection_count":            ("signals", "int"),
        "redrob_signals.endorsements_received":       ("signals", "int"),
        "redrob_signals.notice_period_days":          ("signals", "int 0–180"),
        "redrob_signals.expected_salary_range_inr_lpa": ("signals", "dict {min, max} float"),
        "redrob_signals.preferred_work_mode":         ("signals", "str (enum)"),
        "redrob_signals.willing_to_relocate":         ("signals", "bool"),
        "redrob_signals.github_activity_score":       ("signals", "float  -1 = no GitHub"),
        "redrob_signals.search_appearance_30d":       ("signals", "int"),
        "redrob_signals.saved_by_recruiters_30d":     ("signals", "int"),
        "redrob_signals.interview_completion_rate":   ("signals", "float 0–1"),
        "redrob_signals.offer_acceptance_rate":       ("signals", "float  -1 = no history"),
        "redrob_signals.verified_email":              ("signals", "bool"),
        "redrob_signals.verified_phone":              ("signals", "bool"),
        "redrob_signals.linkedin_connected":          ("signals", "bool"),
    }

    print(f"\n  {'Field':<50} {'Section':<12} {'Type / Notes'}")
    print(f"  {'─'*50} {'─'*12} {'─'*24}")
    for field, (section, dtype) in schema_map.items():
        print(f"  {field:<50} {section:<12} {dtype}")

    # Enum values
    print("\n  Enum values observed in data:\n")
    enums = {
        "current_company_size / career/company_size":
            ["1-10","11-50","51-200","201-500","501-1000","1001-5000","5001-10000","10001+"],
        "skills[*].proficiency":
            ["beginner","intermediate","advanced","expert"],
        "education[*].tier":
            ["tier_1","tier_2","tier_3","tier_4","unknown"],
        "languages[*].proficiency":
            ["basic","conversational","professional","native"],
        "preferred_work_mode":
            ["remote","hybrid","onsite","flexible"],
        "offer_acceptance_rate sentinel":
            ["-1  →  no offer history"],
        "github_activity_score sentinel":
            ["-1  →  no GitHub linked"],
    }
    for field, vals in enums.items():
        print(f"    {field}:")
        print(f"      {', '.join(vals)}\n")


# ─────────────────────────────────────────────
#  SECTION 4 — MISSING VALUE AUDIT
# ─────────────────────────────────────────────

def count_missing(records: list[dict]):
    separator("4.  MISSING VALUES  (null / absent / empty)")
    N = len(records)

    def check(values, label):
        null_count   = sum(1 for v in values if v is None)
        absent_count = sum(1 for v in values if v is None)  # already None from .get default
        empty_count  = sum(1 for v in values if v == "" or v == [] or v == {})
        total_bad    = null_count + empty_count
        print(f"  {label:<55} null/absent: {pct(null_count, N)}   empty: {pct(empty_count, N)}")

    # profile fields
    print("\n  [profile]")
    for k in ["anonymized_name","headline","summary","location","country",
              "years_of_experience","current_title","current_company",
              "current_company_size","current_industry"]:
        check([r.get("profile", {}).get(k) for r in records], f"  profile.{k}")

    # career history
    print("\n  [career_history]")
    end_dates = [job.get("end_date")
                 for r in records for job in r.get("career_history", [])]
    grades    = [edu.get("grade")
                 for r in records for edu in r.get("education", [])]
    print(f"  career_history.end_date  (null = current role):  "
          f"  null: {sum(1 for v in end_dates if v is None):,} / {len(end_dates):,}  "
          f"({100*sum(1 for v in end_dates if v is None)/max(len(end_dates),1):.1f}%)")

    # education
    print("\n  [education]")
    print(f"  education.grade (optional, null expected):  "
          f"  null: {sum(1 for v in grades if v is None):,} / {len(grades):,}  "
          f"({100*sum(1 for v in grades if v is None)/max(len(grades),1):.1f}%)")
    tiers = [edu.get("tier") for r in records for edu in r.get("education", [])]
    unknown_tiers = sum(1 for t in tiers if t == "unknown" or t is None)
    print(f"  education.tier = 'unknown' or null:  "
          f"  {unknown_tiers:,} / {len(tiers):,}  "
          f"({100*unknown_tiers/max(len(tiers),1):.1f}%)")

    # redrob_signals
    print("\n  [redrob_signals]  — sentinel values that mean 'no data'")
    github_scores = [r.get("redrob_signals", {}).get("github_activity_score") for r in records]
    offer_rates   = [r.get("redrob_signals", {}).get("offer_acceptance_rate") for r in records]
    skill_assess  = [r.get("redrob_signals", {}).get("skill_assessment_scores", {}) for r in records]

    no_github = sum(1 for v in github_scores if v == -1 or v is None)
    no_offer  = sum(1 for v in offer_rates   if v == -1 or v is None)
    no_assess = sum(1 for d in skill_assess  if d == {})
    print(f"  github_activity_score = -1  (no GitHub):   {pct(no_github, N)}")
    print(f"  offer_acceptance_rate = -1  (no history):  {pct(no_offer,  N)}")
    print(f"  skill_assessment_scores = {{}}  (none taken): {pct(no_assess, N)}")

    # optional top-level arrays
    print("\n  [optional top-level arrays]")
    for field in ["certifications", "languages"]:
        empty = sum(1 for r in records if not r.get(field))
        print(f"  {field} absent or empty:  {pct(empty, N)}")


# ─────────────────────────────────────────────
#  SECTION 5 — SUMMARY REPORT
# ─────────────────────────────────────────────

def summary_report(records: list[dict]):
    separator("5.  SUMMARY REPORT")
    N = len(records)
    print(f"\n  Total candidates loaded       : {N:,}")

    # ── YoE distribution
    yoe_vals = [r["profile"]["years_of_experience"]
                for r in records if "years_of_experience" in r.get("profile", {})]
    if yoe_vals:
        buckets = Counter()
        for y in yoe_vals:
            if y < 2:    buckets["0–2 yrs"] += 1
            elif y < 5:  buckets["2–5 yrs"] += 1
            elif y < 8:  buckets["5–8 yrs"] += 1
            elif y < 12: buckets["8–12 yrs"] += 1
            else:        buckets["12+ yrs"]  += 1
        print(f"\n  Years-of-Experience distribution:")
        for label in ["0–2 yrs","2–5 yrs","5–8 yrs","8–12 yrs","12+ yrs"]:
            bar = "█" * (buckets[label] * 30 // max(buckets.values(), default=1))
            print(f"    {label:<10} {bar:<30} {pct(buckets[label], N)}")
        print(f"\n    min={min(yoe_vals):.1f}  max={max(yoe_vals):.1f}  "
              f"mean={sum(yoe_vals)/len(yoe_vals):.1f}")

    # ── Open-to-work
    otw = sum(1 for r in records if r.get("redrob_signals", {}).get("open_to_work_flag"))
    print(f"\n  Open-to-work = True           : {pct(otw, N)}")

    # ── Willing to relocate
    reloc = sum(1 for r in records if r.get("redrob_signals", {}).get("willing_to_relocate"))
    print(f"  Willing to relocate = True    : {pct(reloc, N)}")

    # ── Preferred work mode
    modes = Counter(r.get("redrob_signals", {}).get("preferred_work_mode") for r in records)
    print(f"\n  Preferred work mode breakdown:")
    for mode, cnt in modes.most_common():
        print(f"    {str(mode):<12} {pct(cnt, N)}")

    # ── Notice period
    notices = [r["redrob_signals"]["notice_period_days"]
               for r in records
               if "notice_period_days" in r.get("redrob_signals", {})]
    if notices:
        sub30 = sum(1 for v in notices if v <= 30)
        print(f"\n  Notice period ≤ 30 days       : {pct(sub30, N)}")
        print(f"  Notice period mean            : {sum(notices)/len(notices):.1f} days")

    # ── Activity (staleness risk)
    today = date.today()
    inactive_90  = 0
    inactive_180 = 0
    for r in records:
        last = r.get("redrob_signals", {}).get("last_active_date")
        if last:
            try:
                delta = (today - date.fromisoformat(last)).days
                if delta > 90:  inactive_90  += 1
                if delta > 180: inactive_180 += 1
            except ValueError:
                pass
    print(f"\n  Last active > 90 days ago     : {pct(inactive_90,  N)}")
    print(f"  Last active > 180 days ago    : {pct(inactive_180, N)}")

    # ── Recruiter response rate
    rrr = [r["redrob_signals"]["recruiter_response_rate"]
           for r in records
           if "recruiter_response_rate" in r.get("redrob_signals", {})]
    if rrr:
        low = sum(1 for v in rrr if v < 0.2)
        print(f"\n  Recruiter response rate < 20% : {pct(low, N)}")
        print(f"  Avg recruiter response rate   : {sum(rrr)/len(rrr):.2f}")

    # ── GitHub signal
    gh = [r["redrob_signals"]["github_activity_score"]
          for r in records
          if "github_activity_score" in r.get("redrob_signals", {})]
    linked   = sum(1 for v in gh if v >= 0)
    active   = sum(1 for v in gh if v >= 50)
    print(f"\n  GitHub linked (score ≥ 0)     : {pct(linked, N)}")
    print(f"  GitHub active (score ≥ 50)    : {pct(active, N)}")

    # ── Education tiers
    tier_counter = Counter()
    for r in records:
        for edu in r.get("education", []):
            tier_counter[edu.get("tier", "unknown")] += 1
    print(f"\n  Education tier distribution (across all degree entries):")
    for tier in ["tier_1","tier_2","tier_3","tier_4","unknown"]:
        print(f"    {tier:<10} {tier_counter[tier]:,}")

    # ── Salary ranges
    salaries_min = [r["redrob_signals"]["expected_salary_range_inr_lpa"]["min"]
                    for r in records
                    if r.get("redrob_signals", {}).get("expected_salary_range_inr_lpa")]
    salaries_max = [r["redrob_signals"]["expected_salary_range_inr_lpa"]["max"]
                    for r in records
                    if r.get("redrob_signals", {}).get("expected_salary_range_inr_lpa")]
    if salaries_min:
        print(f"\n  Expected salary (INR LPA):")
        print(f"    min of mins  : {min(salaries_min):.1f}")
        print(f"    max of maxes : {max(salaries_max):.1f}")
        print(f"    avg midpoint : {sum((a+b)/2 for a,b in zip(salaries_min, salaries_max))/len(salaries_min):.1f}")

    # ── Profile completeness
    completeness = [r["redrob_signals"]["profile_completeness_score"]
                    for r in records
                    if "profile_completeness_score" in r.get("redrob_signals", {})]
    if completeness:
        low_comp = sum(1 for v in completeness if v < 60)
        print(f"\n  Profile completeness < 60     : {pct(low_comp, N)}")
        print(f"  Avg profile completeness      : {sum(completeness)/len(completeness):.1f}")

    # ── Top skills
    skill_names = Counter()
    for r in records:
        for s in r.get("skills", []):
            skill_names[s.get("name", "")] += 1
    print(f"\n  Top 20 most common skill names:")
    for skill, cnt in skill_names.most_common(20):
        print(f"    {skill:<40} {cnt:>5,} candidates")

    # ── Industry breakdown (current)
    industries = Counter(r.get("profile", {}).get("current_industry") for r in records)
    print(f"\n  Top 10 current industries:")
    for ind, cnt in industries.most_common(10):
        print(f"    {str(ind):<45} {pct(cnt, N)}")

    # ── Location breakdown
    locations = Counter(r.get("profile", {}).get("location") for r in records)
    print(f"\n  Top 10 candidate locations:")
    for loc, cnt in locations.most_common(10):
        print(f"    {str(loc):<45} {pct(cnt, N)}")

    # ── Company size (current)
    sizes = Counter(r.get("profile", {}).get("current_company_size") for r in records)
    print(f"\n  Current company size breakdown:")
    for sz in ["1-10","11-50","51-200","201-500","501-1000","1001-5000","5001-10000","10001+"]:
        print(f"    {sz:<12} {pct(sizes[sz], N)}")

    # ── Verification signals
    v_email = sum(1 for r in records if r.get("redrob_signals", {}).get("verified_email"))
    v_phone = sum(1 for r in records if r.get("redrob_signals", {}).get("verified_phone"))
    v_li    = sum(1 for r in records if r.get("redrob_signals", {}).get("linkedin_connected"))
    print(f"\n  Verification signals:")
    print(f"    verified_email      : {pct(v_email, N)}")
    print(f"    verified_phone      : {pct(v_phone, N)}")
    print(f"    linkedin_connected  : {pct(v_li,    N)}")

    # ── Offer acceptance rate
    oar = [r["redrob_signals"]["offer_acceptance_rate"]
           for r in records
           if r.get("redrob_signals", {}).get("offer_acceptance_rate", -1) != -1]
    if oar:
        print(f"\n  Offer acceptance rate (excl. -1 sentinels):")
        print(f"    N with history : {len(oar):,}")
        print(f"    avg            : {sum(oar)/len(oar):.2f}")

    # ── Interview completion rate
    icr = [r["redrob_signals"]["interview_completion_rate"]
           for r in records
           if "interview_completion_rate" in r.get("redrob_signals", {})]
    if icr:
        no_show = sum(1 for v in icr if v < 0.5)
        print(f"\n  Interview completion rate < 50% (ghosting risk): {pct(no_show, N)}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Explore candidates.jsonl for Redrob challenge")
    parser.add_argument("--file",   default="candidates.jsonl", help="Path to .jsonl file")
    parser.add_argument("--sample", type=int, default=1,        help="Number of sample records to print (section 2)")
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"\n[ERROR] File not found: {filepath}")
        print("  Pass the correct path with:  python explore_candidates.py --file path/to/candidates.jsonl")
        sys.exit(1)

    print(f"\n{'═' * 72}")
    print(f"  REDROB CANDIDATE DATASET EXPLORER")
    print(f"  File : {filepath.resolve()}")
    print(f"  Run  : {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print(f"{'═' * 72}")

    records = load_jsonl(str(filepath))
    print(f"\n  Loaded {len(records):,} records successfully.\n")

    if not records:
        print("[ERROR] No records found. Check the file.")
        sys.exit(1)

    print_fields(records)
    print_one_record(records, n_samples=args.sample)
    print_data_types(records)
    count_missing(records)
    summary_report(records)

    separator()
    print("  Exploration complete.")
    separator()


if __name__ == "__main__":
    main()