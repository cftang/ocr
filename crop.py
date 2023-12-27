import cv2
import sys

# img = cv2.imread(sys.argv[1])
# print(type(img))
  
# Shape of the image
# print("Shape of the image", img.shape)

for i in range(2,33):
    img = cv2.imread(str(i)+'.jpg')

    is_even = True
    if i % 2:
        is_even = False

    x1 = 0
    y1 = 0
    x2 = 933
    y2 = 1206

    if is_even:
    # [rows, columns]
        #even
        x1 = 73
        y1 = 0
        x2 = 995
        y2 = 1206
    crop = img[y1:y2, x1:x2] 
    # odd
    # 902/1173  right
    # 0-933/1202 right

    # even
    # 73/1201-1006/1201 left 
    
    # cv2.imshow('original', img)
    # cv2.imshow('cropped', crop)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Using cv2.imwrite() method
    # Saving the image
    cv2.imwrite('a'+str(i)+'.jpg', crop)
