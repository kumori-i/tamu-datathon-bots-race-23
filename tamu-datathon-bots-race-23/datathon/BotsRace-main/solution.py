import random

from bots_race.environment_factory import EnvironmentFactory

class Solution:
    def __init__(self):
        # TODO code to initialize your solution  
        # self.prevAngAccel = 0.0
        # self.prevLinAccel = 0
        # self.counterState = False
        # self.moving = False

        self.holding = False
        self.step1 = True
        self.lineCheck = False
        self.isLine = False
        # self.prevAngle = 0
        # self.counter = False
        # self.prevPoints = 0

        self.count = 0
        self.max_value = 0
        self.first = False
        self.angular = 0
        self.movement = True
        self.turn = False
        self.lastAngle= 0
        self.anotherOne = False
        self.opp = 0.02
        pass

    def track(self):
        # TODO fill in code here which initializes your controller
        # whenever your robot is placed on a new track
        env_factory = EnvironmentFactory(debug=True)
        env = env_factory.get_random_environment()
        robot_observation = env.reset()
        pass

    # should return [linear_acceleration, angular_acceleration]
    def get_action(self, robot_observation):
        # TODO replace code here to see robot_observation to compute an action whenever your robot receives an observation
        # if not(self.counterState):
        #     #if not(self.moving):
        #     self.prevAngAccel = 2*(robot_observation[2] - robot_observation[4])
        #     #else: self.prevAngAccel = self.prevAngAccel / 5
        #     self.counterState = True
        #     if (self.prevAngAccel < 0):
        #         if (self.prevAngAccel > -0.004):
        #             #print(self.prevAngAccel)
        #             self.prevLinAccel = 0.001
        #             self.prevAngAccel = -self.prevAngAccel
        #             return [self.prevLinAccel, self.prevAngAccel]
        #         else:
        #             self.prevLinAccel = 0
        #             return [self.prevLinAccel, self.prevAngAccel]
        #     else:
        #         if (self.prevAngAccel < 0.004):
        #             self.prevLinAccel = 0.001
        #             self.prevAngAccel = -self.prevAngAccel
        #             return [self.prevLinAccel, self.prevAngAccel]
        #         else: 
        #             self.prevLinAccel = 0
        #             return [self.prevLinAccel, self.prevAngAccel]
        # else:
        #     self.counterState = False
        #     return [-self.prevLinAccel, -self.prevAngAccel]
        if self.step1:
            
            if not(self.holding):
                self.holding = True
                if robot_observation[2] < robot_observation[4]:
                    return[0, self.opp]
                else:
                    self.opp = -self.opp
                    return [0, self.opp]
            else:
                if not(robot_observation[2] == robot_observation[4]):
                    return [0, 0]
                elif not(robot_observation[1] > robot_observation[3]):
                    return [0, 0]
                else:
                    self.step1 = False
                    return [0, -self.opp]
        else:
            if not(self.lineCheck):
                
                self.lineCheck = True
                return [0.001, 0]
            else:
                if  (robot_observation[2] == robot_observation[4]) and ((robot_observation[1] == robot_observation[3])) and not(self.isLine) and not(self.turn):#((robot_observation[2] - robot_observation[4]) >= -0.002) and ((robot_observation[2] - robot_observation[4]) <= 0.002)         ((robot_observation[2] - robot_observation[4]) >= -0.02) and ((robot_observation[2] - robot_observation[4]) <= 0.02) and ((robot_observation[1] - robot_observation[3]) >= -0.02) and ((robot_observation[1] - robot_observation[3]) <= 0.02)
                    self.isLine = True
                if self.isLine:
                    return [0.001, 0]
                else:
                    self.turn = True
                    if self.movement:
                        if robot_observation[2] / 0.024 > 0.1 and not(self.first):
                            self.anotherOne = True
                        elif robot_observation[4] / 0.024 > 0.1 and not(self.first):
                            self.anotherOne = True
                        if self.count == 0:
                            if self.anotherOne:
                                self.movement = False
                                self.anotherOne = False
                                return [0.0, -self.lastAngle]
                            
                            if not(self.first):
                                self.count += 1
                                self.first = True
                                return [0.001, 0]
                            else:
                                self.count += 1
                                return [0.001, -self.lastAngle]
                        else:
                            if self.count < 5:
                                self.count += 1
                                return [0.001, 0]
                            elif self.count > 4:
                                self.count += 1
                                if self.count == 10:
                                    self.count = 0
                                    self.movement = False
                                return [-0.001, 0]
                            else:
                                self.count += 1
                                return [0, 0]
                    else:
                        self.movement = True 
                        if robot_observation[2] > robot_observation[4]:
                            self.lastAngle = 0.785*(robot_observation[2] / 0.024) / (3.14 * 50) #robot_observation[4]
                            return [0, self.lastAngle]
                        elif robot_observation[2] == robot_observation[4]:
                            self.lastAngle = 0
                            return [0, 0]
                        else: 
                            self.lastAngle = -0.785*(robot_observation[4] / 0.024)  / (3.14 * 50)#robot_observation[2]
                            return [0, self.lastAngle]
                        
                        
            
                

        #return  [random.random() - .5, random.random() - .5]#[1, 1]

# this is example of code to test your solution locally
if __name__ == '__main__':
    solution = Solution()

    # TODO check out the environment_factory.py file to create your own test tracks
    env_factory = EnvironmentFactory(debug=True)
    env = env_factory.get_random_environment()

    done = False
    fitness = 0
    robot_observation = env.reset()
    while not done:
        robot_action = solution.get_action(robot_observation)
        robot_observation, fitness, done = env.step(robot_action)
    print('Solution score:', fitness)