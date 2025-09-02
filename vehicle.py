import os
import time

class engineered_vehicle:

    def __init__(self):
        self.speed = 0
        self.__status = "stopped"
        self.__temperature = 0
        

    def get_status(self):
        pass

class formula_one(engineered_vehicle):

    MAX_SPEED = 300
    MIN_SPEED = 0

    #Constructor
    def __init__(self):
        super().__init__()
        self._degrees_right = 0
        self._degrees_left = 0
        self._rpms = 0
        self._wheel_status = 0

    
    def _get_wheel_status(self):
        return self._wheel_status
    
    def _set_wheel_status(self,new_wheel_status):
        self.wheel_status = new_wheel_status
  
    def _get_rpms(self):
        return self._rpms
    
    
    def _set_rpms(self,new_rpms):
        self._rpms = new_rpms

    
    def accelerate(self,speed):
        """ Argument: Initial speed
            Output: Speed and Revolutions Per Minute
        """
        rpm = 0
        while self.speed<= 290:
            try:
                os.system('cls')
                self.speed += 10
                rpm += 100
                self._set_rpms(rpm)
                

                print(f"speed: {self.speed}\n")
                print(f"RPMS: {self._get_rpms()}\n")
                time.sleep(0.1)
            except ValueError:
                print("Over the speed limit")
        

    def decelerate(self,speed,rpm):
        """ Argument: Initial speed
            Output: Speed and Revolutions Per Minute
        """        
        while self.speed>=0:
            try:
                os.system('cls')
                self.speed -= 10
                rpm -= 100
                self._set_rpms(rpm)
                

                print(f"speed: {self.speed}\n")
                print(f"RPMS: {self._get_rpms()}\n")
                time.sleep(0.1)
            except ValueError:
                print("Car in reverse")

    def steer_right(self,_degrees_right):
        """ Argument: Degrees of steer rotation 
            Output: message of confirmation of steering
        """
        if self.speed <= 120:
            print(f"steering{_degrees_right} degrees to the right")
            
        else:return "too fast. slow down."

    def steer_left(self,_degrees_left):
        """ 
            Argument: Degrees of steer rotation 
            Output: message of confirmation of steering
        """
        if self.speed <= 120:
            print(f"steering{_degrees_left}degrees")
        else:return "too fast. slow down."

    


class sapce_x_rocket_ship:

    def __init__(self):
        pass

         
class main:
    car = formula_one()
    speed = 1
    car.accelerate(speed)
    
