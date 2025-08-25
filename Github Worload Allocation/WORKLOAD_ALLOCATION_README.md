# 🎓 Faculty Workload Allocation System

A comprehensive, robust system for optimizing faculty workload allocation using three metaheuristic algorithms: **Hill Climbing**, **Genetic Algorithm**, and **Simulated Annealing**.

## 🎯 **What This System Does**

This system solves the **Faculty Workload Allocation Problem (FWAP)** by:

- ✅ **Allocating every course to at least one professor**
- ✅ **Ensuring every professor gets at least one course**
- ✅ **Maintaining 80% minimum teaching load requirement**
- ✅ **Preventing workload overloading**
- ✅ **Optimizing for fairness and expertise matching**
- ✅ **Supporting team teaching with share percentages**

## 🏗️ **System Architecture**

```
src/
├── workload_allocator.py      # Core algorithms and data structures
├── data_adapter.py            # Dataset loading and conversion
└── run_workload_allocation.py # Main runner and analysis

examples/
└── test_workload_system.py    # Quick system test

results/                        # Generated outputs (created automatically)
├── *.csv                      # Detailed allocation reports
└── *.png                      # Comprehensive visualizations
```

## 🚀 **Quick Start**

### 1. **Test the System (Fast)**
```bash
python examples/test_workload_system.py
```

### 2. **Run Full Analysis (Test Dataset)**
```bash
python src/run_workload_allocation.py
# Choose option 1 for test dataset (20 professors, 15 courses)
```

### 3. **Run Full Analysis (Complete Dataset)**
```bash
python src/run_workload_allocation.py
# Choose option 2 for full dataset (100 professors, 80 courses)
```

## 🔬 **Algorithms Implemented**

### 1. **Hill Climbing** 🧗
- **Type**: Local search optimization
- **Strategy**: Iterative improvement with neighbor generation
- **Best for**: Quick solutions, local optimization
- **Parameters**: 1000 max iterations

### 2. **Genetic Algorithm** 🧬
- **Type**: Population-based evolutionary algorithm
- **Strategy**: Selection, crossover, mutation, elitism
- **Best for**: Global optimization, complex problems
- **Parameters**: 100 population, 300 generations, 15% mutation

### 3. **Simulated Annealing** 🔥
- **Type**: Probabilistic global optimization
- **Strategy**: Temperature-controlled random walk
- **Best for**: Escaping local optima, balanced exploration
- **Parameters**: 100° initial temp, 0.995 cooling rate, 5000 iterations

## 📊 **Output Files Generated**

### **CSV Reports**
1. **`{algorithm}_allocation.csv`** - Detailed course allocations with share percentages
2. **`{algorithm}_professor_summary.csv`** - Professor workload summaries
3. **`algorithm_comparison.csv`** - Comprehensive algorithm comparison

### **Visualizations**
1. **`algorithm_performance_comparison.png`** - 4-panel performance overview
2. **`workload_distribution_comparison.png`** - Workload distribution histograms
3. **`fitness_comparison.png`** - Fitness score comparison
4. **`execution_time_comparison.png`** - Speed comparison
5. **`fairness_analysis.png`** - Fairness analysis across algorithms

## 🎯 **Key Features**

### **Fairness Constraints**
- **Minimum Load**: Every professor must teach at least 80% of their contracted hours
- **Maximum Load**: No professor can exceed their maximum teaching capacity
- **Balanced Distribution**: Workloads optimized for equity across faculty

### **Expertise Matching**
- **Required Skills**: Courses assigned based on professor expertise
- **Primary Specialization**: Bonus scoring for primary expertise matches
- **Department Alignment**: Respects academic department boundaries

### **Team Teaching Support**
- **Share Percentages**: Clear workload distribution among multiple professors
- **Flexible Team Sizes**: 1-3 professors per course based on requirements
- **Equal Distribution**: Default equal shares with optimization capability

## 📈 **Performance Metrics**

### **Solution Quality**
- **Fitness Score**: Weighted combination of fairness, expertise, and balance
- **Constraint Satisfaction**: Binary validation of hard constraints
- **Workload Statistics**: Mean, standard deviation, coefficient of variation

### **Algorithm Efficiency**
- **Execution Time**: Wall-clock time for each algorithm
- **Convergence**: Fitness improvement over iterations
- **Solution Validity**: Percentage of feasible solutions generated

## 🔧 **Configuration Options**

### **Dataset Selection**
- **Test Dataset**: 20 professors, 15 courses (fast testing)
- **Full Dataset**: 100 professors, 80 courses (complete analysis)

### **Algorithm Parameters**
- **Hill Climbing**: Adjustable max iterations
- **Genetic Algorithm**: Population size, generations, mutation rate
- **Simulated Annealing**: Temperature, cooling rate, iterations

## 📋 **Data Requirements**

### **Professor Data**
- ID, name, title, department
- Expertise areas (semicolon-separated)
- Workload constraints (min/max teaching hours)
- Research allocation percentage
- Administrative load

### **Course Data**
- ID, name, code, department
- Contact hours (lecture + lab)
- Student enrollment
- Required expertise
- Team teaching capability
- Difficulty level

## 🎓 **Academic Use Cases**

### **Research Applications**
- **Algorithm Comparison**: Evaluate metaheuristic performance
- **Fairness Analysis**: Study workload distribution equity
- **Constraint Satisfaction**: Academic scheduling optimization
- **Metaheuristic Research**: Parameter tuning and comparison

### **Practical Applications**
- **Department Planning**: Optimize teaching assignments
- **Workload Balance**: Ensure fair distribution among faculty
- **Resource Planning**: Balance teaching, research, and admin
- **Academic Year Planning**: Semester workload distribution

## 🏆 **Algorithm Recommendations**

### **Best Overall Performance**
- **Genetic Algorithm**: Best balance of quality and reliability
- **Simulated Annealing**: Good for escaping local optima
- **Hill Climbing**: Fastest for simple problems

### **Use Case Recommendations**
- **Speed Priority**: Hill Climbing
- **Quality Priority**: Genetic Algorithm
- **Balance**: Simulated Annealing
- **Research**: All three for comprehensive comparison

## 🔍 **Troubleshooting**

### **Common Issues**
1. **Memory Errors**: Use test dataset for large problems
2. **Long Execution**: Reduce algorithm parameters
3. **Import Errors**: Ensure all dependencies installed
4. **Data Loading**: Check CSV file format and paths

### **Performance Tips**
- **Test First**: Always test with small dataset
- **Parameter Tuning**: Adjust based on problem size
- **Early Stopping**: Use conservative iteration limits
- **Resource Monitoring**: Monitor memory and CPU usage

## 📚 **Dependencies**

```bash
pip install numpy pandas matplotlib seaborn scipy
```

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** feature branch
3. **Implement** improvements
4. **Test** thoroughly
5. **Submit** pull request

## 📝 **License**

MIT License - See LICENSE file for details.

## 👨‍💻 **Author**

Academic Workload Optimization Research

## 🙏 **Acknowledgments**

- Academic institutions for workload allocation challenges
- Metaheuristic algorithm research community
- Python scientific computing ecosystem

---

## 🎉 **Ready to Run!**

The system is now ready for your dissertation research. Start with the test dataset to verify everything works, then run the full analysis for comprehensive results.

**Happy optimizing! 🚀**
