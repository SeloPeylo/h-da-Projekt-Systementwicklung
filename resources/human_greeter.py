# HumanGreeter with qi framework

import naoqi

#NAO_IP = "nao.local"
NAO_IP = "141.100.47.205"

mem = ALProxy("ALMemory", NAO_IP, 9559)
tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
ses = mem.session

def HumanGreeterCallback():
	tts.say("Face detected!")
	tts.say("Callback, wow")
	
	
mem = session.service("ALMemory")
sub = mem.subscriber("FaceDetected")
sub.signal.connect(HumanGreeterCallback)