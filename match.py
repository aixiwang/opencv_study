#!/usr/bin/env python
#-*- coding: utf-8 -*-

#------------------------------------------------------------
# Machine vision framework for defect inspection application
#
# v0.1 -- initial code, added window support
#
#------------------------------------------------------------


#--------------------------------------
# external imports
#--------------------------------------
import os
try:
    import cv2
except ImportError, e:
    print e

try:
    import cv
except:
    import cv2.cv as cv
    
import numpy as np
from matplotlib import pyplot as plt  
#import threading, time, random
import time,random
from threading import Thread

import Tkinter
import tkMessageBox
import signal
import sys,os
#from Tkinter import *

#--------------------------------------
# global variables
#--------------------------------------
  
bg_img = np.zeros((512,512,3), np.uint8)
drawing = 0
mode = 1
thread_run_flag = 1
#--------------------------------------
# init
#--------------------------------------

#--------------------------------------
# signal_handler
#--------------------------------------
def signal_handler(signum, frame):
    global thread_run_flag
    thread_run_flag = 0
    print "received a signal %d"%(signum)
    sys.exit(-1)
    
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.namedWindow('config', cv2.WINDOW_NORMAL)
cv2.startWindowThread()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


#--------------------------------------
# show_img
#--------------------------------------
def show_img(window_name,img):
    if cv2.getWindowProperty(window_name,1) == -1:
        print 'no target window:', window_name
    else:
        cv2.imshow(window_name,img)


#--------------------------------------
# mouse_loop
#--------------------------------------             
def mouse_loop(event,x,y,flags,param):
    global ix,iy,drawing,mode
    print 'mouse_mv...',x,y
    
    if 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                if mode == 1:
                    #cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
                    cv2.line(bg_img, (ix,iy),(ix,y), 255, 1, 8, 0)
                    cv2.line(bg_img, (ix,iy),(x,iy), 255, 1, 8, 0)

                    cv2.line(bg_img, (ix,y),(x,y), 255, 1, 8, 0)
                    cv2.line(bg_img, (x,iy),(x,y), 255, 1, 8, 0)
                else:
                    cv2.circle(bg_img,(x,y),5,(0,0,255),-1)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if mode == 1:
                #cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
                cv2.rectangle(bg_img,(ix,y),(x,y),(0,255,0),-1)
                cv2.rectangle(bg_img,(x,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(bg_img,(x,y),5,(0,0,255),-1)

#--------------------------------------
# btn1_callback
#--------------------------------------
def btn1_callback():
    global thread_run_flag
    thread_run_flag = 0

#--------------------------------------
# btn2_callback
#--------------------------------------
def btn2_callback():
    global thread_run_flag
    thread_run_flag = 1
    thread = Thread(target = img_process_thread, args = ())
    thread.start()
    
#--------------------------------------
# btn3_callback
#--------------------------------------
def btn3_callback():
    global thread_run_flag
    # code to exit2
    print 'close window message received' 
    thread_run_flag = 0
    time.sleep(3)
    cv2.destroyAllWindows()
    cv.WaitKey(1)
    cv.WaitKey(1)
    cv.WaitKey(1)
    cv.WaitKey(1) 
    
    sys.exit(-1)

    

#--------------------------------------
# btn2_callback
#--------------------------------------   
def get_screen_size(window):  
    return window.winfo_screenwidth(),window.winfo_screenheight()  
  
def get_window_size(window):  
    return window.winfo_reqwidth(),window.winfo_reqheight()  
  
def center_window(root, width, height):  
    screenwidth = root.winfo_screenwidth()  
    screenheight = root.winfo_screenheight()  
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  
    print(size)  
    root.geometry(size)

#--------------------------------------
# quit
#--------------------------------------   
def quit():
    global thread_run_flag
    # code to exit
    print 'close window message received'
    
    thread_run_flag = 0
    time.sleep(1)
    
    sys.exit(-1)
    
     
#--------------------------------------
# isMatch
#--------------------------------------   
def isMatch(subPath, srcPath, threshold=0.01):
    for img in [subPath, srcPath]: assert os.path.exists(img) , 'No such image:  %s' % (img)
    method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
    try:
        subImg = cv2.imread(subPath) #Load the sub image
        srcImg = cv2.imread(srcPath) #Load the src image
        result = cv2.matchTemplate(subImg, srcImg, method) #comparision
        minVal = cv2.minMaxLoc(result)[0] #Get the minimum squared difference
        if minVal <= threshold: #Compared with the expected similarity
            return True
        else:
            return False
    except:
        return False
  
#--------------------------------------
# getMatchedPoints
#--------------------------------------  
def getMatchedPoints(subPath, srcPath, threshold=0.01, method = cv.CV_TM_SQDIFF_NORMED):   
    xy_points_list = []
    for img in [subPath, srcPath]: assert os.path.exists(img) , "No such image:  %s" % (img)
    #method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
    
    subImg = cv2.imread(subPath) #Load the sub image
    srcImg = cv2.imread(srcPath) #Load the src image
    
    subImg2 = subImg.copy()
    srcImg2 = srcImg.copy()
    # fill it empty
    h, w = srcImg.shape[:2]
    h2, w2 = subImg.shape[:2]

    while True:
        try:
            result = cv2.matchTemplate(subImg, srcImg, method) #comparision
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result) #Get the minimum squared difference
            if minVal <= threshold: #Compared with the expected similarity
                minLocXPoint, minLocYPoint = minLoc
                subImgRow, subImgColumn = subImg.shape[:2]
                xy_point = (minLocXPoint + int(subImgRow/2), minLocYPoint + int(subImgColumn/2))

                xy_points_list.append(xy_point)

                for y in range(h2):
                    for x in range(w2):
                        srcImg[minLocYPoint+y][minLocXPoint+x][0] = 255
                        srcImg[minLocYPoint+y][minLocXPoint+x][1] = 255
                        srcImg[minLocYPoint+y][minLocXPoint+x][2] = 255

                cv2.imwrite('new.bmp',srcImg)
                cv2.circle(srcImg2,xy_point,w2/2,(55,255,155),1)
                
            else:
                break
                
        except Exception, e:
            print 'exception:',str(e)
            return None,None
    
    
    return xy_points_list,srcImg2

#--------------------------------------
# color2gray
#--------------------------------------    
def color2gray(image_file):    
    image = cv2.imread(image_file)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#--------------------------------------
# getMatchedPoints2
#--------------------------------------  
def getMatchedPoints2(subPath, srcPath, maskPath, threshold=0.01, method = cv.CV_TM_SQDIFF_NORMED):
    global thread_run_flag 
   
    print 'getMatchedPoints2 ...'
    
    xy_points_list = []
    for img in [subPath, srcPath]: assert os.path.exists(img) , "No such image:  %s" % (img)
    #method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
    
    

    subImg = color2gray(subPath)
    
    #cv2.imwrite('sub_gray.bmp',subImg)
    
    srcImg = color2gray(srcPath)
    
    #cv2.imwrite('src_gray.bmp',srcImg)
    
    maskImg = cv2.imread(maskPath)
    
    #cv2.imwrite('mask_gray.bmp',maskImg)
    
    
    subImg2 = subImg.copy()
    #srcImg2 = srcImg.copy()
    srcImg2 = cv2.imread(srcPath)
    
    # fill it empty
    h, w = srcImg.shape[:2]
    h2, w2 = subImg.shape[:2]
    h3, w3 = maskImg.shape[:2]
    h4 = h3
    w4 = h4
    
    
    for y2 in range(h2):
        for x2 in range(w2):
            if maskImg[y2][x2][0] == 255 and maskImg[y2][x2][1] == 255 and maskImg[y2][x2][2] == 255:
                #print 'found masked point 1...',y2,x2
                subImg[y2][x2] = 255

    print 'h:',h,' w:',w
    print 'h2:',h2,' w2:',w2
    print 'h3:',h3,' w3:',w3
    #s = raw_input('any key...')
    
    #try:
    if 1:
        y = 0


        #for y in range(h-h2):
        while y < (h-h2+1):
            #print '====================> y:',y
            x = 0            
            #for x in range(w-w2):
            while x < (w-w2+1):
                if thread_run_flag  == 0:
                    return [],srcImg2
                    time.sleep(1)
                    break
                

                #print 'y:',y, ' x:',x                
                detected_sub_img = srcImg[y:y+h2,x:x+w2]
                
                # clean masked points
                for y2 in range(h2):
                    for x2 in range(w2):
                        if maskImg[y2][x2][0] == 255 and maskImg[y2][x2][1] == 255 and maskImg[y2][x2][2] == 255:
                            #print 'found masked point 2...',y2,x2
                            detected_sub_img[y2][x2] = 255

                # match comparing
                # save matched
                    
                minVal = cv2.matchTemplate(subImg, detected_sub_img, method)[0][0] #comparision
                

                #s = raw_input('anykey')
                
                if minVal <= threshold: #Compared with the expected similarity

                    #s = raw_input('any key...')
                    cv2.imwrite('matched_1.bmp',detected_sub_img)
                    cv2.imwrite('matched_2.bmp',subImg)

                
                    print 'matched'
                    print 'minVal:',minVal

                    
                    minLocXPoint, minLocYPoint = x, y
                    xy_point = (minLocXPoint + int(h2/2), minLocYPoint + int(w2/2))
                    
                    xy_points_list.append(xy_point)

                    for y3 in range(h2):
                        for x3 in range(w2):
                            srcImg[minLocYPoint+y3][minLocXPoint+x3] = 255


                    cv2.imwrite('new2.bmp',srcImg)
                    cv2.circle(srcImg2,xy_point,w2/2,(255,0,0),1)
                    print '======================================> found '                        
                    #s = raw_input('any key...')
                    x += w2
                    #y += 
                else:
                
                    #print 'not matched'
                    #print 'minVal:',minVal
                    pass

                x += 3
            y += 3
        #except Exception, e:
        #    print 'exception:',str(e)
        #    return None,None
    
    
    return xy_points_list,srcImg2


#-----------------------------------------
# color2canny
#-----------------------------------------
def color2canny(img_filename, t1, t2):
    img = cv2.imread(img_filename)
    img = cv2.GaussianBlur(img,(3,3),0)
    canny = cv2.Canny(img, t1, t2)
    return canny

#-----------------------------------------
# getMatchedPoints3
# raw_image => canny => template matching
#-----------------------------------------
def getMatchedPoints3(subPath, srcPath, threshold=0.01, canny_threshold1 = 50, canny_threshold2 = 150, method = cv.CV_TM_SQDIFF_NORMED):
    global thread_run_flag 
   
    print 'getMatchedPoints3 ...'
    xy_points_list = []
    for img in [subPath, srcPath]: assert os.path.exists(img) , "No such image:  %s" % (img)
    #method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
    
    subImg = color2canny(subPath, canny_threshold1, canny_threshold2)
    cv2.imwrite('sub_canny.bmp',subImg)
    srcImg = color2canny(srcPath, canny_threshold1, canny_threshold2)
    cv2.imwrite('src_canny.bmp',srcImg)
    srcImg2 = cv2.imread(srcPath)
    
    # fill it empty
    h, w = srcImg.shape[:2]
    h2, w2 = subImg.shape[:2]
    
    while True:
        #try:
        if 1:
            result = cv2.matchTemplate(subImg, srcImg, method) # comparision
            
            #print 'result:',result
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result) # Get the minimum squared difference
            #print 'minVal:',minVal,' maxVal:',maxVal
            print 'minVal:',minVal,' maxVal:',maxVal
            
            if minVal <= threshold: # Compared with the expected similarity
                minLocXPoint, minLocYPoint = minLoc
                subImgRow, subImgColumn = subImg.shape[:2]
                xy_point = (minLocXPoint + int(subImgRow/2), minLocYPoint + int(subImgColumn/2))
                xy_points_list.append(xy_point)

                for y in range(h2):
                    for x in range(w2):
                        srcImg[minLocYPoint+y][minLocXPoint+x] = 0

                cv2.imwrite('new.bmp',srcImg)
                cv2.circle(srcImg2,xy_point,w2/2,(55,255,155),1)
                
            else:
                break
                
        #except Exception, e:
        #    print 'exception:',str(e)
        #    return None,None
        
    
    
    return xy_points_list,srcImg2
    

    
#-----------------------------------------
# getMatchedPoints4
# raw_image => canny => template matching
#-----------------------------------------
def getMatchedPoints4(subPath, srcPath, threshold=0.01, canny_threshold1 = 50, canny_threshold2 = 150, method = cv.CV_TM_SQDIFF_NORMED):
    global thread_run_flag 
   
    print 'getMatchedPoints4 ...'
    xy_points_list = []
    for img in [subPath, srcPath]: assert os.path.exists(img) , "No such image:  %s" % (img)
    #method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
    
    subImg = color2canny(subPath, canny_threshold1, canny_threshold2)
    cv2.imwrite('sub_canny.bmp',subImg)
    srcImg = color2canny(srcPath, canny_threshold1, canny_threshold2)
    cv2.imwrite('src_canny.bmp',srcImg)
    srcImg2 = cv2.imread(srcPath)
    

    
    # fill it empty
    h, w = srcImg.shape[:2]
    h2, w2 = subImg.shape[:2]

    print 'h:',h,' w:',w
    print 'h2:',h2,' w2:',w2

    #s = raw_input('any key...')
    
    #try:
    if 1:
        y = 0
        #for y in range(h-h2):
        while y < (h-h2+1):
            #print '====================> y:',y
            x = 0            
            #for x in range(w-w2):
            while x < (w-w2+1):
                if thread_run_flag  == 0:
                    return [],srcImg2
                    time.sleep(1)
                    break
                
                #print 'y:',y, ' x:',x                
                detected_sub_img = srcImg[y:y+h2,x:x+w2]
                

                # match comparing
                # save matched
                    
                minVal = cv2.matchTemplate(subImg, detected_sub_img, method)[0][0] #comparision
                #s = raw_input('anykey')
                print 'minVal:',minVal
                    
                if minVal <= threshold: #Compared with the expected similarity
                    #s = raw_input('any key...')
                    cv2.imwrite('matched_1.bmp',detected_sub_img)
                    cv2.imwrite('matched_2.bmp',subImg)

                    print 'matched'
                    print 'minVal:',minVal

                    minLocXPoint, minLocYPoint = x, y
                    xy_point = (minLocXPoint + int(h2/2), minLocYPoint + int(w2/2))
                    
                    xy_points_list.append(xy_point)

                    for y3 in range(h2):
                        for x3 in range(w2):
                            srcImg[minLocYPoint+y3][minLocXPoint+x3] = 255

                    cv2.imwrite('new2.bmp',srcImg)
                    cv2.circle(srcImg2,xy_point,w2/2,(255,0,0),1)
                    print '======================================> found '                        
                    #s = raw_input('any key...')
                    x += w2
                    #y += 
                else:
                    #print 'not matched'
                    #print 'minVal:',minVal
                    pass

                x += 1
            y += 1
        #except Exception, e:
        #    print 'exception:',str(e)
        #    return None,None
    
    
    return xy_points_list,srcImg2

    
#--------------------------------------
# img_process_thread
#--------------------------------------  
def img_process_thread(show_image_func):

    global thread_run_flag
    
    print 'start to run img_process_thread ...' 
    while thread_run_flag:
        
        if 0:
            print 'test 1 ...'
            #point_list,img = getMatchedPoints(subPath='sub2_2.bmp', maskPath='sub2_2_mask.bmp', srcPath='full2.bmp', threshold=0.1)
            point_list,img = getMatchedPoints(subPath='sub2_2.bmp', srcPath='src2.bmp', threshold=0.1)
            
            if point_list != [] and point_list != None:
                cv2.imwrite('result_t1.bmp',img)            
                print 'found point_list:',point_list
                img = np.array(img,dtype=float)/float(255)
                #cv2.imshow('image',img)

                show_image_func('image',img)
            
                        
            else:
                print 'sub1 no finding'
                
        time.sleep(1)
        
        if 0:        
            print 'test 2 ...'        
            point_list,img = getMatchedPoints(subPath='sub2_1.bmp', srcPath='src2.bmp', threshold=1)
            
            if point_list != [] and point_list != None:
                cv2.imwrite('result_t2.bmp',img)
                print 'found point_list:',point_list
                img = np.array(img,dtype=float)/float(255)
                #cv2.imshow('image',img)

                show_image_func('image',img)
            else:
                print 'sub2 no finding'

        time.sleep(1)
        
        if 0:        
            print 'test 3 ...'        
            point_list,img = getMatchedPoints3(subPath='sub2_1.bmp', srcPath='src2.bmp', threshold=0.01, method = cv.CV_TM_CCOEFF_NORMED)
            
            if point_list != [] and point_list != None:
                cv2.imwrite('result_t3.bmp',img)
                print 'found point_list:',point_list
                img = np.array(img,dtype=float)/float(255)
                #cv2.imshow('image',img)

                show_image_func('image',img)
            else:
                print 'sub3 no finding'
        time.sleep(1)

        if 1:        
            print 'test 4 ...'        
            point_list,img = getMatchedPoints4(subPath='sub2_1.bmp', srcPath='src2.bmp', threshold=0.1)
            
            if point_list != [] and point_list != None:
                cv2.imwrite('result_t3.bmp',img)
                print 'found point_list:',point_list
                img = np.array(img,dtype=float)/float(255)
                #cv2.imshow('image',img)

                show_image_func('image',img)
            else:
                print 'sub4 no finding'
                
        time.sleep(1)
        
        
    print 'stop to run img_process_thread ...'      

    
#--------------------------------------
# main
#--------------------------------------
if __name__ == '__main__':
    #cv2.setMouseCallback('image',mouse_loop)
    thread_run_flag = 1   
    thread = Thread(target = img_process_thread, args=(show_img,))
    thread.start()

    #show_img('image',bg_img)
            
    #===========================================
    # GUI
    #
    top = Tkinter.Tk()
    top.title('Control Window')  
    center_window(top, 300, 240)  
    top.maxsize(600, 400)  
    top.minsize(300, 240)  
    top.protocol("WM_DELETE_WINDOW", quit)

    b1 = Tkinter.Button(top, text ="stop processing ", command = btn1_callback)
    b1.pack()
    b2 = Tkinter.Button(top, text ="start processing", command = btn2_callback)
    b2.pack()
    
    b3 = Tkinter.Button(top, text ="======exit======", command = btn3_callback)
    b3.pack()

    top.mainloop()
    #===========================================
    
    cv.waitKey(0) # close window when a key press is detected
    cv2.destroyAllWindows()
    cv.WaitKey(1)
    cv.WaitKey(1)
    cv.WaitKey(1)
    cv.WaitKey(1)    
    
    