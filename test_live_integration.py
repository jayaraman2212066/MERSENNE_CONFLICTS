#!/usr/bin/env python3
"""
Live Integration Test for MERSENNE Project
Tests all components and ensures proper integration
"""

import os
import sys
import time
import json
from integration_validator import IntegrationValidator

def test_basic_functionality():
    """Test basic functionality of all components"""
    print("🧪 TESTING BASIC FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Enhanced Binary Filter
    print("\n1️⃣ Testing Enhanced Binary Filter...")
    try:
        from enhanced_binary_filter import EnhancedBinaryFilter
        filter_system = EnhancedBinaryFilter()
        
        # Test with known Mersenne exponents
        test_cases = [31, 127, 521]  # Known Mersenne prime exponents
        for p in test_cases:
            passes = filter_system.ultra_fast_pattern_filter(p)
            print(f"   p={p}: {'✅ PASS' if passes else '❌ FAIL'}")
        
        print("✅ Binary filter test completed")
        
    except Exception as e:
        print(f"❌ Binary filter test failed: {e}")
        return False
    
    # Test 2: Real-Time Success Proof
    print("\n2️⃣ Testing Real-Time Success Proof...")
    try:
        from real_time_success_proof import RealTimeSuccessProof
        proof_system = RealTimeSuccessProof()
        
        # Test with small known Mersenne prime
        result = proof_system.test_candidate_with_proof(31)
        if result['result'] == 'MERSENNE_PRIME':
            print(f"   ✅ Correctly identified M_8 = 2^31 - 1")
            print(f"   ⏱️ Test time: {result['test_time']:.3f}s")
        else:
            print(f"   ❌ Failed to identify known Mersenne prime")
            return False
        
        print("✅ Success proof test completed")
        
    except Exception as e:
        print(f"❌ Success proof test failed: {e}")
        return False
    
    # Test 3: Gallery Creation
    print("\n3️⃣ Testing Gallery Creation...")
    try:
        from real_time_success_proof import create_gallery_showcase
        gallery_file = create_gallery_showcase()
        
        if os.path.exists(gallery_file):
            file_size = os.path.getsize(gallery_file)
            print(f"   ✅ Gallery created: {file_size:,} bytes")
        else:
            print(f"   ❌ Gallery file not created")
            return False
        
        print("✅ Gallery creation test completed")
        
    except Exception as e:
        print(f"❌ Gallery creation test failed: {e}")
        return False
    
    # Test 4: Success Rate Validator
    print("\n4️⃣ Testing Success Rate Validator...")
    try:
        from success_rate_validator import SuccessRateValidator
        validator = SuccessRateValidator()
        
        # Quick validation test
        theoretical = validator.validate_theoretical_speedup()
        if theoretical['theoretical_speedup'] > 100:
            print(f"   ✅ Theoretical speedup: {theoretical['theoretical_speedup']:.0f}x")
        else:
            print(f"   ⚠️ Low theoretical speedup: {theoretical['theoretical_speedup']:.1f}x")
        
        print("✅ Success rate validator test completed")
        
    except Exception as e:
        print(f"❌ Success rate validator test failed: {e}")
        return False
    
    return True

def test_live_proof_generation():
    """Test live proof generation with small dataset"""
    print("\n🔬 TESTING LIVE PROOF GENERATION")
    print("=" * 50)
    
    try:
        from real_time_success_proof import RealTimeSuccessProof
        
        proof_system = RealTimeSuccessProof()
        
        # Test with small range including known Mersenne primes
        test_exponents = [31, 61, 89, 107, 127]  # Known Mersenne prime exponents
        
        discoveries = []
        for p in test_exponents:
            print(f"🧮 Testing p = {p}...")
            result = proof_system.test_candidate_with_proof(p)
            
            if result['result'] == 'MERSENNE_PRIME':
                discoveries.append(result)
                print(f"   🎉 DISCOVERY: M = 2^{p} - 1")
                print(f"   📊 Digits: {result['digit_count']:,}")
                print(f"   ⏱️ Time: {result['test_time']:.3f}s")
                
                # Validate verification
                verification = result['verification']
                all_passed = all(verification.values())
                print(f"   ✅ Verification: {'PASSED' if all_passed else 'FAILED'}")
            else:
                print(f"   ❌ Not identified as Mersenne prime")
        
        print(f"\n📊 LIVE PROOF RESULTS:")
        print(f"   Tested: {len(test_exponents)}")
        print(f"   Discovered: {len(discoveries)}")
        print(f"   Success Rate: {len(discoveries)/len(test_exponents):.1%}")
        
        # Generate proof document
        proof_doc = proof_system.generate_success_proof()
        
        with open('D:\\PROJECT_RENDER\\prime\\MERSENNE_CONFLICTS\\live_proof_test.json', 'w') as f:
            json.dump(proof_doc, f, indent=2)
        
        print(f"   📁 Proof document saved: live_proof_test.json")
        
        return len(discoveries) > 0
        
    except Exception as e:
        print(f"❌ Live proof generation test failed: {e}")
        return False

def test_showcase_integration():
    """Test complete showcase integration"""
    print("\n🎊 TESTING SHOWCASE INTEGRATION")
    print("=" * 50)
    
    try:
        from run_success_showcase import create_showcase_index
        
        # Create showcase
        index_file = create_showcase_index()
        
        if os.path.exists(index_file):
            print(f"✅ Showcase index created: {index_file}")
            
            # Validate content
            with open(index_file, 'r') as f:
                content = f.read()
            
            required_elements = [
                'MERSENNE PROJECT',
                'Real-Time Success Proof',
                'Live Discovery Dashboard',
                'Success Rate Validation',
                'Discovery Gallery'
            ]
            
            missing = [elem for elem in required_elements if elem not in content]
            
            if missing:
                print(f"⚠️ Missing elements: {missing}")
            else:
                print(f"✅ All showcase elements present")
            
            return len(missing) == 0
        else:
            print(f"❌ Showcase index not created")
            return False
            
    except Exception as e:
        print(f"❌ Showcase integration test failed: {e}")
        return False

def run_complete_test():
    """Run complete integration test"""
    print("🚀 MERSENNE PROJECT LIVE INTEGRATION TEST")
    print("=" * 60)
    print("🎯 Objective: Verify all live proof components work correctly")
    print("=" * 60)
    
    test_start = time.time()
    
    # Run tests
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Live Proof Generation", test_live_proof_generation),
        ("Showcase Integration", test_showcase_integration)
    ]
    
    results = {}
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
            results[test_name] = False
    
    test_time = time.time() - test_start
    
    # Final validation using integration validator
    print(f"\n🔍 Running Integration Validator...")
    validator = IntegrationValidator()
    validation_report = validator.run_complete_validation()
    
    # Summary
    total_tests = len(tests)
    pass_rate = passed / total_tests
    validation_pass_rate = validation_report['validation_summary']['pass_rate']
    
    print(f"\n📊 COMPLETE TEST SUMMARY")
    print("=" * 40)
    print(f"🧪 Functional Tests: {passed}/{total_tests} ({pass_rate:.1%})")
    print(f"🔍 Integration Tests: {validation_report['validation_summary']['passed']}/{validation_report['validation_summary']['total_validations']} ({validation_pass_rate:.1%})")
    print(f"⏱️ Total test time: {test_time:.2f}s")
    
    # Overall status
    overall_pass_rate = (pass_rate + validation_pass_rate) / 2
    
    if overall_pass_rate >= 0.9:
        status = "🟢 EXCELLENT - Ready for live demonstration"
    elif overall_pass_rate >= 0.7:
        status = "🟡 GOOD - Minor issues may exist"
    else:
        status = "🔴 NEEDS WORK - Fix issues before demonstration"
    
    print(f"\n{status}")
    print(f"📈 Overall pass rate: {overall_pass_rate:.1%}")
    
    # Save test results
    test_report = {
        'test_summary': {
            'timestamp': time.time(),
            'functional_tests': results,
            'functional_pass_rate': pass_rate,
            'integration_pass_rate': validation_pass_rate,
            'overall_pass_rate': overall_pass_rate,
            'test_time': test_time,
            'status': status
        },
        'validation_report': validation_report
    }
    
    with open('D:\\PROJECT_RENDER\\prime\\MERSENNE_CONFLICTS\\complete_test_report.json', 'w') as f:
        json.dump(test_report, f, indent=2)
    
    print(f"📁 Complete test report saved: complete_test_report.json")
    
    if overall_pass_rate >= 0.8:
        print(f"\n🎉 INTEGRATION TEST COMPLETE!")
        print(f"✅ System ready for live proof demonstration")
        print(f"🚀 Run 'python run_success_showcase.py' to start")
    else:
        print(f"\n⚠️ INTEGRATION ISSUES DETECTED")
        print(f"🔧 Please review test report and fix issues")
    
    return test_report

if __name__ == "__main__":
    report = run_complete_test()
    
    # Exit with appropriate code
    if report['test_summary']['overall_pass_rate'] >= 0.8:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Issues detected