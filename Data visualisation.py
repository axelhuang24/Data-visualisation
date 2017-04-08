from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import json
import time
import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
  
list_arg = []
length_arg = len(sys.argv) - 1
for i in range(length_arg):
	list_arg.append(sys.argv[i+1])

# When -h is in the list of arguments, call this function 
def function_help():
	help_message =  ("optional arguments: -h, --help show this help message and exit -c CROP, --crop CROP specify a region for cropping regions are rectangular"
                     "areas and can be specified as a comma-separated list of 4 numbers for north, east, south, west -n SELECT_NAMES, --name SELECT_NAMES cumulative"
                     "- select cities by this name(s) -a, --all select all cities -l, --list If set, selected city names get listed"
                     "-1,--1d Display a bar chart for the pressure in the first selected city -2, --2d Display a 2D diagram of the positions of selected cities"
                     "-3, --3d Display a 3D diagram of the pressure in all cities")
	print help_message
    
# When -c is in the list of arguments, call this function 
def function_crop():
	# Read the data and add them to the list(meteodata)
	length_arg = len(list_arg) 
	filename = list_arg[length_arg - 1]
	meteodata = []
	for line in open(filename, 'r'):
		meteodata.append(json.loads(line))
	print "Dealing with {} cities.".\
           format(len(meteodata))
	# Crop the data with four given arguments which specify the longitude and the latitude
	for i in range( len(list_arg) ):
		if list_arg[i] == "-c":
			selecteddata = [x for x in meteodata if x["city"]["coord"]["lat"] > float( list_arg[i+3] ) and x["city"]["coord"]["lat"] < float( list_arg[i+1] ) and
					x["city"]["coord"]["lon"] > float( list_arg[i+4] ) and x["city"]["coord"]["lon"] < float( list_arg[i+2] ) ]
	# Return the data selected by longitude and latitude
	return selecteddata

# When -n is in the list of arguments, call this function 
def function_name(selecteddatacrop, meteodata, list_cityname):
	# If we have selected cities by cropping it 
	if len(selecteddatacrop) != 0:
		selecteddataname = []
		# Select cities with names 
		for i in range(len(list_cityname)):
			for x in selecteddatacrop:
				if x["city"]["name"] == list_cityname[i]:
					selecteddataname.append(x)
	# If we didn't crop the data 
	else:
		selecteddataname = []
		# Select cities with names 
		for i in range(len(list_cityname)):
			print list_cityname[i]
			for x in meteodata:
				if x["city"]["name"] == list_cityname[i]:
					selecteddataname.append(x)
	
	return selecteddataname

# When -1 is in the list of arguments, call this function 
def function_afficheone(selectedcity):
	# Get the size
	N = len( selectedcity["data"] )
	# Get morning temperature in this city
	list_morn = [ x["temp"]["morn"]-273.15 for x in selectedcity["data"] ]
	
	# Get day temperature in this city
	list_day = [ x["temp"]["day"]-273.15 for x in selectedcity["data"] ]
	
	# Get evening temperature in this city
	list_eve = [ x["temp"]["eve"]-273.15 for x in selectedcity["data"] ]
	
	# Get night temperature in this city
	list_night = [ x["temp"]["night"]-273.15 for x in selectedcity["data"] ]
	
	# Get the data time 
	list_dt = [ x["dt"] for x in selectedcity["data"] ]
	
	
	date_format="%Y-%m-%d"
	
	list_xticks = [ time.strftime(date_format, time.gmtime(dt)) for dt in list_dt ]
	
	# Plot the graph
	ind = np.arange(N)
	width = 0.2
	
	p1 = plt.bar(ind, list_morn, width,  color='y')
	p2 = plt.bar(ind+0.2, list_day, width,  color='blue')
	p3 = plt.bar(ind+0.4, list_eve, width,  color='r')
	p4 = plt.bar(ind+0.6, list_night, width,  color='black')
	plt.xlabel('Time')
	plt.ylabel('Temperature')
	plt.title('Temperature in selected city at different time')
	plt.xticks(ind + width/2., list_xticks, rotation='vertical')
	plt.yticks(np.arange(-10, 16, 2))
	morn_patch = mpatches.Patch(color='y', label='Morning')
	day_patch = mpatches.Patch(color='blue', label='Day')
	eve_patch = mpatches.Patch(color='r', label='Evening')
	night_patch = mpatches.Patch(color='black', label='Night')
	plt.legend(handles=[morn_patch, day_patch, eve_patch, night_patch])
	plt.show()
	print 'Succeed'

# When -2 is in the list of arguments, call this function 
def function_affichetwo(selectedcity):
	# Read the data and add it to the list(meteodata)
	length_arg = len(list_arg) 
	filename = list_arg[length_arg - 1]
	meteodata = []
	for line in open(filename, 'r'):
		meteodata.append(json.loads(line))
	
	# Get the longitude(as x) and the latitude(as y)
	list_x = [ x["city"]["coord"]["lon"] for x in meteodata ]
	list_y = [ y["city"]["coord"]["lat"] for y in meteodata ]
	
	# Get the longitude(as list_x) and the latitude(as list_y) of selected cities
	list_selectedx = [ x["city"]["coord"]["lon"] for x in selectedcity ]
	list_selectedy = [ y["city"]["coord"]["lat"] for y in selectedcity ]
	
	# Plot it
	plt.figure()
	axes = plt.subplot()
	allcity= axes.scatter(list_x, list_y, s=20)
	ourselectedcity = axes.scatter(list_selectedx, list_selectedy, s=60, c='r')
	plt.title('The scatter graph about the cities around the world')
	axes.legend((allcity, ourselectedcity), (u'All the cities', u'Our selected city'), loc=2)
	plt.show()
	print 'Succeed'

# When -3 is in the list of arguments, call this function 
def function_affichethree():
	# Read the data and add it to the list(meteodata)
	length_arg = len(list_arg) 
	filename = list_arg[length_arg - 1]
	meteodata = []
	for line in open(filename, 'r'):
		meteodata.append(json.loads(line))
	
	# Get longitude(as list_x), latitude(as list_y) and pressure(as list_pressure)
	list_x = [ x["city"]["coord"]["lon"] for x in meteodata ]
	list_y = [ y["city"]["coord"]["lat"] for y in meteodata ]
	list_pressure = [ z["data"][0]["pressure"] for z in meteodata ]

	# plot it in 3D
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.plot_trisurf(list_x, list_y, list_pressure, cmap=cm.jet)
	plt.title('Pressure in the world')
	plt.show()
	print 'Succeed'

if __name__ == "__main__":
	# If '-h' is in the list of arguments, display the help message 
	if '-h' in list_arg:
		print 'can acces to function_help()'
		function_help() 
	else:
		pass 
		
	# If '-c' is in the list of arguments, crop the data with the four arguments that specify the longitude and the latitude
	if '-c' in list_arg:
		print 'can access to function_crop()'
		selecteddatacrop = function_crop()
		print "After cropping we have {} cities.".\
			format(len(selecteddatacrop))
	else:
		selecteddatacrop = []
	
	# If '-n' is in the list of arguments, select cities with given names
	if '-n' in list_arg:
		# Read the data and add it to the list(meteodat)
		print 'can acces to function_name()'
		length_arg = len(list_arg) 
		filename = list_arg[length_arg - 1]
		meteodata = []
		for line in open(filename, 'r'):
			meteodata.append(json.loads(line))
		# Make a list which contains those given names 
		list_cityname = []
		print "Selected cities:"
		for i in range(len(list_arg)):
			if list_arg[i] == '-n':
				print list_arg[i + 1]
				list_cityname.append( list_arg[ i + 1 ] )
		# Call the function to select the data by names 
		selecteddataname = function_name(selecteddatacrop, meteodata, list_cityname)
	else:
		pass
		
	# If '-1' is in the list of arguments, display temperatures in one city
	if '-1' in list_arg:
		print 'Plot in 1 dimension'
		selectedcity = selecteddataname[0]
		
		function_afficheone(selectedcity)
	else:
		pass
	
	# If '-2' is in the list of arguments, display cities and those selected cities tend to be more important
	if '-2' in list_arg:
		print 'Plot in 2 dimensions'
		
		# Get selected cities
		selectedcity = []
		selectedcity = selecteddataname
		
		# Call the function 
		function_affichetwo(selectedcity)
	else:
		pass
	
	# If '-3' is in the list of arguments, display cities' pressure in 3D
	if '-3' in list_arg:
		print 'Plot in 3 dimensions'
		
		function_affichethree()
	else:
		pass
		
		
		
		
		
		
		
		
		
		
		
		
		
		
        

