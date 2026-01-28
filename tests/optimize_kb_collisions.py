import json
import os
import shutil

# Correct Mappings based on Analysis
# Format: "keyword": "Target_Dept_ID" (If target is None, remove from all except target? No, logic is stricter).
# Better Logic:
# 1. REMOVE these keywords from 'general_medicine' because they belong to Specialists
REMOVE_FROM_GEN_MED = [
    # English
    "eye", "ent", "ear", "nose", "throat", "skin", "rashes", "itching",
    "stomach pain", "urine problem", "high bp", "low bp", "ortho", "bone",
    "ophthalmology", "dermatology", "orthopaedics", "blood in stools",
    
    # Hindi
    "ईएनटी", "आंख", "कान", "नाक", "गला", "उच्च रक्तचाप", "निम्न रक्तचाप", "बीपी", "हाई बीपी", "लो बीपी",
    "खुजली", "चर्म रोग", "पेट दर्द", "हड्डी", "सांस", 

    # Telugu
    "ఈఎన్టీ", "కన్ను", "చెవి", "ముక్కు", "గొంతు", "చర్మ వ్యాధి", "దురద", 
    "ఎముక", "ఎముకల", "ఎముకల డాక్టర్", "బీపీ", "హై బీపీ", "లో బీపీ", "అధిక రక్తపోటు", "అల్ప రక్తపోటు",
    "కడుపు నొప్పి", "శ్వాస"
]

# 2. REMOVE these from 'general_opd' because they belong to General Medicine
REMOVE_FROM_GEN_OPD = [
    # English
    "fever", "weakness", "vomiting", "headache", "body pain", "cold", "pain",
    "not feeling well", "stomach pain", # sometimes mapped here
    
    # Hindi
    "बुखार", "कमजोरी", "बदन दर्द", "शरीर दर्द", "दर्द", "बीमारी", "ठीक नहीं लग रहा",
    
    # Telugu
    "జ్వరం", "నీరసం", "ఒళ్ళు నొప్పులు", "శరీర నొప్పి", "నొప్పి", "తాపం", "బలహీనత", "అస్వస్థత"
]

# 3. INTERACTION CLEANUP: Remove these from interactions to let Departments handle them
REMOVE_FROM_INTERACTIONS = [
    # English
    "chest pain", "heart attack", "dental", "dentist", "neurology", 
    "cardiology", "heart pain", "severe chest pain", "pacemaker", 
    
    # Hindi
    "दिल का दौरा", "सीने में दर्द", "डेंटल", "कार्डियोलॉजी", "हार्ट अटैक", "चक्कर आना",
    
    # Telugu
    "ఛాతీ నొప్పి", "గుండెపోటు", "డెంటల్", "కార్డియాలజీ", "గుండె నొప్పి"
]

import unicodedata

def normalize_text(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFC', text).lower().strip()
    return text

def optimize_kb():
    print("Starting KB Optimization Script...")
    kb_path = "hospital_knowledge_base.json"
    backup_path = "hospital_knowledge_base.json.bak"
    
    # Backup
    if not os.path.exists(backup_path):
        shutil.copy(kb_path, backup_path)
        print(f"Backed up KB to {backup_path}")

    with open(kb_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Pre-normalize removal lists for faster lookup
    norm_remove_gen_med = set(normalize_text(x) for x in REMOVE_FROM_GEN_MED)
    norm_remove_gen_opd = set(normalize_text(x) for x in REMOVE_FROM_GEN_OPD)
    norm_remove_interactions = set(normalize_text(x) for x in REMOVE_FROM_INTERACTIONS)

    # 1. Clean Departments
    for dept in data.get("departments", []):
        dept_id = dept["id"]
        
        # Cleanup General Medicine
        if dept_id == "general_medicine":
            if "keywords" in dept:
                for lang in dept["keywords"]:
                    original = dept["keywords"][lang]
                    # Filter
                    cleaned = [k for k in original if normalize_text(k) not in norm_remove_gen_med]
                    
                    removed_count = len(original) - len(cleaned)
                    if removed_count > 0:
                        print(f"[General Medicine] Removed {removed_count} specialist keywords from '{lang}'")
                    
                    dept["keywords"][lang] = cleaned

        # Cleanup General OPD
        if dept_id == "general_opd":
            if "keywords" in dept:
                for lang in dept["keywords"]:
                    original = dept["keywords"][lang]
                    
                    if lang in ['hi'] and dept_id == 'general_opd':
                        print("DEBUG HEX COMPARISON:")
                        
                        # Print first few from removal list
                        bukhar_list = [x for x in norm_remove_gen_opd if "बुखार" in x] # Try substring match?
                        for x in list(norm_remove_gen_opd)[:5]:
                             print(f"  LIST Item: {ascii(x)} -> {[hex(ord(c)) for c in x]}")

                        for k in original:
                            nk = normalize_text(k)
                            print(f"  JSON Item: {ascii(k)} -> Norm: {ascii(nk)} -> {[hex(ord(c)) for c in nk]}")
                            if nk in norm_remove_gen_opd:
                                print(f"  MATCH FOUND: {ascii(k)}")
                            elif "बुखार" in nk:
                                 print(f"  PARTIAL 'बुखार' FOUND but exact match failed! Normalized: {ascii(nk)}")

                    cleaned = [k for k in original if normalize_text(k) not in norm_remove_gen_opd]
                    
                    removed_count = len(original) - len(cleaned)
                    if removed_count > 0:
                        print(f"[General OPD] Removed {removed_count} medical keywords from '{lang}'")
                    
                    dept["keywords"][lang] = cleaned

    # 2. Clean Interactions
    for interaction in data.get("interactions", []):
        if "keywords" in interaction:
            for lang in interaction["keywords"]:
                original = interaction["keywords"][lang]
                cleaned = [k for k in original if normalize_text(k) not in norm_remove_interactions]
                
                removed_count = len(original) - len(cleaned)
                if removed_count > 0:
                    print(f"[Interaction: {interaction['id']}] Removed {removed_count} colliding keywords from '{lang}'")
                
                interaction["keywords"][lang] = cleaned

    # Save
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("\nOptimization Complete. Saved to 'hospital_knowledge_base.json'.")

if __name__ == "__main__":
    optimize_kb()
