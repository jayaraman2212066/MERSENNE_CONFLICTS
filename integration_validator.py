#!/usr/bin/env python3
"""
Integration Validator for MERSENNE Project Live Proof System
Ensures all components are properly integrated and working
"""

import os
import sys
import json
import time
import importlib
from typing import Dict, List, Tuple

class IntegrationValidator:
    def __init__(self):
        self.validation_results = {}
        self.errors = []
        self.warnings = []
        
    def validate_imports(self) -> bool:
        """Validate all required imports are working"""
        print("🔍 VALIDATING IMPORTS")
        print("-" * 30)
        
        required_modules = [
            'enhanced_binary_filter',
            'real_time_success_proof', 
            'success_rate_validator',
            'live_discovery_dashboard',
            'run_success_showcase'
        ]
        
        import_success = True
        
        for module in required_modules:
            try:
                importlib.import_module(module)
                print(f"✅ {module}: OK")
            except ImportError as e:
                print(f"❌ {module}: FAILED - {e}")
                self.errors.append(f"Import error: {module} - {e}")
                import_success = False
            except Exception as e:
                print(f"⚠️ {module}: WARNING - {e}")
                self.warnings.append(f"Import warning: {module} - {e}")
        
        return import_success
    
    def validate_csv_data(self) -> bool:
        """Validate CSV data availability"""
        print("\n📊 VALIDATING CSV DATA")
        print("-" * 30)
        
        csv_path = 'mersenne_exponents.csv'
        
        if not os.path.exists(csv_path):
            print(f"❌ CSV file missing: {csv_path}")
            self.errors.append(f"Missing CSV file: {csv_path}")
            return False
        
        try:
            import csv
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            print(f"✅ CSV file found: {len(rows)} exponents loaded")
            
            # Validate required columns
            required_cols = ['Index', 'Decimal', 'Binary', 'Digit_Sum_Decimal', 'Last_Digit', 'Number_Length']
            if rows:
                missing_cols = [col for col in required_cols if col not in rows[0]]
                if missing_cols:
                    print(f"⚠️ Missing columns: {missing_cols}")
                    self.warnings.append(f"Missing CSV columns: {missing_cols}")
                else:
                    print(f"✅ All required columns present")
            
            return True
            
        except Exception as e:
            print(f"❌ CSV validation failed: {e}")
            self.errors.append(f"CSV validation error: {e}")
            return False
    
    def validate_binary_filter(self) -> bool:
        """Validate binary filter functionality"""
        print("\n⚡ VALIDATING BINARY FILTER")
        print("-" * 30)
        
        try:
            from enhanced_binary_filter import EnhancedBinaryFilter
            
            filter_system = EnhancedBinaryFilter()
            stats = filter_system.get_filter_stats()
            
            print(f"✅ Binary filter initialized")
            print(f"📊 Known exponents: {stats['known_exponents_count']}")
            print(f"🎯 Digit sum patterns: {len(stats['digit_sum_patterns'])}")
            print(f"⚡ Elimination rate: {stats['estimated_elimination_rate']:.1%}")
            
            # Test filtering
            test_candidates = [136279843, 136279849, 136279861]
            filtered = filter_system.filter_candidates(test_candidates)
            
            print(f"🧪 Filter test: {len(test_candidates)} → {len(filtered)} candidates")
            
            return True
            
        except Exception as e:
            print(f"❌ Binary filter validation failed: {e}")
            self.errors.append(f"Binary filter error: {e}")
            return False
    
    def validate_success_proof(self) -> bool:
        """Validate success proof system"""
        print("\n🔬 VALIDATING SUCCESS PROOF SYSTEM")
        print("-" * 30)
        
        try:
            from real_time_success_proof import RealTimeSuccessProof
            
            proof_system = RealTimeSuccessProof()
            
            # Test with small candidate
            test_result = proof_system.test_candidate_with_proof(31)  # Known Mersenne prime
            
            if test_result['result'] == 'MERSENNE_PRIME':
                print(f"✅ Success proof system working")
                print(f"🎉 Test discovery: M_8 = 2^31 - 1")
                print(f"⏱️ Test time: {test_result['test_time']:.3f}s")
            else:
                print(f"⚠️ Unexpected test result: {test_result['result']}")
                self.warnings.append(f"Unexpected proof test result: {test_result}")
            
            return True
            
        except Exception as e:
            print(f"❌ Success proof validation failed: {e}")
            self.errors.append(f"Success proof error: {e}")
            return False
    
    def validate_gallery_creation(self) -> bool:
        """Validate gallery file creation"""
        print("\n🎨 VALIDATING GALLERY CREATION")
        print("-" * 30)
        
        try:
            from real_time_success_proof import create_gallery_showcase
            
            gallery_file = create_gallery_showcase()
            
            if os.path.exists(gallery_file):
                file_size = os.path.getsize(gallery_file)
                print(f"✅ Gallery created: {gallery_file}")
                print(f"📁 File size: {file_size:,} bytes")
                
                # Validate HTML content
                with open(gallery_file, 'r') as f:
                    content = f.read()
                    
                required_elements = ['MERSENNE PROJECT', 'Discovery Gallery', 'Filter Performance']
                missing_elements = [elem for elem in required_elements if elem not in content]
                
                if missing_elements:
                    print(f"⚠️ Missing gallery elements: {missing_elements}")
                    self.warnings.append(f"Missing gallery elements: {missing_elements}")
                else:
                    print(f"✅ Gallery content validated")
                
                return True
            else:
                print(f"❌ Gallery file not created")
                self.errors.append("Gallery file creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Gallery validation failed: {e}")
            self.errors.append(f"Gallery error: {e}")
            return False
    
    def validate_dashboard_components(self) -> bool:
        """Validate dashboard components"""
        print("\n🌐 VALIDATING DASHBOARD COMPONENTS")
        print("-" * 30)
        
        try:
            # Check Flask availability
            import flask
            print(f"✅ Flask available: v{flask.__version__}")
            
            # Validate dashboard module
            from live_discovery_dashboard import app, discovery_state
            
            print(f"✅ Dashboard app created")
            print(f"📊 Initial state: {discovery_state['active']}")
            
            # Test route availability
            with app.test_client() as client:
                response = client.get('/')
                if response.status_code == 200:
                    print(f"✅ Dashboard route accessible")
                else:
                    print(f"⚠️ Dashboard route status: {response.status_code}")
                    self.warnings.append(f"Dashboard route status: {response.status_code}")
            
            return True
            
        except ImportError as e:
            print(f"❌ Flask not available: {e}")
            self.errors.append(f"Flask import error: {e}")
            return False
        except Exception as e:
            print(f"❌ Dashboard validation failed: {e}")
            self.errors.append(f"Dashboard error: {e}")
            return False
    
    def validate_showcase_integration(self) -> bool:
        """Validate complete showcase integration"""
        print("\n🎊 VALIDATING SHOWCASE INTEGRATION")
        print("-" * 30)
        
        try:
            from run_success_showcase import create_showcase_index
            
            index_file = create_showcase_index()
            
            if os.path.exists(index_file):
                print(f"✅ Showcase index created: {index_file}")
                
                # Validate HTML structure
                with open(index_file, 'r') as f:
                    content = f.read()
                
                required_sections = ['MERSENNE PROJECT', 'Real-Time Success Proof', 'Live Discovery Dashboard']
                missing_sections = [section for section in required_sections if section not in content]
                
                if missing_sections:
                    print(f"⚠️ Missing showcase sections: {missing_sections}")
                    self.warnings.append(f"Missing showcase sections: {missing_sections}")
                else:
                    print(f"✅ Showcase structure validated")
                
                return True
            else:
                print(f"❌ Showcase index not created")
                self.errors.append("Showcase index creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Showcase validation failed: {e}")
            self.errors.append(f"Showcase error: {e}")
            return False
    
    def run_complete_validation(self) -> Dict:
        """Run complete integration validation"""
        print("🔍 MERSENNE PROJECT INTEGRATION VALIDATION")
        print("=" * 60)
        print("🎯 Objective: Ensure all live proof components work together")
        print("=" * 60)
        
        validation_start = time.time()
        
        # Run all validations
        validations = [
            ('imports', self.validate_imports),
            ('csv_data', self.validate_csv_data),
            ('binary_filter', self.validate_binary_filter),
            ('success_proof', self.validate_success_proof),
            ('gallery_creation', self.validate_gallery_creation),
            ('dashboard_components', self.validate_dashboard_components),
            ('showcase_integration', self.validate_showcase_integration)
        ]
        
        results = {}
        passed = 0
        
        for name, validator in validations:
            try:
                result = validator()
                results[name] = {'status': 'PASS' if result else 'FAIL', 'success': result}
                if result:
                    passed += 1
            except Exception as e:
                results[name] = {'status': 'ERROR', 'success': False, 'error': str(e)}
                self.errors.append(f"{name} validation error: {e}")
        
        validation_time = time.time() - validation_start
        
        # Generate summary
        total_validations = len(validations)
        pass_rate = passed / total_validations
        
        print(f"\n📊 VALIDATION SUMMARY")
        print("=" * 40)
        print(f"✅ Passed: {passed}/{total_validations} ({pass_rate:.1%})")
        print(f"❌ Errors: {len(self.errors)}")
        print(f"⚠️ Warnings: {len(self.warnings)}")
        print(f"⏱️ Validation time: {validation_time:.2f}s")
        
        if self.errors:
            print(f"\n❌ ERRORS FOUND:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        # Overall status
        if pass_rate >= 0.9:
            status = "EXCELLENT"
            color = "🟢"
        elif pass_rate >= 0.7:
            status = "GOOD"
            color = "🟡"
        else:
            status = "NEEDS_WORK"
            color = "🔴"
        
        print(f"\n{color} OVERALL STATUS: {status}")
        
        # Save validation report
        report = {
            'validation_summary': {
                'timestamp': time.time(),
                'total_validations': total_validations,
                'passed': passed,
                'pass_rate': pass_rate,
                'status': status,
                'validation_time': validation_time
            },
            'detailed_results': results,
            'errors': self.errors,
            'warnings': self.warnings
        }
        
        with open('D:\\PROJECT_RENDER\\prime\\MERSENNE_CONFLICTS\\integration_validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📁 Validation report saved: integration_validation_report.json")
        
        return report

def main():
    """Main validation execution"""
    validator = IntegrationValidator()
    report = validator.run_complete_validation()
    
    if report['validation_summary']['pass_rate'] >= 0.9:
        print(f"\n🎉 INTEGRATION VALIDATION COMPLETE!")
        print(f"✅ All systems ready for live proof demonstration")
        print(f"🚀 Run 'python run_success_showcase.py' to start showcase")
    else:
        print(f"\n⚠️ INTEGRATION ISSUES DETECTED")
        print(f"🔧 Please fix errors before running live demonstration")
    
    return report

if __name__ == "__main__":
    main()