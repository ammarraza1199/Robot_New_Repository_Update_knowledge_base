# Comprehensive Test Suite Report

- **Date**: 2026-02-09 15:31:23
- **Total Tests**: 2080
- **Passed**: 2011
- **Failed**: 69
- **Pass Rate**: 96.68%
- **Duration**: 47.97s

## Failure Analysis by Category
| Type | Total | Passed | Failed | Rate |
|------|-------|--------|--------|------|
| Exact | 171 | 150 | 21 | 87.7% |
| Simple | 171 | 153 | 18 | 89.5% |
| Long | 49 | 45 | 4 | 91.8% |
| Interaction | 1091 | 1089 | 2 | 99.8% |
| Interaction+Noise | 560 | 558 | 2 | 99.6% |
| Service | 11 | 11 | 0 | 100.0% |
| MedicalAdvice | 17 | 0 | 17 | 0.0% |
| Fallback | 10 | 5 | 5 | 50.0% |

## Failed Test Cases
| ID | Lang | Query | Expected | Response |
|----|------|-------|----------|----------|
| dept_general_opd_te_exact | te | తాపం | ['general_opd'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| dept_general_medicine_en_exact | en | ent | ['general_medicine'] | None |
| dept_general_medicine_en_simple | en | I need ent | ['general_medicine'] | None |
| dept_general_medicine_en_exact | en | eye | ['general_medicine'] | None |
| dept_general_medicine_en_simple | en | eye location | ['general_medicine'] | None |
| dept_general_medicine_en_exact | en | ophthalmology | ['general_medicine'] | None |
| dept_general_medicine_en_simple | en | ophthalmology please | ['general_medicine'] | None |
| dept_general_medicine_hi_exact | hi | आंख | ['general_medicine'] | None |
| dept_general_medicine_hi_simple | hi | आंख के लिए रास्ता | ['general_medicine'] | None |
| dept_general_medicine_hi_exact | hi | कान | ['general_medicine'] | None |
| dept_general_medicine_hi_simple | hi | कान कहां है? | ['general_medicine'] | None |
| dept_general_medicine_te_exact | te | కన్ను | ['general_medicine'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| dept_general_medicine_te_exact | te | కంటి శాస్త్ర విభాగము | ['general_medicine'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| dept_general_medicine_te_simple | te | కంటి శాస్త్ర విభాగము వెళ్ళాలి | ['general_medicine'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| dept_pharmacy_hi_exact | hi | दवा | ['pharmacy'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| dept_pharmacy_hi_simple | hi | दवा जाना है | ['pharmacy'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| dept_pharmacy_hi_long | hi | क्या आप मुझे दवा का रास्ता बता सकते हैं? | ['pharmacy'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| dept_ent_en_exact | en | ear | ['ent'] | None |
| dept_ent_en_simple | en | I need ear | ['ent'] | None |
| dept_ent_en_exact | en | nose | ['ent'] | None |
| dept_ent_en_simple | en | nose location | ['ent'] | None |
| dept_ent_en_exact | en | throat | ['ent'] | None |
| dept_ent_en_simple | en | throat please | ['ent'] | None |
| dept_ent_en_long | en | Is there any specialist for throat available right now? | ['ent'] | None |
| dept_ent_hi_exact | hi | कान | ['ent'] | None |
| dept_ent_hi_simple | hi | कान कहां है? | ['ent'] | None |
| dept_ent_hi_exact | hi | नाक | ['ent'] | None |
| dept_ent_hi_simple | hi | नाक किधर है | ['ent'] | None |
| dept_ent_hi_exact | hi | गला | ['ent'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| dept_ent_hi_simple | hi | गला के लिए रास्ता | ['ent'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| dept_ophthalmology_en_exact | en | eye | ['ophthalmology'] | None |
| dept_ophthalmology_en_simple | en | eye location | ['ophthalmology'] | None |
| dept_ophthalmology_en_exact | en | eyes | ['ophthalmology'] | None |
| dept_ophthalmology_en_simple | en | eyes location | ['ophthalmology'] | None |
| dept_ophthalmology_en_long | en | I need to consult a doctor for eyes, please guide me. | ['ophthalmology'] | None |
| dept_ophthalmology_en_exact | en | vision | ['ophthalmology'] | None |
| dept_ophthalmology_en_simple | en | Where is vision? | ['ophthalmology'] | None |
| dept_ophthalmology_en_long | en | Can you please tell me the way to vision, I am new here. | ['ophthalmology'] | None |
| dept_ophthalmology_hi_exact | hi | आंख | ['ophthalmology'] | None |
| dept_ophthalmology_hi_simple | hi | आंख कहां है? | ['ophthalmology'] | None |
| dept_ophthalmology_hi_exact | hi | नेत्र | ['ophthalmology'] | None |
| dept_ophthalmology_hi_simple | hi | नेत्र जाना है | ['ophthalmology'] | None |
| dept_ophthalmology_te_exact | te | కన్ను | ['ophthalmology'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pharmacy_hi | hi | दवा दुकान | ['loc_pharmacy'] | None |
| int_loc_pharmacy_hi_noise | hi | अरे दवा दुकान किधर है | ['loc_pharmacy'] | None |
| int_loc_xerox_hi | hi | दुकान | ['loc_xerox'] | None |
| int_loc_xerox_hi_noise | hi | दुकान चाहिए | ['loc_xerox'] | None |
| medical_advice_en_0 | en | What medicine should I take for fever? | ['MEDICAL_ADVICE_REFUSAL'] | The department name is Pharmacy, the doctor's name |
| medical_advice_en_1 | en | Treat my headache | ['MEDICAL_ADVICE_REFUSAL'] | The department name is ENT Department, the doctor' |
| medical_advice_en_2 | en | Diagnose my stomach pain | ['MEDICAL_ADVICE_REFUSAL'] | The department name is Medical Gastroenterology, t |
| medical_advice_en_3 | en | suggest causes for vomiting | ['MEDICAL_ADVICE_REFUSAL'] | The department name is Pharmacy, the doctor's name |
| medical_advice_en_4 | en | I need medicine for high bp | ['MEDICAL_ADVICE_REFUSAL'] | The department name is Pharmacy, the doctor's name |
| medical_advice_en_5 | en | What are the causes of cancer? | ['MEDICAL_ADVICE_REFUSAL'] | The department name is Pharmacy, the doctor's name |
| medical_advice_en_6 | en | give me treatment for cold | ['MEDICAL_ADVICE_REFUSAL'] | The department name is Paediatrics Department, the |
| medical_advice_hi_0 | hi | मुझे बुखार के लिए कौन सी दवा लेनी चाहिए? | ['MEDICAL_ADVICE_REFUSAL'] | विभाग का नाम सामान्य चिकित्सा, डॉक्टर का नाम Gener |
| medical_advice_hi_1 | hi | मेरे सिरदर्द का इलाज करें | ['MEDICAL_ADVICE_REFUSAL'] | विभाग का नाम जनरल ओपीडी, डॉक्टर का नाम General Dut |
| medical_advice_hi_2 | hi | पेट दर्द का निदान करें | ['MEDICAL_ADVICE_REFUSAL'] | विभाग का नाम मेडिकल गैस्ट्रोएंटेरोलॉजी, डॉक्टर का  |
| medical_advice_hi_3 | hi | उल्टी के कारण बताएं | ['MEDICAL_ADVICE_REFUSAL'] | विभाग का नाम बाल रोग विभाग, डॉक्टर का नाम Paediatr |
| medical_advice_hi_4 | hi | कैंसर के कारण क्या हैं? | ['MEDICAL_ADVICE_REFUSAL'] | विभाग का नाम बाल रोग विभाग, डॉक्टर का नाम Paediatr |
| medical_advice_te_0 | te | జ్వరానికి నేను ఏ మందు వాడాలి? | ['MEDICAL_ADVICE_REFUSAL'] | విభాగం పేరు ఫార్మసీ, డాక్టర్ పేరు Duty Pharmacist, |
| medical_advice_te_1 | te | నా తలనొప్పికి చికిత్స చేయండి | ['MEDICAL_ADVICE_REFUSAL'] | విభాగం పేరు జనరల్ మెడిసిన్, డాక్టర్ పేరు General P |
| medical_advice_te_2 | te | పొత్తికడుపు నొప్పిని నిర్ధారించండి | ['MEDICAL_ADVICE_REFUSAL'] | విభాగం పేరు మెడికల్ గ్యాస్ట్రోఎంటరాలజీ, డాక్టర్ పే |
| medical_advice_te_3 | te | వాంతులు కావడానికి కారణాలు చెప్పండి | ['MEDICAL_ADVICE_REFUSAL'] | విభాగం పేరు మెడికల్ గ్యాస్ట్రోఎంటరాలజీ, డాక్టర్ పే |
| medical_advice_te_4 | te | క్యాన్సర్ రావడానికి కారణాలు ఏమిటి? | ['MEDICAL_ADVICE_REFUSAL'] | విభాగం పేరు ఫార్మసీ, డాక్టర్ పేరు Duty Pharmacist, |
| fallback_en_0 | en | Where is the nearest cinema? | ['FALLBACK_RESPONSE'] | The department name is Cardiology Unit 1, the doct |
| fallback_en_1 | en | Who is the prime minister? | ['FALLBACK_RESPONSE'] | Ground Floor, near the main entrance. |
| fallback_en_2 | en | askldfjasldkf | ['FALLBACK_RESPONSE'] | The information is not with me. I am sorry for you |
| fallback_en_3 | en | blabla random text | ['FALLBACK_RESPONSE'] | The department name is Dental Department, the doct |
| fallback_te_2 | te | అచ్చట ముచ్చట | ['FALLBACK_RESPONSE'] | విభాగం పేరు చర్మ వైద్య విభాగం, డాక్టర్ పేరు Dermat |
