


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
        self.yold = 0
        self.ynew = 0
        self.xpos = 0

        while True:


            if self.hasTarget == True:

                self.yold = self.ynew
                self.ynew = self.tracker.getTargetPosition(0)[1]
                self.xpos = self.tracker.getTargetPosition(0)[0]

               # if self.yold is not None:


                self.difference = 0
                self.difference = self.yold - self.ynew
                self.tolerance = 0.1
                self.minDist = 0.5
                self.maxDist = 1.8

                if self.xpos <= self.minDist:

                    self.tts.say("Sphero you are too close")
                elif self.xpos >= self.maxDist:

                    self.tts.say("Sphero come back. I miss you.")
                elif self.difference <= -self.tolerance:

                    self.tts.say("Left")
                elif self.difference >= self.tolerance:

                    self.tts.say("Right")

                self.tracker.pointAt("LArm", self.tracker.getTargetPosition(0), 0, 0.8)


            if self.tracker.isNewTargetDetected() and self.hasTarget == None:
                self.tts.say("I have detected a red ball")
                self.tracker.pointAt("LArm", self.tracker.getTargetPosition(0), 0, 0.8)
                self.posture.goToPosture("StandInit", self.fractionMaxSpeed)
                self.hasTarget = True



            if self.tracker.isTargetLost() and self.hasTarget == True:
                self.tts.say("I have lost my Target!")
                self.hasTarget = None

            time.sleep(0.1)