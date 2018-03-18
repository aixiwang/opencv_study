# import the necessary packages
#from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# import the necessary packages
import numpy as np
import glob
 
def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged
    
class ShapeDetector:
	def __init__(self):
		pass
 
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
 
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
 
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
 
		# return the name of the shape
		return shape
        
        
#================================================
#                   M A I N
#================================================
if __name__ == "__main__":
        
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to the input image")
    args = vars(ap.parse_args())


    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(args["image"])
    image2 = auto_canny(image)
    cv2.imshow("Image", image2)
    print 'debug 1 - canny'
    cv2.waitKey(0)
    
    print 'debug 2'

    cv2.imshow("Image", image)
    print 'debug 3'

    cv2.waitKey(0)

    resized = imutils.resize(image, width=300)

    print 'debug 4'

    cv2.imshow("Image", resized)
    cv2.waitKey(0)

    print 'debug 5'

    ratio = image.shape[0] / float(resized.shape[0])
     
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Image", gray)
    cv2.waitKey(0)

    print 'debug 6'

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.imshow("Image", blurred)

    v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    
    thresh = cv2.threshold(blurred, lower, upper, cv2.THRESH_BINARY)[1]

    
    cv2.imshow("Image", thresh)

    cv2.waitKey(0)
    print 'debug 7'
    
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()

    print 'debug 8'
    
    print 'cnts:',cnts
    
    # loop over the contours
    for c in cnts:
        print 'c:',c
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        #print 'M:',M
        if M["m00"] == 0:
            print 'zero ..'
            continue
            
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
     
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
     
        # show the output image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        