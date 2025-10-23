#!/usr/bin/env python3
"""
🚀 RUN REVOLUTIONARY MERSENNE DISCOVERY 🚀
Main script to launch the complete discovery system
"""

import sys
import os
import argparse
from datetime import datetime
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from revolutionary_mersenne_discovery import RevolutionaryMersenneDiscovery
from advanced_candidate_generator import AdvancedCandidateGenerator
from discovery_dashboard import DiscoveryDashboard

def main():
    """Main function to run the revolutionary discovery system"""
    parser = argparse.ArgumentParser(description="Revolutionary Mersenne Prime Discovery System")
    parser.add_argument("--start", type=int, default=136279843, help="Start range for search (after M52)")
    parser.add_argument("--end", type=int, default=137279843, help="End range for search")
    parser.add_argument("--candidates", type=int, default=10000, help="Maximum number of candidates to test")
    parser.add_argument("--workers", type=int, default=4, help="Number of worker threads")
    parser.add_argument("--config", type=str, default="mersenne_search_config.json", help="Configuration file")
    parser.add_argument("--dashboard", action="store_true", help="Enable real-time dashboard")
    parser.add_argument("--save-patterns", action="store_true", help="Save pattern analysis")
    parser.add_argument("--quick-test", action="store_true", help="Run quick test with smaller range")
    
    args = parser.parse_args()
    
    # Quick test mode
    if args.quick_test:
        args.start = 136279843  # Start after M52
        args.end = 136280843    # Small 1000 range for testing
        args.candidates = 1000
        print("🧪 QUICK TEST MODE - Using smaller range for testing (after M52)")
    
    print("🚀 REVOLUTIONARY MERSENNE PRIME DISCOVERY SYSTEM 🚀")
    print("=" * 80)
    print(f"📊 Search Range: {args.start:,} to {args.end:,}")
    print(f"🎯 Max Candidates: {args.candidates:,}")
    print(f"🧵 Worker Threads: {args.workers}")
    print(f"📋 Config File: {args.config}")
    print(f"📊 Dashboard: {'Enabled' if args.dashboard else 'Disabled'}")
    print("=" * 80)
    
    try:
        # Initialize discovery engine
        print("🔧 Initializing discovery engine...")
        discovery = RevolutionaryMersenneDiscovery(args.config)
        
        # Update worker count in config
        if "optimization_settings" not in discovery.config:
            discovery.config["optimization_settings"] = {}
        discovery.config["optimization_settings"]["max_workers"] = args.workers
        
        # Initialize dashboard if enabled
        dashboard = None
        if args.dashboard:
            print("📊 Starting real-time dashboard...")
            dashboard = DiscoveryDashboard(discovery)
            dashboard_thread = None
            # Dashboard will be started in a separate thread
        
        # Save pattern analysis if requested
        if args.save_patterns:
            print("🧠 Analyzing patterns and saving analysis...")
            generator = AdvancedCandidateGenerator()
            generator.save_pattern_analysis()
        
        # Run discovery
        print(f"\n🚀 Starting discovery process...")
        print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if dashboard:
            # Start dashboard in background
            import threading
            dashboard_thread = threading.Thread(target=dashboard.start_monitoring)
            dashboard_thread.daemon = True
            dashboard_thread.start()
        
        # Run the discovery
        discoveries = discovery.run_discovery(args.start, args.end, args.candidates)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = discovery.save_results(f"discovery_results_{timestamp}.json")
        
        # Save dashboard report if enabled
        if dashboard:
            dashboard.save_report(f"dashboard_report_{timestamp}.json")
        
        # Final summary
        print(f"\n🎉 DISCOVERY SESSION COMPLETE! 🎉")
        print(f"📁 Results saved to: {results_file}")
        if dashboard:
            print(f"📊 Dashboard report saved")
        
        if discoveries:
            print(f"🏆 Found {len(discoveries)} new Mersenne primes!")
            for i, disc in enumerate(discoveries, 1):
                print(f"  #{i}: p = {disc['exponent']:,}")
        else:
            print(f"💡 No new discoveries this session")
            print(f"   Try expanding the range or increasing candidate count")
        
        print(f"\n🔬 Next steps:")
        print(f"   • Analyze results in {results_file}")
        print(f"   • Adjust search parameters for next run")
        print(f"   • Consider different ranges or pattern weights")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Discovery stopped by user")
        if dashboard:
            dashboard.running = False
    except Exception as e:
        print(f"\n❌ Error during discovery: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n👋 Discovery session ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
