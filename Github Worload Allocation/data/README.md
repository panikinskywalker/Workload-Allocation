# University Faculty Workload Allocation Dataset

This directory contains a comprehensive dataset for testing faculty workload allocation optimization algorithms.

## Dataset Overview

- **100 Professors** across 25 university departments
- **80 Courses** with varying complexity levels and team teaching capabilities
- **Realistic academic parameters** including workload constraints, expertise matching, and team teaching support

## Files

### `professors.csv`
Contains 100 faculty members with the following attributes:
- **id**: Unique professor identifier (P001-P100)
- **name**: Full name of the professor
- **title**: Academic rank (Professor, Associate Professor, Assistant Professor, Lecturer)
- **department**: University department affiliation
- **expertise**: Semicolon-separated list of expertise areas
- **primary_expertise**: Main area of specialization
- **years_experience**: Years of academic experience
- **research_allocation**: Percentage of time allocated to research (0.2-0.4)
- **admin_load**: Administrative duties in hours per week (2-10)
- **max_teaching_load**: Maximum teaching hours per week (15-25)
- **min_teaching_load**: Minimum teaching hours per week (8-12)
- **teaching_quality**: Historical teaching performance score (0.7-1.0)
- **availability**: Semicolon-separated list of available semesters

### `courses.csv`
Contains 80 courses with the following attributes:
- **id**: Unique course identifier (C001-C080)
- **name**: Course title
- **code**: Department course code (e.g., CS101, MATH201)
- **department**: Department offering the course
- **lecture_hours**: Weekly lecture hours
- **lab_hours**: Weekly laboratory hours
- **num_students**: Total enrolled students
- **required_expertise**: Required faculty expertise areas
- **difficulty_level**: Academic level (1=UG Year 1, 5=Graduate)
- **min_professors**: Minimum professors required
- **max_professors**: Maximum professors allowed (for team teaching)
- **assessment_hours**: Total assessment hours per semester
- **prep_factor**: Preparation time multiplier
- **can_be_shared**: Whether course supports team teaching
- **semester**: Semester availability (Fall, Spring, Summer, or Both)

## Department Distribution

### Professors by Department
- **Geology**: 8 professors
- **History**: 8 professors
- **Computer Science & Engineering**: 7 professors
- **Philosophy**: 7 professors
- **Biochemistry**: 7 professors
- **Electrical Engineering**: 5 professors
- **Biology**: 5 professors
- **Communication Studies**: 5 professors
- **Public Health**: 5 professors
- **Environmental Science**: 4 professors
- **Mathematics & Statistics**: 4 professors
- **Sociology**: 4 professors
- **Mechanical Engineering**: 2 professors
- **Civil Engineering**: 2 professors
- **Physics & Astronomy**: 2 professors
- **Political Science**: 2 professors
- **Psychology**: 2 professors
- **Economics**: 2 professors
- **Chemical Engineering**: 3 professors
- **Biomedical Engineering**: 3 professors
- **Chemistry**: 3 professors
- **Medicine**: 3 professors
- **Nursing**: 3 professors
- **Pharmacy**: 3 professors
- **English Literature**: 1 professor

### Courses by Department
- **Computer Science (COMP)**: 20 courses
- **Mathematics (MATH)**: 15 courses
- **Business (BUS)**: 12 courses
- **Engineering**: 15 courses (Mechanical, Electrical, Civil, Chemical, Biomedical)
- **Science & Humanities**: 18 courses (Physics, Chemistry, Biology, Psychology, Sociology, etc.)

## Course Difficulty Distribution

- **UG Year 1 (Level 1)**: 18 courses (22.5%)
- **UG Year 2 (Level 2)**: 20 courses (25.0%)
- **UG Year 3 (Level 3)**: 11 courses (13.8%)
- **UG Year 4 (Level 4)**: 11 courses (13.8%)
- **Graduate (Level 5)**: 20 courses (25.0%)

## Team Teaching Capability

- **Courses that can be shared**: 65 (81.2%)
- **Single-professor courses**: 15 (18.8%)
- **Average maximum professors per course**: 2.09
- **Average minimum professors per course**: 1.00

## Workload Parameters

### Professor Workload Averages
- **Research Allocation**: 28.82%
- **Admin Load**: 6.4 hours/week
- **Maximum Teaching**: 20.0 hours/week
- **Minimum Teaching**: 10.0 hours/week

### Course Workload Parameters
- **Lecture Hours**: 1-4 hours per week
- **Lab Hours**: 0-2 hours per week
- **Student Enrollment**: 10-250 students
- **Assessment Hours**: 10-40 hours per semester
- **Preparation Factor**: 1.5-3.5x (multiplier for prep time)

## Problem Complexity

- **Total Possible Allocations**: 2,270,150
- **Search Space**: Extremely large (overflow)
- **Feasibility**: ✓ Problem is feasible
  - Total Teaching Capacity: 1,995.9 hours/week
  - Total Teaching Requirement: 308.0 hours/week

## Usage

This dataset is designed to be used with the Faculty Workload Allocation System optimization algorithms:

1. **Load the dataset** using `data_loader.py`
2. **Apply optimization algorithms** (Genetic Algorithm, Hill Climbing, Simulated Annealing)
3. **Validate constraints** and workload balancing
4. **Generate allocation reports** and visualizations

## Data Generation

The dataset was generated using `src/dataset_generator.py` with:
- **Random seed**: 42 (for reproducibility)
- **Realistic parameters**: Based on academic workload models
- **Balanced distribution**: Across departments and difficulty levels
- **Team teaching support**: Realistic sharing capabilities

## Constraints

### Hard Constraints
- Every course must be allocated to at least the minimum required professors
- Every professor must have at least the minimum teaching load
- No professor can exceed the maximum teaching load
- Course professor limits must be respected

### Soft Constraints
- Fairness in workload distribution across faculty
- Expertise matching between professors and courses
- Preference satisfaction for course assignments
- Minimize team teaching when single professor is sufficient

## File Formats

All files are in CSV format with UTF-8 encoding and can be opened in:
- Excel/Google Sheets
- Python pandas
- R data frames
- Any CSV-compatible software

## Version Information

- **Dataset Version**: 1.0.0
- **Generated**: 2024
- **Algorithm**: Faculty Workload Allocation System
- **Purpose**: Academic research and optimization testing
