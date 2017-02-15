import time
import inotify.adapters

#IO
sensor_data_node_1 = "/home/pi/sensor_node/output/sensor_node_data.txt"
sensor_data_node_2 = "/home/pi/sensor_node/sensor_node2_output_mount/sensor_node_data.txt"
#detect_data_output_file = "/home/pi/sensor_node/output/detect_data_output.txt"  
detect_events_output_file = "/home/pi/sensor_node/output/detect_sensorchanges_output.txt"

detect = inotify.adapters.Inotify()

detect.add_watch(sensor_data_node_1)
detect.add_watch(sensor_data_node_2)


#################################################################
#Functions
#################################################################
def lastline(data_file):
	with open(data_file, "rb") as f:
		f.seek(-2, 2)
		while f.read(1) != b"\n":
			f.seek(-2, 1)
		last = f.readline()

	return last

def time_to_epoch(date_time):
	pattern = '%Y-%m-%d %H:%M:%S'
	epoch = int(time.mktime(time.strptime(date_time, pattern)))
	return epoch

def epoch_to_time(epoch):
	return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch+3600))
#################################################################
#Main
#################################################################
data_sets_node_1 = []
data_sets_node_2 = []



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
detection_timeout_tmp = 1 #Timeout after detection. During this timeout no other event will be detected
detection_timeout_wind = 1
tmp_delta = 3.0 #Value in Celsius at which delta is evaluated as an event
wind_delta = 5.0 #Value in MPH at which delta is evaluated as an event
data_set_count = 2 #Number of data sets for event detection

#Node 1
initial_lastline_node_1 = lastline(sensor_data_node_1)
initial_last_data_set_node_1 =  initial_lastline_node_1.split(',')
data_sets_node_1.append(initial_last_data_set_node_1)

#Node 2
initial_lastline_node_2 = lastline(sensor_data_node_2)
initial_last_data_set_node_2 =  initial_lastline_node_2.split(',')
data_sets_node_2.append(initial_last_data_set_node_2)

print("-------- Start sensor change detection -------")

for event in detect.event_gen():
	if event is not None:

		#Data set gathering
		current_lastline_node_1 = lastline(sensor_data_node_1)
		current_last_data_set_node_1 = current_lastline_node_1.split(',')
		current_lastline_node_2 = lastline(sensor_data_node_2)
		current_last_data_set_node_2 = current_lastline_node_2.split(',')

		if(len(data_sets_node_1) == 0):
			data_sets_node_1.append(current_last_data_set_node_1)
			#print(current_last_data_set_node_1[0] + "," + current_last_data_set_node_1[2].rstrip('\n') + "," +
			#	  current_last_data_set_node_1[1] + ",node1")
		else:
			if (current_last_data_set_node_1[0] != data_sets_node_1[-1][0]):
				data_sets_node_1.append(current_last_data_set_node_1)
			#	print(current_last_data_set_node_1[0] + "," + current_last_data_set_node_1[2].rstrip('\n') + "," +
			#		  current_last_data_set_node_1[1] + ",node1")

		if(len(data_sets_node_2) == 0):
			data_sets_node_2.append(current_last_data_set_node_2)
			#print(current_last_data_set_node_2[0] + "," + current_last_data_set_node_2[2].rstrip('\n') + "," +
			#	  current_last_data_set_node_2[1] + ",node2")
		else:
			if(current_last_data_set_node_2[0] != data_sets_node_2[-1][0]):
				data_sets_node_2.append(current_last_data_set_node_2)
			#	print(current_last_data_set_node_2[0] + "," + current_last_data_set_node_2[2].rstrip('\n') + "," +
			#		  current_last_data_set_node_2[1] + ",node2")


		#Data evaluation for node 1. Start when number of data_sets from node 1 greater than data_set_count
		if(len(data_sets_node_1) == data_set_count):

			#Evaluate data sets from node 1
			CALC_tmp_delta_node_1 = float(data_sets_node_1[-data_set_count][2])-float(data_sets_node_1[-1][2])
			CALC_ABS_tmp_delta_node_1 = abs(float(data_sets_node_1[-data_set_count][2])-float(data_sets_node_1[-1][2]))
			CALC_wind_delta_node_1 = float(data_sets_node_1[-1][1])-float(data_sets_node_1[-data_set_count][1])
			CALC_ABS_wind_delta_node_1 = abs(float(data_sets_node_1[-data_set_count][1])-float(data_sets_node_1[-1][1]))

			print "-------- Node 1: Start data set evaluation --------"
			print("Node1 - Time Delta: " +str(data_sets_node_1[-data_set_count][0])+ "-" +str(data_sets_node_1[-1][0]))
			print("Node1 - Temp Delta: "+str(float(data_sets_node_1[-data_set_count][2]))+" - "+str(float(data_sets_node_1[-1][2]))+" >> "+str(CALC_tmp_delta_node_1))
			print("Node1 - Wind Delta: "+str(CALC_wind_delta_node_1))
			print("-------- Node 1: End data set evaluation ---------")
			print("\n")

			#Event detected because of temperature change greater than tmp_delta or wind wind change greater than wind_delta
			if(CALC_ABS_tmp_delta_node_1 >= tmp_delta or CALC_ABS_wind_delta_node_1 >= wind_delta):
				#Temperature event
				if(CALC_ABS_tmp_delta_node_1 >= tmp_delta):
					if(event_detected_node_1_count_tmp == 0):
						print("First temperature change at node 1 detected since start of detection on: "+str(data_sets_node_1[-1][0]))
						detect_events_output_fh = open(detect_events_output_file,"a+")
						detect_events_output_fh.write(str(data_sets_node_1[-1][0])+",node1,tmp,"+str(CALC_tmp_delta_node_1)+"\n")
						detect_events_output_fh.close()
						event_detected_node_1_count_tmp = event_detected_node_1_count_tmp +1
						event_detected_node_1_ts_tmp = data_sets_node_1[-1][0]
					else:
							if(time_to_epoch(data_sets_node_1[-1][0])-time_to_epoch(str(event_detected_node_1_ts_tmp))> detection_timeout_tmp):
								print("####### Temperature change at node 1 detected on: "+str(data_sets_node_1[-1][0]) +"#######")
								print("Last temperature change at node 1 detected on: " + str(event_detected_node_1_ts_tmp))
								print("Time-Delta of detected temperature events at node 1: "+str(time_to_epoch(data_sets_node_1[-1][0])-time_to_epoch(str(event_detected_node_1_ts_tmp))))
								detect_events_output_fh = open(detect_events_output_file,"a+")
								detect_events_output_fh.write(str(data_sets_node_1[-1][0])+",node1,tmp,"+str(CALC_tmp_delta_node_1)+"\n")
								detect_events_output_fh.close()
								event_detected_node_1_ts_tmp = data_sets_node_1[-1][0]

				#Wind event
				if(CALC_ABS_wind_delta_node_1 >= wind_delta):
						if(event_detected_node_1_count_wind == 0):
							print("First wind change at node 1 detected since start of detection on: "+str(data_sets_node_1[-1][0]))
							detect_events_output_fh = open(detect_events_output_file,"a+")
							detect_events_output_fh.write(str(data_sets_node_1[-1][0])+",node1,wind,"+str(CALC_wind_delta_node_1)+"\n")
							detect_events_output_fh.close()
							event_detected_node_1_count_wind = event_detected_node_1_count_wind +1
							event_detected_node_1_ts_wind = data_sets_node_1[-1][0]
						else:
							if(time_to_epoch(data_sets_node_1[-1][0])-time_to_epoch(str(event_detected_node_1_ts_wind))> detection_timeout_wind):
								print("####### Wind change at node 1 detected on: "+str(data_sets_node_1[-1][0]) +"#######")
								print("Last wind change at node 1 detected on: " + str(event_detected_node_1_ts_wind))
								print("Time-Delta of detected wind events at node 1: "+str(time_to_epoch(data_sets_node_1[-1][0])-time_to_epoch(str(event_detected_node_1_ts_wind))))
								detect_events_output_fh = open(detect_events_output_file,"a+")
								detect_events_output_fh.write(str(data_sets_node_1[-1][0])+",node1,wind,"+str(CALC_wind_delta_node_1)+"\n")
								detect_events_output_fh.close()
								event_detected_node_1_ts_wind = data_sets_node_1[-1][0]

			#Clear data_sets_node_1
			data_sets_node_1 = []

		#Data evaluation for node 2. Start when number of data_sets at node 2 greater than data_set_count
		if(len(data_sets_node_2) == data_set_count):

			#Evaluate data sets from node 2
			CALC_tmp_delta_node_2 =float(data_sets_node_2[-1][2]) - float(data_sets_node_2[-data_set_count][2])
			CALC_ABS_tmp_delta_node_2 = abs(float(data_sets_node_2[-data_set_count][2])-float(data_sets_node_2[-1][2]))
			CALC_wind_delta_node_2 = float(data_sets_node_2[-1][1])-float(data_sets_node_2[-data_set_count][1])
			CALC_ABS_wind_delta_node_2 = abs(float(data_sets_node_2[-data_set_count][1])-float(data_sets_node_2[-1][1]))

			print "-------- Node 2: Start data set evaluation --------"
			print("Node2 - Time Delta: " +str(data_sets_node_2[-data_set_count][0])+ "-" +str(data_sets_node_2[-1][0]))
			print("Node2 - Temp Delta: "+str(float(data_sets_node_2[-1][2]))+"-"+str(float(data_sets_node_2[-data_set_count][2]))+" >> "+str(CALC_tmp_delta_node_2))
			print("Node2 - Wind Delta: "+str(CALC_wind_delta_node_2))
			print("-------- Node 2: End data set evaluation ---------")
			print("\n")

			#Event detected because of temperature change greater than tmp_delta or wind wind change greater than wind_delta
			if(CALC_ABS_tmp_delta_node_2 >= tmp_delta or CALC_ABS_wind_delta_node_2 >= wind_delta):
				#Temperature event
				if(CALC_ABS_tmp_delta_node_2 >= tmp_delta):
					if(event_detected_node_2_count_tmp == 0):
						print("First temperature change at node 2 detected since start of detection on: "+str(data_sets_node_2[-1][0]))
						detect_events_output_fh = open(detect_events_output_file,"a+")
						detect_events_output_fh.write(str(data_sets_node_2[-1][0])+",node2,tmp,"+str(CALC_tmp_delta_node_2)+"\n")
						detect_events_output_fh.close()
						event_detected_node_2_count_tmp = event_detected_node_2_count_tmp +1
						event_detected_node_2_ts_tmp = data_sets_node_2[-1][0]
					else:
							if(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_tmp))> detection_timeout_tmp):
								print("####### Temperature change at node 2 detected on: "+str(data_sets_node_2[-1][0]) +"#######")
								print("Last temperature change at node 2 detected on: " + str(event_detected_node_2_ts_tmp))
								print("Time-Delta of detected temperature events at node 2: "+str(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_tmp))))
								detect_events_output_fh = open(detect_events_output_file,"a+")
								detect_events_output_fh.write(str(data_sets_node_2[-1][0])+",node2,tmp,"+str(CALC_tmp_delta_node_2)+"\n")
								detect_events_output_fh.close()
								event_detected_node_2_ts_tmp = data_sets_node_2[-1][0]

				#Wind event
				if(CALC_ABS_wind_delta_node_2 >= wind_delta):
					if(event_detected_node_2_count_wind == 0):
						print("First wind change at node 2 detected since start of detection on: "+str(data_sets_node_2[-1][0]))
						detect_events_output_fh = open(detect_events_output_file,"a+")
						detect_events_output_fh.write(str(data_sets_node_2[-1][0])+",node2,wind,"+str(CALC_wind_delta_node_2)+"\n")
						detect_events_output_fh.close()
						event_detected_node_2_count_wind = event_detected_node_2_count_wind +1
						event_detected_node_2_ts_wind = data_sets_node_2[-1][0]
					else:
						if(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_wind))> detection_timeout_wind):
							print("####### Wind change at node 2 detected on: "+str(data_sets_node_2[-1][0]) +"#######")
							print("Last wind change at node 2 detected on: " + str(event_detected_node_2_ts_wind))
							print("Time-Delta of detected wind events at node 2: "+str(time_to_epoch(data_sets_node_2[-1][0])-time_to_epoch(str(event_detected_node_2_ts_wind))))
							detect_events_output_fh = open(detect_events_output_file,"a+")
							detect_events_output_fh.write(str(data_sets_node_2[-1][0])+",node2,wind,"+str(CALC_wind_delta_node_2)+"\n")
							detect_events_output_fh.close()
							event_detected_node_2_ts_wind = data_sets_node_2[-1][0]

			# Clear data_sets_node_2
			data_sets_node_2 = []