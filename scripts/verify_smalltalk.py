from interaction_process import InteractionProcess
import multiprocessing

q1 = multiprocessing.Queue()
q2 = multiprocessing.Queue()
q3 = multiprocessing.Queue()
flag = multiprocessing.Event()
playing = multiprocessing.Event()
ip = InteractionProcess(q1, q2, flag, playing, q3)

tests = [
    # Should NOT be smalltalk (False Positives from before)
    "I have an irregular heartbeat",
    "heart skipping beats please",
    "Treat my headache",
    "I'm sweating a lot",
    "I need something to treat my pain",
    
    # Should be smalltalk (Leaked before)
    "namaste",
    "kaise ho",
    "suprabhat",
    "namaskaram",
    "ela unnavu",
    "hello bot",
    "food",
    "kese ho"
]

print("--- TESTING is_smalltalk_query ---")
for t in tests:
    res = ip.is_smalltalk_query(t)
    print(f"[{'PASS' if (res and t in tests[5:]) or (not res and t in tests[:5]) else 'FAIL'}] '{t}' -> {res}")
