import threading
import time
import anki_vector
from anki_vector import events
from anki_vector.util import degrees
import cv2
import numpy as np
import os


class Image:
    def __init__(self):
        pass
    def annotate_camera_image(self,robot, event_type,event2, done):
        # get image with face annotations
        annotate_PIL_image=event2.image.annotate_image()
        annotated_open_cv_image=np.array(annotate_PIL_image)
        annotated_open_cv_image=annotated_open_cv_image[:,:,::-1].copy()
        self.annotate=annotated_open_cv_image

    def on_new_camera_image(self,robot, event_type, event1_raw, done):
        #get image without face annotations
        main_image=event1_raw.image
        open_cv_primary_image=np.array(main_image)
        open_cv_primary_image=open_cv_primary_image[:,:,::-1].copy()
        
        hsv = cv2.cvtColor(self.annotate, cv2.COLOR_BGR2HSV)
            
        # Threshold of blue in HSV space

        lower_green = np.array([50,100,0])
        upper_green = np.array([100, 255,255])

        # preparing the mask to overlay
        mask = cv2.inRange(hsv, lower_green, upper_green)    
        # The black region in the mask has the value of 0,13
        # so when multiplied with original image removes all non-blue regions
        result = cv2.bitwise_and(self.annotate, self.annotate, mask = mask)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        

        # dilation = cv2.dilate(erosion,kernel,iterations = 2)
        edged = cv2.Canny(gray, 50, 200)


        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        rects = [cv2.boundingRect(cnt) for cnt in contours]
        rects = sorted(rects,key=lambda  x:x[1],reverse=True)


        i = -1
        j = 1
        y_old = 5000
        x_old = 5000
        if len(rects)!=0:
            area_list=[]
            for rect in rects:
                x,y,w,h = rect
                area = w * h
                area_list.append(area)
            max_element_index=np.argmax(area_list)
            rect=rects[max_element_index]
            area=max(area_list)         
            print(area)
            if area > 5000 and area < 70000:

                if (y_old - y) > 200:
                    i += 1
                    y_old = y

                if abs(x_old - x) > 300:
                    x_old = x
                    x,y,w,h = rect

                    out = open_cv_primary_image[y-10:y+h+5,x+20:x+w]
                    j+=1
            if len(out)!=0:
                cv2.imshow("Hi",out)
                cv2.waitKey(0)




        i=0
        directory=r'C:\Anki_vector'
        cv2.imwrite(str(i)+'cropped_img.jpg',self.annotate)
        cv2.imwrite(str(i)+'normal.jpg', open_cv_primary_image)
        os.listdir(directory)
        i+=1
        cv2.imshow("Hi",)
        cv2.waitKey(0)
        done.set()

with anki_vector.Robot(enable_face_detection=True, enable_custom_object_detection=True) as robot:
    robot.camera.init_camera_feed()
    done = threading.Event()
    robot.behavior.set_head_angle(degrees(45.0))
    robot.behavior.set_lift_height(0.0)
    i1=Image()
    robot.events.subscribe(i1.annotate_camera_image, events.Events.new_camera_image, done)
    robot.events.subscribe(i1.on_new_camera_image, events.Events.new_raw_camera_image,done)


    try:
        time.sleep(100)
    except KeyboardInterrupt:
        robot.disconnect()

