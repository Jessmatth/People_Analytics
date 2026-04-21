"""
Generate synthetic data for AI Adoption & Benefits Realization analysis
Domain 10: AI tool adoption, productivity impact, and adoption barriers

Creates realistic AI usage patterns and productivity metrics.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
NUM_EMPLOYEES = 450
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 'Operations', 'HR', 'Finance']
LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP']
WEEKS_TRACKED = 12  # 3 months of data

# AI Tools
AI_TOOLS = [
    'Coding Assistant (Copilot)',
    'Writing Assistant (ChatGPT)',
    'Meeting Summarizer',
    'Data Analysis Tool',
    'Design Assistant'
]

print("Generating AI adoption and usage data...")

# ============================================================================
# Generate Employee Base Data
# ============================================================================

employees_data = []
employee_id = 1000

for i in range(NUM_EMPLOYEES):
    dept = random.choice(DEPARTMENTS)
    level = random.choice(LEVELS)

    # Tenure and demographics
    tenure_months = int(np.random.exponential(24) + 1)
    tenure_months = min(tenure_months, 120)

    age_group = random.choices(
        ['Gen Z (18-27)', 'Millennial (28-43)', 'Gen X (44-59)', 'Boomer (60+)'],
        weights=[0.15, 0.50, 0.30, 0.05]
    )[0]

    # Tech comfort (influences adoption)
    if age_group == 'Gen Z (18-27)':
        tech_comfort = np.random.beta(6, 2) * 5  # Higher comfort
    elif age_group == 'Millennial (28-43)':
        tech_comfort = np.random.beta(5, 3) * 5
    else:
        tech_comfort = np.random.beta(4, 4) * 5

    tech_comfort = np.clip(tech_comfort, 1, 5)

    # Manager effectiveness
    manager_support = np.random.beta(5, 2)  # 0-1 scale

    # Training completion
    completed_training = random.random() < 0.55  # 55% completed training

    # Adoption status (influenced by tech comfort, manager support, training)
    # Adjusted formula to create more realistic adoption rates (~70% overall)
    adoption_score = (tech_comfort / 5) * 0.35 + manager_support * 0.35 + (0.15 if completed_training else 0)
    adoption_score += np.random.normal(0, 0.15)  # Increased variance
    adoption_score = np.clip(adoption_score, 0, 1)

    # Classify adoption level (adjusted thresholds for realistic distribution)
    if adoption_score > 0.75:
        adoption_level = 'Power User'
        weekly_usage_hours = np.random.uniform(8, 15)
    elif adoption_score > 0.55:
        adoption_level = 'Casual User'
        weekly_usage_hours = np.random.uniform(2, 8)
    elif adoption_score > 0.35:
        adoption_level = 'Minimal User'
        weekly_usage_hours = np.random.uniform(0.5, 2)
    else:
        adoption_level = 'Non-Adopter'
        weekly_usage_hours = 0

    # Performance rating
    performance_rating = np.random.beta(5, 2) * 4 + 1
    performance_rating = np.clip(performance_rating, 1, 5)

    # Productivity impact (correlated with adoption)
    if adoption_level == 'Power User':
        time_saved_hours_per_week = np.random.uniform(5, 10)
        productivity_improvement = np.random.uniform(0.25, 0.40)  # 25-40%
    elif adoption_level == 'Casual User':
        time_saved_hours_per_week = np.random.uniform(2, 5)
        productivity_improvement = np.random.uniform(0.10, 0.25)  # 10-25%
    elif adoption_level == 'Minimal User':
        time_saved_hours_per_week = np.random.uniform(0.5, 2)
        productivity_improvement = np.random.uniform(0.02, 0.10)  # 2-10%
    else:
        time_saved_hours_per_week = 0
        productivity_improvement = 0

    # Barriers (for non/low adopters)
    barriers = []
    if adoption_level in ['Non-Adopter', 'Minimal User']:
        if tech_comfort < 3:
            barriers.append('Low tech comfort')
        if not completed_training:
            barriers.append('No training')
        if manager_support < 0.5:
            barriers.append('Manager not supportive')
        if random.random() < 0.3:
            barriers.append('No clear use cases')
        if random.random() < 0.2:
            barriers.append('Security concerns')

    employees_data.append({
        'employee_id': employee_id,
        'department': dept,
        'level': level,
        'tenure_months': tenure_months,
        'age_group': age_group,
        'tech_comfort_score': round(tech_comfort, 1),
        'manager_ai_support': round(manager_support, 2),
        'completed_ai_training': completed_training,
        'adoption_level': adoption_level,
        'weekly_usage_hours': round(weekly_usage_hours, 1),
        'time_saved_hours_per_week': round(time_saved_hours_per_week, 1),
        'productivity_improvement_pct': round(productivity_improvement * 100, 1),
        'performance_rating': round(performance_rating, 2),
        'primary_barriers': '; '.join(barriers) if barriers else 'None'
    })

    employee_id += 1

employees_df = pd.DataFrame(employees_data)

# ============================================================================
# Generate Weekly Usage Data (time series)
# ============================================================================

print("Generating weekly usage time series...")

start_date = datetime(2024, 10, 1)
weekly_usage_data = []

for week in range(WEEKS_TRACKED):
    week_start = start_date + timedelta(weeks=week)

    for _, emp in employees_df.iterrows():
        # Usage grows over time for most users
        growth_factor = 1 + (week / WEEKS_TRACKED) * 0.3  # 30% growth over 12 weeks

        if emp['adoption_level'] == 'Power User':
            hours = emp['weekly_usage_hours'] * growth_factor * np.random.uniform(0.8, 1.2)
        elif emp['adoption_level'] == 'Casual User':
            hours = emp['weekly_usage_hours'] * growth_factor * np.random.uniform(0.7, 1.3)
        elif emp['adoption_level'] == 'Minimal User':
            hours = emp['weekly_usage_hours'] * np.random.uniform(0.5, 1.5)
        else:
            # Non-adopters rarely try (only 10% of the time)
            hours = np.random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5])

        weekly_usage_data.append({
            'employee_id': emp['employee_id'],
            'week_start_date': week_start.strftime('%Y-%m-%d'),
            'week_number': week + 1,
            'hours_used': round(hours, 1),
            'adoption_level': emp['adoption_level']
        })

weekly_usage_df = pd.DataFrame(weekly_usage_data)

# ============================================================================
# Generate AI Tool-Specific Usage
# ============================================================================

print("Generating tool-specific usage...")

tool_usage_data = []

for _, emp in employees_df.iterrows():
    if emp['adoption_level'] != 'Non-Adopter':
        # Determine which tools this employee uses
        dept = emp['department']

        # Department-specific tool preferences
        if dept == 'Engineering':
            tools = ['Coding Assistant (Copilot)', 'Data Analysis Tool']
        elif dept in ['Product', 'Marketing']:
            tools = ['Writing Assistant (ChatGPT)', 'Design Assistant', 'Data Analysis Tool']
        elif dept == 'Sales':
            tools = ['Writing Assistant (ChatGPT)', 'Meeting Summarizer']
        elif dept == 'Customer Success':
            tools = ['Writing Assistant (ChatGPT)', 'Meeting Summarizer']
        else:
            tools = random.sample(AI_TOOLS, random.randint(1, 3))

        for tool in tools:
            # Usage frequency
            if emp['adoption_level'] == 'Power User':
                weekly_sessions = int(np.random.uniform(10, 30))
                satisfaction = np.random.beta(6, 2) * 5
            elif emp['adoption_level'] == 'Casual User':
                weekly_sessions = int(np.random.uniform(3, 10))
                satisfaction = np.random.beta(5, 3) * 5
            else:
                weekly_sessions = int(np.random.uniform(1, 3))
                satisfaction = np.random.beta(4, 4) * 5

            tool_usage_data.append({
                'employee_id': emp['employee_id'],
                'ai_tool': tool,
                'weekly_sessions': weekly_sessions,
                'satisfaction_score': round(np.clip(satisfaction, 1, 5), 1),
                'primary_use_case': random.choice(['Content creation', 'Code generation', 'Analysis', 'Summarization', 'Brainstorming'])
            })

tool_usage_df = pd.DataFrame(tool_usage_data)

# ============================================================================
# Generate Training and Intervention Data
# ============================================================================

print("Generating training and intervention data...")

training_programs = [
    {'program_name': 'AI Fundamentals', 'duration_hours': 2, 'completion_rate': 0.65, 'avg_satisfaction': 4.2},
    {'program_name': 'Advanced Prompting', 'duration_hours': 4, 'completion_rate': 0.45, 'avg_satisfaction': 4.5},
    {'program_name': 'AI for Coding', 'duration_hours': 3, 'completion_rate': 0.55, 'avg_satisfaction': 4.7},
    {'program_name': 'AI Ethics & Responsible Use', 'duration_hours': 1, 'completion_rate': 0.70, 'avg_satisfaction': 3.9},
]

training_df = pd.DataFrame(training_programs)

# ============================================================================
# Generate Adoption Trend Data (Aggregated)
# ============================================================================

print("Generating adoption trends...")

adoption_trends = []

for week in range(WEEKS_TRACKED):
    week_data = weekly_usage_df[weekly_usage_df['week_number'] == week + 1]

    total_users = len(week_data)
    active_users = len(week_data[week_data['hours_used'] > 0])
    adoption_rate = (active_users / total_users * 100) if total_users > 0 else 0

    avg_hours = week_data['hours_used'].mean()
    total_hours = week_data['hours_used'].sum()

    adoption_trends.append({
        'week_number': week + 1,
        'week_start_date': (start_date + timedelta(weeks=week)).strftime('%Y-%m-%d'),
        'active_users': active_users,
        'total_users': total_users,
        'adoption_rate_pct': round(adoption_rate, 1),
        'avg_hours_per_user': round(avg_hours, 1),
        'total_hours_used': round(total_hours, 1)
    })

trends_df = pd.DataFrame(adoption_trends)

# ============================================================================
# Save all datasets
# ============================================================================

print("\nSaving datasets...")

import os
if os.path.exists('../data'):
    data_dir = '../data'
elif os.path.exists('10_AI_Adoption/data'):
    data_dir = '10_AI_Adoption/data'
else:
    os.makedirs('data', exist_ok=True)
    data_dir = 'data'

employees_df.to_csv(f'{data_dir}/ai_adoption_employees.csv', index=False)
weekly_usage_df.to_csv(f'{data_dir}/weekly_usage.csv', index=False)
tool_usage_df.to_csv(f'{data_dir}/tool_specific_usage.csv', index=False)
training_df.to_csv(f'{data_dir}/training_programs.csv', index=False)
trends_df.to_csv(f'{data_dir}/adoption_trends.csv', index=False)

print(f"\n{'='*80}")
print("DATA GENERATION COMPLETE")
print(f"{'='*80}")
print(f"Generated {len(employees_df)} employee AI adoption profiles")
print(f"Generated {len(weekly_usage_df)} weekly usage records")
print(f"Generated {len(tool_usage_df)} tool-specific usage records")
print(f"Generated {len(training_df)} training programs")
print(f"Generated {len(trends_df)} weeks of adoption trends")
print(f"\nDatasets saved to {data_dir}/")
print(f"{'='*80}")

# Print summary statistics
print("\n🤖 AI ADOPTION SUMMARY")
print(f"{'='*80}")

adoption_counts = employees_df['adoption_level'].value_counts()
for level in ['Power User', 'Casual User', 'Minimal User', 'Non-Adopter']:
    if level in adoption_counts.index:
        count = adoption_counts[level]
        pct = count / len(employees_df) * 100
        print(f"  {level:15s}: {count:3d} ({pct:5.1f}%)")

overall_adoption = ((len(employees_df) - adoption_counts.get('Non-Adopter', 0)) / len(employees_df) * 100)
print(f"\nOverall adoption rate: {overall_adoption:.1f}%")

print("\n⏱️ PRODUCTIVITY IMPACT")
print(f"{'='*80}")
avg_time_saved = employees_df[employees_df['adoption_level'] != 'Non-Adopter']['time_saved_hours_per_week'].mean()
total_time_saved = employees_df['time_saved_hours_per_week'].sum()
avg_productivity = employees_df[employees_df['adoption_level'] != 'Non-Adopter']['productivity_improvement_pct'].mean()

print(f"Average time saved (adopters): {avg_time_saved:.1f} hours/week")
print(f"Total organizational time saved: {total_time_saved:.0f} hours/week")
print(f"Average productivity improvement: {avg_productivity:.1f}%")

print("\n🚧 ADOPTION BARRIERS")
print(f"{'='*80}")
all_barriers = []
for barriers_str in employees_df['primary_barriers']:
    if barriers_str and barriers_str != 'None':
        all_barriers.extend([b.strip() for b in barriers_str.split(';')])

if all_barriers:
    barrier_counts = pd.Series(all_barriers).value_counts()
    for barrier, count in barrier_counts.head(5).items():
        print(f"  • {barrier}: {count} employees")

print("\n📈 GROWTH TREND")
print(f"{'='*80}")
week_1_adoption = trends_df[trends_df['week_number'] == 1]['adoption_rate_pct'].values[0]
week_12_adoption = trends_df[trends_df['week_number'] == 12]['adoption_rate_pct'].values[0]
growth = week_12_adoption - week_1_adoption

print(f"Week 1 adoption:  {week_1_adoption:.1f}%")
print(f"Week 12 adoption: {week_12_adoption:.1f}%")
print(f"Growth:           {growth:+.1f} percentage points")

print(f"\n{'='*80}")
print("✅ All datasets ready for analysis!")
print(f"{'='*80}\n")
