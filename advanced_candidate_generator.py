#!/usr/bin/env python3
"""
🧠 ADVANCED CANDIDATE GENERATOR 🧠
Mathematical pattern analysis for intelligent Mersenne prime candidate generation
"""

import math
import numpy as np
from typing import List, Dict, Tuple
import json
from datetime import datetime

class AdvancedCandidateGenerator:
    def __init__(self):
        """Initialize the advanced candidate generator"""
        self.known_mersenne_primes = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
            2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
            23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
            1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
            24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
            43112609, 57885161, 74207281, 77232917, 82589933, 136279841
        ]
        
        # Analyze patterns
        self.patterns = self._analyze_patterns()
        print(f"🧠 Advanced Candidate Generator initialized")
        print(f"📊 Analyzed {len(self.known_mersenne_primes)} known Mersenne primes")
    
    def is_valid_mersenne_exponent_candidate(self, p: int) -> bool:
        """Check if a number is a valid Mersenne exponent candidate based on mathematical properties"""
        # Must be > 52nd Mersenne prime (136,279,841)
        if p <= 136279841:
            return False
        
        # Must be odd (except 2, but we're after 52nd)
        if p % 2 == 0:
            return False
        
        # Must be prime
        if not self.is_prime(p):
            return False
        
        # Modulo 4: must be ≡ 1 or 3 (all odd primes)
        if p % 4 not in [1, 3]:
            return False
        
        # Modulo 6: must be ≡ 1 or 5 (all primes > 3)
        if p > 3 and p % 6 not in [1, 5]:
            return False
        
        # Last digit: must end in 1, 3, 7, or 9 (except 2, 5)
        if p > 5 and p % 10 not in [1, 3, 7, 9]:
            return False
        
        return True
    
    def is_prime(self, n: int) -> bool:
        """Fast primality test for Mersenne exponent candidates"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        
        # Miller-Rabin test with optimal bases
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        
        # Use deterministic bases for different ranges
        if n < 1373653:
            bases = [2, 3]
        elif n < 9080191:
            bases = [31, 73]
        elif n < 4759123141:
            bases = [2, 7, 61]
        else:
            bases = [2, 3, 5, 7, 11, 13, 17]
        
        for a in bases:
            if a >= n:
                continue
            
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
    
    def _analyze_patterns(self) -> Dict:
        """Comprehensive pattern analysis of known Mersenne primes"""
        if len(self.known_mersenne_primes) < 5:
            return {"error": "Not enough data for analysis"}
        
        patterns = {}
        
        # 1. Gap Analysis
        gaps = []
        for i in range(1, len(self.known_mersenne_primes)):
            gap = self.known_mersenne_primes[i] - self.known_mersenne_primes[i-1]
            gaps.append(gap)
        
        patterns["gaps"] = {
            "values": gaps,
            "mean": np.mean(gaps),
            "std": np.std(gaps),
            "min": min(gaps),
            "max": max(gaps),
            "median": np.median(gaps)
        }
        
        # 2. Growth Rate Analysis
        log_primes = [math.log(p) for p in self.known_mersenne_primes]
        growth_rates = []
        for i in range(1, len(log_primes)):
            rate = log_primes[i] - log_primes[i-1]
            growth_rates.append(rate)
        
        patterns["growth"] = {
            "rates": growth_rates,
            "mean_rate": np.mean(growth_rates),
            "std_rate": np.std(growth_rates),
            "trend": "exponential" if np.mean(growth_rates) > 0.1 else "linear"
        }
        
        # 3. Modulo Pattern Analysis
        mod_210 = {}  # 210 = 2*3*5*7
        mod_30 = {}   # 30 = 2*3*5
        mod_6 = {}    # 6 = 2*3
        
        for p in self.known_mersenne_primes:
            m210 = p % 210
            m30 = p % 30
            m6 = p % 6
            
            mod_210[m210] = mod_210.get(m210, 0) + 1
            mod_30[m30] = mod_30.get(m30, 0) + 1
            mod_6[m6] = mod_6.get(m6, 0) + 1
        
        patterns["modulo"] = {
            "mod_210": mod_210,
            "mod_30": mod_30,
            "mod_6": mod_6,
            "preferred_mod_210": max(mod_210.items(), key=lambda x: x[1])[0],
            "preferred_mod_30": max(mod_30.items(), key=lambda x: x[1])[0],
            "preferred_mod_6": max(mod_6.items(), key=lambda x: x[1])[0]
        }
        
        # 4. Digit Pattern Analysis
        digit_counts = [len(str(p)) for p in self.known_mersenne_primes[-10:]]
        patterns["digits"] = {
            "recent_counts": digit_counts,
            "avg_digits": np.mean(digit_counts),
            "digit_growth_rate": (digit_counts[-1] - digit_counts[0]) / len(digit_counts) if len(digit_counts) > 1 else 0
        }
        
        # 5. Prime Density Analysis
        # Analyze density in different ranges
        ranges = [(1, 1000), (1000, 10000), (10000, 100000), (100000, 1000000)]
        density_analysis = {}
        
        for start, end in ranges:
            primes_in_range = [p for p in self.known_mersenne_primes if start <= p < end]
            density = len(primes_in_range) / (end - start)
            density_analysis[f"range_{start}_{end}"] = {
                "count": len(primes_in_range),
                "density": density,
                "primes": primes_in_range
            }
        
        patterns["density"] = density_analysis
        
        # 6. Twin Prime Analysis (consecutive Mersenne exponents)
        twins = []
        for i in range(1, len(self.known_mersenne_primes)):
            if self.known_mersenne_primes[i] - self.known_mersenne_primes[i-1] == 2:
                twins.append((self.known_mersenne_primes[i-1], self.known_mersenne_primes[i]))
        
        patterns["twins"] = {
            "pairs": twins,
            "count": len(twins),
            "twin_rate": len(twins) / (len(self.known_mersenne_primes) - 1)
        }
        
        return patterns
    
    def generate_candidates_exponential(self, start: int, end: int, count: int) -> List[int]:
        """Generate VALID candidates using exponential growth pattern"""
        candidates = []
        growth_rate = self.patterns["growth"]["mean_rate"]
        
        current = start
        while current < end and len(candidates) < count:
            if self.is_valid_mersenne_exponent_candidate(current):
                candidates.append(current)
            # Use exponential growth with some randomness
            increment = int(current * growth_rate * (0.8 + 0.4 * np.random.random()))
            current += max(1, increment)
        
        return candidates
    
    def generate_candidates_gap_based(self, start: int, end: int, count: int) -> List[int]:
        """Generate VALID candidates based on gap analysis"""
        candidates = []
        gap_mean = self.patterns["gaps"]["mean"]
        gap_std = self.patterns["gaps"]["std"]
        
        current = start
        while current < end and len(candidates) < count:
            if self.is_valid_mersenne_exponent_candidate(current):
                candidates.append(current)
            # Use gap distribution with some variation
            gap = int(gap_mean + np.random.normal(0, gap_std * 0.5))
            current += max(1, gap)
        
        return candidates
    
    def generate_candidates_modulo(self, start: int, end: int, count: int) -> List[int]:
        """Generate VALID candidates using modulo pattern analysis"""
        candidates = []
        preferred_mod_210 = self.patterns["modulo"]["preferred_mod_210"]
        preferred_mod_30 = self.patterns["modulo"]["preferred_mod_30"]
        
        # Start from the preferred modulo pattern
        current = start - (start % 210) + preferred_mod_210
        if current < start:
            current += 210
        
        while current < end and len(candidates) < count:
            if self.is_valid_mersenne_exponent_candidate(current):
                candidates.append(current)
            current += 210  # Step by 210 to maintain modulo pattern
        
        return candidates
    
    def generate_candidates_density_weighted(self, start: int, end: int, count: int) -> List[int]:
        """Generate VALID candidates weighted by historical density"""
        candidates = []
        
        # Create density map
        density_map = {}
        for range_name, data in self.patterns["density"].items():
            range_start, range_end = map(int, range_name.split('_')[1:3])
            density = data["density"]
            for i in range(range_start, min(range_end, end)):
                density_map[i] = density
        
        # Weight candidates by density
        if density_map:
            max_density = max(density_map.values())
            for candidate in range(start, end):
                if (self.is_valid_mersenne_exponent_candidate(candidate) and 
                    len(candidates) < count):
                    weight = density_map.get(candidate, 0.1) / max_density
                    if np.random.random() < weight:
                        candidates.append(candidate)
        
        return candidates
    
    def generate_candidates_twin_focused(self, start: int, end: int, count: int) -> List[int]:
        """Generate VALID candidates focusing on potential twin Mersenne exponents"""
        candidates = []
        twin_rate = self.patterns["twins"]["twin_rate"]
        
        # Look for potential twins
        for candidate in range(start, end):
            if len(candidates) >= count:
                break
            
            # Check if candidate-2 or candidate+2 is a known Mersenne prime
            if ((candidate - 2 in self.known_mersenne_primes or 
                 candidate + 2 in self.known_mersenne_primes) and
                self.is_valid_mersenne_exponent_candidate(candidate)):
                candidates.append(candidate)
        
        return candidates
    
    def generate_intelligent_candidates(self, start: int, end: int, count: int = 1000) -> List[int]:
        """Generate intelligent candidates using all pattern analysis methods"""
        print(f"🧠 Generating {count} intelligent candidates in range [{start:,}, {end:,}]")
        
        all_candidates = []
        
        # Method 1: Exponential growth (30%)
        exp_count = int(count * 0.3)
        exp_candidates = self.generate_candidates_exponential(start, end, exp_count)
        all_candidates.extend(exp_candidates)
        print(f"  📈 Exponential: {len(exp_candidates)} candidates")
        
        # Method 2: Gap-based (25%)
        gap_count = int(count * 0.25)
        gap_candidates = self.generate_candidates_gap_based(start, end, gap_count)
        all_candidates.extend(gap_candidates)
        print(f"  📏 Gap-based: {len(gap_candidates)} candidates")
        
        # Method 3: Modulo patterns (20%)
        mod_count = int(count * 0.2)
        mod_candidates = self.generate_candidates_modulo(start, end, mod_count)
        all_candidates.extend(mod_candidates)
        print(f"  🔢 Modulo patterns: {len(mod_candidates)} candidates")
        
        # Method 4: Density-weighted (15%)
        density_count = int(count * 0.15)
        density_candidates = self.generate_candidates_density_weighted(start, end, density_count)
        all_candidates.extend(density_candidates)
        print(f"  🎯 Density-weighted: {len(density_candidates)} candidates")
        
        # Method 5: Twin-focused (10%)
        twin_count = int(count * 0.1)
        twin_candidates = self.generate_candidates_twin_focused(start, end, twin_count)
        all_candidates.extend(twin_candidates)
        print(f"  👥 Twin-focused: {len(twin_candidates)} candidates")
        
        # Remove duplicates and sort
        unique_candidates = sorted(list(set(all_candidates)))
        
        # If we don't have enough, fill with PRIME-VALID candidates only
        if len(unique_candidates) < count:
            import random
            random.seed(42)
            attempts = 0
            # Safety cap to avoid long loops if range is tight
            max_attempts = max(10000, (count - len(unique_candidates)) * 50)
            while len(unique_candidates) < count and attempts < max_attempts:
                candidate = random.randint(start, end)
                attempts += 1
                if (candidate not in unique_candidates and 
                    self.is_valid_mersenne_exponent_candidate(candidate)):
                    unique_candidates.append(candidate)
        
        # Sort and limit
        unique_candidates = sorted(unique_candidates)
        final_candidates = unique_candidates[:count]
        
        print(f"✅ Generated {len(final_candidates)} unique intelligent candidates")
        return final_candidates
    
    def analyze_candidate_quality(self, candidates: List[int]) -> Dict:
        """Analyze the quality of generated candidates"""
        if not candidates:
            return {"error": "No candidates to analyze"}
        
        analysis = {
            "total_candidates": len(candidates),
            "range": {"min": min(candidates), "max": max(candidates)},
            "modulo_distribution": {},
            "gap_analysis": {},
            "density_score": 0
        }
        
        # Modulo distribution
        mod_210_dist = {}
        for candidate in candidates:
            mod = candidate % 210
            mod_210_dist[mod] = mod_210_dist.get(mod, 0) + 1
        analysis["modulo_distribution"]["mod_210"] = mod_210_dist
        
        # Gap analysis
        gaps = []
        for i in range(1, len(candidates)):
            gap = candidates[i] - candidates[i-1]
            gaps.append(gap)
        
        if gaps:
            analysis["gap_analysis"] = {
                "mean_gap": np.mean(gaps),
                "std_gap": np.std(gaps),
                "min_gap": min(gaps),
                "max_gap": max(gaps)
            }
        
        # Density score (how well candidates match historical patterns)
        preferred_mod = self.patterns["modulo"]["preferred_mod_210"]
        preferred_count = mod_210_dist.get(preferred_mod, 0)
        analysis["density_score"] = preferred_count / len(candidates) if candidates else 0
        
        return analysis
    
    def save_pattern_analysis(self, filename: str = None):
        """Save pattern analysis to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mersenne_pattern_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.patterns, f, indent=2)
        
        print(f"💾 Pattern analysis saved to: {filename}")
        return filename

def main():
    """Main function for testing the candidate generator"""
    print("🧠 ADVANCED CANDIDATE GENERATOR TEST 🧠")
    print("=" * 50)
    
    generator = AdvancedCandidateGenerator()
    
    # Test parameters - always start after 52nd Mersenne exponent
    start = 136279843  # Start after M52
    end = 136379843    # 100,000 range for testing
    count = 1000
    
    print(f"Testing with range [{start:,}, {end:,}] and {count} candidates")
    
    # Generate candidates
    candidates = generator.generate_intelligent_candidates(start, end, count)
    
    # Analyze quality
    analysis = generator.analyze_candidate_quality(candidates)
    
    print(f"\n📊 CANDIDATE QUALITY ANALYSIS:")
    print(f"  Total candidates: {analysis['total_candidates']:,}")
    print(f"  Range: {analysis['range']['min']:,} to {analysis['range']['max']:,}")
    print(f"  Density score: {analysis['density_score']:.3f}")
    
    if 'gap_analysis' in analysis:
        gap = analysis['gap_analysis']
        print(f"  Mean gap: {gap['mean_gap']:.1f}")
        print(f"  Gap std: {gap['std_gap']:.1f}")
    
    # Save results
    generator.save_pattern_analysis()
    
    print(f"\n✅ Candidate generation test complete!")

if __name__ == "__main__":
    main()
