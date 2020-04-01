# -*- coding: utf-8 -*-

# __Auther__: Shiyu Mou
# __Copyright__: Iquotient Robotics 2017


#!/usr/bin/env python

# import speech_recognition as sr
# from gtts import gTTS
import os
from pygame import mixer
import time
from voicetools import TuringRobot
from voicetools import BaiduVoice
import socket   
from geometry_msgs.msg import Twist
import rospy
import urllib3
from subprocess import Popen, PIPE
from myRecord import myRecord
from tempfile import NamedTemporaryFile
import snowboydecoder
import sys
import signal


interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


urllib3.disable_warnings()
# from voicetools import BaiduVoice

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def convert_to_wav(file_):
    """convert mp3 to wav"""
    p = Popen(['ffmpeg', '-y', '-i','-', '-ar', '16000', 'hollyshit.wav'], stdin=file_ , stdout=None, stderr=None)

def convert_to_mp3(file_):
    """convert mp3 to wav"""
    p = Popen(['ffmpeg', '-y', '-i', '-', 'answer.mp3'], stdin=file_ , stdout=None, stderr=None)

def speak(bv, content):

    try:
        data = NamedTemporaryFile()
        data.write(bv.tts(content))
        data.seek(0)
        convert_to_mp3(data)
        data.close()
        time.sleep(0.2)
        mixer.music.load("answer.mp3")
        mixer.music.play()
        while mixer.music.get_busy() == True:
            time.sleep(0.01)
            continue
            
    except:
        speak(bv, "抱歉，连接有点问题")
    # while mixer.music.get_busy() == True:
    #     time.sleep(0.01)
    #     continue
def auto_record(bv):
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    mixer.music.load("yes.mp3")
    mixer.music.play()
    # with open("hollyshit.wav", "wb") as f:
    #     f.write(audio.get_wav_data())
    data = NamedTemporaryFile()
    data.write(audio.get_wav_data())
    data.seek(0)
    convert_to_wav(data)
    data.close()
    time.sleep(0.2)
    print("Audio saved")

    
    try:
        results = bv.asr("hollyshit.wav")
        print(results[0].decode("utf-8"))
        result = results[0]
        return result
    except:
        print("Sorry I didn't get that")
        speak(bv, "抱歉我没听清楚")

def chat(bv, chatbot, result, pub):
    
    # print(result)
    # print(type(result))

    if result[0:2] == u"前进":
        pub_steering(pub, 'forward')
        speak(bv, "正在前进")
        # print("Moving forward")
    elif result[0:2] == u"后退":
        pub_steering(pub, 'backward')
        speak(bv, "正在后退")
        # print("Moving backward")
    elif result[0:2] == u"左转":
        pub_steering(pub, 'left')
        speak(bv, "正在左转")
        # print("Turning left")
    elif result[0:2] == u"右转":
        pub_steering(pub, 'right')
        # print("Turning right")
        speak(bv, "正在右转")
    else:
    	try: 
	    	answer = chatbot.ask_turing(result)
	    	return unicode(str(answer))
    	except:
		    print("Sorry I didn't get that")
		    speak(bv, "抱歉我没听清楚")
        # mixer.music.load("sorry.mp3")
        # mixer.music.play()
        # time.sleep(0.6)
def pub_steering(pub, event):
	
    move_cmd = Twist()
    if event == 'forward':
        print('moving forward...')
        move_cmd.linear.x = 0.5
        move_cmd.angular.z = 0
    if event == 'backward':
        move_cmd.linear.x = -0.5
        move_cmd.angular.z = 0
        print('moving backward...')
    if event == 'left':
        move_cmd.linear.x = 0
        move_cmd.angular.z = 1
        print('turning left...')
    if event == 'right':
        move_cmd.linear.x = 0
        move_cmd.angular.z = -1
        print('turning right...')
	
    r = rospy.Rate(10)
    for i in range(0, 10):
        pub.publish(move_cmd)
        r.sleep()

def main():
    
    model = sys.argv[1] # path to hot-word model 
    model = 'resources/alexa.umdl'
    mixer.init(frequency=16000)

    # Baidu Voice API, you may need to update your tokens. 
    token = BaiduVoice.get_baidu_token('VB5dnaiN1uM3b2tWbUYcOFzE', '9577cd3eaa69b68040fdfd204fcd19c1')
    bv = BaiduVoice(token['access_token'])

    # Turing Robots Tokens 
    chatbot = TuringRobot('2b3e14182a7b4cdaa34d1bb65020f822')
    
    # ROS topic
    rospy.init_node('chatbot-node')
    pub=rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)

    # Hot word detector 
    signal.signal(signal.SIGINT, signal_handler)
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.9)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=lambda: chatbot_callback(bv, chatbot, pub),
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()

def chatbot_callback(bv, chatbot, pub):        
        
        # raw_input('Press enter to talk: ')
        # print("Awaiting user input.")
        # audio = r.listen(source)
        # print("Attempting to transcribe user input.")
        mixer.music.load("alart.mp3")
        mixer.music.play()
        time.sleep(1.2)

        content = auto_record(bv)
        if content is not None:
            answer = chat(bv, chatbot, content, pub)
            if answer is not None:
                speak(bv, answer)
        # auto_record()
if __name__ == '__main__':
    main()

