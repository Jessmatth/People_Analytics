# Retention & Attrition Risk

## Overview

Retention is one of the highest-impact areas in people analytics. The cost of losing key talent includes replacement costs (recruiting, onboarding), productivity loss during vacancy, institutional knowledge loss, and team morale impact. This domain focuses on understanding why employees leave, predicting who is at risk, and designing data-driven retention interventions.

**Problem Statement**: Organizations often react to attrition rather than prevent it. By the time an employee gives notice, it's typically too late. This domain enables proactive retention through early warning systems and root cause analysis.

---

## Business Impact

### Cost of Attrition

**Direct Costs**:
- Recruiting costs (job boards, agency fees, recruiter time)
- Onboarding and training costs for replacement
- Sign-on bonuses and relocation for replacement

**Indirect Costs**:
- Lost productivity during vacancy (typically 0.5-1% of salary per day)
- Reduced team productivity (knowledge gaps, extra workload)
- Institutional knowledge loss
- Customer relationship disruption
- Team morale and engagement impact

**Industry Benchmarks**:
- Voluntary attrition cost: **50-200% of annual salary**
  - Entry-level: 50% of salary ($25K for $50K role)
  - Mid-level: 100-125% of salary ($75-94K for $75K role)
  - Senior/specialist: 150-200% of salary ($180-240K for $120K role)

**Example ROI Calculation**:
```
Company: 500 employees, 15% annual attrition (75 departures)
Average salary: $80,000
Cost per departure: 100% of salary = $80,000

Annual attrition cost: 75 × $80,000 = $6,000,000

If analytics reduces attrition by 3 percentage points (15% → 12%):
- Prevented departures: 15 employees
- Savings: 15 × $80,000 = $1,200,000/year

Investment in analytics: $150,000 (headcount + tools)
ROI: 8x in year one
```

---

## Key Metrics & KPIs

| Metric | Definition | Target | Why It Matters |
|--------|------------|--------|----------------|
| **Overall Attrition Rate** | (# departures / avg headcount) × 100 | <12% annually | Industry benchmark comparison |
| **Voluntary Attrition Rate** | (# voluntary departures / avg headcount) × 100 | <10% annually | What you can influence |
| **Regrettable Attrition Rate** | (# regrettable departures / avg headcount) × 100 | <5% annually | Loss of high performers |
| **90-Day New Hire Attrition** | % of new hires leaving within 90 days | <5% | Early warning of hiring/onboarding issues |
| **Flight Risk Score** | Predictive score (0-100) of departure likelihood | Model-dependent | Enables proactive intervention |
| **Retention Rate** | % of employees from cohort still employed after X months | >85% at 12mo | Inverse of attrition |
| **Average Tenure** | Mean years of service | 3-5 years | Stability indicator |
| **Cost per Departure** | Total attrition costs / # departures | Varies by role | ROI justification |

---

## Core Analyses

### 1. Attrition Trend Analysis
**Purpose**: Identify patterns in who leaves, when, and from where.

**Key Questions**:
- What is the overall attrition rate trend? Seasonal patterns?
- Which departments/teams/managers have highest attrition?
- What tenure groups are most at risk? (0-1yr, 1-2yr, 3-5yr, 5+yr)
- Which job levels or roles have highest turnover?
- Are there demographic disparities in attrition?

**Analyses**:
- Monthly/quarterly attrition rates with trend lines
- Attrition heat maps by department × tenure
- Cohort survival curves (% remaining by months since hire)
- Manager-level attrition benchmarking
- Voluntary vs. involuntary breakdown

**Output**: Executive dashboard showing attrition hot spots and trends.

---

### 2. Attrition Drivers & Root Cause Analysis
**Purpose**: Understand WHY employees leave.

**Key Questions**:
- What factors correlate with higher attrition? (compensation, engagement, promotion velocity, manager quality)
- Do employees who leave have different profiles than those who stay?
- What are exit interview themes?
- How does compensation competitiveness affect retention?

**Analyses**:
- Correlation analysis: attrition vs. compensation percentile, engagement scores, promotion gaps, manager tenure
- T-tests comparing leavers vs. stayers on key metrics
- Exit interview sentiment analysis and theme extraction
- Compensation benchmarking for departed employees
- Time since last promotion analysis

**Output**: Root cause report identifying top 3-5 retention drivers.

---

### 3. Flight Risk Prediction Model
**Purpose**: Identify employees at high risk of leaving BEFORE they resign.

**Key Questions**:
- Which employees are most likely to leave in the next 6-12 months?
- What early warning signals predict attrition?
- How accurate is the prediction model?

**Approach**:
- **Model Type**: Classification (logistic regression, random forest, XGBoost)
- **Target Variable**: Left within next 12 months (Yes/No)
- **Features**:
  - Tenure, time since last promotion, time since last raise
  - Compensation percentile vs. market/peers
  - Engagement survey scores and trends
  - Performance rating and trend
  - Manager tenure and team attrition rate
  - Job changes/transfers in last 2 years
  - Commute distance, remote work status
  - Demographics (age, job level)

**Output**:
- Flight risk score (0-100) for each active employee
- Monthly risk tier lists (High/Medium/Low)
- Feature importance analysis (what drives risk)
- Model performance metrics (AUC, precision/recall)

**Use Case**: HR business partners receive monthly lists of high-risk employees to enable proactive conversations and retention offers.

---

### 4. Regrettable vs. Non-Regrettable Attrition
**Purpose**: Focus retention efforts on high-value employees.

**Key Questions**:
- What % of attrition is regrettable (high performers/critical roles)?
- Do regrettable and non-regrettable departures have different patterns?
- Which interventions reduce regrettable attrition?

**Classification Criteria**:
- **Regrettable**: High/excellent performance rating AND (critical role OR hard-to-replace skills)
- **Non-Regrettable**: Low performance rating OR role elimination OR voluntary retirement

**Analyses**:
- Regrettable attrition rate by department
- Profile comparison: regrettable vs. non-regrettable leavers
- Cost impact analysis (regrettable departures cost more)
- Intervention effectiveness tracking

**Output**: Regrettable attrition dashboard and targeted retention programs.

---

### 5. Cohort Retention Analysis
**Purpose**: Track retention over time for specific groups.

**Key Questions**:
- How long do employees hired in each year stay?
- Which recruiting sources produce employees who stay longer?
- Do certain onboarding cohorts have better retention?
- How does retention differ by hire location or remote status?

**Analyses**:
- Survival curves by hire year cohort
- Retention rates at 90 days, 6 months, 1 year, 2 years
- Source-of-hire retention comparison (referrals vs. agencies vs. job boards)
- University recruiting cohort tracking
- Remote vs. in-office hire retention

**Output**: Cohort retention report informing recruiting and onboarding strategy.

---

### 6. Retention Intervention Effectiveness
**Purpose**: Measure impact of retention programs.

**Key Questions**:
- Do retention bonuses work? What's the ROI?
- Does career development (mentoring, promotions, rotations) improve retention?
- How effective are stay interviews vs. exit interviews?
- What's the retention impact of compensation adjustments?

**Experimental Design**:
- **A/B Testing**: Randomly assign high-risk employees to intervention vs. control
- **Propensity Score Matching**: Compare similar employees who received intervention vs. those who didn't
- **Pre/Post Analysis**: Retention rates before and after program launch

**Interventions to Test**:
- Retention bonuses for high-risk high performers
- Career development plans and mentoring
- Compensation equity adjustments
- Manager training on retention conversations
- Flexible work arrangements

**Output**: Intervention ROI report showing cost vs. retention benefit.

---

## Sample Dashboards

### Executive Attrition Dashboard
**Audience**: CHRO, executive team
**Refresh**: Monthly
**KPIs**:
- Overall attrition rate (trailing 12 months)
- Voluntary vs. involuntary breakdown
- Regrettable attrition rate
- Cost of attrition (YTD)
- Attrition by division/function
- Year-over-year comparison

**Visualizations**:
- Trend line: Monthly attrition rate
- Heat map: Attrition by department × tenure
- Bar chart: Top 10 teams by attrition rate
- Waterfall: Attrition cost breakdown

---

### Flight Risk Dashboard
**Audience**: HR business partners, managers
**Refresh**: Monthly
**Content**:
- High-risk employee list (filtered by HRBP's scope)
- Risk score distribution
- Risk factors contributing to scores
- Suggested interventions by risk tier

**Use Case**: HRBPs review monthly and schedule proactive stay conversations with high-risk individuals.

---

### Attrition Drivers Dashboard
**Audience**: People analytics team, CHRO
**Refresh**: Quarterly
**Content**:
- Correlation analysis: Key drivers of attrition
- Comparison: Leavers vs. stayers on compensation, engagement, promotion velocity
- Exit interview themes and sentiment
- Recommendations for retention programs

---

## Data Sources

| Source | Key Fields | Use Case |
|--------|------------|----------|
| **HRIS** | Employee ID, hire date, termination date, termination reason, job title, department, manager, location, employment status | Core attrition calculations, trend analysis |
| **Compensation** | Base salary, total comp, merit increase %, bonus, equity, market percentile | Compensation competitiveness analysis |
| **Performance Management** | Performance rating, goal achievement, promotion history, time since last promotion | Performance vs. attrition correlation |
| **Engagement Surveys** | Overall engagement score, eNPS, manager effectiveness score, growth opportunity score | Engagement as attrition predictor |
| **Talent Reviews** | High potential designation, flight risk flag, succession plan status, critical role flag | Regrettable attrition identification |
| **Exit Interviews** | Reason for leaving, would rehire (Yes/No), sentiment score, open-ended comments | Root cause analysis |
| **Recruiting Data** | Source of hire, requisition ID, hiring manager | Cohort retention by source |

---

## Tools & Technologies

**Data Infrastructure**:
- **Database**: PostgreSQL, Snowflake, or BigQuery for data warehouse
- **ETL**: Python (pandas), dbt, or Fivetran for data pipelines

**Analysis & Modeling**:
- **Python Libraries**: pandas, scikit-learn, XGBoost, lifelines (survival analysis), matplotlib, seaborn
- **Statistical Analysis**: Correlation testing, t-tests, chi-square, survival curves, logistic regression
- **Machine Learning**: Random forest, XGBoost for flight risk prediction

**Dashboards**:
- **BI Tools**: Tableau, Power BI, Looker, or Mode Analytics
- **Reporting**: Jupyter notebooks for ad-hoc analysis

**Survey Analysis**:
- **Text Analytics**: NLTK, spaCy for exit interview sentiment analysis

---

## Best Practices

### 1. Focus on Regrettable Attrition
Not all attrition is bad. Low performers leaving can be healthy. Prioritize reducing regrettable attrition (high performers, critical roles).

### 2. Act on Flight Risk Scores
Predictive models are only valuable if action is taken. Establish a process for HRBPs to review high-risk employees monthly and take proactive steps.

### 3. Conduct Stay Interviews, Not Just Exit Interviews
By the time someone resigns, it's usually too late. Proactive "stay interviews" with high-risk or high-value employees are more effective.

### 4. Track Intervention Effectiveness
Don't just implement retention programs—measure their impact. Use A/B testing or propensity score matching to isolate program effects.

### 5. Address Manager Quality
The #1 reason people leave is their manager. Identify high-attrition managers and provide coaching or leadership development.

### 6. Analyze Early-Tenure Attrition Separately
Employees leaving in the first 90 days signal hiring or onboarding issues. Track this separately and investigate root causes.

### 7. Benchmark Externally
Compare attrition rates to industry benchmarks (SHRM, LinkedIn reports) to understand if your rates are competitive.

### 8. Use Survival Analysis for Cohorts
Survival curves (Kaplan-Meier) are more informative than simple retention percentages because they show time-to-event patterns.

### 9. Protect Employee Privacy
Flight risk scores are sensitive. Limit access to HRBPs and ensure managers use them appropriately (as a conversation starter, not a punishment trigger).

### 10. Combine Quantitative + Qualitative Data
Numbers show patterns, but exit interviews and stay interviews reveal the "why." Use both to build a complete picture.

---

## Common Pitfalls

### 1. Treating All Attrition Equally
**Problem**: Losing a low performer is different from losing a top performer. Undifferentiated attrition rates obscure the real issue.
**Solution**: Track regrettable attrition separately and weight by employee value.

### 2. Ignoring Involuntary Attrition
**Problem**: Focusing only on voluntary attrition misses performance management issues.
**Solution**: Track involuntary attrition trends—spikes may indicate manager issues or unclear performance expectations.

### 3. Building Flight Risk Models Without Action Plans
**Problem**: Predictive models gather dust if no one acts on the insights.
**Solution**: Establish ownership (HRBPs) and a monthly review process before deploying the model.

### 4. Not Updating Models Regularly
**Problem**: Labor markets change. A model trained in 2023 may be inaccurate in 2025.
**Solution**: Retrain models quarterly or annually with fresh data.

### 5. Over-Relying on Exit Interview Data
**Problem**: Exit interviews are biased (people don't always tell the truth) and backward-looking.
**Solution**: Use exit interviews for themes, but prioritize real-time engagement data and stay interviews.

### 6. Ignoring Manager Impact
**Problem**: Treating attrition as an organizational issue when it's often manager-specific.
**Solution**: Calculate manager-level attrition rates and identify outliers for coaching.

### 7. Not Segmenting by Tenure
**Problem**: A 90-day departure has different causes than a 5-year departure.
**Solution**: Analyze attrition by tenure buckets (0-3mo, 3-12mo, 1-2yr, 2-5yr, 5+yr).

### 8. Retention Programs Without ROI Tracking
**Problem**: Spending money on retention bonuses or programs without knowing if they work.
**Solution**: Track pre/post retention rates and calculate ROI (savings from prevented attrition vs. program cost).

---

## Getting Started

### Immediate (This Week)
1. Calculate overall and voluntary attrition rates for last 12 months
2. Identify top 5 departments/teams with highest attrition
3. Gather exit interview data for last 6 months

### Short-term (This Month)
1. Build attrition trend dashboard (monthly rates, by department)
2. Analyze attrition by tenure and job level
3. Compare compensation of leavers vs. stayers
4. Identify regrettable vs. non-regrettable departures

### Long-term (This Quarter)
1. Build flight risk prediction model
2. Pilot stay interview program with high-risk employees
3. Implement retention intervention experiments (bonuses, career development)
4. Create manager-level attrition scorecards

---

## Related Analyses

- **[Talent Acquisition](../01_Talent_Acquisition_Quality_of_Hire/)**: Cohort retention by source of hire informs recruiting strategy
- **Performance Management**: Performance ratings are key predictors of attrition
- **Compensation Equity**: Pay competitiveness is a top retention driver
- **Engagement & Culture**: Engagement scores predict attrition risk
- **Succession Planning**: Flight risk scores identify critical succession gaps

---

## Example Questions This Analysis Answers

1. What is our current attrition rate and how does it compare to last year?
2. Which teams or managers have the highest attrition rates?
3. Why are employees leaving? (compensation, manager, growth, work-life balance)
4. Who is at highest risk of leaving in the next 6 months?
5. How much does attrition cost us annually?
6. Are we losing our best performers or our low performers?
7. How long do employees from different recruiting sources stay?
8. Do retention bonuses work? What's the ROI?
9. Which factors are most predictive of attrition?
10. How can we proactively reduce regrettable attrition?

---

**Last Updated**: April 20, 2026
