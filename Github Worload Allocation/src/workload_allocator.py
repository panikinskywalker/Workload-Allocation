#!/usr/bin/env python3
"""
Comprehensive Faculty Workload Allocation System
Implements Hill Climbing, Genetic Algorithm, and Simulated Annealing
with focus on fairness, expertise matching, and availability constraints
"""

import numpy as np
import pandas as pd
import random
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import copy
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import math

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class Expertise(Enum):
    """Faculty expertise areas"""
    COMPUTER_SCIENCE = "Computer Science"
    SOFTWARE_ENGINEERING = "Software Engineering"
    MACHINE_LEARNING = "Machine Learning"
    DATA_SCIENCE = "Data Science"
    ALGORITHMS = "Algorithms"
    DATABASES = "Database Systems"
    NETWORKS = "Computer Networks"
    CYBERSECURITY = "Cybersecurity"
    MATHEMATICS = "Mathematics"
    STATISTICS = "Statistics"
    PHYSICS = "Physics"
    ENGINEERING = "Engineering"
    BUSINESS = "Business"
    PSYCHOLOGY = "Psychology"
    SOCIOLOGY = "Sociology"
    PHILOSOPHY = "Philosophy"
    HISTORY = "History"
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    MEDICINE = "Medicine"

@dataclass
class Professor:
    """Faculty member with workload constraints"""
    id: str
    name: str
    title: str
    department: str
    expertise: List[Expertise]
    primary_expertise: Expertise
    years_experience: int
    research_allocation: float  # % of time for research
    admin_load: float  # Admin hours per week
    max_teaching_load: float  # Maximum teaching hours per week
    min_teaching_load: float  # Minimum teaching hours per week (80% of contracted)
    teaching_quality: float
    availability: List[str]
    
    def contracted_hours(self) -> float:
        """Total contracted hours per week"""
        return 40.0
    
    def available_teaching_hours(self) -> float:
        """Available hours after research and admin"""
        total = self.contracted_hours()
        research_hours = total * self.research_allocation
        remaining = total - research_hours - self.admin_load
        return min(remaining, self.max_teaching_load)

@dataclass
class Course:
    """Course with teaching requirements"""
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
    
    def total_contact_hours(self) -> float:
        """Total contact hours per week"""
        return self.lecture_hours + self.lab_hours
    
    def total_workload_hours(self) -> float:
        """Total workload including prep and assessment"""
        contact = self.total_contact_hours()
        prep = contact * self.prep_factor
        assessment = self.assessment_hours / 15  # Weekly average
        return contact + prep + assessment

@dataclass
class CourseAllocation:
    """Course allocation to professor(s)"""
    course_id: str
    professor_ids: List[str]
    shares: Dict[str, float]  # professor_id -> share percentage
    
    def get_professor_workload(self, prof_id: str, course: Course) -> float:
        """Get workload for specific professor"""
        if prof_id not in self.shares:
            return 0.0
        share = self.shares[prof_id]
        return course.total_workload_hours() * (share / 100.0)

class WorkloadAllocationProblem:
    """Main problem class for workload allocation"""
    
    def __init__(self, professors: List[Professor], courses: List[Course]):
        self.professors = {p.id: p for p in professors}
        self.courses = {c.id: c for c in courses}
        self.professor_list = professors
        self.course_list = courses
        
    def calculate_professor_load(self, prof_id: str, allocations: List[CourseAllocation]) -> Dict:
        """Calculate total workload for a professor"""
        total_workload = 0.0
        course_workloads = {}
        
        for allocation in allocations:
            if prof_id in allocation.professor_ids:
                course = self.courses[allocation.course_id]
                workload = allocation.get_professor_workload(prof_id, course)
                total_workload += workload
                course_workloads[allocation.course_id] = workload
        
        professor = self.professors[prof_id]
        contracted = professor.contracted_hours()
        research_hours = contracted * professor.research_allocation
        admin_hours = professor.admin_load
        
        return {
            'total_workload': total_workload,
            'teaching_hours': total_workload,
            'research_hours': research_hours,
            'admin_hours': admin_hours,
            'total_hours': total_workload + research_hours + admin_hours,
            'contracted_hours': contracted,
            'load_percentage': (total_workload / professor.max_teaching_load) * 100,
            'course_workloads': course_workloads
        }
    
    def calculate_fitness(self, allocations: List[CourseAllocation]) -> float:
        """Calculate overall fitness of allocation with soft constraint penalties"""
        # Check hard constraints first
        constraint_violations = self._count_constraint_violations(allocations)
        
        if constraint_violations == 0:
            # Valid solution - calculate normal fitness
            fairness_score = self.calculate_fairness_score(allocations)
            expertise_score = self.calculate_expertise_score(allocations)
            balance_score = self.calculate_balance_score(allocations)
            
            # Weighted combination
            total_fitness = (
                fairness_score * 0.4 +
                expertise_score * 0.3 +
                balance_score * 0.3
            )
            
            # Apply soft constraint penalties
            soft_penalties = self._calculate_soft_constraint_penalties(allocations)
            total_fitness -= soft_penalties
            
            return total_fitness
        else:
            # Invalid solution - use penalty for hard constraint violations
            base_penalty = -10.0 * constraint_violations
            return base_penalty
    
    def _count_constraint_violations(self, allocations: List[CourseAllocation]) -> int:
        """Count hard constraint violations - only essential constraints are hard"""
        violations = 0
        
        # Track allocated courses and professors
        allocated_courses = set()
        professors_with_courses = set()
        professor_workloads = {}
        
        # Count violations for each allocation
        for allocation in allocations:
            # Every course must be allocated
            allocated_courses.add(allocation.course_id)
            
            # Every professor must have at least one course
            for prof_id in allocation.professor_ids:
                professors_with_courses.add(prof_id)
                
                # Initialize workload tracking
                if prof_id not in professor_workloads:
                    professor_workloads[prof_id] = 0.0
                
                # Add workload for this course
                course = self.courses[allocation.course_id]
                share = allocation.shares.get(prof_id, 100.0) / 100.0
                course_workload = course.total_workload_hours() * share
                professor_workloads[prof_id] += course_workload
        
        # Hard constraint 1: All courses must be allocated
        if len(allocated_courses) != len(self.courses):
            violations += 1
        
        # Hard constraint 2: Every professor must have at least one course
        if len(professors_with_courses) != len(self.professors):
            violations += 1
        
        # Note: Workload limits and expertise matching are now SOFT constraints
        # They will be penalized in the fitness function but won't make solutions invalid
        
        return violations
    
    def check_hard_constraints(self, allocations: List[CourseAllocation]) -> bool:
        """Check if allocation satisfies essential hard constraints"""
        return self._count_constraint_violations(allocations) == 0
    
    def check_soft_constraints(self, allocations: List[CourseAllocation]) -> Dict[str, bool]:
        """Check soft constraint satisfaction"""
        results = {
            'workload_limits': True,
            'expertise_matching': True,
            'fairness': True
        }
        
        # Check workload limits
        for prof_id in self.professors:
            load = self.calculate_professor_load(prof_id, allocations)
            professor = self.professors[prof_id]
            
            if load['teaching_hours'] > professor.contracted_hours():
                results['workload_limits'] = False
                break
        
        # Check expertise matching
        for allocation in allocations:
            course = self.courses[allocation.course_id]
            for prof_id in allocation.professor_ids:
                professor = self.professors[prof_id]
                if not any(exp in professor.expertise for exp in course.required_expertise):
                    results['expertise_matching'] = False
                    break
        
        # Check fairness (no professor with 0 workload)
        for prof_id in self.professors:
            load = self.calculate_professor_load(prof_id, allocations)
            if load['teaching_hours'] == 0:
                results['fairness'] = False
                break
        
        return results
    
    def calculate_fairness_score(self, allocations: List[CourseAllocation]) -> float:
        """Calculate fairness score based on workload distribution"""
        workloads = []
        for prof_id in self.professors:
            load = self.calculate_professor_load(prof_id, allocations)
            workloads.append(load['load_percentage'])
        
        if not workloads:
            return 0.0
        
        # Calculate coefficient of variation (lower is better)
        mean_load = np.mean(workloads)
        if mean_load == 0:
            return 0.0
        
        std_load = np.std(workloads)
        cv = std_load / mean_load
        
        # Convert to 0-1 scale where 1 is most fair
        fairness = max(0, 1 - cv)
        return fairness
    
    def calculate_expertise_score(self, allocations: List[CourseAllocation]) -> float:
        """Calculate expertise matching score"""
        total_score = 0.0
        total_allocations = 0
        
        for allocation in allocations:
            course = self.courses[allocation.course_id]
            course_score = 0.0
            
            for prof_id in allocation.professor_ids:
                professor = self.professors[prof_id]
                
                # Check if professor has required expertise
                if any(exp in professor.expertise for exp in course.required_expertise):
                    course_score += 1.0
                
                # Bonus for primary expertise match
                if professor.primary_expertise in course.required_expertise:
                    course_score += 0.5
            
            total_score += course_score
            total_allocations += 1
        
        return total_score / total_allocations if total_allocations > 0 else 0.0
    
    def calculate_balance_score(self, allocations: List[CourseAllocation]) -> float:
        """Calculate workload balance score"""
        workloads = []
        for prof_id in self.professors:
            load = self.calculate_professor_load(prof_id, allocations)
            workloads.append(load['teaching_hours'])
        
        if not workloads:
            return 0.0
        
        # Calculate how close workloads are to ideal (mean)
        mean_load = np.mean(workloads)
        if mean_load == 0:
            return 0.0
        
        # Calculate average deviation from mean
        deviations = [abs(w - mean_load) for w in workloads]
        avg_deviation = np.mean(deviations)
        
        # Convert to 0-1 scale where 1 is most balanced
        balance = max(0, 1 - (avg_deviation / mean_load))
        return balance

    def _calculate_soft_constraint_penalties(self, allocations: List[CourseAllocation]) -> float:
        """Calculate penalties for soft constraint violations"""
        total_penalty = 0.0
        
        # Penalty for workload violations
        workload_penalty = self._calculate_workload_penalty(allocations)
        total_penalty += workload_penalty
        
        # Penalty for expertise mismatches
        expertise_penalty = self._calculate_expertise_penalty(allocations)
        total_penalty += expertise_penalty
        
        return total_penalty
    
    def _calculate_workload_penalty(self, allocations: List[CourseAllocation]) -> float:
        """Calculate penalty for workload constraint violations"""
        penalty = 0.0
        
        for prof_id in self.professors:
            load = self.calculate_professor_load(prof_id, allocations)
            professor = self.professors[prof_id]
            
            # Penalty for exceeding contracted hours (soft constraint)
            if load['teaching_hours'] > professor.contracted_hours():
                excess = load['teaching_hours'] - professor.contracted_hours()
                penalty += excess * 2.0  # 2x penalty for exceeding contracted hours
            
            # Penalty for being under minimum load (soft constraint)
            if load['teaching_hours'] < professor.min_teaching_load:
                deficit = professor.min_teaching_load - load['teaching_hours']
                penalty += deficit * 1.5  # 1.5x penalty for being under minimum
        
        return penalty
    
    def _calculate_expertise_penalty(self, allocations: List[CourseAllocation]) -> float:
        """Calculate penalty for expertise mismatches"""
        penalty = 0.0
        
        for allocation in allocations:
            course = self.courses[allocation.course_id]
            
            for prof_id in allocation.professor_ids:
                professor = self.professors[prof_id]
                
                # Check expertise match
                expertise_match = any(exp in professor.expertise for exp in course.required_expertise)
                
                if not expertise_match:
                    # Penalty for expertise mismatch
                    penalty += 5.0  # Base penalty for mismatch
                    
                    # Additional penalty if it's not even in primary expertise
                    if course.required_expertise[0] != professor.primary_expertise:
                        penalty += 2.0
        
        return penalty

# ============================================================================
# HILL CLIMBING ALGORITHM
# ============================================================================

class HillClimbing:
    """Hill Climbing algorithm for workload allocation"""
    
    def __init__(self, problem: WorkloadAllocationProblem, max_iterations: int = 1000):
        self.problem = problem
        self.max_iterations = max_iterations
        self.best_solution = None
        self.best_fitness = -float('inf')
    
    def generate_initial_solution(self) -> List[CourseAllocation]:
        """Generate initial feasible solution"""
        allocations = []
        
        # Track professor workloads to ensure constraints
        professor_workloads = {prof_id: 0.0 for prof_id in self.problem.professors}
        
        # Simple greedy allocation
        for course_id, course in self.problem.courses.items():
            # Find professors with matching expertise and available capacity
            suitable_professors = []
            for prof_id, prof in self.problem.professors.items():
                if any(exp in prof.expertise for exp in course.required_expertise):
                    # Check if professor has capacity
                    current_load = professor_workloads[prof_id]
                    if current_load + course.total_workload_hours() <= prof.max_teaching_load:
                        suitable_professors.append((prof_id, prof))
            
            if not suitable_professors:
                # If no suitable professor with capacity, find any with capacity
                for prof_id, prof in self.problem.professors.items():
                    current_load = professor_workloads[prof_id]
                    if current_load + course.total_workload_hours() <= prof.max_teaching_load:
                        suitable_professors.append((prof_id, prof))
            
            if not suitable_professors:
                # If still no capacity, use any professor (will be repaired later)
                suitable_professors = [(prof_id, prof) for prof_id, prof in self.problem.professors.items()]
            
            # Select professor(s) based on course requirements
            if course.can_be_shared and course.max_professors > 1:
                # Team teaching
                num_profs = min(course.max_professors, len(suitable_professors))
                selected_profs = random.sample(suitable_professors, num_profs)
                
                # Equal shares
                shares = {prof_id: 100.0 / num_profs for prof_id, _ in selected_profs}
                allocation = CourseAllocation(
                    course_id=course.id,
                    professor_ids=[prof_id for prof_id, _ in selected_profs],
                    shares=shares
                )
                
                # Update workloads
                for prof_id, _ in selected_profs:
                    workload = course.total_workload_hours() / num_profs
                    professor_workloads[prof_id] += workload
            else:
                # Single professor
                selected_prof_id, _ = random.choice(suitable_professors)
                allocation = CourseAllocation(
                    course_id=course.id,
                    professor_ids=[selected_prof_id],
                    shares={selected_prof_id: 100.0}
                )
                
                # Update workload
                professor_workloads[selected_prof_id] += course.total_workload_hours()
            
            allocations.append(allocation)
        
        return allocations
    
    def _ensure_all_professors_have_courses(self, allocations: List[CourseAllocation]):
        """Ensure every professor gets at least one course"""
        professors_with_courses = set()
        for allocation in allocations:
            professors_with_courses.update(allocation.professor_ids)
        
        # Find professors without courses
        professors_without_courses = set(self.problem.professors.keys()) - professors_with_courses
        
        for prof_id in professors_without_courses:
            # Strategy 1: Try to add to existing courses that can be shared
            added = False
            for allocation in allocations:
                course = self.problem.courses[allocation.course_id]
                if course.can_be_shared and len(allocation.professor_ids) < course.max_professors:
                    # Add this professor to the course
                    allocation.professor_ids.append(prof_id)
                    
                    # Redistribute shares equally
                    num_profs = len(allocation.professor_ids)
                    new_shares = {prof_id: 100.0 / num_profs for prof_id in allocation.professor_ids}
                    allocation.shares = new_shares
                    added = True
                    break
            
            # Strategy 2: If no shared courses available, reassign a course
            if not added:
                # Find a course that can be reassigned
                for allocation in allocations:
                    course = self.problem.courses[allocation.course_id]
                    if len(allocation.professor_ids) == 1:  # Single professor course
                        # Check if this professor has other courses
                        prof_courses = sum(1 for a in allocations if prof_id in a.professor_ids)
                        if prof_courses > 1:
                            # Reassign this course to the professor without courses
                            allocation.professor_ids = [prof_id]
                            allocation.shares = {prof_id: 100.0}
                            added = True
                            break
            
            # Strategy 3: If still no luck, create a new allocation by splitting a course
            if not added:
                for allocation in allocations:
                    course = self.problem.courses[allocation.course_id]
                    if course.can_be_shared and len(allocation.professor_ids) == 1:
                        # Split this course between the current professor and the new one
                        current_prof = allocation.professor_ids[0]
                        allocation.professor_ids = [current_prof, prof_id]
                        allocation.shares = {current_prof: 50.0, prof_id: 50.0}
                        added = True
                        break
    
    def get_neighbor(self, allocations: List[CourseAllocation]) -> List[CourseAllocation]:
        """Generate neighbor solution"""
        neighbor = copy.deepcopy(allocations)
        
        # Randomly select a course to modify
        course_idx = random.randint(0, len(neighbor) - 1)
        course = self.problem.course_list[course_idx]
        
        # Random modification strategy
        strategy = random.choice(['swap_professor', 'change_shares', 'add_professor', 'remove_professor'])
        
        if strategy == 'swap_professor':
            # Swap one professor with another
            if len(neighbor[course_idx].professor_ids) == 1:
                old_prof_id = neighbor[course_idx].professor_ids[0]
                new_prof_id = random.choice(list(self.problem.professors.keys()))
                if new_prof_id != old_prof_id:
                    neighbor[course_idx].professor_ids = [new_prof_id]
                    neighbor[course_idx].shares = {new_prof_id: 100.0}
        
        elif strategy == 'change_shares':
            # Modify share percentages
            if len(neighbor[course_idx].professor_ids) > 1:
                prof_ids = neighbor[course_idx].professor_ids
                new_shares = {}
                remaining = 100.0
                
                for i, prof_id in enumerate(prof_ids[:-1]):
                    if remaining > 0:
                        share = random.uniform(20.0, remaining - (len(prof_ids) - i - 1) * 20.0)
                        new_shares[prof_id] = share
                        remaining -= share
                    else:
                        new_shares[prof_id] = 0.0
                
                # Last professor gets remaining
                new_shares[prof_ids[-1]] = remaining
                neighbor[course_idx].shares = new_shares
        
        elif strategy == 'add_professor':
            # Add a professor if possible
            if (course.can_be_shared and 
                len(neighbor[course_idx].professor_ids) < course.max_professors):
                
                current_profs = set(neighbor[course_idx].professor_ids)
                available_profs = [p for p in self.problem.professor_list 
                                 if p.id not in current_profs]
                
                if available_profs:
                    new_prof = random.choice(available_profs)
                    neighbor[course_idx].professor_ids.append(new_prof.id)
                    
                    # Redistribute shares
                    num_profs = len(neighbor[course_idx].professor_ids)
                    new_shares = {prof_id: 100.0 / num_profs 
                                for prof_id in neighbor[course_idx].professor_ids}
                    neighbor[course_idx].shares = new_shares
        
        elif strategy == 'remove_professor':
            # Remove a professor if possible
            if len(neighbor[course_idx].professor_ids) > course.min_professors:
                prof_to_remove = random.choice(neighbor[course_idx].professor_ids)
                neighbor[course_idx].professor_ids.remove(prof_to_remove)
                
                # Redistribute shares
                remaining_profs = neighbor[course_idx].professor_ids
                if remaining_profs:
                    new_shares = {prof_id: 100.0 / len(remaining_profs) 
                                for prof_id in remaining_profs}
                    neighbor[course_idx].shares = new_shares
        
        return neighbor
    
    def solve(self) -> Tuple[List[CourseAllocation], float]:
        """Solve the allocation problem"""
        current_solution = self.generate_initial_solution()
        current_fitness = self.problem.calculate_fitness(current_solution)
        
        self.best_solution = current_solution
        self.best_fitness = current_fitness
        
        iterations_without_improvement = 0
        
        for iteration in range(self.max_iterations):
            neighbor = self.get_neighbor(current_solution)
            neighbor_fitness = self.problem.calculate_fitness(neighbor)
            
            if neighbor_fitness > current_fitness:
                current_solution = neighbor
                current_fitness = neighbor_fitness
                iterations_without_improvement = 0
                
                if current_fitness > self.best_fitness:
                    self.best_solution = copy.deepcopy(current_solution)
                    self.best_fitness = current_fitness
            else:
                iterations_without_improvement += 1
            
            # Early stopping if no improvement
            if iterations_without_improvement > 100:
                break
        
        return self.best_solution, self.best_fitness

# ============================================================================
# GENETIC ALGORITHM
# ============================================================================

class GeneticAlgorithm:
    """Genetic Algorithm for workload allocation"""
    
    def __init__(self, problem: WorkloadAllocationProblem, 
                 population_size: int = 100, generations: int = 300,
                 mutation_rate: float = 0.15, crossover_rate: float = 0.8,
                 elite_size: int = 15):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.best_solution = None
        self.best_fitness = -float('inf')
    
    def create_individual(self) -> List[CourseAllocation]:
        """Create a feasible individual"""
        allocations = []
        
        # Track professor workloads
        professor_workloads = {prof_id: 0.0 for prof_id in self.problem.professors}
        
        # Allocate courses one by one
        for course_id, course in self.problem.courses.items():
            # Find suitable professors with available capacity
            suitable_professors = []
            for prof_id, prof in self.problem.professors.items():
                # Check expertise match
                if any(exp in prof.expertise for exp in course.required_expertise):
                    # Check capacity
                    current_load = professor_workloads[prof_id]
                    course_workload = course.total_workload_hours()
                    
                    if current_load + course_workload <= prof.max_teaching_load:
                        suitable_professors.append((prof_id, prof))
            
            if not suitable_professors:
                # Find any professor with capacity
                for prof_id, prof in self.problem.professors.items():
                    current_load = professor_workloads[prof_id]
                    course_workload = course.total_workload_hours()
                    
                    if current_load + course_workload <= prof.max_teaching_load:
                        suitable_professors.append((prof_id, prof))
                        break
            
            if suitable_professors:
                # Choose randomly from suitable professors
                chosen_prof_id, _ = random.choice(suitable_professors)
                
                # Create allocation
                allocation = CourseAllocation(
                    course_id=course.id,
                    professor_ids=[chosen_prof_id],
                    shares={chosen_prof_id: 100.0}
                )
                allocations.append(allocation)
                
                # Update workload
                professor_workloads[chosen_prof_id] += course.total_workload_hours()
            else:
                # Create allocation anyway (will be repaired)
                prof_id = random.choice(list(self.problem.professors.keys()))
                allocation = CourseAllocation(
                    course_id=course.id,
                    professor_ids=[prof_id],
                    shares={prof_id: 100.0}
                )
                allocations.append(allocation)
        
        # Repair the individual
        self._ensure_all_professors_have_courses(allocations)
        
        return allocations
    
    def _ensure_all_professors_have_courses(self, allocations: List[CourseAllocation]):
        """Ensure every professor gets at least one course"""
        professors_with_courses = set()
        for allocation in allocations:
            professors_with_courses.update(allocation.professor_ids)
        
        # Find professors without courses
        professors_without_courses = set(self.problem.professors.keys()) - professors_with_courses
        
        for prof_id in professors_without_courses:
            # Find a course that can be shared or reassigned
            for allocation in allocations:
                course = self.problem.courses[allocation.course_id]
                if course.can_be_shared and len(allocation.professor_ids) < course.max_professors:
                    # Add this professor to the course
                    allocation.professor_ids.append(prof_id)
                    
                    # Redistribute shares equally
                    num_profs = len(allocation.professor_ids)
                    new_shares = {prof_id: 100.0 / num_profs for prof_id in allocation.professor_ids}
                    allocation.shares = new_shares
                    break
    
    def crossover(self, parent1: List[CourseAllocation], 
                 parent2: List[CourseAllocation]) -> List[CourseAllocation]:
        """Perform crossover between two parents"""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1)
        
        child = []
        
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child.append(copy.deepcopy(parent1[i]))
            else:
                child.append(copy.deepcopy(parent2[i]))
        
        return child
    
    def mutate(self, individual: List[CourseAllocation]):
        """Mutate an individual"""
        for allocation in individual:
            if random.random() < self.mutation_rate:
                course = self.problem.courses[allocation.course_id]
                
                # Random mutation strategy
                strategy = random.choice(['swap_professor', 'change_shares', 'modify_team'])
                
                if strategy == 'swap_professor':
                    if len(allocation.professor_ids) == 1:
                        old_prof_id = allocation.professor_ids[0]
                        new_prof_id = random.choice(list(self.problem.professors.keys()))
                        if new_prof_id != old_prof_id:
                            allocation.professor_ids = [new_prof_id]
                            allocation.shares = {new_prof_id: 100.0}
                
                elif strategy == 'change_shares':
                    if len(allocation.professor_ids) > 1:
                        prof_ids = allocation.professor_ids
                        new_shares = {}
                        remaining = 100.0
                        
                        for i, prof_id in enumerate(prof_ids[:-1]):
                            if remaining > 0:
                                share = random.uniform(20.0, remaining - (len(prof_ids) - i - 1) * 20.0)
                                new_shares[prof_id] = share
                                remaining -= share
                            else:
                                new_shares[prof_id] = 0.0
                        
                        new_shares[prof_ids[-1]] = remaining
                        allocation.shares = new_shares
    
    def tournament_selection(self, population: List[List[CourseAllocation]], 
                           tournament_size: int = 3) -> List[CourseAllocation]:
        """Select individual using tournament selection"""
        tournament = random.sample(population, tournament_size)
        tournament_fitness = [self.problem.calculate_fitness(ind) for ind in tournament]
        winner_idx = tournament_fitness.index(max(tournament_fitness))
        return copy.deepcopy(tournament[winner_idx])
    
    def solve(self) -> Tuple[List[CourseAllocation], float]:
        """Solve the allocation problem using genetic algorithm"""
        # Initialize population
        population = [self.create_individual() for _ in range(self.population_size)]
        
        # Evaluate initial population
        population_fitness = [(individual, self.problem.calculate_fitness(individual)) 
                             for individual in population]
        population_fitness.sort(key=lambda x: x[1], reverse=True)
        
        best_individual = population_fitness[0][0]
        best_fitness = population_fitness[0][1]
        
        for generation in range(self.generations):
            # Create new population
            new_population = []
            
            # Elitism: keep best individuals
            elite_size = int(self.population_size * self.elite_size)
            new_population.extend([ind for ind, _ in population_fitness[:elite_size]])
            
            # Generate rest of population
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.tournament_selection(population_fitness)
                parent2 = self.tournament_selection(population_fitness)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child = self.crossover(parent1, parent2)
                else:
                    child = copy.deepcopy(parent1)
                
                # Mutation
                if random.random() < self.mutation_rate:
                    self.mutate(child)
                
                # Ensure all professors have courses
                self._ensure_all_professors_have_courses(child)
                
                new_population.append(child)
            
            # Update population
            population = new_population
            
            # Evaluate new population
            population_fitness = [(individual, self.problem.calculate_fitness(individual)) 
                                 for individual in population]
            population_fitness.sort(key=lambda x: x[1], reverse=True)
            
            # Update best solution
            if population_fitness[0][1] > best_fitness:
                best_individual = copy.deepcopy(population_fitness[0][0])
                best_fitness = population_fitness[0][1]
        
        return best_individual, best_fitness

# ============================================================================
# SIMULATED ANNEALING
# ============================================================================

class SimulatedAnnealing:
    """Simulated Annealing algorithm for workload allocation"""
    
    def __init__(self, problem: WorkloadAllocationProblem, 
                 initial_temp: float = 100.0, cooling_rate: float = 0.995,
                 min_temp: float = 0.1, max_iterations: int = 5000):
        self.problem = problem
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations
        self.best_solution = None
        self.best_fitness = -float('inf')
    
    def generate_neighbor(self, current: List[CourseAllocation]) -> List[CourseAllocation]:
        """Generate neighbor solution"""
        neighbor = copy.deepcopy(current)
        
        # Randomly select a course to modify
        course_idx = random.randint(0, len(neighbor) - 1)
        course = self.problem.course_list[course_idx]
        
        # Random modification
        strategy = random.choice(['swap_professor', 'change_shares', 'modify_team'])
        
        if strategy == 'swap_professor':
            if len(neighbor[course_idx].professor_ids) == 1:
                old_prof_id = neighbor[course_idx].professor_ids[0]
                new_prof_id = random.choice(list(self.problem.professors.keys()))
                if new_prof_id != old_prof_id:
                    neighbor[course_idx].professor_ids = [new_prof_id]
                    neighbor[course_idx].shares = {new_prof_id: 100.0}
        
        elif strategy == 'change_shares':
            if len(neighbor[course_idx].professor_ids) > 1:
                prof_ids = neighbor[course_idx].professor_ids
                new_shares = {}
                remaining = 100.0
                
                for i, prof_id in enumerate(prof_ids[:-1]):
                    if remaining > 0:
                        share = random.uniform(20.0, remaining - (len(prof_ids) - i - 1) * 20.0)
                        new_shares[prof_id] = share
                        remaining -= share
                    else:
                        new_shares[prof_id] = 0.0
                
                new_shares[prof_ids[-1]] = remaining
                neighbor[course_idx].shares = new_shares
        
        elif strategy == 'modify_team':
            if course.can_be_shared:
                current_size = len(neighbor[course_idx].professor_ids)
                
                if current_size == 1 and course.max_professors > 1:
                    # Add a professor
                    available_profs = [p for p in self.problem.professor_list 
                                     if p.id not in neighbor[course_idx].professor_ids]
                    if available_profs:
                        new_prof = random.choice(available_profs)
                        neighbor[course_idx].professor_ids.append(new_prof.id)
                        
                        # Equal shares
                        num_profs = len(neighbor[course_idx].professor_ids)
                        new_shares = {prof_id: 100.0 / num_profs 
                                    for prof_id in neighbor[course_idx].professor_ids}
                        neighbor[course_idx].shares = new_shares
                
                elif current_size > course.min_professors:
                    # Remove a professor
                    prof_to_remove = random.choice(neighbor[course_idx].professor_ids)
                    neighbor[course_idx].professor_ids.remove(prof_to_remove)
                    
                    # Redistribute shares
                    remaining_profs = neighbor[course_idx].professor_ids
                    if remaining_profs:
                        new_shares = {prof_id: 100.0 / len(remaining_profs) 
                                    for prof_id in remaining_profs}
                        neighbor[course_idx].shares = new_shares
        
        return neighbor
    
    def solve(self) -> Tuple[List[CourseAllocation], float]:
        """Solve the allocation problem using simulated annealing"""
        current_solution = self.generate_initial_solution()
        current_fitness = self.problem.calculate_fitness(current_solution)
        
        best_solution = copy.deepcopy(current_solution)
        best_fitness = current_fitness
        
        temperature = self.initial_temp
        
        for iteration in range(self.max_iterations):
            # Generate neighbor
            neighbor = self.generate_neighbor(current_solution)
            neighbor_fitness = self.problem.calculate_fitness(neighbor)
            
            # Calculate acceptance probability
            delta_e = neighbor_fitness - current_fitness
            
            if delta_e > 0 or random.random() < math.exp(delta_e / temperature):
                current_solution = neighbor
                current_fitness = neighbor_fitness
                
                # Update best solution
                if current_fitness > best_fitness:
                    best_solution = copy.deepcopy(current_solution)
                    best_fitness = current_fitness
            
            # Cool down
            temperature *= self.cooling_rate
            
            if temperature < self.min_temp:
                break
        
        return best_solution, best_fitness
    
    def generate_initial_solution(self) -> List[CourseAllocation]:
        """Generate initial feasible solution"""
        allocations = []
        
        # Track professor workloads
        professor_workloads = {prof_id: 0.0 for prof_id in self.problem.professors}
        
        # Allocate courses one by one
        for course_id, course in self.problem.courses.items():
            # Find suitable professors with available capacity
            suitable_professors = []
            for prof_id, prof in self.problem.professors.items():
                # Check expertise match
                if any(exp in prof.expertise for exp in course.required_expertise):
                    # Check capacity
                    current_load = professor_workloads[prof_id]
                    course_workload = course.total_workload_hours()
                    
                    if current_load + course_workload <= prof.max_teaching_load:
                        suitable_professors.append((prof_id, prof))
            
            if not suitable_professors:
                # Find any professor with capacity
                for prof_id, prof in self.problem.professors.items():
                    current_load = professor_workloads[prof_id]
                    course_workload = course.total_workload_hours()
                    
                    if current_load + course_workload <= prof.max_teaching_load:
                        suitable_professors.append((prof_id, prof))
                        break
            
            if suitable_professors:
                # Choose randomly from suitable professors
                chosen_prof_id, _ = random.choice(suitable_professors)
                
                # Create allocation
                allocation = CourseAllocation(
                    course_id=course.id,
                    professor_ids=[chosen_prof_id],
                    shares={chosen_prof_id: 100.0}
                )
                allocations.append(allocation)
                
                # Update workload
                professor_workloads[chosen_prof_id] += course.total_workload_hours()
            else:
                # Create allocation anyway (will be repaired)
                prof_id = random.choice(list(self.problem.professors.keys()))
                allocation = CourseAllocation(
                    course_id=course.id,
                    professor_ids=[prof_id],
                    shares={prof_id: 100.0}
                )
                allocations.append(allocation)
        
        return allocations
    
    def _ensure_all_professors_have_courses(self, allocations: List[CourseAllocation]):
        """Ensure every professor gets at least one course - more aggressive repair"""
        professors_with_courses = set()
        for allocation in allocations:
            professors_with_courses.update(allocation.professor_ids)
        
        # Find professors without courses
        professors_without_courses = set(self.problem.professors.keys()) - professors_with_courses
        
        for prof_id in professors_without_courses:
            professor = self.problem.professors[prof_id]
            added = False
            
            # Strategy 1: Try to add to existing courses that can be shared
            for allocation in allocations:
                course = self.problem.courses[allocation.course_id]
                if course.can_be_shared and len(allocation.professor_ids) < course.max_professors:
                    # Check if professor has any expertise match (even partial)
                    if any(exp in professor.expertise for exp in course.required_expertise):
                        # Add professor to this course with small share
                        allocation.professor_ids.append(prof_id)
                        allocation.shares[prof_id] = 10.0  # 10% share
                        
                        # Reduce other professors' shares proportionally
                        remaining_share = 90.0
                        num_others = len(allocation.professor_ids) - 1
                        if num_others > 0:
                            share_per_other = remaining_share / num_others
                            for other_prof in allocation.professor_ids[:-1]:  # All except the new one
                                allocation.shares[other_prof] = share_per_other
                        
                        added = True
                        break
            
            # Strategy 2: If no suitable shared course, find any course with available capacity
            if not added:
                for allocation in allocations:
                    course = self.problem.courses[allocation.course_id]
                    if course.can_be_shared and len(allocation.professor_ids) < course.max_professors:
                        # Force add professor even without expertise match
                        allocation.professor_ids.append(prof_id)
                        allocation.shares[prof_id] = 10.0  # 10% share
                        
                        # Reduce other professors' shares proportionally
                        remaining_share = 90.0
                        num_others = len(allocation.professor_ids) - 1
                        if num_others > 0:
                            share_per_other = remaining_share / num_others
                            for other_prof in allocation.professor_ids[:-1]:
                                allocation.shares[other_prof] = share_per_other
                        
                        added = True
                        break
            
            # Strategy 3: If still no course found, create a new allocation for a simple course
            if not added:
                # Find a simple course that can be taught by anyone
                for course_id, course in self.problem.courses.items():
                    if course.difficulty_level <= 2:  # Simple course
                        # Check if this course is already allocated
                        course_allocated = any(a.course_id == course_id for a in allocations)
                        if not course_allocated:
                            # Create new allocation
                            new_allocation = CourseAllocation(
                                course_id=course_id,
                                professor_ids=[prof_id],
                                shares={prof_id: 100.0}
                            )
                            allocations.append(new_allocation)
                            added = True
                            break
            
            # Strategy 4: Last resort - force add to any course
            if not added:
                # Find any course and force add professor
                for allocation in allocations:
                    course = self.problem.courses[allocation.course_id]
                    if course.can_be_shared and len(allocation.professor_ids) < course.max_professors:
                        allocation.professor_ids.append(prof_id)
                        allocation.shares[prof_id] = 5.0  # Very small share
                        
                        # Reduce other shares
                        remaining_share = 95.0
                        num_others = len(allocation.professor_ids) - 1
                        if num_others > 0:
                            share_per_other = remaining_share / num_others
                            for other_prof in allocation.professor_ids[:-1]:
                                allocation.shares[other_prof] = share_per_other
                        
                        added = True
                        break
