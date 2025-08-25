#!/usr/bin/env python3
"""
Main Runner for Workload Allocation System
Executes all three algorithms and generates comprehensive results
"""

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

from workload_allocator import (
    WorkloadAllocationProblem, HillClimbing, GeneticAlgorithm, SimulatedAnnealing
)
from data_adapter import load_dataset, create_test_dataset, create_problem, get_dataset_summary

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

class WorkloadAllocationRunner:
    """Main runner class for workload allocation experiments"""
    
    def __init__(self, use_test_dataset: bool = False):
        self.use_test_dataset = use_test_dataset
        self.professors = None
        self.courses = None
        self.problem = None
        self.results = {}
        self.execution_times = {}
        
    def load_data(self):
        """Load dataset (test or full)"""
        if self.use_test_dataset:
            print("🔄 Loading test dataset (20 professors, 15 courses)...")
            self.professors, self.courses = create_test_dataset()
        else:
            print("🔄 Loading full dataset (100 professors, 80 courses)...")
            self.professors, self.courses = load_dataset()
        
        self.problem = create_problem(self.professors, self.courses)
        
        # Print dataset summary
        summary = get_dataset_summary(self.professors, self.courses)
        print(f"✅ Dataset loaded successfully!")
        print(f"   📊 {summary['num_professors']} professors, {summary['num_courses']} courses")
        print(f"   🏢 {len(summary['departments'])} departments")
        print(f"   🎯 {len(summary['expertise_areas'])} expertise areas")
        print(f"   👥 Team teaching: {summary['team_teaching_capability']['can_be_shared']} courses can be shared")
    
    def run_hill_climbing(self) -> Tuple[List, float, float]:
        """Run Hill Climbing algorithm"""
        print("🧗 Running Hill Climbing algorithm...")
        start_time = time.time()
        
        # Use more iterations for full dataset
        max_iterations = 5000 if not self.use_test_dataset else 1000
        algorithm = HillClimbing(self.problem, max_iterations=max_iterations)
        
        solution, fitness = algorithm.solve()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️  Execution time: {execution_time:.2f} seconds")
        print(f"   🎯 Best fitness: {fitness:.4f}")
        
        return solution, fitness, execution_time
    
    def run_genetic_algorithm(self) -> Tuple[List, float, float]:
        """Run Genetic Algorithm"""
        print("🧬 Running Genetic Algorithm...")
        start_time = time.time()
        
        # Use larger population and more generations for full dataset
        if self.use_test_dataset:
            population_size = 50
            generations = 100
        else:
            population_size = 200
            generations = 500
        
        algorithm = GeneticAlgorithm(
            self.problem,
            population_size=population_size,
            generations=generations,
            mutation_rate=0.2,  # Higher mutation for exploration
            crossover_rate=0.8,
            elite_size=20
        )
        
        solution, fitness = algorithm.solve()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️  Execution time: {execution_time:.2f} seconds")
        print(f"   🎯 Best fitness: {fitness:.4f}")
        
        return solution, fitness, execution_time
    
    def run_simulated_annealing(self) -> Tuple[List, float, float]:
        """Run Simulated Annealing algorithm"""
        print("🔥 Running Simulated Annealing...")
        start_time = time.time()
        
        # Use more iterations and slower cooling for full dataset
        if self.use_test_dataset:
            max_iterations = 2000
            cooling_rate = 0.995
        else:
            max_iterations = 10000
            cooling_rate = 0.999  # Slower cooling
        
        algorithm = SimulatedAnnealing(
            self.problem,
            initial_temp=100.0,
            cooling_rate=cooling_rate,
            min_temp=0.1,
            max_iterations=max_iterations
        )
        
        solution, fitness = algorithm.solve()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️  Execution time: {execution_time:.2f} seconds")
        print(f"   🎯 Best fitness: {fitness:.4f}")
        
        return solution, fitness, execution_time
    
    def run_all_algorithms(self):
        """Run all three algorithms"""
        print("🚀 Starting Workload Allocation Experiment")
        print("=" * 60)
        
        # Load data
        self.load_data()
        
        # Run algorithms
        print("\n" + "=" * 60)
        print("🔬 ALGORITHM EXECUTION")
        print("=" * 60)
        
        # Hill Climbing
        hc_solution, hc_fitness, hc_time = self.run_hill_climbing()
        self.results['hill_climbing'] = (hc_solution, hc_fitness, hc_time)
        self.execution_times['hill_climbing'] = hc_time
        
        # Genetic Algorithm
        ga_solution, ga_fitness, ga_time = self.run_genetic_algorithm()
        self.results['genetic_algorithm'] = (ga_solution, ga_fitness, ga_time)
        self.execution_times['genetic_algorithm'] = ga_time
        
        # Simulated Annealing
        sa_solution, sa_fitness, sa_time = self.run_simulated_annealing()
        self.results['simulated_annealing'] = (sa_solution, sa_fitness, sa_time)
        self.execution_times['simulated_annealing'] = sa_time
        
        print("\n" + "=" * 60)
        print("✅ ALL ALGORITHMS COMPLETED")
        print("=" * 60)
    
    def generate_allocation_reports(self):
        """Generate detailed allocation reports for each algorithm"""
        print("\n📊 Generating allocation reports...")
        
        # Create results directory
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        for algo_name, (solution, fitness, execution_time) in self.results.items():
            print(f"   📝 Generating report for {algo_name.replace('_', ' ').title()}...")
            
            # Generate detailed allocation report
            report_df = self._create_allocation_report(solution, algo_name)
            report_filename = f"results/{algo_name}_allocation.csv"
            report_df.to_csv(report_filename, index=False)
            print(f"      💾 Saved: {report_filename}")
            
            # Generate professor workload summary
            summary_df = self._create_professor_summary(solution, algo_name)
            summary_filename = f"results/{algo_name}_professor_summary.csv"
            summary_df.to_csv(summary_filename, index=False)
            print(f"      💾 Saved: {summary_filename}")
    
    def _create_allocation_report(self, allocations: List, algo_name: str) -> pd.DataFrame:
        """Create detailed allocation report"""
        report_data = []
        
        for allocation in allocations:
            course = self.problem.courses[allocation.course_id]
            
            for prof_id in allocation.professor_ids:
                professor = self.problem.professors[prof_id]
                share = allocation.shares[prof_id]
                workload = allocation.get_professor_workload(prof_id, course)
                
                report_data.append({
                    'Algorithm': algo_name.replace('_', ' ').title(),
                    'Course_ID': course.id,
                    'Course_Name': course.name,
                    'Course_Code': course.code,
                    'Department': course.department,
                    'Difficulty_Level': course.difficulty_level,
                    'Num_Students': course.num_students,
                    'Professor_ID': prof_id,
                    'Professor_Name': professor.name,
                    'Professor_Title': professor.title,
                    'Professor_Department': professor.department,
                    'Share_Percentage': share,
                    'Workload_Hours': workload,
                    'Lecture_Hours': course.lecture_hours * (share / 100.0),
                    'Lab_Hours': course.lab_hours * (share / 100.0),
                    'Assessment_Hours': (course.assessment_hours / 15) * (share / 100.0),
                    'Prep_Hours': (course.lecture_hours * course.prep_factor) * (share / 100.0),
                    'Team_Teaching': len(allocation.professor_ids) > 1,
                    'Num_Professors': len(allocation.professor_ids)
                })
        
        return pd.DataFrame(report_data)
    
    def _create_professor_summary(self, allocations: List, algo_name: str) -> pd.DataFrame:
        """Create professor workload summary"""
        summary_data = []
        
        for prof_id in self.problem.professors:
            professor = self.problem.professors[prof_id]
            load_info = self.problem.calculate_professor_load(prof_id, allocations)
            
            # Get course assignments
            assigned_courses = []
            for allocation in allocations:
                if prof_id in allocation.professor_ids:
                    course = self.problem.courses[allocation.course_id]
                    share = allocation.shares[prof_id]
                    assigned_courses.append(f"{course.code} ({share:.1f}%)")
            
            summary_data.append({
                'Algorithm': algo_name.replace('_', ' ').title(),
                'Professor_ID': prof_id,
                'Professor_Name': professor.name,
                'Title': professor.title,
                'Department': professor.department,
                'Years_Experience': professor.years_experience,
                'Teaching_Hours': load_info['teaching_hours'],
                'Research_Hours': load_info['research_hours'],
                'Admin_Hours': load_info['admin_hours'],
                'Total_Hours': load_info['total_hours'],
                'Contracted_Hours': load_info['contracted_hours'],
                'Load_Percentage': load_info['load_percentage'],
                'Min_Teaching_Required': professor.min_teaching_load,
                'Max_Teaching_Allowed': professor.max_teaching_load,
                'Meets_Minimum': load_info['teaching_hours'] >= professor.min_teaching_load,
                'Within_Limits': load_info['teaching_hours'] <= professor.max_teaching_load,
                'Assigned_Courses': '; '.join(assigned_courses),
                'Num_Courses': len(assigned_courses)
            })
        
        return pd.DataFrame(summary_data)
    
    def generate_comparison_report(self):
        """Generate comprehensive algorithm comparison report"""
        print("\n📊 Generating Algorithm Comparison Report...")
        
        comparison_data = []
        
        for algo_name, (solution, fitness, execution_time) in self.results.items():
            # Calculate detailed metrics
            fairness_score = self.problem.calculate_fairness_score(solution)
            expertise_score = self.problem.calculate_expertise_score(solution)
            balance_score = self.problem.calculate_balance_score(solution)
            
            # Check constraints
            hard_constraints_satisfied = self.problem.check_hard_constraints(solution)
            soft_constraints = self.problem.check_soft_constraints(solution)
            
            # Calculate workload statistics
            workloads = []
            for prof_id in self.problem.professors:
                load = self.problem.calculate_professor_load(prof_id, solution)
                workloads.append(load['teaching_hours'])
            
            mean_workload = np.mean(workloads)
            std_workload = np.std(workloads)
            min_workload = np.min(workloads)
            max_workload = np.max(workloads)
            cv_workload = std_workload / mean_workload if mean_workload > 0 else 0
            
            comparison_data.append({
                'Algorithm': algo_name,
                'Fitness_Score': fitness,
                'Execution_Time_Seconds': execution_time,
                'Fairness_Score': fairness_score,
                'Expertise_Score': expertise_score,
                'Balance_Score': balance_score,
                'Hard_Constraints_Satisfied': hard_constraints_satisfied,
                'Workload_Limits_Satisfied': soft_constraints['workload_limits'],
                'Expertise_Matching_Satisfied': soft_constraints['expertise_matching'],
                'Fairness_Satisfied': soft_constraints['fairness'],
                'Mean_Workload': mean_workload,
                'Std_Workload': std_workload,
                'Min_Workload': min_workload,
                'Max_Workload': max_workload,
                'Coefficient_of_Variation': cv_workload
            })
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame(comparison_data)
        
        # Save to CSV
        output_file = "results/algorithm_comparison.csv"
        comparison_df.to_csv(output_file, index=False)
        
        print(f"✅ Comparison report saved to {output_file}")
        
        # Display summary
        print("\n" + "="*80)
        print("ALGORITHM COMPARISON SUMMARY")
        print("="*80)
        
        for _, row in comparison_df.iterrows():
            print(f"\n{row['Algorithm']}:")
            print(f"  🎯 Fitness Score: {row['Fitness_Score']:.4f}")
            print(f"  ⏱️  Execution Time: {row['Execution_Time_Seconds']:.2f}s")
            print(f"  ✅ Hard Constraints: {'Satisfied' if row['Hard_Constraints_Satisfied'] else 'Violated'}")
            print(f"  📚 Workload Limits: {'Respected' if row['Workload_Limits_Satisfied'] else 'Exceeded'}")
            print(f"  🎓 Expertise Matching: {'Good' if row['Expertise_Matching_Satisfied'] else 'Poor'}")
            print(f"  ⚖️  Fairness: {'Good' if row['Fairness_Satisfied'] else 'Poor'}")
            print(f"  📊 Workload: {row['Mean_Workload']:.1f}±{row['Std_Workload']:.1f} hours")
        
        return comparison_df
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n🎨 Creating visualizations...")
        
        # Create results directory
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        # 1. Algorithm Performance Comparison
        self._create_performance_comparison()
        
        # 2. Workload Distribution Comparison
        self._create_workload_distribution_comparison()
        
        # 3. Fitness Score Comparison
        self._create_fitness_comparison()
        
        # 4. Execution Time Comparison
        self._create_execution_time_comparison()
        
        # 5. Fairness Analysis
        self._create_fairness_analysis()
        
        print("   🎨 All visualizations created successfully!")
    
    def _create_performance_comparison(self):
        """Create algorithm performance comparison chart"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Algorithm Performance Comparison', fontsize=16, fontweight='bold')
        
        # Fitness scores
        algo_names = [name.replace('_', ' ').title() for name in self.results.keys()]
        fitness_scores = [result[1] for result in self.results.values()]
        
        axes[0, 0].bar(algo_names, fitness_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[0, 0].set_title('Fitness Scores')
        axes[0, 0].set_ylabel('Fitness Score')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Execution times
        execution_times = [result[2] for result in self.results.values()]
        axes[0, 1].bar(algo_names, execution_times, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[0, 1].set_title('Execution Times')
        axes[0, 1].set_ylabel('Time (seconds)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Fairness scores
        fairness_scores = [self.problem.calculate_fairness_score(result[0]) 
                          for result in self.results.values()]
        axes[1, 0].bar(algo_names, fairness_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[1, 0].set_title('Fairness Scores')
        axes[1, 0].set_ylabel('Fairness Score')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Expertise scores
        expertise_scores = [self.problem.calculate_expertise_score(result[0]) 
                           for result in self.results.values()]
        axes[1, 1].bar(algo_names, expertise_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[1, 1].set_title('Expertise Matching Scores')
        axes[1, 1].set_ylabel('Expertise Score')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('results/algorithm_performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_workload_distribution_comparison(self):
        """Create workload distribution comparison"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Workload Distribution Comparison Across Algorithms', fontsize=16, fontweight='bold')
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for i, (algo_name, result) in enumerate(self.results.items()):
            solution, fitness, execution_time = result
            allocations = solution
            workloads = []
            
            for prof_id in self.problem.professors:
                load_info = self.problem.calculate_professor_load(prof_id, allocations)
                workloads.append(load_info['teaching_hours'])
            
            axes[i].hist(workloads, bins=20, alpha=0.7, color=colors[i], edgecolor='black')
            axes[i].set_title(f'{algo_name.replace("_", " ").title()}')
            axes[i].set_xlabel('Teaching Hours')
            axes[i].set_ylabel('Number of Professors')
            axes[i].axvline(np.mean(workloads), color='red', linestyle='--', 
                           label=f'Mean: {np.mean(workloads):.1f}')
            axes[i].legend()
        
        plt.tight_layout()
        plt.savefig('results/workload_distribution_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_fitness_comparison(self):
        """Create fitness score comparison"""
        plt.figure(figsize=(10, 6))
        
        algo_names = [name.replace('_', ' ').title() for name in self.results.keys()]
        fitness_scores = [result[1] for result in self.results.values()]
        
        bars = plt.bar(algo_names, fitness_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('Algorithm Fitness Score Comparison', fontsize=14, fontweight='bold')
        plt.ylabel('Fitness Score')
        plt.xlabel('Algorithm')
        
        # Add value labels on bars
        for bar, score in zip(bars, fitness_scores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{score:.4f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/fitness_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_execution_time_comparison(self):
        """Create execution time comparison"""
        plt.figure(figsize=(10, 6))
        
        algo_names = [name.replace('_', ' ').title() for name in self.results.keys()]
        execution_times = [result[2] for result in self.results.values()]
        
        bars = plt.bar(algo_names, execution_times, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('Algorithm Execution Time Comparison', fontsize=14, fontweight='bold')
        plt.ylabel('Execution Time (seconds)')
        plt.xlabel('Algorithm')
        
        # Add value labels on bars
        for bar, time_val in zip(bars, execution_times):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{time_val:.2f}s', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/execution_time_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_fairness_analysis(self):
        """Create fairness analysis visualization"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Fairness Analysis Across Algorithms', fontsize=16, fontweight='bold')
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for i, (algo_name, result) in enumerate(self.results.items()):
            solution, fitness, execution_time = result
            allocations = solution
            
            # Calculate workload percentages
            workload_percentages = []
            for prof_id in self.problem.professors:
                load_info = self.problem.calculate_professor_load(prof_id, allocations)
                workload_percentages.append(load_info['load_percentage'])
            
            # Sort for better visualization
            workload_percentages.sort()
            
            axes[i].plot(range(len(workload_percentages)), workload_percentages, 
                        marker='o', color=colors[i], linewidth=2, markersize=4)
            axes[i].set_title(f'{algo_name.replace("_", " ").title()}')
            axes[i].set_xlabel('Professor Rank (by workload)')
            axes[i].set_ylabel('Workload Percentage')
            axes[i].grid(True, alpha=0.3)
            
            # Add ideal line (perfect fairness)
            mean_percentage = np.mean(workload_percentages)
            axes[i].axhline(y=mean_percentage, color='red', linestyle='--', alpha=0.7,
                           label=f'Mean: {mean_percentage:.1f}%')
            axes[i].legend()
        
        plt.tight_layout()
        plt.savefig('results/fairness_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def print_summary(self):
        """Print comprehensive summary of results"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE RESULTS SUMMARY")
        print("=" * 80)
        
        # Algorithm comparison
        comparison_df = self.generate_comparison_report()
        
        print("\n🏆 ALGORITHM RANKINGS:")
        print("-" * 50)
        
        # Sort by fitness score
        sorted_results = sorted(self.results.items(), 
                              key=lambda x: x[1][1], reverse=True)
        
        for i, (algo_name, result) in enumerate(sorted_results):
            rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            print(f"{rank} {algo_name.replace('_', ' ').title()}")
            print(f"   Fitness Score: {result[1]:.4f}")
            print(f"   Execution Time: {result[2]:.2f} seconds")
            print(f"   Fairness Score: {self.problem.calculate_fairness_score(result[0]):.4f}")
            print()
        
        print("\n📈 KEY METRICS:")
        print("-" * 50)
        print(f"Dataset Size: {len(self.professors)} professors, {len(self.courses)} courses")
        print(f"Best Fitness: {sorted_results[0][1][1]:.4f}")
        print(f"Fastest Algorithm: {min(self.execution_times.items(), key=lambda x: x[1])[0].replace('_', ' ').title()}")
        print(f"Most Fair: {max(self.results.items(), key=lambda x: self.problem.calculate_fairness_score(x[1][0]))[0].replace('_', ' ').title()}")
        
        print("\n💾 OUTPUT FILES:")
        print("-" * 50)
        print("📁 Results directory contains:")
        print("   • Individual algorithm allocation reports (CSV)")
        print("   • Professor workload summaries (CSV)")
        print("   • Algorithm comparison report (CSV)")
        print("   • Comprehensive visualizations (PNG)")
        
        print("\n🎯 RECOMMENDATIONS:")
        print("-" * 50)
        best_algo = sorted_results[0][0]
        print(f"• Best Overall: {best_algo.replace('_', ' ').title()}")
        print(f"• For Speed: {min(self.execution_times.items(), key=lambda x: x[1])[0].replace('_', ' ').title()}")
        print(f"• For Fairness: {max(self.results.items(), key=lambda x: self.problem.calculate_fairness_score(x[1][0]))[0].replace('_', ' ').title()}")
        
        print("\n" + "=" * 80)

def main():
    """Main execution function"""
    print("🎓 Faculty Workload Allocation System")
    print("🔬 Comprehensive Algorithm Comparison")
    print("=" * 60)
    
    # Ask user for dataset choice
    print("\nChoose dataset:")
    print("1. Test dataset (20 professors, 15 courses) - Fast testing")
    print("2. Full dataset (100 professors, 80 courses) - Complete analysis")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    use_test_dataset = choice == "1"
    
    # Create and run the system
    runner = WorkloadAllocationRunner(use_test_dataset=use_test_dataset)
    
    try:
        # Run all algorithms
        runner.run_all_algorithms()
        
        # Generate reports
        runner.generate_allocation_reports()
        
        # Create visualizations
        runner.create_visualizations()
        
        # Print summary
        runner.print_summary()
        
        print("\n🎉 Workload allocation experiment completed successfully!")
        print("📁 Check the 'results' directory for all output files.")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
