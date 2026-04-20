"""
Generate synthetic performance and productivity data for analysis.

Datasets created:
- performance_reviews.csv: Historical performance ratings (3 years, bi-annual)
- current_workforce.csv: Current employee snapshot with latest ratings
- nine_box.csv: Performance × Potential matrix data
- pips.csv: Performance improvement plans
- productivity_metrics.csv: Output metrics by employee
- promotions.csv: Promotion history
- managers.csv: Manager information with team stats
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_EMPLOYEES = 500
NUM_MANAGERS = 45
REVIEW_CYCLES = 6  # 3 years of bi-annual reviews

# Generate dates for review cycles (last 3 years, bi-annual)
today = datetime(2026, 4, 1)
review_dates = [today - timedelta(days=180*i) for i in range(REVIEW_CYCLES)]
review_dates.reverse()

print("Generating Performance & Productivity synthetic data...")
print("=" * 70)

# ===========================
# 1. CURRENT WORKFORCE
# ===========================
print("\n1. Generating current workforce...")

departments = ['Engineering', 'Sales', 'Marketing', 'Product', 'Customer Success',
               'Data', 'Finance', 'HR', 'Operations', 'Legal']
dept_weights = [0.30, 0.20, 0.12, 0.10, 0.10, 0.05, 0.05, 0.04, 0.03, 0.01]

job_levels = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP']
level_weights = [0.15, 0.25, 0.25, 0.15, 0.08, 0.07, 0.03, 0.015, 0.005]

locations = ['San Francisco', 'New York', 'Austin', 'Boston', 'Seattle', 'Remote', 'Chicago', 'Los Angeles']

workforce = []
employee_id = 1000

for i in range(NUM_EMPLOYEES):
    dept = np.random.choice(departments, p=dept_weights)
    level = np.random.choice(job_levels, p=level_weights)

    # Tenure (affects performance to some degree)
    tenure_months = int(np.random.exponential(36) + 6)  # Average 3 years, min 6 months
    tenure_months = min(tenure_months, 180)  # Cap at 15 years

    # Base salary by level
    salary_by_level = {
        'IC1': (60000, 80000), 'IC2': (80000, 110000), 'IC3': (110000, 150000),
        'IC4': (140000, 190000), 'IC5': (180000, 250000),
        'Manager': (140000, 180000), 'Senior Manager': (170000, 220000),
        'Director': (200000, 280000), 'VP': (250000, 400000)
    }
    base_salary = np.random.randint(*salary_by_level[level])

    # Demographics
    gender = np.random.choice(['Male', 'Female', 'Non-binary'], p=[0.52, 0.46, 0.02])
    race = np.random.choice(['White', 'Asian', 'Black', 'Hispanic', 'Other'], p=[0.50, 0.25, 0.12, 0.10, 0.03])

    workforce.append({
        'employee_id': employee_id,
        'department': dept,
        'job_level': level,
        'tenure_months': tenure_months,
        'location': np.random.choice(locations),
        'manager_id': None,  # Will assign later
        'base_salary': base_salary,
        'gender': gender,
        'race': race,
        'is_manager': 'Manager' in level or 'Director' in level or 'VP' in level
    })
    employee_id += 1

workforce_df = pd.DataFrame(workforce)

# Assign managers (sample from managers)
managers = workforce_df[workforce_df['is_manager']].sample(NUM_MANAGERS)['employee_id'].tolist()
non_managers = workforce_df[~workforce_df['is_manager']]

for idx in non_managers.index:
    # Assign manager from same department if possible
    dept = workforce_df.loc[idx, 'department']
    dept_managers = workforce_df[(workforce_df['employee_id'].isin(managers)) &
                                  (workforce_df['department'] == dept)]['employee_id'].tolist()
    if dept_managers:
        workforce_df.loc[idx, 'manager_id'] = np.random.choice(dept_managers)
    else:
        workforce_df.loc[idx, 'manager_id'] = np.random.choice(managers)

workforce_df['manager_id'] = workforce_df['manager_id'].fillna(1000)  # CEO has no manager

print(f"   Created {len(workforce_df)} employees across {len(departments)} departments")

# ===========================
# 2. PERFORMANCE REVIEWS (HISTORICAL)
# ===========================
print("\n2. Generating performance review history...")

# Performance rating scale: 1-5
# 1 = Does Not Meet, 2 = Needs Improvement, 3 = Meets Expectations, 4 = Exceeds, 5 = Outstanding
rating_labels = {1: 'Does Not Meet', 2: 'Needs Improvement', 3: 'Meets Expectations',
                 4: 'Exceeds Expectations', 5: 'Outstanding'}

performance_reviews = []

for _, emp in workforce_df.iterrows():
    emp_id = emp['employee_id']
    manager_id = emp['manager_id']

    # Determine employee's "true" performance level (consistent trait)
    # Influenced by tenure and level
    base_performance = np.random.normal(3.2, 0.8)  # Mean slightly above 3
    base_performance = np.clip(base_performance, 1, 5)

    # Adjust for tenure (experienced employees slightly better)
    if emp['tenure_months'] > 36:
        base_performance += 0.2
    elif emp['tenure_months'] < 12:
        base_performance -= 0.1

    base_performance = np.clip(base_performance, 1, 5)

    # Generate reviews for each cycle (only if employed at that time)
    start_date = today - timedelta(days=30 * emp['tenure_months'])

    for review_date in review_dates:
        if review_date < start_date:
            continue  # Employee not yet hired

        # Add some variation to rating over time
        rating = base_performance + np.random.normal(0, 0.3)
        rating = np.clip(rating, 1, 5)
        rating_int = int(round(rating))

        performance_reviews.append({
            'employee_id': emp_id,
            'review_date': review_date.strftime('%Y-%m-%d'),
            'manager_id': manager_id,
            'rating_numeric': rating_int,
            'rating_label': rating_labels[rating_int],
            'goals_met': np.random.choice(['Yes', 'Mostly', 'Partially', 'No'], p=[0.4, 0.35, 0.20, 0.05]),
            'review_cycle': f"{review_date.year}-H{1 if review_date.month <= 6 else 2}"
        })

performance_df = pd.DataFrame(performance_reviews)
print(f"   Created {len(performance_df)} performance review records across {REVIEW_CYCLES} cycles")

# Add latest rating to workforce
latest_reviews = performance_df.sort_values('review_date').groupby('employee_id').last().reset_index()
workforce_df = workforce_df.merge(
    latest_reviews[['employee_id', 'rating_numeric', 'rating_label']],
    on='employee_id',
    how='left'
)
workforce_df.rename(columns={'rating_numeric': 'latest_rating', 'rating_label': 'latest_rating_label'}, inplace=True)

# ===========================
# 3. 9-BOX DATA (Performance × Potential)
# ===========================
print("\n3. Generating 9-box talent matrix data...")

nine_box_data = []

for _, emp in workforce_df.iterrows():
    emp_id = emp['employee_id']
    performance = emp['latest_rating']

    # Potential (1-3: Low, Medium, High)
    # Higher performers more likely to have higher potential, but not perfectly correlated
    if performance >= 4:
        potential = np.random.choice([2, 3], p=[0.3, 0.7])
    elif performance == 3:
        potential = np.random.choice([1, 2, 3], p=[0.2, 0.6, 0.2])
    else:
        potential = np.random.choice([1, 2], p=[0.7, 0.3])

    potential_labels = {1: 'Low', 2: 'Medium', 3: 'High'}

    # Performance category
    if performance >= 4:
        perf_category = 'High'
    elif performance == 3:
        perf_category = 'Medium'
    else:
        perf_category = 'Low'

    # 9-box label
    box_labels = {
        ('High', 'High'): 'Star / Top Talent',
        ('High', 'Medium'): 'High Professional',
        ('High', 'Low'): 'Subject Matter Expert',
        ('Medium', 'High'): 'High Potential / Enigma',
        ('Medium', 'Medium'): 'Core Contributor',
        ('Medium', 'Low'): 'Solid Performer',
        ('Low', 'High'): 'Inconsistent / Enigma',
        ('Low', 'Medium'): 'Needs Development',
        ('Low', 'Low'): 'Low Performer'
    }

    box_label = box_labels[(perf_category, potential_labels[potential])]

    nine_box_data.append({
        'employee_id': emp_id,
        'performance_rating': performance,
        'performance_category': perf_category,
        'potential_rating': potential,
        'potential_category': potential_labels[potential],
        'nine_box_segment': box_label,
        'high_potential_flag': potential == 3,
        'assessment_date': today.strftime('%Y-%m-%d')
    })

nine_box_df = pd.DataFrame(nine_box_data)
print(f"   Created 9-box data for {len(nine_box_df)} employees")

# ===========================
# 4. PERFORMANCE IMPROVEMENT PLANS (PIPs)
# ===========================
print("\n4. Generating performance improvement plans...")

pips = []

# Low performers (rating 1-2) may have PIPs
low_performers = workforce_df[workforce_df['latest_rating'] <= 2]

for _, emp in low_performers.iterrows():
    # 60% of low performers have a PIP
    if np.random.random() < 0.6:
        pip_start = today - timedelta(days=np.random.randint(30, 180))
        pip_duration = 90  # 90 days typically

        # Outcome: Improved (30%), No Change (40%), Exited (30%)
        outcome = np.random.choice(['Improved', 'No Improvement', 'Exited'], p=[0.3, 0.4, 0.3])

        if outcome == 'Improved':
            end_date = pip_start + timedelta(days=pip_duration)
            status = 'Completed'
        elif outcome == 'Exited':
            end_date = pip_start + timedelta(days=np.random.randint(30, pip_duration))
            status = 'Terminated'
        else:
            end_date = None
            status = 'In Progress' if (today - pip_start).days < pip_duration else 'Completed'

        pips.append({
            'employee_id': emp['employee_id'],
            'pip_start_date': pip_start.strftime('%Y-%m-%d'),
            'pip_end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'pip_duration_days': pip_duration,
            'status': status,
            'outcome': outcome if status == 'Completed' or status == 'Terminated' else 'Pending',
            'manager_id': emp['manager_id']
        })

pips_df = pd.DataFrame(pips)
print(f"   Created {len(pips_df)} performance improvement plans")

# ===========================
# 5. PRODUCTIVITY METRICS
# ===========================
print("\n5. Generating productivity metrics...")

productivity = []

for _, emp in workforce_df.iterrows():
    dept = emp['department']
    rating = emp['latest_rating']

    # Department-specific productivity metrics
    if dept == 'Sales':
        deals_closed = int(np.random.normal(rating * 4, 2))
        revenue_generated = deals_closed * np.random.randint(30000, 150000)
        metric_name = 'Deals Closed'
        metric_value = deals_closed
    elif dept == 'Engineering':
        tickets_closed = int(np.random.normal(rating * 20, 8))
        metric_name = 'Tickets Closed'
        metric_value = tickets_closed
    elif dept == 'Customer Success':
        accounts_managed = int(np.random.normal(rating * 15, 5))
        metric_name = 'Accounts Managed'
        metric_value = accounts_managed
    elif dept == 'Marketing':
        campaigns_launched = int(np.random.normal(rating * 5, 2))
        metric_name = 'Campaigns Launched'
        metric_value = campaigns_launched
    else:
        # Generic output metric
        metric_name = 'Projects Completed'
        metric_value = int(np.random.normal(rating * 8, 3))

    metric_value = max(0, metric_value)

    # Productivity score (normalized)
    productivity_score = (rating / 5.0) * 100 + np.random.normal(0, 10)
    productivity_score = np.clip(productivity_score, 0, 100)

    productivity.append({
        'employee_id': emp['employee_id'],
        'metric_name': metric_name,
        'metric_value': metric_value,
        'productivity_score': round(productivity_score, 1),
        'measurement_period': 'Q1 2026'
    })

productivity_df = pd.DataFrame(productivity)
print(f"   Created {len(productivity_df)} productivity records")

# ===========================
# 6. PROMOTIONS
# ===========================
print("\n6. Generating promotion history...")

promotions = []

# High performers more likely to be promoted
for _, emp in workforce_df.iterrows():
    # Only employees with 12+ months tenure eligible
    if emp['tenure_months'] < 12:
        continue

    # Promotion probability based on rating
    if emp['latest_rating'] >= 4:
        promo_prob = 0.25
    elif emp['latest_rating'] == 3:
        promo_prob = 0.05
    else:
        promo_prob = 0.01

    if np.random.random() < promo_prob:
        # Promotion happened in last 2 years
        promo_date = today - timedelta(days=np.random.randint(30, 720))

        # Previous level (simulate)
        level_progression = {
            'IC2': 'IC1', 'IC3': 'IC2', 'IC4': 'IC3', 'IC5': 'IC4',
            'Manager': 'IC4', 'Senior Manager': 'Manager',
            'Director': 'Senior Manager', 'VP': 'Director'
        }

        current_level = emp['job_level']
        previous_level = level_progression.get(current_level, current_level)

        promotions.append({
            'employee_id': emp['employee_id'],
            'promotion_date': promo_date.strftime('%Y-%m-%d'),
            'previous_level': previous_level,
            'new_level': current_level,
            'performance_rating_at_promotion': emp['latest_rating'],
            'tenure_at_promotion_months': max(12, emp['tenure_months'] - int((today - promo_date).days / 30))
        })

promotions_df = pd.DataFrame(promotions)
print(f"   Created {len(promotions_df)} promotion records")

# ===========================
# 7. MANAGER SUMMARY
# ===========================
print("\n7. Generating manager summary...")

manager_summary = []

for mgr_id in managers:
    mgr_data = workforce_df[workforce_df['employee_id'] == mgr_id].iloc[0]
    team = workforce_df[workforce_df['manager_id'] == mgr_id]

    if len(team) == 0:
        continue

    team_size = len(team)
    avg_rating = team['latest_rating'].mean()
    rating_std = team['latest_rating'].std()
    pct_high_performers = (team['latest_rating'] >= 4).sum() / team_size * 100
    pct_low_performers = (team['latest_rating'] <= 2).sum() / team_size * 100

    # Manager rating consistency (variance)
    consistency_score = 'Consistent' if rating_std < 0.8 else 'Inconsistent'

    manager_summary.append({
        'manager_id': mgr_id,
        'manager_name': f'Manager {mgr_id}',
        'department': mgr_data['department'],
        'team_size': team_size,
        'avg_team_rating': round(avg_rating, 2),
        'rating_std_dev': round(rating_std, 2),
        'pct_high_performers': round(pct_high_performers, 1),
        'pct_low_performers': round(pct_low_performers, 1),
        'consistency_score': consistency_score
    })

managers_df = pd.DataFrame(manager_summary)
print(f"   Created summary for {len(managers_df)} managers")

# ===========================
# SAVE ALL DATASETS
# ===========================
print("\n" + "=" * 70)
print("SAVING DATASETS")
print("=" * 70)

performance_df.to_csv('performance_reviews.csv', index=False)
print(f"✓ performance_reviews.csv ({len(performance_df)} records)")

workforce_df.to_csv('current_workforce.csv', index=False)
print(f"✓ current_workforce.csv ({len(workforce_df)} employees)")

nine_box_df.to_csv('nine_box.csv', index=False)
print(f"✓ nine_box.csv ({len(nine_box_df)} employees)")

pips_df.to_csv('pips.csv', index=False)
print(f"✓ pips.csv ({len(pips_df)} PIPs)")

productivity_df.to_csv('productivity_metrics.csv', index=False)
print(f"✓ productivity_metrics.csv ({len(productivity_df)} records)")

promotions_df.to_csv('promotions.csv', index=False)
print(f"✓ promotions.csv ({len(promotions_df)} promotions)")

managers_df.to_csv('managers.csv', index=False)
print(f"✓ managers.csv ({len(managers_df)} managers)")

print("\n" + "=" * 70)
print("DATA GENERATION COMPLETE!")
print("=" * 70)
print("\nKey Statistics:")
print(f"  Total Employees: {len(workforce_df)}")
print(f"  Total Reviews: {len(performance_df)}")
print(f"  High Performers (4-5 rating): {(workforce_df['latest_rating'] >= 4).sum()} ({(workforce_df['latest_rating'] >= 4).sum()/len(workforce_df)*100:.1f}%)")
print(f"  Low Performers (1-2 rating): {(workforce_df['latest_rating'] <= 2).sum()} ({(workforce_df['latest_rating'] <= 2).sum()/len(workforce_df)*100:.1f}%)")
print(f"  Active PIPs: {len(pips_df[pips_df['status'] == 'In Progress'])}")
print(f"  Promotions (last 2 years): {len(promotions_df)}")
print(f"  Average Rating: {workforce_df['latest_rating'].mean():.2f}")
