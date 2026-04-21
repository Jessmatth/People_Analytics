# Retention & Attrition Risk

## Overview
Predicts employee attrition risk, identifies retention drivers, and enables proactive intervention to reduce costly turnover. Focuses on understanding why employees leave before they resign.

## Business Impact
- Voluntary attrition costs 50-200% of annual salary per departure
- Example: 500 employees, 15% attrition rate = $6M annual cost
- 3 percentage point reduction (15%→12%) saves $1.2M annually
- High performer attrition costs 2x more than average employee turnover
- Flight risk models enable proactive retention interventions

## Key Metrics
- Overall Attrition Rate (target: <12% annually) - Industry benchmark comparison
- Voluntary Attrition Rate (target: <10% annually) - What you can influence
- Regrettable Attrition Rate (target: <5% annually) - Loss of high performers
- 90-Day New Hire Attrition (target: <5%) - Hiring/onboarding quality signal
- Flight Risk Score (0-100) - Predictive model for departure likelihood
- Retention Rate at 12 months (target: >85%) - Inverse of attrition

## Notebooks

### 1. Attrition Trend Analysis
Identifies patterns in who leaves, when, and from where.

**Key outputs:** Attrition rates by department/tenure, seasonal patterns, manager-level benchmarking, cohort survival curves

### 2. Attrition Drivers & Root Cause Analysis
Understands WHY employees leave through correlation and exit interview analysis.

**Key outputs:** Top 3-5 retention drivers, leavers vs stayers comparison, compensation competitiveness, exit interview themes

### 3. Flight Risk Prediction Model
Identifies employees at high risk of leaving before they resign.

**Key outputs:** Flight risk scores (0-100) per employee, monthly risk tier lists, feature importance, model accuracy metrics

### 4. Regrettable vs Non-Regrettable Attrition
Focuses retention efforts on high-value employees.

**Key outputs:** Regrettable attrition rate by department, profile comparisons, intervention effectiveness tracking

### 5. Cohort Retention Analysis
Tracks retention over time for specific groups.

**Key outputs:** Survival curves by hire year, retention by recruiting source, university cohort tracking

### 6. Retention Intervention Effectiveness
Measures impact of retention programs through A/B testing or propensity matching.

**Key outputs:** Intervention ROI analysis, retention bonus effectiveness, career development program impact

## Data Requirements
- HRIS: Hire date, termination date, job history, manager, location
- Compensation: Salary, market percentile, merit increases
- Performance Management: Ratings, promotion history
- Engagement Surveys: Engagement scores, eNPS, manager effectiveness
- Exit Interviews: Reason for leaving, sentiment, themes

## Best Practices
- Focus on regrettable attrition (not all turnover is bad)
- Conduct stay interviews, not just exit interviews
- Track intervention effectiveness with experiments
- Address manager quality (top reason people leave)
- Analyze early-tenure attrition separately (signals hiring/onboarding issues)

## Related Analyses
- Domain 1: Talent Acquisition (cohort retention by source informs recruiting)
- Domain 4: Performance (performance ratings predict attrition)
- Domain 7: Engagement (engagement scores predict retention)
- Domain 8: Compensation (pay competitiveness drives retention)

---
*Part of the People Analytics repository | Last updated: April 2026*
