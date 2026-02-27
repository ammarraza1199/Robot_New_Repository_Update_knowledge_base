# Comprehensive Test Suite Report

- **Date**: 2026-01-27 23:40:20
- **Total Tests**: 2080
- **Passed**: 1400
- **Failed**: 680
- **Pass Rate**: 67.31%
- **Duration**: 188.91s

## Failure Analysis by Category
| Type | Total | Passed | Failed | Rate |
|------|-------|--------|--------|------|
| Exact | 171 | 153 | 18 | 89.5% |
| Simple | 171 | 153 | 18 | 89.5% |
| Long | 49 | 45 | 4 | 91.8% |
| Interaction | 1091 | 676 | 415 | 62.0% |
| Interaction+Noise | 560 | 357 | 203 | 63.7% |
| Service | 11 | 11 | 0 | 100.0% |
| MedicalAdvice | 17 | 0 | 17 | 0.0% |
| Fallback | 10 | 5 | 5 | 50.0% |

## Failed Test Cases
| ID | Lang | Query | Expected | Response |
|----|------|-------|----------|----------|
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
| int_greet_hi_hi | hi | नमस्ते | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | नमस्कार | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi_noise | hi | नमस्कार चाहिए | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | हाय | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | हेलो | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | राम राम | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi_noise | hi | राम राम चाहिए | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | प्रणाम | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi_noise | hi | जी प्रणाम | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | नमस्ते जी | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_te | te | హాయ్ | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | హలో | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te_noise | te | అది హలో | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | నమస్కారం | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te_noise | te | అది నమస్కారం | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | నమస్తే | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | హాయ్ అండి | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te_noise | te | హాయ్ అండి కావాలి | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | హలో అండి | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te_noise | te | అది హలో అండి | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_hi | hi | हेलो | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi_noise | hi | जी हेलो | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi | hi | हैलो | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi | hi | मदद | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi | hi | सहायता | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_te | te | హలో | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_te_noise | te | హలో అండి | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_te | te | సహాయం | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_te | te | గైడ్ | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_te_noise | te | అది గైడ్ | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_how_are_you_hi | hi | कैसे हो | ['greet_how_are_you'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_how_are_you_hi | hi | कैसे हैं | ['greet_how_are_you'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_how_are_you_hi | hi | क्या हाल है | ['greet_how_are_you'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_how_are_you_hi | hi | हाल चाल | ['greet_how_are_you'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_how_are_you_hi | hi | सब ठीक | ['greet_how_are_you'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_how_are_you_hi_noise | hi | अरे सब ठीक किधर है | ['greet_how_are_you'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_how_are_you_te | te | బాగున్నారా | ['greet_how_are_you'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_how_are_you_te_noise | te | అది బాగున్నారా | ['greet_how_are_you'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_who_hi | hi | आप कौन हैं | ['identity_who'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_who_hi_noise | hi | जी आप कौन हैं | ['identity_who'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_who_hi | hi | कौन हो तुम | ['identity_who'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_who_hi_noise | hi | जी कौन हो तुम | ['identity_who'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_who_hi | hi | आपका नाम | ['identity_who'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_who_hi | hi | परिचय | ['identity_who'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_who_te | te | నువ్వు ఎవరు | ['identity_who'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_who_te | te | మీరు ఎవరు | ['identity_who'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_who_te | te | నీ పేరు ఏంటి | ['identity_who'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_who_te | te | పరిచయం | ['identity_who'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_what_hi | hi | आप क्या हैं | ['identity_what'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_what_hi | hi | रोबोट हो | ['identity_what'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_what_hi_noise | hi | जी रोबोट हो | ['identity_what'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_what_hi | hi | इंसान हो | ['identity_what'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_what_hi_noise | hi | जी इंसान हो | ['identity_what'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_what_hi | hi | मशीन | ['identity_what'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_identity_what_te | te | నువ్వు ఏంటి | ['identity_what'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_what_te | te | రోబోటా | ['identity_what'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_what_te_noise | te | రోబోటా కావాలి | ['identity_what'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_what_te | te | మనిషా | ['identity_what'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_identity_what_te | te | ఏఐ | ['identity_what'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_eat_hi | hi | खाना खाते हो | ['bot_eat'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_eat_hi | hi | भूख लगी | ['bot_eat'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_eat_hi | hi | खाते हो | ['bot_eat'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_eat_hi_noise | hi | जी खाते हो | ['bot_eat'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_eat_te | te | తింటావా | ['bot_eat'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_eat_te | te | ఆకలిగా ఉందా | ['bot_eat'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_eat_te | te | భోజనం చేస్తావా | ['bot_eat'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_eat_te_noise | te | భోజనం చేస్తావా కావాలి | ['bot_eat'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_sleep_hi | hi | कहाँ सोते हो | ['bot_sleep'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_sleep_hi | hi | सोते हो | ['bot_sleep'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_sleep_hi | hi | चार्ज | ['bot_sleep'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_sleep_hi_noise | hi | जी चार्ज | ['bot_sleep'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bot_sleep_te | te | ఎక్కడ పడుకుంటావు | ['bot_sleep'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_sleep_te | te | నిద్రపోతావా | ['bot_sleep'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bot_sleep_te | te | చార్జ్ | ['bot_sleep'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_query_hi | hi | मदद | ['help_query'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_query_hi | hi | सहायता | ['help_query'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_query_hi_noise | hi | जी सहायता | ['help_query'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_query_hi | hi | आप क्या कर सकते हो | ['help_query'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_query_te | te | సహాయం | ['help_query'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_query_te | te | ఏం చేయగలరు | ['help_query'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_query_te_noise | te | ఏం చేయగలరు కావాలి | ['help_query'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_query_te | te | గైడ్ | ['help_query'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_query_te_noise | te | గైడ్ కావాలి | ['help_query'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_hi | hi | धन्यवाद | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi_noise | hi | अरे धन्यवाद किधर है | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi | hi | शुक्रिया | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi | hi | थैंक यू | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi | hi | बहुत धन्यवाद | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi_noise | hi | जी बहुत धन्यवाद | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi | hi | आभार | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi | hi | धन्यवाद जी | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_hi_noise | hi | अरे धन्यवाद जी किधर है | ['gratitude'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_gratitude_te | te | ధన్యవాదాలు | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te_noise | te | ధన్యవాదాలు కావాలి | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te | te | థాంక్స్ | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te | te | థ్యాంక్యూ | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te_noise | te | థ్యాంక్యూ కావాలి | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te | te | చాలా ధన్యవాదాలు | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te | te | కృతజ్ఞతలు | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_gratitude_te_noise | te | అది కృతజ్ఞతలు | ['gratitude'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_hi | hi | अलविदा | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_hi_noise | hi | अलविदा चाहिए | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_hi | hi | चलता हूँ | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_hi_noise | hi | जी चलता हूँ | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_hi | hi | फिर मिलेंगे | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_hi | hi | ठीक है बाय | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_hi | hi | बाय | ['bye'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_bye_te | te | బాయ్ | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te_noise | te | అది బాయ్ | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te | te | వెళ్ళొస్తాను | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te | te | తర్వాత కలుద్దాం | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te | te | సరే బాయ్ | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te_noise | te | అది సరే బాయ్ | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te | te | బై బై | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_bye_te_noise | te | బై బై కావాలి | ['bye'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_nims_hi | hi | निम्स अस्पताल कहाँ है | ['loc_nims'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_nims_hi | hi | निम्स का पता | ['loc_nims'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_nims_hi | hi | निम्स लोकेशन | ['loc_nims'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_nims_hi_noise | hi | जी निम्स लोकेशन | ['loc_nims'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_nims_hi | hi | अस्पताल कहाँ है | ['loc_nims'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_nims_te | te | నిమ్స్ ఎక్కడ | ['loc_nims'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_nims_te | te | నిమ్స్ లొకేషన్ | ['loc_nims'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_emergency_hi | hi | आपातकाल | ['loc_emergency'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_emergency_hi | hi | कैजुअल्टी | ['loc_emergency'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_emergency_te | te | ఎమర్జెన్సీ | ['loc_emergency'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_emergency_te | te | ఎమర్జెన్సీ వార్డు | ['loc_emergency'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_emergency_te_noise | te | ఎమర్జెన్సీ వార్డు కావాలి | ['loc_emergency'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_emergency_te | te | క్యాజువాలిటీ | ['loc_emergency'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_emergency_te_noise | te | క్యాజువాలిటీ అండి | ['loc_emergency'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_emergency_te | te | అత్యవసర విభాగం | ['loc_emergency'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pharmacy_hi | hi | दवा दुकान | ['loc_pharmacy'] | None |
| int_loc_pharmacy_hi_noise | hi | अरे दवा दुकान किधर है | ['loc_pharmacy'] | None |
| int_loc_canteen_hi | hi | कैंटीन | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_hi | hi | खाना | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_hi_noise | hi | जी खाना | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_hi | hi | भोजन | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_hi | hi | लंच | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_hi_noise | hi | लंच चाहिए | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_hi | hi | कैफेटेरिया | ['loc_canteen'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_canteen_te | te | క్యాంటీన్ | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te_noise | te | అది క్యాంటీన్ | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te | te | ఆహారం | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te | te | టిఫిన్లు యెక్కడా | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te | te | అల్పాహారం | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te | te | భోజనం | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te | te | భోజన హోటల్ | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te_noise | te | భోజన హోటల్ అండి | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te | te | తినడానికి చోటు | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_canteen_te_noise | te | తినడానికి చోటు కావాలి | ['loc_canteen'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_icu_hi | hi | आईसीयू | ['loc_icu'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_icu_hi_noise | hi | अरे आईसीयू किधर है | ['loc_icu'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_icu_hi | hi | इंटेंसिव केयर | ['loc_icu'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_icu_hi | hi | क्रिटिकल केयर | ['loc_icu'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_icu_te | te | ఐసీయూ | ['loc_icu'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_icu_te_noise | te | ఐసీయూ అండి | ['loc_icu'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_icu_te | te | ఇంటెన్సివ్ కేర్ | ['loc_icu'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_icu_te | te | క్రిటికల్ కేర్ | ['loc_icu'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_icu_te | te | తీవ్ర చికిత్స | ['loc_icu'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_icu_te_noise | te | తీవ్ర చికిత్స కావాలి | ['loc_icu'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_director_hi | hi | निदेशक | ['info_director'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_director_hi | hi | अस्पताल निदेशक | ['info_director'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_director_hi | hi | डायरेक्टर कौन | ['info_director'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_director_hi_noise | hi | जी डायरेक्टर कौन | ['info_director'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_director_hi | hi | मुख्य अधिकारी | ['info_director'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_director_hi_noise | hi | अरे मुख्य अधिकारी किधर है | ['info_director'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_director_te | te | హాస్పిటల్ హెడ్ | ['info_director'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_director_te_noise | te | అది హాస్పిటల్ హెడ్ | ['info_director'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_director_te | te | director | ['info_director'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_complaint_hi | hi | शिकायत | ['info_complaint'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_complaint_hi | hi | फीडबैक | ['info_complaint'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_complaint_hi_noise | hi | जी फीडबैक | ['info_complaint'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_complaint_te | te | ఫిర్యాదు | ['info_complaint'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_complaint_te | te | కంప్లైంట్ | ['info_complaint'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_complaint_te_noise | te | కంప్లైంట్ అండి | ['info_complaint'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_complaint_te | te | ఫీడ్‌బ్యాక్ | ['info_complaint'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_complaint_te_noise | te | ఫీడ్‌బ్యాక్ అండి | ['info_complaint'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_hi | hi | मिलने का समय | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi | hi | विजिटिंग टाइम | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi_noise | hi | विजिटिंग टाइम चाहिए | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi | hi | कब मिल सकते | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi_noise | hi | जी कब मिल सकते | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi | hi | मुलाकात | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi | hi | देखने का समय | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi_noise | hi | अरे देखने का समय किधर है | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi | hi | अंदर जाने का समय | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_hi_noise | hi | जी अंदर जाने का समय | ['info_visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_visiting_hours_te | te | విజిట్ టైమ్ | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te | te | ఎప్పుడు కలవచ్చు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te_noise | te | అది ఎప్పుడు కలవచ్చు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te | te | లోపలికి వెల్లే గంటలు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te | te | లోపలికి ఎప్పుడు పంపిస్తారు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te | te | లోపలికి ఎప్పుడు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te_noise | te | లోపలికి ఎప్పుడు అండి | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te | te | పేషెంట్ ను కలిసే వేళలు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te_noise | te | అది పేషెంట్ ను కలిసే వేళలు | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_visiting_hours_te | te | కలవడానికి టైమ్ | ['info_visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_hi | hi | खून | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi_noise | hi | जी खून | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi | hi | खून बह रहा | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi_noise | hi | खून बह रहा चाहिए | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi | hi | चोट | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi | hi | कट गया | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi_noise | hi | अरे कट गया किधर है | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_hi | hi | खून निकल रहा | ['sym_bleeding'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_bleeding_te | te | రక్తం | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te_noise | te | రక్తం అండి | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te | te | రక్తం కారుతోంది | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te_noise | te | రక్తం కారుతోంది కావాలి | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te | te | కట్ | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te_noise | te | కట్ కావాలి | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te | te | గాయం | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te_noise | te | గాయం కావాలి | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te | te | bleeding | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_bleeding_te_noise | te | bleeding అండి | ['sym_bleeding'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te | te | ఓపీడి టైమ్ | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te_noise | te | ఓపీడి టైమ్ కావాలి | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te | te | ఓపీ టైమ్ | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te_noise | te | ఓపీ టైమ్ కావాలి | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te | te | ఎప్పుడు తెరుస్తారు  | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te_noise | te | ఎప్పుడు తెరుస్తారు  కావాలి | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te | te | ఓపీ ఎప్పుడు తెరుస్తారు | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_timing_te_noise | te | ఓపీ ఎప్పుడు తెరుస్తారు కావాలి | ['info_opd_timing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_status_te | te | ఓపీడి మూసి ఉందా | ['info_opd_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_status_te_noise | te | ఓపీడి మూసి ఉందా కావాలి | ['info_opd_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_status_te | te | ఇప్పుడు ఓపీడి | ['info_opd_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_status_te_noise | te | అది ఇప్పుడు ఓపీడి | ['info_opd_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_status_te | te |  OPD తెరిచి ఉందా | ['info_opd_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_opd_status_te_noise | te |  OPD తెరిచి ఉందా అండి | ['info_opd_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_admission_hi | hi | भर्ती | ['info_admission'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_admission_hi_noise | hi | अरे भर्ती किधर है | ['info_admission'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_admission_hi | hi | एडमिशन | ['info_admission'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_admission_hi | hi | अस्पताल में भर्ती | ['info_admission'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_admission_hi_noise | hi | जी अस्पताल में भर्ती | ['info_admission'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_admission_te | te | అడ్మిషన్ | ['info_admission'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_admission_te | te | అడ్మిట్ అవ్వాలి | ['info_admission'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_admission_te | te | ప్రవేశం కోరకు, యెవరిని కలవాలి | ['info_admission'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_admission_te | te | దావా ఖానా | ['info_admission'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_admission_te | te | హాస్పిటల్ అడ్మిషన్ | ['info_admission'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_admission_te_noise | te | హాస్పిటల్ అడ్మిషన్ కావాలి | ['info_admission'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admission_counter_te | te | అడ్మిషన్ కౌంటర్ | ['loc_admission_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admission_counter_te_noise | te | అడ్మిషన్ కౌంటర్ అండి | ['loc_admission_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admission_counter_te | te | రోగి ప్రవేశంలో ఎక్కడ ఉంది | ['loc_admission_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admission_counter_te_noise | te | రోగి ప్రవేశంలో ఎక్కడ ఉంది అండి | ['loc_admission_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admission_counter_te | te | రిజిస్ట్రేషన్ | ['loc_admission_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_hi | hi | डिस्चार्ज | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi | hi | छुट्टी | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi_noise | hi | जी छुट्टी | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi | hi | कैसे निकले | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi_noise | hi | जी कैसे निकले | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi | hi | डिस्चार्ज की प्रक्रिया | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi_noise | hi | जी डिस्चार्ज की प्रक्रिया | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi | hi | घर कब जा सकते हैं | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi | hi | डिस्चार्ज के कागज | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_hi_noise | hi | डिस्चार्ज के कागज चाहिए | ['info_discharge'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_discharge_te | te | డిశ్చార్జ్ | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | రోగిని ఎలా డిశ్చార్జ్ చేస్తారు | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te_noise | te | రోగిని ఎలా డిశ్చార్జ్ చేస్తారు కావాలి | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | విడుదల | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te_noise | te | విడుదల కావాలి | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | ఎలా బయటకు | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | డిశ్చార్జ్ ప్రక్రియ | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | ఎప్పుడు డిశ్చార్జ్ చేస్తారు | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | ఇంటికి ఎప్పుడు వెళ్ళవచ్చు  | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | రోగి ఇంటికి ఎప్పుడు వెళ్ళవచ్చు | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | డిశ్చార్జ్ పేపర్లను ఎక్కడ పొందాలి | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te_noise | te | అది డిశ్చార్జ్ పేపర్లను ఎక్కడ పొందాలి | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te | te | డిశ్చార్జ్ పేపర్లు | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_discharge_te_noise | te | అది డిశ్చార్జ్ పేపర్లు | ['info_discharge'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_discharge_counter_hi | hi | बिलिंग | ['loc_discharge_counter'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_discharge_counter_hi_noise | hi | अरे बिलिंग किधर है | ['loc_discharge_counter'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_discharge_counter_te | te | డిశ్చార్జ్ కౌంటర్ | ['loc_discharge_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_discharge_counter_te_noise | te | అది డిశ్చార్జ్ కౌంటర్ | ['loc_discharge_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_discharge_counter_te | te | బిల్లింగ్ కౌంటర్ ఎక్కడ ఉంది | ['loc_discharge_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_discharge_counter_te_noise | te | అది బిల్లింగ్ కౌంటర్ ఎక్కడ ఉంది | ['loc_discharge_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_discharge_counter_te | te | బిల్లింగ్ | ['loc_discharge_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_discharge_counter_te_noise | te | బిల్లింగ్ కావాలి | ['loc_discharge_counter'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_sample_collection_hi | hi | सैंपल | ['loc_sample_collection'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_sample_collection_te | te | శాంపిల్ | ['loc_sample_collection'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_sample_collection_te | te | మూత్ర నమూనాను ఎక్కడ ఇవ్వాలి | ['loc_sample_collection'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_sample_collection_te_noise | te | మూత్ర నమూనాను ఎక్కడ ఇవ్వాలి అండి | ['loc_sample_collection'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_sample_collection_te | te | కఫం నమూనా ఎక్కడ ఇవ్వాలి | ['loc_sample_collection'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_sample_collection_te_noise | te | అది కఫం నమూనా ఎక్కడ ఇవ్వాలి | ['loc_sample_collection'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_reports_hi | hi | रिपोर्ट | ['loc_reports'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_reports_hi_noise | hi | अरे रिपोर्ट किधर है | ['loc_reports'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_reports_hi | hi | रिजल्ट | ['loc_reports'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_reports_hi | hi | लेनी है | ['loc_reports'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_reports_hi_noise | hi | जी लेनी है | ['loc_reports'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_reports_te | te | రిపోర్టులు | ['loc_reports'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_en | en | aarogyasri | ['info_insurance'] | I cannot provide medical advice. Please consult a  |
| int_info_insurance_hi | hi | आरोग्यश्री | ['info_insurance'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_insurance_hi_noise | hi | आरोग्यश्री चाहिए | ['info_insurance'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_insurance_hi | hi | इंश्योरेंस | ['info_insurance'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_insurance_hi_noise | hi | इंश्योरेंस चाहिए | ['info_insurance'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_insurance_hi | hi | सरकारी योजना | ['info_insurance'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_insurance_hi_noise | hi | सरकारी योजना चाहिए | ['info_insurance'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_insurance_te | te | ఆరోగ్యశ్రీ | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te | te | ఇన్సూరెన్స్ | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te | te | బీమా పాలసీ | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te_noise | te | అది బీమా పాలసీ | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te | te | బీమా | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te_noise | te | అది బీమా | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te | te | రేషన్ కార్డు | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te_noise | te | రేషన్ కార్డు అండి | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te | te | ఆహార భద్రత కార్డు | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te_noise | te | అది ఆహార భద్రత కార్డు | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_insurance_te | te | ప్రభుత్వ పథకం | ['info_insurance'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_insurance_desk_en | en | aarogyasri desk | ['loc_insurance_desk'] | I cannot provide medical advice. Please consult a  |
| int_loc_insurance_desk_hi | hi | इंश्योरेंस डेस्क | ['loc_insurance_desk'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_insurance_desk_hi_noise | hi | जी इंश्योरेंस डेस्क | ['loc_insurance_desk'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_insurance_desk_hi | hi | आरोग्यश्री | ['loc_insurance_desk'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_insurance_desk_te | te | ఆరోగ్యశ్రీ | ['loc_insurance_desk'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ct_scan_hi | hi | सीटी | ['loc_ct_scan'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ct_scan_hi_noise | hi | अरे सीटी किधर है | ['loc_ct_scan'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_missing_report_hi | hi | रिपोर्ट गुम | ['info_missing_report'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_missing_report_hi_noise | hi | जी रिपोर्ट गुम | ['info_missing_report'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_hi | hi | फाइल खो गई | ['info_lost_file'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_hi_noise | hi | फाइल खो गई चाहिए | ['info_lost_file'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_hi | hi | रिकॉर्ड | ['info_lost_file'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_hi_noise | hi | अरे रिकॉर्ड किधर है | ['info_lost_file'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_hi | hi | फाइल नहीं मिल रही | ['info_lost_file'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_hi_noise | hi | जी फाइल नहीं मिल रही | ['info_lost_file'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_lost_file_te | te | ఫైల్ లేదు | ['info_lost_file'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_lost_file_te | te | రికార్డ్స్ | ['info_lost_file'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_lost_file_te | te | నా ఫైల్ | ['info_lost_file'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_lost_file_te_noise | te | నా ఫైల్ అండి | ['info_lost_file'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_lift_hi | hi | लिफ्ट | ['loc_lift'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_lift_hi | hi | सीढ़ी | ['loc_lift'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_lift_hi_noise | hi | जी सीढ़ी | ['loc_lift'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_lift_hi | hi | ऊपर जाना | ['loc_lift'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_lift_te | te | లిఫ్ట్ | ['loc_lift'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_lift_te | te | ఎలివేటర్ | ['loc_lift'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_lift_te_noise | te | అది ఎలివేటర్ | ['loc_lift'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_lift_te | te | మెట్ల మార్గం ఎక్కడ | ['loc_lift'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_lift_te | te | పై అంతస్తులకు ఎలా వెళ్లాలి | ['loc_lift'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_parking_hi | hi | पार्किंग | ['loc_parking'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_parking_hi | hi | गाड़ी | ['loc_parking'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_parking_hi | hi | कार पार्क | ['loc_parking'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_parking_te | te | పార్కింగ్ | ['loc_parking'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_parking_te | te | కారు | ['loc_parking'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_parking_te_noise | te | అది కారు | ['loc_parking'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_parking_te | te | బైక్ | ['loc_parking'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_parking_te_noise | te | బైక్ అండి | ['loc_parking'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admin_hi | hi | प्रशासन | ['loc_admin'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_admin_hi_noise | hi | प्रशासन चाहिए | ['loc_admin'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_admin_hi | hi | एडमिन | ['loc_admin'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_admin_te | te | అడ్మినిస్ట్రేషన్ | ['loc_admin'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admin_te | te | అడ్మిన్ | ['loc_admin'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admin_te | te | కౌంటర్ | ['loc_admin'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_admin_te_noise | te | కౌంటర్ కావాలి | ['loc_admin'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ip_billing_hi | hi | बिलिंग | ['loc_ip_billing'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ip_billing_hi | hi | इन पेशेंट | ['loc_ip_billing'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ip_billing_hi_noise | hi | अरे इन पेशेंट किधर है | ['loc_ip_billing'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ip_billing_hi | hi | भुगतान | ['loc_ip_billing'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ip_billing_te | te | బిల్లింగ్ | ['loc_ip_billing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ip_billing_te_noise | te | బిల్లింగ్ అండి | ['loc_ip_billing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ip_billing_te | te | ఇన్ పేషెంట్ | ['loc_ip_billing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ip_billing_te | te | నగదు చెల్లింపు | ['loc_ip_billing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ip_billing_te | te | పేమెంట్ | ['loc_ip_billing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ot_hi | hi | ओटी | ['loc_ot'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ot_hi | hi | ऑपरेशन | ['loc_ot'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ot_hi_noise | hi | ऑपरेशन चाहिए | ['loc_ot'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ot_hi | hi | थिएटर | ['loc_ot'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ot_te | te | ఓటి | ['loc_ot'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ot_te | te | ఆపరేషన్ | ['loc_ot'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ot_te_noise | te | అది ఆపరేషన్ | ['loc_ot'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ot_te | te | థియేటర్ | ['loc_ot'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ot_te_noise | te | థియేటర్ కావాలి | ['loc_ot'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xerox_hi | hi | जेरॉक्स | ['loc_xerox'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_xerox_hi_noise | hi | जेरॉक्स चाहिए | ['loc_xerox'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_xerox_hi | hi | कॉपी | ['loc_xerox'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_xerox_hi | hi | दुकान | ['loc_xerox'] | None |
| int_loc_xerox_hi_noise | hi | दुकान चाहिए | ['loc_xerox'] | None |
| int_loc_xerox_te | te | జిరాక్స్ | ['loc_xerox'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xerox_te_noise | te | అది జిరాక్స్ | ['loc_xerox'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xerox_te | te | ఫోటోకాపీ | ['loc_xerox'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xerox_te_noise | te | ఫోటోకాపీ కావాలి | ['loc_xerox'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xerox_te | te | కంప్యూటర్ దుకాణం | ['loc_xerox'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xerox_te | te | జిరాక్స్ యంత్రం | ['loc_xerox'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_evening_clinics_hi | hi | इवनिंग क्लीनिक | ['info_evening_clinics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_evening_clinics_hi_noise | hi | इवनिंग क्लीनिक चाहिए | ['info_evening_clinics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_evening_clinics_hi | hi | शाम | ['info_evening_clinics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_evening_clinics_hi_noise | hi | अरे शाम किधर है | ['info_evening_clinics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_evening_clinics_hi | hi | डॉक्टर शाम | ['info_evening_clinics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_evening_clinics_te | te | ఈవినింగ్ క్లినిక్ | ['info_evening_clinics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_evening_clinics_te | te | సాయంత్రం క్లినిక్ ఎక్కడ ఉంది | ['info_evening_clinics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_evening_clinics_te_noise | te | సాయంత్రం క్లినిక్ ఎక్కడ ఉంది కావాలి | ['info_evening_clinics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_evening_clinics_te | te | సాయంత్రం క్లినిక్ | ['info_evening_clinics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_evening_clinics_te_noise | te | సాయంత్రం క్లినిక్ కావాలి | ['info_evening_clinics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_evening_clinics_te | te | సాయంత్రం | ['info_evening_clinics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xray_hi | hi | रूम | ['loc_xray'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_xray_hi_noise | hi | रूम चाहिए | ['loc_xray'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_xray_te | te | గది | ['loc_xray'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_xray_te_noise | te | అది గది | ['loc_xray'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ultrasound_hi | hi | अल्ट्रासाउंड | ['loc_ultrasound'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ultrasound_hi | hi | यूएसजी | ['loc_ultrasound'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_ultrasound_te | te | అల్ట్రాసౌండ్ | ['loc_ultrasound'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ultrasound_te | te | యుఎస్‌జి | ['loc_ultrasound'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_ultrasound_te_noise | te | యుఎస్‌జి కావాలి | ['loc_ultrasound'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_appointment_hi | hi | अपॉइंटमेंट | ['info_appointment'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_appointment_hi | hi | पंजीकरण | ['info_appointment'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_appointment_hi | hi | डॉक्टर मिलना | ['info_appointment'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_appointment_hi_noise | hi | जी डॉक्टर मिलना | ['info_appointment'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_appointment_te | te | రిజిస్ట్రేషన్ | ['info_appointment'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_appointment_te_noise | te | రిజిస్ట్రేషన్ అండి | ['info_appointment'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_feedback_hi | hi | प्रतिक्रिया | ['info_feedback'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_feedback_hi_noise | hi | अरे प्रतिक्रिया किधर है | ['info_feedback'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_feedback_hi | hi | सुझाव | ['info_feedback'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_feedback_hi_noise | hi | सुझाव चाहिए | ['info_feedback'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_feedback_hi | hi | शिकायत | ['info_feedback'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_feedback_hi_noise | hi | अरे शिकायत किधर है | ['info_feedback'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_feedback_te | te | ఫీడ్‌బ్యాక్ | ['info_feedback'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_feedback_te | te | సూచన | ['info_feedback'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_feedback_te | te | ఫిర్యాదులు ఎక్కడ ఇవ్వాలి | ['info_feedback'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_feedback_te_noise | te | ఫిర్యాదులు ఎక్కడ ఇవ్వాలి కావాలి | ['info_feedback'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_feedback_te | te | ఫిర్యాదు | ['info_feedback'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_feedback_te_noise | te | అది ఫిర్యాదు | ['info_feedback'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_hi | hi | पहली बार | ['loc_new_op'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_new_op_hi | hi | पंजीकरण करें | ['loc_new_op'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_new_op_te | te | కొత్త ఓపీ | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_te_noise | te | కొత్త ఓపీ అండి | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_te | te | కొత్త పేషెంట్ | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_te | te | రిజిస్ట్రేషన్ | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_te_noise | te | అది రిజిస్ట్రేషన్ | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_te | te | ఓపీ కార్డు | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_new_op_te | te | మొదటిసారి | ['loc_new_op'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_hi | hi | खाना खा सकते | ['info_fasting'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_fasting_hi | hi | फास्टिंग | ['info_fasting'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_fasting_hi_noise | hi | अरे फास्टिंग किधर है | ['info_fasting'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_fasting_te | te | ఖాళీ కడుపు | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_te_noise | te | అది ఖాళీ కడుపు | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_te | te | ఫాస్టింగ్ | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_te | te | తాగునీరు | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_te | te | తినవచ్చా | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_te_noise | te | తినవచ్చా కావాలి | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_fasting_te | te | అన్నం తినవచ్చా | ['info_fasting'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_hi | hi | खाना | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_hi_noise | hi | जी खाना | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_hi | hi | भोजन | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_hi_noise | hi | जी भोजन | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_hi | hi | डाइट | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_hi | hi | अस्पताल खाना | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_hi_noise | hi | जी अस्पताल खाना | ['info_meals'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_meals_te | te | భోజనం | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te_noise | te | అది భోజనం | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te | te | ఫలహారము | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te_noise | te | ఫలహారము కావాలి | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te | te | అల్పాహారం | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te | te | ఆహారం | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te | te | డైట్ ఫుడ్ | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te_noise | te | డైట్ ఫుడ్ కావాలి | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_meals_te | te | ఇన్ పేషెంట్ | ['info_meals'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_hi | hi | आधार | ['info_documents'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_documents_hi | hi | आईडी | ['info_documents'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_documents_hi_noise | hi | अरे आईडी किधर है | ['info_documents'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_documents_hi | hi | क्या लाना है | ['info_documents'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_documents_te | te | ఆధార్ | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te | te | ఆధార్ కార్డు | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te | te | గుర్తింపు కార్డు | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te_noise | te | గుర్తింపు కార్డు అండి | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te | te | ఐడీ | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te | te | ID కార్డ్ | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te | te | ఉద్యోగి ఆరోగ్య కార్డు | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te | te | ఏం తీసుకురావాలి | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_documents_te_noise | te | అది ఏం తీసుకురావాలి | ['info_documents'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_contact_hi | hi | संपर्क नंबर | ['info_contact'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_contact_hi | hi | फोन नंबर | ['info_contact'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_contact_hi | hi | हेल्पलाइन | ['info_contact'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_contact_hi_noise | hi | जी हेल्पलाइन | ['info_contact'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_contact_te | te | ఫోన్ నంబర్ | ['info_contact'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_contact_te | te | సంప్రదించాలి | ['info_contact'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_contact_te | te | ఎవరిని సంప్రదించాలి | ['info_contact'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_contact_te_noise | te | అది ఎవరిని సంప్రదించాలి | ['info_contact'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_contact_te | te | హెల్ప్‌లైన్ | ['info_contact'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_op_renewal_hi | hi | ओपी कार्ड | ['info_op_renewal'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_op_renewal_hi_noise | hi | अरे ओपी कार्ड किधर है | ['info_op_renewal'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_op_renewal_hi | hi | नवीनीकरण | ['info_op_renewal'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_op_renewal_te | te | ఓపీ రెన్యూవల్ | ['info_op_renewal'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_op_renewal_te_noise | te | ఓపీ రెన్యూవల్ అండి | ['info_op_renewal'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_op_renewal_te | te | కార్డు రెన్యూవల్ | ['info_op_renewal'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_op_renewal_te | te | పాత op కార్డ్ పునరుద్ధరణ | ['info_op_renewal'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_op_renewal_te | te | పాత ఓపీ | ['info_op_renewal'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_hi | hi | यूपीआई | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_hi_noise | hi | यूपीआई चाहिए | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_hi | hi | गूगल पे | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_hi | hi | फोनपे | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_hi_noise | hi | फोनपे चाहिए | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_hi | hi | डिजिटल भुगतान | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_hi_noise | hi | अरे डिजिटल भुगतान किधर है | ['info_upi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_upi_te | te | UPI | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te | te | గూగుల్ పే | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te_noise | te | గూగుల్ పే కావాలి | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te | te | ఫోన్‌పే | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te_noise | te | ఫోన్‌పే కావాలి | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te | te | క్రెడిట్ కార్డ్ | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te | te | డిజిటల్ పేమెంట్ | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_upi_te_noise | te | డిజిటల్ పేమెంట్ కావాలి | ['info_upi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_cardiology_te | te | ఛాతీ | ['loc_cardiology'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_echo_hi | hi | इको | ['loc_echo'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_echo_hi_noise | hi | इको चाहिए | ['loc_echo'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_echo_te | te | ఎకో | ['loc_echo'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_echo_te_noise | te | అది ఎకో | ['loc_echo'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_hi | hi | पेसमेकर | ['loc_pacemaker'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_pacemaker_hi_noise | hi | जी पेसमेकर | ['loc_pacemaker'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_pacemaker_te | te | పేస్‌మేకర్ | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_te_noise | te | పేస్‌మేకర్ కావాలి | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_te | te | పేస్ మేకర్ పని చేయడం లేదు | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_te_noise | te | పేస్ మేకర్ పని చేయడం లేదు కావాలి | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_te | te | పేస్ మేకర్ కోసం ఎవరిని సంప్రదించాలి | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_te | te | కొత్త పేస్‌మేకర్ కోసం ఎవరిని సంప్రదించాలి | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_pacemaker_te_noise | te | కొత్త పేస్‌మేకర్ కోసం ఎవరిని సంప్రదించాలి అండి | ['loc_pacemaker'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_tmt_hi | hi | टीएमटी | ['loc_tmt'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_tmt_hi_noise | hi | टीएमटी चाहिए | ['loc_tmt'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_tmt_hi | hi | ट्रेडमिल | ['loc_tmt'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_tmt_hi_noise | hi | ट्रेडमिल चाहिए | ['loc_tmt'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_tmt_te | te | TMT | ['loc_tmt'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_tmt_te | te | ట్రెడ్‌మిల్ | ['loc_tmt'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_tmt_te | te | tmt యంత్రం | ['loc_tmt'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_tmt_te_noise | te | tmt యంత్రం అండి | ['loc_tmt'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_2d_echo_hi | hi | 2डी इको | ['info_2d_echo'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_2d_echo_hi_noise | hi | जी 2डी इको | ['info_2d_echo'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_2d_echo_te | te | 2D ఎకో | ['info_2d_echo'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_duration_hi | hi | कितना समय | ['info_test_duration'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_test_duration_hi_noise | hi | कितना समय चाहिए | ['info_test_duration'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_test_duration_hi | hi | ईसीजी समय | ['info_test_duration'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_test_duration_hi_noise | hi | अरे ईसीजी समय किधर है | ['info_test_duration'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_test_duration_te | te | రోగనిర్ధారణ పరీక్లకు పట్టు సమయము | ['info_test_duration'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_duration_te_noise | te | రోగనిర్ధారణ పరీక్లకు పట్టు సమయము కావాలి | ['info_test_duration'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_pain_hi | hi | पेनफुल | ['info_test_pain'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_info_test_pain_te | te | బాధ ఉందా | ['info_test_pain'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_pain_te_noise | te | అది బాధ ఉందా | ['info_test_pain'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_pain_te | te | భాధగా ఉందా | ['info_test_pain'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_pain_te_noise | te | భాధగా ఉందా అండి | ['info_test_pain'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_pain_te | te | పెయిన్ | ['info_test_pain'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_info_test_pain_te_noise | te | పెయిన్ కావాలి | ['info_test_pain'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_oncology_hi | hi | कैंसर विभाग | ['loc_oncology'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_oncology_hi_noise | hi | अरे कैंसर विभाग किधर है | ['loc_oncology'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_genetics_hi | hi | जेनेटिक्स | ['loc_genetics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_genetics_hi_noise | hi | अरे जेनेटिक्स किधर है | ['loc_genetics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_genetics_hi | hi | डीएनए | ['loc_genetics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_loc_genetics_te | te | జెనెటిక్స్ | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te_noise | te | జెనెటిక్స్ కావాలి | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te | te | జన్యుశాస్త్ర విభాగం ఎక్కడ ఉంది | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te | te | జెనెటిక్స్ క్లినిక్ ఎక్కడ ఉంది? | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te | te | DNA ఎక్కడ ఉంది | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te_noise | te | అది DNA ఎక్కడ ఉంది | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te | te | డీఎన్ఏ | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_genetics_te_noise | te | డీఎన్ఏ కావాలి | ['loc_genetics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_loc_urology_te | te | కిడ్నీ క్లినిక్ | ['loc_urology'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_breathing_hi | hi | दम घुटना | ['sym_breathing'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_breathing_te | te | ఊపిరి పీల్చుకోలేకపోతున్నారు | ['sym_breathing'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_skin_hi | hi | दाने | ['sym_skin'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_skin_hi_noise | hi | अरे दाने किधर है | ['sym_skin'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_sym_skin_te | te | దద్దుర్లు | ['sym_skin'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_sym_urine_te | te | యుటిఐ | ['sym_urine'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_hi | hi | हाय | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi_noise | hi | जी हाय | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | नमस्ते | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi_noise | hi | नमस्ते चाहिए | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_hi | hi | हेलो | ['greet_hi'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hi_te | te | హాయ్ | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | హలో | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te_noise | te | అది హలో | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hi_te | te | హాయి | ['greet_hi'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_hi | hi | हैलो | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi_noise | hi | हैलो चाहिए | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi | hi | हेलो | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi_noise | hi | अरे हेलो किधर है | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_hi | hi | नमस्ते | ['greet_hello'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_hello_te | te | హలో | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_te | te | హాయ్ | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_hello_te | te | నమస్కారం | ['greet_hello'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_namaste_hi | hi | नमस्ते | ['greet_namaste'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_namaste_hi | hi | नमस्कार | ['greet_namaste'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_namaste_hi_noise | hi | नमस्कार चाहिए | ['greet_namaste'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_namaste_hi | hi | राम राम | ['greet_namaste'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_namaste_hi_noise | hi | राम राम चाहिए | ['greet_namaste'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_namaste_te | te | నమస్తే | ['greet_namaste'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_namaste_te | te | నమస్కారం | ['greet_namaste'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_namaste_te_noise | te | నమస్కారం కావాలి | ['greet_namaste'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_good_morning_hi | hi | सुप्रभात | ['greet_good_morning'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_good_morning_hi | hi | गुड मॉर्निंग | ['greet_good_morning'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_good_morning_hi_noise | hi | अरे गुड मॉर्निंग किधर है | ['greet_good_morning'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_greet_good_morning_te | te | శుభోదయం | ['greet_good_morning'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_greet_good_morning_te_noise | te | శుభోదయం అండి | ['greet_good_morning'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_request_hi | hi | मदद | ['help_request'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_request_hi_noise | hi | मदद चाहिए | ['help_request'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_request_hi | hi | सहायता | ['help_request'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_request_hi_noise | hi | जी सहायता | ['help_request'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_request_hi | hi | मदद चाहिए | ['help_request'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_request_hi_noise | hi | अरे मदद चाहिए किधर है | ['help_request'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_help_request_te | te | సహాయం | ['help_request'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_request_te | te | హెల్ప్ | ['help_request'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_request_te_noise | te | హెల్ప్ కావాలి | ['help_request'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_help_request_te | te | సహాయం కావాలి | ['help_request'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_billing_location_hi | hi | बिलिंग | ['billing_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_billing_location_hi | hi | बिल | ['billing_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_billing_location_hi | hi | पेमेंट | ['billing_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_billing_location_hi_noise | hi | अरे पेमेंट किधर है | ['billing_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_billing_location_te | te | బిల్లింగ్ | ['billing_location'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_billing_location_te | te | పేమెంట్ | ['billing_location'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_reports_location_hi | hi | रिपोर्ट | ['reports_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_reports_location_hi | hi | रिजल्ट | ['reports_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_reports_location_hi_noise | hi | रिजल्ट चाहिए | ['reports_location'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_reports_location_te | te | రిపోర్ట్స్ | ['reports_location'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_reports_location_te | te | రిజల్ట్స్ | ['reports_location'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_reports_location_te_noise | te | అది రిజల్ట్స్ | ['reports_location'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_opd_timings_te | te | ఓపీడి టైమ్ | ['opd_timings'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_visiting_hours_hi | hi | मिलने का समय | ['visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_visiting_hours_hi | hi | विजिट टाइम | ['visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_visiting_hours_hi_noise | hi | विजिट टाइम चाहिए | ['visiting_hours'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_visiting_hours_te | te | ఎప్పుడు కలవచ్చు | ['visiting_hours'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_department_status_hi | hi | बंद है | ['department_status'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_department_status_te | te | తెరిచి ఉందా | ['department_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_department_status_te | te | మూసి ఉందా | ['department_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_department_status_te | te | ఇప్పుడు ఓపెన్ | ['department_status'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_lab_diagnostics_hi | hi | प्रयोगशाला | ['lab_diagnostics'] | जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद  |
| int_lab_diagnostics_te | te | ప్రయోగశాల | ['lab_diagnostics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
| int_lab_diagnostics_te_noise | te | అది ప్రయోగశాల | ['lab_diagnostics'] | సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాన |
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
| fallback_en_1 | en | Who is the prime minister? | ['FALLBACK_RESPONSE'] | The information is not with me. I am sorry for you |
| fallback_en_2 | en | askldfjasldkf | ['FALLBACK_RESPONSE'] | The information is not with me. I am sorry for you |
| fallback_en_3 | en | blabla random text | ['FALLBACK_RESPONSE'] | The department name is Dental Department, the doct |
| fallback_te_2 | te | అచ్చట ముచ్చట | ['FALLBACK_RESPONSE'] | విభాగం పేరు చర్మ వైద్య విభాగం, డాక్టర్ పేరు Dermat |
