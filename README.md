# Rivora – AI Candidate Intelligence Engine

Built for the Redrob Data & AI Challenge 2026.

## Problem

Recruiters often rely on keyword matching, which can miss highly qualified candidates. Rivora helps identify the best candidates by analyzing technical skills, experience, career history, and behavioral signals.

## Solution

Rivora processes candidate profiles and generates recruiter-ready rankings using:

- Technical skill relevance
- Professional experience
- Career history analysis
- GitHub activity
- Recruiter response rate
- Interview completion signals
- Notice period availability

## Features

- Processes 100,000 candidate profiles
- Generates ranked candidate recommendations
- Explainable recruiter-style reasoning
- Interactive Streamlit dashboard
- Top 100 candidate export

## Tech Stack

- Python
- Streamlit
- Pandas
- JSONL Processing

## Project Structure

```text
src/
├── ranker.py
├── scoring_engine.py
├── rank_all_candidates.py

app.py
requirements.txt
```

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
## Architecture 

<img width="1902" height="521" alt="image" src="https://github.com/user-attachments/assets/c8fe0d3c-054b-4fbc-b731-edb4f95c3e07" />



## Output

The system generates:

- Ranked candidate shortlist
- Candidate scores
- Recruiter-style explanations
- Dashboard visualization

  <img width="1898" height="977" alt="image" src="https://github.com/user-attachments/assets/3d92dd64-d8ff-4e33-b015-6155c9284aff" />


  <img width="1917" height="997" alt="image" src="https://github.com/user-attachments/assets/16abdb48-e440-425c-9ea6-f7dc5de9c284" />

## Team

Rivora – Redrob Data & AI Challenge Submission

Shivasri.S - II YEAR BTECH IT Student
Yashaswini.S - II YEAR BTECH IT Student
