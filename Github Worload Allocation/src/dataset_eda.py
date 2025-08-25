#!/usr/bin/env python3
"""
Comprehensive Exploratory Data Analysis (EDA) for Faculty Workload Allocation System
Generates detailed visualizations and insights for the academic paper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

class DatasetEDA:
    def __init__(self):
        self.professors_df = None
        self.courses_df = None
        self.output_dir = "results/eda_visualizations"
        
    def load_data(self):
        """Load the dataset files"""
        print("📊 Loading dataset for EDA...")
        
        # Load professors data
        self.professors_df = pd.read_csv('data/professors.csv')
        
        # Load courses data  
        self.courses_df = pd.read_csv('data/courses.csv')
        
        print(f"✅ Loaded {len(self.professors_df)} professors and {len(self.courses_df)} courses")
        
    def create_output_directory(self):
        """Create output directory for visualizations"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
    def analyze_professors(self):
        """Analyze professors dataset characteristics"""
        print("\n👨‍🏫 Analyzing Professors Dataset...")
        
        # Basic statistics
        print(f"   📊 Total Professors: {len(self.professors_df)}")
        print(f"   🏢 Departments: {self.professors_df['department'].nunique()}")
        print(f"   🎯 Expertise Areas: {self.professors_df['expertise'].nunique()}")
        
        # Experience distribution
        print(f"   📈 Experience Range: {self.professors_df['years_experience'].min()}-{self.professors_df['years_experience'].max()} years")
        print(f"   ⚖️  Average Experience: {self.professors_df['years_experience'].mean():.1f} years")
        
        # Workload constraints
        print(f"   📚 Teaching Load Range: {self.professors_df['min_teaching_load'].min():.1f}-{self.professors_df['max_teaching_load'].max():.1f} hours")
        
    def analyze_courses(self):
        """Analyze courses dataset characteristics"""
        print("\n📚 Analyzing Courses Dataset...")
        
        # Basic statistics
        print(f"   📊 Total Courses: {len(self.courses_df)}")
        print(f"   🏢 Departments: {self.courses_df['department'].nunique()}")
        print(f"   🎯 Difficulty Levels: {self.courses_df['difficulty_level'].min()}-{self.courses_df['difficulty_level'].max()}")
        
        # Student enrollment
        print(f"   👥 Student Range: {self.courses_df['num_students'].min()}-{self.courses_df['num_students'].max()}")
        print(f"   📈 Average Enrollment: {self.courses_df['num_students'].mean():.0f} students")
        
        # Team teaching capability
        team_teaching = self.courses_df['can_be_shared'].sum()
        print(f"   🤝 Team Teaching Courses: {team_teaching}/{len(self.courses_df)} ({team_teaching/len(self.courses_df)*100:.1f}%)")
        
    def create_department_analysis(self):
        """Create comprehensive department analysis visualizations"""
        print("\n🏢 Creating Department Analysis Visualizations...")
        
        # Department distribution
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Department Analysis - Faculty Workload Allocation System', fontsize=20, fontweight='bold')
        
        # 1. Professor distribution by department
        dept_counts = self.professors_df['department'].value_counts()
        axes[0,0].barh(dept_counts.index, dept_counts.values, color='skyblue', edgecolor='navy')
        axes[0,0].set_title('Professor Distribution by Department', fontweight='bold')
        axes[0,0].set_xlabel('Number of Professors')
        axes[0,0].set_ylabel('Department')
        
        # 2. Course distribution by department
        course_dept_counts = self.courses_df['department'].value_counts()
        axes[0,1].barh(course_dept_counts.index, course_dept_counts.values, color='lightcoral', edgecolor='darkred')
        axes[0,1].set_title('Course Distribution by Department', fontweight='bold')
        axes[0,1].set_xlabel('Number of Courses')
        axes[0,1].set_ylabel('Department')
        
        # 3. Professor-to-course ratio by department
        prof_course_ratio = {}
        for dept in dept_counts.index:
            prof_count = dept_counts[dept]
            course_count = course_dept_counts.get(dept, 0)
            ratio = prof_count / max(course_count, 1)  # Avoid division by zero
            prof_course_ratio[dept] = ratio
        
        ratio_df = pd.DataFrame(list(prof_course_ratio.items()), columns=['Department', 'Ratio'])
        ratio_df = ratio_df.sort_values('Ratio', ascending=True)
        
        axes[1,0].barh(ratio_df['Department'], ratio_df['Ratio'], color='lightgreen', edgecolor='darkgreen')
        axes[1,0].set_title('Professor-to-Course Ratio by Department', fontweight='bold')
        axes[1,0].set_xlabel('Professors per Course')
        axes[1,0].set_ylabel('Department')
        axes[1,0].axvline(x=1, color='red', linestyle='--', alpha=0.7, label='1:1 Ratio')
        axes[1,0].legend()
        
        # 4. Department workload capacity
        dept_capacity = {}
        for dept in dept_counts.index:
            dept_profs = self.professors_df[self.professors_df['department'] == dept]
            total_capacity = dept_profs['max_teaching_load'].sum()
            dept_capacity[dept] = total_capacity
        
        capacity_df = pd.DataFrame(list(dept_capacity.items()), columns=['Department', 'Total Capacity'])
        capacity_df = capacity_df.sort_values('Total Capacity', ascending=True)
        
        axes[1,1].barh(capacity_df['Department'], capacity_df['Total Capacity'], color='gold', edgecolor='orange')
        axes[1,1].set_title('Total Teaching Capacity by Department', fontweight='bold')
        axes[1,1].set_xlabel('Total Teaching Hours Available')
        axes[1,1].set_ylabel('Department')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/department_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/department_analysis.png")
        
    def create_expertise_analysis(self):
        """Create expertise and specialization analysis"""
        print("\n🎯 Creating Expertise Analysis Visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Expertise and Specialization Analysis', fontsize=20, fontweight='bold')
        
        # 1. Primary expertise distribution
        primary_exp_counts = self.professors_df['primary_expertise'].value_counts().head(15)
        axes[0,0].barh(primary_exp_counts.index, primary_exp_counts.values, color='lightblue', edgecolor='navy')
        axes[0,0].set_title('Primary Expertise Distribution (Top 15)', fontweight='bold')
        axes[0,0].set_xlabel('Number of Professors')
        axes[0,0].set_ylabel('Expertise Area')
        
        # 2. Years of experience distribution
        axes[0,1].hist(self.professors_df['years_experience'], bins=20, color='lightcoral', edgecolor='darkred', alpha=0.7)
        axes[0,1].set_title('Distribution of Years of Experience', fontweight='bold')
        axes[0,1].set_xlabel('Years of Experience')
        axes[0,1].set_ylabel('Number of Professors')
        axes[0,1].axvline(self.professors_df['years_experience'].mean(), color='red', linestyle='--', 
                          label=f'Mean: {self.professors_df["years_experience"].mean():.1f}')
        axes[0,1].legend()
        
        # 3. Research allocation vs admin load
        axes[1,0].scatter(self.professors_df['research_allocation'], self.professors_df['admin_load'], 
                          alpha=0.6, color='lightgreen', s=50)
        axes[1,0].set_title('Research Allocation vs Administrative Load', fontweight='bold')
        axes[1,0].set_xlabel('Research Allocation (fraction)')
        axes[1,0].set_ylabel('Administrative Load (hours/week)')
        
        # Add trend line
        z = np.polyfit(self.professors_df['research_allocation'], self.professors_df['admin_load'], 1)
        p = np.poly1d(z)
        axes[1,0].plot(self.professors_df['research_allocation'], p(self.professors_df['research_allocation']), 
                       "r--", alpha=0.8)
        
        # 4. Teaching quality distribution
        axes[1,1].hist(self.professors_df['teaching_quality'], bins=20, color='gold', edgecolor='orange', alpha=0.7)
        axes[1,1].set_title('Distribution of Teaching Quality Ratings', fontweight='bold')
        axes[1,1].set_xlabel('Teaching Quality Rating')
        axes[1,1].set_ylabel('Number of Professors')
        axes[1,1].axvline(self.professors_df['teaching_quality'].mean(), color='red', linestyle='--',
                          label=f'Mean: {self.professors_df["teaching_quality"].mean():.3f}')
        axes[1,1].legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/expertise_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/expertise_analysis.png")
        
    def create_course_analysis(self):
        """Create comprehensive course analysis"""
        print("\n📚 Creating Course Analysis Visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Course Characteristics Analysis', fontsize=20, fontweight='bold')
        
        # 1. Difficulty level distribution
        difficulty_counts = self.courses_df['difficulty_level'].value_counts().sort_index()
        axes[0,0].bar(difficulty_counts.index, difficulty_counts.values, color='lightblue', edgecolor='navy')
        axes[0,0].set_title('Course Distribution by Difficulty Level', fontweight='bold')
        axes[0,0].set_xlabel('Difficulty Level (1=Beginner, 5=Advanced)')
        axes[0,0].set_ylabel('Number of Courses')
        
        # 2. Student enrollment distribution
        axes[0,1].hist(self.courses_df['num_students'], bins=20, color='lightcoral', edgecolor='darkred', alpha=0.7)
        axes[0,1].set_title('Distribution of Student Enrollment', fontweight='bold')
        axes[0,1].set_xlabel('Number of Students')
        axes[0,1].set_ylabel('Number of Courses')
        axes[0,1].axvline(self.courses_df['num_students'].mean(), color='red', linestyle='--',
                          label=f'Mean: {self.courses_df["num_students"].mean():.0f}')
        axes[0,1].legend()
        
        # 3. Lecture vs Lab hours
        axes[1,0].scatter(self.courses_df['lecture_hours'], self.courses_df['lab_hours'], 
                          alpha=0.6, color='lightgreen', s=50)
        axes[1,0].set_title('Lecture Hours vs Lab Hours', fontweight='bold')
        axes[1,0].set_xlabel('Lecture Hours per Week')
        axes[1,0].set_ylabel('Lab Hours per Week')
        
        # 4. Assessment hours vs preparation factor
        axes[1,1].scatter(self.courses_df['assessment_hours'], self.courses_df['prep_factor'], 
                          alpha=0.6, color='gold', s=50)
        axes[1,1].set_title('Assessment Hours vs Preparation Factor', fontweight='bold')
        axes[1,1].set_xlabel('Assessment Hours')
        axes[1,1].set_ylabel('Preparation Factor')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/course_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/course_analysis.png")
        
    def create_workload_analysis(self):
        """Create workload constraint analysis"""
        print("\n⚖️ Creating Workload Constraint Analysis...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Workload Constraint Analysis', fontsize=20, fontweight='bold')
        
        # 1. Teaching load constraints distribution
        axes[0,0].hist(self.professors_df['min_teaching_load'], bins=15, alpha=0.7, 
                       label='Minimum Teaching Load', color='lightblue')
        axes[0,0].hist(self.professors_df['max_teaching_load'], bins=15, alpha=0.7,
                       label='Maximum Teaching Load', color='lightcoral')
        axes[0,0].set_title('Distribution of Teaching Load Constraints', fontweight='bold')
        axes[0,0].set_xlabel('Teaching Load (hours/week)')
        axes[0,0].set_ylabel('Number of Professors')
        axes[0,0].legend()
        
        # 2. Workload capacity vs experience
        axes[0,1].scatter(self.professors_df['years_experience'], 
                          self.professors_df['max_teaching_load'] - self.professors_df['min_teaching_load'],
                          alpha=0.6, color='lightgreen', s=50)
        axes[0,1].set_title('Teaching Load Flexibility vs Experience', fontweight='bold')
        axes[0,1].set_xlabel('Years of Experience')
        axes[0,1].set_ylabel('Teaching Load Flexibility (max - min)')
        
        # 3. Research vs teaching allocation
        total_hours = 40  # Contracted hours
        teaching_hours = total_hours * (1 - self.professors_df['research_allocation'])
        admin_hours = self.professors_df['admin_load']
        
        axes[1,0].scatter(teaching_hours, admin_hours, alpha=0.6, color='gold', s=50)
        axes[1,0].set_title('Teaching Hours vs Administrative Hours', fontweight='bold')
        axes[1,0].set_xlabel('Teaching Hours per Week')
        axes[1,0].set_ylabel('Administrative Hours per Week')
        
        # 4. Workload balance analysis
        workload_balance = (self.professors_df['max_teaching_load'] + self.professors_df['min_teaching_load']) / 2
        axes[1,1].hist(workload_balance, bins=20, color='lightcoral', edgecolor='darkred', alpha=0.7)
        axes[1,1].set_title('Distribution of Average Teaching Load', fontweight='bold')
        axes[1,1].set_xlabel('Average Teaching Load (hours/week)')
        axes[1,1].set_ylabel('Number of Professors')
        axes[1,1].axvline(workload_balance.mean(), color='red', linestyle='--',
                          label=f'Mean: {workload_balance.mean():.1f}')
        axes[1,1].legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/workload_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/workload_analysis.png")
        
    def create_complexity_analysis(self):
        """Create problem complexity analysis"""
        print("\n🧮 Creating Problem Complexity Analysis...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Problem Complexity and Constraint Analysis', fontsize=20, fontweight='bold')
        
        # 1. Course difficulty vs student enrollment
        axes[0,0].scatter(self.courses_df['difficulty_level'], self.courses_df['num_students'], 
                          alpha=0.6, color='lightblue', s=50)
        axes[0,0].set_title('Course Difficulty vs Student Enrollment', fontweight='bold')
        axes[0,0].set_xlabel('Difficulty Level')
        axes[0,0].set_ylabel('Number of Students')
        
        # 2. Preparation factor vs difficulty
        axes[0,1].scatter(self.courses_df['difficulty_level'], self.courses_df['prep_factor'], 
                          alpha=0.6, color='lightcoral', s=50)
        axes[0,1].set_title('Preparation Factor vs Difficulty Level', fontweight='bold')
        axes[0,1].set_xlabel('Difficulty Level')
        axes[0,1].set_ylabel('Preparation Factor')
        
        # 3. Team teaching capability by difficulty
        team_teaching_by_difficulty = self.courses_df.groupby('difficulty_level')['can_be_shared'].mean()
        axes[1,0].bar(team_teaching_by_difficulty.index, team_teaching_by_difficulty.values, 
                      color='lightgreen', edgecolor='darkgreen')
        axes[1,0].set_title('Team Teaching Capability by Difficulty Level', fontweight='bold')
        axes[1,0].set_xlabel('Difficulty Level')
        axes[1,0].set_ylabel('Proportion of Courses Supporting Team Teaching')
        axes[1,0].set_ylim(0, 1)
        
        # 4. Course workload complexity
        total_workload = (self.courses_df['lecture_hours'] + self.courses_df['lab_hours']) * \
                        self.courses_df['prep_factor'] + self.courses_df['assessment_hours']
        
        axes[1,1].hist(total_workload, bins=20, color='gold', edgecolor='orange', alpha=0.7)
        axes[1,1].set_title('Distribution of Total Course Workload', fontweight='bold')
        axes[1,1].set_xlabel('Total Workload (hours)')
        axes[1,1].set_ylabel('Number of Courses')
        axes[1,1].axvline(total_workload.mean(), color='red', linestyle='--',
                          label=f'Mean: {total_workload.mean():.1f}')
        axes[1,1].legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/complexity_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   💾 Saved: {self.output_dir}/complexity_analysis.png")
        
    def create_summary_statistics(self):
        """Create summary statistics table"""
        print("\n📊 Creating Summary Statistics...")
        
        # Professors summary
        prof_summary = {
            'Metric': [
                'Total Professors',
                'Departments',
                'Expertise Areas',
                'Average Experience (years)',
                'Average Min Teaching Load (hours/week)',
                'Average Max Teaching Load (hours/week)',
                'Average Research Allocation',
                'Average Admin Load (hours/week)',
                'Average Teaching Quality'
            ],
            'Value': [
                len(self.professors_df),
                self.professors_df['department'].nunique(),
                self.professors_df['expertise'].nunique(),
                f"{self.professors_df['years_experience'].mean():.1f}",
                f"{self.professors_df['min_teaching_load'].mean():.1f}",
                f"{self.professors_df['max_teaching_load'].mean():.1f}",
                f"{self.professors_df['research_allocation'].mean():.3f}",
                f"{self.professors_df['admin_load'].mean():.1f}",
                f"{self.professors_df['teaching_quality'].mean():.3f}"
            ]
        }
        
        # Courses summary
        course_summary = {
            'Metric': [
                'Total Courses',
                'Departments',
                'Difficulty Levels',
                'Average Student Enrollment',
                'Team Teaching Courses (%)',
                'Average Lecture Hours',
                'Average Lab Hours',
                'Average Assessment Hours',
                'Average Preparation Factor'
            ],
            'Value': [
                len(self.courses_df),
                self.courses_df['department'].nunique(),
                f"{self.courses_df['difficulty_level'].min()}-{self.courses_df['difficulty_level'].max()}",
                f"{self.courses_df['num_students'].mean():.0f}",
                f"{self.courses_df['can_be_shared'].mean()*100:.1f}%",
                f"{self.courses_df['lecture_hours'].mean():.1f}",
                f"{self.courses_df['lab_hours'].mean():.1f}",
                f"{self.courses_df['assessment_hours'].mean():.1f}",
                f"{self.courses_df['prep_factor'].mean():.2f}"
            ]
        }
        
        # Save summary tables
        prof_summary_df = pd.DataFrame(prof_summary)
        course_summary_df = pd.DataFrame(course_summary)
        
        prof_summary_df.to_csv(f'{self.output_dir}/professors_summary.csv', index=False)
        course_summary_df.to_csv(f'{self.output_dir}/courses_summary.csv', index=False)
        
        print(f"   💾 Saved: {self.output_dir}/professors_summary.csv")
        print(f"   💾 Saved: {self.output_dir}/courses_summary.csv")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 DATASET SUMMARY STATISTICS")
        print("="*60)
        print("\n👨‍🏫 PROFESSORS DATASET:")
        print(prof_summary_df.to_string(index=False))
        print("\n📚 COURSES DATASET:")
        print(course_summary_df.to_string(index=False))
        
    def run_complete_eda(self):
        """Run the complete EDA analysis"""
        print("🚀 Starting Comprehensive Dataset EDA...")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Create output directory
        self.create_output_directory()
        
        # Run analyses
        self.analyze_professors()
        self.analyze_courses()
        
        # Create visualizations
        self.create_department_analysis()
        self.create_expertise_analysis()
        self.create_course_analysis()
        self.create_workload_analysis()
        self.create_complexity_analysis()
        
        # Generate summary statistics
        self.create_summary_statistics()
        
        print("\n" + "="*60)
        print("🎉 EDA COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📁 All visualizations saved to: {self.output_dir}/")
        print("📊 Summary statistics generated")
        print("🔍 Dataset thoroughly analyzed")
        print("\nReady for algorithm performance analysis! 🚀")

if __name__ == "__main__":
    eda = DatasetEDA()
    eda.run_complete_eda()
