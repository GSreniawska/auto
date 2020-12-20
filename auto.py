import time
import RPi.GPIO as GPIO
from rplidar import RPLidar

GPIO.setmode(GPIO.BOARD)
RIGHT_MOVE_PIN = 16
RIGHT_POWER_PWM_PIN = 12
LEFT_MOVE_PIN = 18
LEFT_POWER_PIN = 13
PORT_NAME = '/dev/ttyUSB0'
LIDAR = RPLidar(PORT_NAME)


def setup():
    GPIO.setup(RIGHT_MOVE_PIN, GPIO.OUT)  # right side
    GPIO.setup(RIGHT_POWER_PWM_PIN, GPIO.OUT)
    GPIO.setup(LEFT_MOVE_PIN, GPIO.OUT)  # left side
    GPIO.setup(LEFT_POWER_PIN, GPIO.OUT)
    GPIO.setwarnings(False)

    # setting PWMs
    power = 0
    motor_right_velocity = GPIO.PWM(RIGHT_POWER_PWM_PIN, 50)
    motor_left_velocity = GPIO.PWM(LEFT_POWER_PIN, 50)
    motor_right_velocity.start(power)
    motor_left_velocity.start(power)
    # setup lidar sensor
    PORT_NAME = '/dev/ttyUSB0'
    LIDAR = RPLidar(PORT_NAME)


def go_forward() -> None:
    power = 20
    RIGHT_POWER_PWM_PIN.ChangeDutyCycle(power)
    LEFT_POWER_PIN.ChangeDutyCycle(power)
    GPIO.output(RIGHT_MOVE_PIN, GPIO.LOW)
    GPIO.output(LEFT_MOVE_PIN, GPIO.LOW)


def lidar_made_full_turn(previous_angle: float, actual_angle: float) -> bool:
    return previous_angle - actual_angle >= 50.


def main():
    duration = 0
    start = time.time()
    while duration >= 10.:
        for measurement in LIDAR.iter_measurments():
            power = 10
            if measurement[3] / 10. <= 30.:
                RIGHT_POWER_PWM_PIN.ChangeDutyCycle(power)
                LEFT_POWER_PIN.ChangeDutyCycle(power)
                GPIO.output(RIGHT_MOVE_PIN, GPIO.LOW)
                GPIO.output(LEFT_MOVE_PIN, GPIO.HIGH)
            else:
                go_forward()
        end = time.time()
        duration = end - start


if __name__=="__main__":
    main()