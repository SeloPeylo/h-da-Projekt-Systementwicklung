# -*- encoding: UTF-8 -*-

"""
This example shows how to use ALTracker with red ball.
"""

import time
import argparse
from naoqi import ALProxy

def main(IP, PORT, ballSize):

    print "Connecting to", IP, "with port", PORT
    motion = ALProxy("ALMotion", IP, PORT)
    posture = ALProxy("ALRobotPosture", IP, PORT)
    tracker = ALProxy("ALTracker", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)

    # First, wake up.
    motion.wakeUp()

    tts.say("Red Ball Detector started")

    fractionMaxSpeed = 0.8
    # Go to posture stand
    posture.goToPosture("StandInit", fractionMaxSpeed)

    # Add target to track.
    targetName = "RedBall"
    diameterOfBall = ballSize
    tracker.registerTarget(targetName, diameterOfBall)
    
	
    # set modes
    mode = "WholeBody"
    tracker.setMode(mode)

    # Then, start tracker.
    tracker.track(targetName)

    tracker.toggleSearch(True)

    print "ALTracker successfully started, now show a red ball to robot!"
    print "Use Ctrl+c to stop this script."

    if tracker.isNewTargetDetected():
        tts.say("I have detected a Red Ball!")
        tracker.pointAt("LArm", tracker.getTargetPosition(0), 0, 0.8)
        tracker.toggleSearch(False)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."

    # Stop tracker, go to posture Sit.
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    #posture.goToPosture("Sit", fractionMaxSpeed)
    motion.rest()

    print "ALTracker stopped."
    tts.say("Red Ball Detector stopped.")

if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="141.100.47.205",
                        help="Robot ip address.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number.")
    parser.add_argument("--ballsize", type=float, default=0.06,
                        help="Diameter of ball.")

    args = parser.parse_args()

    main(args.ip, args.port, args.ballsize)