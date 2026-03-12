import RPi.GPIO as GPIO
import Stepper_Motor_HAT_Code.pi.python.DRV8825 as DRV8825Module
import time
import math
import threading

stepResolution = 2
baseRevolutionsPerSecond = 4

def calculateDelay(revolutionsPerSecond):
    revolutionsPerSecond = abs(revolutionsPerSecond)
    if revolutionsPerSecond:
        return (1.8 / 360 / 2 / baseRevolutionsPerSecond / stepResolution / revolutionsPerSecond)
    else:
        return (1.8 / 360 / 2 / baseRevolutionsPerSecond / stepResolution)

Motor1 = DRV8825Module.DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825Module.DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

class ControlledMotor:
    def __init__(self, motorObject):
        self.motor = motorObject
        self.currentSpeed = 0
        self.timer = 0
        self.currentlyPulsing = False
    
    def setSpeed(self, speed):
        self.currentSpeed = speed
        self.timer = calculateDelay(speed)
        if speed == 0:
            self.motor.Stop()
        else:
            self.motor.Start()
    
    def update(self, deltaTime):
        self.timer -= deltaTime
        self.timer = max(0, self.timer)

        direction = "forward" if self.currentSpeed > 0 else "backward"
        
        if self.timer <= 0 and self.currentSpeed != 0:
            self.currentlyPulsing = not self.currentlyPulsing
            self.motor.WriteStep(Dir=direction, state = self.currentlyPulsing)
            self.timer = calculateDelay(self.currentSpeed)
        elif self.currentSpeed == 0:
            self.motor.WriteStep(Dir=direction, state = False)

class DualMotorController:
    def __init__(self):
        self.motor1 = ControlledMotor(Motor1)
        self.motor2 = ControlledMotor(Motor2)
    
    def backgroundTask(self):
        startTime = time.perf_counter()
        lastFrameTime = startTime
        while True:
            deltaTime = time.perf_counter() - lastFrameTime

            self.motor1.update(deltaTime)
            self.motor2.update(deltaTime)

            lastFrameTime = time.perf_counter()
    
    def start(self):
        threading.Thread(target=self.backgroundTask, daemon=True).start()
        # self.backgroundTask()

    def stop(self):
        self.motor1.setSpeed(0)
        self.motor1.motor.Stop()
        self.motor2.setSpeed(0)
        self.motor2.motor.Stop()