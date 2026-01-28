import unittest
from unittest.mock import MagicMock, patch
import json
import os
import sys
import time
import logging

# Add current directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interaction_process import InteractionProcess
import shared_state

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BrutalStressTest")

class BrutalStressTestRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the brutal test data
        data_path = os.path.join(os.path.dirname(__file__), 'brutal_stress_test_data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            cls.test_cases = json.load(f)
        
        # Mock dependencies
        cls.audio_queue = MagicMock()
        cls.motor_queue = MagicMock()
        cls.shutdown_flag = MagicMock()
        cls.audio_playing_flag = MagicMock()
        cls.audio_feedback_queue = MagicMock()
        
        # Patch external libraries before initialization
        with patch('speech_recognition.Recognizer'), \
             patch('speech_recognition.Microphone'), \
             patch('pyttsx3.init'), \
             patch('gtts.gTTS'):
            
            # Initialize InteractionProcess
            # Dummy API key for safety
            os.environ['GROQ_API_KEY'] = 'test_key'
            # Mock the methods that touch the filesystem in __init__
            with patch('interaction_process.InteractionProcess.initialize_conversation_log'):
                cls.ip = InteractionProcess(
                    cls.audio_queue, 
                    cls.motor_queue, 
                    cls.shutdown_flag, 
                    cls.audio_playing_flag,
                    cls.audio_feedback_queue
                )

    def test_brutal_scenarios(self):
        results = []
        pass_count = 0
        fail_count = 0

        for case in self.test_cases:
            utterance = case['input']
            noise = case['noise']
            expected_tier = case['expected_tier']
            category = case['category']

            logger.info(f"Testing: '{utterance}' | Noise: {noise} | Expected: {expected_tier}")

            # Mock NLU routing logic simulation
            # In a real test, we would call self.ip.process_command(utterance)
            # But here we want to simulate the response and tiered logic
            
            with patch('interaction_process.InteractionProcess.query_llama') as mock_llama:
                mock_llama.return_value = "This is a generative response."
                
                # REAL NLU ROUTING LOGIC
                is_medical = self.ip.is_medical_query(utterance)
                
                if is_medical:
                    actual_tier = "Medical Safety"
                else:
                    # Check for Tier 1 (FAQ) or Tier 2 (Department) in all supported languages
                    tier_found = "Tier 3"
                    for lang in ['en', 'hi', 'te']:
                        if self.ip.find_department(utterance, lang):
                            tier_found = "Tier 2"
                            break
                        if self.ip.find_faq(utterance, lang):
                            tier_found = "Tier 1"
                            break
                    actual_tier = tier_found

                status = "PASS" if actual_tier == expected_tier else "FAIL"
                if status == "PASS": pass_count += 1
                else: fail_count += 1

                results.append({
                    "input": utterance,
                    "noise": noise,
                    "expected_tier": expected_tier,
                    "actual_tier": actual_tier,
                    "status": status,
                    "category": category
                })

        # Save Stress Test Results
        report_path = os.path.join(os.path.dirname(__file__), 'STRESS_TEST_RESULTS.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": {
                    "total": len(self.test_cases),
                    "passed": pass_count,
                    "failed": fail_count,
                    "pass_percentage": (pass_count / len(self.test_cases)) * 100
                },
                "results": results
            }, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Brutal Stress Test Complete. Pass Rate: {(pass_count / len(self.test_cases)) * 100:.2f}%")

if __name__ == "__main__":
    unittest.main()
