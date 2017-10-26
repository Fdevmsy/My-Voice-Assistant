# My Voice Assistant  

Shiyu Mou
Iquotient Robotics 
shiyumou@usc.edu
### Introduction 
This is my Voice Assistant featured with hot-word detection (Alexa!),  natural language chatting (in Chinese), and voice control of ROS robot. 

### Setting Up 
1. Ubuntu 14.04 or later. 
1. Clone the repository. 
2. Install pygame: `sudo apt-get install python-pygame`
3. Install voicetools: `sudo pip install voicetools`
4. Other dependencies: `sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox`

	`pip install pyaudio`
	
	`sudo apt-get install libatlas-base-dev`
	
5. Upgrade requests: `git clone git://github.com/requests/requests.git`
	 `cd requests`
	 `pip install .`
	 
6. Install pyaudio: 
	`sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo pip install pyaudio==0.2.11`
	
7. Install ffmpeg: [https://www.faqforge.com/linux/how-to-install-ffmpeg-on-ubuntu-14-04/](https://www.faqforge.com/linux/how-to-install-ffmpeg-on-ubuntu-14-04/)
8. This code includes voice control of ROS robot, so you may also need to install ROS. 
9. This program is using [Baidu Voice APIs](http://yuyin.baidu.com) for TTS and STT, [Turing Robot](http://www.tuling123.com) for text understanding and replying, you may apply your own keys in these two website and replace them in main() function of run_chatbot.py

###Usage: 
1. Bring up roscore. 
1. cd to ~/chatbot
2. Run: `python run_chatbot.py resources/alexa.umdl`
3. Say "Alexa!" to wake up the chatbot
4. After hearing an alert sound, you can talk to Alexa (in Chinese). 
5. You can say: "前进"， “后退”， “左转”， “右转” to control a ROS robot. The default rostopic is `/cmd_vel_mux/input/teleop`, you can modify this in line 176 of run_chatbot.py.  

### Train your own hotword:

Now the chatbot is using an universal hot-word for waking-up. But no surprisingly, you can give a new name to this chatbot!

1. Open the link here: [https://snowboy.kitt.ai/dashboard](https://snowboy.kitt.ai/dashboard)
2. Login using your preferred method. 
3. Click "Create Hotword" and follow the instructions.
4. Download the model named with '.pmdl' to `~/chatbot/resources/`
5. Run the code with: `python run_chatbot.py resources/your-own-model's-name.pmdl`

