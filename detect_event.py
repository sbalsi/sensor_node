import time
import inotify.adapters

sensor_data_node_1 = "sensor_node_data.txt"

detect = inotify.adapters.Inotify()

detect.add_watch(sensor_data_node_1)

#################################################################
#Functions
#################################################################
def lastline(data_file):
        with open(data_file, "rb") as f:
                f.seek(-2, 2)             # Jump to the second last byte.
                while f.read(1) != b"\n": # Until EOL is found...
                        f.seek(-2, 1)         # ...jump back the read byte plus one more.
                last = f.readline()       # Read last line.

        return last
#################################################################
#Main
#################################################################i
data_sets =[]

initial_lastline = lastline(sensor_data_node_1)
initial_last_data_set =  initial_lastline.split(',')

data_sets.append(initial_last_data_set)

print("Start detection")

for event in detect.event_gen():
    if event is not None:
	current_lastline = lastline(sensor_data_node_1)
	current_last_data_set = current_lastline.split(',')
	if(current_last_data_set[1] != data_sets[-1][1]):
		data_sets.append(current_last_data_set)
		print(current_last_data_set[1])	
	
