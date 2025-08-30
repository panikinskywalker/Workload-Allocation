# 🎓 **Faculty Workload Allocation System (FWAP)**
## Metaheuristic Algorithm Comparison for Academic Workload Optimization

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)](README.md)

---

## 📊 **Project Overview**

The Faculty Workload Allocation System (FWAP) is a comprehensive research project that implements and compares three metaheuristic algorithms for optimizing faculty workload distribution in academic institutions. This project addresses the NP-Hard problem of allocating courses to professors while satisfying multiple constraints and optimizing for fairness and efficiency.

### **Research Contributions**
- **Multi-Algorithm Comparison**: Hill Climbing, Genetic Algorithm, and Simulated Annealing
- **Statistical Validation**: T-tests and significance testing for algorithm differences
- **Comprehensive Visualization**: 37 publication-ready visualizations
- **Realistic Dataset**: 100 professors × 80 courses with realistic constraints
- **Academic Paper Ready**: Complete documentation and integration guides

---

## 🚀 **Key Features**

### **Algorithms Implemented**
- **🏔️ Hill Climbing**: Local search with neighbor generation and improvement
- **🧬 Genetic Algorithm**: Population-based evolution with selection and crossover
- **❄️ Simulated Annealing**: Temperature-controlled exploration with acceptance probability

### **Problem Characteristics**
- **Problem Scale**: 100 professors × 80 courses = 8,000 potential assignments
- **Search Space**: 1.00e+160 possible allocations
- **Constraints**: Expertise matching, workload limits, fairness requirements
- **Objective**: Minimize workload imbalance while satisfying all constraints

### **Visualization Suite**
- **Dataset Analysis**: 9 visualizations for data understanding
- **Algorithm Performance**: 12 visualizations for comparison and ranking
- **Algorithm Operation**: 12 visualizations explaining algorithm mechanics
- **Statistical Analysis**: T-tests, significance testing, and performance metrics

---

## 📁 **Repository Structure**

```
Faculty-Workload-Allocation-System/
├── 📁 src/                                    # Source code
│   ├── 🏔️ hill_climbing_visualization.py     # Hill Climbing operation visualizations
│   ├── 🧬 genetic_algorithm_visualization.py # Genetic Algorithm operation visualizations
│   ├── ❄️ simulated_annealing_visualization.py # Simulated Annealing operation visualizations
│   ├── 📊 dataset_eda.py                     # Exploratory Data Analysis
│   ├── 🔬 advanced_visualizations.py         # Advanced dataset analysis
│   ├── 🏆 algorithm_analysis.py              # Algorithm comparison and ranking
│   └── 🎯 workload_allocator.py              # Core workload allocation system
├── 📁 results/                                # Generated results and visualizations
│   ├── 📊 eda_visualizations/                # Basic dataset analysis (5 files)
│   ├── 🔬 advanced_visualizations/           # Statistical analysis (4 files)
│   ├── 🏆 algorithm_analysis/                # Algorithm comparison (7 files)
│   ├── 🏔️ hill_climbing_visualization/      # Hill Climbing details (4 files)
│   ├── 🧬 genetic_algorithm_visualization/  # GA details (4 files)
│   ├── ❄️ simulated_annealing_visualization/ # SA details (4 files)
│   └── 📋 Documentation files                # Summary reports and guides
├── 📁 data/                                   # Dataset files
│   ├── professors.csv                         # Professor data (100 professors)
│   ├── courses.csv                           # Course data (80 courses)
│   └── expertise_mapping.csv                 # Expertise requirements
├── 📁 examples/                               # Usage examples and tests
├── 📁 docs/                                   # Additional documentation
├── 📁 requirements.txt                        # Python dependencies
├── 📁 LICENSE                                 # MIT License
└── 📁 README.md                               # This file
```

---

## 🛠️ **Installation and Setup**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Installation Steps**

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
   python -c "import pandas, numpy, matplotlib, seaborn; print('All dependencies installed successfully!')"
   ```

---

## 🚀 **Quick Start**

### **1. Generate Dataset**
```bash
python src/dataset_eda.py
```

### **2. Run Workload Allocation**
```bash
python src/workload_allocator.py
```

### **3. Generate Algorithm Visualizations**
```bash
# Hill Climbing
python src/hill_climbing_visualization.py

# Genetic Algorithm
python src/genetic_algorithm_visualization.py

# Simulated Annealing
python src/simulated_annealing_visualization.py
```

### **4. Generate Complete Analysis**
```bash
python src/algorithm_analysis.py
```

---

## 📊 **Results and Outputs**

### **Generated Files**
- **37 Publication-Quality Visualizations** (300 DPI, PNG format)
- **6 CSV Result Files** with algorithm outputs and statistics
- **4 Comprehensive Documentation** files for academic paper integration

### **Key Findings**
1. **Algorithm Rankings**:
   - 1st: Genetic Algorithm (Best fairness, comprehensive approach)
   - 2nd: Hill Climbing (Best fitness, fastest execution)
   - 3rd: Simulated Annealing (Good balance, moderate speed)

2. **Statistical Significance**: All algorithm pairs show statistically significant differences (p < 0.05)

3. **Problem Complexity**: Search space of 1.00e+160 possible allocations with only 1.8% feasibility rate

---

## 🔬 **Technical Details**

### **Algorithm Parameters**

#### **Hill Climbing**
- **Step Size**: 0.5 (neighbor generation distance)
- **Neighbor Count**: 8 (directions for neighbor generation)
- **Max Iterations**: 1000 (convergence limit)
- **Acceptance Threshold**: 0.001 (improvement tolerance)

#### **Genetic Algorithm**
- **Population Size**: 100 individuals
- **Selection Method**: Tournament selection (size 3)
- **Crossover Rate**: 0.8 (80% probability)
- **Mutation Rate**: 0.1 (10% probability)
- **Elitism**: Best individual preserved

#### **Simulated Annealing**
- **Initial Temperature**: 100.0 (starting exploration level)
- **Cooling Rate**: 0.95 (exponential cooling factor)
- **Neighbor Count**: 1 (single neighbor per iteration)
- **Termination**: Maximum iterations or temperature threshold

### **Constraint System**
- **Hard Constraints**: All courses allocated, all professors have work
- **Soft Constraints**: Fairness, expertise match, workload limits
- **Objective Function**: Weighted combination of fairness, expertise, and balance

---

## 📈 **Performance Metrics**

### **Evaluation Criteria**
1. **Solution Quality**: Fitness score optimization
2. **Execution Time**: Algorithm efficiency
3. **Fairness Score**: Workload distribution balance
4. **Expertise Match**: Course-professor alignment
5. **Constraint Satisfaction**: Hard and soft constraint compliance

### **Statistical Analysis**
- **T-Tests**: Independent t-tests between all algorithm pairs
- **Significance Level**: p < 0.05 for statistical significance
- **Sample Size**: 100 professors × 80 courses = 8,000 potential assignments

---

## 🤝 **Contributing**

This is a research project for academic purposes. If you find any issues or have suggestions for improvements, please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### **Development Guidelines**
- Follow PEP 8 Python style guidelines
- Add comprehensive documentation for new features
- Include unit tests for new functionality
- Update the README for significant changes

---

## 📚 **Documentation**

### **Core Documentation**
- **`ALGORITHM_OPERATION_VISUALIZATION_GUIDE.md`**: Complete guide to algorithm visualizations
- **`FINAL_COMPLETE_ALGORITHM_VISUALIZATION_SUMMARY.md`**: Comprehensive visualization inventory
- **`COMPLETE_VISUALIZATION_SUMMARY.md`**: Dataset and performance visualization guide

### **Academic Paper Integration**
- **Section-by-section** visualization usage guide
- **High-impact visualization** recommendations
- **Technical specifications** for publication requirements

---

## 👨‍🎓 **Author**

**panikinskywalker** - MSc Data Science Student


---

## 🙏 **Acknowledgments**

- **Academic Community**: For research guidance and feedback
- **Open Source Community**: For the excellent Python libraries used


---

*This repository contains the complete implementation and analysis for the Faculty Workload Allocation System research project. All visualizations are publication-ready and ready for immediate integration into academic papers.*
