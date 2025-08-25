#!/usr/bin/env python3
"""
Data Adapter for Workload Allocation System
Converts CSV dataset format to workload allocator format
"""

import pandas as pd
from typing import List, Dict, Tuple
from workload_allocator import Professor, Course, Expertise, WorkloadAllocationProblem
import numpy as np

def string_to_expertise_list(expertise_str: str) -> List[Expertise]:
    """Convert semicolon-separated expertise string to list of Expertise enums"""
    if pd.isna(expertise_str) or expertise_str == '':
        return [Expertise.COMPUTER_SCIENCE]  # Default
    
    expertise_names = [exp.strip() for exp in expertise_str.split(';')]
    expertise_list = []
    
    # Map string names to Expertise enum values
    expertise_mapping = {
        'Computer Science': Expertise.COMPUTER_SCIENCE,
        'Software Engineering': Expertise.SOFTWARE_ENGINEERING,
        'Machine Learning': Expertise.MACHINE_LEARNING,
        'Data Science': Expertise.DATA_SCIENCE,
        'Algorithms': Expertise.ALGORITHMS,
        'Database Systems': Expertise.DATABASES,
        'Computer Networks': Expertise.NETWORKS,
        'Cybersecurity': Expertise.CYBERSECURITY,
        'Mathematics': Expertise.MATHEMATICS,
        'Statistics': Expertise.STATISTICS,
        'Physics': Expertise.PHYSICS,
        'Engineering': Expertise.ENGINEERING,
        'Business': Expertise.BUSINESS,
        'Psychology': Expertise.PSYCHOLOGY,
        'Sociology': Expertise.SOCIOLOGY,
        'Philosophy': Expertise.PHILOSOPHY,
        'History': Expertise.HISTORY,
        'Biology': Expertise.BIOLOGY,
        'Chemistry': Expertise.CHEMISTRY,
        'Medicine': Expertise.MEDICINE
    }
    
    for exp_name in expertise_names:
        if exp_name in expertise_mapping:
            expertise_list.append(expertise_mapping[exp_name])
        else:
            # Try to find partial matches
            for key, value in expertise_mapping.items():
                if exp_name.lower() in key.lower() or key.lower() in exp_name.lower():
                    expertise_list.append(value)
                    break
            else:
                # Default fallback
                expertise_list.append(Expertise.COMPUTER_SCIENCE)
    
    return expertise_list if expertise_list else [Expertise.COMPUTER_SCIENCE]

def string_to_availability_list(availability_str: str) -> List[str]:
    """Convert availability string to list"""
    if pd.isna(availability_str) or availability_str == '':
        return ['Fall', 'Spring']
    
    return [sem.strip() for sem in availability_str.split(';')]

def load_professors_from_csv(filepath: str) -> List[Professor]:
    """Load professors from CSV file"""
    df = pd.read_csv(filepath)
    professors = []
    
    for _, row in df.iterrows():
        expertise_list = string_to_expertise_list(row['expertise'])
        primary_expertise = string_to_expertise_list(row['primary_expertise'])[0]
        availability_list = string_to_availability_list(row['availability'])
        
        professor = Professor(
            id=row['id'],
            name=row['name'],
            title=row['title'],
            department=row['department'],
            expertise=expertise_list,
            primary_expertise=primary_expertise,
            years_experience=int(row['years_experience']),
            research_allocation=float(row['research_allocation']),
            admin_load=float(row['admin_load']),
            max_teaching_load=float(row['max_teaching_load']),
            min_teaching_load=float(row['min_teaching_load']),
            teaching_quality=float(row['teaching_quality']),
            availability=availability_list
        )
        professors.append(professor)
    
    return professors

def load_courses_from_csv(filepath: str) -> List[Course]:
    """Load courses from CSV file"""
    df = pd.read_csv(filepath)
    courses = []
    
    for _, row in df.iterrows():
        required_expertise = string_to_expertise_list(row['required_expertise'])
        
        course = Course(
            id=row['id'],
            name=row['name'],
            code=row['code'],
            department=row['department'],
            lecture_hours=int(row['lecture_hours']),
            lab_hours=int(row['lab_hours']),
            num_students=int(row['num_students']),
            required_expertise=required_expertise,
            difficulty_level=int(row['difficulty_level']),
            min_professors=int(row['min_professors']),
            max_professors=int(row['max_professors']),
            assessment_hours=int(row['assessment_hours']),
            prep_factor=float(row['prep_factor']),
            can_be_shared=bool(row['can_be_shared']),
            semester=row['semester']
        )
        courses.append(course)
    
    return courses

def create_test_dataset():
    """Create a smaller test dataset for algorithm testing"""
    # Create test professors with more reasonable workload constraints
    test_professors = [
        Professor(
            id="P001",
            name="Dr. Alice Johnson",
            title="Assistant Professor",
            department="Computer Science",
            expertise=[Expertise.COMPUTER_SCIENCE],
            primary_expertise=Expertise.COMPUTER_SCIENCE,
            years_experience=5,
            research_allocation=0.3,
            admin_load=5.0,
            max_teaching_load=20.0,
            min_teaching_load=4.0,  # Reduced from 8.0
            teaching_quality=0.85,
            availability=['Fall', 'Spring']
        ),
        Professor(
            id="P002", 
            name="Dr. Bob Smith",
            title="Associate Professor",
            department="Computer Science",
            expertise=[Expertise.COMPUTER_SCIENCE],
            primary_expertise=Expertise.COMPUTER_SCIENCE,
            years_experience=8,
            research_allocation=0.4,
            admin_load=6.0,
            max_teaching_load=18.0,
            min_teaching_load=4.0,  # Reduced from 8.0
            teaching_quality=0.88,
            availability=['Fall', 'Spring']
        ),
        Professor(
            id="P003",
            name="Dr. Carol Davis",
            title="Assistant Professor",
            department="Computer Science", 
            expertise=[Expertise.COMPUTER_SCIENCE],
            primary_expertise=Expertise.COMPUTER_SCIENCE,
            years_experience=6,
            research_allocation=0.35,
            admin_load=4.0,
            max_teaching_load=16.0,
            min_teaching_load=4.0,  # Reduced from 8.0
            teaching_quality=0.82,
            availability=['Fall', 'Spring']
        ),
        Professor(
            id="P004",
            name="Dr. David Wilson",
            title="Associate Professor",
            department="Computer Science",
            expertise=[Expertise.COMPUTER_SCIENCE],
            primary_expertise=Expertise.COMPUTER_SCIENCE,
            years_experience=10,
            research_allocation=0.45,
            admin_load=7.0,
            max_teaching_load=20.0,
            min_teaching_load=4.0,  # Reduced from 8.0
            teaching_quality=0.90,
            availability=['Fall', 'Spring']
        ),
        Professor(
            id="P005",
            name="Dr. Eve Brown",
            title="Assistant Professor",
            department="Computer Science",
            expertise=[Expertise.COMPUTER_SCIENCE],
            primary_expertise=Expertise.COMPUTER_SCIENCE,
            years_experience=4,
            research_allocation=0.25,
            admin_load=3.0,
            max_teaching_load=18.0,
            min_teaching_load=4.0,  # Reduced from 8.0
            teaching_quality=0.80,
            availability=['Fall', 'Spring']
        )
    ]
    
    # Create test courses with more reasonable workload
    test_courses = [
        Course(
            id="C001",
            name="Introduction to Programming",
            code="CS101",
            department="Computer Science",
            lecture_hours=2,
            lab_hours=1,
            num_students=40,
            required_expertise=[Expertise.COMPUTER_SCIENCE],
            difficulty_level=1,
            min_professors=1,
            max_professors=2,
            assessment_hours=10,
            prep_factor=1.2,
            can_be_shared=True,
            semester="Fall"
        ),
        Course(
            id="C002",
            name="Data Structures",
            code="CS201",
            department="Computer Science", 
            lecture_hours=3,
            lab_hours=1,
            num_students=35,
            required_expertise=[Expertise.COMPUTER_SCIENCE],
            difficulty_level=2,
            min_professors=1,
            max_professors=2,
            assessment_hours=12,
            prep_factor=1.3,
            can_be_shared=True,
            semester="Fall"
        ),
        Course(
            id="C003",
            name="Algorithms",
            code="CS301",
            department="Computer Science",
            lecture_hours=3,
            lab_hours=1,
            num_students=30,
            required_expertise=[Expertise.COMPUTER_SCIENCE],
            difficulty_level=3,
            min_professors=1,
            max_professors=2,
            assessment_hours=15,
            prep_factor=1.4,
            can_be_shared=True,
            semester="Spring"
        ),
        Course(
            id="C004",
            name="Database Systems",
            code="CS401",
            department="Computer Science",
            lecture_hours=2,
            lab_hours=1,
            num_students=25,
            required_expertise=[Expertise.COMPUTER_SCIENCE],
            difficulty_level=3,
            min_professors=1,
            max_professors=2,
            assessment_hours=14,
            prep_factor=1.3,
            can_be_shared=True,
            semester="Spring"
        ),
        Course(
            id="C005",
            name="Software Engineering",
            code="CS501",
            department="Computer Science",
            lecture_hours=3,
            lab_hours=1,
            num_students=20,
            required_expertise=[Expertise.COMPUTER_SCIENCE],
            difficulty_level=4,
            min_professors=1,
            max_professors=2,
            assessment_hours=18,
            prep_factor=1.5,
            can_be_shared=True,
            semester="Spring"
        )
    ]
    
    return test_professors, test_courses

def load_dataset(data_dir: str = "data") -> Tuple[List[Professor], List[Course]]:
    """Load the full dataset"""
    try:
        professors = load_professors_from_csv(f"{data_dir}/professors.csv")
        courses = load_courses_from_csv(f"{data_dir}/courses.csv")
        return professors, courses
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Falling back to test dataset...")
        return create_test_dataset()

def create_problem(professors: List[Professor], courses: List[Course]) -> WorkloadAllocationProblem:
    """Create a workload allocation problem instance"""
    return WorkloadAllocationProblem(professors, courses)

def get_dataset_summary(professors: List[Professor], courses: List[Course]) -> Dict:
    """Get summary statistics of the dataset"""
    return {
        'num_professors': len(professors),
        'num_courses': len(courses),
        'departments': list(set(p.department for p in professors)),
        'expertise_areas': list(set(exp.value for p in professors for exp in p.expertise)),
        'course_difficulty_distribution': {
            level: len([c for c in courses if c.difficulty_level == level])
            for level in range(1, 6)
        },
        'team_teaching_capability': {
            'can_be_shared': len([c for c in courses if c.can_be_shared]),
            'cannot_be_shared': len([c for c in courses if not c.can_be_shared])
        },
        'workload_constraints': {
            'avg_min_teaching': np.mean([p.min_teaching_load for p in professors]),
            'avg_max_teaching': np.mean([p.max_teaching_load for p in professors]),
            'avg_research_allocation': np.mean([p.research_allocation for p in professors]),
            'avg_admin_load': np.mean([p.admin_load for p in professors])
        }
    }
