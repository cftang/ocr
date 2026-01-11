import time
import sys
import threading
import pyautogui
import cv2
import numpy as np
from paddleocr import PaddleOCR
from pynput import mouse

# Configuration
INTERVAL = 1.0  # Seconds between captures
OUTPUT_FILE = "transcript.txt"

# Global variables for region selection
points = []
selection_complete = threading.Event()

def on_click(x, y, button, pressed):
    if pressed:
        points.append((x, y))
        print(f"Point recorded: {x}, {y}")
        if len(points) >= 1:
            selection_complete.set()
            return False  # Stop listener

def get_screen_region():
    print("Please click the Top-Left corner and then the Bottom-Right corner of the caption area.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
    left, top = points[0]
    # x2, y2 = points[1]
    
    # left = min(x1, x2)
    # top = min(y1, y2)
    # width = abs(x1 - x2)
    # height = abs(y1 - y2)
    width = 1000
    height = 30
    print(f"Region selected: Left={left}, Top={top}, Width={width}, Height={height}")
    # return (left, top, width, height)
    return (left, top, width, height)

def main():
    # 1. Select Region
    region = get_screen_region()
    # region=(left, top, width, height)
    # region = (771, 786, 1000, 30)
    
    # 2. Initialize PaddleOCR
    print("Initializing PaddleOCR...")
    ocr = PaddleOCR(use_textline_orientation=True, lang='ch')  # Simplified Chinese
    print("OCR Initialized. Starting capture loop. Press Ctrl+C to stop.")

    buffer_text = ""
    
    try:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            cnt = 0
            while True:
                start_time = time.time()
                
                # Capture Screenshot
                try:
                    screenshot = pyautogui.screenshot(region=region)
                    filename="screenshot{}.png".format(cnt)
                    print("save to {}".format(filename))
                    screenshot.save(filename)
                    cnt += 1
                    
                    # # Display image of filename
                    # img_show = cv2.imread(filename)
                    # if img_show is not None:
                    #     cv2.imshow("Captured Screenshot", img_show)
                    #     cv2.waitKey(1)

                    # Convert to format suitable for PaddleOCR (numpy array)
                    img_np = np.array(screenshot)
                    # RGB to BGR (PaddleOCR uses BGR/RGB? standard cv2 is BGR, but Paddle usually handles both or expects specific. 
                    # PaddleOCR 'ocr' function accepts ndarray. It usually works with RGB from PIL directly or BGR from cv2.
                    # Let's keep it as RGB or convert if results are bad. Standard cv2 is BGR. 
                    # pyautogui returns RGB PIL image.
                except Exception as e:
                    print(f"Screenshot failed: {e}")
                    continue

                # Run OCR
                try:
                    result = ocr.predict(img_np)
                except Exception as e:
                    print(f"OCR failed: {e}")
                    result = None
                
                current_text_lines = []
                if result and result[0]:
                    for line in result[0]:
                        # line format: [[coords], [text, confidence]]
                        text = line[1][0]
                        current_text_lines.append(text)
                
                new_text = " ".join(current_text_lines).strip()
                
                # Deduplication Logic
                if new_text:
                    if new_text == buffer_text:
                        pass # Exact duplicate
                    elif new_text in buffer_text:
                         # New text is substring of buffer (e.g. glitch or partial fade out)
                        pass 
                    elif buffer_text and buffer_text in new_text:
                        # Buffer is substring of new text (e.g. more text showed up)
                        buffer_text = new_text
                        print(f"Buffered (Expanded): {buffer_text}")
                    else:
                        # Content changed significantly
                        if buffer_text:
                            print(f"Writing: {buffer_text}")
                            f.write(buffer_text + "\n")
                            f.flush()
                        
                        buffer_text = new_text
                        print(f"Buffered (New): {buffer_text}")
                
                # # Sleep remaining time
                # elapsed = time.time() - start_time
                # sleep_time = max(0, INTERVAL - elapsed)
                time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping...")
        # Write remaining buffer
        if buffer_text:
             with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                print(f"Writing final buffer: {buffer_text}")
                f.write(buffer_text + "\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
