#!/usr/bin/env python3
"""
Performance Testing Script for bobmarley AI Assistant
Tests response times, memory usage, and system performance
"""

import requests
import time
import statistics
import psutil
import json
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

def test_response_times(num_tests=10):
    """Test LLM response times"""
    print("\n" + "="*60)
    print("🚀 RESPONSE TIME BENCHMARK")
    print("="*60)
    
    test_queries = [
        ("Simple", "Hello"),
        ("Medium", "Tell me a joke"),
        ("Complex", "Explain artificial intelligence"),
    ]
    
    results = {}
    
    for query_type, query in test_queries:
        print(f"\n📝 Testing {query_type} Query: '{query}'")
        times = []
        
        for i in range(num_tests):
            start = time.time()
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat_stream",
                    json={
                        "message": query,
                        "personality": "Friendly",
                        "language": "English",
                        "temperature": 0.7
                    },
                    stream=True,
                    timeout=30
                )
                
                # Read full response
                full_response = ""
                for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                    if chunk:
                        full_response += chunk.decode('utf-8') if isinstance(chunk, bytes) else chunk
                
                elapsed = time.time() - start
                times.append(elapsed)
                
                status = "✅" if elapsed < 5 else "⚠️"
                print(f"  {status} Test {i+1}: {elapsed:.2f}s")
                
            except Exception as e:
                print(f"  ❌ Test {i+1}: Failed - {str(e)}")
        
        if times:
            results[query_type] = {
                "average": statistics.mean(times),
                "median": statistics.median(times),
                "min": min(times),
                "max": max(times),
                "stdev": statistics.stdev(times) if len(times) > 1 else 0
            }
            
            print(f"\n  📊 {query_type} Query Statistics:")
            print(f"     Average: {results[query_type]['average']:.2f}s")
            print(f"     Median:  {results[query_type]['median']:.2f}s")
            print(f"     Min:     {results[query_type]['min']:.2f}s")
            print(f"     Max:     {results[query_type]['max']:.2f}s")
            print(f"     StdDev:  {results[query_type]['stdev']:.2f}s")
    
    return results

def test_system_resources():
    """Monitor system resource usage"""
    print("\n" + "="*60)
    print("💻 SYSTEM RESOURCE USAGE")
    print("="*60)
    
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    print(f"\n🔥 CPU:")
    print(f"   Usage: {cpu_percent}%")
    print(f"   Cores: {cpu_count}")
    print(f"   Status: {'✅ Good' if cpu_percent < 70 else '⚠️ High'}")
    
    # Memory Usage
    memory = psutil.virtual_memory()
    memory_gb = memory.used / (1024**3)
    memory_total_gb = memory.total / (1024**3)
    print(f"\n💾 RAM:")
    print(f"   Used: {memory_gb:.2f} GB / {memory_total_gb:.2f} GB")
    print(f"   Percent: {memory.percent}%")
    print(f"   Available: {memory.available / (1024**3):.2f} GB")
    print(f"   Status: {'✅ Good' if memory.percent < 80 else '⚠️ High'}")
    
    # Disk Usage
    disk = psutil.disk_usage('/')
    disk_gb = disk.used / (1024**3)
    disk_total_gb = disk.total / (1024**3)
    print(f"\n💿 Disk:")
    print(f"   Used: {disk_gb:.2f} GB / {disk_total_gb:.2f} GB")
    print(f"   Percent: {disk.percent}%")
    print(f"   Free: {disk.free / (1024**3):.2f} GB")
    print(f"   Status: {'✅ Good' if disk.percent < 90 else '⚠️ High'}")
    
    # Network
    net_io = psutil.net_io_counters()
    print(f"\n🌐 Network:")
    print(f"   Sent: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"   Received: {net_io.bytes_recv / (1024**2):.2f} MB")
    
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_used_gb": memory_gb,
        "disk_percent": disk.percent,
        "disk_used_gb": disk_gb
    }

def test_concurrent_requests(num_concurrent=5):
    """Test handling of concurrent requests"""
    print("\n" + "="*60)
    print("⚡ CONCURRENT REQUEST TEST")
    print("="*60)
    
    import concurrent.futures
    
    def make_request(i):
        start = time.time()
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat_stream",
                json={
                    "message": f"Test {i}",
                    "personality": "Friendly",
                    "language": "English"
                },
                stream=True,
                timeout=30
            )
            
            for chunk in response.iter_content(chunk_size=1024):
                pass
            
            elapsed = time.time() - start
            return {"success": True, "time": elapsed, "id": i}
        except Exception as e:
            return {"success": False, "error": str(e), "id": i}
    
    print(f"\n🔄 Sending {num_concurrent} concurrent requests...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_concurrent)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"\n📊 Results:")
    print(f"   Successful: {len(successful)}/{num_concurrent}")
    print(f"   Failed: {len(failed)}/{num_concurrent}")
    
    if successful:
        times = [r["time"] for r in successful]
        print(f"   Average time: {statistics.mean(times):.2f}s")
        print(f"   Max time: {max(times):.2f}s")
    
    if failed:
        print(f"\n❌ Failed requests:")
        for r in failed:
            print(f"   Request {r['id']}: {r.get('error', 'Unknown error')}")
    
    return {
        "total": num_concurrent,
        "successful": len(successful),
        "failed": len(failed),
        "success_rate": len(successful) / num_concurrent * 100
    }

def generate_report(response_results, resource_results, concurrent_results):
    """Generate final test report"""
    print("\n" + "="*60)
    print("📋 FINAL TEST REPORT")
    print("="*60)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n⏰ Test Date: {timestamp}")
    print(f"\n🎯 Overall Status: ", end="")
    
    # Determine overall status
    all_good = True
    
    # Check response times
    if response_results:
        for query_type, stats in response_results.items():
            if stats["average"] > 10:
                all_good = False
    
    # Check resources
    if resource_results["cpu_percent"] > 80 or resource_results["memory_percent"] > 90:
        all_good = False
    
    # Check concurrent
    if concurrent_results["success_rate"] < 80:
        all_good = False
    
    if all_good:
        print("✅ PASS - All tests passed!")
    else:
        print("⚠️ WARNING - Some tests need attention")
    
    print("\n📊 Summary:")
    print(f"   Response Time: {'✅ Good' if all(r['average'] < 10 for r in response_results.values()) else '⚠️ Slow'}")
    print(f"   CPU Usage: {'✅ Good' if resource_results['cpu_percent'] < 70 else '⚠️ High'}")
    print(f"   Memory Usage: {'✅ Good' if resource_results['memory_percent'] < 80 else '⚠️ High'}")
    print(f"   Concurrent Handling: {'✅ Good' if concurrent_results['success_rate'] > 80 else '⚠️ Poor'}")
    
    # Save report to file
    report = {
        "timestamp": timestamp,
        "response_times": response_results,
        "system_resources": resource_results,
        "concurrent_test": concurrent_results,
        "overall_status": "PASS" if all_good else "WARNING"
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Report saved to: test_report.json")

def main():
    """Main test execution"""
    print("\n" + "="*60)
    print("🧪 bobmarley AI Assistant - Performance Test Suite")
    print("="*60)
    
    # Check backend
    print("\n🔍 Checking backend status...")
    if not check_backend_health():
        print("❌ Backend is not running!")
        print("   Please start the backend with Leo.bat")
        return
    
    print("✅ Backend is online")
    
    # Run tests
    try:
        response_results = test_response_times(num_tests=5)
        resource_results = test_system_resources()
        concurrent_results = test_concurrent_requests(num_concurrent=3)
        
        # Generate report
        generate_report(response_results, resource_results, concurrent_results)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ Testing complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
