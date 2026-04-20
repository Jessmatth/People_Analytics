"""
Generate synthetic employee and attrition data for retention analysis.

This script creates realistic sample data including:
- Active employees
- Former employees (departed)
- Compensation data
- Performance reviews
- Engagement survey responses
- Exit interviews
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
N_CURRENT_EMPLOYEES = 500
N_FORMER_EMPLOYEES = 150  # Departed in last 2 years
START_DATE = datetime(2020, 1, 1)
CURRENT_DATE = datetime(2026, 4, 20)

# Reference data
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 
               'Finance', 'HR', 'Operations', 'Legal', 'Data']
JOB_LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP']
LOCATIONS = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Boston', 'Remote', 'Chicago', 'Denver']
EDUCATION_LEVELS = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
HIRE_SOURCES = ['Referral', 'LinkedIn', 'Indeed', 'Company Career Site', 'Recruiting Agency', 
                'University Recruiting', 'Glassdoor', 'Other Job Board']
TERMINATION_REASONS = ['Voluntary - Better Opportunity', 'Voluntary - Compensation', 
                       'Voluntary - Career Growth', 'Voluntary - Work-Life Balance',
                       'Voluntary - Manager Relationship', 'Voluntary - Relocation',
                       'Involuntary - Performance', 'Involuntary - Restructuring',
                       'Retirement', 'Voluntary - Other']

print("Generating employee data...")

# Function to generate hire date with realistic distribution
def generate_hire_date(is_active=True):
    if is_active:
        # Active employees: hired between 2020 and 2025
        days_range = (CURRENT_DATE - START_DATE).days
        days_offset = np.random.exponential(scale=days_range/3)  # Skew toward recent hires
        days_offset = min(days_offset, days_range)
        return START_DATE + timedelta(days=days_offset)
    else:
        # Former employees: hired between 2020 and 2024
        end_hiring = CURRENT_DATE - timedelta(days=90)  # At least 90 days before current
        days_range = (end_hiring - START_DATE).days
        days_offset = np.random.exponential(scale=days_range/3)
        days_offset = min(days_offset, days_range)
        return START_DATE + timedelta(days=days_offset)

# Function to generate termination date
def generate_term_date(hire_date):
    # At least 30 days after hire, within last 2 years
    earliest_term = max(hire_date + timedelta(days=30), CURRENT_DATE - timedelta(days=730))
    days_range = (CURRENT_DATE - earliest_term).days
    if days_range <= 0:
        days_range = 30
    days_offset = random.randint(0, days_range)
    return earliest_term + timedelta(days=days_offset)

# Generate active employees
active_employees = []
employee_id_counter = 1000

for i in range(N_CURRENT_EMPLOYEES):
    emp_id = f"EMP{employee_id_counter:04d}"
    employee_id_counter += 1
    
    hire_date = generate_hire_date(is_active=True)
    tenure_years = (CURRENT_DATE - hire_date).days / 365.25
    
    department = random.choice(DEPARTMENTS)
    
    # Job level correlates with tenure
    if tenure_years < 1:
        job_level = random.choices(['IC1', 'IC2', 'IC3'], weights=[0.5, 0.3, 0.2])[0]
    elif tenure_years < 3:
        job_level = random.choices(['IC2', 'IC3', 'IC4', 'Manager'], weights=[0.3, 0.4, 0.2, 0.1])[0]
    elif tenure_years < 5:
        job_level = random.choices(['IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager'], 
                                   weights=[0.2, 0.3, 0.15, 0.25, 0.1])[0]
    else:
        job_level = random.choices(['IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP'], 
                                   weights=[0.15, 0.15, 0.25, 0.25, 0.15, 0.05])[0]
    
    location = random.choice(LOCATIONS)
    education = random.choices(EDUCATION_LEVELS, weights=[0.05, 0.10, 0.50, 0.30, 0.05])[0]
    hire_source = random.choice(HIRE_SOURCES)
    
    # Base salary by level
    salary_ranges = {
        'IC1': (50000, 70000), 'IC2': (65000, 85000), 'IC3': (80000, 110000),
        'IC4': (100000, 140000), 'IC5': (130000, 180000),
        'Manager': (110000, 150000), 'Senior Manager': (140000, 190000),
        'Director': (170000, 230000), 'VP': (220000, 320000)
    }
    min_sal, max_sal = salary_ranges[job_level]
    base_salary = int(np.random.uniform(min_sal, max_sal))
    
    # Market percentile (will be used for flight risk)
    market_percentile = int(np.random.normal(50, 20))
    market_percentile = np.clip(market_percentile, 10, 90)
    
    # Months since last promotion (risk factor)
    if tenure_years < 1:
        months_since_promotion = tenure_years * 12
    else:
        months_since_promotion = np.random.exponential(scale=18)  # Avg 18 months
        months_since_promotion = min(months_since_promotion, tenure_years * 12)
    
    # Months since last raise
    months_since_raise = np.random.exponential(scale=12)  # Avg 12 months
    months_since_raise = min(months_since_raise, tenure_years * 12)
    
    # Performance rating (1-5 scale)
    performance_rating = np.clip(np.random.normal(3.7, 0.6), 1, 5)
    
    # Engagement score (0-100)
    # Lower engagement = higher flight risk
    engagement_score = np.clip(np.random.normal(72, 15), 20, 100)
    
    # Manager tenure (longer manager tenure = better retention)
    manager_tenure_years = np.clip(np.random.exponential(scale=2.5), 0.5, 15)
    
    active_employees.append({
        'employee_id': emp_id,
        'status': 'Active',
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'termination_date': None,
        'tenure_years': round(tenure_years, 2),
        'department': department,
        'job_level': job_level,
        'location': location,
        'education': education,
        'hire_source': hire_source,
        'base_salary': base_salary,
        'market_percentile': market_percentile,
        'months_since_promotion': round(months_since_promotion, 1),
        'months_since_raise': round(months_since_raise, 1),
        'performance_rating': round(performance_rating, 2),
        'engagement_score': round(engagement_score, 1),
        'manager_tenure_years': round(manager_tenure_years, 2),
        'high_performer': 1 if performance_rating >= 4.0 else 0,
        'critical_role': 1 if random.random() < 0.15 else 0  # 15% are critical roles
    })

print(f"  Generated {len(active_employees)} active employees")

# Generate former employees (those who left)
former_employees = []

for i in range(N_FORMER_EMPLOYEES):
    emp_id = f"EMP{employee_id_counter:04d}"
    employee_id_counter += 1
    
    hire_date = generate_hire_date(is_active=False)
    term_date = generate_term_date(hire_date)
    tenure_years = (term_date - hire_date).days / 365.25
    
    department = random.choice(DEPARTMENTS)
    
    # Attrition is higher for certain groups
    # Higher attrition in first year and around 2-3 year mark
    if tenure_years < 0.25:  # 90 days
        job_level = random.choices(['IC1', 'IC2'], weights=[0.7, 0.3])[0]
    elif tenure_years < 1:
        job_level = random.choices(['IC1', 'IC2', 'IC3'], weights=[0.4, 0.4, 0.2])[0]
    elif tenure_years < 3:
        job_level = random.choices(['IC2', 'IC3', 'IC4', 'Manager'], weights=[0.3, 0.4, 0.2, 0.1])[0]
    else:
        job_level = random.choices(['IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager'], 
                                   weights=[0.25, 0.3, 0.15, 0.2, 0.1])[0]
    
    location = random.choice(LOCATIONS)
    education = random.choices(EDUCATION_LEVELS, weights=[0.05, 0.10, 0.50, 0.30, 0.05])[0]
    hire_source = random.choice(HIRE_SOURCES)
    
    # Salary (leavers skew lower percentile)
    salary_ranges = {
        'IC1': (50000, 70000), 'IC2': (65000, 85000), 'IC3': (80000, 110000),
        'IC4': (100000, 140000), 'IC5': (130000, 180000),
        'Manager': (110000, 150000), 'Senior Manager': (140000, 190000),
        'Director': (170000, 230000), 'VP': (220000, 320000)
    }
    min_sal, max_sal = salary_ranges[job_level]
    base_salary = int(np.random.uniform(min_sal, max_sal))
    
    # Leavers tend to have LOWER market percentiles
    market_percentile = int(np.random.normal(40, 18))  # Lower than stayers
    market_percentile = np.clip(market_percentile, 10, 75)
    
    # Leavers have LONGER time since promotion/raise
    months_since_promotion = np.random.exponential(scale=24)  # Longer than stayers
    months_since_promotion = min(months_since_promotion, tenure_years * 12)
    
    months_since_raise = np.random.exponential(scale=15)  # Longer than stayers
    months_since_raise = min(months_since_raise, tenure_years * 12)
    
    # Performance rating
    # Mix of high and low performers leave
    if random.random() < 0.35:  # 35% are high performers (regrettable)
        performance_rating = np.clip(np.random.normal(4.2, 0.4), 3.5, 5)
        termination_reason = random.choices(
            ['Voluntary - Better Opportunity', 'Voluntary - Compensation', 
             'Voluntary - Career Growth', 'Voluntary - Work-Life Balance'],
            weights=[0.4, 0.3, 0.2, 0.1]
        )[0]
    elif random.random() < 0.20:  # 20% are low performers (involuntary)
        performance_rating = np.clip(np.random.normal(2.5, 0.5), 1, 3.0)
        termination_reason = random.choices(
            ['Involuntary - Performance', 'Involuntary - Restructuring'],
            weights=[0.7, 0.3]
        )[0]
    else:  # 45% are average performers
        performance_rating = np.clip(np.random.normal(3.4, 0.4), 2.5, 4.0)
        termination_reason = random.choice(TERMINATION_REASONS[:6])  # Voluntary reasons
    
    # Engagement score (leavers had lower engagement)
    engagement_score = np.clip(np.random.normal(58, 18), 15, 90)  # Lower than stayers
    
    # Manager tenure
    manager_tenure_years = np.clip(np.random.exponential(scale=1.8), 0.3, 10)
    
    # Regrettable attrition flag
    regrettable = 1 if (performance_rating >= 3.8 and 'Voluntary' in termination_reason) else 0
    
    former_employees.append({
        'employee_id': emp_id,
        'status': 'Terminated',
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'termination_date': term_date.strftime('%Y-%m-%d'),
        'tenure_years': round(tenure_years, 2),
        'department': department,
        'job_level': job_level,
        'location': location,
        'education': education,
        'hire_source': hire_source,
        'base_salary': base_salary,
        'market_percentile': market_percentile,
        'months_since_promotion': round(months_since_promotion, 1),
        'months_since_raise': round(months_since_raise, 1),
        'performance_rating': round(performance_rating, 2),
        'engagement_score': round(engagement_score, 1),
        'manager_tenure_years': round(manager_tenure_years, 2),
        'high_performer': 1 if performance_rating >= 4.0 else 0,
        'critical_role': 1 if random.random() < 0.12 else 0,
        'termination_reason': termination_reason,
        'regrettable_attrition': regrettable
    })

print(f"  Generated {len(former_employees)} former employees")

# Combine into single employee dataset
all_employees = active_employees + former_employees
employees_df = pd.DataFrame(all_employees)

# Add gender and ethnicity for diversity analysis
employees_df['gender'] = np.random.choice(['Male', 'Female', 'Non-Binary'], 
                                          size=len(employees_df), 
                                          p=[0.52, 0.46, 0.02])
employees_df['ethnicity'] = np.random.choice(
    ['White', 'Asian', 'Hispanic/Latino', 'Black/African American', 'Two or More', 'Other'],
    size=len(employees_df),
    p=[0.55, 0.20, 0.12, 0.08, 0.04, 0.01]
)

# Save employee master file
employees_df.to_csv('employees.csv', index=False)
print(f"\nSaved employees.csv ({len(employees_df)} records)")

# Generate exit interview data for former employees
print("\nGenerating exit interview data...")
exit_interviews = []

for emp in former_employees:
    if 'Voluntary' in emp['termination_reason']:
        # Voluntary leavers more likely to complete exit interview
        if random.random() < 0.75:  # 75% response rate
            # Satisfaction scores (1-5 scale)
            overall_satisfaction = np.clip(np.random.normal(2.8, 1.0), 1, 5)
            manager_satisfaction = np.clip(np.random.normal(2.7, 1.1), 1, 5)
            growth_satisfaction = np.clip(np.random.normal(2.5, 1.0), 1, 5)
            comp_satisfaction = np.clip(np.random.normal(2.6, 1.0), 1, 5)
            worklife_satisfaction = np.clip(np.random.normal(3.2, 1.0), 1, 5)
            
            # Would rehire
            would_rehire = 'Yes' if overall_satisfaction >= 3.5 else 'No'
            
            # Primary reason categories
            if 'Compensation' in emp['termination_reason']:
                primary_reason = 'Compensation'
            elif 'Career Growth' in emp['termination_reason']:
                primary_reason = 'Limited Growth Opportunities'
            elif 'Manager' in emp['termination_reason']:
                primary_reason = 'Manager Relationship'
            elif 'Work-Life' in emp['termination_reason']:
                primary_reason = 'Work-Life Balance'
            else:
                primary_reason = random.choice(['Better Opportunity', 'Company Culture', 'Other'])
            
            exit_interviews.append({
                'employee_id': emp['employee_id'],
                'exit_interview_date': emp['termination_date'],
                'overall_satisfaction': round(overall_satisfaction, 2),
                'manager_satisfaction': round(manager_satisfaction, 2),
                'growth_satisfaction': round(growth_satisfaction, 2),
                'compensation_satisfaction': round(comp_satisfaction, 2),
                'worklife_satisfaction': round(worklife_satisfaction, 2),
                'would_rehire': would_rehire,
                'primary_reason': primary_reason,
                'completed': 'Yes'
            })
    else:
        # Involuntary leavers rarely complete exit interview
        if random.random() < 0.20:  # 20% response rate
            exit_interviews.append({
                'employee_id': emp['employee_id'],
                'exit_interview_date': emp['termination_date'],
                'overall_satisfaction': None,
                'manager_satisfaction': None,
                'growth_satisfaction': None,
                'compensation_satisfaction': None,
                'worklife_satisfaction': None,
                'would_rehire': None,
                'primary_reason': None,
                'completed': 'No'
            })

exit_df = pd.DataFrame(exit_interviews)
exit_df.to_csv('exit_interviews.csv', index=False)
print(f"Saved exit_interviews.csv ({len(exit_df)} records)")

# Generate engagement survey data (multiple survey waves for active employees)
print("\nGenerating engagement survey data...")
survey_dates = [
    datetime(2025, 1, 15),
    datetime(2025, 7, 15),
    datetime(2026, 1, 15)
]

engagement_surveys = []

for survey_date in survey_dates:
    for emp in active_employees:
        emp_hire = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        # Only survey employees who were hired before survey date
        if emp_hire < survey_date:
            # 85% response rate
            if random.random() < 0.85:
                # Base scores on employee engagement_score with some variation
                base_engagement = emp['engagement_score']
                
                overall_engagement = np.clip(np.random.normal(base_engagement, 8), 0, 100)
                manager_effectiveness = np.clip(np.random.normal(base_engagement + 3, 10), 0, 100)
                growth_opportunities = np.clip(np.random.normal(base_engagement - 5, 12), 0, 100)
                work_life_balance = np.clip(np.random.normal(base_engagement + 2, 10), 0, 100)
                compensation_fair = np.clip(np.random.normal(emp['market_percentile'], 15), 0, 100)
                recommend_company = np.clip(np.random.normal(base_engagement - 3, 12), 0, 100)
                
                # eNPS calculation (-100 to +100)
                if recommend_company >= 80:
                    enps_category = 'Promoter'
                elif recommend_company >= 60:
                    enps_category = 'Passive'
                else:
                    enps_category = 'Detractor'
                
                engagement_surveys.append({
                    'employee_id': emp['employee_id'],
                    'survey_date': survey_date.strftime('%Y-%m-%d'),
                    'overall_engagement': round(overall_engagement, 1),
                    'manager_effectiveness': round(manager_effectiveness, 1),
                    'growth_opportunities': round(growth_opportunities, 1),
                    'work_life_balance': round(work_life_balance, 1),
                    'compensation_fairness': round(compensation_fair, 1),
                    'recommend_company': round(recommend_company, 1),
                    'enps_category': enps_category,
                    'response_status': 'Completed'
                })

engagement_df = pd.DataFrame(engagement_surveys)
engagement_df.to_csv('engagement_surveys.csv', index=False)
print(f"Saved engagement_surveys.csv ({len(engagement_df)} records)")

# Summary statistics
print("\n" + "="*60)
print("DATA GENERATION COMPLETE")
print("="*60)

active_df = employees_df[employees_df['status'] == 'Active']
termed_df = employees_df[employees_df['status'] == 'Terminated']

print(f"\nEmployee Summary:")
print(f"  Active employees: {len(active_df)}")
print(f"  Former employees: {len(termed_df)}")
print(f"  Total: {len(employees_df)}")

print(f"\nAttrition Metrics:")
total_headcount = len(active_df) + len(termed_df)
attrition_rate = (len(termed_df) / total_headcount) * 100
print(f"  Overall attrition rate: {attrition_rate:.1f}%")

voluntary = termed_df[termed_df['termination_reason'].str.contains('Voluntary', na=False)]
print(f"  Voluntary departures: {len(voluntary)} ({len(voluntary)/len(termed_df)*100:.1f}%)")

regrettable = termed_df[termed_df['regrettable_attrition'] == 1]
print(f"  Regrettable attrition: {len(regrettable)} ({len(regrettable)/len(termed_df)*100:.1f}%)")

print(f"\nAverage Metrics (Active Employees):")
print(f"  Tenure: {active_df['tenure_years'].mean():.1f} years")
print(f"  Engagement score: {active_df['engagement_score'].mean():.1f}")
print(f"  Performance rating: {active_df['performance_rating'].mean():.2f}")
print(f"  Market percentile: {active_df['market_percentile'].mean():.0f}")

print(f"\nSurvey Metrics:")
print(f"  Engagement surveys: {len(engagement_df)} responses")
print(f"  Exit interviews: {len(exit_df)} completed")

print(f"\n" + "="*60)
print("Files created in current directory:")
print("  - employees.csv")
print("  - engagement_surveys.csv")
print("  - exit_interviews.csv")
print("="*60)
