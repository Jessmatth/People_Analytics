"""
Generate Sample Data for Domain 5: Manager Effectiveness

This script creates realistic synthetic data for analyzing manager effectiveness,
including team retention, engagement, behaviors, and development outcomes.

Data Generated:
- managers.csv: 45 managers with effectiveness scores and attributes
- team_members.csv: 500 employees assigned to managers
- team_retention.csv: Rolling 12-month retention by team
- team_engagement.csv: Quarterly engagement surveys by team
- one_on_ones.csv: 1:1 meeting frequency and quality tracking
- manager_behaviors.csv: Leadership behaviors and activities
- team_performance.csv: Performance distribution by team
- promotions_from_team.csv: Promotion outcomes by manager
- manager_training.csv: Manager development program participation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Constants
NUM_MANAGERS = 45
NUM_EMPLOYEES = 500
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 3, 31)

# Departments and their typical manager counts
DEPARTMENTS = {
    'Engineering': 12,
    'Sales': 10,
    'Product': 6,
    'Customer Success': 7,
    'Marketing': 5,
    'Operations': 5
}

MANAGER_LEVELS = ['Manager', 'Senior Manager', 'Director']

# Manager archetypes (realistic distribution)
MANAGER_ARCHETYPES = {
    'Exceptional': 0.10,  # Top 10%
    'Strong': 0.20,       # Next 20%
    'Adequate': 0.40,     # Middle 40%
    'Struggling': 0.20,   # Next 20%
    'Ineffective': 0.10   # Bottom 10%
}

def generate_managers():
    """Generate manager data with realistic effectiveness distributions"""
    managers = []
    manager_id = 1

    for dept, count in DEPARTMENTS.items():
        for i in range(count):
            # Assign archetype based on distribution
            rand = random.random()
            if rand < 0.10:
                archetype = 'Exceptional'
                effectiveness_base = random.uniform(9.0, 10.0)
            elif rand < 0.30:
                archetype = 'Strong'
                effectiveness_base = random.uniform(7.0, 8.9)
            elif rand < 0.70:
                archetype = 'Adequate'
                effectiveness_base = random.uniform(5.0, 6.9)
            elif rand < 0.90:
                archetype = 'Struggling'
                effectiveness_base = random.uniform(3.0, 4.9)
            else:
                archetype = 'Ineffective'
                effectiveness_base = random.uniform(1.0, 2.9)

            # Manager attributes
            tenure_years = random.uniform(0.5, 8.0)
            is_new_manager = tenure_years < 1.5

            # Level based on tenure (roughly)
            if tenure_years < 2:
                level = 'Manager'
            elif tenure_years < 5:
                level = random.choice(['Manager', 'Senior Manager'])
            else:
                level = random.choice(['Senior Manager', 'Director'])

            # Span of control (5-9 optimal, some outliers)
            if archetype in ['Exceptional', 'Strong']:
                span = random.randint(5, 9)
            elif archetype == 'Adequate':
                span = random.randint(4, 11)
            else:
                span = random.choice([3, 4, 10, 11, 12])  # Too few or too many

            managers.append({
                'manager_id': f'MGR{manager_id:03d}',
                'name': f'{random.choice(["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn"])} {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"])}',
                'department': dept,
                'level': level,
                'archetype': archetype,
                'effectiveness_score': round(effectiveness_base, 1),
                'tenure_years': round(tenure_years, 1),
                'is_new_manager': is_new_manager,
                'span_of_control': span,
                'reports_to': f'MGR{random.randint(1, max(1, manager_id-5)):03d}' if manager_id > 5 else None
            })
            manager_id += 1

    return pd.DataFrame(managers)

def generate_team_members(managers_df):
    """Generate employee data assigned to managers"""
    team_members = []
    employee_id = 1

    for _, manager in managers_df.iterrows():
        num_reports = manager['span_of_control']

        for i in range(num_reports):
            # Tenure influenced by manager effectiveness (better managers retain longer)
            if manager['archetype'] in ['Exceptional', 'Strong']:
                tenure_years = random.uniform(0.3, 6.0)
            elif manager['archetype'] == 'Adequate':
                tenure_years = random.uniform(0.3, 4.0)
            else:
                tenure_years = random.uniform(0.3, 2.5)  # Higher turnover

            # Performance rating (better managers develop better performers)
            if manager['archetype'] in ['Exceptional', 'Strong']:
                performance = random.choices([1, 2, 3, 4, 5], weights=[3, 7, 25, 40, 25])[0]
            elif manager['archetype'] == 'Adequate':
                performance = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 50, 25, 5])[0]
            else:
                performance = random.choices([1, 2, 3, 4, 5], weights=[15, 25, 40, 15, 5])[0]

            # Engagement influenced by manager
            if manager['archetype'] in ['Exceptional', 'Strong']:
                engagement = random.uniform(7.5, 10.0)
            elif manager['archetype'] == 'Adequate':
                engagement = random.uniform(5.5, 7.5)
            else:
                engagement = random.uniform(2.0, 6.0)

            team_members.append({
                'employee_id': f'EMP{employee_id:04d}',
                'manager_id': manager['manager_id'],
                'department': manager['department'],
                'tenure_years': round(tenure_years, 1),
                'performance_rating': performance,
                'engagement_score': round(engagement, 1),
                'is_high_performer': performance >= 4,
                'promotion_eligible': tenure_years >= 1.5 and performance >= 4
            })
            employee_id += 1

    return pd.DataFrame(team_members)

def generate_team_retention(managers_df):
    """Generate team-level retention metrics over time"""
    retention_data = []

    for _, manager in managers_df.iterrows():
        # Generate quarterly retention rates
        for quarter in pd.date_range(start='2023-Q1', end='2026-Q1', freq='QE'):
            # Retention varies by manager archetype
            if manager['archetype'] == 'Exceptional':
                retention_rate = random.uniform(0.92, 0.98)
                voluntary_attrition = random.uniform(0.02, 0.08)
            elif manager['archetype'] == 'Strong':
                retention_rate = random.uniform(0.86, 0.94)
                voluntary_attrition = random.uniform(0.06, 0.14)
            elif manager['archetype'] == 'Adequate':
                retention_rate = random.uniform(0.78, 0.88)
                voluntary_attrition = random.uniform(0.12, 0.22)
            elif manager['archetype'] == 'Struggling':
                retention_rate = random.uniform(0.68, 0.80)
                voluntary_attrition = random.uniform(0.20, 0.32)
            else:  # Ineffective
                retention_rate = random.uniform(0.50, 0.70)
                voluntary_attrition = random.uniform(0.30, 0.50)

            regrettable_attrition = voluntary_attrition * random.uniform(0.4, 0.7)

            retention_data.append({
                'manager_id': manager['manager_id'],
                'department': manager['department'],
                'quarter': quarter.strftime('%Y-Q%q'),
                'retention_rate': round(retention_rate, 3),
                'voluntary_attrition_rate': round(voluntary_attrition, 3),
                'regrettable_attrition_rate': round(regrettable_attrition, 3),
                'team_size': manager['span_of_control']
            })

    return pd.DataFrame(retention_data)

def generate_team_engagement(managers_df):
    """Generate team engagement survey results"""
    engagement_data = []

    for _, manager in managers_df.iterrows():
        for quarter in pd.date_range(start='2023-Q1', end='2026-Q1', freq='QE'):
            # Engagement scores by manager archetype
            if manager['archetype'] == 'Exceptional':
                overall_score = random.uniform(8.2, 9.5)
                manager_score = random.uniform(8.5, 9.8)
                development_score = random.uniform(8.0, 9.5)
            elif manager['archetype'] == 'Strong':
                overall_score = random.uniform(7.2, 8.5)
                manager_score = random.uniform(7.5, 8.8)
                development_score = random.uniform(7.0, 8.5)
            elif manager['archetype'] == 'Adequate':
                overall_score = random.uniform(5.8, 7.3)
                manager_score = random.uniform(6.0, 7.5)
                development_score = random.uniform(5.5, 7.0)
            elif manager['archetype'] == 'Struggling':
                overall_score = random.uniform(4.2, 6.0)
                manager_score = random.uniform(4.0, 6.2)
                development_score = random.uniform(4.0, 5.8)
            else:  # Ineffective
                overall_score = random.uniform(2.5, 4.5)
                manager_score = random.uniform(2.0, 4.5)
                development_score = random.uniform(2.5, 4.5)

            response_rate = random.uniform(0.65, 0.95)

            engagement_data.append({
                'manager_id': manager['manager_id'],
                'department': manager['department'],
                'quarter': quarter.strftime('%Y-Q%q'),
                'overall_engagement_score': round(overall_score, 1),
                'manager_effectiveness_score': round(manager_score, 1),
                'development_score': round(development_score, 1),
                'response_rate': round(response_rate, 2),
                'team_size': manager['span_of_control']
            })

    return pd.DataFrame(engagement_data)

def generate_one_on_ones(managers_df, team_members_df):
    """Generate 1:1 meeting frequency and quality data"""
    one_on_one_data = []

    for _, manager in managers_df.iterrows():
        team = team_members_df[team_members_df['manager_id'] == manager['manager_id']]

        for _, employee in team.iterrows():
            for month in pd.date_range(start='2023-01', end='2026-03', freq='ME'):
                # 1:1 frequency varies by manager archetype
                if manager['archetype'] in ['Exceptional', 'Strong']:
                    # Weekly or bi-weekly
                    num_meetings = random.choice([2, 4]) if random.random() > 0.1 else random.choice([1, 3])
                    quality_score = random.uniform(7.5, 10.0)
                    # Career development discussed 25-35% of time for exceptional managers
                    career_dev_prob = 0.30
                elif manager['archetype'] == 'Adequate':
                    # Bi-weekly or monthly
                    num_meetings = random.choice([1, 2])
                    quality_score = random.uniform(5.5, 7.5)
                    # Career development discussed 15-20% of time
                    career_dev_prob = 0.18
                else:
                    # Monthly or less
                    num_meetings = random.choice([0, 1])
                    quality_score = random.uniform(2.0, 6.0) if num_meetings > 0 else 0
                    # Career development discussed 5-10% of time
                    career_dev_prob = 0.08

                avg_duration = random.randint(20, 45) if num_meetings > 0 else 0

                one_on_one_data.append({
                    'manager_id': manager['manager_id'],
                    'employee_id': employee['employee_id'],
                    'month': month.strftime('%Y-%m'),
                    'num_meetings': num_meetings,
                    'avg_duration_minutes': avg_duration,
                    'quality_score': round(quality_score, 1),
                    'covered_career_development': random.random() < career_dev_prob if num_meetings > 0 else False
                })

    return pd.DataFrame(one_on_one_data)

def generate_manager_behaviors(managers_df):
    """Generate manager behavior tracking data"""
    behavior_data = []

    for _, manager in managers_df.iterrows():
        for month in pd.date_range(start='2023-01', end='2026-03', freq='ME'):
            # Behaviors vary by archetype
            if manager['archetype'] == 'Exceptional':
                feedback_count = random.randint(15, 30)
                recognition_count = random.randint(8, 15)
                coaching_hours = random.uniform(4, 8)
                delegation_score = random.uniform(8, 10)
            elif manager['archetype'] == 'Strong':
                feedback_count = random.randint(10, 20)
                recognition_count = random.randint(5, 10)
                coaching_hours = random.uniform(2, 5)
                delegation_score = random.uniform(6, 8)
            elif manager['archetype'] == 'Adequate':
                feedback_count = random.randint(5, 12)
                recognition_count = random.randint(2, 6)
                coaching_hours = random.uniform(1, 3)
                delegation_score = random.uniform(4, 6)
            else:
                feedback_count = random.randint(0, 8)
                recognition_count = random.randint(0, 3)
                coaching_hours = random.uniform(0, 2)
                delegation_score = random.uniform(2, 5)

            behavior_data.append({
                'manager_id': manager['manager_id'],
                'month': month.strftime('%Y-%m'),
                'feedback_instances': feedback_count,
                'recognition_given': recognition_count,
                'coaching_hours': round(coaching_hours, 1),
                'delegation_effectiveness': round(delegation_score, 1),
                'team_meetings_held': random.randint(2, 4),
                'skip_level_meetings': random.randint(0, 2) if manager['archetype'] in ['Exceptional', 'Strong'] else 0
            })

    return pd.DataFrame(behavior_data)

def generate_team_performance(managers_df, team_members_df):
    """Generate team performance distribution data"""
    performance_data = []

    for _, manager in managers_df.iterrows():
        team = team_members_df[team_members_df['manager_id'] == manager['manager_id']]

        for year in [2023, 2024, 2025]:
            ratings = team['performance_rating'].values

            performance_data.append({
                'manager_id': manager['manager_id'],
                'department': manager['department'],
                'year': year,
                'team_size': len(team),
                'avg_performance': round(ratings.mean(), 2),
                'pct_high_performers': round((ratings >= 4).sum() / len(ratings), 3),
                'pct_low_performers': round((ratings <= 2).sum() / len(ratings), 3),
                'performance_std': round(ratings.std(), 2),
                'rating_fairness_score': round(random.uniform(6, 10) if manager['archetype'] in ['Exceptional', 'Strong'] else random.uniform(3, 7), 1)
            })

    return pd.DataFrame(performance_data)

def generate_promotions(managers_df, team_members_df):
    """Generate promotion outcomes by manager"""
    promotion_data = []

    for _, manager in managers_df.iterrows():
        team = team_members_df[team_members_df['manager_id'] == manager['manager_id']]
        eligible = team[team['promotion_eligible']]

        for year in [2023, 2024, 2025]:
            # Promotion rate varies by manager effectiveness
            if manager['archetype'] == 'Exceptional':
                promotion_rate = random.uniform(0.15, 0.25)
            elif manager['archetype'] == 'Strong':
                promotion_rate = random.uniform(0.10, 0.18)
            elif manager['archetype'] == 'Adequate':
                promotion_rate = random.uniform(0.05, 0.12)
            else:
                promotion_rate = random.uniform(0.00, 0.08)

            num_eligible = len(eligible)
            num_promoted = int(num_eligible * promotion_rate) if num_eligible > 0 else 0

            promotion_data.append({
                'manager_id': manager['manager_id'],
                'department': manager['department'],
                'year': year,
                'team_size': len(team),
                'num_eligible': num_eligible,
                'num_promoted': num_promoted,
                'promotion_rate': round(num_promoted / num_eligible, 3) if num_eligible > 0 else 0,
                'internal_mobility_rate': round(random.uniform(0.05, 0.15) if manager['archetype'] in ['Exceptional', 'Strong'] else random.uniform(0.00, 0.08), 3)
            })

    return pd.DataFrame(promotion_data)

def generate_manager_training(managers_df):
    """Generate manager development program participation"""
    training_data = []

    training_programs = [
        'New Manager Bootcamp',
        'Leadership Fundamentals',
        'Effective 1:1s',
        'Difficult Conversations',
        'Coaching Skills',
        'Performance Management',
        'Manager Mentorship Program'
    ]

    for _, manager in managers_df.iterrows():
        # Number of programs based on tenure and archetype
        if manager['is_new_manager']:
            num_programs = random.randint(2, 4)
        elif manager['archetype'] in ['Struggling', 'Ineffective']:
            num_programs = random.randint(2, 5)
        else:
            num_programs = random.randint(1, 3)

        selected_programs = random.sample(training_programs, min(num_programs, len(training_programs)))

        for program in selected_programs:
            completion_date = START_DATE + timedelta(days=random.randint(0, 1000))

            # Pre/post effectiveness change
            if manager['archetype'] in ['Struggling', 'Ineffective']:
                pre_score = manager['effectiveness_score']
                improvement = random.uniform(0.3, 1.2)
                post_score = min(10, pre_score + improvement)
            else:
                pre_score = manager['effectiveness_score']
                improvement = random.uniform(0.1, 0.5)
                post_score = min(10, pre_score + improvement)

            training_data.append({
                'manager_id': manager['manager_id'],
                'program_name': program,
                'completion_date': completion_date.strftime('%Y-%m-%d'),
                'pre_effectiveness_score': round(pre_score, 1),
                'post_effectiveness_score': round(post_score, 1),
                'improvement': round(post_score - pre_score, 1),
                'applied_learnings': random.choice([True, False]) if random.random() > 0.2 else True
            })

    return pd.DataFrame(training_data)

def main():
    """Generate all datasets for Manager Effectiveness domain"""
    print("Generating Manager Effectiveness sample data...")
    print("="*80)

    # Generate managers
    print("\n1. Generating managers data...")
    managers_df = generate_managers()
    print(f"   Created {len(managers_df)} managers")
    print(f"   Departments: {managers_df['department'].value_counts().to_dict()}")
    print(f"   Archetypes: {managers_df['archetype'].value_counts().to_dict()}")

    # Generate team members
    print("\n2. Generating team members data...")
    team_members_df = generate_team_members(managers_df)
    print(f"   Created {len(team_members_df)} employees")
    print(f"   Avg span of control: {len(team_members_df) / len(managers_df):.1f}")

    # Generate team retention
    print("\n3. Generating team retention data...")
    retention_df = generate_team_retention(managers_df)
    print(f"   Created {len(retention_df)} retention records")

    # Generate team engagement
    print("\n4. Generating team engagement data...")
    engagement_df = generate_team_engagement(managers_df)
    print(f"   Created {len(engagement_df)} engagement records")

    # Generate 1:1 data
    print("\n5. Generating 1:1 meeting data...")
    one_on_ones_df = generate_one_on_ones(managers_df, team_members_df)
    print(f"   Created {len(one_on_ones_df)} 1:1 records")

    # Generate manager behaviors
    print("\n6. Generating manager behaviors data...")
    behaviors_df = generate_manager_behaviors(managers_df)
    print(f"   Created {len(behaviors_df)} behavior records")

    # Generate team performance
    print("\n7. Generating team performance data...")
    performance_df = generate_team_performance(managers_df, team_members_df)
    print(f"   Created {len(performance_df)} team performance records")

    # Generate promotions
    print("\n8. Generating promotions data...")
    promotions_df = generate_promotions(managers_df, team_members_df)
    print(f"   Created {len(promotions_df)} promotion records")

    # Generate manager training
    print("\n9. Generating manager training data...")
    training_df = generate_manager_training(managers_df)
    print(f"   Created {len(training_df)} training records")

    # Save all datasets
    print("\n" + "="*80)
    print("Saving datasets...")

    managers_df.to_csv('05_Manager_Effectiveness/data/managers.csv', index=False)
    team_members_df.to_csv('05_Manager_Effectiveness/data/team_members.csv', index=False)
    retention_df.to_csv('05_Manager_Effectiveness/data/team_retention.csv', index=False)
    engagement_df.to_csv('05_Manager_Effectiveness/data/team_engagement.csv', index=False)
    one_on_ones_df.to_csv('05_Manager_Effectiveness/data/one_on_ones.csv', index=False)
    behaviors_df.to_csv('05_Manager_Effectiveness/data/manager_behaviors.csv', index=False)
    performance_df.to_csv('05_Manager_Effectiveness/data/team_performance.csv', index=False)
    promotions_df.to_csv('05_Manager_Effectiveness/data/promotions_from_team.csv', index=False)
    training_df.to_csv('05_Manager_Effectiveness/data/manager_training.csv', index=False)

    print("\n✓ All datasets generated successfully!")
    print("\nDatasets created:")
    print("  - managers.csv")
    print("  - team_members.csv")
    print("  - team_retention.csv")
    print("  - team_engagement.csv")
    print("  - one_on_ones.csv")
    print("  - manager_behaviors.csv")
    print("  - team_performance.csv")
    print("  - promotions_from_team.csv")
    print("  - manager_training.csv")
    print("="*80)

if __name__ == "__main__":
    main()
