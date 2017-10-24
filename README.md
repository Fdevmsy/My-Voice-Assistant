# My Voice Assistant  

###Usage: 
1. cd to ~/chatbot
2. Run: `python run_chatbot.py resources/alexa.umdl`
3. Say "Alexa!" to wake up the chatbot
4. After hearing an alert sound, you can talk to Alexa (in Chinese). 

### Train your own hotword:

Now the chatbot is using an universal hot-word for waking-up. But no surprisingly, you can give a new name to this chatbot!

1. Open the link here: [https://snowboy.kitt.ai/dashboard](https://snowboy.kitt.ai/dashboard)
2. Login using your preferred method. 
3. Click "Create Hotword" and follow the instructions.
4. Download the model named with '.pmdl' to `~/chatbot/resources/`
5. Run the code with: `python run_chatbot.py resources/your-own-model's-name.pmdl`

