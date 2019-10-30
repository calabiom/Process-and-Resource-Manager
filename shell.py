## Mark Calabio
## 12488362

## shell.py - Handling of shell input commands and shell interface

## The following commands will be used in the test files for this project:
##      - in
##          - Restore the system to its initial state.
##
##	- cr <p>
##          - Invoke function create(), which creates a new process at the priority level <p>; 
##            <p> can be 1 or 2 (0 is reserved for init process)
##
##	- de <i>
##          - Invoke the function destroy(), which destroy the process identified by the PCB index <i>, and all of its descendants
##
##	- rq <r> <n>
##          - Invoke the function request(), which requests <n> units of resource <r>; 
##            <r> can be 0, 1, 2, or 3; n=1 for <r>=0 and <r>=1, <n>=2 for <r>=2, and <n>=3 for <r>=3.
##
##	- rl <r> <n>
##          - Invoke the function release(), which release the resource <r>;
##            <r> can be 0, 1, 2, or 3; <n> gives the number of units to be released
##
##      - to
##          - Invoke the function timeout().

from nmanager import NewManager

VALID_COMMANDS = ["in","cr","de","rq","rl","to"]
VALID_RESOURCES = [i for i in range(0, 4)]
    
def shell():

    manager = NewManager() ## Instantiate Manager object

    ## Manager object handles their own ecosystem of processes and resources
    ## It will create processes and allocate resources accordingly
    
    manager.sayHi()

    f = open("official_test.txt", "r")

    fl = f.readlines()

    result = []
    for command in fl:
    #while True:   
        print(command)
        #print()
        #command = input()

        #print(command)
        
        isValid, feedback = _is_command_valid(command)
        
        if isValid:
            pass
        else:
            print("Error: ", feedback)
            continue

        ## print("\nProgress")

        ## We are assuming that at this point, the input is valid
        ## (only thing left to check is the validity of argumentss -- to be checked by individual functions)

        split_command = command.split()
        main_command = split_command[0]

        index = None

        ## print(split_command[1:])

        if main_command == "in":
            index = manager.initialize()
        
        if main_command == "cr":
            priority = int(split_command[1:][0])
            
            index = manager.create(priority)

        if main_command == "de":
            index_to_destroy = int(split_command[1:][0])

            index = manager.destroy(index_to_destroy)

        if main_command == "rq":
            resource_to_request = int(split_command[1:][0])
            units = int(split_command[1:][1])

            #print(units)

            index = manager.request(resource_to_request, units)

        if main_command == "rl":
            resource_to_release = int(split_command[1:][0])
            units = int(split_command[1:][1])

            index = manager.release(resource_to_release, units)

        if main_command == "to":
            
            index = manager.timeout()

        ######
        if main_command == "child":
            manager.see_children()

        if main_command == "stat":
            manager.status()

        ## write index to output file
        
        print("write this to output file: ", index)
        result.append(index)

    print(result)        


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
        
def _is_command_valid(cmd_as_input):
    '''Verify if command is acceptable and if the arguments are the right # and type'''

    split_cmd_list = cmd_as_input.split()

    if not split_cmd_list: return (False, "Empty")

    command = split_cmd_list[0]
    parameters = split_cmd_list[1:]
    len_scl = len(split_cmd_list)
    
    # print("From _is_command_valid: ",split_cmd_list)

    message = ""

    # Check if length of the command (in general) doesn't match expected input
    if len_scl == 0 or len_scl > 3:
        return (False, "Invalid command or input must be 1 - 3 words.")

    # Check for "in" and "to" cmd
    if command in ["in","to", "child", "stat"] and len_scl == 1: 
        return (True, "Success")

    message = "Invalid command or # of arguments is wrong."
        
    # Check for "cr" and "de" cmd
    if command in ["cr","de"] and len_scl == 2:

        if parameters[0].isdigit():
            return (True, "Success")
        else:
            message = "Invalid command (cr or de). Argument should be int."

    # Check for "cr" and "de" cmd
    if command in ["rq","rl"] and len_scl == 3:
        #print("cmd: rq or rl")
        if parameters[0].isdigit() and parameters[1].isdigit():
            if int(parameters[0]) >= 0 and int(parameters[0]) < 4:
                return (True, "Success")
            else:
                message = "Invalid resource reference"
        else:
            message = "Invalid command (rq or rl). Both arguments should be int."

    return (False, message) ## meaning either the wrong command was called, or the right cmd was called but had invalid parameters


shell()
