#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import socket
import math
import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
motor1 = Motor(Port.A)
motor2 = Motor(Port.B)
gyro = GyroSensor(Port.S3)
sonic = UltrasonicSensor(Port.S2)
color_sensor = ColorSensor(Port.S1)
ev3.speaker.beep()
ev3.screen.clear()
color = "unknown"
use_color = False
print("Calibrating... DO NOT TOUCH!")
ev3.screen.draw_text(10, 100, "CALIBRATING DO NOT TOUCH!!!")
ev3.screen.load_image(ImageFile.WARNING)
while True:
    gyro_min, gyro_max = 440, -440
    gyro_sum = 0
    for _ in range(200):
        val = gyro.speed()
        gyro_sum += val
        if val > gyro_max: gyro_max = val
        if val < gyro_min: gyro_min = val
        wait(5)
    if gyro_max - gyro_min < 2:
        break

# Save our true resting drift value
gyro_offset = gyro_sum / 200
ev3.speaker.beep(frequency=1000, duration=500)
print("Calibrated! Offset is:", gyro_offset)
ev3.screen.load_image(ImageFile.ACCEPT)
def music():
    ev3.speaker.beep(frequency=500, duration=100)
    ev3.speaker.beep(frequency=600, duration=100)
    ev3.speaker.beep(frequency=700, duration=100)
    ev3.speaker.beep(frequency=800, duration=100)
    ev3.speaker.beep(frequency=900, duration=100)
    ev3.speaker.beep(frequency=1000, duration=100)
    ev3.speaker.beep(frequency=1500, duration=500)

def moveBothMotors(speed, degrees):
    motor1.run_angle(speed, degrees, wait=False)
    motor2.run_angle(speed, degrees, wait=True)

def one_angle(d):
    circumference = math.pi * d
    return circumference / 360
        

def move_cm(cm, speed, one_angle):
    to_move = cm / one_angle
    moveBothMotors(speed, to_move)


def gyro_turn(target_angle, max_speed):
    # We will track our angle manually since we can't use gyro.angle()
    current_angle = 0.0
    last_time = time.time()
    
    while True:
        # Calculate how much time passed since the last loop
        now = time.time()
        dt = now - last_time
        last_time = now
        
        # Read the raw speed and SUBTRACT the drift offset we found at startup!
        real_speed = gyro.speed() - gyro_offset
        
        # Add the speed to our angle (Angle = Speed * Time)
        current_angle += real_speed * dt
        
        error = target_angle - current_angle
        
        # Stop check
        if abs(error) < 2:
            break
            
        if error > 0:
            direction = 1
        else:
            direction = -1
            
        # Standard flat speed turn
        motor1.run(max_speed * direction)
        motor2.run(-max_speed * direction)
        wait(10) # 10ms loop time works best for this math
        
    motor1.brake()
    motor2.brake()
    wait(200)

def forward(speed):
    motor1.run(speed)
    motor2.run(speed)


def stop():
    motor1.brake()
    motor2.brake()

def color_name(c):
    if c == Color.RED:
        return "red"
    elif c == Color.GREEN:
        return "green"
    elif c == Color.BLUE:
        return "blue"
    elif c == Color.YELLOW:
        return "yellow"
    elif c == Color.WHITE:
        return "white"
    elif c == Color.BLACK:
        return "black"
    else:
        return "unknown"

one_angle = one_angle(5.6)
brick_ip = "10.42.0.18"
port = 5000
s = socket.socket()
s.connect(('10.42.0.1', port))
while True:
    if use_color == True:
        to_send = "Distance from wall: " + str(sonic.distance()) + " millimetres; Color of object analysed: " + color + "; Explain what you will do and choose a command on a newline"
        use_color = False
    else:
        to_send = "Distance from wall: " + str(sonic.distance()) + " millimetres; Explain what you will do and choose a command on a newline"
    s.send(to_send.encode('utf-8'))
    ev3.speaker.beep()
    response = s.recv(1024).decode('utf-8')
    ev3.screen.clear
    ev3.screen.draw_text(10, 100, response)
    print(response)
    lines = response.splitlines() 
    for line in lines:
        line = line.strip()
        if not line:
            continue
        ev3.speaker.beep()
        response_split = line.split(" ", 1)
        command = response_split[0]
        if command != "ANALYSE":
            value = response_split[1]
        
        if len(response_split) > 1:
            value = response_split[1]
        else:
            value = ""
        
        if command == "MOVE_CM":
            if sonic.distance() <= 10:
                break
            move_cm(int(value), 300, one_angle)
        elif command == "TURN":
            gyro_turn(int(value), 200)
        elif command == "SAY":
            ev3.speaker.say(value)
        elif command == "ANALYSE":
            to_move_mm = sonic.distance() - 40
            to_move = to_move_mm / 100
            move_cm(to_move, 300, one_angle)
            detected_color = color_sensor.color()
            color = color_name(detected_color)
            use_color = True
            move_cm(-to_move, 300, one_angle)
        else:
            print("Invalid command from AI!")
    

s.close()
# Write your program here.
ev3.speaker.beep()
