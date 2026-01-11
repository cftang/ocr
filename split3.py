# Program To Read video
# and Extract Frames
# https://www.geeksforgeeks.org/python-program-extract-frames-using-opencv/
# pip3 install opencv-python Pillow
# python3 split2.py 1.mp4 500
import cv2
import sys
from PIL import Image

# Function to extract frames
def FrameCapture(path,interval):

	# Path to video file
	vidObj = cv2.VideoCapture(path)

	# Used as counter variable
	count = 0

	# checks whether frames were extracted
	success = 1

	while success:

		# vidObj object calls read
		# function extract frames
		success, image = vidObj.read()

		# Saves the frames with frame-count
		if count % interval == 0 and success:
			im = Image.fromarray(image)
			# print(im.width)
			# print(count)
			#left top right bottom
			im = im.crop((610,750,1920,775))
			# im = im.crop((430,300,1820,820))

			# 通道分离合并
			# https://zhuanlan.zhihu.com/p/45326961
			r, g, b = im.split()
			im = Image.merge('RGB', (b, g, r))
			
			im.save("frame%d.jpg" % count)

		count += 1
		if count>200:
			break


# Driver Code
if __name__ == '__main__':

	interval = 50
	if len(sys.argv) > 2:
		interval = int(sys.argv[2])
	# Calling the function
	if len(sys.argv) > 1:
		FrameCapture(sys.argv[1],interval)
	else:
		print("Usage: python split3.py <video_path> [interval]")
