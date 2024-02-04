# This script has main functionalities such as getting the robot to capture the face, cropping the image, gesture prediction, and finally giving the command to act.
# Please note you have to change the paths as per your system
import threading
import time
import anki_vector
from anki_vector import events
from anki_vector.util import degrees
import cv2
import numpy as np
import os
from keras.models import model_from_json
from anki_vector.util import degrees, distance_mm, speed_mmps
import os
import sys
import time
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report,ConfusionMatrixDisplay
from anki_vector.util import degrees

class Image:
    def __init__(self):
        self.inc=0
        self.name="random"
        self.im_flag=False
        self.emotion_list=[]
        self.action_flag=False
        self.main_im=0

    def annotate_camera_image(self,robot, event_type,event2, done):
        # get image with face annotations
        annotate_PIL_image=event2.image.annotate_image()
        annotated_open_cv_image=np.array(annotate_PIL_image)
        annotated_open_cv_image=annotated_open_cv_image[:,:,::-1].copy()
        self.annotate=annotated_open_cv_image

    def on_new_camera_image(self,robot, event_type, event1_raw, done):
        #___________get image without face annotations______________#
        #___________image preprocessing from camera__________________#
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
                    out = open_cv_primary_image[y-30:y+h+5,x+5:x+w+10]
                    j+=1
                    self.model_image=out
                    self.model_image = cv2.cvtColor(self.model_image, cv2.COLOR_BGR2GRAY)
                    self.black_test_image= self.model_image
                    directory = r"C:\Anki_vector\anki_dataset\participant_dataset\all_faces"
                    name = str(self.main_im) + self.name
                    cv2.imwrite(os.path.join(directory, str(name) + 'test_img.jpg'), self.black_test_image)
                    os.listdir(directory)
                    self.main_im+=1
                    self.model_image=cv2.resize( self.model_image,(45,45),interpolation=cv2.INTER_AREA)
                    self.model_image = np.expand_dims(np.expand_dims(cv2.resize(self.model_image, (48, 48)), -1), 0)
                    self.im_flag=True
        print(self.im_flag,self.action_flag)
        if self.im_flag==True and self.action_flag==False:
            print("TIme to Classify")
            self.im_flag==False
            # __________________model Implementation______________________#
            # if self.model_image!=0:
            emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad",
                            6: "Surprised"}
            # load json and create model
            # json_file = r"C:\Anki_vector\anki_dataset\Face_gesture\model\emotion_model.json"
            json_file = open('C:\Anki_vector\Face_gesture\scripts\model\emotion_model.json', 'r')
            # json_file = open(":/Anki_vector/anki_dataset/Face_gesture/model/emotion_model.json", 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            emotion_model = model_from_json(loaded_model_json)
            # load weights into new model
            emotion_model.load_weights("C:\Anki_vector\Face_gesture\scripts\model\emotion_model.h5")
            print("Loaded model from disk")
            emotion_prediction = emotion_model.predict(self.model_image)
            maxindex = int(np.argmax(emotion_prediction))
            self.emotion_list.append(maxindex)
            if len(self.emotion_list)>=10:
                mode_index=np.bincount(self.emotion_list).argmax()
                self.emotion_list=[]
                print(emotion_dict[mode_index], "----------------------Predicting Gesture/Emotion-------------------------------")
                self.final_emotion_pred_value=mode_index
                self.action_flag=True
                
            ### Happy
            if self.action_flag==True and  self.final_emotion_pred_value==3 :
                print("square action")
                for _ in range(4):
                    robot.behavior.drive_off_charger()
                    print("Drive Vector straight...")
                    robot.behavior.drive_straight(distance_mm(100), speed_mmps(50))
                    print("Turn Vector in place...")
                    robot.behavior.turn_in_place(degrees(90))
                robot.behavior.set_head_angle(degrees(45.0))
                robot.behavior.set_lift_height(0.0)
                directory = r"C:\Anki_vector\anki_dataset\participant_dataset\happy"
                name = str(self.inc) + self.name
                cv2.imwrite(os.path.join(directory, str(name) + 'test_img.jpg'),  self.black_test_image)
                os.listdir(directory)
                self.inc+=1
                self.action_flag = False
            ###Sad
            if self.action_flag == True and self.final_emotion_pred_value == 5:
                robot.audio.stream_wav_file("siri_joke.wav", 100)
                robot.behavior.set_head_angle(degrees(45.0))
                robot.behavior.set_lift_height(0.0)
                directory = r"C:\Anki_vector\anki_dataset\participant_dataset\sad"
                name = str(self.inc) + self.name
                cv2.imwrite(os.path.join(directory, str(name) + 'test_img.jpg'),  self.black_test_image)
                os.listdir(directory)
                self.inc += 1
                self.action_flag = False

            ###Angryy
            if self.action_flag == True and self.final_emotion_pred_value == 0:
                # print("Playing Animation Trigger 1:")
                # robot.anim.play_animation_trigger('GreetAfterLongTime')
                print("Playing Animation Trigger 2: (Ignoring the body track)")
                robot.anim.play_animation_trigger('GreetAfterLongTime', ignore_body_track=True)
                animation = 'anim_pounce_success_02'
                print("Playing animation by name: " + animation)
                robot.anim.play_animation(animation)
                robot.behavior.set_head_angle(degrees(45.0))
                robot.behavior.set_lift_height(0.0)
                directory = r"C:\Anki_vector\anki_dataset\participant_dataset\angry"
                name = str(self.inc) + self.name
                cv2.imwrite(os.path.join(directory, str(name) + 'test_img.jpg'),  self.black_test_image)
                os.listdir(directory)
                self.inc += 1
                self.action_flag = False
                
            ### neutral
            if self.action_flag == True and self.final_emotion_pred_value == 4:
                for k in range(5):
                    robot.motors.set_lift_motor(5)
                    time.sleep(0.25)
                    robot.motors.set_lift_motor(-5)
                    time.sleep(0.25)
                directory = r"C:\Anki_vector\anki_dataset\participant_dataset\neutral"
                name = str(self.inc) + self.name
                cv2.imwrite(os.path.join(directory, str(name) + 'test_img.jpg'),  self.black_test_image)
                os.listdir(directory)
                self.inc += 1
                self.action_flag = False

            ### Other emotions
            else:
                if self.action_flag == True:
                    print("Set Vector's eye color to purple...")
                    robot.behavior.set_eye_color(hue=0.83, saturation=0.76)
                    time.sleep(2)
                    robot.behavior.set_eye_color(hue=0.23, saturation=0.76)
                    time.sleep(2)
                    robot.behavior.set_eye_color(hue=0.63, saturation=0.76)
                    time.sleep(2)
                    robot.behavior.set_eye_color(hue=0.95, saturation=0.76)
                    time.sleep(2)
                    directory = r"C:\Anki_vector\anki_dataset\participant_dataset\other"
                    name=str(self.inc)+self.name
                    cv2.imwrite(os.path.join(directory, str(name) + 'test_img.jpg'), self.black_test_image)
                    os.listdir(directory)
                    self.inc += 1
                    self.action_flag = False
        # _______________________Saving the images in a datset ____________________
        if self.inc>5 and self.inc<45:
            directory=r"C:\Anki_vector\anki_dataset\koushik\suprised"
            cv2.imwrite(os.path.join(directory,str(self.inc)+'cropped_img.jpg'),out)
        
            os.listdir(directory)
        else:
            print("-----------------------------end--------------------------------------")
        self.inc+=1
        self.cropped_image=out
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
        time.sleep(120)
    except KeyboardInterrupt:
        robot.disconnect()

