#!/usr/bin/env python3
import subprocess
import os
import sys
import time
import re
from io import StringIO

class GameExploit:
    def __init__(self):
        self.game_path = "./game"
        self.pot = 1000
        self.target = 1000000
        self.process = None
        
    def start_game(self):
        """Start the game process"""
        try:
            self.process = subprocess.Popen(
                [self.game_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            return True
        except Exception as e:
            print(f"Failed to start game: {e}")
            return False
    
    def send_input(self, data):
        """Send input to the game"""
        if self.process:
            try:
                self.process.stdin.write(data + '\n')
                self.process.stdin.flush()
                return True
            except Exception as e:
                print(f"Failed to send input: {e}")
                return False
        return False
    
    def read_output(self, timeout=1):
        """Read output from the game with timeout"""
        if not self.process:
            return ""
        
        output = ""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.process.poll() is not None:
                break
            try:
                # Read available output
                import select
                if select.select([self.process.stdout], [], [], 0.1)[0]:
                    line = self.process.stdout.readline()
                    if line:
                        output += line
                        print(line.strip())  # Debug output
                    else:
                        break
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error reading output: {e}")
                break
        
        return output
    
    def parse_pot_value(self, output):
        """Extract pot value from game output"""
        pot_match = re.search(r'Your pot is (\d+)', output)
        if pot_match:
            return int(pot_match.group(1))
        return self.pot
    
    def play_round(self, bet):
        """Play a single round with given bet"""
        print(f"\n=== Playing round with bet: {bet} ===")
        
        # Send bet
        if not self.send_input(str(bet)):
            return False
        
        # Read house roll
        output = self.read_output(2)
        
        # Press enter to roll
        if not self.send_input(""):
            return False
        
        # Read our roll and result
        output += self.read_output(2)
        
        # Update pot
        self.pot = self.parse_pot_value(output)
        print(f"Current pot: {self.pot}")
        
        return True
    
    def exploit_strategy_1(self):
        """Strategy 1: Conservative betting with pattern recognition"""
        print("=== Starting Strategy 1: Conservative Pattern Recognition ===")
        
        if not self.start_game():
            return False
        
        # Read initial output
        initial_output = self.read_output(2)
        print("Initial game output:")
        print(initial_output)
        
        bet = 1  # Start with minimum bet
        rounds = 0
        wins = 0
        losses = 0
        
        while self.pot > 0 and self.pot < self.target and rounds < 1000:
            rounds += 1
            
            # Adaptive betting strategy
            if self.pot < 100:
                bet = 1  # Conservative when low
            elif self.pot > 10000:
                bet = min(100, self.pot // 100)  # More aggressive when ahead
            else:
                bet = min(10, self.pot // 100)
            
            if not self.play_round(bet):
                break
            
            # Check if we won or lost based on pot change
            if rounds == 1:
                continue  # Can't compare on first round
            
            time.sleep(0.1)  # Small delay to avoid overwhelming the game
        
        print(f"\nGame ended after {rounds} rounds")
        print(f"Final pot: {self.pot}")
        
        if self.process:
            self.process.terminate()
        
        return self.pot >= self.target
    
    def exploit_strategy_2(self):
        """Strategy 2: Look for RNG predictability or buffer overflow"""
        print("=== Starting Strategy 2: RNG/Buffer Overflow Analysis ===")
        
        # Test with very large inputs to see if there's a buffer overflow
        test_inputs = [
            "A" * 100,
            "A" * 500,
            "A" * 1000,
            "9999999999999",
            "-1",
            "0",
            "%s" * 10,
            "\x00" * 50
        ]
        
        for test_input in test_inputs:
            print(f"\nTesting with input: {repr(test_input[:50])}")
            
            if not self.start_game():
                continue
            
            # Read initial output
            self.read_output(1)
            
            # Send malicious input
            self.send_input(test_input)
            
            # See what happens
            output = self.read_output(3)
            
            if self.process:
                self.process.terminate()
                self.process = None
            
            time.sleep(0.5)
    
    def exploit_strategy_3(self):
        """Strategy 3: High-frequency betting to find patterns"""
        print("=== Starting Strategy 3: High-Frequency Pattern Detection ===")
        
        if not self.start_game():
            return False
        
        # Read initial output
        self.read_output(2)
        
        # Track patterns
        house_rolls = []
        player_rolls = []
        results = []
        
        for i in range(50):  # Quick sampling
            bet = 1
            
            # Send bet
            self.send_input(str(bet))
            
            # Get house roll
            output = self.read_output(1)
            house_match = re.search(r'house rolls (\d+)', output)
            
            # Roll
            self.send_input("")
            
            # Get player roll and result
            output = self.read_output(1)
            player_match = re.search(r'You roll (\d+)', output)
            
            if house_match and player_match:
                house_roll = int(house_match.group(1))
                player_roll = int(player_match.group(1))
                
                house_rolls.append(house_roll)
                player_rolls.append(player_roll)
                
                if player_roll > house_roll:
                    results.append("win")
                elif player_roll < house_roll:
                    results.append("lose")
                else:
                    results.append("push")
                
                print(f"Round {i+1}: House={house_roll}, Player={player_roll}, Result={results[-1]}")
            
        
        # Analyze patterns
        print(f"\nPattern Analysis:")
        print(f"House rolls: {house_rolls}")
        print(f"Player rolls: {player_rolls}")
        print(f"Results: {results}")
        
        # Look for correlations
        if len(house_rolls) > 10:
            print(f"Average house roll: {sum(house_rolls)/len(house_rolls):.2f}")
            print(f"Average player roll: {sum(player_rolls)/len(player_rolls):.2f}")
            print(f"Win rate: {results.count('win')/len(results)*100:.1f}%")
        
        if self.process:
            self.process.terminate()
        
        return False

def main():
    os.chdir('/workspaces/SkillsUSA-Nats-2025/Game')
    
    exploit = GameExploit()
    
    print("Game Exploitation Tool")
    print("=====================")
    
    # Try different strategies
    strategies = [
        exploit.exploit_strategy_2,  # Check for buffer overflows first
        exploit.exploit_strategy_3,  # Pattern analysis
        exploit.exploit_strategy_1,  # Normal gameplay
    ]
    
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{'='*50}")
        print(f"Executing Strategy {i}")
        print(f"{'='*50}")
        
        try:
            success = strategy()
            if success:
                print(f"Strategy {i} succeeded!")
                break
        except Exception as e:
            print(f"Strategy {i} failed with error: {e}")
        
        time.sleep(1)  # Brief pause between strategies

if __name__ == "__main__":
    main()