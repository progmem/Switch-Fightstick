import cv2
import numpy as np

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

if __name__ == "__main__":
	res = isContainTemplate("sample_color_HLS.png", "dougu_to_bag.png", 0.7, False)
