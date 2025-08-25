# User Guide - Faculty Workload Allocation System

## 🚀 Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Faculty-Workload-Allocation-System.git
   cd Faculty-Workload-Allocation-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import numpy, pandas, matplotlib, seaborn, scipy; print('All packages installed successfully!')"
   ```

### Quick Test

Run the basic test to ensure everything works:
```bash
python examples/test_realistic_fwap.py
```

## 📖 Basic Usage

### Running the Main System

The main system can be run with a single command:

```bash
python src/realistic-fwap.py
```

This will:
1. Generate a realistic dataset (15 professors, 10 courses)
2. Run the genetic algorithm optimization
3. Generate detailed reports
4. Display workload analysis

### Understanding the Output

The system provides several types of output:

#### 1. Console Output
- **Dataset Information**: Professor and course details
- **Algorithm Progress**: Generation updates and fitness scores
- **Workload Summary**: Individual professor workloads
- **Fairness Analysis**: Statistical metrics and recommendations

#### 2. Generated Files
- **`faculty_workload_allocation.csv`**: Detailed task breakdown
- **`faculty_workload_summary.csv`**: Professor summary with load ratios
- **`workload_distribution.png`**: Visual workload analysis

## 🔧 Configuration Options

### Modifying Dataset Size

To change the number of professors or courses, edit `src/realistic-fwap.py`:

```python
# In the main() function, change these lines:
professors, courses = generate_realistic_dataset(
    num_faculty=20,    # Change from 15 to desired number
    num_courses=15     # Change from 10 to desired number
)
```

### Adjusting Algorithm Parameters

Modify the genetic algorithm parameters:

```python
# In the main() function:
ga = FairGeneticAlgorithm(
    problem, 
    population_size=200,      # Increase for better results (slower)
    generations=500           # Increase for better results (slower)
)
```

### Customizing Fitness Weights

To change the importance of different factors, modify the `calculate_fitness` method in `WorkloadAllocationProblem`:

```python
def calculate_fitness(self, allocations: List[CourseAllocation]) -> float:
    # ... existing code ...
    
    # Adjust these weights as needed:
    fitness += self._calculate_fairness_score(allocation) * 50      # Was 40
    fitness += self._calculate_expertise_match_score(allocation) * 20  # Was 25
    fitness += self._calculate_workload_balance_score(allocation) * 25  # Was 20
    fitness += self._calculate_preference_score(allocation) * 5     # Was 10
```

## 📊 Interpreting Results

### Workload Metrics

#### Teaching Load Distribution
- **Optimal Range**: 70-90% of available capacity
- **Underloaded**: <70% capacity (may need more work)
- **Overloaded**: >90% capacity (may need workload reduction)

#### Fairness Indicators
- **Coefficient of Variation (CV)**: Lower is better (target: <0.5)
- **Gini Coefficient**: Lower is better (target: <0.3)
- **Optimal Load Ratio**: Higher percentage is better

### Team Teaching Analysis

#### Share Percentages
- **Single Professor**: 100%
- **Two Professors**: 50% each
- **Three Professors**: 33.3% each

#### When Team Teaching Occurs
- Large classes (>100 students)
- Courses requiring multiple expertise areas
- High-difficulty courses needing specialized knowledge

## 🎯 Advanced Usage

### Custom Dataset Creation

Create your own professor and course data:

```python
from src.realistic_fwap import *

# Define custom professors
custom_professors = [
    Professor(
        id="P001",
        name="Dr. John Smith",
        title="Professor",
        expertise=[Expertise.MACHINE_LEARNING, Expertise.STATISTICS],
        primary_expertise=Expertise.MACHINE_LEARNING,
        years_experience=15,
        research_allocation=0.4,
        admin_load=5.0,
        max_teaching_load=12,
        min_teaching_load=6,
        preferences={},
        teaching_quality=0.9
    )
    # Add more professors...
]

# Define custom courses
custom_courses = [
    Course(
        id="C001",
        name="Advanced Machine Learning",
        code="ML701",
        lecture_hours=4,
        lab_hours=2,
        num_students=60,
        required_expertise=[Expertise.MACHINE_LEARNING, Expertise.STATISTICS],
        difficulty_level=4,
        min_professors=1,
        max_professors=2,
        assessment_hours=80,
        prep_factor=1.8
    )
    # Add more courses...
]

# Create problem and solve
problem = WorkloadAllocationProblem(custom_professors, custom_courses)
ga = FairGeneticAlgorithm(problem)
best_allocation = ga.solve()
```

### Batch Processing

Run multiple scenarios and compare results:

```python
import pandas as pd
from src.realistic_fwap import *

results = []

for scenario in range(5):
    print(f"Running scenario {scenario + 1}")
    
    # Generate different dataset
    professors, courses = generate_realistic_dataset()
    problem = WorkloadAllocationProblem(professors, courses)
    
    # Run optimization
    ga = FairGeneticAlgorithm(problem)
    allocation = ga.solve()
    
    # Analyze results
    fairness = analyze_allocation_fairness(problem, allocation)
    
    results.append({
        'scenario': scenario + 1,
        'fitness': problem.calculate_fitness(allocation),
        'gini_coefficient': fairness['gini_coefficient'],
        'optimal_load_ratio': fairness['optimal_load_ratio'],
        'mean_teaching_load': fairness['teaching_mean']
    })

# Compare scenarios
results_df = pd.DataFrame(results)
print(results_df)
```

### Integration with Other Systems

Export results for use in other tools:

```python
# Export to Excel with multiple sheets
with pd.ExcelWriter('workload_analysis.xlsx') as writer:
    report_df.to_excel(writer, sheet_name='Detailed_Allocation', index=False)
    summary_df.to_excel(writer, sheet_name='Professor_Summary', index=False)
    results_df.to_excel(writer, sheet_name='Scenario_Comparison', index=False)

# Export to JSON for web applications
import json
allocation_data = {
    'professors': [{'id': p.id, 'name': p.name} for p in problem.professors],
    'courses': [{'id': c.id, 'name': c.name} for c in problem.courses],
    'allocations': [
        {
            'course_id': a.course_id,
            'professors': a.professor_ids,
            'shares': a.shares
        } for a in best_allocation
    ]
}

with open('allocation_data.json', 'w') as f:
    json.dump(allocation_data, f, indent=2)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'numpy'`
**Solution**: Install required packages:
```bash
pip install -r requirements.txt
```

#### 2. Memory Issues
**Problem**: System runs out of memory with large datasets
**Solution**: Reduce population size and generations:
```python
ga = FairGeneticAlgorithm(problem, population_size=50, generations=100)
```

#### 3. Poor Results
**Problem**: Algorithm doesn't find good solutions
**Solution**: 
- Increase population size and generations
- Check constraint violations in output
- Verify dataset parameters are reasonable

#### 4. Long Runtime
**Problem**: Algorithm takes too long to complete
**Solution**:
- Reduce population size and generations
- Use smaller dataset for testing
- Run on more powerful machine

### Performance Optimization

#### For Quick Testing
```python
ga = FairGeneticAlgorithm(
    problem, 
    population_size=30,      # Smaller population
    generations=50           # Fewer generations
)
```

#### For Production Use
```python
ga = FairGeneticAlgorithm(
    problem, 
    population_size=200,     # Larger population
    generations=500          # More generations
)
```

#### For Research/Comparison
```python
ga = FairGeneticAlgorithm(
    problem, 
    population_size=100,     # Balanced
    generations=300          # Balanced
)
```

## 📈 Monitoring and Analysis

### Real-time Progress Monitoring

The system provides progress updates during execution:

```
Generation 0: Best Fitness = -10000.00
Generation 30: Best Fitness = -10000.00
Generation 60: Best Fitness = -10000.00
...
```

**Note**: Negative fitness values indicate constraint violations. The system will continue until it finds a valid solution.

### Post-Execution Analysis

After completion, analyze the results:

```python
# Load results
report_df = pd.read_csv('faculty_workload_allocation.csv')
summary_df = pd.read_csv('faculty_workload_summary.csv')

# Basic statistics
print(f"Total tasks allocated: {len(report_df)}")
print(f"Professors with work: {summary_df['Teaching_Hours'].gt(0).sum()}")
print(f"Average teaching load: {summary_df['Teaching_Hours'].mean():.1f} hours/week")

# Identify issues
overloaded = summary_df[summary_df['Load_Ratio'] > 0.9]
underloaded = summary_df[summary_df['Load_Ratio'] < 0.7]

print(f"Overloaded professors: {len(overloaded)}")
print(f"Underloaded professors: {len(underloaded)}")
```

## 🔄 Maintenance and Updates

### Regular Updates

1. **Check for dependency updates**:
   ```bash
   pip list --outdated
   pip install --upgrade numpy pandas matplotlib seaborn scipy
   ```

2. **Update requirements.txt**:
   ```bash
   pip freeze > requirements.txt
   ```

3. **Test system after updates**:
   ```bash
   python examples/test_realistic_fwap.py
   ```

### Data Backup

Regularly backup your results and configurations:
```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d)

# Copy results
cp results/*.csv backups/$(date +%Y%m%d)/
cp results/*.png backups/$(date +%Y%m%d)/
```

## 📞 Support and Community

### Getting Help

1. **Check the documentation** in the `docs/` folder
2. **Review example code** in the `examples/` folder
3. **Check GitHub issues** for known problems
4. **Create a new issue** for bugs or feature requests

### Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Reporting Issues

When reporting issues, include:
- Python version
- Operating system
- Error messages
- Steps to reproduce
- Expected vs. actual behavior

---

**Happy optimizing!** 🎓✨
