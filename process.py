## Mark Calabio
## 12488362

## process.py - Implementation of Process representation
## Each process is represented by a data structure PCB[n], which is to be
## used in main.py

from collections import deque

class Process():

    def __init__(self, index, priority, state, parent): ### ADD PRIORITY AS AN ARGUMENT #####
        self.id = index
        self.state = state
        self.parent = parent        
        self.priority = priority
        self.children = []    
        self.resources = {} ##{} ## in (resource, allocated units)

    def add_child(self, index):
        self.children.append(index)

    def add_resource(self, resource, units):
        if resource in self.resources:
            self.resources[resource] += units
        else:
            self.resources[resource] = units
        return
    
    def __str__(self):
        string = "Process id/index: {} \t State: {} \t Birthed from Parent Process: {}".format(self.id, self.state, self.parent)
        return string
