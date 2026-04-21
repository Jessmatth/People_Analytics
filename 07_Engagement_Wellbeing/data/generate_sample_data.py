"""
Generate synthetic data for Employee Engagement & Wellbeing analysis
Domain 7: Engagement surveys, burnout risk, and wellbeing trends

Creates realistic datasets demonstrating engagement patterns and wellbeing indicators.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
NUM_EMPLOYEES = 500
NUM_PULSE_SURVEYS = 4  # Quarterly surveys
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 'Operations', 'HR', 'Finance']
LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP']

# Engagement drivers (research-based from Gallup Q12)
ENGAGEMENT_DIMENSIONS = [
    'expectations_clarity',
    'materials_equipment',
    'opportunity_best',
    'recognition_praise',
    'cares_about_me',
    'development_encouraged',
    'opinions_count',
    'mission_purpose',
    'quality_commitment',
    'best_friend_work',
    'progress_discussion',
    'learn_grow'
]

WELLBEING_DIMENSIONS = [
    'work_life_balance',
    'manageable_workload',
    'adequate_rest',
    'feeling_energized',
    'stress_level_manageable',
    'boundary_respect'
]

# ============================================================================
# Generate Employee Records
# ============================================================================

print("Generating employee data...")

employees_data = []
employee_id = 1000

for i in range(NUM_EMPLOYEES):
    dept = random.choice(DEPARTMENTS)
    level = random.choice(LEVELS)

    # Tenure influences engagement and burnout risk
    tenure_months = int(np.random.exponential(24) + 1)
    tenure_months = min(tenure_months, 120)  # Cap at 10 years

    # Manager effectiveness (from Domain 5)
    manager_effectiveness = np.random.beta(5, 2)  # Skew toward higher scores

    # Base engagement level (influenced by manager, tenure, department)
    base_engagement = 0.5
    base_engagement += manager_effectiveness * 0.3  # Manager impact
    base_engagement += (min(tenure_months, 24) / 24) * 0.1  # Honeymoon period

    # Department effects (some have systematically lower engagement)
    dept_effects = {
        'Engineering': 0.05,
        'Product': 0.10,
        'Sales': -0.10,  # High pressure
        'Customer Success': -0.05,  # Burnout prone
        'Operations': -0.08,
        'Marketing': 0.0,
        'HR': 0.05,
        'Finance': 0.0
    }
    base_engagement += dept_effects.get(dept, 0)

    # Add individual variation
    base_engagement += np.random.normal(0, 0.15)
    base_engagement = np.clip(base_engagement, 0.1, 0.95)

    # Work hours and burnout risk
    standard_hours = 40
    dept_hour_multipliers = {
        'Engineering': 1.15,
        'Product': 1.10,
        'Sales': 1.20,
        'Customer Success': 1.15,
        'Operations': 1.05,
        'Marketing': 1.10,
        'HR': 1.0,
        'Finance': 1.25  # Highest burnout risk
    }

    avg_weekly_hours = standard_hours * dept_hour_multipliers.get(dept, 1.0)
    avg_weekly_hours += np.random.normal(0, 5)
    avg_weekly_hours = max(35, avg_weekly_hours)

    # PTO usage (low usage = burnout risk)
    pto_days_available = 20
    pto_days_used = np.random.beta(3, 2) * pto_days_available
    pto_usage_rate = pto_days_used / pto_days_available

    # Burnout risk score (0-100)
    burnout_risk = 20  # Base
    burnout_risk += max(0, (avg_weekly_hours - 45) * 2)  # Hours over 45
    burnout_risk += max(0, (0.5 - pto_usage_rate) * 40)  # Low PTO usage
    burnout_risk += (1 - manager_effectiveness) * 30  # Poor manager
    burnout_risk += (1 - base_engagement) * 20  # Low engagement
    burnout_risk = np.clip(burnout_risk + np.random.normal(0, 10), 0, 100)

    # Performance rating (correlated with engagement, negatively with burnout)
    performance = 3.0  # Base "meets expectations"
    performance += base_engagement * 1.5
    performance -= (burnout_risk / 100) * 1.0
    performance += np.random.normal(0, 0.3)
    performance = np.clip(performance, 1.0, 5.0)

    # Attrition risk
    left = False
    if base_engagement < 0.3 or burnout_risk > 80:
        left = random.random() < 0.4  # 40% leave if highly disengaged or burned out
    elif base_engagement < 0.5 or burnout_risk > 60:
        left = random.random() < 0.15  # 15% leave if moderately disengaged
    else:
        left = random.random() < 0.05  # 5% baseline attrition

    employees_data.append({
        'employee_id': employee_id,
        'department': dept,
        'level': level,
        'tenure_months': tenure_months,
        'manager_effectiveness_score': round(manager_effectiveness, 3),
        'avg_weekly_hours': round(avg_weekly_hours, 1),
        'pto_days_available': pto_days_available,
        'pto_days_used': round(pto_days_used, 1),
        'pto_usage_rate': round(pto_usage_rate, 3),
        'performance_rating': round(performance, 2),
        'has_left': left,
        'base_engagement_level': round(base_engagement, 3),
        'burnout_risk_score': round(burnout_risk, 1)
    })

    employee_id += 1

employees_df = pd.DataFrame(employees_data)

# ============================================================================
# Generate Pulse Survey Responses
# ============================================================================

print("Generating pulse survey data...")

survey_dates = [
    datetime(2025, 1, 15),
    datetime(2025, 4, 15),
    datetime(2025, 7, 15),
    datetime(2025, 10, 15)
]

pulse_surveys_data = []

for survey_num, survey_date in enumerate(survey_dates, 1):
    # Response rate (increases with engagement)
    for _, emp in employees_df.iterrows():
        # Response rate correlated with engagement
        response_prob = 0.5 + emp['base_engagement_level'] * 0.45

        if random.random() > response_prob:
            continue  # Employee didn't respond

        # Engagement dimension scores (1-5 scale)
        engagement_scores = []
        for dim in ENGAGEMENT_DIMENSIONS:
            # Base score from employee's engagement level
            score = emp['base_engagement_level'] * 4 + 1  # Map 0-1 to 1-5
            score += np.random.normal(0, 0.5)
            score = np.clip(score, 1, 5)
            engagement_scores.append(round(score, 1))

        # Wellbeing dimension scores (1-5 scale)
        wellbeing_scores = []
        for dim in WELLBEING_DIMENSIONS:
            # Base score from burnout risk (inverted)
            score = (100 - emp['burnout_risk_score']) / 100 * 4 + 1
            score += np.random.normal(0, 0.5)
            score = np.clip(score, 1, 5)
            wellbeing_scores.append(round(score, 1))

        # Overall satisfaction (1-5)
        overall_satisfaction = round(emp['base_engagement_level'] * 4 + 1 + np.random.normal(0, 0.3), 1)
        overall_satisfaction = np.clip(overall_satisfaction, 1, 5)

        # eNPS (0-10)
        enps_score = round(emp['base_engagement_level'] * 10 + np.random.normal(0, 1), 0)
        enps_score = int(np.clip(enps_score, 0, 10))

        # Likelihood to leave (1-5, inverted from engagement)
        likelihood_leave = round((1 - emp['base_engagement_level']) * 4 + 1 + np.random.normal(0, 0.5), 1)
        likelihood_leave = np.clip(likelihood_leave, 1, 5)

        survey_response = {
            'survey_id': f"Q{survey_num}_2025",
            'survey_date': survey_date.strftime('%Y-%m-%d'),
            'employee_id': emp['employee_id'],
            'department': emp['department'],
            'level': emp['level'],
            'tenure_months': emp['tenure_months'],
            'manager_effectiveness_score': emp['manager_effectiveness_score'],
        }

        # Add engagement dimensions
        for i, dim in enumerate(ENGAGEMENT_DIMENSIONS):
            survey_response[dim] = engagement_scores[i]

        # Add wellbeing dimensions
        for i, dim in enumerate(WELLBEING_DIMENSIONS):
            survey_response[dim] = wellbeing_scores[i]

        # Add overall metrics
        survey_response['overall_satisfaction'] = overall_satisfaction
        survey_response['enps_score'] = enps_score
        survey_response['likelihood_to_leave'] = likelihood_leave

        # Calculate composite scores
        survey_response['engagement_index'] = round(np.mean(engagement_scores), 2)
        survey_response['wellbeing_index'] = round(np.mean(wellbeing_scores), 2)

        pulse_surveys_data.append(survey_response)

pulse_surveys_df = pd.DataFrame(pulse_surveys_data)

# ============================================================================
# Generate Intervention Programs Data
# ============================================================================

print("Generating intervention programs data...")

interventions_data = []

# Intervention 1: Manager Training (Q2 2025)
# Target: Managers with low team engagement in Q1
q1_surveys = pulse_surveys_df[pulse_surveys_df['survey_id'] == 'Q1_2025']
low_engagement_managers = q1_surveys.groupby('department')['engagement_index'].mean()
low_engagement_depts = low_engagement_managers[low_engagement_managers < 3.5].index.tolist()

for dept in low_engagement_depts:
    interventions_data.append({
        'intervention_id': f"MGR_TRAIN_{dept}",
        'intervention_type': 'Manager Training',
        'department': dept,
        'start_date': '2025-05-01',
        'end_date': '2025-06-30',
        'participants_count': random.randint(3, 8),
        'cost': random.randint(5000, 15000),
        'description': '8-week manager effectiveness program'
    })

# Intervention 2: Flexible Work Policy (Q3 2025)
# Company-wide, focus on high burnout departments
high_burnout_depts = employees_df.groupby('department')['burnout_risk_score'].mean()
high_burnout_depts = high_burnout_depts[high_burnout_depts > 60].index.tolist()

for dept in high_burnout_depts:
    interventions_data.append({
        'intervention_id': f"FLEX_WORK_{dept}",
        'intervention_type': 'Flexible Work Policy',
        'department': dept,
        'start_date': '2025-07-01',
        'end_date': '2025-12-31',
        'participants_count': len(employees_df[employees_df['department'] == dept]),
        'cost': 0,  # Policy change, no direct cost
        'description': 'Remote work 3 days/week, core hours flexibility'
    })

# Intervention 3: Wellbeing Program (Q4 2025)
# Target entire company
interventions_data.append({
    'intervention_id': 'WELLBEING_ALL',
    'intervention_type': 'Wellbeing Program',
    'department': 'All',
    'start_date': '2025-10-01',
    'end_date': '2025-12-31',
    'participants_count': len(employees_df),
    'cost': 50000,
    'description': 'Mental health resources, meditation app, PTO encouragement'
})

interventions_df = pd.DataFrame(interventions_data)

# ============================================================================
# Generate Engagement Trend Data (Aggregate)
# ============================================================================

print("Generating engagement trends...")

trends_data = []

for survey_num, survey_date in enumerate(survey_dates, 1):
    survey_responses = pulse_surveys_df[pulse_surveys_df['survey_id'] == f"Q{survey_num}_2025"]

    # Overall metrics
    trends_data.append({
        'survey_quarter': f"Q{survey_num}_2025",
        'survey_date': survey_date.strftime('%Y-%m-%d'),
        'response_rate': round(len(survey_responses) / len(employees_df) * 100, 1),
        'avg_engagement_index': round(survey_responses['engagement_index'].mean(), 2),
        'avg_wellbeing_index': round(survey_responses['wellbeing_index'].mean(), 2),
        'avg_enps': round(survey_responses['enps_score'].mean(), 1),
        'promoters_pct': round((survey_responses['enps_score'] >= 9).sum() / len(survey_responses) * 100, 1),
        'passives_pct': round(((survey_responses['enps_score'] >= 7) & (survey_responses['enps_score'] <= 8)).sum() / len(survey_responses) * 100, 1),
        'detractors_pct': round((survey_responses['enps_score'] <= 6).sum() / len(survey_responses) * 100, 1),
        'highly_engaged_pct': round((survey_responses['engagement_index'] >= 4.0).sum() / len(survey_responses) * 100, 1),
        'at_risk_pct': round((survey_responses['engagement_index'] <= 2.5).sum() / len(survey_responses) * 100, 1),
        'high_burnout_risk_pct': round((survey_responses['wellbeing_index'] <= 2.5).sum() / len(survey_responses) * 100, 1)
    })

trends_df = pd.DataFrame(trends_data)

# ============================================================================
# Save all datasets
# ============================================================================

print("\nSaving datasets...")

import os
# Determine the correct path based on where we're running from
if os.path.exists('../data'):
    # Running from notebooks directory
    data_dir = '../data'
elif os.path.exists('07_Engagement_Wellbeing/data'):
    # Running from project root
    data_dir = '07_Engagement_Wellbeing/data'
else:
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    data_dir = 'data'

employees_df.to_csv(f'{data_dir}/employees.csv', index=False)
pulse_surveys_df.to_csv(f'{data_dir}/pulse_surveys.csv', index=False)
interventions_df.to_csv(f'{data_dir}/interventions.csv', index=False)
trends_df.to_csv(f'{data_dir}/engagement_trends.csv', index=False)

print(f"\n{'='*80}")
print("DATA GENERATION COMPLETE")
print(f"{'='*80}")
print(f"Generated {len(employees_df)} employee records")
print(f"Generated {len(pulse_surveys_df)} pulse survey responses")
print(f"Generated {len(interventions_df)} intervention programs")
print(f"Generated {len(trends_df)} quarterly trend records")
print(f"\nDatasets saved to {data_dir}/")
print(f"{'='*80}")

# Print summary statistics
print("\n📊 ENGAGEMENT SUMMARY")
print(f"{'='*80}")
latest_survey = pulse_surveys_df[pulse_surveys_df['survey_id'] == 'Q4_2025']
print(f"Average Engagement Index: {latest_survey['engagement_index'].mean():.2f}/5.0")
print(f"Average Wellbeing Index: {latest_survey['wellbeing_index'].mean():.2f}/5.0")
print(f"Average eNPS: {latest_survey['enps_score'].mean():.1f}/10")

print("\n⚠️ BURNOUT RISK")
print(f"{'='*80}")
print(f"High burnout risk (>70): {(employees_df['burnout_risk_score'] > 70).sum()} employees ({(employees_df['burnout_risk_score'] > 70).mean()*100:.1f}%)")
print(f"Moderate burnout risk (50-70): {((employees_df['burnout_risk_score'] >= 50) & (employees_df['burnout_risk_score'] <= 70)).sum()} employees")
print(f"Low burnout risk (<50): {(employees_df['burnout_risk_score'] < 50).sum()} employees")

print("\n💼 WORK HOURS")
print(f"{'='*80}")
print(f"Average weekly hours: {employees_df['avg_weekly_hours'].mean():.1f}")
print(f"Working >50 hours/week: {(employees_df['avg_weekly_hours'] > 50).sum()} employees ({(employees_df['avg_weekly_hours'] > 50).mean()*100:.1f}%)")
print(f"Average PTO usage: {employees_df['pto_usage_rate'].mean()*100:.1f}%")

print("\n🚪 ATTRITION")
print(f"{'='*80}")
print(f"Overall attrition rate: {employees_df['has_left'].mean()*100:.1f}%")
print(f"Attrition among highly disengaged (<30%): {employees_df[employees_df['base_engagement_level'] < 0.3]['has_left'].mean()*100:.1f}%")
print(f"Attrition among highly engaged (>70%): {employees_df[employees_df['base_engagement_level'] > 0.7]['has_left'].mean()*100:.1f}%")

print(f"\n{'='*80}")
print("✅ All datasets ready for analysis!")
print(f"{'='*80}\n")
