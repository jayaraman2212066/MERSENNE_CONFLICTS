from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import math
import time
import threading
from datetime import datetime
import os

app = Flask(__name__)

class MersenneCalculator:
    def __init__(self):
        self.known_mersenne_primes = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
            2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
            23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
            1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
            24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
            43112609, 57885161, 74207281, 77232917, 82589933, 136279841
        ]
    
    def lucas_lehmer_test(self, p, time_budget_seconds=8.0):
        if p == 2: return True
        if p < 2: return False
        
        start = time.time()
        s = 4
        M = (1 << p) - 1
        
        for _ in range(p - 2):
            s = (s * s - 2) % M
            if time_budget_seconds and (time.time() - start) > time_budget_seconds:
                raise TimeoutError("Lucas-Lehmer timed out")
        
        return s == 0
    
    def test_mersenne_number(self, p, time_budget_seconds=8.0):
        start_time = time.time()
        
        if p <= 0:
            return {"valid": False, "error": "Exponent must be positive"}
        
        try:
            M = (1 << p) - 1
            is_prime = self.lucas_lehmer_test(p, time_budget_seconds)
            end_time = time.time()
            
            return {
                "valid": True,
                "exponent": p,
                "mersenne_number": str(M),
                "is_prime": is_prime,
                "computation_time": round(end_time - start_time, 4),
                "digits": len(str(M))
            }
        except TimeoutError:
            return {"valid": False, "error": "Computation timed out — try a smaller exponent"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def analyze_patterns(self):
        if len(self.known_mersenne_primes) < 2:
            return {"error": "Not enough data for analysis"}
        
        gaps = []
        for i in range(1, len(self.known_mersenne_primes)):
            gap = self.known_mersenne_primes[i] - self.known_mersenne_primes[i-1]
            gaps.append(gap)
        
        return {
            "total_known": len(self.known_mersenne_primes),
            "largest_known": max(self.known_mersenne_primes),
            "average_gap": sum(gaps) / len(gaps) if gaps else 0,
            "min_gap": min(gaps) if gaps else 0,
            "max_gap": max(gaps) if gaps else 0,
            "gaps": gaps[:10]
        }

calculator = MersenneCalculator()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        return "<h1>MERSENNE Project</h1><p>Revolutionary Mathematical Discovery System</p>"

@app.route('/api/test_mersenne', methods=['POST'])
def test_mersenne():
    try:
        data = request.get_json()
        exponent = int(data.get('exponent', 0))
        result = calculator.test_mersenne_number(exponent)
        return jsonify(result)
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})

@app.route('/api/patterns')
def get_patterns():
    return jsonify(calculator.analyze_patterns())

@app.route('/api/status')
def status():
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "calculator_ready": True,
        "known_mersenne_count": len(calculator.known_mersenne_primes)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)