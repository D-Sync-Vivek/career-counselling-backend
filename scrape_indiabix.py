import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import re
import time
import os

def clean_text(text):
    """Removes weird spacing and unsupported characters for the PDF."""
    if not text: return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text.encode('latin-1', 'ignore').decode('latin-1')

def sanitize_filename(name):
    """Removes illegal characters from topic names to create safe file names."""
    safe_name = re.sub(r'[\\/*?:"<>|]', "", name)
    return safe_name.replace(" ", "_") + ".pdf"

def get_all_topics(index_url):
    """Scrapes the main index page to find every topic folder."""
    print(f"Scanning main directory: {index_url} ...")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    response = requests.get(index_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    topics = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # Break the URL into parts, completely ignoring trailing or double slashes
        parts = [p for p in href.split('/') if p]
        
        # THE BULLETPROOF FILTER:
        # We want links where the parent folder is exactly 'aptitude'
        if len(parts) >= 2 and parts[-2] == 'aptitude' and parts[-1] != 'questions-and-answers':
            topic_name = a.get_text(strip=True)
            
            # Ignore empty links or pure numbers in the UI
            if len(topic_name) > 2 and not topic_name.isdigit():
                topic_slug = parts[-1]
                full_url = f"https://www.indiabix.com/aptitude/{topic_slug}/"
                
                # Prevent duplicates from mobile/desktop responsive menus
                if not any(t['url'] == full_url for t in topics):
                    topics.append({'name': topic_name, 'url': full_url})
                    
    return topics

def scrape_topic_to_pdf(start_url, output_filename, topic_name):
    """Scrapes all pages of a specific topic and compiles them into a PDF."""
    print(f"\n==================================================")
    print(f"📥 Starting topic: {topic_name}")
    print(f"==================================================")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=f"Aptitude: {topic_name}", ln=True, align='C')
    pdf.ln(5)

    current_url = start_url
    page_count = 1
    global_q_num = 1

    while current_url:
        print(f"--> Fetching Page {page_count}: {current_url}")
        response = requests.get(current_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        questions = soup.find_all('div', class_='bix-div-container')
        if not questions:
            print("No questions found on this page. Stopping.")
            break

        for q in questions:
            q_text_div = q.find('div', class_='bix-td-qtxt')
            q_text = clean_text(q_text_div.get_text()) if q_text_div else "Question text not found."
            
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 8, txt=f"Q{global_q_num}. {q_text}")
            pdf.set_font("Arial", size=12)

            options = q.find_all('div', class_='bix-td-option-val')
            labels = ['A', 'B', 'C', 'D', 'E']
            for idx, opt in enumerate(options):
                opt_text = clean_text(opt.get_text())
                pdf.multi_cell(0, 8, txt=f"   {labels[idx]}) {opt_text}")

            ans_input = q.find('input', class_='jq-hdnakq')
            answer_val = ans_input['value'] if ans_input else "Unknown"
            
            pdf.ln(2)
            pdf.set_font("Arial", 'I', 11)
            pdf.multi_cell(0, 8, txt=f"Correct Answer: Option {answer_val}")
            pdf.set_font("Arial", size=12)
            pdf.ln(5)
            
            global_q_num += 1

        next_page_link = None
        for a in soup.find_all('a', href=True):
            text = a.get_text().strip().lower()
            if ('next' in text or '»' in text) and a['href'] != '#':
                next_page_link = a['href']
                if next_page_link.startswith('/'):
                    next_page_link = "https://www.indiabix.com" + next_page_link
                break
        
        if next_page_link and next_page_link != current_url:
            current_url = next_page_link
            page_count += 1
            time.sleep(1) # Short pause between pages
        else:
            break

    pdf.output(output_filename)
    print(f"✅ Success! Saved {global_q_num - 1} questions to {output_filename}")


# =====================================================================
# THE MASTER LAUNCHER
# =====================================================================
if __name__ == "__main__":
    main_index_url = "https://www.indiabix.com/aptitude/questions-and-answers/"
    
    # 1. Get all topics
    all_topics = get_all_topics(main_index_url)
    print(f"🎯 Found {len(all_topics)} different aptitude topics to scrape!\n")
    
    if len(all_topics) == 0:
        print("Wait, 0 topics found. Exiting to prevent empty loops.")
        exit()
        
    # 2. Create a folder to store the PDFs
    output_folder = "Aptitude_PDFs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # 3. Loop through every topic and scrape
    for topic in all_topics:
        file_path = os.path.join(output_folder, sanitize_filename(topic['name']))
        
        # Check if we already downloaded this PDF (allows resuming)
        if os.path.exists(file_path):
            print(f"⏩ Skipping '{topic['name']}' -> PDF already exists.")
            continue
            
        # Scrape and save
        scrape_topic_to_pdf(topic['url'], file_path, topic['name'])
        
        # ANTI-BAN COOLDOWN: Wait 5 seconds before hitting the next topic folder
        print("⏳ Taking a 5-second breather to avoid IP ban...")
        time.sleep(5)
        
    print("\n🎉 MASTER SCRAPE COMPLETE! All PDFs are in the 'Aptitude_PDFs' folder.")