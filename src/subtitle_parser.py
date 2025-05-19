import math
import os
import re
import sys
from arguments import *

DEBUG = False

def main():
    
    try:
        args:Arguments = read_arguments(sys.argv[1:])
    except ValueError as e:
        print(e)
        print_usage()
        exit()

    path = args.path
    filename = args.filename
    shift_amount = args.shift_amount
    starting_block = args.starting_block
    ending_block = args.ending_block
    starting_phrase = args.starting_phrase

    seconds_to_shift = math.trunc(float(shift_amount))
    miliseconds_to_shift = int(round(float(shift_amount) - seconds_to_shift, 3) * 1000)

    print('Path: ', path)
    print('Filename: ', filename)
    print('Seconds to shift: ', seconds_to_shift)
    print('Miliseconds to shift: ', miliseconds_to_shift)
    print('Starting block: ', starting_block)
    print('Ending block: ', ending_block)
    print('Starting phrase: ', starting_phrase)


    if (not starting_block): # we need to search the file and find the actual starting line based on the starting phrase
        print('TODO!')


    extension = filename.split('.')[1]
    filename = filename.split('.')[0]

    original_filename = path + f'\\{filename}.{extension}'
    temp_filename = path + f'\\{filename}-tmp.{extension}'

    # open the subtitle file in read mode
    file = open(original_filename, "r")

    # create new file
    with open(temp_filename, 'w') as updated_file:

        current_block_lines = []
        last_subtitle_block_num = -1
        should_update = False

        for line in file:
            if not line.strip().isnumeric():
                process_line(line, seconds_to_shift, miliseconds_to_shift, current_block_lines, should_update)
            else:
                # write all the already-updated lines of the current block, if any
                if len(current_block_lines) > 0:
                    write_current_block(updated_file, current_block_lines)
                    if (DEBUG): print(f'Finished updating subtitle block #{last_subtitle_block_num}')
                    current_block_lines.clear()
                
                # get ready to start processing the next block...
                current_block_num = int(line.strip())
                should_update = current_block_num >= starting_block and current_block_num <= ending_block

                last_subtitle_block_num = current_block_num
                current_block_lines.append(line)
                if (DEBUG): print(f'Subtitle block #{current_block_num} will start to be updated')

        # at this point we will have the last block in the array, still not written, so we need to write it into the file
        write_current_block(updated_file, current_block_lines)

    # close the files
    file.close()
    updated_file.close()

    # remove the original file and rename the temp file to the original (workaround to avoid writing directly to the original, which may be messy)
    os.remove(original_filename)
    os.rename(temp_filename, original_filename)

def write_current_block(file, block_lines_array):
    for line in block_lines_array:
        file.write(line)

# checks whether the line 'line' is a timestamp line, and if so, updates the timestamps by shifting them 'seconds_to_shift_seconds'
# the updated line is added to the 'lines_array' array, ready to be written
# if the 'should_update' flag is tuerned off the line is not updated but just added without modifications
def process_line(line, int_seconds_to_shift, int_miliseconds_to_shift, lines_array, should_udpate):
    
    timestamp = re.search(r'(\d\d):(\d\d):(\d\d),(\d*) --> (\d\d):(\d\d):(\d\d),(\d*)', line)
    
    # if it's a timestamp line we update the corresponding values. otherwise, we just add the line as it is to be written
    if timestamp and should_udpate:

        from_timestamp = update_timestamp(timestamp.group(1), timestamp.group(2), timestamp.group(3), timestamp.group(4), int_seconds_to_shift, int_miliseconds_to_shift)
        to_timestamp = update_timestamp(timestamp.group(5), timestamp.group(6), timestamp.group(7), timestamp.group(8), int_seconds_to_shift, int_miliseconds_to_shift)

        updated_timestamp = f'{from_timestamp} --> {to_timestamp}'
        lines_array.append(updated_timestamp + '\n')
    else:
        lines_array.append(line)

# generates a shifted timestamp in SRT format
# 'hours:minutes:seconds,miliseconds' turns into: 'hours:minutes:seconds(+/-)seconds_to_shift,miliseconds(+/-)miliseconds_to_shift'
def update_timestamp(hours_str, minutes_str, seconds_str, miliseconds_str, seconds_to_shift, miliseconds_to_shift):

    minutes = int(minutes_str)
    seconds = int(seconds_str)
    miliseconds = int(miliseconds_str)

    updated_miliseconds = miliseconds + miliseconds_to_shift
    normalized_miliseconds = updated_miliseconds % 1000
    updated_seconds = seconds

    if updated_miliseconds < 0: # miliseconds were backward-wrapped, so we need to decrease the seconds
        if seconds > 0: updated_seconds-=1
    elif normalized_miliseconds != updated_miliseconds: # miliseconds were forward-wrapped, so we need to increase the seconds
        if seconds < 59: updated_seconds+=1

    updated_seconds = updated_seconds + seconds_to_shift
    normalized_seconds = updated_seconds % 60
    updated_minutes = minutes
    
    if updated_seconds < 0: # seconds were backward-wrapped, so we need to decrease the minutes
        if minutes > 0: updated_minutes-=1
    elif normalized_seconds != updated_seconds: # seconds were forward-wrapped, so we need to increase the minutes
        if minutes < 59: updated_minutes+=1

    # TODO: we should do the same for the minutes/hours in case it's a +1-hour-long subtitle file

    updated_minutes = "{:02}".format(updated_minutes)
    updated_seconds = "{:02}".format(normalized_seconds)
    updated_miliseconds = "{:03}".format(normalized_miliseconds)

    updated_timestamp = f'{hours_str}:{updated_minutes}:{updated_seconds},{updated_miliseconds}'

    return updated_timestamp

def print_tool_description():
    print('This tool is useful when subtitle files are shifted off with respect to the movie file, allowing to update the timestamps by a specified amount of seconds either backwards or forward')
    print('Currently supported subtitle formats: SRT (SubRip Subtitle file)\n')

def print_usage():
    print('USAGE: subtitle_parser.py absolute_path filename starting_line ending_line shift_amount')
    print('EXAMPLE: py .\\subtitle_parser.py "D:\\Downloads\\American Horror Story\\S02 - Asylum (2012)\\S02E01" "S02E01 (1080p).srt" 200 300 3.5\n')
    print('  - absolute_path: absolute path where the subtitle file to be updates is located in the file system')
    print('  - filename: subtitle file name including extension. The resulting modified subtitle file will be created in the same path with name filename-updated.ext')
    print('  - starting_block: number of the subtitle block from which timestamps will start being updated')
    print('  - ending_block: number of the subtitle block until which timestamps will end being updated')
    print('  - shift_amount: amount of seconds (using . for the decimal part if any) to shift the dialogs off (negative number: shift subtitles earlier/backwards, positive number: shift subtitles later/forward)')

# Using the special variable 
# __name__
if __name__=="__main__":
    main()