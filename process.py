## Mark Calabio
## 12488362

## process.py - Implementation of Process representation
## Each process is represented by a data structure PCB[n], which is to be
## used in main.py

from collections import deque

class Process():

    def __init__(self, index, state, parent):
        self.id = index
        self.state = state
        self.parent = parent        ## To be populated by parent process
        #self.priority = priority
        self.children = []    ## To be populated by self.
        self.resources = []

    def create_process(self, index):
        '''Creates a new child process'''
        new_process = Process(index, 1, self.id)

        ##print("New Child process {} created from Parent process {}".format(index, self.id))
        return new_process

    def destroy(self):
        '''Destroy child process, and recursively destroy child's descendants, etc.'''

        ## for all k in children of j
        ##      destroy(k)
        ## remove j from list of children of i
        ## remove j from RL or waiting list
        ## release all resources of j
        ## free PCB of j

        #print("n processes destroyed") ## display number of processes
        return True

    def add_child(self, index):
        self.children.append(index)

    def add_resource(self, resource):
        self.resources.append(resource)
        return
    
    def __str__(self):
        string = "Process id/index: {} \t State: {} \t Birthed from Parent Process: {}".format(self.id, self.state, self.parent)
        return string
