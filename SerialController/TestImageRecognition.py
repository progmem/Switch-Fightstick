import cv2
import numpy as np
from copy import deepcopy
import time

TEMPLATE_PATH = "./Template/"
# Detect image by template matching
def isContainTemplate(src_path, template_path, threshold=0.7, use_gray=True):
	src = cv2.imread(TEMPLATE_PATH+src_path, cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)

	template = cv2.imread(TEMPLATE_PATH+template_path, cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
	w, h = template.shape[1], template.shape[0]
	
	method = cv2.TM_CCOEFF_NORMED
	res = cv2.matchTemplate(src, template, method)
	_, max_val, _, max_loc = cv2.minMaxLoc(res)
	print("corelation: " + str(max_val))

	if max_val > threshold:
		print('Detected!')
		if use_gray:
			src = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

		top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		cv2.rectangle(src, top_left, bottom_right, (255, 0, 255), 2)

		# show image with matched area
		cv2.imshow('detected area', src)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return True
	else:
		print('not Detected')
		return False

def getInterframeDiff(frame1, frame2, frame3, threshold):
	diff1 = cv2.absdiff(frame1, frame2)
	diff2 = cv2.absdiff(frame2, frame3)
	diff = cv2.bitwise_and(diff1, diff2)

	# binarize
	img_th = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

	# remove noises
	mask = cv2.medianBlur(img_th, 3)
	return mask

def testInterframeDiff():
	cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

	frame1 = cv2.cvtColor(cap.read()[1][0:239, :], cv2.COLOR_RGB2GRAY)
	
	print(type(frame1))
	time.sleep(0.1)
	frame2 = cv2.cvtColor(cap.read()[1][0:239, :], cv2.COLOR_RGB2GRAY)
	time.sleep(0.1)
	frame3 = cv2.cvtColor(cap.read()[1][0:239, :], cv2.COLOR_RGB2GRAY)

	while cap.isOpened():
		time.sleep(0.1)
		mask = getInterframeDiff(frame1, frame2, frame3, 15)

		cv2.imshow("Frame2", frame2)
		cv2.imshow("Mask", mask)

		frame1 = frame2
		frame2 = frame3
		frame3 = cv2.cvtColor(cap.read()[1][0:239, :], cv2.COLOR_RGB2GRAY)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	print("release")
	cap.release()
	cv2.destroyAllWindows()

def getRobustFeatures(img1, img2, matcher):
	# create AKAZE detector and compute features
	akaze = cv2.AKAZE_create()                                
	kp1, des1 = akaze.detectAndCompute(img1, None)
	kp2, des2 = akaze.detectAndCompute(img2, None)

	# matching by des with Brute-Force & KNN
	matches = matcher.knnMatch(des1, des2, k=2)

	# leave only good matches
	ratio = 0.5
	good = []
	for m, n in matches:
		if m.distance < ratio * n.distance:
			good.append([m])
	
	return kp1, des1, kp2, des2, good
	
def testAkaze(test_path):
	cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
	cap.set(cv2.CAP_PROP_FPS, 30)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

	img1 = cv2.imread(TEMPLATE_PATH+test_path, cv2.IMREAD_COLOR)
	img2 = None

	# generate Brute-Force Matcher
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

	while cap.isOpened():
		img2 = cap.read()[1]

		try:
			kp1, _, kp2, _, good = getRobustFeatures(img1, img2, bf)
			img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
			cv2.imshow('img', img3)

		except: # examine later
			cv2.imshow('img', img2)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	print("release")
	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	#res = isContainTemplate("sample.png", "dougu_to_bag.png", 0.7, True)
	#testInterframeDiff()

	testAkaze('pannels.png')