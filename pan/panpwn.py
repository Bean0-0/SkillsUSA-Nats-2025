#!/usr/bin/env python3
import subprocess
import sys
import time
from pwn import *

# Enable debugging
context.log_level = 'info'

def test_number(number, use_remote=False):
    """
    Test a number against the pickanumber binary or remote server
    Returns: 
        -1 if number is too low
        1 if number is too high
        0 if number is correct (and prints the flag)
    """
    if use_remote:
        try:
            # Connect to remote server
            conn = remote('vacr.io', 5277)
            
            # Wait for prompt and send number
            conn.recvuntil(b':')
            conn.sendline(str(number).encode())
            
            # Get response
            response = conn.recvall(timeout=3).decode()
            
            # Close connection
            conn.close()
            
            # Process response
            if "Too low" in response:
                return -1
            elif "Too high" in response:
                return 1
            else:
                print(f"Got interesting response: {response}")
                return 0
                
        except Exception as e:
            log.error(f"Error with remote connection: {e}")
            time.sleep(1)  # Add delay to avoid overwhelming the server
            return -2  # Error value
    else:
        # Use local binary
        try:
            # Run the pickanumber binary with the number as input
            process = subprocess.run(
                ["./pickanumber"], 
                input=f"{number}\n".encode(), 
                capture_output=True,
                timeout=2
            )
            
            stdout = process.stdout.decode()
            stderr = process.stderr.decode()
            exit_code = process.returncode
            
            log.info(f"Exit code: {exit_code}")
            log.info(f"Output: {stdout}")
            
            # Process based on exit code - we observed code 9 for too low, 10 for too high
            if exit_code == 9:  # Too low
                return -1
            elif exit_code == 10:  # Too high  
                return 1
            else:
                # If exit code is neither 9 nor 10, we might have found the answer
                log.success(f"Got exit code {exit_code}, checking output...")
                if stdout:
                    log.success(f"Output: {stdout}")
                if stderr:
                    log.success(f"Error: {stderr}")
                return 0
                
        except subprocess.TimeoutExpired:
            log.error(f"Process timed out at number {number}")
            return -2  # Error value
        except Exception as e:
            log.error(f"Error running process: {e}")
            return -2  # Error value

def main():
    # Check if we should use local or remote
    use_remote = True
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        use_remote = False
        log.info("Using local binary")
    else:
        log.info("Using remote server")
    
    # Initialize binary search parameters
    low = 1
    high = 10000000
    
    while low <= high:
        # Calculate the middle value
        mid = (low + high) // 2
        log.info(f"Trying number: {mid} (range: [{low}, {high}])")
        
        # Test the number
        result = test_number(mid, use_remote)
        
        # Process the result
        if result == -1:  # Too low
            low = mid + 1
            log.info(f"Too low, adjusting range: [{low}, {high}]")
        elif result == 1:  # Too high
            high = mid - 1
            log.info(f"Too high, adjusting range: [{low}, {high}]")
        elif result == 0:  # Correct
            log.success(f"Found it! Number is {mid}")
            break
        else:  # Error
            log.warning(f"Error occurred, retrying with same number")
            time.sleep(1)  # Add delay before retrying
    
    log.info(f"Final answer: {low}")

if __name__ == "__main__":
    main()