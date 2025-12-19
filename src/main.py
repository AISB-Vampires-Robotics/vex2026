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

sensitivity = 1
mode = 0

refresh_queued = True

# Connection scheme
motorLF = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
motorRF = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
motorLR = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motorRR = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
motorIntake = Motor(Ports.PORT11)
motorPickaxe = Motor(Ports.PORT12)


def manual_control():
    global sensitivity
    global motorLF, motorRF, motorRF, motorRR, motorIntake
    global refresh_queued
    
    # See https://www.vexforum.com/t/wiki/67132/33
    # Or https://www.youtube.com/watch?v=gnSW2QpkGXQ
    forward = controller.axis3.position()
    sideways = controller.axis4.position()
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

    if controller.buttonUp.pressing():
        if sensitivity < 1:
            sensitivity += 0.25
            refresh_queued = True
    elif controller.buttonDown.pressing():
        if sensitivity > 0:
            sensitivity -= 0.25
            refresh_queued = True

    if controller.buttonR1.pressing():
        motorPickaxe.set_velocity(100, PERCENT)
        if motorPickaxe.position(DEGREES) < 20:
            motorPickaxe.spin_to_position(90, DEGREES, False)
        elif motorPickaxe.position(DEGREES) > 85:
            motorPickaxe.spin_to_position(0, DEGREES, False)

def auto_control():
    pass

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
    if (mode == 0 or mode == 2):
        display.print("Sens: N/A")
    else:
        display.print("Sens: " + str(sensitivity))
    display.next_row()
    display.print("Left")
    display.set_cursor(display.row(), 20)
    display.print("Right")
    refresh_queued = False


while True:
    if controller.buttonRight.pressing():
        if mode != 2:
            mode = mode + 1
            refresh_queued = True
    elif controller.buttonLeft.pressing():
        if mode != 0:
            mode = mode - 1
            refresh_queued = True

    if mode == 0:
        disable()
    elif mode == 1:
        manual_control()
    elif mode == 2:
        auto_control()

    if refresh_queued:
        draw(controller.screen)    
