#!/usr/bin/env python3
"""
Simple script to generate the comprehensive university dataset
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from dataset_generator import main

if __name__ == "__main__":
    print("Starting dataset generation...")
    main()
    print("\nDataset generation completed successfully!")
