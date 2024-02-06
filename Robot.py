from pydualsense import *
from robomaster import robot
from robomaster import camera
import time

# get dualsense instance
dualsense = pydualsense()
# initialize controller and connect
dualsense.init()

# set left l2 trigger to Rigid and set index 1 to force 255
dualsense.triggerL.setMode(TriggerModes.Pulse)
dualsense.triggerL.setForce(0, 100)
dualsense.triggerL.setForce(2, 150)
dualsense.triggerL.setForce(5, 200)

# set left r2 trigger to Rigid
dualsense.triggerR.setMode(TriggerModes.Pulse)
dualsense.triggerR.setForce(0, 100)
dualsense.triggerR.setForce(2, 150)
dualsense.triggerR.setForce(5, 200)

maxXSpeed = 2
maxZSpeed = 100

ep_robot = robot.Robot()
ep_robot.initialize(conn_type='ap', proto_type="udp")
ep_chassis = ep_robot.chassis
ep_camera = ep_robot.camera
ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)

fireType = "ir"
ep_robot.led.set_led(r=0, g=255, b=0)
ep_robot.gimbal.move(pitch=0, yaw=0)
x, y, z = 0, 0, 0

def setVelocity():
    ep_chassis.drive_speed(x = x, y = y, z = z)

def RideX(need):
    global x
    x = maxXSpeed * need / 255
    setVelocity()

def RideMinusX(need):
    global x
    x = maxXSpeed * need / 255 * -1
    setVelocity()

def RideZ(needX, needY):
    if(x > 5 or x < 5):
        global z
        z = maxZSpeed * needX / 128
        ep_robot.gimbal.drive_speed(0, needX / 128 * maxZSpeed)
        setVelocity()

def RideGribber(x, y):
    if(x > 5 or x < 5):
        ep_robot.gimbal.drive_speed(y / 128 * maxZSpeed * -1, x / 128 * maxZSpeed)

def Fire(b):
    if(b):
        ep_robot.blaster.fire(fireType)

def SelectFire(b):
    if(b):
        global fireType
        if(fireType == "ir"):
            fireType = "water"
            ep_robot.led.set_led(r=255, g=0, b=0)
        else:
            fireType = "ir"
            ep_robot.led.set_led(r=0, g=255, b=0)
def PlayAudio(b):
    if(b):
        ep_robot.play_audio(filename="maks.wav")

dualsense.l2_changed += RideX
dualsense.r2_changed += RideMinusX
dualsense.l1_changed += Fire
dualsense.left_joystick_changed += RideZ
dualsense.right_joystick_changed += RideGribber
dualsense.triangle_pressed += SelectFire
dualsense.square_pressed += PlayAudio

while not dualsense.state.DpadDown:
    ...

ep_camera.stop_video_stream()
ep_robot.close()
dualsense.close()