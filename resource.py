## Mark Calabio
## 12488362

## resource.py - Implementation of Resource representation
## Each resource is represented by a data structure RCB[n], which is to be
## used in main.py

from collections import deque

class Resource():

    def __init__(self, r_id, inventory):
        self.id = r_id
        self.state = inventory
        self.waitlist = deque()     ## STRICTLY FIFO ORDER (NO PRIORITY)
        self.inventory = inventory

    def add_to_waitlist(self, processid, units):
        self.waitlist.append((processid, units))

        return processid
