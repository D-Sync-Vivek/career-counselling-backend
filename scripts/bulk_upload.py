import os
import requests
import time

API_URL = "http://localhost:8000/api/v1/ingest/aptitude"

# Define the folders and their corresponding categories
# (Removed Aptitude_PDFs since it was already ingested)
FOLDERS_TO_PROCESS = {
    "Logical_PDFs": "Logical Reasoning",
    "Verbal_PDFs": "Verbal Ability"
}

# Add any specific Grade/Difficulty mappings here. 
# If a file isn't listed, it defaults to Grade 9-10 / Medium.
CURRICULUM_MAP = {
    "Blood_Relation_Test.pdf": {"grade": "9-10", "diff": "Medium"},
    "Syllogism.pdf": {"grade": "11-12", "diff": "Hard"},
    "Synonyms.pdf": {"grade": "6-8", "diff": "Medium"},
    "Antonyms.pdf": {"grade": "6-8", "diff": "Medium"},
}

def upload_all_folders():
    total_success = 0
    total_fail = 0

    for folder_name, category_name in FOLDERS_TO_PROCESS.items():
        if not os.path.exists(folder_name):
            print(f"⏩ Skipping {folder_name} (Folder not found)")
            continue

        files = [f for f in os.listdir(folder_name) if f.endswith(".pdf")]
        print(f"\n🚀 Processing {len(files)} files in {folder_name} as '{category_name}'...\n")

        for filename in files:
            file_path = os.path.join(folder_name, filename)
            clean_topic_name = filename.replace("_", " ").replace(".pdf", "")
            
            # Get metadata or use default
            mapping = CURRICULUM_MAP.get(filename, {"grade": "9-10", "diff": "Medium"})

            print(f"📤 Uploading: {clean_topic_name}...")

            data = {
                "category": category_name, # Dynamically uses Verbal or Logical
                "topic": clean_topic_name,
                "target_grade": mapping["grade"],
                "difficulty": mapping["diff"]
            }

            try:
                with open(file_path, "rb") as f:
                    files_payload = {"file": (filename, f, "application/pdf")}
                    response = requests.post(API_URL, data=data, files=files_payload)
                    
                    if response.status_code == 200:
                        total_success += 1
                    else:
                        print(f"   ❌ Failed: {response.text}")
                        total_fail += 1
            except Exception as e:
                print(f"   🚨 Error: {str(e)}")
                total_fail += 1
                
            time.sleep(1) # DB breather

    print(f"\n🎉 Master Upload Complete! Success: {total_success} | Failed: {total_fail}")

if __name__ == "__main__":
    upload_all_folders()