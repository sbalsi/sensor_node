import time
#import inotify.adapters

#IO
sensorchanges_output_file = "/home/pi/sensor_node/output/detect_sensorchanges_output.txt"

#detect = inotify.adapters.Inotify()
#detect.add_watch(sensorchanges_output_file)

#################################################################
#Functions
#################################################################
def add_data_set_sort_by_time(data_set):
    data_set_timedate = data_set[0]
    data_set_epoch = time_to_epoch(data_set_timedate)

    if len(sensorchanges_data_sets) != 0:
        for i in reversed(sensorchanges_data_sets):
            current_element_epoch = time_to_epoch(i[0])
            if current_element_epoch <= data_set_epoch:
                insert_index = sensorchanges_data_sets.index(i)+1
                sensorchanges_data_sets.insert(insert_index,data_set)
                print(data_set[0]+","+data_set[1]+","+data_set[2]+","+data_set[3].rstrip('\n') + " added to event evaluation")
                break
    else:
        sensorchanges_data_sets.append(data_set)
        print(data_set[0] + "," + data_set[1] + "," + data_set[2] + "," + data_set[3].rstrip('\n') + " added to event evaluation")

    #If difference between last timedate and timedate of current data set greater than EVENT_TIMEOUT --> event block detected.
    if(len(sensorchanges_data_sets) >=2):
        last_timedate_of_data_set = sensorchanges_data_sets[-1][0]
        second_last_timedate_of_data_set = sensorchanges_data_sets[-2][0]
        if(time_to_epoch(last_timedate_of_data_set) - time_to_epoch(second_last_timedate_of_data_set) > EVENT_TIMEOUT):
            print "EVENT BLOCK DETECTED"
            print "Block data sets:"
            for block_data_set in sensorchanges_data_sets:
                print block_data_set
            global sensorchanges_data_sets
            sensorchanges_data_sets = []
            print "Block data cleared"




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
#################################################################
sensorchanges_data_set = ""
sensorchanges_data_sets = []
last_data_set_date_time = ""
EVENT_TIMEOUT = 60 #Time in seconds. Seperates related sensorchanges to different events


print "----------- Start event detection -----------"

while True:
    current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    current_epoch = time_to_epoch(current_date_time)

    sensorchanges_data_set = lastline(sensorchanges_output_file).split(',')
    if (last_data_set_date_time != ""):
        if (time_to_epoch(last_data_set_date_time) != time_to_epoch(sensorchanges_data_set[0]) and current_epoch - time_to_epoch(sensorchanges_data_set[0])<=30):
            add_data_set_sort_by_time(sensorchanges_data_set)
            last_data_set_date_time = sensorchanges_data_set[0]
    else:
        if(current_epoch - time_to_epoch(sensorchanges_data_set[0])<=30):
            add_data_set_sort_by_time(sensorchanges_data_set)
            last_data_set_date_time = sensorchanges_data_set[0]

    time.sleep(1)




