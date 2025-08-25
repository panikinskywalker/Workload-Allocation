# API Reference - Faculty Workload Allocation System

## Core Classes and Functions

### Data Structures

#### `Expertise` (Enum)
Faculty expertise areas used for course matching.

```python
class Expertise(Enum):
    STATISTICS = "Statistics"
    MACHINE_LEARNING = "Machine Learning"
    DATA_ENGINEERING = "Data Engineering"
    DATABASES = "Database Systems"
    ALGORITHMS = "Algorithms"
    SOFTWARE_ENG = "Software Engineering"
    VISUALIZATION = "Data Visualization"
    BIG_DATA = "Big Data"
    DEEP_LEARNING = "Deep Learning"
    RESEARCH_METHODS = "Research Methods"
```

#### `Course` (dataclass)
Represents a course with all its components.

```python
@dataclass
class Course:
    id: str                    # Unique course identifier
    name: str                  # Course name
    code: str                  # Course code (e.g., "COMP101")
    lecture_hours: int         # Hours per week
    lab_hours: int            # Lab hours per week
    num_students: int         # Total enrolled students
    required_expertise: List[Expertise]  # Required expertise areas
    difficulty_level: int     # 1-5 (UG year 1 to PhD)
    min_professors: int       # Minimum professors needed
    max_professors: int       # Maximum professors (for team teaching)
    assessment_hours: int     # Total assessment hours per semester
    prep_factor: float        # Preparation time multiplier
```

#### `Professor` (dataclass)
Represents a faculty member with comprehensive workload model.

```python
@dataclass
class Professor:
    id: str                   # Unique professor identifier
    name: str                 # Professor name
    title: str                # Academic title
    expertise: List[Expertise] # Areas of expertise
    primary_expertise: Expertise # Main specialization
    years_experience: int     # Years of experience
    research_allocation: float # % of time for research (0.2-0.4)
    admin_load: float         # Admin hours per week
    max_teaching_load: float  # Maximum teaching hours per week
    min_teaching_load: float  # Minimum teaching hours per week
    preferences: Dict[str, float] # Course preferences
    teaching_quality: float   # Historical teaching score
    
    def available_teaching_hours(self) -> float:
        """Calculate available teaching hours after research and admin"""
```

#### `CourseAllocation` (dataclass)
Represents allocation of a course to professor(s).

```python
@dataclass
class CourseAllocation:
    course_id: str            # Course identifier
    professor_ids: List[str]  # List of professor IDs
    shares: Dict[str, float]  # professor_id -> share percentage
```

### Main Problem Class

#### `WorkloadAllocationProblem`
Main class representing the faculty workload allocation problem.

```python
class WorkloadAllocationProblem:
    def __init__(self, professors: List[Professor], courses: List[Course])
    
    def calculate_professor_load(self, prof_id: str, allocations: List[CourseAllocation]) -> Dict
    def calculate_fitness(self, allocations: List[CourseAllocation]) -> float
    def check_hard_constraints(self, allocations: List[CourseAllocation]) -> bool
    def calculate_fairness_score(self, allocations: List[CourseAllocation]) -> float
    def calculate_expertise_score(self, allocations: List[CourseAllocation]) -> float
    def calculate_balance_score(self, allocations: List[CourseAllocation]) -> float
    def calculate_preference_score(self, allocations: List[CourseAllocation]) -> float
    def calculate_team_teaching_efficiency(self, allocations: List[CourseAllocation]) -> float
```

**Key Methods:**

- **`calculate_fitness()`**: Main fitness function with weighted components:
  - Fairness (40% weight)
  - Expertise match (25% weight)
  - Workload balance (20% weight)
  - Preference satisfaction (10% weight)
  - Team teaching efficiency (5% weight)

- **`check_hard_constraints()`**: Ensures:
  - All courses are allocated
  - Every professor has work
  - Workload limits are respected
  - Course professor requirements are met

### Algorithm Classes

#### `FairGeneticAlgorithm`
Genetic algorithm optimized for fair workload distribution.

```python
class FairGeneticAlgorithm:
    def __init__(self, problem: WorkloadAllocationProblem, 
                 population_size: int = 100, generations: int = 300)
    
    def create_individual(self) -> List[CourseAllocation]
    def crossover(self, parent1: List[CourseAllocation], 
                  parent2: List[CourseAllocation]) -> List[CourseAllocation]
    def mutate(self, individual: List[CourseAllocation]) -> List[CourseAllocation]
    def solve(self) -> List[CourseAllocation]
    def repair_individual(self, individual: List[CourseAllocation])
    def optimize_fairness(self, individual: List[CourseAllocation])
    def balance_workloads(self, individual: List[CourseAllocation])
```

**Key Features:**
- Population size: 100 individuals
- Generations: 300 iterations
- Mutation rate: 15%
- Elite preservation: 15%
- Tournament selection: 5 participants

### Utility Functions

#### Dataset Generation

```python
def generate_realistic_dataset() -> Tuple[List[Professor], List[Course]]
```
Generates realistic dataset with 15 professors and 10 courses.

#### Reporting Functions

```python
def generate_detailed_allocation_report(problem: WorkloadAllocationProblem, 
                                       allocations: List[CourseAllocation],
                                       output_file: str = "faculty_workload_allocation.csv") -> pd.DataFrame

def analyze_allocation_fairness(problem: WorkloadAllocationProblem, 
                               allocations: List[CourseAllocation]) -> Dict
```

## Usage Examples

### Basic Setup

```python
from src.realistic_fwap import *

# Generate dataset
professors, courses = generate_realistic_dataset()

# Create problem instance
problem = WorkloadAllocationProblem(professors, courses)

# Run genetic algorithm
ga = FairGeneticAlgorithm(problem, population_size=100, generations=300)
best_allocation = ga.solve()

# Generate reports
report_df = generate_detailed_allocation_report(problem, best_allocation)
fairness_metrics = analyze_allocation_fairness(problem, best_allocation)
```

### Custom Configuration

```python
# Modify algorithm parameters
ga = FairGeneticAlgorithm(
    problem, 
    population_size=200,      # Larger population
    generations=500           # More generations
)

# Custom fitness weights (modify in WorkloadAllocationProblem.calculate_fitness)
# Fairness: 40%, Expertise: 25%, Balance: 20%, Preferences: 10%, Team Teaching: 5%
```

### Output Analysis

```python
# Get individual professor workload
for prof in problem.professors:
    load = problem.calculate_professor_load(prof.id, best_allocation)
    print(f"{prof.name}: {load['total_teaching']:.1f} teaching hours/week")

# Analyze fairness
metrics = analyze_allocation_fairness(problem, best_allocation)
print(f"Gini Coefficient: {metrics['gini_coefficient']:.3f}")
print(f"Optimal Load Ratio: {metrics['optimal_load_ratio']:.1%}")
```

## Configuration Options

### Dataset Parameters
- **Number of professors**: Configurable in `generate_realistic_dataset()`
- **Number of courses**: Configurable in `generate_realistic_dataset()`
- **Course characteristics**: Student numbers, difficulty levels, expertise requirements
- **Professor profiles**: Titles, experience levels, research allocations

### Algorithm Parameters
- **Population size**: 50-500 (default: 100)
- **Generations**: 100-1000 (default: 300)
- **Mutation rate**: 0.05-0.25 (default: 0.15)
- **Elite preservation**: 0.05-0.25 (default: 0.15)
- **Tournament size**: 3-7 (default: 5)

### Fitness Weights
- **Fairness**: 30-50% (default: 40%)
- **Expertise match**: 20-30% (default: 25%)
- **Workload balance**: 15-25% (default: 20%)
- **Preference satisfaction**: 5-15% (default: 10%)
- **Team teaching efficiency**: 3-8% (default: 5%)

## Error Handling

The system includes comprehensive error handling for:
- Invalid allocations
- Constraint violations
- Missing professors or courses
- Invalid share percentages
- Workload limit violations

## Performance Considerations

- **Memory usage**: Scales linearly with population size and number of courses
- **Computation time**: O(generations × population_size × courses × professors)
- **Optimization**: Use smaller population for quick testing, larger for production
- **Parallelization**: Algorithm can be parallelized for better performance
