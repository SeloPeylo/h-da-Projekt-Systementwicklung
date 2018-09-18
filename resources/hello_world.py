from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.53.93", 9559)
tts.say("Hello, world!")