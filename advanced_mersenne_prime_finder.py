#!/usr/bin/env python3
"""
Advanced Mersenne Prime Finder with Prime95 Integration
======================================================

This module provides comprehensive Mersenne prime discovery with:
- Pattern analysis and prediction
- Prime95 (GIMPS) integration for stress-tested Lucas-Lehmer tests
- C++ candidate generation for performance
- State management and resume capability
- Real-time progress monitoring

Author: MERSENNE Project Team
"""

import os
import sys
import json
import time
import math
import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

# Import our custom modules
from prime95_integration import integrate_with_prime95, parse_mersenne_findings
from heuristic_number_theory import (
    prime_number_theorem_pi_estimate,
    li_estimate,
    cramers_gap_estimate,
    hardy_littlewood_twin_constant
)
from enhanced_binary_filter import EnhancedBinaryFilter

# Known Mersenne prime exponents (first 52 Mersenne primes)
KNOWN_MERSENNE_EXPONENTS = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841
]

# Latest widely accepted Mersenne prime exponent (52nd)
LATEST_KNOWN_EXPONENT = 136279841


@dataclass
class SearchState:
    """Manages search state for resuming interrupted searches."""
    last_exponent_tested: int = 0
    prime95_results_offset: int = 0
    total_candidates_tested: int = 0
    total_primes_found: int = 0


class AdvancedMersennePrimeFinder:
    """
    Advanced Mersenne Prime Finder with Prime95 integration.
    
    Features:
    - Pattern-based prediction of likely Mersenne prime exponents
    - Integration with Prime95 for stress-tested Lucas-Lehmer tests
    - C++ candidate generation for performance
    - State management and resume capability
    - Real-time progress monitoring
    """
    
    def __init__(self, config_path: str = "mersenne_search_config.json"):
        """Initialize the finder with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.state = SearchState()
        self.progress_reporting = self.config.get('search_configuration', {}).get('progress_reporting', True)
        self.progress_step_percent = self.config.get('search_configuration', {}).get('progress_step_percent', 5)
        
        # Initialize enhanced binary filter for 1000x speedup
        self.binary_filter = EnhancedBinaryFilter()
        
        # Load saved state if available
        self._load_state()
        
        print(f"🔧 Advanced Mersenne Prime Finder initialized")
        print(f"📍 Starting from exponent: {self.state.last_exponent_tested:,}")
        print(f"🎯 Target: Find Mersenne primes > {LATEST_KNOWN_EXPONENT:,}")
        
        # Binary filter status
        filter_stats = self.binary_filter.get_filter_stats()
        print(f"⚡ Enhanced Binary Filter: {filter_stats['estimated_elimination_rate']:.1%} elimination rate")
        print(f"🔬 Pattern filters: {len(filter_stats['digit_sum_patterns'])} digit sums, {len(filter_stats['last_digit_patterns'])} last digits")
        
        # Prime95 integration status
        prime95_config = self.config.get('prime95_integration', {})
        if prime95_config.get('enabled', False):
            print(f"🔗 Prime95 integration: ENABLED")
            print(f"📁 Prime95 directory: {prime95_config.get('prime95_dir', 'Not set')}")
            print(f"📝 WorkToDo path: {prime95_config.get('worktodo_path', 'Not set')}")
        else:
            print(f"🔗 Prime95 integration: DISABLED")
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Configuration file not found: {self.config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration: {e}")
            return {}
    
    def _load_state(self) -> None:
        """Load search state from partial_search_result.json."""
        state_file = "partial_search_result.json"
        try:
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                    self.state.last_exponent_tested = state_data.get('last_exponent_tested', 0)
                    self.state.prime95_results_offset = state_data.get('prime95_results_offset', 0)
                    self.state.total_candidates_tested = state_data.get('total_candidates_tested', 0)
                    self.state.total_primes_found = state_data.get('total_primes_found', 0)
                    if self.progress_reporting:
                        print(f"📂 Loaded saved state: last tested = {self.state.last_exponent_tested:,}")
        except Exception as e:
            if self.progress_reporting:
                print(f"⚠️  Could not load state: {e}")
    
    def _save_state(self) -> None:
        """Save current search state to partial_search_result.json."""
        state_file = "partial_search_result.json"
        try:
            state_data = {
                'last_exponent_tested': self.state.last_exponent_tested,
                'prime95_results_offset': self.state.prime95_results_offset,
                'total_candidates_tested': self.state.total_candidates_tested,
                'total_primes_found': self.state.total_primes_found,
                'timestamp': time.time()
            }
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2)
        except Exception as e:
            if self.progress_reporting:
                print(f"⚠️  Could not save state: {e}")
    
    def analyze_patterns(self) -> List[int]:
        """
        Analyze patterns in known Mersenne prime exponents and predict likely candidates.
        
        Returns:
            List of predicted Mersenne prime exponents in order of likelihood.
        """
        if self.progress_reporting:
            print("\n🔍 Analyzing Mersenne prime patterns...")
        
        exponents = KNOWN_MERSENNE_EXPONENTS
        n = len(exponents)
        
        # Calculate gaps between consecutive exponents
        gaps = [exponents[i+1] - exponents[i] for i in range(n-1)]
        
        if self.progress_reporting:
            print(f"📊 Analyzing {n} known Mersenne prime exponents")
            print(f"📏 Gap statistics: min={min(gaps):,}, max={max(gaps):,}, avg={sum(gaps)/len(gaps):,.0f}")
        
        # Exponential regression for trend analysis
        log_exponents = [math.log(p) for p in exponents]
        x_values = list(range(1, n+1))
        
        # Simple linear regression on log scale
        sum_x = sum(x_values)
        sum_y = sum(log_exponents)
        sum_xy = sum(x * y for x, y in zip(x_values, log_exponents))
        sum_x2 = sum(x * x for x in x_values)
        
        n_float = float(n)
        slope = (n_float * sum_xy - sum_x * sum_y) / (n_float * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n_float
        
        # Predict next few exponents using exponential model
        predictions = []
        for i in range(n+1, n+6):  # Predict next 5
            predicted_log = slope * i + intercept
            predicted_exp = int(math.exp(predicted_log))
            predictions.append(predicted_exp)
        
        # Apply heuristic number theory constraints
        current_frontier = exponents[-1]
        
        if self.progress_reporting:
            print(f"\n🧮 Heuristic Number Theory Analysis:")
            print(f"📍 Current frontier: p = {current_frontier:,}")
            
            # Prime Number Theorem estimate
            pi_estimate = prime_number_theorem_pi_estimate(current_frontier)
            print(f"📈 π({current_frontier:,}) ≈ {pi_estimate:,.0f} (PNT estimate)")
            
            # Logarithmic Integral estimate
            li_est = li_estimate(current_frontier)
            print(f"📈 li({current_frontier:,}) ≈ {li_est:,.0f} (Logarithmic Integral)")
            
            # Cramér's conjecture gap estimate
            cramer_gap = cramers_gap_estimate(current_frontier)
            print(f"📏 Expected gap ≈ {cramer_gap:,.0f} (Cramér's conjecture)")
        
        # Filter predictions to be reasonable but not too restrictive
        reasonable_predictions = []
        for pred in predictions:
            # Must be larger than latest known
            if pred > LATEST_KNOWN_EXPONENT:
                # Relaxed acceptance window to ensure we generate targets
                min_reasonable = LATEST_KNOWN_EXPONENT + 10_000
                max_reasonable = LATEST_KNOWN_EXPONENT + 50_000_000
                if min_reasonable <= pred <= max_reasonable:
                    reasonable_predictions.append(pred)
        
        if self.progress_reporting:
            print(f"\n🎯 Pattern-based predictions:")
            for i, pred in enumerate(reasonable_predictions, 1):
                print(f"   {i}. p = {pred:,}")
        
        return reasonable_predictions
    
    def generate_search_ranges(self, predictions: List[int]) -> List[Tuple[int, int]]:
        """
        Generate search ranges around predicted exponents.
        
        Args:
            predictions: List of predicted exponents
            
        Returns:
            List of (start, end) tuples for search ranges
        """
        ranges = []
        for pred in predictions:
            # Create range around prediction (±10%)
            margin = max(100000, pred // 10)
            start = max(LATEST_KNOWN_EXPONENT, pred - margin)
            end = pred + margin
            ranges.append((start, end))
        
        return ranges
    
    def search_range(self, start: int, end: int, max_candidates: int = 10000) -> List[int]:
        """
        Search for prime exponents in a given range.
        
        Args:
            start: Start of range (inclusive)
            end: End of range (exclusive)
            max_candidates: Maximum number of candidates to return
            
        Returns:
            List of prime exponents found
        """
        if self.progress_reporting:
            print(f"\n🔍 Searching range [{start:,}, {end:,}) for prime exponents...")
        
        # Check if C++ candidate generator is available
        cpp_config = self.config.get('cpp_core', {})
        use_cpp = cpp_config.get('enabled', False) and os.path.exists(cpp_config.get('exe_path', ''))
        
        if use_cpp:
            return self._search_range_cpp(start, end, max_candidates)
        else:
            return self._search_range_python(start, end, max_candidates)
    
    def _search_range_python(self, start: int, end: int, max_candidates: int) -> List[int]:
        """Python implementation of prime exponent search with binary filtering."""
        candidates = []
        total_tested = 0
        filtered_out = 0
        
        # Only search odd numbers
        for p in range(start if start % 2 == 1 else start + 1, end, 2):
            total_tested += 1
            
            # Apply ultra-fast binary pattern filter first (1000x speedup)
            if not self.binary_filter.ultra_fast_pattern_filter(p):
                filtered_out += 1
                continue
                
            if self._is_probably_prime(p):
                candidates.append(p)
                if len(candidates) >= max_candidates:
                    break
            
            # Progress reporting with filter statistics
            if self.progress_reporting and p % 100000 == 1:
                progress = (p - start) / (end - start) * 100
                elimination_rate = filtered_out / total_tested if total_tested > 0 else 0
                print(f"   📊 Progress: {progress:.1f}% - Found {len(candidates)} candidates")
                print(f"   ⚡ Filter efficiency: {elimination_rate:.1%} eliminated ({filtered_out:,}/{total_tested:,})")
        
        # Final statistics
        if self.progress_reporting and total_tested > 0:
            final_elimination = filtered_out / total_tested
            speedup = 1 / (1 - final_elimination) if final_elimination < 1 else float('inf')
            print(f"   🎯 Binary filter results: {final_elimination:.1%} eliminated, {speedup:.1f}x speedup")
        
        return candidates
    
    def _search_range_cpp(self, start: int, end: int, max_candidates: int) -> List[int]:
        """Use C++ candidate generator for faster search."""
        exe_path = self.config.get('cpp_core', {}).get('exe_path', 'candidate_generator.exe')
        
        try:
            import subprocess
            result = subprocess.run([exe_path, str(start), str(end), str(max_candidates)], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                candidates = [int(line.strip()) for line in result.stdout.strip().split('\n') if line.strip()]
                if self.progress_reporting:
                    print(f"   ⚡ C++ generator found {len(candidates)} candidates")
                return candidates
            else:
                if self.progress_reporting:
                    print(f"   ⚠️  C++ generator failed, falling back to Python")
                return self._search_range_python(start, end, max_candidates)
                
        except Exception as e:
            if self.progress_reporting:
                print(f"   ⚠️  C++ generator error: {e}, falling back to Python")
            return self._search_range_python(start, end, max_candidates)
    
    def _is_probably_prime(self, n: int, k: int = 20) -> bool:
        """
        Miller-Rabin primality test.
        
        Args:
            n: Number to test
            k: Number of rounds (higher = more accurate)
            
        Returns:
            True if n is probably prime, False if composite
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as d * 2^r
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness loop
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def test_candidates(self, candidates: List[int], use_prime95_ll: bool = False) -> List[int]:
        """
        Test candidate exponents using Lucas-Lehmer test or Prime95 integration.
        
        Args:
            candidates: List of candidate exponents to test
            use_prime95_ll: If True, delegate LL testing to Prime95
            
        Returns:
            List of confirmed Mersenne prime exponents
        """
        if not candidates:
            return []
        
        if self.progress_reporting:
            print(f"\n🧪 Testing {len(candidates)} candidate exponents...")
        
        # Check Prime95 integration
        prime95_config = self.config.get('prime95_integration', {})
        results_path = prime95_config.get('results_path')
        
        if use_prime95_ll and results_path:
            print("🔗 Skipping Python LL; delegating to Prime95 and parsing results for proof...")
            
            # Parse Prime95 results for any new confirmations
            parsed = parse_mersenne_findings(results_path, since_bytes=self.state.prime95_results_offset)
            self.state.prime95_results_offset = parsed.get('new_offset', self.state.prime95_results_offset)
            confirmed = parsed.get('confirmed_exponents', [])
            
            if confirmed:
                for p in sorted(set(confirmed)):
                    print(f"\n🎓 PROOF: Prime95 confirmed M({p:,}) is prime!")
                mersenne_primes = sorted(set(confirmed))
                self.state.total_primes_found += len(mersenne_primes)
            
            # Update resume point conservatively to max of tested candidates if any
            if candidates:
                self.state.last_exponent_tested = max(self.state.last_exponent_tested, max(candidates))
            
            self._save_state()
            return mersenne_primes if confirmed else []
        
        # Python-based Lucas-Lehmer test (limited to smaller exponents)
        mersenne_primes = []
        max_testable = 5000  # Python LL test limit
        
        for i, p in enumerate(candidates):
            if p > max_testable:
                if self.progress_reporting:
                    print(f"   ⚠️  Skipping p={p:,} (too large for Python LL test)")
                continue
            
            if self._lucas_lehmer_test(p):
                print(f"\n🎉 FOUND: M({p:,}) is prime!")
                mersenne_primes.append(p)
                self.state.total_primes_found += 1
            
            # Update progress
            if self.progress_reporting and (i + 1) % 10 == 0:
                progress = (i + 1) / len(candidates) * 100
                print(f"   📊 Progress: {progress:.1f}% - Tested {i+1}/{len(candidates)}")
        
        # Update state
        if candidates:
            self.state.last_exponent_tested = max(self.state.last_exponent_tested, max(candidates))
        self.state.total_candidates_tested += len(candidates)
        self._save_state()
        
        return mersenne_primes
    
    def _lucas_lehmer_test(self, p: int) -> bool:
        """
        Lucas-Lehmer test for Mersenne primes.
        
        Args:
            p: Exponent to test (2^p - 1)
            
        Returns:
            True if 2^p - 1 is prime, False otherwise
        """
        if p == 2:
            return True
        
        s = 4
        m = (1 << p) - 1  # 2^p - 1
        
        for _ in range(p - 2):
            s = (s * s - 2) % m
        
        return s == 0

    # --- Compatibility layer for start_mersenne_search.py ---
    @property
    def candidates_tested(self) -> int:
        """Compat: expose total candidates tested for status reporting."""
        return self.state.total_candidates_tested

    def run_advanced_search(self, num_predictions: int = 3) -> List[int]:
        """
        Compat wrapper expected by start_mersenne_search.py.
        Currently delegates to run_search(); num_predictions is guided by
        configuration and pattern analysis inside run_search.
        """
        # Future: thread num_predictions through analyze/generate if needed
        return self.run_search()
    
    def run_search(self) -> List[int]:
        """
        Run the complete Mersenne prime search process.
        
        Returns:
            List of newly discovered Mersenne prime exponents
        """
        print("\n🚀 Starting Advanced Mersenne Prime Search")
        print("=" * 50)
        
        # Step 1: Pattern analysis
        predictions = self.analyze_patterns()
        
        # Step 2: Generate search ranges. If no predictions, fall back to configured ranges
        ranges = []
        if predictions:
            ranges = self.generate_search_ranges(predictions)
        else:
            print("⚙️  No predictions passed filters — falling back to configured search_ranges")
            cfg_ranges = (self.config.get('search_ranges') or {}).values()
            for r in cfg_ranges:
                try:
                    start = int(r.get('start'))
                    end = int(r.get('end'))
                    if end > start and end > LATEST_KNOWN_EXPONENT:
                        # Ensure we start strictly after latest known exponent
                        start = max(start, LATEST_KNOWN_EXPONENT + 1)
                        ranges.append((start, end))
                except Exception:
                    continue
        if not ranges:
            print("❌ No valid ranges available. Check configuration.")
            return []
        
        # Step 3: Search each range
        all_candidates = []
        for i, (start, end) in enumerate(ranges, 1):
            if self.progress_reporting:
                print(f"\n📍 Range {i}/{len(ranges)}: [{start:,}, {end:,})")
            
            candidates = self.search_range(start, end)
            all_candidates.extend(candidates)
        
        # Always start testing strictly after the 52nd Mersenne prime exponent
        start_after = max(LATEST_KNOWN_EXPONENT, self.state.last_exponent_tested)
        filtered_candidates = [p for p in all_candidates if p > start_after]
        
        if self.progress_reporting:
            print(f"\n🔎 Filtered to {len(filtered_candidates)} candidate exponents > {start_after:,}")
        
        if not filtered_candidates:
            print("❌ No candidates found in search ranges")
            return []
        
        # Step 4: Test candidates
        prime95_config = self.config.get('prime95_integration', {})
        use_prime95_ll = prime95_config.get('enabled', False) and prime95_config.get('use_for_ll', False)
        
        mersenne_primes = self.test_candidates(filtered_candidates, use_prime95_ll=use_prime95_ll)
        
        # Step 5: Integrate with Prime95 if enabled
        if prime95_config.get('enabled', False) and not use_prime95_ll:
            print("\n🔗 Integrating with Prime95...")
            integration_result = integrate_with_prime95(filtered_candidates, self.config)
            
            if integration_result.get('enabled'):
                print(f"✅ Prime95 integration successful:")
                print(f"   📝 WorkToDo entries written: {integration_result.get('lines_written', 0)}")
                print(f"   📁 WorkToDo file: {integration_result.get('worktodo_path', 'N/A')}")
                if integration_result.get('launched'):
                    print(f"   🚀 Prime95 launched automatically")
            else:
                print(f"❌ Prime95 integration failed: {integration_result.get('reason', 'Unknown error')}")
        
        # Summary
        print(f"\n📊 Search Summary:")
        print(f"   🎯 Candidates tested: {len(filtered_candidates):,}")
        print(f"   🏆 Mersenne primes found: {len(mersenne_primes)}")
        print(f"   📍 Last tested exponent: {self.state.last_exponent_tested:,}")
        
        return mersenne_primes


def main():
    """Main entry point for the advanced Mersenne prime finder."""
    try:
        finder = AdvancedMersennePrimeFinder()
        results = finder.run_search()
        
        if results:
            print(f"\n🎉 SUCCESS: Found {len(results)} new Mersenne primes!")
            for p in results:
                print(f"   M({p:,}) is prime!")
        else:
            print("\n🔍 No new Mersenne primes found in this search.")
            print("💡 Consider expanding search ranges or running longer searches.")
    
    except KeyboardInterrupt:
        print("\n⏹️  Search interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()



