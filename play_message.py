from gtts import gTTS
from io import BytesIO
from pygame import mixer
import paho.mqtt.client as mqtt

broker = ''
port = 1883
topic = ""

start = True


#this method is call when achieves connected with the server
def on_connect(client,userdata,flags,rc):
    print("it conct with server mqtt "+ str(rc))
    client.subscribe(topic)


#whenever that receive a message, this method is going to play for audio
def on_message(client,userdata,msg):
    global start
   
    if not start: 
        
        texto = msg.payload.decode("utf-8") #convert the message in string
        print(texto)
        if texto == "exit":
            client.disconnect()
            
        
        #create and save the audio in mp3 file
        tts=gTTS(text=texto, lang="en") 
        tts.save("audio.mp3")
        mp3_fp= BytesIO()
        tts=gTTS(texto,lang="en")
        tts.write_to_fp(mp3_fp)

        
        #play the audio
        mixer.music.load('audio.mp3')
        mixer.music.set_volume(2)
        mixer.music.play()
    
    start = False
   
mixer.init() #start the player

client=mqtt.Client() #start the mqtt client

#save the both method
client.on_connect=on_connect
client.on_message=on_message

client.disconnect()
client.connect(broker,port) #it conect with the server 
client.loop_forever()


