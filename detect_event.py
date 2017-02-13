import time
import inotify.adapters

sensor_data_node_1 = "/home/pi/sensor_node/output/sensor_node_data.txt"
sensor_data_node_2 = "/home/pi/sensor_node/sensor_node2_output_mount/sensor_node_data.txt"

detect = inotify.adapters.Inotify()

detect.add_watch(sensor_data_node_1)
detect.add_watch(sensor_data_node_2)

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
data_sets_node_1 = []
data_sets_node_2 = []


#Node 1
initial_lastline_node_1 = lastline(sensor_data_node_1)
initial_last_data_set_node_1 =  initial_lastline_node_1.split(',')
data_sets_node_1.append(initial_last_data_set_node_1)

#Node 2
initial_lastline_node_2 = lastline(sensor_data_node_2)
initial_last_data_set_node_2 =  initial_lastline_node_2.split(',')
data_sets_node_2.append(initial_last_data_set_node_2)

print("Start detection")

for event in detect.event_gen():
    if event is not None:
	current_lastline_node_1 = lastline(sensor_data_node_1)
	current_last_data_set_node_1 = current_lastline_node_1.split(',')
	current_lastline_node_2 = lastline(sensor_data_node_2)
        current_last_data_set_node_2 = current_lastline_node_2.split(',')


	if(current_last_data_set_node_1[0] != data_sets_node_1[-1][0]):
		data_sets_node_1.append(current_last_data_set_node_1)
		print(current_last_data_set_node_1[0]+","+current_last_data_set_node_1[2].rstrip('\n')+","+current_last_data_set_node_1[1]+",node1")	

	if(current_last_data_set_node_2[0] != data_sets_node_2[-1][0]):
                data_sets_node_2.append(current_last_data_set_node_2)
                print(current_last_data_set_node_2[0]+","+current_last_data_set_node_2[2].rstrip('\n')+","+current_last_data_set_node_2[1]+",node2") 

	
