import inotify.adapters

i = inotify.adapters.Inotify()

i.add_watch('sensor_node_data.txt')

for event in i.event_gen():
    if event is not None:
	print("File changed!\n")
