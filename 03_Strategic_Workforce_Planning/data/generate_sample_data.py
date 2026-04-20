"""
Generate synthetic workforce planning data.

This script creates realistic sample data including:
- Historical headcount trends
- Current workforce with skills and succession data
- Business growth targets
- Critical roles and succession readiness
- Organizational structure
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed
np.random.seed(42)
random.seed(42)

# Configuration
CURRENT_DATE = datetime(2026, 4, 20)
HISTORICAL_MONTHS = 24  # 2 years of history

# Reference data
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 
               'Finance', 'HR', 'Operations', 'Legal', 'Data']
JOB_LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP']
LOCATIONS = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Boston', 'Remote']

# Skills by department
SKILLS_BY_DEPT = {
    'Engineering': ['Python', 'JavaScript', 'Java', 'React', 'Node.js', 'AWS', 'Kubernetes', 
                   'Machine Learning', 'SQL', 'Git', 'Docker', 'TypeScript'],
    'Product': ['Product Strategy', 'Roadmap Planning', 'User Research', 'A/B Testing', 
               'Agile', 'SQL', 'Analytics', 'Wireframing', 'Stakeholder Management'],
    'Sales': ['Enterprise Sales', 'SaaS Sales', 'Negotiation', 'Salesforce', 'Lead Generation',
             'Account Management', 'Sales Forecasting', 'Closing'],
    'Marketing': ['Digital Marketing', 'SEO', 'Content Marketing', 'Marketing Analytics',
                 'Brand Strategy', 'Social Media', 'Email Marketing', 'Campaign Management'],
    'Customer Success': ['Customer Onboarding', 'Account Management', 'Support', 'CRM',
                        'Customer Retention', 'Upselling', 'Training'],
    'Finance': ['Financial Modeling', 'Accounting', 'FP&A', 'Excel', 'ERP Systems',
               'Budgeting', 'Financial Reporting', 'Audit'],
    'HR': ['Recruiting', 'Employee Relations', 'Compensation', 'Benefits', 'HRIS',
          'Performance Management', 'Talent Development', 'HR Analytics'],
    'Operations': ['Process Improvement', 'Project Management', 'Vendor Management',
                  'Supply Chain', 'Logistics', 'Six Sigma', 'Lean'],
    'Legal': ['Contract Law', 'Employment Law', 'Corporate Law', 'Compliance',
             'Litigation', 'Negotiation', 'Risk Management'],
    'Data': ['SQL', 'Python', 'R', 'Tableau', 'Power BI', 'Machine Learning',
            'Statistical Analysis', 'Data Modeling', 'ETL', 'BigQuery']
}

EMERGING_SKILLS = ['AI/ML', 'Blockchain', 'Cloud Architecture', 'Data Science', 
                   'Cybersecurity', 'DevOps', 'Product-Led Growth', 'Change Management']

print("="*60)
print("STRATEGIC WORKFORCE PLANNING DATA GENERATION")
print("="*60)

# =============================================================================
# 1. HISTORICAL HEADCOUNT DATA
# =============================================================================
print("\n1. Generating historical headcount data...")

historical_data = []

# Starting headcount (24 months ago)
base_headcount = {
    'Engineering': 85,
    'Product': 25,
    'Sales': 50,
    'Marketing': 30,
    'Customer Success': 35,
    'Finance': 18,
    'HR': 12,
    'Operations': 22,
    'Legal': 8,
    'Data': 15
}

# Monthly growth rates (varying by department)
growth_rates = {
    'Engineering': 0.03,  # 3% monthly growth
    'Product': 0.025,
    'Sales': 0.02,
    'Marketing': 0.015,
    'Customer Success': 0.025,
    'Finance': 0.01,
    'HR': 0.015,
    'Operations': 0.01,
    'Legal': 0.005,
    'Data': 0.035  # Fastest growing
}

for month_offset in range(HISTORICAL_MONTHS + 1):
    snapshot_date = CURRENT_DATE - timedelta(days=30 * (HISTORICAL_MONTHS - month_offset))
    
    for dept, base_hc in base_headcount.items():
        # Calculate headcount with growth + some randomness
        months_growth = month_offset
        growth_rate = growth_rates[dept]
        
        expected_hc = base_hc * (1 + growth_rate) ** months_growth
        # Add some noise (±5%)
        actual_hc = int(expected_hc * np.random.uniform(0.95, 1.05))
        
        historical_data.append({
            'snapshot_date': snapshot_date.strftime('%Y-%m-%d'),
            'department': dept,
            'headcount': actual_hc,
            'year': snapshot_date.year,
            'month': snapshot_date.month,
            'quarter': f"Q{(snapshot_date.month-1)//3 + 1}"
        })

historical_df = pd.DataFrame(historical_data)
historical_df.to_csv('headcount_history.csv', index=False)
print(f"  ✓ Saved headcount_history.csv ({len(historical_df)} records)")
print(f"    Current total headcount: {historical_df[historical_df['snapshot_date']==CURRENT_DATE.strftime('%Y-%m-%d')]['headcount'].sum()}")

# =============================================================================
# 2. CURRENT WORKFORCE WITH SKILLS
# =============================================================================
print("\n2. Generating current workforce with skills...")

current_headcount = historical_df[historical_df['snapshot_date'] == CURRENT_DATE.strftime('%Y-%m-%d')]

employees = []
employee_skills = []
emp_id = 5000

for _, row in current_headcount.iterrows():
    dept = row['department']
    hc = row['headcount']
    
    for i in range(hc):
        emp_id += 1
        
        # Assign job level (realistic distribution)
        level = random.choices(
            ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP'],
            weights=[0.15, 0.25, 0.25, 0.15, 0.10, 0.06, 0.03, 0.008, 0.002]
        )[0]
        
        # Tenure
        tenure_years = np.clip(np.random.exponential(scale=3), 0.1, 20)
        
        # Age (correlated with level and tenure)
        base_age = 25
        if 'IC1' in level:
            base_age = np.random.uniform(22, 28)
        elif 'IC2' in level:
            base_age = np.random.uniform(25, 32)
        elif 'IC3' in level:
            base_age = np.random.uniform(28, 38)
        elif 'IC4' in level:
            base_age = np.random.uniform(32, 45)
        elif 'IC5' in level:
            base_age = np.random.uniform(35, 50)
        elif 'Manager' in level:
            base_age = np.random.uniform(30, 45)
        elif 'Senior Manager' in level:
            base_age = np.random.uniform(35, 50)
        elif 'Director' in level:
            base_age = np.random.uniform(40, 55)
        elif 'VP' in level:
            base_age = np.random.uniform(45, 60)
        
        age = int(base_age + min(tenure_years, 10))
        
        # Retirement eligibility (age 62+ or 30+ years tenure)
        retirement_eligible = 1 if (age >= 62 or tenure_years >= 30) else 0
        
        # Performance rating
        performance = np.clip(np.random.normal(3.7, 0.6), 1, 5)
        
        # High potential flag (top 10%)
        high_potential = 1 if (performance >= 4.2 and random.random() < 0.15) else 0
        
        # Location
        if dept in ['Engineering', 'Data', 'Product']:
            location = random.choices(LOCATIONS, weights=[0.15, 0.15, 0.15, 0.15, 0.10, 0.30])[0]
        else:
            location = random.choice(LOCATIONS)
        
        employees.append({
            'employee_id': f'EMP{emp_id:05d}',
            'department': dept,
            'job_level': level,
            'location': location,
            'tenure_years': round(tenure_years, 1),
            'age': age,
            'retirement_eligible': retirement_eligible,
            'performance_rating': round(performance, 2),
            'high_potential': high_potential
        })
        
        # Assign skills
        dept_skills = SKILLS_BY_DEPT.get(dept, [])
        
        # Number of skills (more senior = more skills)
        if 'IC1' in level or 'IC2' in level:
            num_skills = random.randint(2, 4)
        elif 'IC3' in level:
            num_skills = random.randint(3, 6)
        elif 'IC4' in level or 'IC5' in level:
            num_skills = random.randint(4, 8)
        else:  # Management
            num_skills = random.randint(5, 10)
        
        emp_skills = random.sample(dept_skills, min(num_skills, len(dept_skills)))
        
        # Some employees have emerging skills (more likely for high performers)
        if random.random() < 0.15 * (1.5 if high_potential else 1):
            emp_skills.append(random.choice(EMERGING_SKILLS))
        
        # Proficiency levels
        for skill in emp_skills:
            proficiency = random.choices(
                ['Basic', 'Intermediate', 'Advanced', 'Expert'],
                weights=[0.20, 0.35, 0.30, 0.15]
            )[0]
            
            years_experience = min(tenure_years, random.uniform(0.5, tenure_years))
            
            employee_skills.append({
                'employee_id': f'EMP{emp_id:05d}',
                'skill': skill,
                'proficiency': proficiency,
                'years_experience': round(years_experience, 1)
            })

employees_df = pd.DataFrame(employees)
skills_df = pd.DataFrame(employee_skills)

employees_df.to_csv('current_workforce.csv', index=False)
skills_df.to_csv('employee_skills.csv', index=False)

print(f"  ✓ Saved current_workforce.csv ({len(employees_df)} employees)")
print(f"  ✓ Saved employee_skills.csv ({len(skills_df)} skill records)")
print(f"    Avg age: {employees_df['age'].mean():.1f} years")
print(f"    Retirement eligible: {employees_df['retirement_eligible'].sum()} ({employees_df['retirement_eligible'].sum()/len(employees_df)*100:.1f}%)")
print(f"    High potentials: {employees_df['high_potential'].sum()} ({employees_df['high_potential'].sum()/len(employees_df)*100:.1f}%)")

# =============================================================================
# 3. BUSINESS GROWTH TARGETS
# =============================================================================
print("\n3. Generating business growth targets...")

targets = []

# Next 12 quarters (3 years)
for quarter_offset in range(1, 13):
    quarter_date = CURRENT_DATE + timedelta(days=90 * quarter_offset)
    year = quarter_date.year
    quarter = f"Q{(quarter_date.month-1)//3 + 1}"
    
    # Revenue growth (15% annual, compounded quarterly)
    base_revenue = 50_000_000  # $50M current ARR
    quarterly_growth = 0.035  # ~15% annually
    projected_revenue = base_revenue * (1 + quarterly_growth) ** quarter_offset
    
    # Headcount targets by department (linked to revenue)
    # Engineering grows fastest, support functions grow slower
    for dept in DEPARTMENTS:
        current_hc = current_headcount[current_headcount['department']==dept]['headcount'].values[0]
        
        if dept == 'Engineering':
            growth_factor = 1.04 ** quarter_offset  # 4% per quarter
        elif dept in ['Data', 'Product']:
            growth_factor = 1.035 ** quarter_offset
        elif dept in ['Sales', 'Customer Success']:
            growth_factor = 1.03 ** quarter_offset
        elif dept == 'Marketing':
            growth_factor = 1.025 ** quarter_offset
        else:  # Support functions
            growth_factor = 1.015 ** quarter_offset
        
        target_hc = int(current_hc * growth_factor)
        
        targets.append({
            'year': year,
            'quarter': quarter,
            'department': dept,
            'target_headcount': target_hc,
            'projected_revenue': int(projected_revenue) if dept == 'Sales' else None
        })

targets_df = pd.DataFrame(targets)
targets_df.to_csv('business_targets.csv', index=False)
print(f"  ✓ Saved business_targets.csv ({len(targets_df)} quarterly targets)")

# Calculate total hiring need for next year
next_year_targets = targets_df[targets_df['year'] == 2027].groupby('department')['target_headcount'].max()
current_hc_by_dept = current_headcount.set_index('department')['headcount']
hiring_need = (next_year_targets - current_hc_by_dept).sum()
print(f"    Total hiring need for 2027: {int(hiring_need)} employees")

# =============================================================================
# 4. CRITICAL ROLES & SUCCESSION PLANNING
# =============================================================================
print("\n4. Generating succession planning data...")

# Define critical roles (typically ~10-15% of workforce)
critical_roles_list = [
    ('Engineering', 'VP', 'VP Engineering', 'High'),
    ('Engineering', 'Director', 'Director of Backend Engineering', 'High'),
    ('Engineering', 'Director', 'Director of Frontend Engineering', 'High'),
    ('Engineering', 'Senior Manager', 'Engineering Manager - Platform', 'Medium'),
    ('Product', 'VP', 'VP Product', 'High'),
    ('Product', 'Director', 'Director of Product', 'High'),
    ('Sales', 'VP', 'VP Sales', 'High'),
    ('Sales', 'Director', 'Director of Enterprise Sales', 'High'),
    ('Sales', 'Senior Manager', 'Sales Manager - East', 'Medium'),
    ('Data', 'Director', 'Director of Data Science', 'High'),
    ('Data', 'Senior Manager', 'Data Science Manager', 'Medium'),
    ('Finance', 'VP', 'CFO', 'High'),
    ('Finance', 'Director', 'Director of FP&A', 'Medium'),
    ('HR', 'VP', 'CHRO', 'High'),
    ('Marketing', 'VP', 'CMO', 'High'),
    ('Customer Success', 'Director', 'Director of Customer Success', 'High'),
    ('Operations', 'Director', 'Director of Operations', 'Medium'),
    ('Legal', 'Director', 'General Counsel', 'High')
]

critical_roles = []
succession_plans = []

for dept, level, role_name, criticality in critical_roles_list:
    # Find current incumbent
    incumbents = employees_df[
        (employees_df['department'] == dept) & 
        (employees_df['job_level'] == level)
    ]
    
    if len(incumbents) > 0:
        incumbent = incumbents.sample(1).iloc[0]
        
        critical_roles.append({
            'role_name': role_name,
            'department': dept,
            'job_level': level,
            'current_incumbent': incumbent['employee_id'],
            'incumbent_retirement_risk': incumbent['retirement_eligible'],
            'criticality': criticality,
            'time_to_fill_days': 90 if criticality == 'High' else 60
        })
        
        # Identify successors (1-3 per role)
        # Look one level below
        level_map = {
            'VP': 'Director',
            'Director': 'Senior Manager',
            'Senior Manager': 'Manager'
        }
        
        successor_level = level_map.get(level)
        if successor_level:
            potential_successors = employees_df[
                (employees_df['department'] == dept) &
                (employees_df['job_level'] == successor_level) &
                (employees_df['performance_rating'] >= 3.5)
            ]
            
            num_successors = min(random.randint(1, 3), len(potential_successors))
            
            if num_successors > 0:
                successors = potential_successors.sample(num_successors)
                
                for _, successor in successors.iterrows():
                    # Readiness assessment
                    if successor['high_potential']:
                        readiness = random.choices(
                            ['Ready Now', '1-2 Years', '2-3 Years'],
                            weights=[0.30, 0.50, 0.20]
                        )[0]
                    else:
                        readiness = random.choices(
                            ['Ready Now', '1-2 Years', '2-3 Years', '3+ Years'],
                            weights=[0.10, 0.30, 0.40, 0.20]
                        )[0]
                    
                    succession_plans.append({
                        'role_name': role_name,
                        'department': dept,
                        'current_incumbent': incumbent['employee_id'],
                        'successor_id': successor['employee_id'],
                        'successor_performance': successor['performance_rating'],
                        'successor_high_potential': successor['high_potential'],
                        'readiness': readiness,
                        'development_plan': 'Yes' if readiness != 'Ready Now' else 'No'
                    })

critical_roles_df = pd.DataFrame(critical_roles)
succession_df = pd.DataFrame(succession_plans)

critical_roles_df.to_csv('critical_roles.csv', index=False)
succession_df.to_csv('succession_plans.csv', index=False)

print(f"  ✓ Saved critical_roles.csv ({len(critical_roles_df)} critical roles)")
print(f"  ✓ Saved succession_plans.csv ({len(succession_df)} succession plans)")

# Calculate succession coverage
roles_with_successors = succession_df['role_name'].nunique()
total_critical_roles = len(critical_roles_df)
coverage_rate = (roles_with_successors / total_critical_roles) * 100

print(f"    Succession coverage: {roles_with_successors}/{total_critical_roles} roles ({coverage_rate:.1f}%)")
ready_now = len(succession_df[succession_df['readiness'] == 'Ready Now'])
print(f"    Ready now successors: {ready_now}")

# =============================================================================
# 5. ORGANIZATIONAL STRUCTURE (Span of Control)
# =============================================================================
print("\n5. Generating organizational structure data...")

org_structure = []

# Assign managers
managers = employees_df[employees_df['job_level'].isin(['Manager', 'Senior Manager', 'Director', 'VP'])].copy()
ics = employees_df[employees_df['job_level'].str.contains('IC')].copy()

for _, manager in managers.iterrows():
    dept = manager['department']
    level = manager['job_level']
    
    # Span of control varies by level
    if level == 'VP':
        span = random.randint(4, 7)
    elif level == 'Director':
        span = random.randint(5, 8)
    elif level == 'Senior Manager':
        span = random.randint(6, 10)
    else:  # Manager
        span = random.randint(6, 12)
    
    org_structure.append({
        'manager_id': manager['employee_id'],
        'manager_level': level,
        'department': dept,
        'span_of_control': span,
        'team_size': span
    })

org_df = pd.DataFrame(org_structure)
org_df.to_csv('org_structure.csv', index=False)

print(f"  ✓ Saved org_structure.csv ({len(org_df)} managers)")
avg_span = org_df['span_of_control'].mean()
print(f"    Average span of control: {avg_span:.1f}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*60)
print("DATA GENERATION COMPLETE")
print("="*60)
print(f"\nFiles created:")
print(f"  - headcount_history.csv: {len(historical_df)} monthly snapshots")
print(f"  - current_workforce.csv: {len(employees_df)} current employees")
print(f"  - employee_skills.csv: {len(skills_df)} skill records")
print(f"  - business_targets.csv: {len(targets_df)} quarterly targets")
print(f"  - critical_roles.csv: {len(critical_roles_df)} critical roles")
print(f"  - succession_plans.csv: {len(succession_df)} succession plans")
print(f"  - org_structure.csv: {len(org_df)} manager records")

print(f"\nKey Metrics:")
print(f"  Current headcount: {len(employees_df)}")
print(f"  Projected 2027 headcount: {int(next_year_targets.sum())}")
print(f"  Hiring need (2027): ~{int(hiring_need)} employees")
print(f"  Succession coverage: {coverage_rate:.1f}%")
print(f"  Retirement eligible: {employees_df['retirement_eligible'].sum()} employees")
print(f"  High potentials: {employees_df['high_potential'].sum()} employees")
print("="*60)
