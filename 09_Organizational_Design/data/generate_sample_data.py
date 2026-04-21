"""
Generate synthetic data for Organizational Design & Collaboration analysis
Domain 9: Spans of control, collaboration networks, and organizational efficiency

Creates realistic organizational hierarchy and collaboration patterns.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
NUM_EMPLOYEES = 400
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Customer Success', 'Operations', 'HR', 'Finance']
LEVELS = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5', 'Manager', 'Senior Manager', 'Director', 'VP', 'C-Suite']

# Organizational structure parameters
TARGET_SPAN_MIN = 5
TARGET_SPAN_MAX = 9
VP_COUNT = 4
DIRECTOR_COUNT = 12
SENIOR_MGR_COUNT = 25
MANAGER_COUNT = 50

print("Generating organizational hierarchy...")

# ============================================================================
# Generate Organizational Hierarchy
# ============================================================================

employees_data = []
employee_id = 1000

# Create C-Suite (CEO)
employees_data.append({
    'employee_id': employee_id,
    'name': f'Employee_{employee_id}',
    'level': 'C-Suite',
    'department': 'Executive',
    'manager_id': None,
    'reports_count': 0  # Will update later
})
ceo_id = employee_id
employee_id += 1

# Create VPs reporting to CEO
vp_ids = []
for i in range(VP_COUNT):
    dept = DEPARTMENTS[i % len(DEPARTMENTS)]
    employees_data.append({
        'employee_id': employee_id,
        'name': f'Employee_{employee_id}',
        'level': 'VP',
        'department': dept,
        'manager_id': ceo_id,
        'reports_count': 0
    })
    vp_ids.append(employee_id)
    employee_id += 1

# Create Directors reporting to VPs
director_ids = []
for i in range(DIRECTOR_COUNT):
    manager_id = random.choice(vp_ids)
    manager_dept = [e for e in employees_data if e['employee_id'] == manager_id][0]['department']

    employees_data.append({
        'employee_id': employee_id,
        'name': f'Employee_{employee_id}',
        'level': 'Director',
        'department': manager_dept,
        'manager_id': manager_id,
        'reports_count': 0
    })
    director_ids.append(employee_id)
    employee_id += 1

# Create Senior Managers reporting to Directors
senior_mgr_ids = []
for i in range(SENIOR_MGR_COUNT):
    manager_id = random.choice(director_ids)
    manager_dept = [e for e in employees_data if e['employee_id'] == manager_id][0]['department']

    employees_data.append({
        'employee_id': employee_id,
        'name': f'Employee_{employee_id}',
        'level': 'Senior Manager',
        'department': manager_dept,
        'manager_id': manager_id,
        'reports_count': 0
    })
    senior_mgr_ids.append(employee_id)
    employee_id += 1

# Create Managers reporting to Senior Managers or Directors
manager_ids = []
for i in range(MANAGER_COUNT):
    # 70% report to Senior Managers, 30% directly to Directors
    if random.random() < 0.7 and len(senior_mgr_ids) > 0:
        manager_id = random.choice(senior_mgr_ids)
    else:
        manager_id = random.choice(director_ids)

    manager_dept = [e for e in employees_data if e['employee_id'] == manager_id][0]['department']

    employees_data.append({
        'employee_id': employee_id,
        'name': f'Employee_{employee_id}',
        'level': 'Manager',
        'department': manager_dept,
        'manager_id': manager_id,
        'reports_count': 0
    })
    manager_ids.append(employee_id)
    employee_id += 1

# Create ICs reporting to Managers
ic_levels = ['IC1', 'IC2', 'IC3', 'IC4', 'IC5']
ics_per_manager = (NUM_EMPLOYEES - len(employees_data)) // len(manager_ids)

for mgr_id in manager_ids:
    manager_dept = [e for e in employees_data if e['employee_id'] == mgr_id][0]['department']

    # Vary span of control (4-12 reports)
    num_reports = int(np.random.normal(7, 2))
    num_reports = np.clip(num_reports, 4, 12)

    for j in range(num_reports):
        if employee_id >= 1000 + NUM_EMPLOYEES:
            break

        ic_level = random.choice(ic_levels)

        employees_data.append({
            'employee_id': employee_id,
            'name': f'Employee_{employee_id}',
            'level': ic_level,
            'department': manager_dept,
            'manager_id': mgr_id,
            'reports_count': 0
        })
        employee_id += 1

employees_df = pd.DataFrame(employees_data)

# Calculate reports_count for each manager
for idx, emp in employees_df.iterrows():
    reports = len(employees_df[employees_df['manager_id'] == emp['employee_id']])
    employees_df.at[idx, 'reports_count'] = reports

# Calculate organizational distance from CEO
def calculate_distance_from_ceo(emp_id, employees_df, ceo_id):
    if emp_id == ceo_id:
        return 0

    emp = employees_df[employees_df['employee_id'] == emp_id]
    if len(emp) == 0 or pd.isna(emp.iloc[0]['manager_id']):
        return 0

    manager_id = emp.iloc[0]['manager_id']
    return 1 + calculate_distance_from_ceo(manager_id, employees_df, ceo_id)

employees_df['distance_from_ceo'] = employees_df['employee_id'].apply(
    lambda x: calculate_distance_from_ceo(x, employees_df, ceo_id)
)

# ============================================================================
# Generate Collaboration Network Data
# ============================================================================

print("Generating collaboration network...")

collaboration_data = []

# Create collaboration edges (who works with whom)
for i, emp1 in employees_df.iterrows():
    # Same department collaborations (high frequency)
    same_dept = employees_df[employees_df['department'] == emp1['department']]
    for _, emp2 in same_dept.sample(min(5, len(same_dept))).iterrows():
        if emp1['employee_id'] != emp2['employee_id']:
            collab_count = int(np.random.exponential(10) + 2)  # 2-30 interactions
            collaboration_data.append({
                'employee_1': emp1['employee_id'],
                'employee_2': emp2['employee_id'],
                'department_1': emp1['department'],
                'department_2': emp2['department'],
                'collaboration_type': 'Intra-Department',
                'interaction_count': collab_count,
                'avg_interaction_quality': round(np.random.beta(5, 2) * 5, 1)  # 1-5 scale
            })

    # Cross-department collaborations (lower frequency)
    if random.random() < 0.6:  # 60% of employees have cross-dept collabs
        other_depts = employees_df[employees_df['department'] != emp1['department']]
        for _, emp2 in other_depts.sample(min(3, len(other_depts))).iterrows():
            collab_count = int(np.random.exponential(3) + 1)  # 1-10 interactions
            collaboration_data.append({
                'employee_1': emp1['employee_id'],
                'employee_2': emp2['employee_id'],
                'department_1': emp1['department'],
                'department_2': emp2['department'],
                'collaboration_type': 'Cross-Department',
                'interaction_count': collab_count,
                'avg_interaction_quality': round(np.random.beta(4, 2) * 5, 1)
            })

collaboration_df = pd.DataFrame(collaboration_data)

# Calculate network metrics
print("Calculating network metrics...")

# Collaboration score by employee (total interactions)
employee_collab_scores = []
for emp_id in employees_df['employee_id']:
    total_interactions = collaboration_df[
        (collaboration_df['employee_1'] == emp_id) |
        (collaboration_df['employee_2'] == emp_id)
    ]['interaction_count'].sum()

    unique_connections = len(set(
        list(collaboration_df[collaboration_df['employee_1'] == emp_id]['employee_2']) +
        list(collaboration_df[collaboration_df['employee_2'] == emp_id]['employee_1'])
    ))

    cross_dept_interactions = collaboration_df[
        ((collaboration_df['employee_1'] == emp_id) | (collaboration_df['employee_2'] == emp_id)) &
        (collaboration_df['collaboration_type'] == 'Cross-Department')
    ]['interaction_count'].sum()

    employee_collab_scores.append({
        'employee_id': emp_id,
        'total_interactions': total_interactions,
        'unique_connections': unique_connections,
        'cross_dept_interactions': cross_dept_interactions,
        'collaboration_score': round(total_interactions * 0.5 + unique_connections * 2 + cross_dept_interactions * 1.5, 1)
    })

collab_scores_df = pd.DataFrame(employee_collab_scores)

# Merge with employees
employees_df = employees_df.merge(collab_scores_df, on='employee_id', how='left')

# ============================================================================
# Generate Organizational Efficiency Metrics
# ============================================================================

print("Generating efficiency metrics...")

# Calculate department-level metrics
dept_metrics = []
for dept in DEPARTMENTS:
    dept_employees = employees_df[employees_df['department'] == dept]
    dept_managers = dept_employees[dept_employees['reports_count'] > 0]
    dept_ics = dept_employees[dept_employees['reports_count'] == 0]

    if len(dept_employees) > 0:
        avg_span = dept_managers['reports_count'].mean() if len(dept_managers) > 0 else 0
        manager_ratio = len(dept_managers) / len(dept_employees) if len(dept_employees) > 0 else 0
        avg_distance = dept_employees['distance_from_ceo'].mean()

        dept_metrics.append({
            'department': dept,
            'total_employees': len(dept_employees),
            'total_managers': len(dept_managers),
            'total_ics': len(dept_ics),
            'avg_span_of_control': round(avg_span, 1),
            'manager_to_employee_ratio': round(manager_ratio, 3),
            'avg_distance_from_ceo': round(avg_distance, 1),
            'total_collaboration_score': dept_employees['collaboration_score'].sum()
        })

dept_metrics_df = pd.DataFrame(dept_metrics)

# ============================================================================
# Save all datasets
# ============================================================================

print("\nSaving datasets...")

import os
if os.path.exists('../data'):
    data_dir = '../data'
elif os.path.exists('09_Organizational_Design/data'):
    data_dir = '09_Organizational_Design/data'
else:
    os.makedirs('data', exist_ok=True)
    data_dir = 'data'

employees_df.to_csv(f'{data_dir}/org_hierarchy.csv', index=False)
collaboration_df.to_csv(f'{data_dir}/collaboration_network.csv', index=False)
dept_metrics_df.to_csv(f'{data_dir}/department_metrics.csv', index=False)

print(f"\n{'='*80}")
print("DATA GENERATION COMPLETE")
print(f"{'='*80}")
print(f"Generated {len(employees_df)} employees in organizational hierarchy")
print(f"Generated {len(collaboration_df)} collaboration relationships")
print(f"Generated metrics for {len(dept_metrics_df)} departments")
print(f"\nDatasets saved to {data_dir}/")
print(f"{'='*80}")

# Print summary statistics
print("\n🏢 ORGANIZATIONAL STRUCTURE")
print(f"{'='*80}")
print(f"Total employees: {len(employees_df)}")
print(f"Total managers:  {len(employees_df[employees_df['reports_count'] > 0])}")
print(f"Manager ratio:   {len(employees_df[employees_df['reports_count'] > 0])/len(employees_df)*100:.1f}%")
print(f"Organizational layers: {employees_df['distance_from_ceo'].max()}")
print(f"Average distance from CEO: {employees_df['distance_from_ceo'].mean():.1f}")

print("\n📊 SPANS OF CONTROL")
print(f"{'='*80}")
managers = employees_df[employees_df['reports_count'] > 0]
print(f"Average span: {managers['reports_count'].mean():.1f}")
print(f"Median span:  {managers['reports_count'].median():.1f}")
print(f"Min span:     {managers['reports_count'].min()}")
print(f"Max span:     {managers['reports_count'].max()}")
print(f"Spans outside optimal range (5-9): {((managers['reports_count'] < 5) | (managers['reports_count'] > 9)).sum()} managers")

print("\n🤝 COLLABORATION")
print(f"{'='*80}")
print(f"Total collaboration relationships: {len(collaboration_df)}")
intra_dept = len(collaboration_df[collaboration_df['collaboration_type'] == 'Intra-Department'])
cross_dept = len(collaboration_df[collaboration_df['collaboration_type'] == 'Cross-Department'])
print(f"Intra-department: {intra_dept} ({intra_dept/len(collaboration_df)*100:.1f}%)")
print(f"Cross-department: {cross_dept} ({cross_dept/len(collaboration_df)*100:.1f}%)")
print(f"Average connections per employee: {employees_df['unique_connections'].mean():.1f}")

print(f"\n{'='*80}")
print("✅ All datasets ready for analysis!")
print(f"{'='*80}\n")
