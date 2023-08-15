#!/usr/bin/env python3

# Python script to visualize data from the Nagel-Schreckenberg traffic model
# simulation.
# The script generates plots for position (density) and velocity of the cars 
# as a function of time.
# Plots can be generated in PNG, INTERACTIVE or HTML formats.
#
# Arguments:
#	- parameter file, e.g. test.ini
#	- file format: png, interactive or html
#
# Requires:
#	Python 3, matplotlib, numpy and plotly (ver 5.15.0+)
#
# Usage:
#	python npyplot.py PARAM_FILE.ini [format]
#
# where format can be 'png', 'interactive' or 'html'
#
# Example:
#	python3 npyplot.py test.ini interactive
#
#
#	/ Ramses van Zon and Marcelo Ponce
#	/ Aug. 2023
#########################################################

import numpy as np
import sys

##########################################################

##### READ AND PROCESS DATA FUNCTION

def read_data(param_File):
	"""Function to read and process numpy arrays from simulation"""

        ## READ and process DATA
	ini=dict()
	for line in open(param_File):
		key,value=line.split("=",2)
		ini[key]=value[:-1]

	prefix = ini['outputprefix']
	time = np.load(prefix+"-time.npy")
	dens = np.load(prefix+"-dens.npy")
	velo = np.load(prefix+"-velo.npy")

	t1 = time[0][0]
	t2 = time[-1][0]
	x1 = 0
	x2 = dens.shape[1]-1
	extent = [x1,x2,t1,t2]

	parameters  = ""
	for key in ini:
		parameters += " "+key+"="+ini[key]

	return time,dens,velo, extent, parameters, prefix;


##########################################################

##### PLOTTING FUNCTIONS #####
### PNG OUTPUT

def png_output(dens,velo, parameters,extent,prefix):
	"""Function to generate plots in a PNG file."""

	import matplotlib.pyplot as plt

	fig,(ax1,ax2) = plt.subplots(1,2)
	fig.set_size_inches(14,7)
	fig.suptitle("Nagel-Schreckenberg Traffic Model\n\n"+parameters)

	im1 = ax1.imshow(dens,origin='lower',cmap='gray_r',extent=extent,aspect='auto')
	plt.colorbar(im1,ax=ax1)
	ax1.title.set_text("car density")
	ax1.set_xlabel("x")
	ax1.set_ylabel("t")

	im2 = ax2.imshow(velo,origin='lower',cmap='RdYlGn',extent=extent,aspect='auto')
	plt.colorbar(im2,ax=ax2)
	ax2.title.set_text("car velocity")
	ax2.set_xlabel("x")

	plt.tight_layout()

	plt.savefig(prefix+".png")
	print("Created",prefix+".png", file=sys.stdout)

##########################################################

### INTERACTIVE PLOT

def interactive_plot(dens,velo, time, fmt="html", filename=''):
	""" Function to generate interactive plots or HTML files. Requires plotly version 5+."""
	import plotly.express as px
                
	print(">> interactive mode detected...", file=sys.stdout)
	print("\t ** WARNING ** Please note that is a 'beta' feature -- i.e. it may not work as expected when trying to visualize *large* datasets!", file=sys.stdout)
	if (fmt=="html"):
		print("\t figures will be saved in HTML files...", file=sys.stdout)
	else:
		print("\t visualizations will be rendered in your browser...", file=sys.stdout)

	# separated plots
	# density
	fig_dens=px.imshow(dens, labels=dict(x="position", y="time", color="density"),
		y=np.linspace(float(time[0]),float(time[-1]),time.shape[0]),
		origin='lower', aspect='auto')	#, binary_string=True)
	# adjust axes
	fig_dens.update_layout(template='plotly_dark', margin=dict(l=10, r=10, t=100, b=50))
	fig_dens.update_xaxes(range=[0, dens.shape[1]])
	fig_dens.update_yaxes(range=[0, 1000], autorange=True)
	#fig_dens.update_layout(yaxis_range=[0, time[-1]])

	if (fmt=="html"):
		fig_dens.write_html(filename+"-dens"+'.html')
	else:
		fig_dens.show()

	# velocity
	fig_veloc=px.imshow(velo, labels=dict(x="position", y="time", color="velocity"),
		y=np.linspace(float(time[0]),float(time[-1]),time.shape[0]),
		origin='lower', aspect='auto')
	# adjust axes
	fig_veloc.update_layout(template='plotly_dark', margin=dict(l=10, r=10, t=100, b=50))
	fig_veloc.update_xaxes(range=[0, velo.shape[1]])
	fig_veloc.update_yaxes(range=[0, time[-1]], autorange=True)

	if (fmt=="html"):
		fig_veloc.write_html(filename+"-veloc"+'.html')
	else:
		fig_veloc.show()

	# combined plots
	fig_mosaic = px.imshow(np.array([dens,velo]),
			y=np.linspace(float(time[0]),float(time[-1]),time.shape[0]), origin='lower', facet_col=0)	#, labels={'facet_col':'sigma'} )
	# Set facet titles
	for i, sigma in enumerate(["density","velocity"]):
	       fig_mosaic.layout.annotations[i]['text'] = '%s' %sigma

	# use different color scales
	# update traces to use different coloraxis
	for i, t in enumerate(fig_mosaic.data):
		t.update(coloraxis=f"coloraxis{i+1}")
	for fr in fig_mosaic.frames:
	# update each of the traces in each of the animation frames
		for i, t in enumerate(fr.data):
			t.update(coloraxis=f"coloraxis{i+1}")
	fig_mosaic.update_layout(
		coloraxis={"colorbar": {"x": 0.25, "y": -.1, "len": 0.45, "orientation": 'h', },
				"colorscale": 'gray_r',
			},
		coloraxis2={"colorbar": {"x": 0.75, "y": -.1, "len": 0.45, "orientation": 'h'},
				"colorscale": 'RdYlGn',	#'Thermal',
			},
	)
	if (fmt=='html'):
		fig_mosaic.write_html(filename+'.html')
	else:
		fig_mosaic.show()


##########################################################
##########################################################

def main() -> int: 

	# define possible formats for output
	formats=["png","interactive","html"]

	## command-line argument parsing...
	# 1st argument must be an INI file
	# check that at least one argument is given
	if len(sys.argv)<2:
		print("Error: no ini file prefix given on command line", file=sys.stderr)
		sys.exit(1)
	# check whether a second argument, output format, was given...
	elif len(sys.argv)>=3:
		fmt=sys.argv[2]
		# check that is indeed a valid format...
		if not(fmt in formats):
			print("Error: unrecognized format "+"<"+fmt+">"+" -- possible options are "+str(formats), file=sys.stderr)
			sys.exit(1)
	else:
		# if not format was specifeid, then will assume default format, i.e. formats[0] <- PNG
		fmt=formats[0]


	#####################################

	## READ and process DATA
	time,dens,velo, extent, parameters, prefix = read_data(sys.argv[1])


	#####################################


	# generate output
	if (fmt == formats[0]):
		png_output(dens,velo, parameters,extent,prefix)
	else:
		interactive_plot(dens,velo, time, fmt,prefix)

	return 0

	
	#############################################################


# to be executed when run as a script
if __name__ == '__main__':
	sys.exit(main())


#####################################################################
#####################################################################
