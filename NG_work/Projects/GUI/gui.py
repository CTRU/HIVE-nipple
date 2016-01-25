# Test GUI using Tkinter
# Nick Gleadall - 26/05/2015

# -----------------------------------------------------------------------------------------------------------------
# IMPORT MODULES

from Tkinter import *
import subprocess


# -----------------------------------------------------------------------------------------------------------------
# DEFINE FUNCTIONS

# Define system_call - this is from pipeliners. 

def system_call( step_name, cmd ):
	try:
		subprocess.check_call(cmd, shell=True)

	except subprocess.CalledProcessError as scall:
		print "Script failed at %s stage - exit code was %s" % (step_name, scall.returncode)
		exit()

# Define the pipeline calling command

def pipeline(script, analysisdir, fastqs):
	# Executes the other scripts
	return "cd " + fastqs.get() + "; python " + script.get() + " " + analysisdir.get() + " " + fastqs.get()


# -----------------------------------------------------------------------------------------------------------------
# SETUP GUI

# Create and name the window
root = Tk()
root.title("Nick's pipeline GUI - TEST VERSION")

# Set the variables needed as string variables

pipeline_name = StringVar()
analysis_dir = StringVar()
fastq_dir = StringVar()

# Make text entry box
w = Label(root, text="Path to pipeline script")
w.pack()

text_entry = Entry(root, textvariable = pipeline_name)
text_entry.pack()
# ------------------------------------------------------


w = Label(root, text="Name of analysis directory e.g. \"Test\"")
w.pack()

text_entry = Entry(root, textvariable = analysis_dir)
text_entry.pack()
# ------------------------------------------------------

w = Label(root, text="Path to directory containing fastq files")
w.pack()

text_entry = Entry(root, textvariable = fastq_dir)
text_entry.pack()

# Add a 'Run' button 
b = Button(root, text="Run fuction", command = lambda: system_call('Command call', pipeline(pipeline_name, analysis_dir,fastq_dir)))
b.pack()

# Call the GUI
root.mainloop()




