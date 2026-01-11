import sys
from paddleocr import PaddleOCR

# time python v5all.py 10 7680 10 > result.txt
# 1m35s
# grep -v frame result.txt|uniq  > result1.txt

# Initialize PaddleOCR instance
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

start_no = int(sys.argv[1])
end_no = int(sys.argv[2])
step = int(sys.argv[3])

for i in range(start_no, end_no, step):
    # Run OCR inference on a sample image
    filename = f'frame{i}.jpg'
    print(filename) 
    result = ocr.predict(filename)
    for text in result[0]['rec_texts']:
        print(text)

#    input="frame570.jpg")

# Visualize the results and save the JSON results
#for res in result:
#    res.print()
#    res.save_to_img("output")
#    res.save_to_json("output")
