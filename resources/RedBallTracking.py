# -*- encoding: UTF-8 -*-

"""
This example shows how to use ALTracker with red ball.
"""

import time
import argparse
from naoqi import ALProxy

#   IP Adresse als Makro
NAO_IP = "141.100.53.93"

#   Bewegungserkennung durch Vergleich zweier Positionen
def getBallStatus(yold, ynew, xpos):
    tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
    
    if yold is None:
        return

    difference = 0
    difference = yold - ynew
    tolerance = 0.1
    minDist = 0.45
    maxDist = 1.8

    if xpos <= minDist:
        print "Too Close"
        tts.say("Sphero you are too close")
    elif xpos >= maxDist:
        print "Too Far"
        tts.say("Sphero come back. I miss you.")
    elif difference <= -tolerance:
        print "Left"
        tts.say("Left")
    elif difference >= tolerance:
        print "Right"
        tts.say("Right")


def main(IP, PORT, ballSize):

    #   Initialisierung der Proxys
    print "Connecting to", IP, "with port", PORT
    motion = ALProxy("ALMotion", IP, PORT)
    posture = ALProxy("ALRobotPosture", IP, PORT)
    tracker = ALProxy("ALTracker", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    alife = ALProxy("ALAutonomousLife", IP, PORT)

    #   Autonomous Life ausschalten
    alife.setState("disabled")
    posture.goToPosture("StandInit", 0.8)
    motion.wakeUp()

    #   ALTracker resetten und konfigurieren
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    tracker.toggleSearch(False)

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
    tts.say("Red Ball Detector started")

    print "ALTracker successfully started, now show a red ball to robot!"
    print "Use Ctrl+c to stop this script."

    # Variablen für die Tracking-Schleife
    hasTarget = None    # Wird True gesetzt wenn ein Target fokussiert wurde
    yold = None
    ynew = None
    xpos = None

    #   Routine nach der Init.. hier wird auf das getrackte Objekt reagiert
    try:
        while True:
            print tracker.getTargetPosition(0)

            if hasTarget == True:
                yold = ynew
                ynew = tracker.getTargetPosition(0)[1]
                xpos = tracker.getTargetPosition(0)[0]
                getBallStatus(yold, ynew, xpos)
                tracker.pointAt("LArm", tracker.getTargetPosition(0), 0, 0.8)


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