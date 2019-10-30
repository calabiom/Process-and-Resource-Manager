## Mark Calabio
## 12488362

## manager.py - Implementation of the manager

from process import Process
from resource import Resource
from collections import deque

VALID_PRIORITIES = [0,1,2]

class NewManager():

    def __init__(self):
        self.PCB = [None] * 16      
        self.RCB = [None] * 4       ## List of tuple objects (Resource, units)
        #self.ready_list = deque()

        self.ready_list ={0: deque(), 1: deque(), 2: deque()}
        self.active_processes = 0  ## to cache how many process are there

        self.run_proc = None

        ## When we extend the manager features, self.ready_list will be
        ## dict of lists/queue of prioritized processes (k: Priority #, v: Deque)
        
        ## Head of the list of ready processes is always the running process!
        
    ## When it comes to deletion of process in the PCB, simple remove the value
    ## at that index and mark it as None. Then when creating a process, add that
    ## process to the lowest indexed empty cell.

        
    def initialize(self):
        ''' Restore system to its initial state and create Process 0
            Returns process 0
        '''
        self.PCB = [None] * 16
        self.RCB = [None] * 4
        #self.ready_list = deque() 
        self.ready_list = {2: deque(), 1: deque(), 0: deque()} #### WHERE YOU LAST LEFT OFF 10.28.19 5:20 AM

        ## Creating Process 0 and placing it into Ready List
        self.PCB[0] = Process(0, 0, 1, 0)  ## Process(id/index, state, parent)

        self.active_processes += 1

        self.ready_list[0].append(self.PCB[0].id)
        self.run_proc = self.PCB[self.ready_list[0][0]]
        #print(self.run_proc.id)

        ## Set up all Resources
        self.RCB[0] = Resource(0, 1)
        self.RCB[1] = Resource(1, 1)
        self.RCB[2] = Resource(2, 2)
        self.RCB[3] = Resource(3, 3)
        return 0

    def create(self, priority): ## Priority to be used later
        '''Creates a new process for the current Process by invoking Process.create()

            Responsibilities:
                - put new Process in self.PCB
                - append to ready list

            Returns the parent process that created the new process
        '''
        if priority not in VALID_PRIORITIES:
            print("ERROR: Invalid Priority #")
            return -1 #### Incorrect priority #
        
        index = 0
        for p in range(0,len(self.PCB)):
            if self.PCB[p] == None:
                new_process = Process(index, priority, 1, self.run_proc.id) ######### ADD PRIORITY AS AN ARGUMENT #########

                self.PCB[p] = new_process

                self.ready_list[priority].append(index)

                self.run_proc.add_child(index)
                
                print("Process ", index, " created from ", self.run_proc.id) #, " {}".format(list(self.ready_list)))
                #print(self.PCB)
                print(self.ready_list)

                self.active_processes += 1

                if priority > self.run_proc.priority:
                    #print("ok")
                    self.scheduler()
                return self.run_proc.id # index

            index = index + 1

        return -1 ## Error: no more processes can be created
                
        # print("Manager: Process created their own childprocess, ew")
        

    def handle_destruction(self, index):
        ''' Remove child and child's child, recursively
        '''
        resources_to_release = []
        children = self.PCB[index].children.copy()
        parent_id = self.PCB[index].parent
        
        for child in children:
            print(child)
            resources_to_release = self.handle_destruction(child)

        ## Remove any reference to the deleted process from the Resource waitlist
        for i, r in enumerate(self.RCB):
            print(self.RCB[i].id)
            print(self.RCB[i].waitlist)
            wl = self.RCB[i].waitlist.copy()
            for pair in wl:
                if index == pair[0]:
                    self.RCB[i].waitlist.remove(pair)

        ## Remove any reference to the deleted process from
        ##      - Process.resources
        ##  Then, update the Resource waitlist, and if there is a Process
        ##  up next, then update that Process.resource
        resource_cpy = self.PCB[index].resources.copy()
        for r_index in resource_cpy:
            units_to_give = 0
            if r_index in self.PCB[index].resources:
                units_to_give += self.PCB[index].resources[r_index]
            else:
                continue
            
            self.PCB[index].resources.pop(r_index, None)

            self.RCB[r_index].state += units_to_give
            
            print(self.RCB[r_index].state)

            r = self.RCB[r_index]
            wl_cpy = r.waitlist.copy()
            while (wl_cpy and r.state > 0):
                wl_head = r.waitlist[0]
                print(wl_head)
                if (r.state >= wl_head[1]):
                    r.state = r.state - wl_head[1]
                    self.PCB[wl_head[0]].add_resource(r.id, wl_head[1])
                    self.PCB[wl_head[0]].state = 1
                    proc_ready = r.waitlist.popleft()
                    self.ready_list[self.PCB[proc_ready[0]].priority].append(proc_ready[0])
                    wl_cpy = r.waitlist.copy()

                else:
                    break
                    
            #self.scheduler()
            print("Resource {} released".format(r_index))
        try:
            #print(self.ready_list)
            #print("about to remove {}".format(index))
            self.ready_list[self.PCB[index].priority].remove(index)
        except:
            print("{} not in ready_list".format(index))
            
        self.PCB[parent_id].children.remove(index)

        #print("Destroyed: ", self.PCB[index])
        self.PCB[index] = None

        print("After removing {}: ".format(index), " ", self.ready_list)
        display_PCB = [1 if i != None else 0 for i in self.PCB]
        print(display_PCB)

        self.active_processes -= 1
        
        result = self.scheduler()
        return result

        

    def destroy(self, index):
        '''Destroy THAT child process, and recursively destroy child's descendants, etc.'''

        ## destroyed_processes = []     ## keep track of what's deleted so that way we can
                                        ## delete stuff from readylist properly
        ## has to be direct child
        ## can't destroy itself or Process 0
        print(self.run_proc.children)

        if index in self.run_proc.children and index != 0 and index != self.run_proc.id:
            print("Deletion APPROVED")

            number_before = self.active_processes

            result = self.handle_destruction(index)

            difference = number_before - self.active_processes

            print("{} processes destroyed".format(difference))

        else:
            print("Deletion REJECTED")

        
        # print("Manager: Process killed their children, and their own children. fuck")
        return result

#################################
#################################

    def request(self, resource, units):
        ''' Running process can request a resource with specific # of units

            Returns the process that requested the resource
            Returns -1 for any errors
        '''
        if resource not in [0, 1, 2, 3] or units == 0:
            print("ERROR: Invalid resource referenced or requested 0 units")
            return -1

        if self.run_proc.id == self.PCB[0].id:
            print("ERROR: Process 0 can't request resources")
            return -1 ## Process 0 can't req res.

        ## If this process is requesting a resource it's already holding...
        
        proc_resources = self.PCB[self.run_proc.id].resources
        if resource in proc_resources:
            if units + proc_resources[resource] > self.RCB[resource].inventory:
                print("Requesting too much of a resource you're holding")
                print(self.PCB[self.run_proc.id].resources)
                return -1
            else:
                self.run_proc.add_resource(resource, units)
                self.RCB[resource].state -= units
            return self.run_proc.id

        if units > self.RCB[resource].inventory:
            print("ERROR: # of units requested is beyond resource inventory")
            return -1

        ## If this process is requesting a resource it's NOT holding...
        ## ..and the resource is being used by (even partly) by another process

        if (self.RCB[resource].state >= units):
            self.run_proc.state = 1
            self.RCB[resource].state -= units
            self.run_proc.add_resource(resource, units)
        else:
            self.run_proc.state = 0
            blocked_proc = self.ready_list[self.run_proc.priority].popleft()
            self.RCB[resource].add_to_waitlist(blocked_proc, units)
            print("Process {} blocked, waiting on resource".format(self.run_proc.id))

            waitlist = [list(i.waitlist) for i in self.RCB]
            print("Resources waitlist: ", waitlist)
            self.scheduler()
            return self.run_proc.id
            #return resource
        return self.run_proc.id

    def release(self, resource, units):
        if resource in self.run_proc.resources:
            if self.run_proc.resources[resource] < units:
                print("ERROR: Attempted to release more units than what the process is actually holding")
                return -1

            self.run_proc.resources[resource] -= units
            
            if self.run_proc.resources[resource] == 0:
                self.run_proc.resources.pop(resource, None)

            self.RCB[resource].state += units
            print(self.RCB[resource].state)

            r = self.RCB[resource]
            wl_cpy = r.waitlist.copy()
            while (wl_cpy and r.state > 0):
                wl_head = r.waitlist[0]
                print(wl_head)
                if (r.state >= wl_head[1]):
                    r.state = r.state - wl_head[1]
                    self.PCB[wl_head[0]].add_resource(r.id, wl_head[1])
                    self.PCB[wl_head[0]].state = 1
                    proc_ready = r.waitlist.popleft()
                    self.ready_list[self.PCB[proc_ready[0]].priority].append(proc_ready[0])
                    wl_cpy = r.waitlist.copy()
                else:
                    break
                    
            self.scheduler()
            print("Resource {} released".format(resource))
            self.resource_status()
            return self.run_proc.id
                    

        return -1

##            ## restore units back to resource inventory
##
##            if not self.RCB[resource].waitlist: ## empty
##                self.RCB[resource].state = 0
##            else:
##
####                ## FIND the highest-priority process that matches the units available for the resource
####
####                ## what happens when you release a resource but every process on the waitlist
####                ## requests units higher than what's available?? is it marked as alloc?? 
####
####                # highest_proc = self.RCB[resource].waitlist.copy().popleft()
####                # for p in self.RCB[resource].waitlist:                         # p will be a tuple!!!!!
####                #       if self.PCB[p].priority > self.PCB[highest_proc].priority and p[1] == units:
####                #           highest_proc = p
####
####                # we have to check if the high-priority process is on another waitlist
####                # or later in line on the same waitlist
####
####                ## OR: CAN a process only be at max 1 waitlist bc it'll be blcoked and not on the RL???
####    
####
####                wl_copy = self.RCB[resource].waitlist.copy()
####                # for p in wl_copy:
####                #   if p = highest_proc:
####                #       self.RCB[resource].waitlist.re
####                #       break
##
##                # Priority plays no role for the resource waiting list. All processes should be handled in FIFO order.
##                
##                head_of_waitlist = self.RCB[resource].waitlist.popleft()
##                try: ## in the event that the process doesn't exist
##                    if head_of_waitlist in [p.id if p != None else -1 for p in self.PCB]:
##                        self.PCB[head_of_waitlist].state = 1
##                        self.ready_list.append(head_of_waitlist)
##                        self.PCB[head_of_waitlist].resources.append(resource)
##                        ## self.scheduler()
##                        
##                except:
##                    pass
##            print("Resource {} released".format(resource))
##            self.resource_status()
##            return True
##                
##        #print("Manager: I RELEASE RESOURCES")
##        print("Resource {} is not used by this process".format(resource))
##        return True

    def timeout(self):
        ''' Running process can request a resource with specific # of units

            Returns the new running process 
        '''
        index_to_bring_to_end = self.ready_list[self.run_proc.priority].popleft()
        self.ready_list[self.run_proc.priority].append(index_to_bring_to_end)

        self.PCB[index_to_bring_to_end].state = 1

        self.scheduler()
      
        # print("Manager: TIME OUT")
        return self.run_proc.id

    def scheduler(self):
        ##
        ## for i,p in self.rl:
        ##      if self.rl[i] not empty:
        ##          new_proc = self.rl[i][0]
        ##          break

        ## self.run_proc = self.PCB[new_proc]

        new_proc = None
        sorted(self.ready_list, reverse = True)
        for priority, ready_proc in self.ready_list.items():
            print(ready_proc)
            if self.ready_list[priority]:
                new_proc = self.ready_list[priority][0]
                print("here with ", new_proc)
                break

        self.run_proc = self.PCB[new_proc]
        
        print("Process {} running: ".format(self.run_proc.id))
        print(self.ready_list)
        return self.run_proc.id

#################################
#################################

    def sayHi(self):
        print("Manager: Hello there")

    def see_children(self):
        print(self.run_proc.children)

    def process_status(self):
        print()
        print("Running Process {}, Parent of {}".format(self.run_proc.id, self.run_proc.parent))
        #print(self.PCB)
        #print(self.RCB)
        print("Ready list: ", self.ready_list)
        display_PCB = [1 if i != None else 0 for i in self.PCB]
        print("All Processes: ", display_PCB)
        print("Parents and Children:")
        for i, idx in enumerate(display_PCB):
            if idx == 1:
                to = "{}: {}".format(i, self.PCB[i].children)
                print(to)

    def resource_status(self):
        print("Resources used by Process {}: ".format(self.run_proc.id), self.run_proc.resources)
        display_RCB = [i.state for i in self.RCB]
        print("Resources Status: ", display_RCB)
        waitlist = [list(i.waitlist) for i in self.RCB]
        print("Resources waitlist: ", waitlist)
        self.print_resource_usage()

    def print_resource_usage(self):
        display_PCB = [1 if i != None else 0 for i in self.PCB]
        print("Resource Usage (Process: Resource):")
        for i, idx in enumerate(display_PCB):
            if idx == 1:
                to = "{}: {}".format(i, self.PCB[i].resources)
                print(to)

                
    def status(self):
        self.process_status()
        print()
        self.resource_status()
