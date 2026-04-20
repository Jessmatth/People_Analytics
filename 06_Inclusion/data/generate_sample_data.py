"""
Generate synthetic data for Inclusion analysis
Domain 6: Inclusion - Equity in hiring, promotion, pay, and retention

Creates realistic datasets with demographic diversity and systematic inequities
to demonstrate inclusion analysis techniques.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
NUM_EMPLOYEES = 600
NUM_CANDIDATES = 2000
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 'Operations', 'HR', 'Finance']
LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP', 'C-Suite']
LOCATIONS = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Remote', 'Denver', 'Boston']

# Demographic distributions (approximating US tech industry)
GENDER_DIST = {'Female': 0.35, 'Male': 0.62, 'Non-Binary': 0.03}
RACE_DIST = {
    'White': 0.52,
    'Asian': 0.30,
    'Hispanic/Latino': 0.08,
    'Black': 0.06,
    'Two or More Races': 0.03,
    'Native American': 0.01
}
LGBTQ_RATE = 0.10
DISABILITY_RATE = 0.08

def assign_demographic(dist):
    """Randomly assign a demographic based on distribution"""
    return random.choices(list(dist.keys()), weights=list(dist.values()))[0]

def introduce_bias(base_rate, demographic, attribute, bias_map):
    """Apply systematic bias to outcomes based on demographic"""
    multiplier = bias_map.get((demographic, attribute), 1.0)
    return base_rate * multiplier

# Bias patterns (multipliers applied to base rates)
# Values < 1.0 = disadvantage, values > 1.0 = advantage

HIRING_BIAS = {
    # Gender bias in technical roles
    ('Female', 'screen_rate'): 0.85,
    ('Female', 'interview_rate'): 0.90,
    ('Female', 'offer_rate'): 0.92,
    ('Male', 'screen_rate'): 1.05,
    ('Male', 'interview_rate'): 1.05,

    # Race bias in hiring
    ('Black', 'screen_rate'): 0.80,
    ('Black', 'interview_rate'): 0.85,
    ('Hispanic/Latino', 'screen_rate'): 0.85,
    ('Asian', 'interview_rate'): 1.05,
    ('White', 'offer_rate'): 1.08,
}

PROMOTION_BIAS = {
    # Gender promotion gap
    ('Female', 'promotion_rate'): 0.80,
    ('Non-Binary', 'promotion_rate'): 0.75,
    ('Male', 'promotion_rate'): 1.10,

    # Race promotion gap
    ('Black', 'promotion_rate'): 0.70,
    ('Hispanic/Latino', 'promotion_rate'): 0.75,
    ('Asian', 'promotion_rate'): 0.95,
    ('White', 'promotion_rate'): 1.15,

    # Intersectional effects (compounded disadvantage)
    ('Female-Black', 'promotion_rate'): 0.65,
    ('Female-Hispanic/Latino', 'promotion_rate'): 0.68,
}

PAY_BIAS = {
    # Gender pay gap (after controlling for role/level)
    ('Female', 'base_salary'): 0.95,
    ('Female', 'bonus_pct'): 0.90,
    ('Non-Binary', 'base_salary'): 0.93,

    # Race pay gap
    ('Black', 'base_salary'): 0.92,
    ('Hispanic/Latino', 'base_salary'): 0.93,
    ('Asian', 'base_salary'): 0.98,
    ('White', 'base_salary'): 1.05,

    # Intersectional pay gaps
    ('Female-Black', 'base_salary'): 0.88,
    ('Female-Hispanic/Latino', 'base_salary'): 0.89,
}

ATTRITION_BIAS = {
    # Underrepresented groups leave at higher rates
    ('Female', 'attrition_risk'): 1.25,
    ('Black', 'attrition_risk'): 1.40,
    ('Hispanic/Latino', 'attrition_risk'): 1.30,
    ('LGBTQ+', 'attrition_risk'): 1.35,
    ('Disability', 'attrition_risk'): 1.20,

    # Intersectional attrition
    ('Female-Black', 'attrition_risk'): 1.55,
    ('Female-Hispanic/Latino', 'attrition_risk'): 1.50,
}

# ============================================================================
# 1. Generate Employee Data
# ============================================================================

print("Generating employee data...")

employees = []
for i in range(NUM_EMPLOYEES):
    gender = assign_demographic(GENDER_DIST)
    race = assign_demographic(RACE_DIST)
    is_lgbtq = random.random() < LGBTQ_RATE
    has_disability = random.random() < DISABILITY_RATE

    # Intersectional identity
    intersectional_id = f"{gender}-{race}"

    # Tenure (more senior = longer tenure)
    tenure_years = random.uniform(0.5, 12)

    # Level (biased by demographics - underrepresented groups more likely at lower levels)
    level_weights = [0.15, 0.20, 0.25, 0.18, 0.10, 0.06, 0.03, 0.02, 0.008, 0.002]

    # Apply representation bias (underrepresented less likely at senior levels)
    if gender == 'Female' or race in ['Black', 'Hispanic/Latino']:
        # Shift probability toward lower levels
        level_weights = [0.18, 0.24, 0.26, 0.18, 0.08, 0.04, 0.015, 0.01, 0.003, 0.001]
    if gender == 'Male' and race == 'White':
        # Shift probability toward higher levels
        level_weights = [0.12, 0.16, 0.22, 0.20, 0.12, 0.08, 0.05, 0.03, 0.015, 0.005]

    level = random.choices(LEVELS, weights=level_weights)[0]
    level_num = LEVELS.index(level)

    # Base salary by level
    base_salaries = {
        'IC1': 85000, 'IC2': 110000, 'IC3': 140000, 'IC4': 175000, 'IC5': 210000,
        'Manager': 160000, 'Senior Manager': 195000, 'Director': 230000,
        'VP': 290000, 'C-Suite': 380000
    }
    base_salary = base_salaries[level] * random.uniform(0.90, 1.15)

    # Apply pay bias
    gender_multiplier = PAY_BIAS.get((gender, 'base_salary'), 1.0)
    race_multiplier = PAY_BIAS.get((race, 'base_salary'), 1.0)
    intersect_multiplier = PAY_BIAS.get((intersectional_id, 'base_salary'), 1.0)

    final_multiplier = (gender_multiplier + race_multiplier + intersect_multiplier) / 3
    base_salary = base_salary * final_multiplier

    # Performance rating (slightly biased)
    base_performance = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.15, 0.50, 0.25, 0.05])[0]

    # Bonus (% of salary, biased)
    bonus_pct_base = {
        'IC1': 0.10, 'IC2': 0.12, 'IC3': 0.15, 'IC4': 0.18, 'IC5': 0.20,
        'Manager': 0.20, 'Senior Manager': 0.25, 'Director': 0.30,
        'VP': 0.40, 'C-Suite': 0.60
    }[level]

    bonus_multiplier = PAY_BIAS.get((gender, 'bonus_pct'), 1.0)
    bonus_pct = bonus_pct_base * bonus_multiplier * base_performance / 3
    bonus_amount = base_salary * bonus_pct

    # Compa-ratio (pay relative to market midpoint)
    compa_ratio = base_salary / base_salaries[level]

    # Belonging score (biased lower for underrepresented)
    belonging_base = random.uniform(3.0, 5.0)
    if gender == 'Female':
        belonging_base *= 0.90
    if race in ['Black', 'Hispanic/Latino']:
        belonging_base *= 0.85
    if is_lgbtq:
        belonging_base *= 0.88
    if has_disability:
        belonging_base *= 0.87

    belonging_score = max(1.0, min(5.0, belonging_base))

    # Attrition risk
    base_attrition = 0.12  # 12% annual attrition
    attrition_multiplier = 1.0
    if gender == 'Female':
        attrition_multiplier *= ATTRITION_BIAS.get((gender, 'attrition_risk'), 1.0)
    if race in ['Black', 'Hispanic/Latino']:
        attrition_multiplier *= ATTRITION_BIAS.get((race, 'attrition_risk'), 1.0)
    if is_lgbtq:
        attrition_multiplier *= ATTRITION_BIAS.get(('LGBTQ+', 'attrition_risk'), 1.0)
    if has_disability:
        attrition_multiplier *= ATTRITION_BIAS.get(('Disability', 'attrition_risk'), 1.0)

    # Check intersectional attrition
    intersect_attrition = ATTRITION_BIAS.get((intersectional_id, 'attrition_risk'), 1.0)
    if intersect_attrition > 1.0:
        attrition_multiplier = max(attrition_multiplier, intersect_attrition)

    attrition_risk = base_attrition * attrition_multiplier
    has_left = random.random() < attrition_risk

    employees.append({
        'employee_id': f'EMP{i+1:04d}',
        'gender': gender,
        'race': race,
        'is_lgbtq': is_lgbtq,
        'has_disability': has_disability,
        'intersectional_id': intersectional_id,
        'level': level,
        'level_num': level_num,
        'department': random.choice(DEPARTMENTS),
        'location': random.choice(LOCATIONS),
        'tenure_years': round(tenure_years, 1),
        'base_salary': round(base_salary, 0),
        'bonus_amount': round(bonus_amount, 0),
        'bonus_pct': round(bonus_pct, 3),
        'total_comp': round(base_salary + bonus_amount, 0),
        'compa_ratio': round(compa_ratio, 3),
        'performance_rating': base_performance,
        'belonging_score': round(belonging_score, 2),
        'has_left': has_left,
        'attrition_risk': round(attrition_risk, 3)
    })

employees_df = pd.DataFrame(employees)

# ============================================================================
# 2. Generate Hiring Funnel Data
# ============================================================================

print("Generating hiring funnel data...")

hiring_funnel = []

for i in range(NUM_CANDIDATES):
    gender = assign_demographic(GENDER_DIST)
    race = assign_demographic(RACE_DIST)
    is_lgbtq = random.random() < LGBTQ_RATE
    has_disability = random.random() < DISABILITY_RATE
    intersectional_id = f"{gender}-{race}"

    # Stage 1: Applied
    applied = True

    # Stage 2: Screened (resume review)
    base_screen_rate = 0.35
    screen_multiplier = 1.0
    screen_multiplier *= HIRING_BIAS.get((gender, 'screen_rate'), 1.0)
    screen_multiplier *= HIRING_BIAS.get((race, 'screen_rate'), 1.0)
    passed_screen = random.random() < (base_screen_rate * screen_multiplier)

    # Stage 3: Interviewed
    passed_interview = False
    if passed_screen:
        base_interview_rate = 0.60
        interview_multiplier = 1.0
        interview_multiplier *= HIRING_BIAS.get((gender, 'interview_rate'), 1.0)
        interview_multiplier *= HIRING_BIAS.get((race, 'interview_rate'), 1.0)
        passed_interview = random.random() < (base_interview_rate * interview_multiplier)

    # Stage 4: Offered
    received_offer = False
    if passed_interview:
        base_offer_rate = 0.45
        offer_multiplier = 1.0
        offer_multiplier *= HIRING_BIAS.get((gender, 'offer_rate'), 1.0)
        offer_multiplier *= HIRING_BIAS.get((race, 'offer_rate'), 1.0)
        received_offer = random.random() < (base_offer_rate * offer_multiplier)

    # Stage 5: Accepted
    accepted_offer = False
    if received_offer:
        # Underrepresented candidates more likely to decline (may sense non-inclusive culture)
        base_accept_rate = 0.78
        if gender == 'Female':
            base_accept_rate *= 0.92
        if race in ['Black', 'Hispanic/Latino']:
            base_accept_rate *= 0.90

        accepted_offer = random.random() < base_accept_rate

    # Time to decision (days)
    time_to_decision = None
    if received_offer:
        time_to_decision = random.randint(3, 21)
        # Underrepresented candidates take longer (more due diligence)
        if gender == 'Female' or race in ['Black', 'Hispanic/Latino']:
            time_to_decision += random.randint(2, 7)

    hiring_funnel.append({
        'candidate_id': f'CAND{i+1:05d}',
        'gender': gender,
        'race': race,
        'is_lgbtq': is_lgbtq,
        'has_disability': has_disability,
        'intersectional_id': intersectional_id,
        'role_applied': random.choice(['Software Engineer', 'Product Manager', 'Sales Rep',
                                       'Marketing Manager', 'Data Analyst', 'Designer']),
        'source': random.choice(['LinkedIn', 'Referral', 'Company Website', 'Recruiter',
                                'University', 'Job Board']),
        'applied': applied,
        'passed_screen': passed_screen,
        'passed_interview': passed_interview,
        'received_offer': received_offer,
        'accepted_offer': accepted_offer,
        'time_to_decision_days': time_to_decision
    })

hiring_funnel_df = pd.DataFrame(hiring_funnel)

# ============================================================================
# 3. Generate Promotion History Data
# ============================================================================

print("Generating promotion history data...")

promotions = []

# For each current employee, generate promotion history
for emp in employees:
    # Number of promotions based on tenure
    expected_promotions = int(emp['tenure_years'] / 2.5)  # Promote every ~2.5 years

    # Apply promotion bias
    gender_mult = PROMOTION_BIAS.get((emp['gender'], 'promotion_rate'), 1.0)
    race_mult = PROMOTION_BIAS.get((emp['race'], 'promotion_rate'), 1.0)
    intersect_mult = PROMOTION_BIAS.get((emp['intersectional_id'], 'promotion_rate'), 1.0)

    promotion_multiplier = min(gender_mult, race_mult, intersect_mult)  # Take most disadvantaged
    actual_promotions = int(expected_promotions * promotion_multiplier)

    if actual_promotions > 0:
        for p in range(actual_promotions):
            months_since_last = (emp['tenure_years'] * 12) / (actual_promotions + 1) * (p + 1)

            # Time to promotion (longer for underrepresented)
            time_penalty = 1.0
            if emp['gender'] == 'Female':
                time_penalty *= 1.15
            if emp['race'] in ['Black', 'Hispanic/Latino']:
                time_penalty *= 1.20

            months_since_last *= time_penalty

            promotions.append({
                'employee_id': emp['employee_id'],
                'gender': emp['gender'],
                'race': emp['race'],
                'is_lgbtq': emp['is_lgbtq'],
                'has_disability': emp['has_disability'],
                'promotion_number': p + 1,
                'months_since_last_promotion': round(months_since_last, 1),
                'promoted_to_level': LEVELS[min(p + 1, len(LEVELS) - 1)],
                'performance_at_promotion': random.choices([3, 4, 5], weights=[0.15, 0.60, 0.25])[0]
            })

promotions_df = pd.DataFrame(promotions)

# ============================================================================
# 4. Generate Engagement & Belonging Survey Data
# ============================================================================

print("Generating engagement survey data...")

engagement_surveys = []

for emp in employees:
    # 5-point Likert scale questions about inclusion

    # Base scores
    belonging = emp['belonging_score']

    # Psychological safety
    psych_safety_base = random.uniform(3.0, 5.0)
    if emp['gender'] == 'Female':
        psych_safety_base *= 0.92
    if emp['race'] in ['Black', 'Hispanic/Latino']:
        psych_safety_base *= 0.88
    psych_safety = max(1.0, min(5.0, psych_safety_base))

    # Authentic self
    authentic_base = random.uniform(3.0, 5.0)
    if emp['is_lgbtq']:
        authentic_base *= 0.85
    if emp['has_disability']:
        authentic_base *= 0.87
    authentic_self = max(1.0, min(5.0, authentic_base))

    # Career growth opportunities
    career_growth_base = random.uniform(3.0, 5.0)
    if emp['gender'] == 'Female':
        career_growth_base *= 0.88
    if emp['race'] in ['Black', 'Hispanic/Latino']:
        career_growth_base *= 0.82
    career_growth = max(1.0, min(5.0, career_growth_base))

    # Manager inclusion effectiveness
    manager_inclusion_base = random.uniform(3.0, 5.0)
    if emp['gender'] != 'Male' or emp['race'] != 'White':
        manager_inclusion_base *= 0.90
    manager_inclusion = max(1.0, min(5.0, manager_inclusion_base))

    engagement_surveys.append({
        'employee_id': emp['employee_id'],
        'gender': emp['gender'],
        'race': emp['race'],
        'is_lgbtq': emp['is_lgbtq'],
        'has_disability': emp['has_disability'],
        'intersectional_id': emp['intersectional_id'],
        'q_belonging': round(belonging, 1),
        'q_psychological_safety': round(psych_safety, 1),
        'q_authentic_self': round(authentic_self, 1),
        'q_career_growth_opportunities': round(career_growth, 1),
        'q_manager_inclusion': round(manager_inclusion, 1),
        'overall_inclusion_score': round((belonging + psych_safety + authentic_self +
                                         career_growth + manager_inclusion) / 5, 2)
    })

engagement_surveys_df = pd.DataFrame(engagement_surveys)

# ============================================================================
# 5. Generate Representation by Level Data (aggregated view)
# ============================================================================

print("Generating representation by level data...")

representation_data = []

for level in LEVELS:
    level_employees = employees_df[employees_df['level'] == level]
    total_at_level = len(level_employees)

    if total_at_level > 0:
        for gender in GENDER_DIST.keys():
            count = len(level_employees[level_employees['gender'] == gender])
            representation_data.append({
                'level': level,
                'demographic_dimension': 'Gender',
                'demographic_value': gender,
                'count': count,
                'percentage': round(count / total_at_level * 100, 1)
            })

        for race in RACE_DIST.keys():
            count = len(level_employees[level_employees['race'] == race])
            representation_data.append({
                'level': level,
                'demographic_dimension': 'Race',
                'demographic_value': race,
                'count': count,
                'percentage': round(count / total_at_level * 100, 1)
            })

representation_df = pd.DataFrame(representation_data)

# ============================================================================
# Save all datasets
# ============================================================================

print("\nSaving datasets...")

employees_df.to_csv('06_Inclusion/data/employees.csv', index=False)
hiring_funnel_df.to_csv('06_Inclusion/data/hiring_funnel.csv', index=False)
promotions_df.to_csv('06_Inclusion/data/promotions.csv', index=False)
engagement_surveys_df.to_csv('06_Inclusion/data/engagement_surveys.csv', index=False)
representation_df.to_csv('06_Inclusion/data/representation_by_level.csv', index=False)

print(f"\n{'='*80}")
print("DATA GENERATION COMPLETE")
print(f"{'='*80}")
print(f"Generated {len(employees_df)} employee records")
print(f"Generated {len(hiring_funnel_df)} hiring funnel records")
print(f"Generated {len(promotions_df)} promotion records")
print(f"Generated {len(engagement_surveys_df)} engagement survey responses")
print(f"Generated {len(representation_df)} representation data points")
print(f"\nDatasets saved to 06_Inclusion/data/")
print(f"{'='*80}")

# Print summary statistics
print("\n📊 DEMOGRAPHIC SUMMARY")
print(f"{'='*80}")
print("\nGender Distribution:")
print(employees_df['gender'].value_counts(normalize=True).round(3))
print("\nRace Distribution:")
print(employees_df['race'].value_counts(normalize=True).round(3))
print(f"\nLGBTQ+: {employees_df['is_lgbtq'].sum()} ({employees_df['is_lgbtq'].mean()*100:.1f}%)")
print(f"Has Disability: {employees_df['has_disability'].sum()} ({employees_df['has_disability'].mean()*100:.1f}%)")

print("\n📈 HIRING FUNNEL CONVERSION RATES")
print(f"{'='*80}")
print(f"Applied → Screened: {hiring_funnel_df['passed_screen'].mean()*100:.1f}%")
print(f"Screened → Interviewed: {hiring_funnel_df[hiring_funnel_df['passed_screen']]['passed_interview'].mean()*100:.1f}%")
print(f"Interviewed → Offered: {hiring_funnel_df[hiring_funnel_df['passed_interview']]['received_offer'].mean()*100:.1f}%")
print(f"Offered → Accepted: {hiring_funnel_df[hiring_funnel_df['received_offer']]['accepted_offer'].mean()*100:.1f}%")

print("\n💰 PAY EQUITY SNAPSHOT")
print(f"{'='*80}")
print(f"Average base salary: ${employees_df['base_salary'].mean():,.0f}")
print(f"Average total comp: ${employees_df['total_comp'].mean():,.0f}")
print(f"Average compa-ratio: {employees_df['compa_ratio'].mean():.3f}")

print("\n🚪 ATTRITION")
print(f"{'='*80}")
print(f"Overall attrition rate: {employees_df['has_left'].mean()*100:.1f}%")
print(f"Employees who left: {employees_df['has_left'].sum()}")

print(f"\n{'='*80}")
print("✅ All datasets ready for analysis!")
print(f"{'='*80}\n")
