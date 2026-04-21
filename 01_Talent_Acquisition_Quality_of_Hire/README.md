# Talent Acquisition & Quality of Hire

## Overview
Analyzes recruiting effectiveness and quality of hire to optimize sourcing channels, interview processes, and candidate selection. Identifies which recruiting channels and candidate attributes predict on-the-job success.

## Business Impact
- Bad hires cost 30-50% of annual salary in recruiting, training, and productivity loss
- Each vacant day costs 0.5% of annual salary in lost productivity
- 25% reduction in time-to-fill saves $500K+ annually (500-person company)
- 10% improvement in quality of hire generates $1M+ in productivity gains
- Better sourcing allocation reduces cost-per-hire by 20-30%

## Key Metrics

**Recruiting Efficiency:**
- Time-to-Fill (target: 30-45 days) - Speed of hiring process
- Cost-per-Hire (target: $3K-$5K) - Total recruiting costs divided by hires
- Offer Acceptance Rate (target: >85%) - Competitiveness of offers
- Application Completion Rate (target: >70%) - Candidate experience indicator

**Quality of Hire:**
- Performance Rating at 12 months (target: ≥3.5/5) - Most direct quality measure
- Retention Rate at 12 months (target: >90%) - Early turnover indicates bad hires
- 90-Day Regrettable Attrition (target: <5%) - Signal of mis-hire
- Time-to-Productivity - How quickly new hires reach full effectiveness

**Predictive Factors (Schmidt & Hunter meta-analyses):**
- Structured interviews (0.51 correlation with performance)
- Work sample tests (0.54 correlation)
- Cognitive ability tests (0.51 correlation)
- References (0.26 correlation)
- Years of experience (0.15 correlation)
- Education level (0.10 correlation)

## Notebooks

### 1. Source of Hire Effectiveness
Analyzes which recruiting channels produce the best hires.

**Key outputs:** Quality of hire by source, cost-per-hire comparison, ROI analysis, sourcing recommendations

### 2. Interview Process Optimization
Correlates interview components with performance outcomes.

**Key outputs:** Interview predictive validity, structured vs unstructured effectiveness, interviewer bias analysis

### 3. Quality of Hire Prediction Model
Builds ML model to predict candidate success before hiring.

**Key outputs:** Candidate risk scores, feature importance, model performance metrics (AUC, precision/recall)

### 4. Time-to-Fill Bottleneck Analysis
Maps candidate flow through hiring funnel to identify delays.

**Key outputs:** Funnel conversion rates, stage duration analysis, bottleneck identification

### 5. Diversity Pipeline Analysis
Tracks demographic composition at each funnel stage.

**Key outputs:** Conversion rates by demographic, bias pattern identification, intervention recommendations

## Data Requirements
- Applicant Tracking System (ATS): Applications, interviews, offers, hires
- HRIS: Employee records, demographics, job history
- Performance Management: Performance ratings, reviews
- Optional: Assessment platforms, candidate surveys, background checks

## Related Analyses
- Domain 2: Retention (cohort retention by source informs recruiting)
- Domain 3: Workforce Planning (hiring roadmap based on workforce needs)
- Domain 6: Inclusion (diversity funnel analysis)

---
*Part of the People Analytics repository | Last updated: April 2026*
