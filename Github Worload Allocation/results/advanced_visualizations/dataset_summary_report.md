
# FACULTY WORKLOAD ALLOCATION SYSTEM - DATASET ANALYSIS SUMMARY

## 📊 DATASET OVERVIEW
- **Total Professors**: 100
- **Total Courses**: 80
- **Total Departments**: 25
- **Professor-to-Course Ratio**: 1.25:1

## 🧮 PROBLEM COMPLEXITY
- **Search Space Size**: 1.00e+160 possible allocations
        - **Log10(Search Space)**: 160.00
- **Feasibility Rate**: 1.8% of potential assignments are feasible

## ⚖️ CONSTRAINT ANALYSIS
- **Average Min Teaching Load**: 10.0 hours/week
- **Average Max Teaching Load**: 20.0 hours/week
- **Average Teaching Load Flexibility**: 9.9 hours/week
- **Average Research Allocation**: 0.288 (fraction of 40 hours)
- **Average Administrative Load**: 6.4 hours/week

## 📚 COURSE CHARACTERISTICS
- **Difficulty Levels**: 1-5
- **Average Student Enrollment**: 98 students
- **Team Teaching Support**: 81.2% of courses
- **Average Course Workload**: 34.6 hours

## 🎯 KEY INSIGHTS
1. **High Complexity**: The search space is extremely large (1.00e+160 possibilities)
2. **Moderate Feasibility**: 1.8% of potential assignments satisfy constraints
3. **Balanced Workload**: Professors have reasonable flexibility in teaching load (9.9 hours)
4. **Team Teaching**: 65/80 courses support multiple professors
5. **Realistic Constraints**: Workload limits are realistic for academic environments

## 🚀 IMPLICATIONS FOR ALGORITHMS
- **Hill Climbing**: May struggle with local optima due to large search space
- **Genetic Algorithm**: Population-based approach beneficial for exploring diverse solutions
- **Simulated Annealing**: Temperature-based acceptance helpful for escaping local optima
- **Constraint Satisfaction**: All algorithms must handle 98.2% infeasible assignments

## 📁 GENERATED VISUALIZATIONS
- Department Analysis
- Expertise Analysis  
- Course Analysis
- Workload Analysis
- Complexity Analysis
- Correlation Analysis
- Constraint Analysis
- Problem Complexity
- Statistical Analysis

This dataset represents a realistic, complex academic workload allocation problem suitable for testing metaheuristic algorithms.
