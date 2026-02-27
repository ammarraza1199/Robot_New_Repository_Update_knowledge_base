
import logging

# Mock Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockShutdownFlag:
    def __init__(self):
        self._set = False
    def set(self):
        self._set = True
    def is_set(self):
        return self._set

class MockInteraction:
    def __init__(self):
        self.EXIT_COMMANDS = {
            "en": ["exit now", "quit application", "stop interaction", "end conversation", "bye", "stop"],
            "hi": ["baat khatam", "band karo", "ab nahi", "ruko", "vida"], # Standardized
            "te": ["sare chalu", "aapandi", "inka vaddu", "aapu", "vaddu"]
        }
        self.shutdown_flag = MockShutdownFlag()

    def process_command_mock(self, command, lang):
        # Robust Exit Logic Copy
        is_exit = False
        for lang_code, phrases in self.EXIT_COMMANDS.items():
            if any(cmd in command for cmd in phrases):
                is_exit = True
                print(f"   -> Exit Triggered! (Matched '{lang_code}')")
                break
        
        if is_exit:
            self.shutdown_flag.set()
            return "Goodbye!"
        return "Normal Response"

    def is_medical_query(self, text):
        # Expanded List Copy
        medical_keywords = [
            "what is", "symptoms of", "causes of", "treatment for", "diagnose", "medicine for", "pain in", "cure for", "heal",
            "kya hai", "lakshan", "ilaaj", "upchar", "chikitsa", "dawa", "dard", "taklif", "bimari", "rog",
            "noppi", "mandhu", "nivarana", "samasya", "baadha", "rogam", "jabbulu", "chikitsa"
        ]
        return any(keyword in text for keyword in medical_keywords)

def run_test():
    bot = MockInteraction()
    print("--- Verifying Robust Features ---")
    
    # EXIT TESTS
    print("\n[Exit Command Tests]")
    exit_tests = [
        ("stop interaction", "en", "English -> English"),
        ("ruko", "en", "Hindi Command -> Detected as English"),
        ("aapandi", "hi", "Telugu Command -> Detected as Hindi")
    ]
    
    for cmd, lang, desc in exit_tests:
        bot.shutdown_flag = MockShutdownFlag() # Reset
        print(f"Test: '{cmd}' | Lang: '{lang}' ({desc})")
        resp = bot.process_command_mock(cmd, lang)
        
        if bot.shutdown_flag.is_set():
            print("RESULT: PASSED (Shutdown Triggered)")
        else:
            print("RESULT: FAILED (Shutdown NOT Triggered)")

    # MEDICAL TESTS
    print("\n[Medical Query Tests]")
    med_tests = [
        ("what is cancer", "en", "Standard English"),
        ("cancer ka upchar kya hai", "en", "Hindi (upchar) -> Detected as English"),
        ("cancer ki chikitsa", "te", "Hindi (chikitsa) -> Detected as Telugu"),
        ("naku noppi undi", "en", "Telugu (noppi) -> Detected as English")
    ]
    
    for text, lang, desc in med_tests:
        print(f"Test: '{text}' ({desc})")
        if bot.is_medical_query(text):
            print("RESULT: PASSED (Identified as Medical)")
        else:
            print("RESULT: FAILED (Missed Medical Keyword)")

    print("\nVerification Complete.")

if __name__ == "__main__":
    run_test()
