#!/usr/bin/env python3
"""
Simple Launcher for MERSENNE Live Proof System
Windows-compatible version without Unicode issues
"""

import os
import sys
import time
import subprocess

def install_flask():
    """Install Flask if not available"""
    try:
        import flask
        print("Flask is available")
        return True
    except ImportError:
        print("Installing Flask...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
            print("Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install Flask")
            return False

def run_success_proof_demo():
    """Run the success proof demonstration"""
    print("\n=== RUNNING SUCCESS PROOF DEMO ===")
    
    try:
        from real_time_success_proof import run_success_proof_demo
        results = run_success_proof_demo()
        print("Success proof demo completed")
        return True
    except Exception as e:
        print(f"Success proof demo failed: {e}")
        return False

def run_validation():
    """Run success rate validation"""
    print("\n=== RUNNING SUCCESS RATE VALIDATION ===")
    
    try:
        from success_rate_validator import run_complete_validation
        results = run_complete_validation()
        print("Success rate validation completed")
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False

def create_showcase_files():
    """Create showcase files"""
    print("\n=== CREATING SHOWCASE FILES ===")
    
    try:
        from run_success_showcase import create_showcase_index
        from real_time_success_proof import create_gallery_showcase
        
        index_file = create_showcase_index()
        gallery_file = create_gallery_showcase()
        
        print(f"Created: {index_file}")
        print(f"Created: {gallery_file}")
        return True
    except Exception as e:
        print(f"Showcase creation failed: {e}")
        return False

def test_binary_filter():
    """Test the binary filter system"""
    print("\n=== TESTING BINARY FILTER ===")
    
    try:
        from enhanced_binary_filter import EnhancedBinaryFilter
        
        filter_system = EnhancedBinaryFilter()
        stats = filter_system.get_filter_stats()
        
        print(f"Known exponents: {stats['known_exponents_count']}")
        print(f"Elimination rate: {stats['estimated_elimination_rate']:.1%}")
        
        # Test with known Mersenne prime
        test_candidates = [31, 127, 521]
        filtered = filter_system.filter_candidates(test_candidates)
        
        print(f"Filter test: {len(test_candidates)} -> {len(filtered)} candidates")
        return True
    except Exception as e:
        print(f"Binary filter test failed: {e}")
        return False

def main():
    """Main function"""
    print("MERSENNE LIVE PROOF SYSTEM")
    print("=" * 50)
    print("Starting comprehensive demonstration...")
    
    # Step 1: Install dependencies
    if not install_flask():
        print("Cannot proceed without Flask")
        return False
    
    # Step 2: Test binary filter
    if not test_binary_filter():
        print("Binary filter test failed")
        return False
    
    # Step 3: Run validation
    if not run_validation():
        print("Validation failed")
        return False
    
    # Step 4: Run success proof demo
    if not run_success_proof_demo():
        print("Success proof demo failed")
        return False
    
    # Step 5: Create showcase files
    if not create_showcase_files():
        print("Showcase creation failed")
        return False
    
    print("\n" + "=" * 50)
    print("MERSENNE SYSTEM LAUNCHED SUCCESSFULLY!")
    print("=" * 50)
    print("Generated files:")
    print("  - success_showcase.html")
    print("  - discovery_gallery.html")
    print("  - success_proof.json")
    print("  - success_validation_proof.json")
    print("\nOpen success_showcase.html in your browser to view the complete showcase")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\nSystem ready! Open success_showcase.html to view results.")
        else:
            print("\nSystem launch failed. Check error messages above.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()