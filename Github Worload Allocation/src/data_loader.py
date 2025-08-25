#!/usr/bin/env python3
"""
Data Loader Utility for Faculty Workload Allocation System
Loads CSV datasets back into the data structures needed by optimization algorithms
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# DATA STRUCTURES (matching dataset_generator.py)
# ============================================================================

class Expertise(Enum):
    """Comprehensive faculty expertise areas across university departments"""
    # Computer Science & Engineering
    COMPUTER_SCIENCE = "Computer Science"
    SOFTWARE_ENGINEERING = "Software Engineering"
    COMPUTER_ENGINEERING = "Computer Engineering"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    MACHINE_LEARNING = "Machine Learning"
    DEEP_LEARNING = "Deep Learning"
    DATA_SCIENCE = "Data Science"
    DATABASE_SYSTEMS = "Database Systems"
    COMPUTER_NETWORKS = "Computer Networks"
    CYBERSECURITY = "Cybersecurity"
    HUMAN_COMPUTER_INTERACTION = "Human-Computer Interaction"
    COMPUTER_GRAPHICS = "Computer Graphics"
    ALGORITHMS = "Algorithms"
    DATA_STRUCTURES = "Data Structures"
    OPERATING_SYSTEMS = "Operating Systems"
    
    # Mathematics & Statistics
    MATHEMATICS = "Mathematics"
    STATISTICS = "Statistics"
    APPLIED_MATHEMATICS = "Applied Mathematics"
    PURE_MATHEMATICS = "Pure Mathematics"
    LINEAR_ALGEBRA = "Linear Algebra"
    CALCULUS = "Calculus"
    DIFFERENTIAL_EQUATIONS = "Differential Equations"
    NUMERICAL_ANALYSIS = "Numerical Analysis"
    PROBABILITY_THEORY = "Probability Theory"
    MATHEMATICAL_MODELING = "Mathematical Modeling"
    
    # Physics & Engineering
    PHYSICS = "Physics"
    APPLIED_PHYSICS = "Applied Physics"
    QUANTUM_PHYSICS = "Quantum Physics"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    CIVIL_ENGINEERING = "Civil Engineering"
    CHEMICAL_ENGINEERING = "Chemical Engineering"
    BIOMEDICAL_ENGINEERING = "Biomedical Engineering"
    
    # Business & Economics
    BUSINESS_ADMINISTRATION = "Business Administration"
    FINANCE = "Finance"
    ACCOUNTING = "Accounting"
    MARKETING = "Marketing"
    MANAGEMENT = "Management"
    ECONOMICS = "Economics"
    OPERATIONS_RESEARCH = "Operations Research"
    SUPPLY_CHAIN = "Supply Chain Management"
    
    # Humanities & Social Sciences
    PSYCHOLOGY = "Psychology"
    SOCIOLOGY = "Sociology"
    PHILOSOPHY = "Philosophy"
    HISTORY = "History"
    ENGLISH_LITERATURE = "English Literature"
    POLITICAL_SCIENCE = "Political Science"
    COMMUNICATION = "Communication"
    LINGUISTICS = "Linguistics"
    
    # Natural Sciences
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    BIOCHEMISTRY = "Biochemistry"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    GEOLOGY = "Geology"
    ASTRONOMY = "Astronomy"
    
    # Health Sciences
    MEDICINE = "Medicine"
    NURSING = "Nursing"
    PUBLIC_HEALTH = "Public Health"
    PHARMACY = "Pharmacy"
    PHYSICAL_THERAPY = "Physical Therapy"

@dataclass
class Course:
    """Comprehensive course structure with realistic academic parameters"""
    id: str
    name: str
    code: str
    department: str
    lecture_hours: int
    lab_hours: int
    num_students: int
    required_expertise: List[Expertise]
    difficulty_level: int
    min_professors: int
    max_professors: int
    assessment_hours: int
    prep_factor: float
    can_be_shared: bool
    semester: str

@dataclass
class Professor:
    """Comprehensive faculty member with realistic workload model"""
    id: str
    name: str
    title: str
    department: str
    expertise: List[Expertise]
    primary_expertise: Expertise
    years_experience: int
    research_allocation: float
    admin_load: float
    max_teaching_load: float
    min_teaching_load: float
    preferences: Dict[str, float]
    teaching_quality: float
    availability: List[str]

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def string_to_expertise_list(expertise_str: str) -> List[Expertise]:
    """Convert semicolon-separated expertise string to list of Expertise enums"""
    if pd.isna(expertise_str) or expertise_str == '':
        return []
    
    expertise_names = [name.strip() for name in expertise_str.split(';')]
    expertise_list = []
    
    for name in expertise_names:
        try:
            # Find the enum by value
            for expertise in Expertise:
                if expertise.value == name:
                    expertise_list.append(expertise)
                    break
        except ValueError:
            print(f"Warning: Could not find expertise '{name}'")
            continue
    
    return expertise_list

def string_to_availability_list(availability_str: str) -> List[str]:
    """Convert semicolon-separated availability string to list"""
    if pd.isna(availability_str) or availability_str == '':
        return []
    
    return [semester.strip() for semester in availability_str.split(';')]

def string_to_preferences_dict(preferences_str: str) -> Dict[str, float]:
    """Convert preferences string to dictionary (placeholder for now)"""
    # This would need to be implemented based on how preferences are stored
    # For now, return empty dict
    return {}

def load_courses_from_csv(filepath: str) -> List[Course]:
    """Load courses from CSV file"""
    try:
        df = pd.read_csv(filepath)
        courses = []
        
        for _, row in df.iterrows():
            course = Course(
                id=str(row['id']),
                name=str(row['name']),
                code=str(row['code']),
                department=str(row['department']),
                lecture_hours=int(row['lecture_hours']),
                lab_hours=int(row['lab_hours']),
                num_students=int(row['num_students']),
                required_expertise=string_to_expertise_list(row['required_expertise']),
                difficulty_level=int(row['difficulty_level']),
                min_professors=int(row['min_professors']),
                max_professors=int(row['max_professors']),
                assessment_hours=int(row['assessment_hours']),
                prep_factor=float(row['prep_factor']),
                can_be_shared=bool(row['can_be_shared']),
                semester=str(row['semester'])
            )
            courses.append(course)
        
        print(f"Loaded {len(courses)} courses from {filepath}")
        return courses
        
    except Exception as e:
        print(f"Error loading courses from {filepath}: {e}")
        return []

def load_professors_from_csv(filepath: str) -> List[Professor]:
    """Load professors from CSV file"""
    try:
        df = pd.read_csv(filepath)
        professors = []
        
        for _, row in df.iterrows():
            # Generate preferences for all courses (placeholder)
            preferences = {}
            for i in range(80):  # Assuming 80 courses
                course_id = f"C{i+1:03d}"
                preferences[course_id] = np.random.uniform(0.5, 1.0)
            
            professor = Professor(
                id=str(row['id']),
                name=str(row['name']),
                title=str(row['title']),
                department=str(row['department']),
                expertise=string_to_expertise_list(row['expertise']),
                primary_expertise=string_to_expertise_list(row['primary_expertise'])[0] if string_to_expertise_list(row['primary_expertise']) else Expertise.COMPUTER_SCIENCE,
                years_experience=int(row['years_experience']),
                research_allocation=float(row['research_allocation']),
                admin_load=float(row['admin_load']),
                max_teaching_load=float(row['max_teaching_load']),
                min_teaching_load=float(row['min_teaching_load']),
                preferences=preferences,
                teaching_quality=float(row['teaching_quality']),
                availability=string_to_availability_list(row['availability'])
            )
            professors.append(professor)
        
        print(f"Loaded {len(professors)} professors from {filepath}")
        return professors
        
    except Exception as e:
        print(f"Error loading professors from {filepath}: {e}")
        return []

def load_dataset(data_dir: str = "data") -> Tuple[List[Professor], List[Course]]:
    """Load the complete dataset from CSV files"""
    print("Loading university dataset...")
    print("="*50)
    
    # Load courses and professors
    courses = load_courses_from_csv(f"{data_dir}/courses.csv")
    professors = load_professors_from_csv(f"{data_dir}/professors.csv")
    
    if not courses or not professors:
        raise ValueError("Failed to load dataset")
    
    print(f"\nDataset loaded successfully:")
    print(f"- {len(professors)} professors")
    print(f"- {len(courses)} courses")
    
    # Print some statistics
    print("\nDataset Statistics:")
    print("-" * 30)
    
    # Department distribution
    dept_counts = {}
    for prof in professors:
        dept = prof.department
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    print("Top 10 departments by professor count:")
    sorted_depts = sorted(dept_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for dept, count in sorted_depts:
        print(f"  {dept}: {count} professors")
    
    # Course difficulty distribution
    difficulty_counts = {}
    for course in courses:
        level = course.difficulty_level
        difficulty_counts[level] = difficulty_counts.get(level, 0) + 1
    
    print("\nCourse distribution by difficulty:")
    for level in sorted(difficulty_counts.keys()):
        level_name = {1: "UG Year 1", 2: "UG Year 2", 3: "UG Year 3", 4: "UG Year 4", 5: "Graduate"}[level]
        print(f"  {level_name} (Level {level}): {difficulty_counts[level]} courses")
    
    # Team teaching capability
    shared_courses = sum(1 for course in courses if course.can_be_shared)
    print(f"\nTeam teaching capability:")
    print(f"  Courses that can be shared: {shared_courses} ({shared_courses/len(courses)*100:.1f}%)")
    print(f"  Single-professor courses: {len(courses) - shared_courses}")
    
    return professors, courses

def get_dataset_summary(professors: List[Professor], courses: List[Course]) -> Dict:
    """Get a comprehensive summary of the dataset"""
    summary = {
        'total_professors': len(professors),
        'total_courses': len(courses),
        'departments': {},
        'expertise_areas': {},
        'course_difficulty': {},
        'team_teaching_stats': {
            'shared_courses': 0,
            'single_courses': 0,
            'avg_max_professors': 0,
            'avg_min_professors': 0
        },
        'workload_stats': {
            'avg_research_allocation': 0,
            'avg_admin_load': 0,
            'avg_max_teaching': 0,
            'avg_min_teaching': 0
        }
    }
    
    # Department counts
    for prof in professors:
        dept = prof.department
        summary['departments'][dept] = summary['departments'].get(dept, 0) + 1
    
    # Expertise counts
    for prof in professors:
        for expertise in prof.expertise:
            summary['expertise_areas'][expertise.value] = summary['expertise_areas'].get(expertise.value, 0) + 1
    
    # Course difficulty counts
    for course in courses:
        level = course.difficulty_level
        summary['course_difficulty'][level] = summary['course_difficulty'].get(level, 0) + 1
    
    # Team teaching stats
    shared_count = sum(1 for course in courses if course.can_be_shared)
    summary['team_teaching_stats']['shared_courses'] = shared_count
    summary['team_teaching_stats']['single_courses'] = len(courses) - shared_count
    summary['team_teaching_stats']['avg_max_professors'] = np.mean([course.max_professors for course in courses])
    summary['team_teaching_stats']['avg_min_professors'] = np.mean([course.min_professors for course in courses])
    
    # Workload stats
    summary['workload_stats']['avg_research_allocation'] = np.mean([prof.research_allocation for prof in professors])
    summary['workload_stats']['avg_admin_load'] = np.mean([prof.admin_load for prof in professors])
    summary['workload_stats']['avg_max_teaching'] = np.mean([prof.max_teaching_load for prof in professors])
    summary['workload_stats']['avg_min_teaching'] = np.mean([prof.min_teaching_load for prof in professors])
    
    return summary

def main():
    """Test the data loader"""
    try:
        professors, courses = load_dataset()
        
        print("\n" + "="*50)
        print("DATASET LOADING TEST COMPLETED SUCCESSFULLY")
        print("="*50)
        
        # Get and display summary
        summary = get_dataset_summary(professors, courses)
        
        print(f"\nDataset Summary:")
        print(f"- Total Professors: {summary['total_professors']}")
        print(f"- Total Courses: {summary['total_courses']}")
        print(f"- Departments: {len(summary['departments'])}")
        print(f"- Expertise Areas: {len(summary['expertise_areas'])}")
        
        print(f"\nTeam Teaching Capability:")
        print(f"- Shared Courses: {summary['team_teaching_stats']['shared_courses']}")
        print(f"- Single Courses: {summary['team_teaching_stats']['single_courses']}")
        print(f"- Avg Max Professors per Course: {summary['team_teaching_stats']['avg_max_professors']:.2f}")
        
        print(f"\nWorkload Averages:")
        print(f"- Research Allocation: {summary['workload_stats']['avg_research_allocation']:.2%}")
        print(f"- Admin Load: {summary['workload_stats']['avg_admin_load']:.1f} hours/week")
        print(f"- Max Teaching: {summary['workload_stats']['avg_max_teaching']:.1f} hours/week")
        print(f"- Min Teaching: {summary['workload_stats']['avg_min_teaching']:.1f} hours/week")
        
        return True
        
    except Exception as e:
        print(f"Error in data loading test: {e}")
        return False

if __name__ == "__main__":
    main()
