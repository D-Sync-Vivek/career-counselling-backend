import os
import requests
import time

# --- Configuration ---
API_URL = "http://localhost:8000/api/v1/ingest/aptitude"
PDF_FOLDER = "Aptitude_PDFs"

# --- The Curriculum Map ---
# This dictionary tells the script exactly how to tag each file.
# If a file isn't listed here, it will use the default fallback at the bottom.
CURRICULUM_MAP = {
    "Problems_on_Ages.pdf": {"category": "Quantitative Aptitude", "topic": "Problems on Ages", "grade": "6-8", "diff": "Medium"},
    "Percentage.pdf": {"category": "Quantitative Aptitude", "topic": "Percentage", "grade": "6-8", "diff": "Medium"},
    "Ratio_and_Proportion.pdf": {"category": "Quantitative Aptitude", "topic": "Ratio and Proportion", "grade": "6-8", "diff": "Hard"},
    
    "Time_and_Work.pdf": {"category": "Quantitative Aptitude", "topic": "Time and Work", "grade": "9-10", "diff": "Hard"},
    "Profit_and_Loss.pdf": {"category": "Quantitative Aptitude", "topic": "Profit and Loss", "grade": "9-10", "diff": "Medium"},
    "Simple_Interest.pdf": {"category": "Quantitative Aptitude", "topic": "Simple Interest", "grade": "9-10", "diff": "Medium"},
    "Compound_Interest.pdf": {"category": "Quantitative Aptitude", "topic": "Compound Interest", "grade": "9-10", "diff": "Hard"},
    "Time_and_Distance.pdf": {"category": "Quantitative Aptitude", "topic": "Time and Distance", "grade": "9-10", "diff": "Medium"},
    
    "Probability.pdf": {"category": "Quantitative Aptitude", "topic": "Probability", "grade": "11-12", "diff": "Hard"},
    "Permutation_and_Combination.pdf": {"category": "Quantitative Aptitude", "topic": "Permutation & Combination", "grade": "11-12", "diff": "Hard"},
    "Logarithm.pdf": {"category": "Quantitative Aptitude", "topic": "Logarithm", "grade": "11-12", "diff": "Hard"}
}

DEFAULT_MAPPING = {"category": "General Aptitude", "grade": "9-10", "diff": "Medium"}

def upload_pdfs_to_db():
    if not os.path.exists(PDF_FOLDER):
        print(f"❌ Folder '{PDF_FOLDER}' not found. Did you run the scraper yet?")
        return

    files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    
    if not files:
        print("📂 No PDFs found in the folder.")
        return

    print(f"🚀 Found {len(files)} PDFs. Starting bulk ingestion to Vector Database...\n")

    success_count = 0
    fail_count = 0

    for filename in files:
        file_path = os.path.join(PDF_FOLDER, filename)
        
        # 1. Determine the Metadata
        mapping = CURRICULUM_MAP.get(filename)
        if mapping:
            category = mapping["category"]
            topic = mapping["topic"]
            grade = mapping["grade"]
            diff = mapping["diff"]
        else:
            # Fallback for topics not explicitly mapped
            clean_topic_name = filename.replace("_", " ").replace(".pdf", "")
            category = DEFAULT_MAPPING["category"]
            topic = clean_topic_name
            grade = DEFAULT_MAPPING["grade"]
            diff = DEFAULT_MAPPING["diff"]

        print(f"📤 Uploading: {topic} (Grade: {grade}, Diff: {diff})...")

        # 2. Prepare the payload for FastAPI
        data = {
            "category": category,
            "topic": topic,
            "target_grade": grade,
            "difficulty": diff
        }

        # 3. Open the file and send the POST request
        try:
            with open(file_path, "rb") as f:
                files_payload = {"file": (filename, f, "application/pdf")}
                
                response = requests.post(API_URL, data=data, files=files_payload)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Success! {result['chunks_processed']} chunks vectorized.")
                    success_count += 1
                else:
                    print(f"   ❌ Failed. Status: {response.status_code}, Error: {response.text}")
                    fail_count += 1
                    
        except requests.exceptions.ConnectionError:
            print("   🚨 ERROR: Could not connect to the backend. Is your FastAPI server running?")
            break
        except Exception as e:
            print(f"   🚨 Unexpected Error: {str(e)}")
            fail_count += 1
            
        # Slight pause so we don't overwhelm the local PostgreSQL database
        time.sleep(1)

    print(f"\n🎉 Bulk Upload Complete! Successfully ingested: {success_count} | Failed: {fail_count}")

if __name__ == "__main__":
    upload_pdfs_to_db()