"""
Generate synthetic data for Compensation Equity & Benchmarking analysis
Domain 8: Pay equity, market benchmarking, and total rewards optimization

Creates realistic compensation datasets with market data and equity scenarios.
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
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 'Operations', 'HR', 'Finance']
LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP']
LOCATIONS = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Remote']

# Demographic distributions
GENDER_DIST = {'Female': 0.35, 'Male': 0.62, 'Non-Binary': 0.03}
RACE_DIST = {
    'White': 0.52,
    'Asian': 0.30,
    'Hispanic/Latino': 0.08,
    'Black': 0.06,
    'Two or More Races': 0.03,
    'Native American': 0.01
}

# Base salary ranges by level (market midpoint in SF)
BASE_SALARY_RANGES = {
    'IC1': (70000, 90000),
    'IC2': (90000, 120000),
    'IC3': (120000, 160000),
    'IC4': (160000, 210000),
    'IC5': (210000, 280000),
    'Manager': (140000, 180000),
    'Senior Manager': (180000, 230000),
    'Director': (230000, 300000),
    'VP': (300000, 450000)
}

# Department multipliers (some departments pay more)
DEPT_PAY_MULTIPLIERS = {
    'Engineering': 1.1,
    'Product': 1.05,
    'Sales': 1.15,  # Higher base
    'Marketing': 1.0,
    'Customer Success': 0.95,
    'Operations': 0.98,
    'HR': 0.95,
    'Finance': 1.0
}

# Location cost-of-living multipliers
LOCATION_MULTIPLIERS = {
    'San Francisco': 1.3,
    'New York': 1.25,
    'Seattle': 1.15,
    'Austin': 1.05,
    'Remote': 1.0  # National average
}

# Pay equity bias patterns (systematic underpayment)
PAY_BIAS = {
    ('Female', 'base_salary'): 0.95,  # 5% gap
    ('Black', 'base_salary'): 0.93,  # 7% gap
    ('Hispanic/Latino', 'base_salary'): 0.96,  # 4% gap
    ('Female-Black', 'base_salary'): 0.90,  # 10% gap (intersectional)
}

def assign_demographic(dist):
    """Randomly assign a demographic based on distribution"""
    return random.choices(list(dist.keys()), weights=list(dist.values()))[0]

def apply_pay_bias(base_value, gender, race):
    """Apply systematic pay bias"""
    multiplier = 1.0

    # Apply gender bias
    gender_key = (gender, 'base_salary')
    if gender_key in PAY_BIAS:
        multiplier *= PAY_BIAS[gender_key]

    # Apply race bias
    race_key = (race, 'base_salary')
    if race_key in PAY_BIAS:
        multiplier *= PAY_BIAS[race_key]

    # Apply intersectional bias
    intersect_key = (f"{gender}-{race}", 'base_salary')
    if intersect_key in PAY_BIAS:
        multiplier = PAY_BIAS[intersect_key]  # Override with intersectional

    return base_value * multiplier

# ============================================================================
# Generate Employee Compensation Records
# ============================================================================

print("Generating employee compensation data...")

employees_data = []
employee_id = 1000

for i in range(NUM_EMPLOYEES):
    # Demographics
    gender = assign_demographic(GENDER_DIST)
    race = assign_demographic(RACE_DIST)

    # Job characteristics
    dept = random.choice(DEPARTMENTS)
    level = random.choice(LEVELS)
    location = random.choice(LOCATIONS)

    # Tenure and performance
    tenure_months = int(np.random.exponential(24) + 1)
    tenure_months = min(tenure_months, 120)  # Cap at 10 years
    tenure_years = tenure_months / 12

    performance_rating = np.random.beta(5, 2) * 4 + 1  # 1-5 scale, skewed high
    performance_rating = np.clip(performance_rating, 1.0, 5.0)

    # Base salary calculation
    level_min, level_max = BASE_SALARY_RANGES[level]
    base_salary = np.random.uniform(level_min, level_max)

    # Apply multipliers
    base_salary *= DEPT_PAY_MULTIPLIERS[dept]
    base_salary *= LOCATION_MULTIPLIERS[location]

    # Tenure adjustment (1% per year up to 10%)
    tenure_multiplier = 1 + min(tenure_years * 0.01, 0.10)
    base_salary *= tenure_multiplier

    # Performance adjustment (±10% based on rating)
    perf_multiplier = 0.90 + (performance_rating - 1) * 0.05  # 0.9 to 1.1
    base_salary *= perf_multiplier

    # Apply pay bias BEFORE adding random variation
    base_salary = apply_pay_bias(base_salary, gender, race)

    # Add random variation
    base_salary *= np.random.uniform(0.95, 1.05)
    base_salary = round(base_salary, 2)

    # Bonus calculation (percentage of base)
    if level in ['VP', 'Director', 'Senior Manager']:
        target_bonus_pct = 0.25  # 25% target
    elif level in ['Manager']:
        target_bonus_pct = 0.15  # 15% target
    else:
        target_bonus_pct = 0.10  # 10% target

    # Actual bonus tied to performance
    bonus_multiplier = (performance_rating - 3) * 0.5 + 1  # 0.5x to 1.5x target
    bonus_multiplier = max(0, bonus_multiplier)
    actual_bonus = base_salary * target_bonus_pct * bonus_multiplier
    actual_bonus = round(actual_bonus, 2)

    # Equity grants (RSUs - restricted stock units)
    if level in ['VP', 'Director']:
        equity_value = base_salary * np.random.uniform(0.4, 0.8)  # 40-80% of base
    elif level in ['Senior Manager', 'IC5']:
        equity_value = base_salary * np.random.uniform(0.2, 0.4)  # 20-40% of base
    elif level in ['Manager', 'IC4']:
        equity_value = base_salary * np.random.uniform(0.1, 0.2)  # 10-20% of base
    else:
        equity_value = base_salary * np.random.uniform(0, 0.1)  # 0-10% of base

    equity_value = round(equity_value, 2)

    # Benefits value (healthcare, 401k match, etc.)
    benefits_value = 15000  # Base benefits package
    if level in ['VP', 'Director', 'Senior Manager']:
        benefits_value += 5000  # Executive benefits
    benefits_value = round(benefits_value, 2)

    # Total compensation
    total_comp = base_salary + actual_bonus + equity_value + benefits_value

    # Market data (for benchmarking)
    market_50th = np.mean(BASE_SALARY_RANGES[level])
    market_50th *= DEPT_PAY_MULTIPLIERS[dept]
    market_50th *= LOCATION_MULTIPLIERS[location]

    market_25th = market_50th * 0.90
    market_75th = market_50th * 1.10

    # Compa-ratio (actual vs market midpoint)
    compa_ratio = base_salary / market_50th

    # Market percentile (where does this employee fall?)
    if base_salary < market_25th:
        market_percentile = 25 * (base_salary / market_25th)
    elif base_salary < market_50th:
        market_percentile = 25 + 25 * ((base_salary - market_25th) / (market_50th - market_25th))
    elif base_salary < market_75th:
        market_percentile = 50 + 25 * ((base_salary - market_50th) / (market_75th - market_50th))
    else:
        market_percentile = 75 + 25 * min((base_salary - market_75th) / (market_75th - market_50th), 1)

    market_percentile = np.clip(market_percentile, 1, 99)

    employees_data.append({
        'employee_id': employee_id,
        'gender': gender,
        'race': race,
        'department': dept,
        'level': level,
        'location': location,
        'tenure_months': tenure_months,
        'performance_rating': round(performance_rating, 2),
        'base_salary': base_salary,
        'target_bonus_pct': round(target_bonus_pct * 100, 1),
        'actual_bonus': actual_bonus,
        'equity_value_annual': equity_value,
        'benefits_value': benefits_value,
        'total_compensation': round(total_comp, 2),
        'market_25th': round(market_25th, 2),
        'market_50th': round(market_50th, 2),
        'market_75th': round(market_75th, 2),
        'market_percentile': round(market_percentile, 1),
        'compa_ratio': round(compa_ratio, 3)
    })

    employee_id += 1

employees_df = pd.DataFrame(employees_data)

# ============================================================================
# Generate Market Benchmark Data
# ============================================================================

print("Generating market benchmark data...")

market_data = []

for dept in DEPARTMENTS:
    for level in LEVELS:
        for location in LOCATIONS:
            # Base market data
            level_min, level_max = BASE_SALARY_RANGES[level]
            market_50th = np.mean([level_min, level_max])
            market_50th *= DEPT_PAY_MULTIPLIERS[dept]
            market_50th *= LOCATION_MULTIPLIERS[location]

            market_25th = market_50th * 0.90
            market_75th = market_50th * 1.10
            market_10th = market_50th * 0.80
            market_90th = market_50th * 1.20

            # Sample size (data sources)
            sample_size = random.randint(50, 300)

            market_data.append({
                'department': dept,
                'level': level,
                'location': location,
                'market_10th': round(market_10th, 2),
                'market_25th': round(market_25th, 2),
                'market_50th': round(market_50th, 2),
                'market_75th': round(market_75th, 2),
                'market_90th': round(market_90th, 2),
                'sample_size': sample_size,
                'data_source': 'Radford/Mercer/Payscale Composite',
                'data_date': '2024-06-30'
            })

market_df = pd.DataFrame(market_data)

# ============================================================================
# Generate Benefits Utilization Data
# ============================================================================

print("Generating benefits utilization data...")

benefits_programs = [
    {'program': 'Health Insurance (PPO)', 'annual_cost_per_ee': 12000, 'utilization_rate': 0.95, 'perceived_value': 4.5},
    {'program': 'Health Insurance (HDHP)', 'annual_cost_per_ee': 8000, 'utilization_rate': 0.30, 'perceived_value': 3.8},
    {'program': '401k Match (4%)', 'annual_cost_per_ee': 4000, 'utilization_rate': 0.85, 'perceived_value': 4.7},
    {'program': 'HSA Contribution', 'annual_cost_per_ee': 1500, 'utilization_rate': 0.30, 'perceived_value': 3.5},
    {'program': 'Commuter Benefits', 'annual_cost_per_ee': 1200, 'utilization_rate': 0.40, 'perceived_value': 3.2},
    {'program': 'Gym Membership', 'annual_cost_per_ee': 600, 'utilization_rate': 0.35, 'perceived_value': 3.0},
    {'program': 'Learning & Development', 'annual_cost_per_ee': 2000, 'utilization_rate': 0.45, 'perceived_value': 4.2},
    {'program': 'Mental Health Resources', 'annual_cost_per_ee': 1500, 'utilization_rate': 0.25, 'perceived_value': 4.0},
    {'program': 'Parental Leave', 'annual_cost_per_ee': 3000, 'utilization_rate': 0.08, 'perceived_value': 4.8},
    {'program': 'Life Insurance', 'annual_cost_per_ee': 400, 'utilization_rate': 1.0, 'perceived_value': 3.5},
]

benefits_df = pd.DataFrame(benefits_programs)

# Calculate cost-effectiveness
benefits_df['cost_per_participant'] = benefits_df['annual_cost_per_ee'] / benefits_df['utilization_rate']
benefits_df['value_per_dollar'] = benefits_df['perceived_value'] / (benefits_df['annual_cost_per_ee'] / 1000)

# ============================================================================
# Generate Pay Adjustment Scenarios
# ============================================================================

print("Generating pay adjustment scenarios...")

# Identify underpaid employees
employees_df['underpaid'] = employees_df['market_percentile'] < 40
employees_df['significantly_underpaid'] = employees_df['market_percentile'] < 25

# Calculate adjustment needed to reach market
employees_df['adjustment_to_50th'] = employees_df['market_50th'] - employees_df['base_salary']
employees_df['adjustment_pct'] = (employees_df['adjustment_to_50th'] / employees_df['base_salary'] * 100).round(1)

# Only positive adjustments
employees_df['adjustment_to_50th'] = employees_df['adjustment_to_50th'].apply(lambda x: max(0, x))
employees_df['adjustment_pct'] = employees_df['adjustment_pct'].apply(lambda x: max(0, x))

# ============================================================================
# Save all datasets
# ============================================================================

print("\nSaving datasets...")

import os
# Determine the correct path based on where we're running from
if os.path.exists('../data'):
    # Running from notebooks directory
    data_dir = '../data'
elif os.path.exists('08_Compensation_Equity/data'):
    # Running from project root
    data_dir = '08_Compensation_Equity/data'
else:
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    data_dir = 'data'

employees_df.to_csv(f'{data_dir}/employees_compensation.csv', index=False)
market_df.to_csv(f'{data_dir}/market_benchmark.csv', index=False)
benefits_df.to_csv(f'{data_dir}/benefits_programs.csv', index=False)

print(f"\n{'='*80}")
print("DATA GENERATION COMPLETE")
print(f"{'='*80}")
print(f"Generated {len(employees_df)} employee compensation records")
print(f"Generated {len(market_df)} market benchmark data points")
print(f"Generated {len(benefits_df)} benefits programs")
print(f"\nDatasets saved to {data_dir}/")
print(f"{'='*80}")

# Print summary statistics
print("\n💰 COMPENSATION SUMMARY")
print(f"{'='*80}")
print(f"Average base salary:     ${employees_df['base_salary'].mean():,.0f}")
print(f"Average total comp:      ${employees_df['total_compensation'].mean():,.0f}")
print(f"Median compa-ratio:      {employees_df['compa_ratio'].median():.3f}")
print(f"Average market percentile: {employees_df['market_percentile'].mean():.1f}")

print("\n📊 PAY EQUITY INDICATORS")
print(f"{'='*80}")
# Gender pay gaps
male_avg = employees_df[employees_df['gender'] == 'Male']['base_salary'].mean()
female_avg = employees_df[employees_df['gender'] == 'Female']['base_salary'].mean()
gender_gap = (male_avg - female_avg) / male_avg * 100

print(f"Raw gender pay gap: {gender_gap:.1f}%")
print(f"  Male average:   ${male_avg:,.0f}")
print(f"  Female average: ${female_avg:,.0f}")

# Race pay gaps
white_avg = employees_df[employees_df['race'] == 'White']['base_salary'].mean()
for race in ['Asian', 'Black', 'Hispanic/Latino']:
    race_avg = employees_df[employees_df['race'] == race]['base_salary'].mean()
    gap = (white_avg - race_avg) / white_avg * 100
    print(f"\n{race} vs White gap: {gap:.1f}%")
    print(f"  White average: ${white_avg:,.0f}")
    print(f"  {race} average: ${race_avg:,.0f}")

print("\n⚠️ MARKET COMPETITIVENESS")
print(f"{'='*80}")
underpaid_count = employees_df['underpaid'].sum()
sig_underpaid_count = employees_df['significantly_underpaid'].sum()
print(f"Employees below 40th percentile: {underpaid_count} ({underpaid_count/len(employees_df)*100:.1f}%)")
print(f"Employees below 25th percentile: {sig_underpaid_count} ({sig_underpaid_count/len(employees_df)*100:.1f}%)")
print(f"\nTotal adjustment needed to reach market 50th: ${employees_df['adjustment_to_50th'].sum():,.0f}")

print("\n💵 BENEFITS SUMMARY")
print(f"{'='*80}")
total_benefits_cost = benefits_df['annual_cost_per_ee'].sum()
print(f"Total benefits value per employee: ${total_benefits_cost:,.0f}")
print(f"Top 3 highest perceived value:")
top_benefits = benefits_df.nlargest(3, 'perceived_value')[['program', 'perceived_value', 'annual_cost_per_ee']]
for _, row in top_benefits.iterrows():
    print(f"  • {row['program']:30s}: {row['perceived_value']:.1f}/5.0 (${row['annual_cost_per_ee']:,.0f})")

print(f"\n{'='*80}")
print("✅ All datasets ready for analysis!")
print(f"{'='*80}\n")
