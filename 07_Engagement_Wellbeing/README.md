# Domain 7: Employee Engagement & Wellbeing

## Overview
This domain measures employee engagement, identifies burnout risks, and tracks wellbeing trends to maintain a healthy, productive workforce.

## Business Impact
- **Engagement drives performance**: Highly engaged teams show 21% greater profitability (Gallup)
- **Wellbeing predicts retention**: Employees experiencing burnout are 2.6x more likely to leave
- **Prevention is cost-effective**: Addressing burnout early prevents costly turnover and performance decline

## Key Metrics
- **eNPS (Employee Net Promoter Score)**: Likelihood to recommend company as place to work
- **Engagement Index**: Composite score from survey items on satisfaction, commitment, and advocacy
- **Burnout Risk Score**: Based on work hours, stress indicators, and wellbeing survey responses
- **Work-Life Balance Score**: Self-reported balance and boundary-setting behaviors
- **Pulse Survey Participation**: Response rates indicate engagement with feedback process

## Research Foundation
- Gallup Q12 engagement framework (Harter et al., 2002)
- Maslach Burnout Inventory dimensions (Maslach & Jackson, 1981)
- WHO burnout guidelines and organizational interventions (2019)
- Job Demands-Resources model (Bakker & Demerouti, 2007)

## Analysis Notebooks

### 1. Engagement Survey Analysis (`01_engagement_survey_analysis.ipynb`)
**Purpose**: Analyze pulse survey results to identify engagement drivers and at-risk segments

**Key Analyses**:
- eNPS calculation and benchmarking
- Engagement score distribution by department, tenure, manager
- Driver analysis: Which factors most predict overall engagement?
- Engagement segmentation: Actively Disengaged → Highly Engaged

**Business Questions**:
- What is our overall engagement level compared to industry benchmarks?
- Which departments or teams have the lowest engagement?
- What are the top drivers of engagement in our organization?
- How does manager quality impact team engagement?

### 2. Wellbeing & Burnout Risk Assessment (`02_wellbeing_burnout_risk.ipynb`)
**Purpose**: Identify employees at risk of burnout and assess wellbeing indicators

**Key Analyses**:
- Burnout risk scoring model (hours worked, stress, exhaustion)
- Work-life balance assessment by role and department
- Correlation between burnout and performance/retention
- High-risk population identification and intervention targeting

**Business Questions**:
- What percentage of our workforce is at high risk of burnout?
- Which roles or departments show the highest burnout risk?
- How does burnout correlate with attrition and performance?
- Are long work hours predictive of burnout in our organization?

### 3. Engagement Trends & Action Planning (`03_engagement_trends_actions.ipynb`)
**Purpose**: Track engagement over time and evaluate effectiveness of interventions

**Key Analyses**:
- Longitudinal engagement trends (quarter-over-quarter)
- Impact of specific interventions (manager training, flexibility programs)
- Segmentation analysis: Which groups improved/declined?
- ROI of engagement initiatives through retention impact

**Business Questions**:
- Is engagement improving or declining over time?
- Which interventions have been most effective at improving engagement?
- How quickly do engagement initiatives show measurable impact?
- What is the ROI of our engagement programs through reduced attrition?

## Data Sources
- Quarterly pulse surveys (engagement, wellbeing, eNPS)
- HRIS data (work hours, PTO usage, schedule flexibility)
- Performance review data
- Attrition records
- Manager effectiveness scores

## Strategic Applications
1. **Predictive retention**: Use engagement/wellbeing as leading indicators of attrition risk
2. **Targeted interventions**: Focus resources on high-risk segments rather than blanket programs
3. **Manager accountability**: Track team-level engagement as manager performance metric
4. **Resource allocation**: Justify investment in wellbeing programs through retention ROI
5. **Cultural health monitoring**: Use engagement trends to assess organizational health

## Ethical Considerations
- **Confidentiality**: Individual survey responses must be anonymous; only report aggregated data
- **Minimum group size**: Do not report results for groups smaller than 5 people
- **No retaliation**: Ensure employees feel safe providing honest feedback without consequences
- **Action obligation**: Collecting feedback creates obligation to act on results
- **Burnout intervention**: High-risk individuals should be offered support, not punished

## Related Domains
- **Domain 2 (Retention)**: Engagement predicts attrition risk
- **Domain 5 (Manager Effectiveness)**: Manager quality drives team engagement
- **Domain 6 (Inclusion)**: Belonging scores correlate with engagement
- **Domain 8 (Compensation)**: Pay equity impacts engagement and satisfaction
