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
import math
from enum import Enum

class Mode(Enum):
    DISABLED = 0
    MANUAL = 1
    AUTO = 2

brain = Brain()
controller = Controller()

sensitivity = 1
mode = Mode.DISABLED

# Connection scheme
motorLF = Motor(Ports.PORT1)
motorLR = Motor(Ports.PORT2)
motorRF = Motor(Ports.PORT3)
motorRR = Motor(Ports.PORT4)
motorIntake = Motor(Ports.PORT11)


def manual_control():
    global sensitivity
    global motorLF, motorRF, motorRF, motorRR, motorIntake
    
    # See https://www.vexforum.com/t/wiki/67132/33
    # Or https://www.youtube.com/watch?v=gnSW2QpkGXQ
    y = controller.axis3.position()
    x = controller.axis4.position()
    turn = controller.axis1.position()

    # don't touch
    theta = math.atan2(y, x)
    power = math.hypot(x, y)

    sin = math.sin(theta - math.pi/4)
    cos = math.cos(theta - math.pi/4)


    velocity_LF = sensitivity * (power * cos + turn)
    velocity_RF = sensitivity * (power * sin + turn)

    velocity_LR = sensitivity * (power * sin - turn)
    velocity_RR = sensitivity * (power * cos - turn)

    motorLF.spin(FORWARD, max(-100, min(velocity_LF, 100)), PERCENT)
    motorLR.spin(FORWARD, max(-100, min(velocity_LR, 100)), PERCENT)
    motorRR.spin(FORWARD, max(-100, min(velocity_RR, 100)), PERCENT)
    motorRF.spin(FORWARD, max(-100, min(velocity_RF, 100)), PERCENT)


    if controller.buttonL1.pressing():
        motorIntake.spin(FORWARD, 25, PERCENT)
    elif controller.buttonL2.pressing():
        motorIntake.spin(FORWARD, 50, PERCENT)
    else:
        motorIntake.stop()

    if controller.buttonUp.pressing():
        if sensitivity < 1:
            sensitivity += 0.25
    elif controller.buttonDown.pressing():
        if sensitivity > 0:
            sensitivity -= 0.25

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
    global sensitivity
    display.clear_screen()
    display.set_cursor(1, 1)

    display.print("Mode: " + mode.name)
    display.next_row()
    display.print("Sens: " + str(sensitivity))
    display.next_row()
    display.print("L")
    display.set_cursor(display.row(), 19)
    display.print("R")


while True:

    if controller.buttonRight.pressing():
        if mode.value != 2:
            mode = Mode(mode.value + 1)
    elif controller.buttonLeft.pressing():
        if mode.value != 0:
            mode = Mode(mode.value - 1)


    if mode.value == Mode.DISABLED:
        disable()
    elif mode.value == Mode.MANUAL:
        manual_control()
    elif mode.value == Mode.AUTO:
        auto_control()

    draw(controller.screen)
    