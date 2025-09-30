#!/usr/bin/env python3
"""
Data Setup Script for Movie Recommendation System
Generates the required data files for the application to work.
"""

import os
import sys
from pathlib import Path

def setup_data_files():
    """Generate required data files for the movie recommendation system."""
    
    # Change to src directory
    src_dir = Path(__file__).parent / "src"
    os.chdir(src_dir)
    
    print("🔧 Setting up data files for Movie Recommendation System...")
    
    # Check if movies.csv exists
    if not Path("movies.csv").exists():
        print("❌ Error: movies.csv not found in src directory!")
        print("Please ensure the movie dataset is available.")
        sys.exit(1)
    
    print("📊 Running preprocessing to generate data files...")
    
    # Run preprocessing
    try:
        import subprocess
        result = subprocess.run([sys.executable, "preprocess.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Data files generated successfully!")
            print("Generated files:")
            
            files_to_check = [
                "cleaned.parquet",
                "cosine_sim.npz", 
                "tfidf_matrix.npz"
            ]
            
            for file in files_to_check:
                if Path(file).exists():
                    size = Path(file).stat().st_size / (1024*1024)  # MB
                    print(f"  ✓ {file} ({size:.1f} MB)")
                else:
                    print(f"  ❌ {file} (missing)")
            
            print("\n🚀 Setup complete! You can now run the application.")
            
        else:
            print("❌ Error during preprocessing:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_data_files()