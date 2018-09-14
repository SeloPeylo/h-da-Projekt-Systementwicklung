# -*- encoding: UTF-8 -*-

"""
This example shows how to use ALTracker with red ball.
"""

import time
import argparse
from naoqi import ALProxy

NAO_IP = "141.100.47.205"

def main(IP, PORT, ballSize):

    print "Connecting to", IP, "with port", PORT
    motion = ALProxy("ALMotion", IP, PORT)
    posture = ALProxy("ALRobotPosture", IP, PORT)
    tracker = ALProxy("ALTracker", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    alife = ALProxy("ALAutonomousLife", IP, PORT)

    alife.setState("disabled")
    # First, wake up
    motion.wakeUp()
    print "waking up"

   

    tracker.stopTracker()
    tracker.unregisterAllTargets()
    tracker.toggleSearch(False)

    tts.say("Red Ball Detector started")

    fractionMaxSpeed = 0.8
    # Go to posture stand
    posture.goToPosture("StandInit", fractionMaxSpeed)

    # Add target to track.
    targetName = "RedBall"
    diameterOfBall = ballSize
    tracker.registerTarget(targetName, diameterOfBall)
    
	
    # set modes
    mode = "Head"
    tracker.setMode(mode)

    # Then, start tracker.
    tracker.track(targetName)

    print "ALTracker successfully started, now show a red ball to robot!"
    print "Use Ctrl+c to stop this script."
    hasTarget = None
    lastPositions = []

    try:
        while True:

            print tracker.getTargetPosition(0)
            if tracker.isNewTargetDetected():
                tracker.pointAt("LArm", tracker.getTargetPosition(0), 0, 0.8)
                tracker.pointAt("RArm", tracker.getTargetPosition(0), 0, 0.8)

                if len(lastPositions) <= 5:
                    lastPositions.append(tracker.getTargetPosition(0))
                else:
                    lastPositions.pop()
                    lastPositions.append(tracker.getTargetPosition(0))

            if tracker.isNewTargetDetected() and hasTarget == None:
                tts.say("I have detected a red ball")
                tracker.pointAt("LArm", tracker.getTargetPosition(0), 0, 0.8)
                print tracker.getTargetPosition(0)
                posture.goToPosture("StandInit", fractionMaxSpeed)
                hasTarget = True

       
            if tracker.isTargetLost() and hasTarget == True:
                tts.say("I have lost my Target!")
                hasTarget = None

            time.sleep(0.1)

    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."

        print lastPositions

    # Stop tracker, go to posture Sit.
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    #posture.goToPosture("Sit", fractionMaxSpeed)
    motion.rest()

    print "ALTracker stopped."
    tts.say("Red Ball Detector stopped.")
    alife.setState("solitary")

if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=NAO_IP,
                        help="Robot ip address.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number.")
    parser.add_argument("--ballsize", type=float, default=0.06,
                        help="Diameter of ball.")

    args = parser.parse_args()

    main(args.ip, args.port, args.ballsize)