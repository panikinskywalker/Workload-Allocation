#!/usr/bin/env python3
"""
Advanced Visualizations for Faculty Workload Allocation System
Creates specialized plots for academic paper analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

class AdvancedVisualizations:
    def __init__(self):
        self.professors_df = None
        self.courses_df = None
        self.output_dir = "results/advanced_visualizations"
        
    def load_data(self):
        """Load the dataset files"""
        print("📊 Loading dataset for advanced visualizations...")
        
        # Load professors data
        self.professors_df = pd.read_csv('data/professors.csv')
        
        # Load courses data  
        self.courses_df = pd.read_csv('data/courses.csv')
        
        print(f"✅ Loaded {len(self.professors_df)} professors and {len(self.courses_df)} courses")
        
    def create_output_directory(self):
        """Create output directory for visualizations"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_correlation_analysis(self):
        """Create correlation analysis between key variables"""
        print("\n🔗 Creating Correlation Analysis...")
        
        # Select numeric columns for correlation
        prof_numeric = self.professors_df.select_dtypes(include=[np.number])
        course_numeric = self.courses_df.select_dtypes(include=[np.number])
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Correlation Analysis - Faculty Workload Allocation System', fontsize=20, fontweight='bold')
        
        # 1. Professor correlations
        prof_corr = prof_numeric.corr()
        mask = np.triu(np.ones_like(prof_corr, dtype=bool))
        sns.heatmap(prof_corr, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=axes[0,0])
        axes[0,0].set_title('Professor Variables Correlation Matrix', fontweight='bold')
        
        # 2. Course correlations
        course_corr = course_numeric.corr()
        mask = np.triu(np.ones_like(course_corr, dtype=bool))
        sns.heatmap(course_corr, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=axes[0,1])
        axes[0,1].set_title('Course Variables Correlation Matrix', fontweight='bold')
        
        # 3. Key professor correlations
        key_prof_vars = ['years_experience', 'research_allocation', 'admin_load', 
                         'max_teaching_load', 'min_teaching_load', 'teaching_quality']
        key_prof_corr = self.professors_df[key_prof_vars].corr()
        mask = np.triu(np.ones_like(key_prof_corr, dtype=bool))
        sns.heatmap(key_prof_corr, mask=mask, annot=True, cmap='RdBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=axes[1,0])
        axes[1,0].set_title('Key Professor Variables Correlation', fontweight='bold')
        
        # 4. Key course correlations
        key_course_vars = ['difficulty_level', 'num_students', 'lecture_hours', 
                          'lab_hours', 'assessment_hours', 'prep_factor']
        key_course_corr = self.courses_df[key_course_vars].corr()
        mask = np.triu(np.ones_like(key_course_corr, dtype=bool))
        sns.heatmap(key_course_corr, mask=mask, annot=True, cmap='RdBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=axes[1,1])
        axes[1,1].set_title('Key Course Variables Correlation', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/correlation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/correlation_analysis.png")
        
    def create_constraint_analysis(self):
        """Create detailed constraint analysis visualizations"""
        print("\n⚖️ Creating Constraint Analysis...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Constraint Analysis - Workload Allocation Problem', fontsize=20, fontweight='bold')
        
        # 1. Teaching load feasibility analysis
        min_load = self.professors_df['min_teaching_load']
        max_load = self.professors_df['max_teaching_load']
        flexibility = max_load - min_load
        
        axes[0,0].scatter(min_load, max_load, alpha=0.6, c=flexibility, cmap='viridis', s=60)
        axes[0,0].plot([min_load.min(), max_load.max()], [min_load.min(), max_load.max()], 'r--', alpha=0.7)
        axes[0,0].set_title('Teaching Load Constraints: Min vs Max', fontweight='bold')
        axes[0,0].set_xlabel('Minimum Teaching Load (hours/week)')
        axes[0,0].set_ylabel('Maximum Teaching Load (hours/week)')
        cbar = plt.colorbar(axes[0,0].collections[0], ax=axes[0,0])
        cbar.set_label('Flexibility (hours/week)')
        
        # 2. Constraint satisfaction probability
        # Calculate how many courses each professor can potentially teach
        course_workloads = []
        for _, course in self.courses_df.iterrows():
            total_workload = (course['lecture_hours'] + course['lab_hours']) * course['prep_factor'] + course['assessment_hours']
            course_workloads.append(total_workload)
        
        course_workloads = np.array(course_workloads)
        feasible_professors = []
        
        for _, prof in self.professors_df.iterrows():
            feasible_courses = np.sum(course_workloads <= prof['max_teaching_load'])
            feasible_professors.append(feasible_courses)
        
        axes[0,1].hist(feasible_professors, bins=20, color='lightcoral', edgecolor='darkred', alpha=0.7)
        axes[0,1].set_title('Distribution of Feasible Course Assignments per Professor', fontweight='bold')
        axes[0,1].set_xlabel('Number of Feasible Courses')
        axes[0,1].set_ylabel('Number of Professors')
        axes[0,1].axvline(np.mean(feasible_professors), color='red', linestyle='--',
                          label=f'Mean: {np.mean(feasible_professors):.1f}')
        axes[0,1].legend()
        
        # 3. Workload balance analysis
        contracted_hours = 40
        research_hours = contracted_hours * self.professors_df['research_allocation']
        admin_hours = self.professors_df['admin_load']
        available_teaching = contracted_hours - research_hours - admin_hours
        
        axes[1,0].scatter(available_teaching, self.professors_df['max_teaching_load'], alpha=0.6, color='lightgreen', s=50)
        axes[1,0].plot([available_teaching.min(), available_teaching.max()], 
                       [available_teaching.min(), available_teaching.max()], 'r--', alpha=0.7)
        axes[1,0].set_title('Available vs Maximum Teaching Hours', fontweight='bold')
        axes[1,0].set_xlabel('Available Teaching Hours (40 - research - admin)')
        axes[1,0].set_ylabel('Maximum Teaching Load')
        
        # 4. Constraint violation risk
        violation_risk = []
        for _, prof in self.professors_df.iterrows():
            # Risk based on how close min and max are, and how close max is to available hours
            risk = (prof['max_teaching_load'] - prof['min_teaching_load']) / prof['max_teaching_load']
            violation_risk.append(risk)
        
        axes[1,1].hist(violation_risk, bins=20, color='gold', edgecolor='orange', alpha=0.7)
        axes[1,1].set_title('Distribution of Constraint Violation Risk', fontweight='bold')
        axes[1,1].set_xlabel('Risk Factor (Lower = Higher Risk)')
        axes[1,1].set_ylabel('Number of Professors')
        axes[1,1].axvline(np.mean(violation_risk), color='red', linestyle='--',
                          label=f'Mean: {np.mean(violation_risk):.3f}')
        axes[1,1].legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/constraint_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/constraint_analysis.png")
        
    def create_problem_complexity_visualizations(self):
        """Create problem complexity and search space analysis"""
        print("\n🧮 Creating Problem Complexity Analysis...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Problem Complexity and Search Space Analysis', fontsize=20, fontweight='bold')
        
        # 1. Search space complexity by department
        dept_complexity = {}
        for dept in self.professors_df['department'].unique():
            prof_count = len(self.professors_df[self.professors_df['department'] == dept])
            course_count = len(self.courses_df[self.courses_df['department'] == dept])
            if course_count > 0:
                # Rough estimate of search space size
                complexity = prof_count ** course_count
                dept_complexity[dept] = np.log10(complexity)  # Log scale for readability
        
        dept_complexity_df = pd.DataFrame(list(dept_complexity.items()), columns=['Department', 'Log Complexity'])
        dept_complexity_df = dept_complexity_df.sort_values('Log Complexity', ascending=True)
        
        axes[0,0].barh(dept_complexity_df['Department'], dept_complexity_df['Log Complexity'], 
                       color='lightblue', edgecolor='navy')
        axes[0,0].set_title('Search Space Complexity by Department (Log Scale)', fontweight='bold')
        axes[0,0].set_xlabel('Log10(Search Space Size)')
        axes[0,0].set_ylabel('Department')
        
        # 2. Course difficulty distribution by department
        dept_difficulty = self.courses_df.groupby('department')['difficulty_level'].agg(['mean', 'std', 'count'])
        dept_difficulty = dept_difficulty.sort_values('mean', ascending=True)
        
        axes[0,1].barh(dept_difficulty.index, dept_difficulty['mean'], 
                       yerr=dept_difficulty['std'], color='lightcoral', edgecolor='darkred', alpha=0.7)
        axes[0,1].set_title('Average Course Difficulty by Department', fontweight='bold')
        axes[0,1].set_xlabel('Average Difficulty Level')
        axes[0,1].set_ylabel('Department')
        
        # 3. Workload distribution complexity
        # Calculate total workload for each course
        self.courses_df['total_workload'] = (self.courses_df['lecture_hours'] + self.courses_df['lab_hours']) * \
                                           self.courses_df['prep_factor'] + self.courses_df['assessment_hours']
        
        workload_bins = pd.cut(self.courses_df['total_workload'], bins=10)
        workload_dist = workload_bins.value_counts().sort_index()
        
        axes[1,0].bar(range(len(workload_dist)), workload_dist.values, color='lightgreen', edgecolor='darkgreen')
        axes[1,0].set_title('Course Workload Distribution', fontweight='bold')
        axes[1,0].set_xlabel('Workload Range')
        axes[1,0].set_ylabel('Number of Courses')
        axes[1,0].set_xticks(range(len(workload_dist)))
        axes[1,0].set_xticklabels([f'{int(interval.left)}-{int(interval.right)}' for interval in workload_dist.index], rotation=45)
        
        # 4. Constraint satisfaction matrix
        # Create a heatmap showing how many professors can teach each course
        course_prof_matrix = np.zeros((len(self.courses_df), len(self.professors_df)))
        
        for i, course in self.courses_df.iterrows():
            course_workload = course['total_workload']
            for j, prof in self.professors_df.iterrows():
                if course_workload <= prof['max_teaching_load']:
                    course_prof_matrix[i, j] = 1
        
        # Sample a subset for visualization (every 10th course and professor)
        sample_matrix = course_prof_matrix[::10, ::10]
        
        im = axes[1,1].imshow(sample_matrix, cmap='RdYlGn', aspect='auto')
        axes[1,1].set_title('Course-Professor Feasibility Matrix (Sampled)', fontweight='bold')
        axes[1,1].set_xlabel('Professors (sampled)')
        axes[1,1].set_ylabel('Courses (sampled)')
        cbar = plt.colorbar(im, ax=axes[1,1])
        cbar.set_label('Feasible Assignment (1=Yes, 0=No)')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/problem_complexity.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/problem_complexity.png")
        
    def create_statistical_analysis(self):
        """Create statistical analysis and distribution plots"""
        print("\n📊 Creating Statistical Analysis...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Statistical Analysis and Distribution Plots', fontsize=20, fontweight='bold')
        
        # 1. Normal distribution test for key variables
        # Years of experience
        experience = self.professors_df['years_experience']
        axes[0,0].hist(experience, bins=20, density=True, alpha=0.7, color='lightblue', edgecolor='navy')
        
        # Fit normal distribution
        mu, sigma = stats.norm.fit(experience)
        x = np.linspace(experience.min(), experience.max(), 100)
        y = stats.norm.pdf(x, mu, sigma)
        axes[0,0].plot(x, y, 'r-', linewidth=2, label=f'Normal fit (μ={mu:.1f}, σ={sigma:.1f})')
        
        axes[0,0].set_title('Years of Experience Distribution with Normal Fit', fontweight='bold')
        axes[0,0].set_xlabel('Years of Experience')
        axes[0,0].set_ylabel('Density')
        axes[0,0].legend()
        
        # 2. Box plots for teaching loads by experience groups
        experience_groups = pd.cut(self.professors_df['years_experience'], bins=5, labels=['1-5', '6-10', '11-15', '16-20', '21-25'])
        self.professors_df['experience_group'] = experience_groups
        
        box_data = [self.professors_df[self.professors_df['experience_group'] == group]['max_teaching_load'].values 
                   for group in ['1-5', '6-10', '11-15', '16-20', '21-25']]
        
        axes[0,1].boxplot(box_data, labels=['1-5', '6-10', '11-15', '16-20', '21-25'])
        axes[0,1].set_title('Teaching Load Distribution by Experience Groups', fontweight='bold')
        axes[0,1].set_xlabel('Experience Group (years)')
        axes[0,1].set_ylabel('Maximum Teaching Load (hours/week)')
        
        # 3. Q-Q plot for teaching quality
        stats.probplot(self.professors_df['teaching_quality'], dist="norm", plot=axes[1,0])
        axes[1,0].set_title('Q-Q Plot: Teaching Quality vs Normal Distribution', fontweight='bold')
        
        # 4. Violin plot for course difficulty vs student enrollment
        difficulty_groups = pd.cut(self.courses_df['difficulty_level'], bins=5, labels=['1-1.8', '1.8-2.6', '2.6-3.4', '3.4-4.2', '4.2-5'])
        self.courses_df['difficulty_group'] = difficulty_groups
        
        violin_data = [self.courses_df[self.courses_df['difficulty_group'] == group]['num_students'].values 
                      for group in ['1-1.8', '1.8-2.6', '2.6-3.4', '3.4-4.2', '4.2-5']]
        
        axes[1,1].violinplot(violin_data, positions=range(1, 6))
        axes[1,1].set_title('Student Enrollment Distribution by Difficulty Level', fontweight='bold')
        axes[1,1].set_xlabel('Difficulty Level Group')
        axes[1,1].set_ylabel('Number of Students')
        axes[1,1].set_xticks(range(1, 6))
        axes[1,1].set_xticklabels(['1-1.8', '1.8-2.6', '2.6-3.4', '3.4-4.2', '4.2-5'])
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/statistical_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/statistical_analysis.png")
        
    def create_summary_report(self):
        """Create a comprehensive summary report"""
        print("\n📋 Creating Summary Report...")
        
        # Calculate key metrics
        total_professors = len(self.professors_df)
        total_courses = len(self.courses_df)
        total_departments = self.professors_df['department'].nunique()
        
        # Calculate search space size
        search_space_size = total_professors ** total_courses
        
        # Calculate constraint satisfaction metrics
        feasible_assignments = 0
        for _, course in self.courses_df.iterrows():
            course_workload = (course['lecture_hours'] + course['lab_hours']) * course['prep_factor'] + course['assessment_hours']
            for _, prof in self.professors_df.iterrows():
                if course_workload <= prof['max_teaching_load']:
                    feasible_assignments += 1
        
        feasibility_rate = feasible_assignments / (total_courses * total_professors) * 100
        
        # Create summary report
        summary_report = f"""
# FACULTY WORKLOAD ALLOCATION SYSTEM - DATASET ANALYSIS SUMMARY

## 📊 DATASET OVERVIEW
- **Total Professors**: {total_professors}
- **Total Courses**: {total_courses}
- **Total Departments**: {total_departments}
- **Professor-to-Course Ratio**: {total_professors/total_courses:.2f}:1

## 🧮 PROBLEM COMPLEXITY
- **Search Space Size**: {search_space_size:.2e} possible allocations
        - **Log10(Search Space)**: {np.log10(float(search_space_size)):.2f}
- **Feasibility Rate**: {feasibility_rate:.1f}% of potential assignments are feasible

## ⚖️ CONSTRAINT ANALYSIS
- **Average Min Teaching Load**: {self.professors_df['min_teaching_load'].mean():.1f} hours/week
- **Average Max Teaching Load**: {self.professors_df['max_teaching_load'].mean():.1f} hours/week
- **Average Teaching Load Flexibility**: {(self.professors_df['max_teaching_load'] - self.professors_df['min_teaching_load']).mean():.1f} hours/week
- **Average Research Allocation**: {self.professors_df['research_allocation'].mean():.3f} (fraction of 40 hours)
- **Average Administrative Load**: {self.professors_df['admin_load'].mean():.1f} hours/week

## 📚 COURSE CHARACTERISTICS
- **Difficulty Levels**: {self.courses_df['difficulty_level'].min()}-{self.courses_df['difficulty_level'].max()}
- **Average Student Enrollment**: {self.courses_df['num_students'].mean():.0f} students
- **Team Teaching Support**: {self.courses_df['can_be_shared'].mean()*100:.1f}% of courses
- **Average Course Workload**: {self.courses_df['total_workload'].mean():.1f} hours

## 🎯 KEY INSIGHTS
1. **High Complexity**: The search space is extremely large ({search_space_size:.2e} possibilities)
2. **Moderate Feasibility**: {feasibility_rate:.1f}% of potential assignments satisfy constraints
3. **Balanced Workload**: Professors have reasonable flexibility in teaching load ({(self.professors_df['max_teaching_load'] - self.professors_df['min_teaching_load']).mean():.1f} hours)
4. **Team Teaching**: {self.courses_df['can_be_shared'].sum()}/{len(self.courses_df)} courses support multiple professors
5. **Realistic Constraints**: Workload limits are realistic for academic environments

## 🚀 IMPLICATIONS FOR ALGORITHMS
- **Hill Climbing**: May struggle with local optima due to large search space
- **Genetic Algorithm**: Population-based approach beneficial for exploring diverse solutions
- **Simulated Annealing**: Temperature-based acceptance helpful for escaping local optima
- **Constraint Satisfaction**: All algorithms must handle {100-feasibility_rate:.1f}% infeasible assignments

## 📁 GENERATED VISUALIZATIONS
- Department Analysis
- Expertise Analysis  
- Course Analysis
- Workload Analysis
- Complexity Analysis
- Correlation Analysis
- Constraint Analysis
- Problem Complexity
- Statistical Analysis

This dataset represents a realistic, complex academic workload allocation problem suitable for testing metaheuristic algorithms.
"""
        
        # Save summary report
        with open(f'{self.output_dir}/dataset_summary_report.md', 'w') as f:
            f.write(summary_report)
        
        print(f"   💾 Saved: {self.output_dir}/dataset_summary_report.md")
        
        # Print key insights
        print("\n" + "="*60)
        print("🔍 KEY DATASET INSIGHTS")
        print("="*60)
        print(f"   🧮 Search Space Size: {search_space_size:.2e} possible allocations")
        print(f"   ⚖️  Feasibility Rate: {feasibility_rate:.1f}% of assignments are feasible")
        print(f"   🎯 Problem Complexity: Extremely high (log10 = {np.log10(float(search_space_size)):.2f})")
        print(f"   🤝 Team Teaching: {self.courses_df['can_be_shared'].sum()}/{len(self.courses_df)} courses")
        print(f"   📚 Workload Balance: {(self.professors_df['max_teaching_load'] - self.professors_df['min_teaching_load']).mean():.1f} hours flexibility")
        
    def run_advanced_visualizations(self):
        """Run all advanced visualizations"""
        print("🚀 Starting Advanced Visualization Generation...")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Create output directory
        self.create_output_directory()
        
        # Generate visualizations
        self.create_correlation_analysis()
        self.create_constraint_analysis()
        self.create_problem_complexity_visualizations()
        self.create_statistical_analysis()
        
        # Generate summary report
        self.create_summary_report()
        
        print("\n" + "="*60)
        print("🎉 ADVANCED VISUALIZATIONS COMPLETED!")
        print("="*60)
        print(f"📁 All visualizations saved to: {self.output_dir}/")
        print("📊 Statistical analysis completed")
        print("🔍 Problem complexity analyzed")
        print("📋 Summary report generated")
        print("\nReady for comprehensive academic paper analysis! 🎓")

if __name__ == "__main__":
    adv_viz = AdvancedVisualizations()
    adv_viz.run_advanced_visualizations()
