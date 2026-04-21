# Domain 8: Compensation Equity & Benchmarking

## Overview
This domain analyzes pay equity, performs market benchmarking, and optimizes total rewards strategy to ensure competitive and fair compensation.

## Business Impact
- **Pay equity prevents legal risk**: Unexplained pay gaps create legal liability and reputational damage
- **Competitive pay drives retention**: Employees paid below market are 3.5x more likely to leave
- **Total rewards optimize cost**: Strategic mix of cash and benefits maximizes value per dollar spent

## Key Metrics
- **Compa-Ratio**: Actual salary / midpoint of pay range (target: 0.95-1.05)
- **Market Positioning**: Percentile of company pay vs external market
- **Pay Equity Gap**: Unexplained variance in regression-controlled pay analysis
- **Pay-for-Performance Correlation**: Strength of link between performance and compensation
- **Total Rewards Value**: Combined value of base, bonus, equity, and benefits

## Research Foundation
- Regression-controlled pay equity methodology (Oaxaca-Blinder, 1973)
- Market pricing best practices (WorldatWork Compensation Handbook)
- Total rewards framework (Towers Watson, 2012)
- Pay transparency and equity (Castilla, 2015)

## Analysis Notebooks

### 1. Pay Equity Analysis (`01_pay_equity_analysis.ipynb`)
**Purpose**: Identify and quantify unexplained pay gaps across demographic groups

**Key Analyses**:
- Descriptive pay statistics by demographics, level, and department
- Regression-controlled pay equity (isolate unexplained variance)
- Pay-for-performance correlation assessment
- Compa-ratio distribution and outlier identification

**Business Questions**:
- Are there statistically significant pay gaps between demographic groups?
- How much of the pay variance is explained by legitimate factors (level, performance, tenure)?
- Which employees are paid significantly above or below their peers?
- Does pay correlate appropriately with performance ratings?

### 2. Market Benchmarking Analysis (`02_market_benchmarking.ipynb`)
**Purpose**: Compare internal pay to external market data to ensure competitiveness

**Key Analyses**:
- Market positioning by role, level, and location
- Compression analysis (manager vs IC pay relationships)
- Geographic pay differentials and cost-of-living adjustments
- Competitive retention risk identification

**Business Questions**:
- How does our pay compare to market (25th, 50th, 75th percentiles)?
- Which roles are significantly underpaid relative to market?
- Are we at risk of losing employees due to uncompetitive pay?
- How should we adjust pay for remote workers in different locations?

### 3. Total Rewards Optimization (`03_total_rewards_optimization.ipynb`)
**Purpose**: Analyze complete compensation package and optimize mix of cash vs benefits

**Key Analyses**:
- Total rewards calculation (base + bonus + equity + benefits value)
- Cost-per-employee by segment and effectiveness analysis
- Benefits utilization and perceived value assessment
- Budget reallocation scenarios to maximize impact

**Business Questions**:
- What is our total investment per employee including all rewards?
- Are we allocating compensation dollars effectively across cash, equity, and benefits?
- Which benefits deliver the highest perceived value per dollar spent?
- How can we reallocate budget to improve retention without increasing total cost?

## Data Sources
- HRIS compensation data (base salary, bonus, equity grants)
- External market survey data (e.g., Radford, Mercer, Payscale)
- Benefits cost and utilization data
- Performance review ratings
- Demographic data (for equity analysis)

## Strategic Applications
1. **Legal compliance**: Proactively identify and correct pay inequities before audits or lawsuits
2. **Competitive positioning**: Use market data to set pay ranges that attract and retain talent
3. **Budget optimization**: Shift compensation dollars to highest-ROI components
4. **Retention**: Ensure high performers are paid competitively to prevent poaching
5. **Transparency**: Build trust through fair, explainable compensation practices

## Ethical Considerations
- **Privacy**: Salary data is highly sensitive; maintain strict confidentiality
- **Bias detection**: Statistical significance ≠ discrimination, but flags areas for investigation
- **Correction obligation**: Finding gaps creates ethical obligation to address them
- **Individual fairness**: Balance statistical analysis with individual circumstances
- **Transparency trade-offs**: Pay transparency can improve equity but may create comparison anxiety

## Related Domains
- **Domain 2 (Retention)**: Uncompetitive pay drives attrition
- **Domain 6 (Inclusion)**: Pay equity is core inclusion metric
- **Domain 4 (Recruiting)**: Competitive offers require market data
- **Domain 7 (Engagement)**: Pay fairness impacts satisfaction and engagement
