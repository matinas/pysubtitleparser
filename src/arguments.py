import sys
from dataclasses import dataclass

start_flag = '--start'
end_flag = '--end'
start_phrase_flag = '--startphrase'

@dataclass
class Arguments:
    path: str
    filename: str
    shift_amount: float
    starting_block: int
    ending_block: int
    starting_phrase: str

def read_arguments(argsList):
    
    if len(argsList) < 3:
        raise ValueError("Not enough arguments. Please check usage") 

    path = argsList[0]
    filename = argsList[1]
    shift_amount = float(argsList[2])
    starting_block = None
    ending_block = None
    starting_phrase = None

    flag_args = argsList[3:]

    if is_flag_present(flag_args, start_flag):
        try:
            starting_block = int(get_flag_argument_value(flag_args, start_flag))
            print(f'Starting value {starting_block} was found and will be used as starting line')
        except:
            raise ValueError("Error trying to read starting block value")
    elif is_flag_present(flag_args, start_phrase_flag): # there's no starting block, so we check for a starting phrase, if any
        try:
            starting_phrase = get_flag_argument_value(flag_args, start_phrase_flag)
            print(f'Starting phrase \'{starting_block}\' was found and will be used to find the starting line')
        except:
            raise ValueError("Error trying to read starting phrase value")
    else:
        print(f'There\'s no starting value so it will be set to the default value (i.e.: first line)')
        starting_block = 1

    # done reading starting value at this point, so we check for an optional ending block value
    if is_flag_present(flag_args, end_flag):
        try:
            ending_block = int(get_flag_argument_value(flag_args, end_flag))
            print(f'Ending value {ending_block} was found and will be used as ending line')
        except:
            raise ValueError("Error trying to read ending block value")
    else:
        print(f'There\'s no ending value so it will be set to the default value (i.e.: last line)')
        ending_block = sys.maxsize

    return Arguments(path, filename, shift_amount, starting_block, ending_block, starting_phrase)

def is_flag_present(flag_args, flag):
    try:
        flag_args.index(flag)
        return True
    except:
        return False

def get_flag_argument_value(flag_args, flag):

    arg = None
    index = flag_args.index(flag)
    arg = flag_args[index+1]
    
    return arg