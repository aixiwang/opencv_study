import cv2
import numpy as np

def extract_red(image):
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV)
    lower_red = np.array([0, 0, 0])
    upper_red = np.array([5, 255, 255])
    mask = cv2.inRange(HSV,lower_red,upper_red)
    mask_img = cv2.bitwise_and(image,image,mask=mask)
    return mask_img
 
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged

def remove_short_line(image):
    img = image.copy()
    h,w,dim_n = img.shape
    for x in range(w):
        for y in range(h):
            if img[y][x][2] > r_threshold:
                img[y][x] = [255,255,255]
            else:
                img[y][x] = [0,0,0]
            
    return img
    
    
def extract_red(image):
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV)
    # 4, 196, 158
    lower_red = np.array([4-4, 196-20, 158-20])
    upper_red = np.array([4+10, 196+20, 158+20])
    mask = cv2.inRange(HSV,lower_red,upper_red)
    mask_img = cv2.bitwise_and(image,image,mask=mask)
    return mask_img

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


    
def extract_red2(image,h_threshold):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h[h > h_threshold] = 255
    h[h <= h_threshold] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def extract_red3(image,r_threshold):
    img = image.copy()
    h,w,dim_n = img.shape
    for x in range(w):
        for y in range(h):
            if img[y][x][2] > r_threshold:
                img[y][x] = [255,255,255]
            else:
                img[y][x] = [0,0,0]
            
    return img

def extract_red4(image,h_threshold):
    img = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h = hsv[:,:,0]
    print 'len h:',len(h),' len w:',len(h[0])
    height,width,dim_n = img.shape
    print height,width,dim_n
    for x in range(width):
        for y in range(height):
            #print 'h[y][x]:',type(h[y][x])
            if h[y][x] > h_threshold:
                img[y][x] = [255,255,255]
            else:
                img[y][x] = [0,0,0]
            
    return img
    
img = cv2.imread('meter.bmp')
cv2.imshow('raw img',img)
cv2.waitKey(0)

img1 = auto_canny(img)
cv2.imshow('edged',img1)
cv2.waitKey(0)

img2 = extract_red(img)
cv2.imshow('red',img2)
cv2.waitKey(0)


if 0:
    circles = cv2.HoughCircles(img1,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img1,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img1,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()