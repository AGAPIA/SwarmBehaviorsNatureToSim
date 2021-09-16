import carla
import random

class Walker:

    instance_id = 0


    def __init__(self, actor_id,  controller_id, trace=[], targets =[]):
        self.actor_id = actor_id
        self.controller_id = controller_id
        self.trace = []
        self.targets = []
        self.walker_tag = Walker.instance_id
        Walker.instance_id += 1
        #self.actor = actor
        #self.controller = controller

    def get_location(self):
        return self.controller.get_transform()


    def set_actor(self, actor):
        self.actor = actor

    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        self.controller.start()

    def set_destination(self, target_location):
        self.controller.go_to_location(target_location)
    
    def set_max_speed(self, max_speed):
        self.max_speed = max_speed
        self.controller.set_max_speed(self.max_speed)

    def add_to_trace(self,frame,x,y):
        if(len(self.trace) < 8):
            self.trace.append((frame,self.walker_tag,x,y))
        else:
            self.trace.pop(0)
            self.trace.append((frame,self.walker_tag,x,y))

    def set_targets(self, targets):
        self.targets = targets

    def get_trace_length(self):
        return len(self.trace)

    def has_enough_trace(self):
        return len(self.trace) == 8

    def needs_new_target(self):
        return len(self.targets) == 0