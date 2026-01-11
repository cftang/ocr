import base64
import os
import requests
import glob
import re
import logging
import time

# PaddleOCR-VL API
# https://aistudio.baidu.com/paddleocr/task

API_URL = "https://udhfacndh547rerf.aistudio-app.com/layout-parsing"
TOKEN = "56aa1eb1132ddfc27ccf9093de91caade39c84aa"
OUTPUT_FILE = "transcript_mcp.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def numeric_sort_key(s):
    """Sort strings by embedded numbers."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def clean_text(text):
    """Clean up whitespace."""
    if not text:
        return ""
    return text.strip()

def process_one_file(file_path):
    # file_path = "screenshot0.png"
    logging.info(f"Uploading {file_path}")

    try:
        with open(file_path, "rb") as file:
            file_bytes = file.read()
            file_data = base64.b64encode(file_bytes).decode("ascii")

        headers = {
            "Authorization": f"token {TOKEN}",
            "Content-Type": "application/json"
        }

        required_payload = {
            "file": file_data,
            "fileType": 1,  # For PDF documents, set `fileType` to 0; for images, set `fileType` to 1
        }

        optional_payload = {
            "useDocOrientationClassify": False,
            "useDocUnwarping": False,
            "useChartRecognition": False,
        }

        payload = {**required_payload, **optional_payload}

        start_time = time.time()
        response = requests.post(API_URL, json=payload, headers=headers)
        # print(response.status_code)
        
        if response.status_code != 200:
            logging.error(f"API Error {response.status_code}: {response.text}")
            return None

        result = response.json().get("result")
        if not result:
            logging.warning("No result found in response")
            return None

        full_text = []
        if 'layoutParsingResults' in result:
             for res in result['layoutParsingResults']:
                if 'markdown' in res and 'text' in res['markdown']:
                     full_text.append(res['markdown']['text'])
        
        return clean_text("\n".join(full_text))

    except Exception as e:
        logging.error(f"Failed to process {file_path}: {e}")
        return None

def main():
    # Gather both frame*.jpg (from split3.py) and screenshot*.png, just in case
    files = glob.glob("screenshot*.png") + glob.glob("frame*.jpg")
    files.sort(key=numeric_sort_key)
    
    if not files:
        logging.error("No screenshot*.png or frame*.jpg files found.")
        return
    
    logging.info(f"Found {len(files)} files to process.")
    
    buffer_text = ""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for filename in files:
            logging.info(f"---- Processing {filename} ----")
            new_text = process_one_file(filename)
            
            if not new_text:
                continue
            
            # Deduplication Logic
            if not buffer_text:
                buffer_text = new_text
                logging.info(f"Buffered (Start): {buffer_text[:50]}...")
            else:
                if new_text == buffer_text:
                    # Exact duplicate
                    logging.info("Duplicate content (skip)")
                    pass 
                elif new_text in buffer_text:
                    # New text is a partial substring of existing buffer -> Ignore new
                    logging.info("Partial subset of buffer (skip)")
                    pass
                elif buffer_text in new_text:
                    # Existing buffer is a partial substring of new text -> Update to new
                    buffer_text = new_text
                    logging.info(f"Buffered (Expanded to better version): {buffer_text[:50]}...")
                else:
                    # Significant change -> Write old buffer, start new
                    logging.info(f"Content changed. Writing previous buffer.")
                    f.write(buffer_text + "\n")
                    f.flush()
                    
                    buffer_text = new_text
                    logging.info(f"Buffered (New): {buffer_text[:50]}...")

        # Write final buffer
        if buffer_text:
            logging.info(f"Writing final buffer.")
            f.write(buffer_text + "\n")

    logging.info(f"Done. Transcript saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
