# Knowledge Base Failure Analysis

## Summary
- **Total Failures:** 469
- **NLU Misses (No Match):** 24 (Safer failure - Robot asks again)
- **Misclassifications (Wrong Dept):** 445 (Risk of wrong transfer)

## 1. Misclassifications (The Dangerous Pattern)
These are keywords that mapped to the WRONG department. These are high priority fixes.

### Pattern: ENT -> general_medicine (17 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | ear | Department |
| en | nose | Department |
| en | throat | Department |
| en | ent | Department |
| en | hearing | Department |
| en | sinus | Department |
| en | otorhinolaryngology | Department |
| hi | कान | Department |
| hi | नाक | Department |
| hi | सुनने में दिक्कत | Department |
| te | గొంతులో సమశ్య | Department |
| te | గొంతులో దురద | Department |
| te | కొండా నాలిక | Department |
| te | చెవిలో దురద | Department |
| te | వినికిడి సమస్య | Department |
| en | ear nose throat | Department Alias |
| en | otorhinolaryngology | Department Alias |

### Pattern: Cardiology Unit-1 -> General Medicine (15 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | चक्कर आना | Department |
| hi | दर्द का बाएं हाथ में फैलना | Department |
| te | ఛాతీ నొప్పి | Department |
| te | గుండె నొప్పి | Department |
| te | అధిక రక్తపోటు | Department |
| te | అల్ప రక్తపోటు | Department |
| te | నొప్పి ఎడమ చేతికి పాకడం | Department |
| te | దవడకు నొప్పి పాకడం | Department |
| te | గుండె నొప్పి | Department |
| te | కాలు నొప్పి | Department |
| te | కాళ్ల నొప్పి | Department |
| te | రక్త పోటు | Department |
| te | నిన్నటి నుంచి ఛాతీ నొప్పి | Department |
| te | ఛాతీ చాలా నొప్పిగా ఉంది | Department |
| te | అమ్మకు గుండె నొప్పి | Department |

### Pattern: Ophthalmology -> general_medicine (12 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | eye | Department |
| en | eyes | Department |
| en | vision | Department |
| en | ophthalmology | Department |
| en | cataract | Department |
| en | blindness | Department |
| hi | आंख | Department |
| hi | नेत्र | Department |
| hi | मोतियाबिंद | Department |
| te | కంట్లో దురద | Department |
| en | eye | Department Alias |
| en | vision | Department Alias |

### Pattern: Cardiology Unit-4 -> Cardiology Unit-1 (6 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | दिल का दौरा | Department |
| hi | सीने में दर्द के साथ बेहोशी | Department |
| te | గుండెపోటు | Department |
| te | ఛాతీ నొప్పితో కుప్పకూలడం | Department |
| te | ఛాతీ నొప్పితో స్పృహ కోల్పోవడం | Department |
| te | గుండె వైఫల్యం | Department |

### Pattern: డాక్టర్ సంతకం చేసిన తర్వాత, బి... -> నేను అలసిపోయినప్పుడు నా ఛార్జి... (6 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | డిశ్చార్జ్ | Interaction |
| te | రోగిని ఎలా డిశ్చార్జ్ చేస్తారు | Interaction |
| te | డిశ్చార్జ్ ప్రక్రియ | Interaction |
| te | ఎప్పుడు డిశ్చార్జ్ చేస్తారు | Interaction |
| te | డిశ్చార్జ్ పేపర్లను ఎక్కడ పొందాలి | Interaction |
| te | డిశ్చార్జ్ పేపర్లు | Interaction |

### Pattern: नमस्ते! मैं आपकी कैसे मदद कर स... -> नमस्ते! निम्स अस्पताल में आपका... (6 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | हाय | Interaction |
| hi | नमस्ते | Interaction |
| hi | हेलो | Interaction |
| hi | नमस्ते | Interaction |
| hi | नमस्कार | Interaction |
| hi | राम राम | Interaction |

### Pattern: Cardiology Unit-1 -> Neurology (5 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మేడ నరాలు లాగుతున్నాయి | Department |
| te | మేడ నరాలు గుంజుతున్నాయి | Department |
| te | నరాలు గుంజుతున్నాయి | Department |
| te | తల తిరగడం | Department |
| te | కల్లు తిరగటం | Department |

### Pattern: డెంటల్ విభాగానికి వెళ్లండి.... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (5 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | రూట్ కెనాల్ సమస్య | Interaction |
| te | జ్ఞాన దంతాల సమస్య | Interaction |
| te | దంతాల చిగుళ్ల సమస్య | Interaction |
| te | దంతాల అమరిక సమస్య | Interaction |
| te | దంతాల సమస్య | Interaction |

### Pattern: Cardiology Unit-2 -> Cardiology Unit-1 (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | दिल की धड़कन छूटना | Department |
| te | గుండె లయ తప్పడం | Department |
| te | గుండె కొట్టుకోవడం ఆగడం | Department |
| te | గుండె బరువుగా వుంది | Department |

### Pattern: Medical Gastroenterology -> General Medicine (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | भूख न लगना | Department |
| te | పై కడుపులో నొప్పి | Department |
| te | కడుపు నొప్పి | Department |
| te | నిన్నటి నుంచి కడుపులో నొప్పి | Department |

### Pattern: Pulmonary Medicine -> General Medicine (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | దీర్ఘకాలిక దగ్గు | Department |
| te | రెండు వారాల కంటే ఎక్కువ దగ్గు | Department |
| te | దగ్గులో రక్తం | Department |
| te | పల్మనరీ మెడిసిన్ | Department |

### Pattern: Orthopaedics -> General Medicine (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కీళ్ల నొప్పులు | Department |
| te | నడుము నొప్పి | Department |
| te | ముడుకుల్లో నొప్పి | Department |
| te | మోకాళ్ళ నొప్పి | Department |

### Pattern: Neurology -> General Medicine (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | चक्कर आना | Department |
| hi | नसों की कमजोरी | Department |
| hi | याददाश्त कमजोर होना | Department |
| te | తల నొప్పి | Department |

### Pattern: Please visit the Medical Super... -> I am an AI robot designed to a... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | complaint | Interaction |
| en | register complaint | Interaction |
| en | complain | Interaction |
| en | where complain | Interaction |

### Pattern: Main Block, Ground Floor.... -> Ground Floor, near the main en... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | admission counter | Interaction |
| en | where admit | Interaction |
| en | registration counter | Interaction |
| en | insurance counter | Interaction |

### Pattern: Diagnostic Block.... -> Ground Floor, near Diagnostic ... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | lab | Interaction |
| en | diagnostic lab | Interaction |
| en | laboratory | Interaction |
| en | test lab | Interaction |

### Pattern: OTs are on respective floors (... -> Ground Floor, near the main en... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | operation theatre | Interaction |
| en | surgery room | Interaction |
| en | operation | Interaction |
| en | theater | Interaction |

### Pattern: Near the OPD entrance or Main ... -> Ground Floor, near the main en... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | xerox | Interaction |
| en | printer shop | Interaction |
| en | colour printer | Interaction |
| en | computer shop | Interaction |

### Pattern: Yes, diet meals are provided t... -> I consume electricity, not foo... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | hospital food | Interaction |
| en | diet food | Interaction |
| en | inpatient food | Interaction |
| en | do you give food | Interaction |

### Pattern: It is an ultrasound test for t... -> Cardiology, Ground Floor.... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | 2d echo | Interaction |
| en | echo test | Interaction |
| en | heart echo | Interaction |
| en | cardiac echo | Interaction |

### Pattern: No, ECG and Echo are painless.... -> I am an AI robot designed to a... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | painful test | Interaction |
| en | test pain | Interaction |
| en | is ecg painful | Interaction |
| en | echo painful | Interaction |

### Pattern: లేదు, ఇవి నొప్పి లేని పరీక్షలు... -> గ్రౌండ్ ఫ్లోర్, గది 2-6.... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మీకు ఇప్పుడు ఛాతీ నొప్పిగా ఉందా | Interaction |
| te | మీ ఛాతీ నొప్పి ఎంత తీవ్రంగా ఉంది | Interaction |
| te | మీకు ఏ వైపు ఛాతీ నొప్పి ఉంది | Interaction |
| te | ఛాతీలో ఏదైనా నొప్పి ఉందా? | Interaction |

### Pattern: Hello! How can I help you toda... -> Hello! Welcome to NIMS Hospita... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | hi | Interaction |
| en | hello | Interaction |
| en | hey | Interaction |
| en | hii | Interaction |

### Pattern: Hello! Welcome to NIMS Hospita... -> Hello! Welcome to NIMS Hospita... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | hello | Interaction |
| en | hii | Interaction |
| en | hey | Interaction |
| en | hi | Interaction |

### Pattern: I'm here to help! You can ask ... -> Hello! I am here to help you n... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | help | Interaction |
| en | assist | Interaction |
| en | guide me | Interaction |
| en | can you help | Interaction |

### Pattern: OPD timings are 8:00 AM to 12:... -> 8:00 AM to 12:00 PM on working... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | opd timing | Interaction |
| en | opd time | Interaction |
| en | opd hours | Interaction |
| en | when opd open | Interaction |

### Pattern: Visiting hours are 4:00 PM to ... -> Visiting hours are from 4:00 P... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | visiting hours | Interaction |
| en | visitor time | Interaction |
| en | when can visit | Interaction |
| en | meeting time | Interaction |

### Pattern: Laboratory is on Ground Floor,... -> Ground Floor, near Diagnostic ... (4 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | lab | Interaction |
| en | laboratory | Interaction |
| en | sample collection | Interaction |
| en | diagnostic lab | Interaction |

### Pattern: Cardiology Unit-2 -> Medical Gastroenterology (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | चलते समय सांस फूलना | Department |
| hi | मेहनत करने पर सांस फूलना | Department |
| hi | सांस फूलना | Department |

### Pattern: Vascular Surgery -> Cardiology Unit-1 (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కాళ్ళ వాపు | Department |
| te | నొప్పితో కూడిన కాళ్ళ వాపు | Department |
| te | కాళ్ళ వాపు | Department |

### Pattern: Paediatrics -> General OPD (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పిల్లల డాక్టర్ | Department |
| te | పసిపిల్లల వైద్యం | Department |
| te | చిన్న పిల్లల డాక్టర్ | Department |

### Pattern: Dental -> General Medicine (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పంటి చిగుళ్ల నొప్పి | Department |
| te | చిగుళ్ల నొప్పి | Department |
| te | దవడలో నొప్పి | Department |

### Pattern: I can guide you to departments... -> Hello! I am here to help you n... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | help | Interaction |
| en | assist me | Interaction |
| en | guide me | Interaction |

### Pattern: After the doctor signs the sum... -> I go to my charging station wh... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | discharge | Interaction |
| en | discharge process | Interaction |
| en | get discharged | Interaction |

### Pattern: डॉक्टर के हस्ताक्षर के बाद, बि... -> जब मैं थक जाता हूं तो मैं अपने... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | डिस्चार्ज | Interaction |
| hi | डिस्चार्ज की प्रक्रिया | Interaction |
| hi | डिस्चार्ज के कागज | Interaction |

### Pattern: कृपया अपनी रसीद के साथ रिपोर्ट... -> डायग्नोस्टिक ब्लॉक में रिपोर्ट... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | रिपोर्ट गुम | Interaction |
| hi | रिपोर्ट नहीं मिली | Interaction |
| hi | मेरी रिपोर्ट | Interaction |

### Pattern: దయచేసి మెడికల్ సూపరింటెండెంట్ ... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఫీడ్‌బ్యాక్ | Interaction |
| te | ఫిర్యాదులు ఎక్కడ ఇవ్వాలి | Interaction |
| te | ఫిర్యాదు | Interaction |

### Pattern: हाँ, डॉक्टर की सलाह के अनुसार ... -> पार्किंग क्षेत्र के पास / ओपीड... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | खाना | Interaction |
| hi | भोजन | Interaction |
| hi | अस्पताल खाना | Interaction |

### Pattern: అవును, డాక్టర్ సలహా ప్రకారం పే... -> పార్కింగ్ ఏరియా దగ్గర / ఓపీడి ... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | భోజనం | Interaction |
| te | అల్పాహారం | Interaction |
| te | ఆహారం | Interaction |

### Pattern: Please check the NIMS website ... -> Ground Floor, near the main en... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | contact number | Interaction |
| en | phone number | Interaction |
| en | important numbers | Interaction |

### Pattern: ఇది గుండె కోసం చేసే అల్ట్రాసౌం... -> కార్డియాలజీ, గ్రౌండ్ ఫ్లోర్.... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | 2D ఎకో | Interaction |
| te | ఎకో టెస్ట్ | Interaction |
| te | హార్ట్ ఎకో | Interaction |

### Pattern: Visit Gastroenterology (5th Fl... -> I am an AI robot designed to a... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | stomach pain | Interaction |
| en | abdominal pain | Interaction |
| en | gas pain | Interaction |

### Pattern: Visit Dental Department.... -> I am an AI robot designed to a... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | tooth pain | Interaction |
| en | gum pain | Interaction |
| en | dental pain | Interaction |

### Pattern: నమస్కారం! నిమ్స్ ఆసుపత్రికి స్... -> నమస్కారం! నిమ్స్ ఆసుపత్రికి స్... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | హలో | Interaction |
| te | హాయ్ | Interaction |
| te | నమస్కారం | Interaction |

### Pattern: Lab reports can be collected f... -> Report Dispatch Counter in Dia... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | reports | Interaction |
| en | collect report | Interaction |
| en | test results | Interaction |

### Pattern: लैब रिपोर्ट डायग्नोस्टिक ब्लॉक... -> डायग्नोस्टिक ब्लॉक में रिपोर्ट... (3 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | रिपोर्ट | Interaction |
| hi | रिजल्ट | Interaction |
| hi | टेस्ट रिपोर्ट | Interaction |

### Pattern: General OPD -> Neurology (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | జనరల్ ఓపీడీ | Department |
| en | sexology | Department Alias |

### Pattern: General Medicine -> General OPD (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | సాధారణ వైద్యం | Department |
| te | చెక్కెర వ్యాధి | Department |

### Pattern: Cardiology Unit-1 -> ENT (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఆరి చేతులు చెమటలు పడుతున్నాయి | Department |
| te | చేతులు గుంజు తున్నాయ్ | Department |

### Pattern: Cardiology Unit-1 -> General OPD (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | గుండె జబ్బు | Department |
| te | గుండె డాక్టర్ | Department |

### Pattern: Cardiology Unit-2 -> Pulmonary Medicine (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | శ్రమతో ఆయాసం | Department |
| te | శ్వాస ఆడకపోవడం | Department |

### Pattern: Cardiology Unit-4 -> General Medicine (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | అకస్మాత్తుగా ఛాతీ నొప్పి | Department |
| te | తీవ్రమైన ఛాతీ నొప్పి | Department |

### Pattern: Urology -> Medical Gastroenterology (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | बार-बार पेशाब आना | Department |
| hi | पेशाब रुकना | Department |

### Pattern: Urology -> General Medicine (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మూత్రం పోసేటప్పుడు నొప్పి | Department |
| te | కిడ్నీలో రాళ్ల నొప్పి | Department |

### Pattern: Vascular Surgery -> Medical Gastroenterology (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | पैर का काला पड़ना | Department |
| hi | पैर काला पड़ना | Department |

### Pattern: Vascular Surgery -> Neurology (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | నరాలు ఉబ్బడం | Department |
| te | నరాలు | Department |

### Pattern: Radiology -> Laboratory (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | खून की जांच | Department |
| en | diagnostics | Department Alias |

### Pattern: Paediatrics -> General Medicine (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | बच्चे को बुखार है | Department |
| te | పిల్లలకి జ్వరం | Department |

### Pattern: Dermatology -> General OPD (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | त्वचा की समस्याएं | Department |
| hi | नाखून की समस्या | Department |

### Pattern: Dermatology -> Pulmonary Medicine (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | చర్మ సమస్యలు | Department |
| te | గోళ్ళ సమస్యలు | Department |

### Pattern: Ophthalmology -> Paediatrics (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కల్లు యెర్ర బరాటం | Department |
| te | కంటి ఆసుపత్రి | Department |

### Pattern: Ophthalmology -> General OPD (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కంటి వైద్యం | Department |
| te | కంటి డాక్టర్ | Department |

### Pattern: नमस्ते! मैं अस्पताल में आपका म... -> नमस्ते! निम्स अस्पताल में आपका... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | हेलो | Interaction |
| hi | सहायता | Interaction |

### Pattern: హలో! ఆసుపత్రిలో మీకు మార్గనిర్... -> నమస్కారం! నిమ్స్ ఆసుపత్రికి స్... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | హలో | Interaction |
| te | హలో బాబు | Interaction |

### Pattern: నేను మీకు విభాగాలు, డాక్టర్లు ... -> హలో! ఆసుపత్రిలో మీకు మార్గనిర్... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | సహాయం | Interaction |
| te | గైడ్ | Interaction |

### Pattern: Near the parking area / backsi... -> I consume electricity, not foo... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | food | Interaction |
| en | food court | Interaction |

### Pattern: मेन ब्लॉक, ग्राउंड फ्लोर।... -> पहले ओपीडी में डॉक्टर को दिखाए... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | एडमिशन काउंटर | Interaction |
| hi | भर्ती काउंटर | Interaction |

### Pattern: Main Block, Ground Floor.... -> Yes, NIMS accepts Aarogyasri a... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | insurance desk | Interaction |
| en | aarogyasri desk | Interaction |

### Pattern: मेन ब्लॉक, ग्राउंड फ्लोर।... -> हाँ, निम्स आरोग्यश्री स्वीकार ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | इंश्योरेंस डेस्क | Interaction |
| hi | आरोग्यश्री | Interaction |

### Pattern: మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... -> అవును, నిమ్స్ ఆరోగ్యశ్రీని అంగ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఇన్సూరెన్స్ డెస్క్ | Interaction |
| te | ఆరోగ్యశ్రీ | Interaction |

### Pattern: Main Block lobby.... -> Main Block, Ground Floor (Veri... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | ip billing | Interaction |
| en | inpatient billing | Interaction |

### Pattern: Main Block lobby.... -> Ground Floor, near the main en... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | billing counter | Interaction |
| en | payment counter | Interaction |

### Pattern: Radiology Department.... -> Radiology/Diagnostic Block.... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | radiology | Interaction |
| en | ct scan room | Interaction |

### Pattern: Please contact the Medical Sup... -> Please visit the Medical Super... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | feedback | Interaction |
| en | give feedback | Interaction |

### Pattern: OPD Registration Counter, Grou... -> Ground Floor, near the main en... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | outpatient register | Interaction |
| en | register opd | Interaction |

### Pattern: ओपीडी पंजीकरण काउंटर, ग्राउंड ... -> ओपीडी पंजीकरण काउंटर पर जाएं।... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | नए मरीज पंजीकरण | Interaction |
| hi | पंजीकरण करें | Interaction |

### Pattern: గ్రౌండ్ ఫ్లోర్, గది 2-6.... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | శ్వాసక్రియ సమస్య | Interaction |
| te | శ్వాస సమస్య | Interaction |

### Pattern: Please enquire at the Cardio-T... -> Ground Floor, near the main en... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | pacemaker surgery | Interaction |
| en | cardio surgery | Interaction |

### Pattern: దయచేసి కార్డియో-థొరాసిక్ సర్జర... -> దయచేసి రిసెప్షన్ డెస్క్‌లో అడగ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పేస్ మేకర్ కోసం ఎవరిని సంప్రదించాలి | Interaction |
| te | కొత్త పేస్‌మేకర్ కోసం ఎవరిని సంప్రదించాలి | Interaction |

### Pattern: Go to Emergency/Casualty IMMED... -> I am an AI robot designed to a... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | pain in chest | Interaction |
| en | left chest pain | Interaction |

### Pattern: यह दिल के लिए एक अल्ट्रासाउंड ... -> कार्डियोलॉजी, ग्राउंड फ्लोर।... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | 2डी इको | Interaction |
| hi | दिल का इको | Interaction |

### Pattern: Usually 15-30 minutes, dependi... -> Cardiology, Ground Floor.... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | time for echo | Interaction |
| en | echo time | Interaction |

### Pattern: OPD Block.... -> Hello! Welcome to NIMS Hospita... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | children department | Interaction |
| en | child specialist | Interaction |

### Pattern: OPD Block.... -> Radiology/Diagnostic Block.... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | kids doctor | Interaction |
| en | skin doctor | Interaction |

### Pattern: ఓపీడి బ్లాక్.... -> అవును, కొన్ని విభాగాలకు ఈవినిం... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | చిల్డ్రన్ డాక్టర్ | Interaction |
| te | స్కిన్ డాక్టర్ | Interaction |

### Pattern: 4th Floor, Room 410.... -> Ground Floor, near the main en... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | cancer department | Interaction |
| en | tumor surgery | Interaction |

### Pattern: పల్మనరీ మెడిసిన్ (4వ అంతస్తు) ... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | శ్వాస సమస్య | Interaction |
| te | శ్వాసకోశ సమస్య | Interaction |

### Pattern: నమస్కారం! నేను మీకు ఎలా సహాయపడ... -> నమస్కారం! నిమ్స్ ఆసుపత్రికి స్... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | హాయ్ | Interaction |
| te | హలో | Interaction |

### Pattern: Hello! Welcome to NIMS Hospita... -> Hello! I am here to help you n... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | helo | Interaction |
| en | hallo | Interaction |

### Pattern: नमस्ते! निम्स अस्पताल में आपका... -> नमस्ते! निम्स अस्पताल में आपका... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | हेलो | Interaction |
| hi | नमस्ते | Interaction |

### Pattern: Namaste! How can I guide you?... -> Hello! Welcome to NIMS Hospita... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | namaste | Interaction |
| en | greetings indian | Interaction |

### Pattern: నమస్తే! నేను మీకు ఎలా సహాయపడగల... -> నమస్కారం! నిమ్స్ ఆసుపత్రికి స్... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | నమస్తే | Interaction |
| te | నమస్కారం | Interaction |

### Pattern: मैं मदद के लिए हूं! आप मुझसे व... -> नमस्ते! मैं अस्पताल में आपका म... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | मदद | Interaction |
| hi | मदद चाहिए | Interaction |

### Pattern: నేను సహాయం చేయడానికి ఇక్కడ ఉన్... -> హలో! ఆసుపత్రిలో మీకు మార్గనిర్... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | సహాయం | Interaction |
| te | సహాయం కావాలి | Interaction |

### Pattern: Billing counter is on Ground F... -> Ground Floor, near the main en... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | bill counter | Interaction |
| en | cash counter | Interaction |

### Pattern: ओपीडी का समय कार्य दिवसों में ... -> कार्य दिवसों में सुबह 8:00 बजे... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | ओपीडी समय | Interaction |
| hi | ओपीडी टाइम | Interaction |

### Pattern: ఓపీడి సమయాలు పని దినాలలో ఉదయం ... -> పని దినాలలో ఉదయం 8:00 నుండి మధ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఓపీడి సమయం | Interaction |
| te | ఓపీడి టైమ్ | Interaction |

### Pattern: సందర్శన సమయాలు ప్రతిరోజు సాయంత... -> సందర్శకుల సమయం సాయంత్రం 4:00 న... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | సందర్శన సమయం | Interaction |
| te | ఎప్పుడు కలవచ్చు | Interaction |

### Pattern: प्रयोगशाला ग्राउंड फ्लोर, डायग... -> डायग्नोस्टिक ब्लॉक के पास ग्रा... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | लैब | Interaction |
| hi | ब्लड टेस्ट | Interaction |

### Pattern: ప్రయోగశాల గ్రౌండ్ ఫ్లోర్, డయాగ... -> డయాగ్నస్టిక్ బ్లాక్ దగ్గర గ్రౌ... (2 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ల్యాబ్ | Interaction |
| te | బ్లడ్ టెస్ట్ | Interaction |

### Pattern: General OPD -> Dental (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | mental health | Department Alias |

### Pattern: General OPD -> Paediatrics (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | pediatrics | Department Alias |

### Pattern: General Medicine -> Cardiology Unit-1 (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | मुझे बीपी है | Department |

### Pattern: General Medicine -> Orthopaedics (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఎముక వైద్యుడు | Department |

### Pattern: General Medicine -> Vascular Surgery (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | నాకు బిపి ఉంది | Department |

### Pattern: General Medicine -> Neurology (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | తల తిరగడం | Department |

### Pattern: General Medicine -> Medical Gastroenterology (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | వాంతులు | Department |

### Pattern: Cardiology Unit-1 -> Ophthalmology (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కళ్ళు బైర్లు కమ్మడం | Department |

### Pattern: Cardiology Unit-1 -> Vascular Surgery (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కాళ్లు వాపు | Department |

### Pattern: Medical Gastroenterology -> General OPD (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | लीवर की समस्या | Department |

### Pattern: Medical Gastroenterology -> Pharmacy (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | मेडिकल गैस्ट्रोएंटेरोलॉजी | Department |

### Pattern: Medical Gastroenterology -> Urology (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పసుపు రంగు మూత్రం | Department |

### Pattern: Medical Gastroenterology -> Laboratory (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | గ్యాస్ సమస్య | Department |

### Pattern: Medical Gastroenterology -> Pulmonary Medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కడుపు ఉబ్బరం | Department |

### Pattern: Pulmonary Medicine -> General OPD (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | टीबी की समस्या | Department |

### Pattern: Pulmonary Medicine -> general_medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | గొంతులో కఫం  | Department |

### Pattern: Pharmacy -> General OPD (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | पर्ची की दवा | Department |

### Pattern: Pharmacy -> General Medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మెడిసిన్ కౌంటర్ | Department |

### Pattern: Urology -> Radiology (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కిడ్నీ స్టోన్ | Department |

### Pattern: Vascular Surgery -> Paediatrics (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కాలు నల్లగా మారడం | Department |

### Pattern: Vascular Surgery -> General Medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | షుగర్ పుండు | Department |

### Pattern: Dermatology -> General Medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | చర్మ వైద్యుడు | Department |

### Pattern: Orthopaedics -> General OPD (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఎముకల డాక్టర్ | Department |

### Pattern: Neurology -> Cardiology Unit-1 (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మెదడు | Department |

### Pattern: Laboratory -> Urology (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మూత్రం లో రక్తం | Department |

### Pattern: Laboratory -> Paediatrics (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పిత్తులు యెక్కువగా వస్తున్నాయి | Department |

### Pattern: ENT -> General Medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | చెవి నొప్పి | Department |

### Pattern: Ophthalmology -> General Medicine (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | కల్లు నీరు కరటం | Department |

### Pattern: Hello! I am here to help you n... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | hello | Interaction |

### Pattern: I am an AI robot designed to a... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | machine | Interaction |

### Pattern: मैं आपको विभागों, डॉक्टरों और ... -> नमस्ते! मैं अस्पताल में आपका म... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | मदद | Interaction |

### Pattern: मैं आपको विभागों, डॉक्टरों और ... -> नमस्ते! निम्स अस्पताल में आपका... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | सहायता | Interaction |

### Pattern: Punjagutta, Hyderabad, Telanga... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | nims kaha hai | Interaction |

### Pattern: Ground Floor, near the main en... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | emergency kaha hai | Interaction |

### Pattern: Ground Floor, Super Specialty ... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | pharmacy kaha hai | Interaction |

### Pattern: Near the parking area / backsi... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | cafeteria | Interaction |

### Pattern: ICUs are located on multiple f... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | serious patient | Interaction |

### Pattern: Dr. Bheerappa Nagari.... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | chief | Interaction |

### Pattern: Please check the current time.... -> I am just a robot, but I am fu... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | opd status | Interaction |

### Pattern: Main Block, Ground Floor.... -> Consult a doctor in OPD first.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | admission desk | Interaction |

### Pattern: మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... -> ముందుగా ఓపీడిలో డాక్టర్‌ని కలవ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | అడ్మిషన్ కౌంటర్ | Interaction |

### Pattern: Main Block, Ground Floor (Veri... -> I go to my charging station wh... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | discharge counter | Interaction |

### Pattern: Main Block, Ground Floor (Veri... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | final counter | Interaction |

### Pattern: Main Block, Ground Floor (Veri... -> After the doctor signs the sum... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | leave hospital desk | Interaction |

### Pattern: मेन ब्लॉक, ग्राउंड फ्लोर।... -> जब मैं थक जाता हूं तो मैं अपने... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | डिस्चार्ज काउंटर | Interaction |

### Pattern: మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... -> నేను అలసిపోయినప్పుడు నా ఛార్జి... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | డిశ్చార్జ్ కౌంటర్ | Interaction |

### Pattern: Ground Floor, near Diagnostic ... -> Please go to Emergency / Casua... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | blood test | Interaction |

### Pattern: Report Dispatch Counter in Dia... -> Ground Floor, near Diagnostic ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | lab report | Interaction |

### Pattern: Yes, NIMS accepts Aarogyasri a... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | government scheme | Interaction |

### Pattern: Main Block, Ground Floor.... -> Hello! I am here to help you n... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | help desk | Interaction |

### Pattern: Radiology Department, Ground F... -> Radiology/Diagnostic Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | radiology | Interaction |

### Pattern: रेडियोलॉजी विभाग, ग्राउंड फ्लो... -> रेडियोलॉजी ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | स्कैन | Interaction |

### Pattern: Please ask at the Report Dispa... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | where is my report | Interaction |

### Pattern: Report to Medical Records Dept... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | where is my file | Interaction |

### Pattern: अपनी ओपी आईडी के साथ मेडिकल रि... -> ग्राउंड फ्लोर, सुपर स्पेशियलिट... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | मेडिकल फाइल | Interaction |

### Pattern: Lifts are available in all maj... -> I am an AI robot designed to a... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | stairs | Interaction |

### Pattern: Lifts are available in all maj... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | upper floor | Interaction |

### Pattern: Designated parking is availabl... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | vehicle park | Interaction |

### Pattern: Designated parking is availabl... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | where to park | Interaction |

### Pattern: Main Block.... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | admin counter | Interaction |

### Pattern: मेन ब्लॉक लॉबी।... -> मेन ब्लॉक, ग्राउंड फ्लोर।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | बिलिंग | Interaction |

### Pattern: మెయిన్ బ్లాక్ లాబీ.... -> మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | బిల్లింగ్ | Interaction |

### Pattern: डायग्नोस्टिक ब्लॉक।... -> डायग्नोस्टिक ब्लॉक के पास ग्रा... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | लैब | Interaction |

### Pattern: డయాగ్నస్టిక్ బ్లాక్.... -> డయాగ్నస్టిక్ బ్లాక్ దగ్గర గ్రౌ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ల్యాబ్ | Interaction |

### Pattern: Near the OPD entrance or Main ... -> OTs are on respective floors (... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | photocopy | Interaction |

### Pattern: Near the OPD entrance or Main ... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | copy machine shop | Interaction |

### Pattern: Yes, select departments have e... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | after noon clinic | Interaction |

### Pattern: Yes, select departments have e... -> Radiology/Diagnostic Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | doctor evening | Interaction |

### Pattern: అవును, కొన్ని విభాగాలకు ఈవినిం... -> పంజాగుట్ట, హైదరాబాద్, తెలంగాణ ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | సాయంత్రం ఆసుపత్రి ఎక్కడ ఉంది | Interaction |

### Pattern: रेडियोलॉजी विभाग।... -> रेडियोलॉजी ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | स्कैन | Interaction |

### Pattern: రేడియాలజీ విభాగం.... -> రేడియాలజీ విభాగం, గ్రౌండ్ ఫ్లో... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | స్కాన్ | Interaction |

### Pattern: Visit the OPD Registration Cou... -> Radiology/Diagnostic Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | doctor meet | Interaction |

### Pattern: ఓపీడి రిజిస్ట్రేషన్ కౌంటర్‌కు ... -> మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | రిజిస్ట్రేషన్ | Interaction |

### Pattern: ఓపీడి రిజిస్ట్రేషన్ కౌంటర్‌కు ... -> అవును, కొన్ని విభాగాలకు ఈవినిం... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | డాక్టర్ కలవాలి | Interaction |

### Pattern: Please contact the Medical Sup... -> I am an AI robot designed to a... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | complaint | Interaction |

### Pattern: कृपया चिकित्सा अधीक्षक कार्याल... -> कृपया चिकित्सा अधीक्षक कार्याल... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | शिकायत | Interaction |

### Pattern: OPD Registration Counter, Grou... -> Visit the OPD Registration Cou... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | op registration | Interaction |

### Pattern: ఓపీడి రిజిస్ట్రేషన్ కౌంటర్, గ్... -> మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | రిజిస్ట్రేషన్ | Interaction |

### Pattern: Common blood tests like sugar ... -> I consume electricity, not foo... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | without food | Interaction |

### Pattern: Common blood tests like sugar ... -> Please go to Emergency / Casua... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | blood test fasting | Interaction |

### Pattern: शुगर या कोलेस्ट्रॉल जैसे सामान... -> डायग्नोस्टिक ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | टेस्ट के लिए | Interaction |

### Pattern: शुगर या कोलेस्ट्रॉल जैसे सामान... -> पार्किंग क्षेत्र के पास / ओपीड... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | खाना खा सकते | Interaction |

### Pattern: షుగర్ లేదా కొలెస్ట్రాల్ వంటి ర... -> పార్కింగ్ ఏరియా దగ్గర / ఓపీడి ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | నేను ఆహారం తీసుకోవచ్చా | Interaction |

### Pattern: हाँ, डॉक्टर की सलाह के अनुसार ... -> पहले ओपीडी में डॉक्टर को दिखाए... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | भर्ती मरीज | Interaction |

### Pattern: అవును, డాక్టర్ సలహా ప్రకారం పే... -> మెయిన్ బ్లాక్ లాబీ.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఇన్ పేషెంట్ | Interaction |

### Pattern: Carry Aadhaar card, past recor... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | which documents | Interaction |

### Pattern: Please check the NIMS website ... -> Hello! I am here to help you n... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | helpline | Interaction |

### Pattern: हाँ, अधिकांश काउंटरों पर डिजिट... -> मेन ब्लॉक लॉबी।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | डिजिटल भुगतान | Interaction |

### Pattern: అవును, చాలా కౌంటర్లలో డిజిటల్ ... -> మెయిన్ బ్లాక్ లాబీ.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | డిజిటల్ పేమెంట్ | Interaction |

### Pattern: Ground Floor, Rooms 2-6.... -> Radiology/Diagnostic Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | heart doctor | Interaction |

### Pattern: Cardiology, Ground Floor.... -> Ground Floor, Rooms 2-6.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | echocardiography | Interaction |

### Pattern: Cardiology, Ground Floor.... -> Radiology Department.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | scan echo | Interaction |

### Pattern: कार्डियोलॉजी विभाग के अंदर।... -> डायग्नोस्टिक ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | स्ट्रेस टेस्ट | Interaction |

### Pattern: కార్డియాలజీ విభాగం లోపల.... -> డయాగ్నస్టిక్ బ్లాక్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | ఒత్తిడి పరీక్ష యంత్రం | Interaction |

### Pattern: It is an ultrasound test for t... -> Ground Floor, Rooms 2-6.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | echocardiography | Interaction |

### Pattern: यह दिल के लिए एक अल्ट्रासाउंड ... -> डायग्नोस्टिक ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | इको टेस्ट | Interaction |

### Pattern: आमतौर पर 15-30 मिनट।... -> डायग्नोस्टिक ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | टेस्ट टाइम | Interaction |

### Pattern: సాధారణంగా 15-30 నిమిషాలు.... -> డయాగ్నస్టిక్ బ్లాక్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పరీక్షలకు ఎంత సమయం ఉంది | Interaction |

### Pattern: नहीं, यह दर्द रहित हैं।... -> डायग्नोस्टिक ब्लॉक।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | टेस्ट दर्द | Interaction |

### Pattern: Please check the OP Block dire... -> I am an AI robot designed to a... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | brain department | Interaction |

### Pattern: Please check the OP Block dire... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | nerve doctor | Interaction |

### Pattern: OPD Block.... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | dermatology | Interaction |

### Pattern: 6th Floor, Rooms 609-611.... -> Please visit the Medical Super... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | urine problem | Interaction |

### Pattern: 6वीं मंजिल, कमरा 609-611।... -> कृपया चिकित्सा अधीक्षक कार्याल... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | पेशाब समस्या | Interaction |

### Pattern: 6వ అంతస్తు, గది 609-611.... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | మూత్ర సమస్య | Interaction |

### Pattern: Dental Department, OPD Block.... -> Radiology/Diagnostic Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | tooth doctor | Interaction |

### Pattern: Dental Department, OPD Block.... -> Please visit the Medical Super... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | teeth problem | Interaction |

### Pattern: డెంటల్ విభాగం, ఓపీడి బ్లాక్.... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | దంతాల సమస్య  | Interaction |

### Pattern: Visit Pulmonary Medicine (4th ... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | breathing problem | Interaction |

### Pattern: Visit Dermatology.... -> OPD Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | rashes | Interaction |

### Pattern: Visit Dermatology.... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | itching | Interaction |

### Pattern: Visit Dermatology.... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | skin allergy | Interaction |

### Pattern: చర్మ వ్యాధుల విభాగానికి వెళ్లం... -> దయచేసి మెడికల్ సూపరింటెండెంట్ ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | చర్మ సంబంధిత సమస్య | Interaction |

### Pattern: Visit Urology (6th Floor).... -> I am an AI robot designed to a... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | urine pain | Interaction |

### Pattern: Visit Urology (6th Floor).... -> Radiology/Diagnostic Block.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | urinary infection | Interaction |

### Pattern: Visit Gastroenterology (5th Fl... -> Ground Floor, near the main en... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | severe stomach ache | Interaction |

### Pattern: Visit Dental Department.... -> OTs are on respective floors (... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | toothache | Interaction |

### Pattern: డెంటల్ విభాగానికి వెళ్లండి.... -> డెంటల్ విభాగం, ఓపీడి బ్లాక్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పంటి నొప్పి | Interaction |

### Pattern: Hello! How can I help you toda... -> Hello! I am here to help you n... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | helo | Interaction |

### Pattern: नमस्ते! निम्स अस्पताल में आपका... -> नमस्ते! मैं अस्पताल में आपका म... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | हैलो | Interaction |

### Pattern: Good morning! How can I assist... -> Hello! Welcome to NIMS Hospita... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | good morning | Interaction |

### Pattern: I'm here to help! You can ask ... -> I can guide you to departments... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | support | Interaction |

### Pattern: मैं मदद के लिए हूं! आप मुझसे व... -> नमस्ते! निम्स अस्पताल में आपका... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | सहायता | Interaction |

### Pattern: Billing counter is on Ground F... -> Main Block, Ground Floor (Veri... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | billing | Interaction |

### Pattern: बिलिंग काउंटर ग्राउंड फ्लोर, म... -> मेन ब्लॉक, ग्राउंड फ्लोर।... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | बिलिंग | Interaction |

### Pattern: బిల్లింగ్ కౌంటర్ గ్రౌండ్ ఫ్లోర... -> మెయిన్ బ్లాక్, గ్రౌండ్ ఫ్లోర్.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | బిల్లింగ్ | Interaction |

### Pattern: బిల్లింగ్ కౌంటర్ గ్రౌండ్ ఫ్లోర... -> మెయిన్ బ్లాక్ లాబీ.... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| te | పేమెంట్ | Interaction |

### Pattern: Lab reports can be collected f... -> Ground Floor, near Diagnostic ... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | lab report | Interaction |

### Pattern: मिलने का समय रोज शाम 4:00 से 6... -> मिलने का समय शाम 4:00 बजे से श... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| hi | मिलने का समय | Interaction |

### Pattern: Most departments are open from... -> I am just a robot, but I am fu... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | department status | Interaction |

### Pattern: Laboratory is on Ground Floor,... -> Please go to Emergency / Casua... (1 cases)
| Lang | Input Question | Type |
| :--- | :--- | :--- |
| en | blood test | Interaction |

## 2. NLU Misses (The Safe Failures)
These questions returned `None`. This usually happens for multi-word phrases that fuzzy matching missed.
To fix these, we can lower `fuzzy_threshold` or add more specific keywords.

### Cardiology Unit-1 (te)
- ఛాతీలో బిగుతుగా ఉండటం

### Cardiology Unit-2 (hi)
- धड़कन बढ़ना

### Cardiology Unit-2 (te)
- శ్వాస బరువుగా వుంది

### ENT (hi)
- गला

### General Medicine (te)
- కంటి శాస్త్ర విభాగము
- చలి

### General OPD (hi)
- डॉक्टर को दिखाना है

### General OPD (te)
- సలహా కోసం

### Laboratory (te)
- మలం లో రక్తం

### Medical Gastroenterology (hi)
- बार-बार उल्टी होना

### Medical Gastroenterology (te)
- మలం లో రక్తం

### Ophthalmology (hi)
- दिखाई नहीं दे रहा

### Ophthalmology (te)
- కంటి శాస్త్ర విభాగము

### Pharmacy (hi)
- दवा

### Pulmonary Medicine (hi)
- दमा
- फेफड़ों की बीमारी

### Pulmonary Medicine (te)
- శ్వాస తీసుకోవడంలో ఇబ్బంది
- కఫం

### Radiology (te)
- రిపోర్టులు ఎక్కడ ఇస్తారు

### Urology (te)
- మూత్ర విసర్జనలో ఇబ్బంది

### Vascular Surgery (hi)
- पैर में घाव जो ठीक न हो
- पैर में खून का थक्का

### Vascular Surgery (te)
- మానని పాదాల పుండు
- పాదాల పుండు

