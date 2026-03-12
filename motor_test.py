import RPi.GPIO as GPIO
import Stepper_Motor_HAT_Code.pi.python.DRV8825 as DRV8825Module
import time

Motor1 = DRV8825Module.DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825Module.DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

revolutions = 1
stepResolution = 8
pythonStupidityRatio = 1
# pythonStupidityRatio = 2.1 / 2.0 # INNACCURATE - Calculated from an "experiment"

lastTime = time.time()
# Motor2.TurnStep(Dir='forward', steps=revolutions * 200 * stepResolution, stepdelay=1.8 / 360 / stepResolution / 2 / pythonStupidityRatio)
Motor2.TurnStep(Dir='backward', steps=440 * 2, stepdelay=1 / 440 / 2 / 2)
# Motor1.TurnStep(Dir='forward', steps=revolutions * 200 * stepResolution, stepdelay=1.8 / 360 / stepResolution / 2 / pythonStupidityRatio)
Motor2.Stop()
# Motor1.Stop()
print(time.time() - lastTime)