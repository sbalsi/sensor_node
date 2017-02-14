import time
import inotify.adapters

#IO
sensor_data_node_1 = "/home/pi/sensor_node/output/sensor_node_data.txt"
sensor_data_node_2 = "/home/pi/sensor_node/sensor_node2_output_mount/sensor_node_data.txt"
#detect_data_output_file = "/home/pi/sensor_node/output/detect_data_output.txt"  
detect_events_output_file = "/home/pi/sensor_node/output/detect_events_output.txt"

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

def time_to_epoch(date_time):
    pattern = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return epoch

def epoch_to_time(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch+3600))
#################################################################
#Main
#################################################################i
data_sets_node_1 = []
data_sets_node_2 = []
data_set_count_node_1 = 0
data_set_count_node_2 = 0
data_set_count = 3 #Number of data sets for event detection

current_time = ""
event_detected_node_1_ts_tmp = 0 #Timestamp for last detected event
event_detected_node_1_ts_wind = 0 
event_detected_node_2_ts_tmp = 0
event_detected_node_2_ts_wind = 0
event_detected_node_1_count_tmp = 0
event_detected_node_1_count_wind = 0
event_detected_node_2_count_tmp = 0
event_detected_node_2_count_wind = 0

#Detection parameters
detection_timeout_tmp = 120 #Timeout after detection. During this timeout no other event will be detected
detection_timeout_wind = 60
tmp_delta = 3.0 #Value in Celsius at which delta is evaluated as an event
wind_delta = 5.0 #Value in MPH at which delta is evaluated as an event

#Node 1
initial_lastline_node_1 = lastline(sensor_data_node_1)
initial_last_data_set_node_1 =  initial_lastline_node_1.split(',')
data_sets_node_1.append(initial_last_data_set_node_1)

#Node 2
initial_lastline_node_2 = lastline(sensor_data_node_2)
initial_last_data_set_node_2 =  initial_lastline_node_2.split(',')
data_sets_node_2.append(initial_last_data_set_node_2)

print("-------- Start detection -------")

for event in detect.event_gen():
    if event is not None:
	current_lastline_node_1 = lastline(sensor_data_node_1)

#	detect_data_output_fh = open(detect_data_output_file,"a+")
#	detect_data_output_fh.write(current_lastline_node_1)
#	detect_data_output_fh.close()

	current_last_data_set_node_1 = current_lastline_node_1.split(',')
	current_lastline_node_2 = lastline(sensor_data_node_2)
        current_last_data_set_node_2 = current_lastline_node_2.split(',')


	if(current_last_data_set_node_1[0] != data_sets_node_1[-1][0]):
		data_sets_node_1.append(current_last_data_set_node_1)
		data_set_count_node_1 = data_set_count_node_1 + 1
		print(current_last_data_set_node_1[0]+","+current_last_data_set_node_1[2].rstrip('\n')+","+current_last_data_set_node_1[1]+",node1")

	if(current_last_data_set_node_2[0] != data_sets_node_2[-1][0]):
                data_sets_node_2.append(current_last_data_set_node_2)
		data_set_count_node_2 = data_set_count_node_2 + 1
                print(current_last_data_set_node_2[0]+","+current_last_data_set_node_2[2].rstrip('\n')+","+current_last_data_set_node_2[1]+",node2") 

	
	#Data evaluation
	if(data_set_count_node_1 >= data_set_count and data_set_count_node_2 >= data_set_count):
		data_set_count_node_1 = 0
		data_set_count_node_2 = 0
		event_detected = 0 #1 for event @ node 1; 2 for event @ node 2
		print "-------- Node 1: Start data set evaluation --------"
		
		#Evaluate data sets from node 1
		print("Node1 - Delta of: " +str(data_sets_node_1[data_set_count-1][0])+" " + str(data_sets_node_1[data_set_count-1][2]).rstrip('\n')+ " and " +str(data_sets_node_1[-1][0]).rstrip('\n')+" " + str(data_sets_node_1[-1][2]).rstrip('\n'))
		print("Node1 - Temp Delta: "+str(abs(float(data_sets_node_1[data_set_count-1][2])-float(data_sets_node_1[-1][2]))))
		print("-------- Node 1: End data set evaluation ---------")		
		print("\n\n")
		
		if(abs(float(data_sets_node_1[data_set_count-1][2])-float(data_sets_node_1[-1][2]))  >= tmp_delta ):
			current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
			print("####### Event on Node 1 detected "+str(data_sets_node_1[-1][0]) +"#######")
			print("Last event at node 1 detected at: " + str(event_detected_node_1_ts))
			print("Delta of detected events on node 1 :"+data_sets_node_1[-1][0]-event_detected_node_1_ts)
			event_detected_node_1_ts = data_sets_node_1[-1][0]

		#Evaluate data sets from node 2
		print "-------- Node 2: Start data set evaluation --------"
		print("Node2 - Delta of: " +str(data_sets_node_2[data_set_count-1][0])+" " +str(data_sets_node_2[data_set_count-1][2]).rstrip('\n')+ " and " +str(data_sets_node_2[-1][0])+" " + str(data_sets_node_2[-1][2]).rstrip('\n'))
                print("Node2 - Temp Delta: "+str(abs(float(data_sets_node_2[data_set_count-1][2])-float(data_sets_node_2[-1][2]))))
		print("-------- Node 2: End data set evaluation ---------")
		print("\n\n")
		
		#Event detected because of temperature change greater than tmp_delta or wind wind change greater than wind_delta
                if(abs(float(data_sets_node_2[0][2])-float(data_sets_node_2[len(data_sets_node_2)-1][2])) >= tmp_delta or abs(float(data_sets_node_2[0][1])-float(data_sets_node_2[len(data_sets_node_2)-1][1])) >= wind_delta):
			#Temperature event
			if(abs(float(data_sets_node_2[0][2])-float(data_sets_node_2[len(data_sets_node_2)-1][2])) >= tmp_delta):
				if(event_detected_node_2_count_tmp == 0):
                        		print("First temperature change at node 2 detected since start of detection: "+str(data_sets_node_2[-1][0]))
					detect_events_output_fh = open(detect_events_output_file,"a+")
					detect_events_output_fh.write(str(data_sets_node_2[-1][0])+",tmp,"+str(abs(float(data_sets_node_2[0][2])-float(data_sets_node_2[len(data_sets_node_2)-1][2]))))
					detect_events_output_fh.close()		
                        		event_detected_node_2_count_tmp = event_detected_node_2_count_tmp +1
               				event_detected_node_2_ts_tmp = data_sets_node_2[-1][0]
				else:
					if(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_tmp))> detection_timeout_tmp):
						print("####### Temperature change at node 2 detected on: "+str(data_sets_node_2[-1][0]) +"#######")
						print("Last temperature change at node 2 detected on: " + str(event_detected_node_2_ts_tmp))
						print("Time-Delta of detected temperature events at node 2: "+str(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_tmp))))
						detect_events_output_fh = open(detect_events_output_file,"a+")
						detect_events_output_fh.write(str(data_sets_node_2[-1][0])+",tmp,"+str(float(data_sets_node_2[0][2])-float(data_sets_node_2[len(data_sets_node_2)-1][2]))+"\n")
						detect_events_output_fh.close()
						event_detected_node_2_ts_tmp = data_sets_node_2[-1][0]
			#Wind event
			else:
				if(event_detected_node_2_count_wind == 0):
                                        print("First wind change at node 2 detected since start of detection: "+str(data_sets_node_2[-1][0]))
                                        event_detected_node_2_count_wind = event_detected_node_2_count_wind +1
                                        event_detected_node_2_ts_wind = data_sets_node_2[-1][0]
                                else:
                                        if(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_wind))> detection_timeout_wind):
                                                print("####### Wind change at Node 2 detected on:  "+str(data_sets_node_2[-1][0]) +"#######")
                                                print("Last wind change at node 2 detected on: " + str(event_detected_node_2_ts_wind))
                                                print("Time-Delta of detected wind events at node 2: "+str(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_wind))))
                                                event_detected_node_2_ts = data_sets_node_2[-1][0]
