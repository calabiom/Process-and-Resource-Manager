## Mark Calabio
## 12488362

## manager.py - Implementation of the manager

from process import Process
from resource import Resource
from collections import deque

class Manager():

    def __init__(self):
        self.PCB = [None] * 16      
        self.RCB = [None] * 4       ## List of tuple objects (Resource, units)
        self.ready_list = deque()

        self.rl ={0: deque(), 1: deque(), 2: deque()}
        self.active_processes = 0  ## to cache how many process are there

        self.run_proc = None

        ## When we extend the manager features, self.ready_list will be
        ## dict of lists/queue of prioritized processes (k: Priority #, v: Deque)
        
        ## Head of the list of ready processes is always the running process!
        
    ## When it comes to deletion of process in the PCB, simple remove the value
    ## at that index and mark it as None. Then when creating a process, add that
    ## process to the lowest indexed empty cell.

        
    def initialize(self):
        '''Restore system to its initial state and create Process 0'''
        self.PCB = [None] * 16
        self.RCB = [None] * 4
        self.ready_list = deque() 
        self.rl = {0: deque(), 1: deque(), 2: deque()} #### WHERE YOU LAST LEFT OFF 10.28.19 5:20 AM

        ## Creating Process 0 and placing it into Ready List
        self.PCB[0] = Process(0, 1, 0)  ## Process(id/index, state, parent)

        self.active_processes += 1

        self.ready_list.append(self.PCB[0].id)
        self.run_proc = self.PCB[self.ready_list[0]]

        ## Set up all Resources
        self.RCB[0] = Resource(0, 1, 0)
        self.RCB[1] = Resource(1, 1, 0)
        self.RCB[2] = Resource(2, 2, 0)
        self.RCB[3] = Resource(3, 3, 0)
        return 0

    def create(self, priority): ## Priority to be used later
        '''Creates a new process for the current Process by invoking Process.create()

            Responsibilities:
                - put new Process in self.PCB
                - append to ready list
        '''
        index = 0
        for p in range(0,len(self.PCB)):
            if self.PCB[p] == None:
                new_process = self.run_proc.create_process(index)

                self.PCB[p] = new_process

                self.ready_list.append(index)

                self.run_proc.add_child(index)
                
                print("Process ", index, " created from ", self.run_proc.id) #, " {}".format(list(self.ready_list)))
                ##print(self.PCB)
                print(list(self.ready_list))
                self.active_processes += 1
                return index

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
            while index in wl:
                print(wl)
                self.RCB[i].waitlist.remove(index)
                wl = self.RCB[i].waitlist.copy()

        ## Remove any reference to the deleted process from
        ##      - Process.resources
        ##  Then, update the Resource waitlist, and if there is a Process
        ##  up next, then update that Process.resource
        resource_cpy = self.PCB[index].resources.copy()
        for r in resource_cpy:
            self.PCB[index].resources.remove(r)

            if not self.RCB[r].waitlist: ## empty
                self.RCB[r].state = 0
            else:
                head_of_waitlist = self.RCB[r].waitlist.popleft()
                print("HEY LOOK OVER HERE MARK CALABIO: ", head_of_waitlist)
                #print("head ", head_of_waitlist)
                print("is h in pcb?: ", head_of_waitlist in [p.id if p != None else -1 for p in self.PCB])
                try:
                    if head_of_waitlist in [p.id if p != None else -1 for p in self.PCB]:
                        self.PCB[head_of_waitlist].state = 1
                        #print("b: ", self.ready_list)
                        self.ready_list.append(head_of_waitlist)
                        #print("a: ", self.ready_list)
                        #print(resource)
                        self.PCB[head_of_waitlist].resources.append(r)
                except:
                    pass
            print("Resource {} released".format(r))

        try:
            #print(self.ready_list)
            #print("about to remove {}".format(index))
            self.ready_list.remove(index)
        except:
            print("{} not in ready_list".format(index))
            
        self.PCB[parent_id].children.remove(index)

        #print("Destroyed: ", self.PCB[index])
        self.PCB[index] = None

        print("After removing {}: ".format(index), " ", list(self.ready_list))
        display_PCB = [1 if i != None else 0 for i in self.PCB]
        print(display_PCB)

        self.active_processes -= 1
        return resources_to_release

        

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

            resources_to_release = self.handle_destruction(index)

            difference = number_before - self.active_processes

            print("{} processes destroyed".format(difference))

        else:
            print("Deletion REJECTED")

        
        # print("Manager: Process killed their children, and their own children. fuck")
        return True

#################################
#################################

    def request(self, resource, units):
        if resource not in [0, 1, 2, 3]: return -1

        if self.run_proc.id == self.PCB[0].id: return -1 ## Process 0 can't req res.

        ## if the current process holds ALL the units of a resource they're
        ## requesting, then return -1 ----> TB IMPLEMENTED LATER
        
        if self.RCB[resource].state == 0:   ## if resource is free rn... 
            self.RCB[resource].state = 1    ## RESOURCE ALLOCATED
            self.run_proc.add_resource(resource)
            print("Resource r allocated")
            self.print_resource_usage()
        else:                               ## if resource is already allocated (1)
            self.run_proc.state = 0         ## PROCESS BLOCKED
            blocked_process = self.ready_list.popleft()
            self.RCB[resource].add_to_waitlist(blocked_process)
            print("Process {} blocked, waiting on resource".format(self.run_proc.id))

            waitlist = [list(i.waitlist) for i in self.RCB]
            print("Resources waitlist: ", waitlist)

            self.scheduler()
        ##print("Manager: I REQUEST MORE RESOURCES")
        return True

    def release(self, resource, units):
        if resource in self.run_proc.resources:
            self.run_proc.resources.remove(resource)

            if not self.RCB[resource].waitlist: ## empty
                self.RCB[resource].state = 0
            else:
                head_of_waitlist = self.RCB[resource].waitlist.popleft()
                try: ## in the event that the process doesn't exist
                    if head_of_waitlist in [p.id if p != None else -1 for p in self.PCB]:
                        self.PCB[head_of_waitlist].state = 1
                        self.ready_list.append(head_of_waitlist)
                        self.PCB[head_of_waitlist].resources.append(resource)
                except:
                    pass
            print("Resource {} released".format(resource))
            self.resource_status()
            return True
                
        #print("Manager: I RELEASE RESOURCES")
        print("Resource {} is not used by this process".format(resource))
        return True

    def timeout(self):
        index_to_bring_to_end = self.ready_list.popleft()
        self.ready_list.append(index_to_bring_to_end)

        self.PCB[index_to_bring_to_end].status = 1

        self.scheduler()
      
        # print("Manager: TIME OUT")
        return True

    def scheduler(self):
        self.run_proc = self.PCB[self.ready_list[0]]
        print("Process {} running: ".format(self.run_proc.id))
        print(list(self.ready_list))

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
        display_RCB = ["FREE" if i.state == 0 else "ALLOC" for i in self.RCB]
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
