from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.43.61", 9559)
tts.say("Hello, world!")