# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       A. Simonov                                                   #
# 	Created:      01/12/2025, 12:18:38                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()

mode = 0

refresh_queued = True

tubePos = False
barrierPos = False

# Connection scheme
motorLF = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
motorRF = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
motorLR = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
motorRR = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
motorTube = Motor(Ports.PORT16)
motorIntake = Motor(Ports.PORT10)
motorBarrier = Motor(Ports.PORT15)
motorPickaxe = Motor(Ports.PORT14)

def manual_control():
    global motorLF, motorRF, motorRF, motorRR, motorIntake, motorPickaxe, motorBarrier
    global refresh_queued, tubePos, barrierPos
    
    # See https://www.vexforum.com/t/wiki/67132/33
    # Or https://www.youtube.com/watch?v=gnSW2QpkGXQ
    forward = controller.axis4.position()
    sideways = controller.axis3.position()
    turn = controller.axis1.position()

    # don't touch
    
    leftB = forward - sideways - turn
    rightB = forward + sideways - turn
    leftF = forward + sideways + turn
    rightF = forward - sideways + turn

    motorLF.spin(FORWARD, leftF, PERCENT)
    motorRF.spin(FORWARD, rightF, PERCENT)
    motorLR.spin(FORWARD, leftB, PERCENT)
    motorRR.spin(FORWARD, rightB, PERCENT)

    if controller.buttonL1.pressing():
        motorIntake.spin(REVERSE, 100, PERCENT)
    elif controller.buttonL2.pressing():
        motorIntake.spin(FORWARD, 100, PERCENT)
    else:
        motorIntake.stop()

    if controller.buttonR1.pressing():
        motorPickaxe.spin_to_position(90 + motorPickaxe.position(DEGREES), DEGREES, 100, PERCENT, wait=False)
    elif controller.buttonR2.pressing():
        motorPickaxe.spin_to_position(-90 + motorPickaxe.position(DEGREES), DEGREES, 100, PERCENT, wait=False)


    if controller.buttonA.pressing():
        motorTube.spin(FORWARD, 15, PERCENT)
    elif controller.buttonB.pressing():
        motorTube.spin(REVERSE, 15, PERCENT)
    else:
        motorTube.stop()

    if controller.buttonX.pressing():
        if tubePos:
            #motorTube.spin_to_position(90, DEGREES, 100, PERCENT, wait=True)
            motorTube.spin(REVERSE, 15, PERCENT)
            tubePos = False
        else:
            motorTube.spin(FORWARD, 50, PERCENT)
            #motorTube.spin_to_position(0, DEGREES, 100, PERCENT, wait=True)
            tubePos = True

    if controller.buttonY.pressing():
        if barrierPos:
            motorBarrier.spin_to_position(-270, DEGREES, 100, PERCENT, wait=True)
            barrierPos = False
        else:
            motorBarrier.spin_to_position(0, DEGREES, 100, PERCENT, wait=True)
            barrierPos = True


# TODO
def auto_control2():
    global mode, refresh_queued

    motorBarrier.spin_to_position(-270, DEGREES, 100, PERCENT, wait=True)
    
    move(6, 100, 370)
    
    motorIntake.spin(REVERSE, 100, PERCENT)

    move(3, 80, 1555)
    
    wait(3, SECONDS)
    motorIntake.stop()
    move(4, 100, 1000)
    move(2, 100, 1000)
    move(4, 100, 1125)
    move(2, 100, 1100)
    motorBarrier.spin_to_position(0, DEGREES, 100, PERCENT, wait=True)

    move(4, 100, 1000)
    motorIntake.spin(REVERSE, 100, PERCENT)
    wait(5, SECONDS)

    move(3, 25, 1000)

    mode = 1
    refresh_queued = True

# Places preloaded block into the long goal
# Robot should be alligned to the top right corner of the parking zone
def auto_control():
    global mode, refresh_queued
    move(1, 100, 1000)
    move(3, 100, 1300)
    move(1, 100, 1200)
    move(4, 100, 1000)

    motorIntake.spin(REVERSE, 100, PERCENT)

    wait(4, SECONDS)
    
    mode = 1
    refresh_queued = True

def disable():
    global motorLF, motorRF, motorRF, motorRR, motorIntake
    motorLF.stop()
    motorLR.stop()
    motorRF.stop()
    motorRR.stop()
    motorIntake.stop()

def draw(display):
    global sensitivity, refresh_queued
    display.clear_screen()
    display.set_cursor(1, 1)

    if (mode == 0):
        display.print("Mode: DISABLED")
    elif (mode == 1): 
        display.print("Mode: MANUAL")
    elif (mode == 2):
        display.print("Mode: AUTO")
    display.next_row()
    display.print("Left")
    display.set_cursor(display.row(), 20)
    display.print("Right")
    refresh_queued = False

def move(direction, power, duration):
    # 1 = turn left, 2 = turn right, 3 = forward, 4 = backward, 5 = strafe right, 6 = strafe left
    if direction == 1:
        motorLF.set_velocity(power, PERCENT)
        motorRF.set_velocity(power, PERCENT)
        motorLR.set_velocity(power, PERCENT)
        motorRR.set_velocity(power, PERCENT)

        motorLF.spin(REVERSE)
        motorRF.spin(REVERSE)
        motorLR.spin(FORWARD)
        motorRR.spin(FORWARD)
        wait(duration, MSEC)
        motorLF.stop()
        motorRF.stop()
        motorLR.stop()
        motorRR.stop()
    if direction == 2:
        motorLF.set_velocity(power, PERCENT)
        motorRF.set_velocity(power, PERCENT)
        motorLR.set_velocity(power, PERCENT)
        motorRR.set_velocity(power, PERCENT)

        motorLF.spin(FORWARD)
        motorRF.spin(FORWARD)
        motorLR.spin(REVERSE)
        motorRR.spin(REVERSE)
        wait(duration, MSEC)
        motorLF.stop()
        motorRF.stop()
        motorLR.stop()
        motorRR.stop()
    if direction == 3:
        motorLF.set_velocity(power, PERCENT)
        motorRF.set_velocity(power, PERCENT)
        motorLR.set_velocity(-power, PERCENT)
        motorRR.set_velocity(-power, PERCENT)

        motorLF.spin(FORWARD)
        motorRF.spin(REVERSE)
        motorLR.spin(FORWARD)
        motorRR.spin(REVERSE)
        wait(duration, MSEC)
        motorLF.stop()
        motorRF.stop()
        motorLR.stop()
        motorRR.stop()
    if direction == 4:
        motorLF.set_velocity(power, PERCENT)
        motorRF.set_velocity(power, PERCENT)
        motorLR.set_velocity(power, PERCENT)
        motorRR.set_velocity(power, PERCENT)

        motorLF.spin(REVERSE)
        motorRF.spin(FORWARD)
        motorLR.spin(FORWARD)
        motorRR.spin(REVERSE)
        wait(duration, MSEC)
        motorLF.stop()
        motorRF.stop()
        motorLR.stop()
        motorRR.stop()
    if direction == 5:
        motorLF.set_velocity(power, PERCENT)
        motorRF.set_velocity(power, PERCENT)
        motorLR.set_velocity(power, PERCENT)
        motorRR.set_velocity(power, PERCENT)


        motorLF.spin(FORWARD)
        motorRF.spin(FORWARD)
        motorLR.spin(FORWARD)
        motorRR.spin(FORWARD)
        wait(duration, MSEC)
        motorLF.stop()
        motorRF.stop()
        motorLR.stop()
        motorRR.stop()
    if direction == 6:
        motorLF.set_velocity(power, PERCENT)
        motorRF.set_velocity(power, PERCENT)
        motorLR.set_velocity(power, PERCENT)
        motorRR.set_velocity(power, PERCENT)

        motorLF.spin(REVERSE)
        motorRF.spin(REVERSE)
        motorLR.spin(REVERSE)
        motorRR.spin(REVERSE)
        wait(duration, MSEC)
        motorLF.stop()
        motorRF.stop()
        motorLR.stop()
        motorRR.stop()

while True:
    if controller.buttonRight.pressing():
        if mode != 2:
            mode += 1
            refresh_queued = True
    elif controller.buttonLeft.pressing():
        if mode != 0:
            mode -= 1
            refresh_queued = True

    if refresh_queued:
        draw(controller.screen)

    if mode == 0:
        disable()
    elif mode == 1:
        manual_control()
    elif mode == 2:
        #auto_control()
        auto_control2()