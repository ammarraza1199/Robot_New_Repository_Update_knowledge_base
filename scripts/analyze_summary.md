=== TOP 10 HALLUCINATED RESPONSES ===
51 times: I am a navigation robot. I can help you find hospital departments.
40 times: Ground Floor, near the main entrance.
28 times: नमस्ते! निम्स अस्पताल में आपका स्वागत है। आज मैं आपकी कैसे मदद कर सकता हूँ?
24 times: Hello! I am here to help you navigate the hospital.
23 times: Hello! Welcome to NIMS Hospital. How can I assist you today?
21 times: నమస్కారం! నిమ్స్ ఆసుపత్రికి స్వాగతం. ఈ రోజు నేను మీకు ఎలా సహాయపడగలను?
18 times: You're welcome! Take care.
18 times: Goodbye!
14 times: I am an AI robot designed to assist patients.
14 times: నేను అలసిపోయినప్పుడు నా ఛార్జింగ్ స్టేషన్‌కు వెళ్తాను.

=== TOP 10 MISMATCHED RESPONSES ===
44 times: The department name is Department of Lab Medicine, the doctor's name is Lab Technician, and the addr | Expected: ["'loc_pharmacy'", "'loc_tmt'", "'info_2d_echo'"]
37 times: The department name is Pharmacy, the doctor's name is Duty Pharmacist, and the address is Ground Flo | Expected: ["'loc_emergency'", "'loc_admission_counter'", "'loc_ip_billing'"]
34 times: The department name is Cardiology Unit 1, the doctor's name is Dr. O. Sai Satish, and the address is | Expected: ["'info_director'", "'loc_ot'", "'loc_echo'"]
31 times: The department name is Radiology Department, the doctor's name is Radiology Technician, and the addr | Expected: ["'info_opd_timing'", "'sym_breathing'", "'loc_echo'"]
26 times: The department name is Ophthalmology Department, the doctor's name is Ophthalmologist, and the addre | Expected: ["'loc_admission_counter'", "'info_admission'", "'ophthalmology'"]
24 times: విభాగం పేరు ల్యాబ్ మెడిసిన్ విభాగం, డాక్టర్ పేరు Lab Technician, మరియు చిరునామా డయాగ్నోస్టిక్ బ్లాక్ | Expected: ["'loc_tmt'", "'info_2d_echo'", "'loc_sample_collection'"]
24 times: విభాగం పేరు రేడియాలజీ విభాగం, డాక్టర్ పేరు Radiology Technician, మరియు చిరునామా గ్రౌండ్ ఫ్లోర్, డయాగ | Expected: ["'info_missing_report'", "'loc_dermatology'", "'loc_insurance_desk'"]
24 times: విభాగం పేరు జనరల్ ఓపీడీ, డాక్టర్ పేరు General Duty Doctor, మరియు చిరునామా ఓపీడి బ్లాక్, గ్రౌండ్ ఫ్లో | Expected: ["'info_opd_timing'", "'greet_hello'", "'info_evening_clinics'"]
23 times: विभाग का नाम ईएनटी विभाग, डॉक्टर का नाम ENT Specialist, और पता ओपीडी ब्लॉक, पहली मंजिल है। | Expected: ["'info_director'", "'sym_skin'", "'info_evening_clinics'"]
23 times: The department name is General OPD, the doctor's name is General Duty Doctor, and the address is OPD | Expected: ["'loc_ip_billing'", "'loc_dental'", "'info_meals'"]

=== ANALYZING POTENTIAL MISCLASSIFICATIONS ===
'I am a navigation robot...' response - For smalltalk (int_): 46, For departments (dept_): 5
