## Mark Calabio
## 12488362

## resource.py - Implementation of Resource representation
## Each resource is represented by a data structure RCB[n], which is to be
## used in main.py

from collections import deque

class Resource():

    def __init__(self, r_id, state, inventory):
        self.id = r_id
        self.state = state
        self.waitlist = deque()
        ## self.inventory

    def add_to_waitlist(self, processid):
        self.waitlist.append(processid)

        return processid
