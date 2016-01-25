#!/usr/bin/python

# Import modules for CGI handling 
import cgi
import cgitb 
import MySQLdb
import subprocess

import pprint
pp = pprint.PrettyPrinter(indent=4)


# Webpages


TITLE = ""

#panels = ["nick", "is", "cool"]

def system_call ( process ):

	while ( True ):
		locate = process.stdout.readlines()

		return locate


def fetch_panels_from_DB():

	panels = []

	db = MySQLdb.connect(host="mgsrv01",    # your host, usually localhost
                     user="easih_ro",         # your username
#                     passwd="megajonhy",  # your password
                     db="GeminiDB")        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Use all the SQL you like
	cur.execute("SELECT * FROM panel")

# print all the first cell of all the rows
	for row in cur.fetchall():

		name = row[ 1 ] 
		name = name.lstrip(" ")
		if (name.startswith("_")):
			continue

		panels.append( name )

	db.close()

	return panels


def fetch_gnumbers_from_DB():

	gnumbers = []

	db = MySQLdb.connect(host="mgsrv01",    # your host, usually localhost
                     user="easih_ro",         # your username
#                     passwd="megajonhy",  # your password
                     db="GeminiDB")        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Use all the SQL you like
	cur.execute("SELECT name, runfolder FROM sample")

# print all the first cell of all the rows
	for row in cur.fetchall():

		gnumber = row[ 0 ] 

		gnumbers.append( gnumber )

	db.close()


	return gnumbers


#
# Setup the page
#
def make_header(  ):

	s  =  "Content-type:text/html\r\n\r\n"
	s +=  "<html><head><title>%s</title></head>\n" % TITLE
	s +=  "<body bgcolor=lightgrey>"
	return s

def print_page( page ):

		
# AUTO GENERATED PAGES

	if ( page == "Re-Analyse" ):
		global TITLE 
		TITLE = "Gemini re-analysis"
		print make_header()

		### SUBMIT BUTTON PAGE ###

		if (form.getvalue ('Run_button')):
			
			s  = "<center><h1>Re-Analyser : Results</h1></center>\n"
			s += "<p></p>\n <hr>"
			s += "<BR>"
			gnumber = form.getvalue('gnumber')
			panel_list = form.getvalue('panels')

			panels_printed = panel_list.split(",")
			panels_printed = "<BR>".join(panels_printed)
			s += "<font size=3>"
			s += "Running re analysis of :  <b> %s </b>" % gnumber
			s += "<BR><BR>"
			s += "Selected panels: <BR>"
			s += "<b>%s</b>" % panels_printed
			s += "<BR><BR><BR>"

			path_hyperlink = "placeholder"

			s += "New gemini report location : <b> %s </b>"	% path_hyperlink
			s += "</font>"
			s += "<BR><BR>"
			s += "<hr>"
			s += "<footer> Return to: <a href=?page=Re-Analyse> Re-Analyser</a> </footer>"
			s += "<footer> Return to: <a href=?page=> Tools index</a> </footer>"

			print s
			exit()

		############################################

		gnumber = ""

		if (form.getvalue('gnumber')):
			gnumber = form.getvalue('gnumber')

		picked_panels = ''

		if ( form.getvalue('panels')):
			picked_panels = form.getvalue('panels')

		if ( form.getvalue('panel')):
			picked_panels = ",".join([picked_panels, form.getvalue('panel')])

		if ( form.getvalue('rm_panels_button') ):
			rm_panels = form.getvalue('rm_panels')

			if (isinstance( rm_panels, list)):
				for rm_panel in rm_panels:
					picked_panels = picked_panels.replace(str( rm_panel), "")
			else:
				pass
				picked_panels = picked_panels.replace(str( rm_panels ), "")

		picked_panels = picked_panels.replace(",,", ",")
		picked_panels = picked_panels.rstrip(",")
		picked_panels = picked_panels.lstrip(",")



		s  = "<center><h1>Re-Analyser : Gemini sample re-analysis</h1></center>\n"
		s += "<p></p>\n <hr>"
		s += "<BR> This page is for the re analysis of gemini samples. You will need;<BR><ul><li><b> Gnumber</li><BR><li> Idea of what panel you want to use<b></li></ul>"
		s += "<BR>"
		s += "<form name='sample_and_panel' action='testface.cgi'>"  
		

		##### GNUMBER MEMORY #####

		if form.getvalue('gnumber'):
			gnumber = form.getvalue('gnumber')
			s += "G-number   :&nbsp&nbsp&nbsp&nbsp<select disabled name='gnumber''"
			s += "<option value='%s'> Select sample </option>" % gnumber
		else:
			s += "G-number   :&nbsp&nbsp&nbsp&nbsp<select name='gnumber'>"
			s += "<option value=""> Select sample </option>"
		
		############################################	

		gnumbers = fetch_gnumbers_from_DB()

		for gnum in sorted(gnumbers):
			#print gnumber
			#exit()
			if not gnum.startswith("G"):
				continue
			s += "<option value='%s' > %s </option>" % (gnum, gnum)

		s += "</select>"
		s += "<BR>"

			
		s += "Panel name : <select name='panel' >"
		s += "<option value=""> Select a panel </option>"
		
		panels = fetch_panels_from_DB()
		#pp.pprint( panels )

		for panel in sorted(panels):
			if panel.startswith("_"):
				continue
			s += "<option value='%s' > %s </option>" % ( panel, panel)

		s += "</select>"
		s += "<input type='submit' name='add_panel' value='Add Panel'>"
		s += "<BR>"
		s += "<input type='hidden' name='page' value='Re-Analyse'>"
		s += "<input type='hidden' name='panels' value='%s'>" % picked_panels
		
		
		s += "<BR>Panels for re analysis :<BR>"
		
		duplet_panels = {}
		for picked_panel in sorted(picked_panels.split(",")):
			if (picked_panel == "" ):
				continue

			if picked_panel in duplet_panels:
				continue

			s += '<BR><input type="checkbox" name="rm_panels" value="%s"> %s<br>' % (picked_panel , picked_panel)
			duplet_panels[ picked_panel ] = 1

		s += "<BR><input type='submit' name='rm_panels_button' value='Remove Panel'>"
		s += "<BR>"

		# see BRUGGERFU MANUAL FOR MORE TIPS LIKE THIS


		if picked_panels == "":
			s += "<input type='submit' name='Run_button' value='Please add panels to continue' disabled>"
		else:
			s += "<input type='submit' name='Run_button' value='Re-Analyse'>"


		
		s += "<BR><BR>"
		s += "<hr>"
		s += "<footer> To reset this page : <a href=?page=Re-Analyse> click here</a> </footer>"
		s += "<footer> Return to : <a href=?page=> Tools index</a> </footer>"


		s += "</form>"

		print s
		exit()

################# BAMFIND ###########################################################################


	if (page == "bam_find"):
		global TITLE 
		TITLE = "Gemini .bam finder"
		print make_header()

		
			

		gnumber = ""
		if (form.getvalue('gnumber')):
			gnumber = form.getvalue('gnumber')


  		s = "<center><h1>Bam-Find : Gemini .bam file locator</h1></center>\n"
		s += "<p></p>\n <hr>"
		s += "<BR> This tool locates a <b>\".bamfile\"</b> for a <b>GEMINI</b> sample - this can then be loaded up in IGV2 for inspection<BR><BR> You will need;<BR><ul><li><b> Gnumber</li></ul>"
		s += "<BR><BR><BR>"

		s += "<form name='bamfinder' action ='testface.cgi'>"
		s += "<input type='hidden' name='page' value='bam_find'>"

		s += "G-number   :&nbsp&nbsp&nbsp&nbsp<select name='gnumber'>"
		s += "<option value=""> Select sample </option>"
		


		gnumbers = fetch_gnumbers_from_DB()

		for gnum in sorted(gnumbers):
			#print gnumber
			#exit()
			if not gnum.startswith("G"):
				continue
			s += "<option value='%s' > %s </option>" % (gnum, gnum)



		
		s += "<input type='submit' name='locate_file' value='Please select a Gnumber' required>"

		if form.getvalue('gnumber') == None:
			s += "<BR><BR><BR><font color=red><b>!!!PLEASE SELECT A GNUMBER AND RE-RUN!!!</font></b><BR><BR>"
		else:
			proc1 = subprocess.Popen("ssh mgcl01 locate test" , stdout=subprocess.PIPE, shell=True)
			location_return = system_call(proc1)
			print ("").join(location_return)
			


		s += "<hr>"
		s += "<footer> To reset this page : <a href=?page=bam_find> click here</a> </footer>"
		s += "<footer> Return to : <a href=?page=> Tools index</a> </footer>"

		print s
		exit()

####################################################################################################
		
			
	else:
		global TITLE 
		TITLE = "Informatic Tool Index"
		print make_header()
		s  = "<center><h1>Molecular Genetics : Informatic Tools Directory</h1></center>\n"
		s += "<p></p>\n <hr>"
		s += "<BR><ul><li><b>Re-Analyse:</b> Re-do bio-informatic analysis of a gemini sample - <a href=?page=Re-Analyse>Re-Analyse</a>"
		s += "<BR>"
		s += "<li><b>Bam-Find:</b> find the path to a Gemini bamfile <a href=?page=bam_find>Bam-Find</a></ul>"	
	
		print s
		exit()




# Create instance of FieldStorage 
form = cgi.FieldStorage() 
page = form.getvalue('page')




print_page( page )