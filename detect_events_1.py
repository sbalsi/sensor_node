import time
#import inotify.adapters

#IO
sensorchanges_output_file = "/home/pi/sensor_node/output/detect_sensorchanges_output.txt"

#################################################################
#Globals
#################################################################
sensorchanges_data_set = ""
sensorchanges_data_set_str = ""
sensorchanges_data_sets = []
last_data_set_str = ""
last_data_set_added_epoch = 0
data_set_archive = []
SENSORCHANGE_TIMEOUT = 5


#################################################################
#Functions
#################################################################
def add_data_set_sort_by_time(data_set_str, dataset):

    global data_set_archive

    if(data_set_str == ""):
        data_set = dataset
        data_set_timedate = data_set[0]
        data_set_epoch = time_to_epoch(data_set_timedate)

    if(dataset ==0):
        data_set = data_set_str.split(',')
        data_set_timedate = data_set[0]
        data_set_epoch = time_to_epoch(data_set_timedate)

    if len(sensorchanges_data_sets) != 0:
        for i in reversed(sensorchanges_data_sets):
            current_element_epoch = time_to_epoch(i[0])
            if current_element_epoch <= data_set_epoch:
                insert_index = sensorchanges_data_sets.index(i)+1
                sensorchanges_data_sets.insert(insert_index,data_set)
                data_set_archive.append(data_set)
                global last_data_set_added_epoch
                last_data_set_added_epoch = time_to_epoch(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
                print(data_set[0]+","+data_set[1]+","+data_set[2]+","+data_set[3].rstrip('\n') + " added to event evaluation")
                break
    else:
        sensorchanges_data_sets.append(data_set)
        data_set_archive.append(data_set)
        global last_data_set_added_epoch
        last_data_set_added_epoch = time_to_epoch(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        print(data_set[0] + "," + data_set[1] + "," + data_set[2] + "," + data_set[3].rstrip('\n') + " added to event evaluation")


def evaluateEventBlock(data):
    print "Block data sets:"
    for block_data_set in data:
        print block_data_set
    global sensorchanges_data_sets
    sensorchanges_data_sets = []
    global last_data_set_added_epoch
    last_data_set_added_epoch = []
    print "Block data cleared"


def lastline(data_file):
    with open(data_file, "r") as f:
        lines = f.readlines()
    return lines[-1].strip('\n')


def secondtolastline(data_file):
    with open(data_file, "r") as f:
        lines = f.readlines()
    return lines[-2].strip('\n')

def time_to_epoch(date_time):
    pattern = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return epoch

def epoch_to_time(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch+3600))


#################################################################
#Main
#################################################################


print "----------- Start event detection -----------"

while True:
    current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    current_epoch = time_to_epoch(current_date_time)

    sensorchanges_data_set_str = lastline(sensorchanges_output_file)
    sensorchanges_data_set = sensorchanges_data_set_str.split(',')
    secondtolast_sensorchanges_data_set_str = secondtolastline(sensorchanges_output_file)
    secondtolast_sensorchanges_data_set = secondtolast_sensorchanges_data_set_str.split(',')
    buffer_sensorchanges = []

    #Test if data_set already evaluated
    if(len(data_set_archive) ==0):
        buffer_sensorchanges.append(sensorchanges_data_set)
        buffer_sensorchanges.append(secondtolast_sensorchanges_data_set)
    elif(len(data_set_archive) >0):
        foundlast = 0
        foundsecondtolast = 0
        for archive_set in data_set_archive:
            if (archive_set[0] == sensorchanges_data_set[0] and archive_set[1] == sensorchanges_data_set[1] and archive_set[2] == sensorchanges_data_set[2] ):
                foundlast = 1
        if(foundlast ==0):
            buffer_sensorchanges.append(sensorchanges_data_set)

        for archive_set in data_set_archive:
            if (archive_set[0] == sensorchanges_data_set[0] and archive_set[1] == sensorchanges_data_set[1] and archive_set[2] == sensorchanges_data_set[2]):
                foundsecondtolast = 1
        if(foundsecondtolast ==0):
            buffer_sensorchanges.append(secondtolast_sensorchanges_data_set)


    #Adding values to event block for evaluation
    if (len(sensorchanges_data_sets) != 0 and len(buffer_sensorchanges)>=1):
        found = 0
        for buffer_set in buffer_sensorchanges:
            for sensorchange in sensorchanges_data_sets:
                if(buffer_set[0] == sensorchange[0] and buffer_set[1] == sensorchange[1] and buffer_set[2] == sensorchange[2]):
                    found = 1
            if(found ==0 and current_epoch - time_to_epoch(buffer_set[0]) <= 30 ):
                add_data_set_sort_by_time("",buffer_set)
            found = 0
    elif(len(sensorchanges_data_sets) == 0 and len(buffer_sensorchanges) >=1):
        if(sensorchanges_data_set_str != secondtolast_sensorchanges_data_set_str):
            if (current_epoch - time_to_epoch(secondtolast_sensorchanges_data_set[0]) <= 30 ):
                add_data_set_sort_by_time(secondtolast_sensorchanges_data_set_str, 0)
            if (current_epoch - time_to_epoch(sensorchanges_data_set[0]) <= 30 ):
                add_data_set_sort_by_time(sensorchanges_data_set_str, 0)
        else:
                add_data_set_sort_by_time(sensorchanges_data_set_str,0)


    # If no new sensorchange is registred for SENSORCHANGE_TIMEOUT
    if (last_data_set_added_epoch != 0 and len(sensorchanges_data_sets) != 0 and current_epoch-last_data_set_added_epoch >= SENSORCHANGE_TIMEOUT):
        print "SENSORCHANGE TIMEOUT"
        evaluateEventBlock(sensorchanges_data_sets)

    time.sleep(1)




