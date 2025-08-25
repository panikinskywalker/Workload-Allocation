#!/usr/bin/env python3
"""
Comprehensive Dataset Generator for University Faculty Workload Allocation
Generates realistic data for 100 professors and 80 courses across multiple departments
"""

import numpy as np
import pandas as pd
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# EXPANDED EXPERTISE AREAS FOR MULTI-DEPARTMENT UNIVERSITY
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

# ============================================================================
# REALISTIC DATA STRUCTURES
# ============================================================================

@dataclass
class Course:
    """Comprehensive course structure with realistic academic parameters"""
    id: str
    name: str
    code: str  # e.g., "COMP101", "MATH201"
    department: str
    lecture_hours: int  # Hours per week
    lab_hours: int  # Lab hours per week
    num_students: int  # Total enrolled students
    required_expertise: List[Expertise]
    difficulty_level: int  # 1-5 (UG year 1 to PhD)
    min_professors: int  # Minimum professors needed
    max_professors: int  # Maximum professors (for team teaching)
    assessment_hours: int  # Total assessment hours per semester
    prep_factor: float  # Preparation time multiplier
    can_be_shared: bool  # Whether course can be team-taught
    semester: str  # Fall, Spring, Summer, or Both

@dataclass
class Professor:
    """Comprehensive faculty member with realistic workload model"""
    id: str
    name: str
    title: str  # Professor, Associate Prof, Assistant Prof, Lecturer
    department: str
    expertise: List[Expertise]
    primary_expertise: Expertise
    years_experience: int
    research_allocation: float  # % of time for research (0.2-0.4)
    admin_load: float  # Admin hours per week
    max_teaching_load: float  # Maximum teaching hours per week
    min_teaching_load: float  # Minimum teaching hours per week
    preferences: Dict[str, float]  # Course preferences
    teaching_quality: float  # Historical teaching score (0.0-1.0)
    availability: List[str]  # Semesters available

# ============================================================================
# DATASET GENERATION FUNCTIONS
# ============================================================================

def generate_professor_names() -> List[str]:
    """Generate realistic professor names"""
    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna",
        "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle",
        "Kenneth", "Laura", "Kevin", "Emily", "Brian", "Kimberly", "George", "Deborah",
        "Edward", "Dorothy", "Ronald", "Lisa", "Timothy", "Nancy", "Jason", "Karen",
        "Jeffrey", "Betty", "Ryan", "Helen", "Jacob", "Sandra", "Gary", "Donna",
        "Nicholas", "Carol", "Eric", "Ruth", "Jonathan", "Sharon", "Stephen", "Michelle",
        "Larry", "Laura", "Justin", "Emily", "Scott", "Kimberly", "Brandon", "Deborah",
        "Benjamin", "Dorothy", "Frank", "Lisa", "Gregory", "Nancy", "Raymond", "Karen",
        "Samuel", "Betty", "Patrick", "Helen", "Alexander", "Sandra", "Jack", "Donna",
        "Dennis", "Carol", "Jerry", "Ruth", "Tyler", "Sharon", "Aaron", "Michelle",
        "Jose", "Laura", "Adam", "Emily", "Nathan", "Kimberly", "Henry", "Deborah"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
        "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
        "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
        "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
        "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox",
        "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett",
        "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders"
    ]
    
    names = []
    for _ in range(100):
        first = random.choice(first_names)
        last = random.choice(last_names)
        names.append(f"{first} {last}")
    
    return names

def generate_departments() -> List[str]:
    """Generate realistic university departments"""
    return [
        "Computer Science & Engineering",
        "Mathematics & Statistics", 
        "Physics & Astronomy",
        "Mechanical Engineering",
        "Electrical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Biomedical Engineering",
        "Business Administration",
        "Economics",
        "Psychology",
        "Sociology",
        "Philosophy",
        "History",
        "English Literature",
        "Political Science",
        "Communication Studies",
        "Biology",
        "Chemistry",
        "Biochemistry",
        "Environmental Science",
        "Geology",
        "Medicine",
        "Nursing",
        "Public Health",
        "Pharmacy"
    ]

def generate_course_data() -> List[Course]:
    """Generate 80 realistic courses across multiple departments"""
    courses = []
    
    # Computer Science Courses (20 courses)
    cs_courses = [
        ("CS101", "Introduction to Programming", "COMP", 3, 2, 120, [Expertise.COMPUTER_SCIENCE], 1, 1, 2, 30, 1.5, True, "Both"),
        ("CS102", "Data Structures", "COMP", 3, 2, 100, [Expertise.DATA_STRUCTURES], 2, 1, 2, 25, 1.8, True, "Both"),
        ("CS201", "Algorithms", "COMP", 3, 1, 80, [Expertise.ALGORITHMS], 2, 1, 2, 20, 2.0, True, "Both"),
        ("CS202", "Computer Organization", "COMP", 3, 2, 90, [Expertise.COMPUTER_ENGINEERING], 2, 1, 2, 25, 1.7, True, "Both"),
        ("CS301", "Operating Systems", "COMP", 3, 2, 70, [Expertise.OPERATING_SYSTEMS], 3, 1, 2, 20, 2.2, True, "Both"),
        ("CS302", "Database Systems", "COMP", 3, 2, 85, [Expertise.DATABASE_SYSTEMS], 3, 1, 2, 25, 1.9, True, "Both"),
        ("CS401", "Software Engineering", "COMP", 3, 2, 60, [Expertise.SOFTWARE_ENGINEERING], 4, 1, 3, 30, 2.5, True, "Both"),
        ("CS402", "Computer Networks", "COMP", 3, 1, 65, [Expertise.COMPUTER_NETWORKS], 4, 1, 2, 20, 2.1, True, "Both"),
        ("CS501", "Artificial Intelligence", "COMP", 3, 1, 50, [Expertise.ARTIFICIAL_INTELLIGENCE], 5, 1, 2, 20, 2.8, True, "Both"),
        ("CS502", "Machine Learning", "COMP", 3, 1, 55, [Expertise.MACHINE_LEARNING], 5, 1, 2, 25, 2.6, True, "Both"),
        ("CS601", "Advanced Algorithms", "COMP", 3, 0, 40, [Expertise.ALGORITHMS], 5, 1, 2, 20, 3.0, False, "Both"),
        ("CS602", "Computer Graphics", "COMP", 3, 1, 45, [Expertise.COMPUTER_GRAPHICS], 5, 1, 2, 20, 2.4, True, "Both"),
        ("CS701", "Research Methods", "COMP", 2, 1, 30, [Expertise.COMPUTER_SCIENCE], 5, 1, 2, 15, 2.5, False, "Both"),
        ("CS702", "Thesis Project", "COMP", 1, 0, 25, [Expertise.COMPUTER_SCIENCE], 5, 1, 1, 40, 3.5, False, "Both"),
        ("CS801", "Advanced Topics", "COMP", 3, 0, 20, [Expertise.COMPUTER_SCIENCE], 5, 1, 2, 20, 3.2, False, "Both"),
        ("CS802", "Seminar", "COMP", 2, 0, 15, [Expertise.COMPUTER_SCIENCE], 5, 1, 2, 15, 2.8, False, "Both"),
        ("CS803", "Independent Study", "COMP", 1, 0, 10, [Expertise.COMPUTER_SCIENCE], 5, 1, 1, 30, 3.0, False, "Both"),
        ("CS804", "Special Topics", "COMP", 3, 1, 35, [Expertise.COMPUTER_SCIENCE], 4, 1, 2, 20, 2.3, True, "Both"),
        ("CS805", "Capstone Project", "COMP", 2, 2, 45, [Expertise.SOFTWARE_ENGINEERING], 4, 1, 3, 35, 2.7, True, "Both"),
        ("CS806", "Internship", "COMP", 0, 8, 60, [Expertise.COMPUTER_SCIENCE], 4, 1, 2, 10, 1.5, True, "Both")
    ]
    
    # Mathematics Courses (15 courses)
    math_courses = [
        ("MATH101", "Calculus I", "MATH", 4, 1, 200, [Expertise.CALCULUS], 1, 1, 3, 40, 1.8, True, "Both"),
        ("MATH102", "Calculus II", "MATH", 4, 1, 180, [Expertise.CALCULUS], 1, 1, 3, 35, 1.9, True, "Both"),
        ("MATH201", "Linear Algebra", "MATH", 3, 1, 150, [Expertise.LINEAR_ALGEBRA], 2, 1, 2, 25, 2.0, True, "Both"),
        ("MATH202", "Differential Equations", "MATH", 3, 1, 120, [Expertise.DIFFERENTIAL_EQUATIONS], 2, 1, 2, 30, 2.2, True, "Both"),
        ("MATH301", "Advanced Calculus", "MATH", 3, 0, 80, [Expertise.CALCULUS], 3, 1, 2, 25, 2.5, True, "Both"),
        ("MATH302", "Abstract Algebra", "MATH", 3, 0, 60, [Expertise.PURE_MATHEMATICS], 3, 1, 2, 20, 2.8, False, "Both"),
        ("MATH401", "Real Analysis", "MATH", 3, 0, 50, [Expertise.PURE_MATHEMATICS], 4, 1, 2, 25, 3.0, False, "Both"),
        ("MATH402", "Complex Analysis", "MATH", 3, 0, 45, [Expertise.PURE_MATHEMATICS], 4, 1, 2, 20, 2.9, False, "Both"),
        ("MATH501", "Numerical Analysis", "MATH", 3, 1, 40, [Expertise.NUMERICAL_ANALYSIS], 5, 1, 2, 25, 2.7, True, "Both"),
        ("MATH502", "Mathematical Modeling", "MATH", 3, 1, 35, [Expertise.MATHEMATICAL_MODELING], 5, 1, 2, 30, 2.8, True, "Both"),
        ("MATH601", "Topology", "MATH", 3, 0, 30, [Expertise.PURE_MATHEMATICS], 5, 1, 2, 20, 3.2, False, "Both"),
        ("MATH602", "Differential Geometry", "MATH", 3, 0, 25, [Expertise.PURE_MATHEMATICS], 5, 1, 2, 20, 3.1, False, "Both"),
        ("MATH701", "Research Seminar", "MATH", 2, 0, 20, [Expertise.MATHEMATICS], 5, 1, 2, 15, 2.8, False, "Both"),
        ("MATH702", "Thesis", "MATH", 1, 0, 15, [Expertise.MATHEMATICS], 5, 1, 1, 40, 3.5, False, "Both"),
        ("MATH703", "Independent Study", "MATH", 1, 0, 10, [Expertise.MATHEMATICS], 5, 1, 1, 30, 3.0, False, "Both")
    ]
    
    # Business Courses (12 courses)
    business_courses = [
        ("BUS101", "Introduction to Business", "BUS", 3, 0, 180, [Expertise.BUSINESS_ADMINISTRATION], 1, 1, 2, 25, 1.5, True, "Both"),
        ("BUS201", "Principles of Management", "BUS", 3, 0, 150, [Expertise.MANAGEMENT], 2, 1, 2, 20, 1.8, True, "Both"),
        ("BUS202", "Financial Accounting", "BUS", 3, 1, 160, [Expertise.ACCOUNTING], 2, 1, 2, 30, 2.0, True, "Both"),
        ("BUS301", "Marketing Principles", "BUS", 3, 0, 140, [Expertise.MARKETING], 3, 1, 2, 25, 1.9, True, "Both"),
        ("BUS302", "Corporate Finance", "BUS", 3, 0, 120, [Expertise.FINANCE], 3, 1, 2, 30, 2.2, True, "Both"),
        ("BUS401", "Operations Management", "BUS", 3, 1, 100, [Expertise.OPERATIONS_RESEARCH], 4, 1, 2, 25, 2.3, True, "Both"),
        ("BUS402", "Strategic Management", "BUS", 3, 0, 90, [Expertise.MANAGEMENT], 4, 1, 2, 30, 2.4, True, "Both"),
        ("BUS501", "Business Analytics", "BUS", 3, 1, 70, [Expertise.DATA_SCIENCE], 5, 1, 2, 25, 2.6, True, "Both"),
        ("BUS502", "Supply Chain Management", "BUS", 3, 0, 65, [Expertise.SUPPLY_CHAIN], 5, 1, 2, 20, 2.3, True, "Both"),
        ("BUS601", "Research Methods", "BUS", 2, 1, 45, [Expertise.BUSINESS_ADMINISTRATION], 5, 1, 2, 20, 2.5, True, "Both"),
        ("BUS602", "Thesis Project", "BUS", 1, 0, 35, [Expertise.BUSINESS_ADMINISTRATION], 5, 1, 1, 40, 3.2, False, "Both"),
        ("BUS603", "Capstone", "BUS", 2, 1, 50, [Expertise.BUSINESS_ADMINISTRATION], 4, 1, 3, 35, 2.7, True, "Both")
    ]
    
    # Engineering Courses (15 courses)
    engineering_courses = [
        ("ME101", "Engineering Mechanics", "MECH", 4, 2, 150, [Expertise.MECHANICAL_ENGINEERING], 1, 1, 2, 30, 2.0, True, "Both"),
        ("ME201", "Thermodynamics", "MECH", 3, 1, 120, [Expertise.MECHANICAL_ENGINEERING], 2, 1, 2, 25, 2.2, True, "Both"),
        ("ME301", "Machine Design", "MECH", 3, 2, 90, [Expertise.MECHANICAL_ENGINEERING], 3, 1, 2, 30, 2.4, True, "Both"),
        ("EE101", "Circuit Analysis", "ELEC", 4, 2, 140, [Expertise.ELECTRICAL_ENGINEERING], 1, 1, 2, 30, 2.1, True, "Both"),
        ("EE201", "Electronics", "ELEC", 3, 2, 110, [Expertise.ELECTRICAL_ENGINEERING], 2, 1, 2, 25, 2.3, True, "Both"),
        ("EE301", "Control Systems", "ELEC", 3, 1, 80, [Expertise.ELECTRICAL_ENGINEERING], 3, 1, 2, 25, 2.5, True, "Both"),
        ("CE101", "Statics", "CIVIL", 4, 1, 130, [Expertise.CIVIL_ENGINEERING], 1, 1, 2, 25, 2.0, True, "Both"),
        ("CE201", "Structural Analysis", "CIVIL", 3, 1, 100, [Expertise.CIVIL_ENGINEERING], 2, 1, 2, 25, 2.2, True, "Both"),
        ("CE301", "Design of Structures", "CIVIL", 3, 2, 85, [Expertise.CIVIL_ENGINEERING], 3, 1, 2, 30, 2.4, True, "Both"),
        ("CHE101", "Chemical Principles", "CHEM", 4, 2, 120, [Expertise.CHEMICAL_ENGINEERING], 1, 1, 2, 30, 2.1, True, "Both"),
        ("CHE201", "Process Design", "CHEM", 3, 2, 95, [Expertise.CHEMICAL_ENGINEERING], 2, 1, 2, 30, 2.3, True, "Both"),
        ("CHE301", "Reaction Engineering", "CHEM", 3, 1, 75, [Expertise.CHEMICAL_ENGINEERING], 3, 1, 2, 25, 2.5, True, "Both"),
        ("BME101", "Biomechanics", "BME", 3, 1, 80, [Expertise.BIOMEDICAL_ENGINEERING], 2, 1, 2, 25, 2.2, True, "Both"),
        ("BME201", "Biomaterials", "BME", 3, 1, 60, [Expertise.BIOMEDICAL_ENGINEERING], 3, 1, 2, 25, 2.4, True, "Both"),
        ("BME301", "Medical Devices", "BME", 3, 2, 50, [Expertise.BIOMEDICAL_ENGINEERING], 4, 1, 2, 30, 2.6, True, "Both")
    ]
    
    # Science & Humanities Courses (18 courses)
    science_humanities = [
        ("PHYS101", "General Physics I", "PHYS", 4, 2, 180, [Expertise.PHYSICS], 1, 1, 3, 35, 2.0, True, "Both"),
        ("PHYS102", "General Physics II", "PHYS", 4, 2, 160, [Expertise.PHYSICS], 1, 1, 3, 30, 2.1, True, "Both"),
        ("PHYS201", "Modern Physics", "PHYS", 3, 1, 120, [Expertise.PHYSICS], 2, 1, 2, 25, 2.3, True, "Both"),
        ("CHEM101", "General Chemistry", "CHEM", 4, 2, 200, [Expertise.CHEMISTRY], 1, 1, 3, 35, 2.0, True, "Both"),
        ("CHEM201", "Organic Chemistry", "CHEM", 3, 2, 150, [Expertise.CHEMISTRY], 2, 1, 2, 30, 2.2, True, "Both"),
        ("BIO101", "Introduction to Biology", "BIO", 4, 2, 190, [Expertise.BIOLOGY], 1, 1, 3, 30, 1.9, True, "Both"),
        ("BIO201", "Cell Biology", "BIO", 3, 2, 130, [Expertise.BIOLOGY], 2, 1, 2, 25, 2.1, True, "Both"),
        ("PSYCH101", "Introduction to Psychology", "PSYCH", 3, 0, 220, [Expertise.PSYCHOLOGY], 1, 1, 3, 25, 1.6, True, "Both"),
        ("PSYCH201", "Research Methods", "PSYCH", 3, 1, 140, [Expertise.PSYCHOLOGY], 2, 1, 2, 30, 2.0, True, "Both"),
        ("SOC101", "Introduction to Sociology", "SOC", 3, 0, 180, [Expertise.SOCIOLOGY], 1, 1, 2, 20, 1.7, True, "Both"),
        ("SOC201", "Social Theory", "SOC", 3, 0, 120, [Expertise.SOCIOLOGY], 2, 1, 2, 25, 2.1, True, "Both"),
        ("ENG101", "Composition", "ENG", 3, 0, 250, [Expertise.ENGLISH_LITERATURE], 1, 1, 3, 30, 1.8, True, "Both"),
        ("ENG201", "Literature Survey", "ENG", 3, 0, 160, [Expertise.ENGLISH_LITERATURE], 2, 1, 2, 25, 2.0, True, "Both"),
        ("HIST101", "World History", "HIST", 3, 0, 170, [Expertise.HISTORY], 1, 1, 2, 20, 1.7, True, "Both"),
        ("HIST201", "American History", "HIST", 3, 0, 140, [Expertise.HISTORY], 2, 1, 2, 25, 1.9, True, "Both"),
        ("PHIL101", "Introduction to Philosophy", "PHIL", 3, 0, 130, [Expertise.PHILOSOPHY], 1, 1, 2, 20, 1.8, True, "Both"),
        ("ECON101", "Principles of Economics", "ECON", 3, 0, 200, [Expertise.ECONOMICS], 1, 1, 3, 25, 1.8, True, "Both"),
        ("ECON201", "Microeconomics", "ECON", 3, 0, 150, [Expertise.ECONOMICS], 2, 1, 2, 25, 2.0, True, "Both")
    ]
    
    # Combine all courses
    all_course_data = cs_courses + math_courses + business_courses + engineering_courses + science_humanities
    
    # Create Course objects
    for i, (code, name, dept_code, lec, lab, students, exp, level, min_prof, max_prof, assess, prep, shared, sem) in enumerate(all_course_data):
        course = Course(
            id=f"C{i+1:03d}",
            name=name,
            code=code,
            department=dept_code,
            lecture_hours=lec,
            lab_hours=lab,
            num_students=students,
            required_expertise=exp,
            difficulty_level=level,
            min_professors=min_prof,
            max_professors=max_prof,
            assessment_hours=assess,
            prep_factor=prep,
            can_be_shared=shared,
            semester=sem
        )
        courses.append(course)
    
    return courses

def generate_professor_data() -> List[Professor]:
    """Generate 100 realistic professors across multiple departments"""
    professors = []
    names = generate_professor_names()
    departments = generate_departments()
    
    # Department expertise mapping
    dept_expertise = {
        "Computer Science & Engineering": [
            Expertise.COMPUTER_SCIENCE, Expertise.SOFTWARE_ENGINEERING, Expertise.COMPUTER_ENGINEERING,
            Expertise.ARTIFICIAL_INTELLIGENCE, Expertise.MACHINE_LEARNING, Expertise.DEEP_LEARNING,
            Expertise.DATA_SCIENCE, Expertise.DATABASE_SYSTEMS, Expertise.COMPUTER_NETWORKS,
            Expertise.CYBERSECURITY, Expertise.HUMAN_COMPUTER_INTERACTION, Expertise.COMPUTER_GRAPHICS,
            Expertise.ALGORITHMS, Expertise.DATA_STRUCTURES, Expertise.OPERATING_SYSTEMS
        ],
        "Mathematics & Statistics": [
            Expertise.MATHEMATICS, Expertise.STATISTICS, Expertise.APPLIED_MATHEMATICS,
            Expertise.PURE_MATHEMATICS, Expertise.LINEAR_ALGEBRA, Expertise.CALCULUS,
            Expertise.DIFFERENTIAL_EQUATIONS, Expertise.NUMERICAL_ANALYSIS,
            Expertise.PROBABILITY_THEORY, Expertise.MATHEMATICAL_MODELING
        ],
        "Business Administration": [
            Expertise.BUSINESS_ADMINISTRATION, Expertise.FINANCE, Expertise.ACCOUNTING,
            Expertise.MARKETING, Expertise.MANAGEMENT, Expertise.ECONOMICS,
            Expertise.OPERATIONS_RESEARCH, Expertise.SUPPLY_CHAIN
        ],
        "Mechanical Engineering": [Expertise.MECHANICAL_ENGINEERING, Expertise.PHYSICS],
        "Electrical Engineering": [Expertise.ELECTRICAL_ENGINEERING, Expertise.PHYSICS],
        "Civil Engineering": [Expertise.CIVIL_ENGINEERING, Expertise.PHYSICS],
        "Chemical Engineering": [Expertise.CHEMICAL_ENGINEERING, Expertise.CHEMISTRY],
        "Biomedical Engineering": [Expertise.BIOMEDICAL_ENGINEERING, Expertise.BIOLOGY],
        "Physics & Astronomy": [Expertise.PHYSICS, Expertise.APPLIED_PHYSICS, Expertise.QUANTUM_PHYSICS],
        "Biology": [Expertise.BIOLOGY, Expertise.BIOCHEMISTRY],
        "Chemistry": [Expertise.CHEMISTRY, Expertise.BIOCHEMISTRY],
        "Psychology": [Expertise.PSYCHOLOGY],
        "Sociology": [Expertise.SOCIOLOGY],
        "Philosophy": [Expertise.PHILOSOPHY],
        "History": [Expertise.HISTORY],
        "English Literature": [Expertise.ENGLISH_LITERATURE, Expertise.LINGUISTICS],
        "Political Science": [Expertise.POLITICAL_SCIENCE],
        "Communication Studies": [Expertise.COMMUNICATION],
        "Economics": [Expertise.ECONOMICS],
        "Medicine": [Expertise.MEDICINE, Expertise.BIOLOGY],
        "Nursing": [Expertise.NURSING],
        "Public Health": [Expertise.PUBLIC_HEALTH],
        "Pharmacy": [Expertise.PHARMACY, Expertise.CHEMISTRY],
        "Physical Therapy": [Expertise.PHYSICAL_THERAPY, Expertise.BIOLOGY]
    }
    
    # Generate professors
    for i in range(100):
        # Assign department
        dept = random.choice(departments)
        available_expertise = dept_expertise.get(dept, [Expertise.COMPUTER_SCIENCE])
        
        # Generate expertise (2-4 areas)
        num_expertise = random.randint(2, 4)
        expertise = random.sample(available_expertise, min(num_expertise, len(available_expertise)))
        primary_expertise = random.choice(expertise)
        
        # Generate title based on experience
        years_exp = random.randint(1, 25)
        if years_exp >= 20:
            title = "Professor"
        elif years_exp >= 12:
            title = "Associate Professor"
        elif years_exp >= 6:
            title = "Assistant Professor"
        else:
            title = "Lecturer"
        
        # Generate workload parameters
        research_allocation = random.uniform(0.2, 0.4)
        admin_load = random.uniform(2, 10)
        max_teaching = random.uniform(15, 25)
        min_teaching = random.uniform(8, 12)
        teaching_quality = random.uniform(0.7, 1.0)
        
        # Generate course preferences (random weights for courses)
        preferences = {f"C{j+1:03d}": random.uniform(0.5, 1.0) for j in range(80)}
        
        # Availability (most available both semesters)
        availability = ["Fall", "Spring"] if random.random() > 0.1 else ["Fall", "Spring", "Summer"]
        
        professor = Professor(
            id=f"P{i+1:03d}",
            name=names[i],
            title=title,
            department=dept,
            expertise=expertise,
            primary_expertise=primary_expertise,
            years_experience=years_exp,
            research_allocation=research_allocation,
            admin_load=admin_load,
            max_teaching_load=max_teaching,
            min_teaching_load=min_teaching,
            preferences=preferences,
            teaching_quality=teaching_quality,
            availability=availability
        )
        professors.append(professor)
    
    return professors

def save_dataset_to_csv(professors: List[Professor], courses: List[Course], output_dir: str = "data"):
    """Save the generated dataset to CSV files"""
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save professors
    prof_data = []
    for prof in professors:
        prof_data.append({
            'id': prof.id,
            'name': prof.name,
            'title': prof.title,
            'department': prof.department,
            'expertise': ';'.join([e.value for e in prof.expertise]),
            'primary_expertise': prof.primary_expertise.value,
            'years_experience': prof.years_experience,
            'research_allocation': prof.research_allocation,
            'admin_load': prof.admin_load,
            'max_teaching_load': prof.max_teaching_load,
            'min_teaching_load': prof.min_teaching_load,
            'teaching_quality': prof.teaching_quality,
            'availability': ';'.join(prof.availability)
        })
    
    prof_df = pd.DataFrame(prof_data)
    prof_df.to_csv(f"{output_dir}/professors.csv", index=False)
    
    # Save courses
    course_data = []
    for course in courses:
        course_data.append({
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'department': course.department,
            'lecture_hours': course.lecture_hours,
            'lab_hours': course.lab_hours,
            'num_students': course.num_students,
            'required_expertise': ';'.join([e.value for e in course.required_expertise]),
            'difficulty_level': course.difficulty_level,
            'min_professors': course.min_professors,
            'max_professors': course.max_professors,
            'assessment_hours': course.assessment_hours,
            'prep_factor': course.prep_factor,
            'can_be_shared': course.can_be_shared,
            'semester': course.semester
        })
    
    course_df = pd.DataFrame(course_data)
    course_df.to_csv(f"{output_dir}/courses.csv", index=False)
    
    print(f"Dataset saved to {output_dir}/")
    print(f"- {len(professors)} professors saved to professors.csv")
    print(f"- {len(courses)} courses saved to courses.csv")

def main():
    """Generate and save the comprehensive dataset"""
    print("Generating comprehensive university dataset...")
    print("="*60)
    
    # Generate data
    professors = generate_professor_data()
    courses = generate_course_data()
    
    print(f"Generated {len(professors)} professors across multiple departments")
    print(f"Generated {len(courses)} courses with varying complexity levels")
    
    # Save to CSV
    save_dataset_to_csv(professors, courses)
    
    # Print summary statistics
    print("\nDataset Summary:")
    print("-" * 30)
    
    # Department distribution
    dept_counts = {}
    for prof in professors:
        dept = prof.department
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    print("Professor distribution by department:")
    for dept, count in sorted(dept_counts.items()):
        print(f"  {dept}: {count} professors")
    
    # Course distribution
    course_dept_counts = {}
    for course in courses:
        dept = course.department
        course_dept_counts[dept] = course_dept_counts.get(dept, 0) + 1
    
    print("\nCourse distribution by department:")
    for dept, count in sorted(course_dept_counts.items()):
        print(f"  {dept}: {count} courses")
    
    # Difficulty level distribution
    difficulty_counts = {}
    for course in courses:
        level = course.difficulty_level
        difficulty_counts[level] = difficulty_counts.get(level, 0) + 1
    
    print("\nCourse distribution by difficulty level:")
    for level in sorted(difficulty_counts.keys()):
        level_name = {1: "UG Year 1", 2: "UG Year 2", 3: "UG Year 3", 4: "UG Year 4", 5: "Graduate"}[level]
        print(f"  {level_name} (Level {level}): {difficulty_counts[level]} courses")
    
    print("\nDataset generation complete!")

if __name__ == "__main__":
    main()
