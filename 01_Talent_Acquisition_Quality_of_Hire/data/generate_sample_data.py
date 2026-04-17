"""
Generate Synthetic Recruiting Data for Analysis

This script creates realistic sample datasets for talent acquisition analytics.
All data is completely synthetic and does not represent real individuals.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_REQUISITIONS = 50
NUM_CANDIDATES = 1000
HIRE_RATE = 0.05  # 5% of candidates get hired

print("🔧 Generating synthetic recruiting data...")
print(f"   Requisitions: {NUM_REQUISITIONS}")
print(f"   Candidates: {NUM_CANDIDATES}")
print()

# ============================================================================
# 1. Generate Requisitions
# ============================================================================

print("📋 Generating requisitions...")

req_ids = [f"REQ-{i+1:04d}" for i in range(NUM_REQUISITIONS)]
departments = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 'Finance', 'HR', 'Operations']
job_families = {
    'Engineering': ['Software Engineer', 'Senior Software Engineer', 'Staff Engineer', 'Engineering Manager'],
    'Product': ['Product Manager', 'Senior Product Manager', 'Product Designer'],
    'Sales': ['Account Executive', 'Sales Development Rep', 'Sales Manager'],
    'Marketing': ['Marketing Manager', 'Content Writer', 'Marketing Analyst'],
    'Customer Success': ['Customer Success Manager', 'Support Engineer'],
    'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager'],
    'HR': ['Recruiter', 'HR Business Partner', 'HR Coordinator'],
    'Operations': ['Operations Manager', 'Program Manager', 'Business Analyst']
}

levels = ['Entry', 'Mid', 'Senior', 'Lead/Manager']

requisitions_data = []
for req_id in req_ids:
    dept = random.choice(departments)
    title = random.choice(job_families[dept])
    level = random.choice(levels)

    # Senior/Lead roles have longer time-to-fill
    if 'Senior' in title or 'Manager' in title or level in ['Senior', 'Lead/Manager']:
        base_ttf = 55
    elif level == 'Mid':
        base_ttf = 40
    else:
        base_ttf = 30

    opened_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 120))
    time_to_fill = int(np.random.normal(base_ttf, 10))
    time_to_fill = max(15, time_to_fill)  # Minimum 15 days

    status = random.choices(['Filled', 'Open', 'Cancelled'], weights=[0.7, 0.25, 0.05])[0]

    if status == 'Filled':
        filled_date = opened_date + timedelta(days=time_to_fill)
    else:
        filled_date = None
        time_to_fill = None

    requisitions_data.append({
        'requisition_id': req_id,
        'department': dept,
        'job_title': title,
        'level': level,
        'opened_date': opened_date.strftime('%Y-%m-%d'),
        'filled_date': filled_date.strftime('%Y-%m-%d') if filled_date else None,
        'time_to_fill_days': time_to_fill,
        'status': status,
        'target_fill_date': (opened_date + timedelta(days=45)).strftime('%Y-%m-%d'),
        'hiring_manager': f"Manager_{random.randint(1, 20)}"
    })

requisitions_df = pd.DataFrame(requisitions_data)

# ============================================================================
# 2. Generate Candidates
# ============================================================================

print("👥 Generating candidates...")

candidate_ids = [f"CAND-{i+1:05d}" for i in range(NUM_CANDIDATES)]
sources = ['Referral', 'LinkedIn', 'Indeed', 'Company Career Site', 'Recruiting Agency',
           'University Recruiting', 'Glassdoor', 'Other Job Board']
source_weights = [0.20, 0.25, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05]

genders = ['Male', 'Female', 'Non-binary', 'Prefer not to say']
gender_weights = [0.48, 0.48, 0.02, 0.02]

ethnicities = ['White', 'Asian', 'Hispanic/Latino', 'Black/African American',
               'Two or more races', 'Native American', 'Prefer not to say']
ethnicity_weights = [0.55, 0.20, 0.12, 0.08, 0.03, 0.01, 0.01]

candidates_data = []
for cand_id in candidate_ids:
    # Random requisition application
    req_id = random.choice(req_ids)
    req_info = requisitions_df[requisitions_df['requisition_id'] == req_id].iloc[0]

    # Application date after req opened
    req_opened = datetime.strptime(req_info['opened_date'], '%Y-%m-%d')
    days_after_open = random.randint(1, 60)
    applied_date = req_opened + timedelta(days=days_after_open)

    source = random.choices(sources, weights=source_weights)[0]

    # Demographics
    gender = random.choices(genders, weights=gender_weights)[0]
    ethnicity = random.choices(ethnicities, weights=ethnicity_weights)[0]

    # Experience and education
    years_exp = random.randint(0, 20)
    education = random.choices(['High School', 'Bachelors', 'Masters', 'PhD'],
                               weights=[0.05, 0.60, 0.30, 0.05])[0]

    # Stage progression
    stages = ['Applied', 'Screening', 'Phone Screen', 'Technical Interview',
              'Onsite Interview', 'Offer', 'Hired', 'Rejected', 'Withdrew']

    # Progression probabilities
    if source == 'Referral':
        hired_prob = 0.10  # Referrals convert better
    elif source == 'Recruiting Agency':
        hired_prob = 0.07
    else:
        hired_prob = HIRE_RATE

    got_hired = random.random() < hired_prob

    if got_hired:
        current_stage = 'Hired'
    elif random.random() < 0.1:
        current_stage = 'Withdrew'
    elif random.random() < 0.6:
        current_stage = random.choice(['Screening', 'Phone Screen', 'Rejected'])
    else:
        current_stage = random.choice(['Technical Interview', 'Onsite Interview', 'Offer', 'Rejected'])

    candidates_data.append({
        'candidate_id': cand_id,
        'requisition_id': req_id,
        'applied_date': applied_date.strftime('%Y-%m-%d'),
        'source': source,
        'current_stage': current_stage,
        'gender': gender,
        'ethnicity': ethnicity,
        'years_experience': years_exp,
        'education_level': education,
        'referrer_id': f"EMP-{random.randint(1, 200)}" if source == 'Referral' else None
    })

candidates_df = pd.DataFrame(candidates_data)

# ============================================================================
# 3. Generate Interview Data
# ============================================================================

print("💼 Generating interview data...")

interview_types = ['Phone Screen', 'Technical Screen', 'Hiring Manager',
                   'Team Interview', 'Executive Interview', 'Culture Fit']

interviews_data = []
interview_id = 1

for _, cand in candidates_df.iterrows():
    # Only generate interviews for candidates past screening
    if cand['current_stage'] in ['Applied', 'Screening']:
        continue

    # Number of interviews based on stage
    if cand['current_stage'] in ['Phone Screen', 'Rejected', 'Withdrew']:
        num_interviews = random.randint(1, 2)
    elif cand['current_stage'] in ['Technical Interview']:
        num_interviews = random.randint(2, 3)
    elif cand['current_stage'] in ['Onsite Interview', 'Offer', 'Hired']:
        num_interviews = random.randint(3, 5)
    else:
        num_interviews = 1

    applied_date = datetime.strptime(cand['applied_date'], '%Y-%m-%d')

    for i in range(num_interviews):
        interview_type = random.choice(interview_types[:min(i+2, len(interview_types))])

        # Interview date after application
        interview_date = applied_date + timedelta(days=random.randint(5 + i*7, 14 + i*7))

        # Score (1-5 scale)
        # Hired candidates generally score higher
        if cand['current_stage'] == 'Hired':
            score = random.choices([3, 4, 5], weights=[0.1, 0.3, 0.6])[0]
        elif cand['current_stage'] == 'Rejected':
            score = random.choices([1, 2, 3], weights=[0.3, 0.4, 0.3])[0]
        else:
            score = random.choices([2, 3, 4], weights=[0.2, 0.5, 0.3])[0]

        interviews_data.append({
            'interview_id': f"INT-{interview_id:06d}",
            'candidate_id': cand['candidate_id'],
            'requisition_id': cand['requisition_id'],
            'interview_type': interview_type,
            'interview_date': interview_date.strftime('%Y-%m-%d'),
            'interviewer_id': f"EMP-{random.randint(1, 200)}",
            'score': score,
            'notes_completed': random.choices([True, False], weights=[0.85, 0.15])[0]
        })

        interview_id += 1

interviews_df = pd.DataFrame(interviews_data)

# ============================================================================
# 4. Generate Hires Data (with outcomes)
# ============================================================================

print("✅ Generating hires data with outcomes...")

hires_df = candidates_df[candidates_df['current_stage'] == 'Hired'].copy()

hires_data = []
for _, hire in hires_df.iterrows():
    req_info = requisitions_df[requisitions_df['requisition_id'] == hire['requisition_id']].iloc[0]

    if pd.notna(req_info['filled_date']):
        hire_date = datetime.strptime(req_info['filled_date'], '%Y-%m-%d')
    else:
        applied_date = datetime.strptime(hire['applied_date'], '%Y-%m-%d')
        hire_date = applied_date + timedelta(days=random.randint(30, 60))

    # Generate outcomes (measured 12 months post-hire)
    # Source affects quality
    quality_boost = 0
    if hire['source'] == 'Referral':
        quality_boost = 0.3
    elif hire['source'] == 'Recruiting Agency':
        quality_boost = 0.1
    elif hire['source'] == 'University Recruiting':
        quality_boost = 0.15

    # Performance rating (1-5)
    perf_mean = 3.5 + quality_boost
    performance_12mo = np.clip(np.random.normal(perf_mean, 0.7), 1, 5)
    performance_12mo = round(performance_12mo, 1)

    # Still employed at 12 months?
    retention_prob = 0.85 + quality_boost * 0.2
    still_employed_12mo = random.random() < retention_prob

    # Hiring manager satisfaction
    satisfaction = np.clip(np.random.normal(4.0 + quality_boost, 0.8), 1, 5)
    satisfaction = round(satisfaction, 1)

    # Time to productivity (days)
    if hire['years_experience'] < 2:
        productivity_days = int(np.random.normal(90, 20))
    elif hire['years_experience'] < 5:
        productivity_days = int(np.random.normal(60, 15))
    else:
        productivity_days = int(np.random.normal(45, 10))

    hires_data.append({
        'employee_id': f"EMP-{random.randint(1000, 9999)}",
        'candidate_id': hire['candidate_id'],
        'requisition_id': hire['requisition_id'],
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'source': hire['source'],
        'department': req_info['department'],
        'job_title': req_info['job_title'],
        'level': req_info['level'],
        'gender': hire['gender'],
        'ethnicity': hire['ethnicity'],
        'years_experience': hire['years_experience'],
        'education_level': hire['education_level'],
        'performance_rating_12mo': performance_12mo,
        'still_employed_12mo': still_employed_12mo,
        'manager_satisfaction': satisfaction,
        'days_to_productivity': productivity_days,
        'promoted_within_24mo': random.choices([True, False], weights=[0.20, 0.80])[0] if still_employed_12mo else False
    })

hires_outcomes_df = pd.DataFrame(hires_data)

# ============================================================================
# 5. Save all datasets
# ============================================================================

print("\n💾 Saving datasets...")

requisitions_df.to_csv('requisitions.csv', index=False)
print(f"   ✅ requisitions.csv ({len(requisitions_df)} records)")

candidates_df.to_csv('candidates.csv', index=False)
print(f"   ✅ candidates.csv ({len(candidates_df)} records)")

interviews_df.to_csv('interviews.csv', index=False)
print(f"   ✅ interviews.csv ({len(interviews_df)} records)")

hires_outcomes_df.to_csv('hires.csv', index=False)
print(f"   ✅ hires.csv ({len(hires_outcomes_df)} records)")

# ============================================================================
# 6. Generate summary statistics
# ============================================================================

print("\n📊 Summary Statistics:")
print(f"\n   Requisitions:")
print(f"      Total: {len(requisitions_df)}")
print(f"      Filled: {len(requisitions_df[requisitions_df['status'] == 'Filled'])}")
print(f"      Open: {len(requisitions_df[requisitions_df['status'] == 'Open'])}")
print(f"      Avg Time-to-Fill: {requisitions_df['time_to_fill_days'].mean():.1f} days")

print(f"\n   Candidates:")
print(f"      Total Applications: {len(candidates_df)}")
print(f"      Hired: {len(candidates_df[candidates_df['current_stage'] == 'Hired'])}")
print(f"      Hire Rate: {len(candidates_df[candidates_df['current_stage'] == 'Hired']) / len(candidates_df) * 100:.1f}%")

print(f"\n   Top Sources:")
for source in candidates_df['source'].value_counts().head(5).items():
    print(f"      {source[0]}: {source[1]} candidates")

print(f"\n   Quality of Hire:")
print(f"      Avg Performance (12mo): {hires_outcomes_df['performance_rating_12mo'].mean():.2f}/5")
print(f"      12-Month Retention: {hires_outcomes_df['still_employed_12mo'].mean() * 100:.1f}%")
print(f"      Avg Manager Satisfaction: {hires_outcomes_df['manager_satisfaction'].mean():.2f}/5")

print(f"\n   Quality by Source:")
for source in hires_outcomes_df.groupby('source')['performance_rating_12mo'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(5).itertuples():
    print(f"      {source.Index}: {source.mean:.2f}/5 (n={int(source.count)})")

print("\n✅ Data generation complete!")
print("\n📂 Files created:")
print("   - requisitions.csv")
print("   - candidates.csv")
print("   - interviews.csv")
print("   - hires.csv")
