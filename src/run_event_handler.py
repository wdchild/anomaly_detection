#!/Users/danielchild/anaconda/bin/python3

from event_handler import *
from person import *
import time
import os

print()
cwd = os.getcwd()
print('CURRENT WORKING: {}'.format(cwd))
current = os.path.dirname(__file__)
print('CURRENT DIRECTORY: {}'.format(current))

tic = time.clock() # not the best way but works in a pinch

# PATHS IF USING RELATIVE PYTHON FROM TERMINAL
# batch_file_loc = 'log_input/batch_log.json' # provided by INSIGHT
# stream_file_loc = 'log_input/stream_log.json'
# flagged_file_loc = 'log_output/flagged_log.json' 

# NOTE I RECOMMEND USING OTHER FILES (SMALLER) FOR QUICKER TESTING 
batch_file_loc = os.path.join(current, '../log_input/batch_log.json') # provided by INSIGHT
stream_file_loc = os.path.join(current, '../log_input/stream_log.json') # provided by INSIGHT
flagged_file_loc = os.path.join(current, '../log_output/flagged_purchases.json') # as specified

print()
print('REL BATCH FILE: {}'.format(batch_file_loc))
print('REL STREAM FILE: {}'.format(stream_file_loc))
print('REL FLAGGED FILE: {}'.format(flagged_file_loc))

# filename = os.path.join(fileDir, '../Folder2/same.txt')
# filename = os.path.abspath(os.path.realpath(filename))

batch_file_loc = os.path.abspath(os.path.realpath(batch_file_loc))
stream_file_loc = os.path.abspath(os.path.realpath(stream_file_loc))
flagged_file_loc = os.path.abspath(os.path.realpath(flagged_file_loc))

print()
print('ABS BATCH: {}'.format(batch_file_loc))
print('ABS STREAM: {}'.format(stream_file_loc))
print('ABS FLAGGED: {}'.format(flagged_file_loc))
print()

# INITIATE THE EVENT HANDLER FOR PROCESSING DATA
# (This is not a real GUI event handler, just literally an object to handle data of
# various types found in the batch_log and stream_log.
handler = EventHandler(batch_file_loc, stream_file_loc, flagged_file_loc)

# PROCESS THE BATCH DATA
handler.processBatchData(batch_file_loc)

# PROCESS THE STREAM DATA
# Note, this should be put in a different python script if you were
# doing this in in a real application.
handler.processStreamData(stream_file_loc)

# SEE HOW LONG IT TOOK
toc = time.clock()
elapsed = toc - tic
print('Time elapsed to process batch and stream {}'.format(round(elapsed, 5)))
