# Talent Acquisition & Quality of Hire

## 🎯 Overview

**The Problem**: Organizations spend millions on recruiting but often can't answer basic questions like "Which sourcing channels produce our best hires?" or "What predicts on-the-job success?" Without data, talent acquisition operates on gut feel, resulting in bad hires, extended vacancies, and wasted resources.

**What Analytics Solves**:
- Identify which sourcing channels, candidate attributes, and interview processes predict on-the-job success
- Reduce bad hires and time-to-fill
- Optimize recruiting spend and resource allocation
- Improve candidate experience and employer brand
- Make hiring decisions based on evidence, not intuition

---

## 💰 Business Impact

**Cost of a Bad Hire**:
- Direct costs: 30-50% of annual salary (recruiting, training, severance)
- Indirect costs: Team productivity loss, morale impact, customer relationships
- Average cost: $15,000 - $240,000 depending on role level

**Time-to-Fill Impact**:
- Each vacant day costs: 0.5% of annual salary
- 90-day vacancy for $100K role = $13,700 in lost productivity
- Extended vacancies burden existing team, risk project delays

**ROI of Analytics**:
- 25% reduction in time-to-fill → $500K+ savings (500-person company)
- 10% improvement in quality of hire → $1M+ in productivity gains
- Better sourcing allocation → 20-30% reduction in cost-per-hire

---

## 📊 Key Metrics & KPIs

### Input Metrics (Recruiting Efficiency)

| Metric | Definition | Target | Why It Matters |
|--------|------------|--------|----------------|
| **Time-to-Fill** | Days from req opened to offer accepted | 30-45 days | Measures recruiting speed; long cycles cost productivity |
| **Time-to-Hire** | Days from application to offer accepted | 20-30 days | Candidate experience metric; long waits = lost candidates |
| **Cost-per-Hire** | Total recruiting costs / # hires | $3K-$5K | Efficiency metric; optimize spend allocation |
| **Source-of-Hire** | % hires by channel (referral, LinkedIn, etc.) | Varies | Shows where candidates come from |
| **Application Completion Rate** | % who start vs. finish application | >70% | Candidate experience; complex forms lose talent |
| **Offer Acceptance Rate** | % offers accepted | >85% | Market competitiveness; selling effectiveness |
| **Requisition Fill Rate** | % reqs filled within target time | >90% | Overall recruiting effectiveness |

### Output Metrics (Quality of Hire)

| Metric | Definition | Target | Why It Matters |
|--------|------------|--------|----------------|
| **Performance Rating** | Avg performance score at 12 months | ≥3.5/5 | Most direct quality measure |
| **Retention Rate** | % hired still employed at 12/24 months | >90% @ 12mo | Bad hires leave early; costly turnover |
| **Hiring Manager Satisfaction** | Survey score on hire quality | >4/5 | Stakeholder perception of TA value |
| **90-Day Regrettable Attrition** | % top performers who leave <90 days | <5% | Signal of mis-hire or poor onboarding |
| **Promotion Rate** | % promoted within 2 years | 15-25% | High performers advance faster |
| **Time-to-Productivity** | Days until fully productive | Role-dependent | Faster = better hire or onboarding |

### Predictive Metrics (What Predicts Success)

| Factor | Measurement | Predictive Power |
|--------|-------------|------------------|
| **Structured Interview Scores** | Behavioral/situational scoring | High (0.51 correlation) |
| **Work Sample Tests** | Job-relevant task performance | Very High (0.54) |
| **Cognitive Ability Tests** | Problem-solving assessments | Very High (0.51) |
| **References** | Structured reference checks | Moderate (0.26) |
| **Years of Experience** | Total years in field | Low (0.15) |
| **Education Level** | Degree attainment | Low (0.10) |
| **Unstructured Interviews** | Casual conversation | Very Low (0.14) |

*Correlation values from meta-analyses (Schmidt & Hunter, 1998; updated)*

---

## 🔍 Core Analyses

### 1. Source of Hire Effectiveness

**Question**: Which recruiting channels produce the best hires?

**Analysis**:
- Track quality of hire by source (referrals, LinkedIn, agencies, job boards, career site)
- Compare performance ratings, retention, promotion rates by source
- Calculate cost-per-hire and time-to-fill by source
- ROI = (Quality Score / Cost) × Volume

**Common Findings**:
- Referrals often produce highest quality (but limited volume)
- Agency hires cost 3-5x more but fill faster for specialized roles
- Job boards produce high volume but lower average quality
- LinkedIn effective for mid-senior roles; career site for entry-level

**Action**: Reallocate budget to high-ROI sources; improve low-performing channels

---

### 2. Interview Process Optimization

**Question**: Which interview components predict performance?

**Analysis**:
- Correlate interview scores (by type) with performance outcomes
- Test structured vs. unstructured interview effectiveness
- Identify interviewer bias (consistency, rating distributions)
- Measure candidate experience by interview stage

**Common Findings**:
- Structured behavioral interviews outperform casual conversations
- Panel interviews reduce individual bias
- Work sample/case studies highly predictive for technical roles
- Culture fit questions weakly predictive (often bias proxy)

**Action**: Replace low-signal steps; train interviewers; standardize scoring

---

### 3. Time-to-Fill Bottleneck Analysis

**Question**: Where do candidates drop off or delays occur?

**Analysis**:
- Map candidate flow through funnel (apply → screen → interview → offer)
- Calculate conversion rates and time spent at each stage
- Identify bottlenecks (e.g., long scheduling, slow approvals)
- Segment by role family, level, department

**Common Findings**:
- 40-60% of time is scheduling/admin (not interviewing)
- Hiring manager delays (not responding) = top bottleneck
- Executive approvals add 7-14 days for senior roles
- Candidates withdraw most during long silent periods

**Action**: Automate scheduling; set SLAs; improve communication

---

### 4. Candidate Experience Analysis

**Question**: What drives positive candidate experience?

**Analysis**:
- Survey candidates (hired and not hired) on experience
- Correlate experience metrics with offer acceptance
- Analyze application drop-off points
- Review Glassdoor/employer review sites

**Common Findings**:
- Communication frequency > content (just update them!)
- Application length >15 min = 40% drop-off
- Rejected candidates who get feedback = better brand perception
- Slow process = top complaint, even for hired candidates

**Action**: Simplify application; improve communication; offer feedback

---

### 5. Diversity Pipeline Analysis

**Question**: Where do we lose diverse candidates?

**Analysis**:
- Track demographic composition at each funnel stage
- Compare application → hire conversion rates by group
- Identify stages with disproportionate attrition
- Analyze interview scores for bias patterns

**Common Findings**:
- Referrals often reduce diversity (homophily bias)
- Resume screening can filter out non-traditional backgrounds
- Unstructured interviews amplify bias
- "Culture fit" often coded bias

**Action**: Blind resume review; structured interviews; diverse panels

---

### 6. Quality of Hire Prediction Model

**Question**: Can we predict who will succeed before hiring?

**Analysis**:
- Build predictive model: Candidate attributes → Performance outcome
- Features: Interview scores, assessments, experience, education, source
- Model types: Logistic regression, random forest, XGBoost
- Validate on holdout set; measure AUC, precision, recall

**Common Findings**:
- Structured interview + work sample = best predictors
- Resume credentials (GPA, school prestige) often non-predictive
- Models identify "false positives" (look good, perform poorly)
- 70-80% accuracy achievable with quality data

**Action**: Prioritize high-signal assessments; flag risky hires for support

---

## 📈 Sample Dashboards

### Executive Dashboard
- Total hires this quarter vs. target
- Average time-to-fill trend (12 months)
- Quality of hire score (composite metric)
- Cost-per-hire by department
- Open requisitions by age

### Recruiter Dashboard
- My open reqs and days open
- Candidates by stage (pipeline view)
- Interview-to-offer conversion rate
- Offers pending/accepted/declined
- Upcoming interviews and tasks

### Hiring Manager Dashboard
- My open reqs and pipeline
- Time-to-fill for my department
- Quality of hire for my past hires
- Candidate feedback summaries
- Interview schedule

---

## 📁 Data Sources

### Required Data

**Applicant Tracking System (ATS)**:
- Greenhouse, Lever, Workday Recruiting, iCims, Taleo
- Data: Applications, candidates, interviews, offers, hires
- Refresh: Daily or real-time

**HRIS (Human Resources Information System)**:
- Workday, SAP SuccessFactors, Oracle HCM, BambooHR
- Data: Employee records, demographics, job history
- Refresh: Daily

**Performance Management System**:
- Workday, SuccessFactors, Lattice, 15Five, Culture Amp
- Data: Performance ratings, goals, reviews
- Refresh: Post-review cycles (quarterly/annually)

### Optional Data

- **Sourcing Tools**: LinkedIn Recruiter, Indeed, Glassdoor
- **Assessment Platforms**: HireVue, Pymetrics, Criteria
- **Background Check**: Checkr, Sterling, HireRight
- **Surveys**: Candidate experience surveys (Qualtrics, SurveyMonkey)
- **Calendar Data**: Interview scheduling (Calendly, Goodtime)

---

## 🛠️ Tools & Technologies

### Analysis
- **Python**: pandas, numpy, scikit-learn, scipy
- **R**: dplyr, ggplot2, survival analysis
- **SQL**: Data extraction from ATS/HRIS

### Visualization
- **Tableau / Power BI**: Executive dashboards
- **Looker / Metabase**: Self-service analytics
- **Plotly / Streamlit**: Interactive web apps

### Predictive Modeling
- **scikit-learn**: Logistic regression, random forest
- **XGBoost / LightGBM**: Gradient boosting
- **Survival Analysis**: Time-to-event models (attrition, promotion)

---

## 📚 Best Practices

### Data Quality
- ✅ Clean source-of-hire data (standardize naming)
- ✅ Link ATS candidate ID to HRIS employee ID
- ✅ Validate performance data completeness (not all rated)
- ✅ Handle selection bias (only analyzing hires, not rejected candidates)

### Metrics Design
- ✅ Define "quality of hire" clearly and consistently
- ✅ Set appropriate measurement timeframe (6-12 months for performance)
- ✅ Benchmark against industry/role-specific standards
- ✅ Use composite metrics (not single score)

### Analysis Rigor
- ✅ Control for confounds (role, level, department, tenure)
- ✅ Use statistical significance tests (not just descriptive stats)
- ✅ Validate findings on holdout samples
- ✅ Consider sample size limitations (small hires = noisy data)

### Storytelling
- ✅ Lead with business impact ("$500K waste on ineffective channel")
- ✅ Show trends over time (not just point-in-time)
- ✅ Segment by relevant dimensions (role family, level)
- ✅ Include confidence intervals and caveats

---

## ⚠️ Common Pitfalls

### 1. Survivorship Bias
**Problem**: Only analyzing hired candidates ignores rejected candidates who may have succeeded

**Solution**: Track "false negatives" by surveying rejected candidates who succeeded elsewhere

### 2. Short Measurement Window
**Problem**: Measuring quality at 3 months misses long-term performance

**Solution**: Use 12-24 month performance as primary outcome; supplement with early signals

### 3. Confounding Variables
**Problem**: "Referrals produce better hires" might reflect easier roles or manager bias

**Solution**: Control for role difficulty, manager, and other factors; use regression models

### 4. Sample Size Issues
**Problem**: "Marketing hires from Source X are better" with n=3

**Solution**: Report confidence intervals; combine small segments; require minimum sample size

### 5. Gaming the Metrics
**Problem**: Recruiters optimize for time-to-fill by hiring worse candidates faster

**Solution**: Balanced scorecard (efficiency + quality); avoid single-metric incentives

---

## 📖 Key Questions This Analysis Answers

### Strategic Questions
- Which recruiting sources should we invest in (or cut)?
- Should we hire for skills or potential?
- Is our interview process predictive of performance?
- Where should we focus diversity recruiting efforts?
- Are we hiring fast enough to support business growth?

### Operational Questions
- Why is time-to-fill increasing?
- Which recruiters are most effective?
- What's causing low offer acceptance rates?
- Where do candidates drop out of our process?
- Are hiring managers satisfied with candidate quality?

### Predictive Questions
- Who is likely to be a top performer?
- Which offers are at risk of rejection?
- Will this candidate stay >2 years?
- What interview score predicts success?
- How many applications do we need to fill 10 roles?

---

## 📂 Files in This Folder

- `data/` - Sample recruiting datasets
  - `candidates.csv` - Candidate applications and demographics
  - `interviews.csv` - Interview stages and scores
  - `hires.csv` - Hired candidates with outcomes
  - `requisitions.csv` - Open and closed job requisitions

- `notebooks/` - Jupyter analysis notebooks
  - `01_source_of_hire_analysis.ipynb` - Channel effectiveness
  - `02_time_to_fill_analysis.ipynb` - Funnel and bottlenecks
  - `03_quality_of_hire_prediction.ipynb` - ML prediction model
  - `04_interview_effectiveness.ipynb` - Interview validity
  - `05_diversity_pipeline.ipynb` - Diversity funnel analysis

- `dashboards/` - Visualization templates
  - `executive_dashboard.twbx` - Tableau dashboard
  - `recruiter_metrics.pbix` - Power BI dashboard
  - `hiring_manager_view.py` - Streamlit app

- `docs/` - Supporting documentation
  - `metrics_definitions.md` - Detailed metric definitions
  - `data_dictionary.md` - Field descriptions
  - `analysis_methodology.md` - Statistical methods

---

## 🚀 Getting Started

1. **Understand Your Data**: Review your ATS and HRIS data structure
2. **Define Quality of Hire**: Align with stakeholders on success metrics
3. **Start Simple**: Begin with descriptive analytics (source-of-hire, time-to-fill)
4. **Build Trust**: Share initial findings; get feedback
5. **Add Complexity**: Progress to predictive models and experimentation

---

## 📧 Questions?

Open an issue or contribute improvements to this analysis framework!

---

**Last Updated**: March 19, 2026
**Status**: Active Development
**Contributors**: Welcome
