def getxStatus(xt,xold):
    if xt<xold:
       
     
        self.tts.say("Right")
    elif xt>xold:
        
         self.tts.say("Left")
         
    return     
         
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        
    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
        
    def onLoad(self):
        #put initialization code here
        self.motion=self.session().service( "ALMotion" )
        self.posture=self.session().service( "ALRobotPosture" )
        self.tracker=self.session().service( "ALTracker" )
        self.tts=self.session().service( "ALTextToSpeech" )
        self.alife=self.session().service( "ALAutonomousLife" )
      
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        #self.onStopped() #activate the output of the box
        self.motion.wakeUp()
        self.alife.setState("disabled")
        
        
        self.tracker.stopTracker()
        self.tracker.unregisterAllTargets()
        self.tracker.toggleSearch(False)

        self.tts.say("Red Ball Detector started")
        self.fractionMaxSpeed = 0.8
        # Go to posture stand
        self.posture.goToPosture("StandInit", self.fractionMaxSpeed)

        # Add target to track.
        self.targetName = "RedBall"
        self.diameterOfBall = 0.06
        self.tracker.registerTarget(self.targetName, self.diameterOfBall)
         # set modes
        self.mode = "Head"
        self.tracker.setMode(self.mode)
        # Then, start tracker.
        self.tracker.track(self.targetName)

   
        self.hasTarget = None
        self.x=0
        while True:
                #Cordinates in variables
          
                if self.tracker.isNewTargetDetected():
                    self.tracker.pointAt("LArm",self.tracker.getTargetPosition(0), 0, 0.8)
              
                    self.postion=self.tracker.getTargetPosition(0)
                    
                    if self.x!=0:
                        self.tts.say("IAM IN THE ZONE")
                        self.getxStatus(self.postion[1],self.x)
                        self.x=self.postion[1]
                if self.tracker.isNewTargetDetected() and self.hasTarget == None:
                    self.tts.say("I have detected a red ball")
                    self.tracker.pointAt("LArm", self.tracker.getTargetPosition(0), 0, 0.8)
                    self.x=self.postion[1]
               
               
                    
                    self.posture.goToPosture("StandInit", self.fractionMaxSpeed)
                    self.hasTarget = True

        
                if  self.tracker.isTargetLost() and self.hasTarget == True:
                    self.tts.say("I have lost my Target!")
                    self.hasTarget = None

                    self.time.sleep(0.5)
                self.tts.say("end of line")
                

    
