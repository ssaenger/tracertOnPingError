from matplotlib import pyplot as plt
from matplotlib import style
import sys, getopt
import argparse
import glob
import errno


style.use('ggplot')

from datetime import datetime as DT

ping_errors = dict()
data = dict()
totalCount = 0

def usage():
	prsr = argparse.ArgumentParser()
	prsr.add_argument
	print("Usage: name-of-python-script -d <day>")
	print("Options:")
	print("  -d day to plot   ##/## (2 digit month and 2 digit day)")
	print("Example:")
	print("python parse.py -d 02/20") 

def parseCLA():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'd:h', ['d=', 'help'])
	except getopt.GetoptError as msg:
		print(msg)
		usage()
		sys.exit(2)
		
	if len(opts) == 0:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
			sys.exit(2)
		elif opt in ('-d', '--day'):
			global dayToPlot
			dayToPlot = DT.strptime(arg[:5], '%m/%d')
		else:
			usage()
			sys.exit(2)


def plot():
	# Create key value pairs. Keys are the hours from 1 to 24
	# and values are the drops for each hour.
	for i in range(0,24):
		data[i] = 0
		for x in ping_errors.keys():
			if x.time().hour == i:
				data[i] += 1


	# Prepare the chart			
	x_axis = list(data.keys())
	y_axis = list(data.values())

	fig, ax = plt.subplots()

	ax.bar(x_axis, y_axis, align='center')
	titleStr = str(totalCount) + " ten-second drops on " + str(dayToPlot.date().month) + "-" + str(dayToPlot.date().day)
	ax.set_title(titleStr)
	ax.set_ylabel('Number of drops')
	ax.set_xlabel('Hour')

	ax.set_xticks(x_axis)
	ax.set_yticks(y_axis)

	plt.show()
		


		
if __name__ == "__main__":
	
	parseCLA()
	
	path = './*.log'
	files = glob.glob(path)
	lastMonth = 0
	lastDay = 0
	
	for name in files:
		try:
			with open(name) as fo:
				for line in fo:
					if 'ERROR' in line: # A tracert printout will follow
						global pingTime
						pingTime = DT.strptime(line[:23],'%a %m/%d/%Y %H:%M:%S')
					#print(dayToPlot.date().month, "/", dayToPlot.date().day)
					words = line.strip().split()
					if len(words) > 0:
						if words[0] == '4':
							if '*' in line:
								if pingTime.date().month == dayToPlot.date().month and pingTime.date().day == dayToPlot.date().day:
									# Found packet timeout in hop # 4
									totalCount += 1
									ping_errors[pingTime] = 1
		except IOError as exc:
			if exc.errno != errno.EISDIR:
				sys.exit(2)
				
	plot()			


	

