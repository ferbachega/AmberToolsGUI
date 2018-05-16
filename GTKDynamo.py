text1 = """
#	
#
#	
#	
#
#	
#
#                           ---- GTKDynamo ----
#		                    
#		
#       Copyright 2012 Jose Fernando R Bachega  <ferbachega@gmail.com>
#
#               visit: https://sites.google.com/site/gtkdynamo/
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       GTKDynamo team:
#       - Jose Fernando R Bachega  < Univesity of Sao Paulo - SP, Brazil                              >
#       - Troy Wymore              < Pittsburgh Super Computer Center, Pittsburgh PA - USA            >
#       - Martin Field             < Institut de Biologie Structurale, Grenoble, France               >		
#       - Luis Fernando S M Timmers< Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#
#       Special thanks to:
#       - Lucas Assirati           < Univesity of Sao Paulo - SP, Brazil                              >
#       - Leonardo R Bachega       < University of Purdue - West Lafayette, IN - USA                  >
#       - Richard Garratt          < Univesity of Sao Paulo - SP, Brazil                              >
#
#
#		
"""  
texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"



dialog_text = { 
				'error_topologies/Parameters' : "Error: the topology, parameters or coordinates do not match the system type: ",
				'error_coordiantes'           : "Error: the coordinates do not match the loaded system.",
				'error_trajectory'            : "Error: the trajectory does not match the loaded system.",
				'delete'                      : "Delete memory system.",
				'prune'                       : "Warning: this is an irreversible process. Do you want to continue?",
				'qc_region'                   : "Warning: no quantum region has been defined. Would you like to put all atoms in the quantum region?",
				'delete2'                     : "Warning: there is a system loaded in memory. Are you sure that you want to delete it?"
				}

#System
import datetime
import time
import gtk

try:
	#gtk.rc_parse('gtkrc')
	gtk.rc_parse('.gtkrc-2.0')
except:
	a = None

import threading
import gobject
import sys



import glob, math, os

#pdynamo
from pBabel           import *
from pCore            import * 
from pMolecule        import * 
from pMoleculeScripts import *

#GTKDynamo
from DynamoProject    import *
from Extensions       import *
#pymol
from pymol            import *



class DualTextLogFileWriter ( TextLogFileWriter ):
	  
    def Text ( self, text ):
        #"""Text."""
        #if self.isActive and ( text is not None ): #old code M.F.
		self.file.write ( text )
		log_out = open("log.gui.txt", "a") # RWM / Bachega
		log_out.write(text)                # redirects output to a log text file
		log_out.close()                    #


class window_4_trajectory_tool():
	def on_4window_BARSET_SETFRAME (self,hscale,text= None,  data=None):            # SETUP  trajectory window
		valor =hscale.get_value()
		cmd.frame( int (valor) )
	
	def on_4window_ENTRY_PUSH(self, entry, data=None):
		MAX  = int(self.builder.get_object('4_window_max_hset').get_text())
		MIN  = int(self.builder.get_object('4_window_min_hset').get_text())

		scale = self.builder.get_object("4_window_hscale1")
		scale.set_range(MIN, MAX)
		scale.set_increments(1, 10)
		scale.set_digits(0)	

	def show (self):
		""" Function doc """
		self.builder.get_object('4_window_trajectory_tool').show()

	def hide (self, widget, data=None):
		""" Function doc """
		gtk_dynamo.TrajectoryTool = False
		return False
		
	def on_window_destroy(self, widget, data=None):
		gtk.main_quit()
				
	def __init__(self):
		#builder = gtk_dynamo.builder
		

		builder = gtk.Builder()
		#builder.add_from_string(window2)
		#builder.get_object('window2').show()
		builder.add_from_file("window_4_trajectory_tool.glade") 

		self.builder = builder
		builder.connect_signals(self)		
		gtk_dynamo.TrajectoryTool = False
		
		scale = builder.get_object("4_window_hscale1")
		scale.set_range(1, 100)
		scale.set_increments(1, 10)
		scale.set_digits(0)	
	
class window_23_quickscript():
	def show (self):
		""" Function doc """
		self.builder.get_object('23window_quick_script').show()

	def hide (self, widget, data=None):
		""" Function doc """
		gtk_dynamo.QuickScript = False
		return False
		
	def on_window_destroy(self, widget, data=None):
		gtk.main_quit()
				
	def __init__(self):
		#builder = gtk_dynamo.builder
		

		builder = gtk.Builder()
		#builder.add_from_string(window2)
		#builder.get_object('window2').show()
		builder.add_from_file("window_23_quickscript.glade") 

		self.builder = builder
		builder.connect_signals(self)		
		gtk_dynamo.QuickScript = False
				
class GTKDynamo(threading.Thread):
	
	def import_gtkdyn_project_settings(self,filein):
		last_step      = 0
		working_folder = None
		system         = None
		pymol_session  = None
		last_pymol_id  = None
		
		arq = open (filein, 'r')
		
		for line in arq:

			line2 = line.split()
			try:
				if line2[0] == "last_step":
					last_step = line2[2]
				
				if line2[0] == "working_folder":
					line2Split = line2[2].split("'")
					working_folder = line2Split[1]

				if line2[0] == "system":
					line2Split = line2[2].split("'")
					system = line2Split[1]

				if line2[0] == "pymol_session":
					line2Split = line2[2].split("'")
					pymol_session = line2Split[1]			

				if line2[0] == "last_pymol_id":
					line2Split = line2[2].split("'")
	
					last_pymol_id = line2Split[1]		
			except:
				a =None
		print last_step
		print working_folder
		print system
		print pymol_session
		print last_pymol_id
		 
		return 	last_step ,	working_folder,	system,	pymol_session, last_pymol_id	
	
	def on_window_destroy(self, widget, data=None):
		gtk.main_quit()	

			#=====================#
			# M E N U   I T E N S # 
			#=====================#	

	#======================================#
	# -          1_window_MAIN           - #
	#======================================#	
	def on_1window_MENU_QUIT(self, menuitem, data=None):
		#print "quit"
		cmd.quit()


	def on_1window_MENU_OPEN_SYSTEM(self, menuitem, data=None):	# janela de procura de arquivo
 		
 		filepath = self.get_open_filename()  
		try:
			filetype = get_file_type (filepath)
		except:
			return 0
		print filepath
		
		

		
				
		if  filetype == "py" or filetype == "gtkdyn" :
			self.project = DynamoProject()
			
			# - nova funcao pra abrir os arquivos de projetos - mais robusta - #
			
			last_step,working_folder,system,pymol_session,last_pymol_id = self.import_gtkdyn_project_settings(filepath)
			print last_step
			print working_folder
			print system,pymol_session
			print last_pymol_id
			
			# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
			
			#path = "run " + filepath      - - old function - -  import_gtkdyn_project_settings - - 
			#cmd.do(path) 
			
			#print "system",         system
			#print "last step",      last_step
			#print "pymol_session",  pymol_session
			#print "working folder", working_folder

			self.project.step                       = int(last_step)

			if  filetype == "gtkdyn":
				project_name = filepath.split(".gtkdyn")
				project_name = project_name[0]
			if  filetype == "py":
				project_name = filepath.split(".py")
				project_name = project_name[0]
			self.project_name                       = project_name

			try:
				print last_pymol_id
				self.project.settings['last_pymol_id']  = last_pymol_id
			except:
				print 'last_pymol_id not found'
			
			
			self.builder.get_object("1window_main_dataPath_finder").set_current_folder(working_folder)
			self.builder.get_object("5_window_traj_name").set_current_folder(working_folder)
			self.builder.get_object("8_window_directory_surface_file").set_current_folder(working_folder)
			self.builder.get_object("7_window_filechooserbutton_PRODUCTS").set_current_folder(working_folder)
			self.builder.get_object("7_window_filechooserbutton_REACTANTS").set_current_folder(working_folder)	
			
			self.project.load_coordinate_file_as_new_system(system, self.dualLog)
			#self.project.system      = Unpickle( system )
			cmd.load(pymol_session)		
		
		elif filetype == "pkl" or filetype == "yaml" :
			self.project = DynamoProject()
			data_path    = self.builder.get_object("1window_main_dataPath_finder").get_filename()
			
			#print 'system = ',filepath, '\nfiletype = ', filetype
			
			# loading the pkl or yaml file
			self.project.load_coordinate_file_as_new_system(filepath, self.dualLog)
			self.project.increment_step()
			self.project.check_system(self.dualLog)
			self.project.export_frames_to_pymol('new', self.types_allowed , data_path)
			
			# JOB HISTORY
			step       =  self.project.step
			process    = "new system"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
		
		cmd.set ('sphere_scale'     , self.sphere_scale)
		cmd.set ('stick_radius'     , self.stick_radius)
		cmd.set ('label_distance_digits', self.label_distance_digits)
		cmd.set ('mesh_width',       self.mesh_width )
		cmd.set ("retain_order") # keep atom ordering
		
	def on_1window_MENU_OPEN_NBMODEL_PROPERTIES(self, menuitem, data=None):
		self.window_27_nbmodel.run()
		self.window_27_nbmodel.hide()
		
	def on_1window_MENU_OPEN_TRAJECTORY_DIALOG(self, menuitem, data=None):
		self.load_trj_windows.run()
		self.load_trj_windows.hide()	

	def on_1window_MENU_OPEN_IMPORT_COORDINATES_DIALOG(self, menuitem, data=None):
		self.import_coord_window.run()
		self.import_coord_window.hide()	

	def on_1window_MENU_OPEN_SAVE_FRAME_DIALOG(self, menuitem, data=None):
		text = "step_"+str(self.project.step)+"_frame"
		self.builder.get_object('17_window_SAVE_FRAME_save_frame').set_text(text)
		print text
		self.SAVE_FRAME_dialog.run()
		self.SAVE_FRAME_dialog.hide()

	def on_1window_MENU_OPEN_UMBRELLA_SAMPLING_DIALOG(self, menuitem, data=None):
		text = "step_"+str(self.project.step + 1)+"_umbrella_sampling.trj"
		self.builder.get_object('25_window_umbrella_entry_TRAJECTORY').set_text(text)
		self.umbrella_window.run()
		self.umbrella_window.hide()
 
	def on_1window_MENU_OPEN_NEB_DIALOG(self, menuitem, data=None):
		text = "step_"+str(self.project.step + 1)+"_NEB.trj"
		self.builder.get_object('7_window_NEB__pd_traj_out').set_text(text)
		self.run_NEB_window.run()
		self.run_NEB_window.hide()

	def on_1window_MENU_OPEN_SAW_DIALOG(self, menuitem, data=None):
		text = "step_"+str(self.project.step + 1)+"_SAW.trj"
		self.builder.get_object('30_window_SAW_pd_traj_out').set_text(text)
		self.window_30_SAW.run()
		self.window_30_SAW.hide()
	
	def on_1window_MENU_OPEN_NORMAL_MODES_DIALOG(self, menuitem, data=None):
		text = "step_"+str(self.project.step + 1)+"_normal_modes.trj"
		self.builder.get_object('10_window_NMoldes_traj').set_text(text)
		self.normal_modes_window.run()	
		self.normal_modes_window.hide()

	def on_1window_MENU_OPEN_CHARGE_DIALOG(self, menuitem, data=None):
		self.charge_window.run()	
		self.charge_window.hide()

	def on_1window_MENU_OPEN_QUICK_SCRIPT_WINDOW(self, menuitem, data=None):
		if self.QuickScript == False:
			window = window_23_quickscript()
			window.show()
			self.TrajectoryTool = True
			#return "window2 open"
	
	def on_1window_MENU_OPEN_MERGE_DIALOG(self, menuitem, data=None):
		self.merge_window.run()	
		self.merge_window.hide()

	def on_1window_MENU_OPEN_SURFACE_DIALOG (self, menuitem, data=None):
		""" Function doc """
		text = "step_"+str(self.project.step)+"_surface"
		self.builder.get_object('8_window_entry_name_save_surface').set_text(text)
		self.surf_Save_window.run()
		self.surf_Save_window.hide()
		
	def on_1window_MENU_OPEN_CHARGE_RESCALE(self, menuitem, data=None):
		self.charge_res_window.run()	
		self.charge_res_window.hide()

	def on_1window_MENU_OPEN_LOG_FILES(self, menuitem, data=None):
		filename = self.get_open_filename_log()	
		x,y = parse_log_file (filename)
		#print y
		if x == "matrix":
			print 'matrix log file'
			print y
			self.render_plot_matrix (y, title = 'GTK Dynamo 2D SCAN', xlabel = 'r(3 - 4)', ylabel = 'r(1 - 2)')
		else:	
			self.render_plot(x,y)

	def on_1window_MENU_RUN_OPEN_SELECTIONS_PDYNAMO(self, menuitem, data=None):
		try: 
			self.on_29window_build_treeview()
			self.window_29_selections.run()
			self.window_29_selections.hide()
		except:
			print "system empty"		
	
	def on_1window_MENU_RUN_COMPLETE_RESIDUES(self, menuitem, data=None):
		data_path  = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		selection  = "sele"   
		selection  = take_pymol_selection(selection)
		print selection 
		
		filename = data_path + "/tmp.pdb"
		
		# saving a pdb file
		self.project.export_state_to_file (filename, "pdb")
		
		# building the selection
		new_selection =	COMPLETE_residue_from_PDB(filename, selection)
		
		new_list = []
	
		for i in  new_selection:
			i = i - 1
			new_list.append(i)
		
			pymol_put_table (new_list, "sele")
		pymol_id  = self.project.settings['last_pymol_id']
		string22  = 'select sele, ('+pymol_id+ ' and  sele )'
		cmd.do(string22)
			
	def on_1window_MENU_OPEN_TLEAP_DIALOG(self, menuitem, data=None):
		self.TLEAP_window.run()	
		self.TLEAP_window.hide()
	
	def on_1window_MENU_OPEN_ANTECHAMBER_DIALOG(self, menuitem, data=None):
		self.ANTECHAMBER_window.run()
		self.ANTECHAMBER_window.hide()

	def on_1window_MENU_OPEN_GMX_BUILDER_DIALOG(self, menuitem, data=None):
		self.GromacsProject = GromacsProject()
		self.GMX_window.run()
		self.GMX_window.hide()

	def on_1window_MENU_OPEN_SCAN_DIALOG(self, menuitem, data=None):
		print texto_d1
		print texto_d2d1
		text = "step_"+str(self.project.step + 1)+"_scan"
		self.builder.get_object('19_window_SCAN_mim_param_entry_TRAJECTORY1').set_text(text)
		self.SCAN_window.run()
		self.SCAN_window.hide()

	def on_1window_MENU_OPEN_SCAN_2D_DIALOG(self, menuitem, data=None):
		print texto_d1
		print texto_d2d1
		text = "step_"+str(self.project.step + 1)+"_scan2D"
		self.builder.get_object('26_window_scan2d_entry_mim_param_TRAJECTORY').set_text(text)
		self.SCAN_2D_window.run()
		self.SCAN_2D_window.hide()

	def on_1window_MENU_OPEN_TRAJECTORY_TOOL_WINDOW(self, menuitem, data=None):
		if self.builder.get_object('1window_main_menuitem2').get_active():
			self.builder.get_object('4_window_trajectory_tool').show() 
		else:
			self.builder.get_object('4_window_trajectory_tool').hide()

	def on_1window_MENU_OPEN_HISTORY_JOBS_WINDOW(self, data = None):
		if self.TrajectoryTool == False:
			window = window_4_trajectory_tool()
			window.show()
			self.TrajectoryTool = True

	
	def on_1window_BUTTON_IMPORT_MM_SYSTEM(self, button, data=None):  #"old import_molmec_system(*args): "
		if self.project.system != None:
			# 1 step
			#self.builder.get_object('33_window_message_label1').set_text("Delete the system in memory?")
			self.builder.get_object('33_window_messagedialog_warning').format_secondary_text(dialog_text['delete2'])
			# 2 step
			#self.load_trj_windows.hide() # hide the load_trj window
			
			# 3 step
			a = self.window_33_message.run()
			
			# 4 step
			self.window_33_message.hide()
			
			# 5 step
			#print a
			if a == -5:
				# 6 step
				b = None
			else:
				return 0
		try:
			data_path    = self.builder.get_object("1window_main_dataPath_finder").get_filename()												
			fftype       = self.builder.get_object("1window_main_combobox_MM_model").get_active_text()			# combo box combox_model
			self.project = DynamoProject()
			
			if fftype == "AMBER":
				amber_params  	= self.builder.get_object("1window_main_entry_prmtop").get_filename()
				amber_coords  	= self.builder.get_object("1window_main_entry_crd").get_filename()
				
				self.project.set_AMBER_MM(amber_params, amber_coords, self.dualLog)
				
			elif fftype == "CHARMM":											
				charmm_params     = self.builder.get_object("1window_main_entry_prmtop").get_filename()
				charmm_topologies = self.builder.get_object("1window_main_entry_crd").get_filename()
				charmm_coords     = self.builder.get_object("1window_main_xyzc").get_filename()
				
				self.project.set_CHARMM_MM(charmm_params, charmm_topologies, self.dualLog)
				filetype = self.project.load_coordinate_file_to_system(charmm_coords, self.dualLog)	
				self.project.settings['coordinates'] = charmm_coords
				
			elif fftype == "GROMACS":
				gromacs_params    = self.builder.get_object("1window_main_entry_prmtop").get_filename()					#
				gromacs_coords    = self.builder.get_object("1window_main_entry_crd").get_filename()					#			
				
				self.project.set_GROMACS_MM (gromacs_params, gromacs_coords, self.dualLog)
			
			elif fftype == "OPLS":
				opls_params       = self.builder.get_object("1window_main_entry_prm_opls").get_filename()
				opls_coords       = self.builder.get_object("1window_main_entry_crd").get_filename()		
				self.project.set_OPLS_MM( opls_params, opls_coords, self.dualLog)
			
			# nbModel applied
			self.project.set_nbModel_to_system()
			
			# nbModel incrementing the step
			self.project.increment_step()
			
			# Loading the actual frame in pymol.
			self.project.export_frames_to_pymol('new', self.types_allowed , data_path)

			# Check System
			self.project.check_system(self.dualLog)

			# JOB HISTORY
			step       =  self.project.step
			process    = "new system"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
		except:
			

			print dialog_text['error_coordiantes']	
			
			self.builder.get_object('35_window_messagedialog_error').format_secondary_text(dialog_text['error_topologies/Parameters'] + fftype)
			self.window_35_message.run()
			self.window_35_message.hide()
			return 0


			"""
			fftype       = self.builder.get_object("1window_main_combobox_MM_model").get_active_text()			# combo box combox_model
			# creating a error message
			self.builder.get_object('32_window_warning_Error_message_label1').set_text(dialog_text['error_topologies/Parameters'] + fftype)
			#print "Error, the trajectory does not match with system in memory."
			# creating a error message
			#self.load_trj_windows.hide()
			a = self.window_32_warning.run() #32_window_warning_Error_message
			self.window_32_warning.hide()
			#print a
			#self.load_trj_windows.run()	
			"""
	
	
	# beta test	
	def GTKDynamo_and_Pymol_active_mode (self):
		""" Function doc """
		if self.builder.get_object("1window_main_GTKDyn_active_mode_checkbox").get_active():
			print "Using GTKDynamo in the active mode"
			data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
			pymol_object = self.project.settings['last_pymol_id']
			state    	 = -1
			label        = "tmp file"
			file_out     = "tmp.xyz"	
			filename     = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, state)	
			self.project.load_coordinate_file_to_system  ( filename , self.dualLog)	
		else:
			print "Using GTKDynamo in the passive mode"
		#self.builder.get_object('1window_main_statusbar1').push(1, pymol_object)  add item to the status bar
		#self.builder.get_object('1window_main_statusbar1').push(2, pymol_object)
		
	
	def on_1window_BUTTON_IMPORT_COORDINATES(self, button, data=None):   #"antigo   load_coords_pymol_or_file_load_it(*args)"
		data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		state    	 = int(self.builder.get_object("1window_main_import_state_from_pymol").get_text())

		
		if self.builder.get_object('1window_main_check_button_import_coord').get_active():
			filename     = self.builder.get_object('1window_main_import_coord_from_file').get_filename()
		else:
			try:
				pymol_object = self.builder.get_object('1window_main_import_coord_from_pymol').get_text()
				label        = pymol_object + " XYZ file"
				file_out     = "tmp.xyz"	
				filename     = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, state)
			except:
				pymol_object = self.builder.get_object('1window_main_import_coord_from_pymol').get_text()
				print "The PyMOL object ",pymol_object," not found"
				return 0
		
		import_type  = self.builder.get_object("1window_main_combobox_coordToSys_or_coordNewSys").get_active_text()
		
		
		
		if import_type == "Coordinates to System":
			try:
				print "importing as Coordinates to System"
				self.project.load_coordinate_file_to_system  ( filename , self.dualLog)
				self.project.settings['last_pymol_id'] = pymol_object		
				print "Done!"
				if self.builder.get_object('1window_main_check_button_import_coord').get_active(): 
					self.project.increment_step()
					# Loading the actual frame in pymol.
					self.project.export_frames_to_pymol('new', self.types_allowed , data_path)		
				
					step       =  self.project.step
					process    = "new coordiantes"
					potencial  = self.project.settings["potencial"]
					energy     = " - "
					time       = " - " 
					self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
			except:
				print dialog_text['error_coordiantes']	
				
				self.builder.get_object('35_window_messagedialog_error').format_secondary_text(dialog_text['error_coordiantes'])
				self.window_35_message.run()
				self.window_35_message.hide()
				return 0
			
		
		if import_type == "New System":
			#-------------------------------------------------------------------------------------------------------------------------------#
			# 
			#		 Message Dialog  -  when 2 buttons will be showed
			#  1 -create the warning message
			#  2 -hide the actual dialog - optional
			#  3 -show the message dialog
			#  4 -hide the message dialog
			#  5 -check the returned valor by the message dialog
			#  6 -do something
			#  7 -restore the actual dialog - optional	
			#-------------------------------------------------------------------------------------------------------------------------------#
			# creating a error message
			if self.project.system != None:
				# 1 step
				#self.builder.get_object('33_window_message_label1').set_text("Delete system in memory.")
				self.builder.get_object('33_window_messagedialog_warning').format_secondary_text(dialog_text['delete2'])
				# 2 step
				#self.load_trj_windows.hide() # hide the load_trj window
				
				# 3 step
				a = self.window_33_message.run()
				# 4 step
				self.window_33_message.hide()
				
				# 5 step
				#print a
				if a != -5:
					# 6 step
					return 0
				
				# 7 step
				#self.load_trj_windows.run()
			print "importing as a New System"
			self.project = DynamoProject()                                             # Creating a new project!!!
			self.project.load_coordinate_file_as_new_system( filename , self.dualLog)  # 
			
			if self.builder.get_object('1window_main_check_button_import_coord').get_active():
				self.project.increment_step()
				self.project.export_frames_to_pymol('new', self.types_allowed , data_path)
				
				step       =  self.project.step
				process    = "new system"
				potencial  = self.project.settings["potencial"]
				energy     = " - "
				time       = " - " 
				self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )

				print "Done!"
			else:
				print "Done!"
				self.project.increment_step()
				self.project.settings['last_pymol_id'] = pymol_object
				
	def on_1window_BUTTON_CLEAR_TABLES(self, button, data=None):
		import_type  = self.builder.get_object("1window_main_QC_FIX_PRUNE_combo").get_active_text()		
		data_path	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		
		if import_type == "FIX atoms":
			table = []
			self.project.put_fix_table(table)
			self.project.check_system(self.dualLog)   		
		if import_type == "QC region atoms":	
			table = []
			self.project.put_qc_table(table)
			print "number of atoms in the quantum region  = " + str(len(self.project.settings["qc_table"]))
					
	def on_1window_BUTTON_IMPORT_TABLES(self, button, data=None):
		import_type  = self.builder.get_object("1window_main_QC_FIX_PRUNE_combo").get_active_text()		
		data_path	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		
		if import_type == "FIX atoms":
			if  self.builder.get_object("1window_main_check_button_import_table").get_active():
				table_file   = self.builder.get_object("1window_main_import_table_from_file1").get_filename()
				table        = load_table_from_file(table_file)
				pymol_put_table(table, "FIX_atoms")
				
			else:
				try:
					pymol_selection = self.builder.get_object("1window_main_entry_fix_qc_prune").get_text()
					string22  = 'select FIX_atoms, ('+pymol_selection+ ')'
					cmd.do(string22)
					string5  = 'color grey80, FIX_atoms'
					cmd.do(string5)

					table        = pymol_get_table (pymol_selection)
				except:
					#print "Invalid PyMOL selection"
					return 0
			self.project.put_fix_table(table)
			self.project.check_system(self.dualLog)                                     # Check System
		
		if import_type == "QC region atoms":	
			if  self.builder.get_object("1window_main_check_button_import_table").get_active():
				table_file   = self.builder.get_object("1window_main_import_table_from_file1").get_filename()
				table        = load_table_from_file(table_file)
				pymol_put_table(table, "QC_atoms")
			else:
				try:
					pymol_selection = self.builder.get_object("1window_main_entry_fix_qc_prune").get_text()
					table        = pymol_get_table (pymol_selection)		
				except:
					#print "Invalid PyMOL selection"
					return 0
			self.project.put_qc_table(table)
			print "number of atoms in the quantum region  = " + str(len(self.project.settings["qc_table"]))

		if import_type == "PRUNE atoms":	
			#-------------------------------------------------------------------------------------------------------------------------------#
			# 
			#		 Message Dialog  -  when 2 buttons will be showed
			#  1 -create the warning message
			#  2 -hide the actual dialog - optional
			#  3 -show the message dialog
			#  4 -hide the message dialog
			#  5 -check the returned valor by the message dialog
			#  6 -do something
			#  7 -restore the actual dialog - optional	
			#-------------------------------------------------------------------------------------------------------------------------------#
			# creating a error message

			# 1 step
			#self.builder.get_object('33_window_message_label1').set_text("This is an irreversible process.")
			self.builder.get_object('33_window_messagedialog_warning').format_secondary_text(dialog_text['prune'])
			
			# 2 step
			#self.load_trj_windows.hide() # hide the load_trj window
			
			# 3 step
			a = self.window_33_message.run()
			# 4 step
			self.window_33_message.hide()
			
			# 5 step
			#print a
			if a != -5:
				# 6 step
				return 0
			
			# 7 step
			#self.load_trj_windows.run()
		
			#-------------------------------------------------------------------------------------------------------------------------------#			
			if  self.builder.get_object("1window_main_check_button_import_table").get_active():
				table_file   = self.builder.get_object("1window_main_import_table_from_file1").get_filename()
				table        = load_table_from_file(table_file)
			else:
				try:
					pymol_selection = self.builder.get_object("1window_main_entry_fix_qc_prune").get_text()
					table        = pymol_get_table (pymol_selection)		
				except:
					#print "Invalid PyMOL selection"
					return 0
			self.project.put_prune_table(table)                                         # prune
			self.project.increment_step()                                               # step
			self.project.check_system(self.dualLog)                                     # Check System
			self.project.export_frames_to_pymol('prn', self.types_allowed , data_path)	# Loading the actual frame in pymol.		
			#JOB HISTORY
			step       =  self.project.step
			process    = "prune system"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
	
	"""		
	def on_1window_COBOBOX_SET_QC_METHOD(self, button, data=None):
		DFT = ["DFT - demon, lda, 321g",
				"DFT - demon, blyp, 321g",
				"DFT - ahlrichs, lda, 631gs",
				"DFT - ahlrichs, blyp, 631gs",
				"DFT - weigend, lda, svp",
				"DFT - weigend, blyp, svp"]
		
		qc_method       = self.builder.get_object('1window_main_qc_method_combobox').get_active_text()
		if qc_method in DFT:
			self.builder.get_object('1window_main_label58').set_sensitive(True)
			self.builder.get_object('1window_main_label77').set_sensitive(True)
			self.builder.get_object('1window_main_density_tol').set_sensitive(True)
			self.builder.get_object('1window_main_Maximum_SCF').set_sensitive(True)
		else:
			self.builder.get_object('1window_main_label58').set_sensitive(False)
			self.builder.get_object('1window_main_label77').set_sensitive(False)
			self.builder.get_object('1window_main_density_tol').set_sensitive(False)
			self.builder.get_object('1window_main_Maximum_SCF').set_sensitive(False)				
	"""
	
	def on_1window_BUTTON_SET_QC_PARAMS(self, button, data=None):  #"old   set_qc_parameters(*args):"	density_tol = App.get_object('density_tol').get_text()


		if self.project.system == None:
			return "system empty"
		#-------------------------------------------------------------------------------------------------------------------------------#
		# 
		#		 Message Dialog  -  when 2 buttons will be showed
		#  1 -create the warning message
		#  2 -hide the actual dialog - optional
		#  3 -show the message dialog
		#  4 -hide the message dialog
		#  5 -check the returned valor by the message dialog
		#  6 -do something
		#  7 -restore the actual dialog - optional	
		#-------------------------------------------------------------------------------------------------------------------------------#
		
		

		# creating a error message
		qc_table      = self.project.settings['qc_table']
		if qc_table == []:
			# 1 step
			#self.builder.get_object('33_window_message_label1').set_text("You have no atoms in your QC_list, would you like\nto add all the atoms of your system to the QC region.")
			self.builder.get_object('34_window_messagedialog_question').format_secondary_text(dialog_text['qc_region'])
			
			# 2 step
			#self.load_trj_windows.hide() # hide the load_trj window
			
			# 3 step
			a = self.window_34_message.run()
			# 4 step
			self.window_34_message.hide()
			
			
			# possible "a" valors 
			#	-8  -  yes
			#	-9  -  no
			#	-4  -  close
			#   -5  -  OK
			#   -6  -  Cancel
			
			
			# 5 step
			#print a
			if a == -8:
				# 6 step
				b = None
			else:
				return 0
			# 7 step
			#self.load_trj_windows.run()
		
		#-------------------------------------------------------------------------------------------------------------------------------#
		qc_method       = self.builder.get_object('1window_main_qc_method_combobox').get_active_text()

		density_tol     = self.builder.get_object('1window_main_density_tol').get_text()
		Maximum_SCF     = self.builder.get_object('1window_main_Maximum_SCF').get_text()
		
		charge          = self.builder.get_object('1window_main_entry_chrg').get_value_as_int()
		multiplicity    = self.builder.get_object('1window_main_entry_mult').get_value_as_int()
		
		selection       = self.builder.get_object('1window_main_entry_fix_qc_prune').get_text()
		
		converger       = DIISSCFConverger ( densityTolerance = float(density_tol), maximumSCFCycles = int(Maximum_SCF) ) # only DFT methods
		qc_table        = self.project.settings['qc_table']
		nbModel         = self.project.settings['nbModel']
		
		orca_string     = self.builder.get_object('6_window_entry_keywords').get_text()
		
		self.project.settings['qc_method']     = qc_method
		self.project.settings['charge']        = charge
		self.project.settings['multiplicity']  = multiplicity	
		

		
		if  qc_method[0:3]  == 'DFT':
			self.project.settings['density_tol']  = density_tol
			self.project.settings['Maximum_SCF']  = Maximum_SCF

		if qc_method in self.mndo_list:
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
		'''
		if qc_method   == "am1":
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
		elif qc_method == "rm1":	
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)		
		elif qc_method == "pm3":	
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
		elif qc_method == "pm6":	
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
		
		elif qc_method == "chops":
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
			
		elif qc_method == "pddg":
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
		elif qc_method == "pddg/pm3":
			self.project.set_qc_parameters_MNDO(qc_method, charge, multiplicity, qc_table, self.dualLog)
		'''

		if qc_method == "DFT - demon, lda, 321g":	
			densityBasis  = "demon"
			functional   = "lda"
			orbitalBasis = "321g"
			self.project.set_qc_parameters_DFT( qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis,self.dualLog)
			
		elif qc_method == "DFT - demon, blyp, 321g":	
			densityBasis  = "demon"
			functional   = "blyp"
			orbitalBasis = "321g"			
			self.project.set_qc_parameters_DFT( qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis,self.dualLog)
			
					
		elif qc_method == "DFT - ahlrichs, lda, 631gs":	
			densityBasis = "ahlrichs"
			functional   = "lda"
			orbitalBasis = "631gs" 
			self.project.set_qc_parameters_DFT( qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis,self.dualLog)
		
		elif qc_method == "DFT - ahlrichs, blyp, 631gs":	
			densityBasis = "ahlrichs"
			functional   = "blyp"
			orbitalBasis = "631gs"
			self.project.set_qc_parameters_DFT( qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis,self.dualLog)


		elif qc_method == "DFT - weigend, lda, svp":	
			densityBasis = "weigend"
			functional   = "lda"
			orbitalBasis = "svp" 
			self.project.set_qc_parameters_DFT( qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis,self.dualLog)
		
		elif qc_method == "DFT - weigend, blyp, svp":	
			densityBasis = "weigend"
			functional   = "blyp"
			orbitalBasis = "svp"
			self.project.set_qc_parameters_DFT( qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis,self.dualLog)
		
		if qc_method == "ORCA - ab initio":

			ORCA_pal 	= self.builder.get_object('6_window_SpinButton1_ORCA_pal').get_value_as_int()
			ORCA_method = self.builder.get_object('6_window_combobox1_ORCA_method').get_active_text()
			ORCA_SCF    = self.builder.get_object('6_window_combobox2_ORCA_SCF').get_active_text()
			ORCA_basis  = self.builder.get_object('6_window_combobox3_ORCA_basis').get_active_text()

			self.project.settings['ORCA_method']    = ORCA_method
			self.project.settings['ORCA_SCF']       = ORCA_SCF
			self.project.settings['ORCA_basis']     = ORCA_basis
			self.project.settings['ORCA_pal']       = ORCA_pal
			
			#self.project.set_qc_parameters_ORCA(qc_method, charge, multiplicity, qc_table, ORCA_method, ORCA_SCF, ORCA_basis, ORCA_pal,self.dualLog )
			self.project.set_qc_parameters_ORCA(qc_method, charge, multiplicity, qc_table, orca_string, ORCA_pal, self.dualLog )

		if self.project.settings['qc_table'] != []:
			cmd.set ('sphere_scale'     , self.sphere_scale)
			cmd.set ('stick_radius'     , self.stick_radius)
			cmd.set ('label_distance_digits', self.label_distance_digits)			
			cmd.set ('mesh_width',       self.mesh_width )
			#cmd.select(string name, string selection)
			#string2  = 'select QC_atoms, ('+ selection + ')'
			try:
				last_pymol_id = self.project.settings['last_pymol_id']
				cmd.hide("stick", last_pymol_id)
				cmd.hide("sphere", last_pymol_id)

				#pymol_put_table (self.project.settings['qc_table'], 'QC_atoms')
				cmd.select('QC_atoms', selection)
				cmd.show( "stick", "QC_atoms" )
				cmd.show( "sphere", "QC_atoms" )

				#cmd.select('QC_atoms', last_pymol_id)
				#cmd.show( "stick", "QC_atoms" )
				#cmd.show( "sphere", "QC_atoms" )					
			except:
				a = None

		if self.project.settings['qc_table'] == []:
			
			self.project.settings['qc_table']  = ( self.project.system.energyModel.qcAtoms.QCAtomSelection ( ) )
			cmd.set ('sphere_scale'     , self.sphere_scale)
			cmd.set ('stick_radius'     , self.stick_radius)
			cmd.set ('label_distance_digits', self.label_distance_digits)			
			cmd.set ('mesh_width',       self.mesh_width )
			last_pymol_id = self.project.settings['last_pymol_id']
			
			#cmd.select(string name, string selection)
			#string2  = 'select QC_atoms, ('+ selection + ')'
			try:
				cmd.show("stick",last_pymol_id)
				cmd.show("sphere" ,last_pymol_id)
			except:
				a = None

			
	def on_1window_BUTTON_SAVE_DATA_PATH(self, button, data=None):  #"old   save_config_file"
		data_path  	 	= self.builder.get_object("1window_main_dataPath_finder").get_filename()
		try:
			self.project.settings['data_path'] = data_path 
		except:
			a = None
		self.builder.get_object('1window_main_entry_prmtop').set_current_folder(data_path)				#
		self.builder.get_object('1window_main_entry_crd').set_current_folder(data_path)
		self.builder.get_object('1window_main_entry_prm_opls').set_current_folder(data_path)				#on_1window_BUTTON_SAVE_DATA_PATH
		self.builder.get_object('1window_main_xyzc').set_current_folder(data_path)
		self.builder.get_object('5_window_traj_name').set_current_folder(data_path)

		#self.builder.get_object('1window_main_load_QC_table_entry').set_current_folder(data_path)
		#self.builder.get_object('1window_main_load_fix_table_chooser_button').set_current_folder(data_path)
		
		self.builder.get_object('17_window_SAVE_FRAME_directory_save_file').set_current_folder(data_path)
		self.builder.get_object('12_window_traj_name_charges').set_current_folder(data_path)
		#self.builder.get_object('11_window_filechooserbutton1_prune').set_current_folder(data_path)
		self.builder.get_object('14_window_filechooserbutton1').set_current_folder(data_path)
		self.builder.get_object('5_window_traj_name').set_current_folder(data_path)
		
		
		
		
		self.builder.get_object('7_window_filechooserbutton_REACTANTS').set_current_folder(data_path)
		self.builder.get_object('7_window_filechooserbutton_PRODUCTS').set_current_folder(data_path)
		self.builder.get_object('8_window_directory_surface_file').set_current_folder(data_path)
		
		self.save_config_file()

	def on_1window_TOOLBAR_OPEN_NEW_PROJECT(self, data = None):    # old "open_load_pymol_session_dialog"
		result = self.new_prjct_window.run()
		self.new_prjct_window.hide()	
	





	def on_1window_TOOLBAR_OPEN_SAVE_PROJECT(self, data = None):    # old "open_load_pymol_session_dialog
		if self.project.system == None:
			print 'system empty'
			return 0
		
		if self.project_name == None:
			try:
				filename = self.get_save_filename()   # apenas um teste
				data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
				self.project.settings['data_path'] = data_path
				self.project_name = filename
				self.project.export_GTKDynamo_session_to_file(filename)
				print "\n\nSaving process successful - ", self.project_name + ".gtkdyn"
				print "\n\nSaving process successful - ", self.project_name+ ".pkl"
				print "\n\nSaving process successful - ", self.project_name+ ".pse"
			except:
				return 0
		else:
			
			try:
				#filename = self.get_save_filename()   
				#data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
				#self.project.settings['data_path'] = data_path 
				self.project.export_GTKDynamo_session_to_file(self.project_name)
				print "\n\nSaving process successful - ", self.project_name + ".gtkdyn"
				print "\n\nSaving process successful - ", self.project_name+ ".pkl"
				print "\n\nSaving process successful - ", self.project_name+ ".pse"		
			except:
				return 0

		
		
		
	def on_1window_TOOLBAR_OPEN_SAVE_AS_PROJECT(self, data = None):   
		if self.project.system == None:
			print 'system empty'
			return 0
		try:
			filename = self.get_save_filename()
			data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
			self.project.settings['data_path'] = data_path
			
			"""---------------------------------checks if the files already exist-------------------------------"""
			
			"""                                                                                                   """
			
			# just grab the full path and deletes the file name ex: /home/fernando/myproject  -> /home/fernando/
			fullpath     = filename.split("/")
			fileNAME     = fullpath.pop(-1)
			fullPATH     = ""
			for i in fullpath:
				fullPATH = fullPATH + i
				fullPATH = fullPATH + "/"
			
			# check if already exist an file with the same name in the directory where the project will be saved
			file1 = fileNAME + '.gtkdyn' 				#
			file2 = fileNAME + '.pkl'    				# file that will be generated
			file3 = fileNAME + '.pse'    				#
			
			
			filelist = os.listdir(fullPATH) # list of the files directory
			
			#if file1 in filelist:
			#	print 'the ' + fileNAME + '.gtkdyn' + " already existes. Replace it?"
				
			#	asn = input('Yes/No: ')
			
			"""----------------------------------------------------------------------------------------------------"""	
			
			
			 
			self.project.export_GTKDynamo_session_to_file(filename)
			self.project_name = filename
			print "\n\nSaving process successful - ", self.project_name + ".gtkdyn"
			print "\n\nSaving process successful - ", self.project_name+ ".pkl"
			print "\n\nSaving process successful - ", self.project_name+ ".pse"	
		except:
			return 0
		
		
		
				
	def on_1window_TOOLBAR_RUN_CHECK_SYSTEM(self, data = None):
		# Check System
		try:
			self.project.check_system(self.dualLog)
		except:
			print "system empty"
			
	def on_1window_TOOLBAR_RUN_SINGLE_POINT(self, data = None):
		try:
			self.GTKDynamo_and_Pymol_active_mode ()
			#---------------------- log back up -----------------------#
			self.project.system.Summary ( self.dualLog )			   #
			os.rename("log.gui.txt", "log.gui.old")					   # 
			self.project.system.Summary ( self.dualLog )			   # 
			#----------------------------------------------------------#
			
			
				
			data_path  	  = self.builder.get_object("1window_main_dataPath_finder").get_filename()												
			print "\n\n------------------------- Step Number - " + str(self.project.step +1 )  + " Single Point -------------------------"

			energy, time  = self.project.check_energy(data_path, self.dualLog)
			self.project.increment_step()

			
			#----------------------------------------------- log back up -------------------------------------------#
			tmp         = data_path+"/tmp"                              #  temporary folder                         #
			if not os.path.exists ( tmp ): os.mkdir ( tmp )             #  checks if already exist an tmp directory #
																													#
			os.rename("log.gui.txt",  data_path+ "/tmp/step_" + str(self.project.step) + "_single_point.log")	    #
			print "Saving log file:   ", data_path+ "/tmp/step_" + str(self.project.step) + "_single_point.log"     #																		                            #
			#-------------------------------------------------------------------------------------------------------#
			
			self.builder.get_object('36_window_messagedialog_info').format_secondary_text("Energy = " + str(energy) + "kj/mol" )
			self.window_36_message.run()
			self.window_36_message.hide()
				
			""" exemple
			------------------------- Step Number - 4 Single Point -------------------------

			-------------------------- ABFS NB Model State Summary -------------------------
			MM/MM Pairs            =            634  MM/MM 1-4 Pairs        =             91
			--------------------------------------------------------------------------------

			--------------------------------- Summary of Energy Terms --------------------------------
			Potential Energy          =        -495.7684  RMS Gradient              =             None
			Harmonic Bond             =          51.6260  Fourier Improper          =           0.5854
			Harmonic Angle            =         152.2608  Fourier Dihedral          =          90.2797
			MM/MM Elect.              =        1828.0685  MM/MM LJ                  =          -7.9054
			MM/MM 1-4 Elect.          =       -2651.8545  MM/MM 1-4 LJ              =          41.1710
			------------------------------------------------------------------------------------------
			Total time = :  0.00289607048035
			Total energy = :  -495.76840443
			"""
			
			
			
			"""
			try:
				SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
				data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
				tmp_path = data_path + '/tmp'
				if not os.path.exists( tmp_path ): 
					os.mkdir(tmp_path)
					
				os.rename(SCRATCH + "/job.out", tmp_path+'/orca_step' + str(self.project.step) + ".out" )
				print "Saving orca output: ",  tmp_path+'/orca_step' + str(self.project.step) + ".out"
			except:
				a = None
			"""
			
			# JOB HISTORY
			step           = self.project.step
			potencial      = self.project.settings['potencial']
			process        = "single point"
			
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
		except:
			print "System empty"
	def on_1window_TOOLBAR_OPEN_MINIMIZATION_DIALOG(self, widget, data = None):   #   O P E N      MINIMIZATION  WINDOW
		text = "step_"+str(self.project.step + 1 )+"_minimization"
		self.builder.get_object('2_window_entry_traj_name').set_text(text)		
		self.min_windows.run()
		self.min_windows.hide()

	def on_1window_TOOLBAR_OPEN_MOLECULAR_DYNAMICS_DIALOG(self, data = None):
		text = "step_"+str(self.project.step +1 )+"_molecular_dynamics"
		self.builder.get_object('3_windowentry_trajectory_name').set_text(text)
		self.dyn_windows.run()
		self.dyn_windows.hide()
		
	def on_1window_TOOLBAR_OPEN_TRAJECTORY_TOOL_WINDOW(self, data = None):
		if self.TrajectoryTool == False:
			window = window_4_trajectory_tool()
			window.show()
			self.TrajectoryTool = True
			#return "window2 open"

		"""
		if self.TrajectoryTool == True:
			self.builder.get_object('4_window_trajectory_tool').hide()
			self.TrajectoryTool = False

		elif self.TrajectoryTool == False:
			self.TrajectoryTool = True
			self.builder.get_object('4_window_trajectory_tool').show()
		"""

	def on_1window_TOOLBAR_RUN_DELETE_SYSTEM(self, data = None):

		#-------------------------------------------------------------------------------------------------------------------------------#
		# 
		#		 Message Dialog  -  when 2 buttons will be showed
		#  1 -create the warning message
		#  2 -hide the actual dialog - optional
		#  3 -show the message dialog
		#  4 -hide the message dialog
		#  5 -check the returned valor by the message dialog
		#  6 -do something
		#  7 -restore the actual dialog - optional	
		#-------------------------------------------------------------------------------------------------------------------------------#
		# creating a error message
		if self.project.system != None:
			# 1 step
			#self.builder.get_object('33_window_message_label1').set_text("Delete the system in memory?")
			self.builder.get_object('33_window_messagedialog_warning').format_secondary_text(dialog_text['delete2'])
			# 2 step
			#self.load_trj_windows.hide() # hide the load_trj window
			
			# 3 step
			a = self.window_33_message.run()
			
			# 4 step
			self.window_33_message.hide()
			
			# 5 step
			#print a
			if a == -5:
				# 6 step
				b = None
			else:
				return 0
			
			# 7 step
			#self.load_trj_windows.run()
		
		#-------------------------------------------------------------------------------------------------------------------------------#


		self.project = DynamoProject()
		self.project_name = None
		cmd.reinitialize()
		cmd.set ('sphere_scale'     , self.sphere_scale)
		cmd.set ('stick_radius'     , self.stick_radius)
		cmd.set ('label_distance_digits', self.label_distance_digits)
		cmd.set ('mesh_width',       self.mesh_width )
		cmd.set ("retain_order") # keep atom ordering
		
	def on_1window_COMBOBOX_MM_MODEL_CHANGE(self, menuitem, data=None):  # combobox event 
		fftype = self.builder.get_object("1window_main_combobox_MM_model").get_active_text()
		
		if fftype == "AMBER":
			self.builder.get_object("1window_main_xyzc").hide()
			self.builder.get_object("1window_main_entry_prm_opls").hide()
			self.builder.get_object("1window_main_entry_prmtop").show()
			self.builder.get_object("1window_main_chm_crd_label1").hide()
			
			self.builder.get_object('1window_main_prm_top_label').set_text("AMBER Param/ Topol file:")
			self.builder.get_object('1window_main_psfx_crd_label').set_text("AMBER Coordinates File:")
	
		if fftype == "CHARMM":
			self.builder.get_object("1window_main_xyzc").show()
			self.builder.get_object("1window_main_entry_prm_opls").hide()
			self.builder.get_object("1window_main_entry_prmtop").show()
			self.builder.get_object("1window_main_chm_crd_label1").show()
			
			self.builder.get_object('1window_main_prm_top_label').set_text("CHARMM Parameters:")
			self.builder.get_object('1window_main_psfx_crd_label').set_text("CHARMM Topology:")

		if fftype == "GROMACS":
			self.builder.get_object("1window_main_xyzc").hide()
			self.builder.get_object("1window_main_entry_prm_opls").hide()
			self.builder.get_object("1window_main_entry_prmtop").show()
			self.builder.get_object("1window_main_chm_crd_label1").hide()
			
			self.builder.get_object('1window_main_prm_top_label').set_text("GROMACS Param/Topol file (AMBER/CHARMM/OPLS):")
			self.builder.get_object('1window_main_psfx_crd_label').set_text("GROMACS Coordinate file (gro):")
		
		if fftype == "OPLS":
			self.builder.get_object("1window_main_xyzc").hide()
			self.builder.get_object("1window_main_entry_prm_opls").show()
			self.builder.get_object("1window_main_entry_prmtop").hide()
			self.builder.get_object("1window_main_chm_crd_label1").hide()
			
			self.builder.get_object('1window_main_prm_top_label').set_text("OPLS Param/Topol folder:")
			self.builder.get_object('1window_main_psfx_crd_label').set_text("OPLS Coordinates:")

	def on_1window_COMBOBOX_CHECK_QC_PARAMETERS(self, menuitem, data=None):
		DFT = ["DFT - demon, lda, 321g",
				"DFT - demon, blyp, 321g",
				"DFT - ahlrichs, lda, 631gs",
				"DFT - ahlrichs, blyp, 631gs",
				"DFT - weigend, lda, svp",
				"DFT - weigend, blyp, svp"]
		
		qc_method       = self.builder.get_object('1window_main_qc_method_combobox').get_active_text()
		if qc_method in DFT:
			self.builder.get_object('1window_main_label58').set_sensitive(True)
			self.builder.get_object('1window_main_label77').set_sensitive(True)
			self.builder.get_object('1window_main_density_tol').set_sensitive(True)
			self.builder.get_object('1window_main_Maximum_SCF').set_sensitive(True)
		else:
			self.builder.get_object('1window_main_label58').set_sensitive(False)
			self.builder.get_object('1window_main_label77').set_sensitive(False)
			self.builder.get_object('1window_main_density_tol').set_sensitive(False)
			self.builder.get_object('1window_main_Maximum_SCF').set_sensitive(False)


		method = self.builder.get_object('1window_main_qc_method_combobox').get_active_text()
		if method == "ORCA - ab initio":
			self.setupORCA_window.run()
			self.setupORCA_window.hide()
			print "ORCA Method"
		else:
			a = None	
			print "pDynamo Method"
			
	def on_1window_COMBOBOX_CHANGE_QC_FIX_PRUNE(self, menuitem, data=None):
		""" Function doc """
		
		import_type =   self.builder.get_object("1window_main_QC_FIX_PRUNE_combo").get_active_text()


		if import_type == "FIX atoms":
			self.builder.get_object("1window_main_image_FIX_QC_PRUNE").set_from_file("lock3_50_50.png")
		
		if import_type == "QC region atoms":	
			self.builder.get_object("1window_main_image_FIX_QC_PRUNE").set_from_file("h2o3_50_50.png")
		
		if import_type == "PRUNE atoms":	
			self.builder.get_object("1window_main_image_FIX_QC_PRUNE").set_from_file("scissors3.png")

	def on_1window_CHECKBUTTON_IMPORT_COORDINATES(self, checkbutton, data=None):
		if self.builder.get_object("1window_main_check_button_import_coord").get_active():
			self.builder.get_object("1window_main_import_coord_from_file").show()
			self.builder.get_object("1window_main_import_coord_from_pymol").hide()
			self.builder.get_object("1window_main_label_frame").hide()
			self.builder.get_object("1window_main_import_state_from_pymol").hide()
			
		else:
			self.builder.get_object("1window_main_import_coord_from_file").hide()
			self.builder.get_object("1window_main_import_coord_from_pymol").show()
			self.builder.get_object("1window_main_label_frame").show()
			self.builder.get_object("1window_main_import_state_from_pymol").show()

	def on_1window_CHECKBUTTON_PDB_XYZ_MOL2_FILE_TYPES(self, checkbutton, data=None):
		if self.builder.get_object("1window_main_xyz_check_box").get_active():
			self.types_allowed['xyz'] = True
		else: 
			self.types_allowed['xyz'] = False
		
		if self.builder.get_object("1window_main_pdb_check_box").get_active():
			self.types_allowed['pdb'] = True
		else:
			self.types_allowed['pdb'] = False
		
		if self.builder.get_object("1window_main_mol2_check_box").get_active():
			self.types_allowed['mol2'] = True
		else:
			self.types_allowed['mol2'] = False

	def on_1window_CHECKBUTTON_IMPORT_TABLE_FROM_FILE(self, checkbutton, data=None):
		if self.builder.get_object("1window_main_check_button_import_table").get_active():
			self.builder.get_object("1window_main_import_table_from_file1").show()
			self.builder.get_object("1window_main_entry_fix_qc_prune").hide()
			self.builder.get_object("1window_main_label7_entry_fix_qc_prune").set_text("File in: ")
			#self.builder.get_object("1window_main_label_frame").hide()
			#self.builder.get_object("1window_main_import_state_from_pymol").hide()
			
		else:
			self.builder.get_object("1window_main_import_table_from_file1").hide()
			self.builder.get_object("1window_main_entry_fix_qc_prune").show()
			self.builder.get_object("1window_main_label7_entry_fix_qc_prune").set_text("Pymol selection: ")

	#==============================#			
	# -  2_window - minimization   #
	#==============================#

	def on_2window_BUTTON_RUN_MINIMIZATION(self, button, data=None):
		data_path  	 	      = self.builder.get_object("1window_main_dataPath_finder").get_filename()												
		trajectory_name       = self.builder.get_object("2_window_entry_traj_name").get_text()
		
		max_int               = int(self.builder.get_object("2_window_entry_max_int").get_text())
		log_freq              = int(self.builder.get_object("2_window_entry_log_freq").get_text())
		trajectory_freq       = int(self.builder.get_object("2_window_entry_traj_freq").get_text())
		rms_grad              = float(self.builder.get_object("2_window_entry_rmsGRAD").get_text())
		min_method			  = "Conjugate Gradient"
		
		
		
		method                = self.builder.get_object("2_window_mim_Method_box").get_active_text()

		
		output_traj_flag      = False
		if self.builder.get_object('2_window_Output_trajectory_checkbox').get_active():
			output_traj_flag      = True
			print "output_traj_flag = True"
		amber_traj_flag       = False
		if self.builder.get_object('2_window_AMBER_trajectory_checkbox').get_active():
			amber_traj_flag       = True
			print "amber_traj_flag = True"

		
		#-------------------------------------#
		#   minimization_Conjugate Gradient   #
		#-------------------------------------#		
		self.GTKDynamo_and_Pymol_active_mode () #BETA
		
		
		if method == 'Conjugate Gradient':
			x, y, t = self.project.run_minimization (data_path, 
													trajectory_name, 
													max_int, 
													log_freq, 
													trajectory_freq, 
													rms_grad, 
													min_method, 
													output_traj_flag, 
													amber_traj_flag,	
													self.dualLog)
		
		
		#-----------------------------------#
		#   minimization_Steepest_Descent   #
		#-----------------------------------#		
		
		if method == 'Steepest Descent':
			functionStep      = 2.0
			pathStep          = 0.025
			x, y, t = self.project.run_minimization_Steepest_Descent (
																	data_path       ,
																	trajectory_name ,

																	functionStep    ,
																	pathStep        ,   
																	max_int         ,   # maximun number of interactions 

																	log_freq        ,   # print log frequence
																	trajectory_freq ,   # Trajectory frequence
																	rms_grad        ,
																	min_method      ,
																	output_traj_flag,   # save trajectory yes - no ?
																	amber_traj_flag ,   # amber output traj
																	self.dualLog)

		
		print "total time = ", t
		
		self.project.increment_step()
		
		self.project.export_frames_to_pymol('min', self.types_allowed , data_path)
		
		self.min_windows.hide()  #  I M P O R T A N T E , se nao a janela nao fecha.
			
		# JOB HISTORY
		time = t
		energy = y[-1]
		step           = self.project.step
		potencial      = self.project.settings['potencial']
		process        = "minimization"
		
		self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
		
		#plot_plot()
		self.render_plot( x, y)

	#====================================#		
	# -  3_window - Molecular Dynamics   #
	#====================================#

	def on_3window_BUTTON_RUN_DYNAMICS(self, button, data=None):
		data_path  	 	  = self.builder.get_object("1window_main_dataPath_finder").get_filename()												
		trajectory_name   = self.builder.get_object("3_windowentry_trajectory_name").get_text()
		nsteps            = int(self.builder.get_object('3_windown_steps_dy').get_text())
		log_freq          = int(self.builder.get_object("3_windowentry_log_freq_dy").get_text())
		trajectory_freq   = int(self.builder.get_object("3_windowentry_traj_freq_dy").get_text())
		timestep          = float(self.builder.get_object('3_window_timestep').get_text())
		method            = self.builder.get_object("3_windowDynamics_Method_box").get_active_text()
		seed              = int(self.builder.get_object('3_windowentry_seed_dy').get_text())
		temperature       = int(self.builder.get_object('3_window_temperature').get_text())
		temp_scale_freq   = int(self.builder.get_object('3_window_temp_scale_freq').get_text())
		coll_freq         = int(self.builder.get_object('3_window_collision_frequency').get_text())
		dualLog           = self.dualLog
		
		self.GTKDynamo_and_Pymol_active_mode () #BETA
		
	
		output_traj_flag      = False
		if self.builder.get_object('3_windowOutput_trajectory_checkbox1').get_active():
			output_traj_flag      = True
		
		amber_traj_flag       = False
		if self.builder.get_object('3_windowAMBER_trajectory_checkbox1').get_active():
			amber_traj_flag       = True
		

		self.project.run_dynamics(data_path,
								trajectory_name,
								nsteps,
								log_freq,
								trajectory_freq,
								timestep,
								method,
								seed,
								temperature,
								temp_scale_freq,
								coll_freq,
								dualLog)
		
		
		self.project.increment_step()
		
		self.project.export_frames_to_pymol('dyn', self.types_allowed , data_path)
		
		self.dyn_windows.hide()  #  I M P O R T A N T E , se nao a janela nao fecha.

		# J O B    H I S T O R Y
		step       =  self.project.step
		process    = "molecular Dynamics"
		potencial  = self.project.settings["potencial"]
		energy     = " - "
		time       = " - " 
		self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
			
	def on_3window_COMBOBOX_MD_METHODS_CHANGE(self, menuitem, data=None):  # combobox event 
		method = self.builder.get_object("3_windowDynamics_Method_box").get_active_text()
		
		if method == "Velocity Verlet Dynamics":
			self.builder.get_object("3_window_collision_frequency").hide()
			self.builder.get_object("3_windowlabel68_collision_freq").hide()

		elif method == "Leap Frog Dynamics":
			self.builder.get_object("3_window_collision_frequency").hide()
			self.builder.get_object("3_windowlabel68_collision_freq").hide()

		elif method == "Langevin Dynamics":
			self.builder.get_object("3_window_collision_frequency").show()
			self.builder.get_object("3_windowlabel68_collision_freq").show()

	#===================================#
	# -     4_window_-                - #
	#===================================#
	
	def on_4window_BARSET_SETFRAME (self,hscale,text= None,  data=None):            # SETUP  trajectory window
		valor =hscale.get_value()
		cmd.frame( int (valor) )
	
	def on_4window_ENTRY_PUSH(self, entry, data=None):
		MAX  = int(self.builder.get_object('4_window_max_hset').get_text())
		MIN  = int(self.builder.get_object('4_window_min_hset').get_text())

		scale = self.builder.get_object("4_window_hscale1")
		scale.set_range(MIN, MAX)
		scale.set_increments(1, 10)
		scale.set_digits(0)	

	def on_4window_COMBOX_OBJ_TRAJECTORY(self, menuitem, data=None):    #  remover
		pymol_items = cmd.get_names()
		print pymol_items
		builder = self.builder
		cbox = builder.get_object('4_window_combobox1')   #  ----> combobox_MM_model
		store = gtk.ListStore(gobject.TYPE_STRING)
		store.clear()
		cbox.set_model(store )
		for i in pymol_items:		
			cbox.append_text(i)
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		
	
	#================================#		
	# -  5_window_Load_traj_window	 #	
	#================================#	

	def on_5window_BUTTON_LOAD_TRAJETORY(self, button, data=None):
		try:
			traj_name        = self.builder.get_object('5_window_traj_name').get_filename()
			new_pymol_object = self.builder.get_object('5_window_Load_traj_entry').get_text()
			
			
			first            = int(self.builder.get_object('5_window_first').get_text())
			last             = int(self.builder.get_object('5_window_last').get_text())
			stride           = int(self.builder.get_object('5_window_stride').get_text())
			export_type      = "xyz"
			
			if self.builder.get_object('5_window_load_trajectory_pdb_checkbox').get_active():
				export_type  = 'pdb'
				
			self.project.load_trajectory_to_system(first, last, stride, traj_name, new_pymol_object, export_type)
			self.load_trj_windows.hide()
			
			if self.project.settings['qc_table'] != []:
				cmd.set ('sphere_scale'     , self.sphere_scale)
				cmd.set ('stick_radius'     , self.stick_radius)
				cmd.set ('label_distance_digits', self.label_distance_digits)
				
				pymol_put_table  (self.project.settings['qc_table'], "QC_atoms")
				string   = 'select QC_atoms ('+new_pymol_object+ ' and  QC_atoms )'
				cmd.do(string)

				cmd.show( "stick",  "QC_atoms" )
				cmd.show( "sphere", "QC_atoms" )

		except:
			# alert Dialog     -  when only one button will be showed
			
			# creating a error message
			#self.builder.get_object('32_window_warning_Error_message_label1').set_text("Error, the trajectory does not match with system in memory.")
			
			self.builder.get_object('35_window_messagedialog_error').format_secondary_text(dialog_text['error_trajectory'])
			#self.window_35_message.run()
			#self.window_35_message.hide()
			
			#print "Error, the trajectory does not match with system in memory."
			# creating a error message
			self.load_trj_windows.hide()
			a = self.window_35_message.run() #32_window_warning_Error_message
			self.window_35_message.hide()
			#print a
			self.load_trj_windows.run()			
			
			
			
			'''
			# Message Dialog  -  when 2 buttons will be showed
		
			
			# creating a error message
			self.builder.get_object('33_window_message_label1').set_text("Error, the trajectory does not match with system in memory.")
			self.load_trj_windows.hide() # hide the load_trj window
			
			a = self.window_33_message.run()
			self.window_33_message.hide()
			print a
			if a == -5:
				print "gordao"
			self.load_trj_windows.run()
			
			'''


	
	def on_5_return_ok (self, button, data=None):
		self.window_32_warning.destroy()
		return 1
	#============================#
    #        7_window_ORCA       #
	#============================#
	
	def on_6window_check_paramaters (self, button, data=None):
		""" Function doc """
		try:
			orca_method = self.builder.get_object("6_window_combobox1_ORCA_method").get_active_text()
			orca_scf    = self.builder.get_object("6_window_combobox2_ORCA_SCF").get_active_text()
			orca_basis  = self.builder.get_object("6_window_combobox3_ORCA_basis").get_active_text()
			orca_pol    = self.builder.get_object("6_window_combobox2_ORCA_POLARIZATION").get_active_text()
			orca_diff   = self.builder.get_object("6_window_combobox2_ORCA_DIFFUSE").get_active_text()
			
			orca_restriciton = None
			
			if  self.builder.get_object("6_window_ORCA_radiobutton_restrict").get_active():
				if orca_method in self.KS_list:
					orca_restriciton = "RKS"
				if orca_method in self.HF_list:
					orca_restriciton = "RHF"
		
			if  self.builder.get_object("6_window_ORCA_radiobutton_unrestrict").get_active():
				if orca_method in self.KS_list:
					orca_restriciton = "UKS"
				if orca_method in self.HF_list:
					orca_restriciton = "UHF"
			
			orca_method2 = orca_method.split()
			orca_method2 = orca_method2[0]
				
			orca_basis2 = orca_basis.split()
			orca_basis2 = orca_basis2[0]
			
			if orca_diff != "No":
				orca_basis2 = orca_basis2.split("G")
				orca_basis2 = orca_basis2[0] + orca_diff + "G"
			if orca_pol != "No":
				orca_basis2 = orca_basis2 + orca_pol
				
			orca_string = orca_method2 +' '+ orca_basis2 +' '+ orca_scf +' '+ orca_restriciton +' CHELPG'
			
			self.builder.get_object("6_window_entry_keywords").set_text(orca_string)
		except:
			return 0
		#print orca_method2, orca_scf, orca_basis2, orca_pol, orca_diff, orca_restriciton
		#print "\n\n",orca_string
		
		
		
	#============================#
    #        7_window_NEB        #
	#============================#
	def take_NEB_parameters(self):
		NEB_number_of_structures = int(self.builder.get_object('7_window_NEB_number_of_structures').get_text())
		NEB_maximum_interations  = int(self.builder.get_object('7_window_NEB_maximum_interations').get_text())
		NEB_grad_tol             = float(self.builder.get_object('7_window_NEB_grad_tol').get_text())
		trajectory_name          = self.builder.get_object('7_window_NEB__pd_traj_out').get_text()
		data_path  	 	         = self.builder.get_object("1window_main_dataPath_finder").get_filename()

		# reactants
		if self.builder.get_object('7_window_checkbutton_REACTANTS').get_active():
			reactants_file          = self.builder.get_object('7_window_filechooserbutton_REACTANTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('7_window_entry_REACTANTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "reactants_NEB.xyz"	
			reactants_file          = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)			
		
		
		# products
		if self.builder.get_object('7_window_checkbutton_PRODUCTS').get_active():
			products_file       = self.builder.get_object('7_window_filechooserbutton_PRODUCTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('7_window_entry_PRODUCTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "products_NEB.xyz"	
			products_file           = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)
		print      NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol , trajectory_name, data_path, reactants_file, products_file
		return     NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol , trajectory_name, data_path, reactants_file, products_file

	def on_7window_BUTTON_RUN_NEB(self, button, data=None):
		NEB_number_of_structures = int(self.builder.get_object('7_window_NEB_number_of_structures').get_text())
		NEB_maximum_interations  = int(self.builder.get_object('7_window_NEB_maximum_interations').get_text())
		NEB_grad_tol             = float(self.builder.get_object('7_window_NEB_grad_tol').get_text())
		trajectory_name          = self.builder.get_object('7_window_NEB__pd_traj_out').get_text()
		data_path  	 	         = self.builder.get_object("1window_main_dataPath_finder").get_filename()

		# reactants
		if self.builder.get_object('7_window_checkbutton_REACTANTS').get_active():
			reactants_file          = self.builder.get_object('7_window_filechooserbutton_REACTANTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('7_window_entry_REACTANTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "reactants_NEB.xyz"	
			reactants_file          = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)			
		
		if self.builder.get_object('7_window_checkbutton_PRODUCTS').get_active():
			products_file       = self.builder.get_object('7_window_filechooserbutton_PRODUCTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('7_window_entry_PRODUCTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "products_NEB.xyz"	
			products_file           =pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)
		plot_flag  = False
		if self.builder.get_object('7_window_NEB_Check_print_graf').get_active():
			plot_flag  = True			
		
		x, y, t = self.project.run_NEB( reactants_file, products_file, 	data_path, NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol, trajectory_name, plot_flag, self.dualLog )
		                               #reactants_file, products_file, data_path, NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol, trajectory_name, plot_flag, dualLog ):
		     
		print "total time = ", t
			
		self.run_NEB_window.hide()  #  I M P O R T A N T E , se nao a janela nao fecha.
			
		self.render_plot( x, y)
		# incrementing the step after Umbrella Sampling
		self.project.increment_step()
		
	def on_7window_CHECKBUTTON_REACTANTS(self, checkbutton, data=None):
		if self.builder.get_object("7_window_checkbutton_REACTANTS").get_active():
			self.builder.get_object("7_window_filechooserbutton_REACTANTS").show()
			self.builder.get_object("7_window_entry_REACTANTS").hide()
		else:
			self.builder.get_object("7_window_filechooserbutton_REACTANTS").hide()
			self.builder.get_object("7_window_entry_REACTANTS").show()

	def on_7window_CHECKBUTTON_PRODUCTS(self, checkbutton, data=None):
		if self.builder.get_object("7_window_checkbutton_PRODUCTS").get_active():
			self.builder.get_object("7_window_filechooserbutton_PRODUCTS").show()
			self.builder.get_object("7_window_entry_PRODUCTS").hide()
		else:
			self.builder.get_object("7_window_filechooserbutton_PRODUCTS").hide()
			self.builder.get_object("7_window_entry_PRODUCTS").show()		
	
	
	#============================#
    #      8_surface_window      #
	#============================#
	
	def on_8window_BUTTON_EXPORT_SURFACE(self, checkbutton, data=None):
		file_name = self.builder.get_object("8_window_entry_name_save_surface").get_text()
		out_path  = self.builder.get_object("8_window_directory_surface_file").get_filename()
		mode      = self.builder.get_object("8_window_combobox_surface").get_active_text()
		grid      = float(self.builder.get_object("8_window_entry_surface_grid").get_text())
		
		if mode == "density":
			try:
				( energies, HOMO, LUMO ) = self.project.system.energyModel.qcModel.OrbitalEnergies ( self.project.system.configuration )
				GaussianCubeFile_FromSystemDensity   ( os.path.join ( out_path, file_name + ".cube" ), self.project.system, gridspacing = grid, log =self.dualLog)
			except:
				data_path  	 	         = self.builder.get_object("1window_main_dataPath_finder").get_filename()
				energy, time  = self.project.check_energy(data_path, self.dualLog)
				( energies, HOMO, LUMO ) = self.project.system.energyModel.qcModel.OrbitalEnergies ( self.project.system.configuration )
				GaussianCubeFile_FromSystemDensity   ( os.path.join ( out_path, file_name + ".cube" ), self.project.system, gridspacing = grid, log =self.dualLog)
								
		if self.builder.get_object('8_window_PyMOL_checkbutton_auto_open').get_active():	
			print  "load "+ out_path+"/"+file_name +".cube"
			cmd.do("load "+ out_path+"/"+file_name +".cube")
			cmd.set ('mesh_width',       self.mesh_width )
			if self.builder.get_object('8_window_PyMOL_checkbutton_isomesh').get_active():
				level = self.builder.get_object("8_window_PyMOL_entry_isomesh").get_text()
				cmd.do("isomesh "+file_name+"_m,"+file_name+","+level)
				cmd.color("slate",file_name+"_m")
				#print  "isomesh "+file_name+"_m,"+file_name+","+level
			
			if self.builder.get_object('8_window_PyMOL_checkbutton_isosurface').get_active():
				level = self.builder.get_object("8_window_PyMOL_entry_isosurface").get_text()
				cmd.do("isosurface "+file_name+"_s,"+file_name+","+level)
				#print  "isosurface "+file_name+"_s,"+file_name+","+level			
				cmd.color("slate",file_name+"_s")
				
			if self.builder.get_object('8_window_PyMOL_checkbutton_isodot').get_active():
				level = self.builder.get_object("8_window_PyMOL_entry_isodot").get_text()
				cmd.do("isodot "+file_name+"_d,"+file_name+","+level)
				#print  "isodot "+file_name+"_d,"+file_name+","+level	
				cmd.color("slate",file_name+"_d")		
		"""
		if mode == "":
            ( energies, HOMO, LUMO ) = molecule.energyModel.qcModel.OrbitalEnergies ( molecule.configuration )
            if log is not None:
                if energies is not None: energies.Print ( log = log, title = "Orbital Energies" )
                log.Paragraph ( "HOMO and LUMO indices: " + `HOMO` + ", " + `LUMO` + "." )
            indices = [ HOMO, LUMO ]

            # . Write out the cube files.
            GaussianCubeFile_FromSystemDensity   ( os.path.join ( outPath, _SystemLabel + "_" + qcLabel + "_density"  + _Extension ), molecule, gridspacing = _GridSpacing, log = log )
            GaussianCubeFile_FromSystemOrbitals  ( os.path.join ( outPath, _SystemLabel + "_" + qcLabel + "_orbitals" + _Extension ), molecule, gridspacing = _GridSpacing, orbitals = indices, log = log )
        #    GaussianCubeFile_FromSystemPotential ( os.path.join ( outPath, _SystemLabel + "_" + qclabel + "_potential" + _Extension ), molecule, gridspacing = _GridSpacing, log = log )
		
		"""
			
	#============================#
    #    9_window_new_project    #
	#============================#
	
	def on_9window_BUTTON_CREATE_NEW_SYSTEM(self, button, data=None):  #"old import_molmec_system(*args): "
		project_name = self.builder.get_object("9_window_enter_project_name_new_system").get_text()
		data_path    = self.builder.get_object("9_window_data_path_finder_new_system").get_filename()												
		fftype       = self.builder.get_object("9_window_combobox_MM_model_new_system").get_active_text()			# combo box combox_model
		try :
			import shutil
		except:
			print "shutil module is no available"
		
		self.builder.get_object("1window_main_dataPath_finder").set_filename(data_path)
		#  Creating the project  object  where:
		#  system      = None 
		#  force_field = None
		
		self.project = DynamoProject()
		
		
		if fftype == "AMBER":
			amber_params  	= self.builder.get_object("9_window_entry_prmtop_system").get_filename()
			amber_coords  	= self.builder.get_object("9_window_entry_crd_new_system").get_filename()
			#if  self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():	
			self.project.set_AMBER_MM(amber_params, amber_coords, self.dualLog)
			
			# BACKUP SOURCE FILES
			if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():

				source_files        = data_path+"/source_files"                   #  diretorio de arquivos temporarios 
				if not os.path.exists (source_files): os.mkdir (source_files)     #  verifica se existe o diretorio tmp
				try:
					shutil.copy2(amber_params, source_files)
					shutil.copy2(amber_coords, source_files)
					print "the source files have been successfully transferred to:", source_files
				except:
					a = None
				
		elif fftype == "CHARMM":											
			charmm_params     = self.builder.get_object("9_window_entry_prmtop_system").get_filename()
			charmm_topologies = self.builder.get_object("9_window_entry_crd_new_system").get_filename()
			charmm_coords     = self.builder.get_object("9_window_xyzc_new_system").get_filename()
			
			self.project.set_CHARMM_MM(charmm_params, charmm_topologies, self.dualLog)
			filetype = self.project.load_coordinate_file_to_system(charmm_coords, self.dualLog)	
			
			# BACKUP SOURCE FILES
			if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():

				source_files        = data_path+"/source_files"                   #  diretorio de arquivos temporarios 
				if not os.path.exists (source_files): os.mkdir (source_files)     #  verifica se existe o diretorio tmp
				try:
					shutil.copy2(charmm_params,     source_files)
					shutil.copy2(charmm_topologies, source_files)
					shutil.copy2(charmm_coords,     source_files)
					print "the source files have been successfully transferred to:", source_files
				except:
					a = None

		elif fftype == "GROMACS":
			gromacs_params    = self.builder.get_object("9_window_entry_prmtop_system").get_filename()					#
			gromacs_coords    = self.builder.get_object("9_window_entry_crd_new_system").get_filename()					#			
			
			self.project.set_GROMACS_MM (gromacs_params, gromacs_coords, self.dualLog)
			
			# BACKUP SOURCE FILES
			if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():

				source_files        = data_path+"/source_files"                   #  temporary files directory
				if not os.path.exists (source_files): os.mkdir (source_files)     #  check if the tmp directory exist
				try:
					shutil.copy2(gromacs_params, source_files)
					shutil.copy2(gromacs_coords, source_files)
				
					print "the source files have been successfully transferred to:", source_files
				except:
					a = None
				
						
		elif fftype == "OPLS":
			opls_params       = self.builder.get_object("9_window_prm_opls_new_system").get_filename()
			opls_coords       = self.builder.get_object("9_window_entry_crd_new_system").get_filename()		
			self.project.set_OPLS_MM( opls_params, opls_coords, self.dualLog)

			# BACKUP SOURCE FILES
			if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():

				source_files        = data_path+"/source_files"                   #  
				if not os.path.exists (source_files): os.mkdir (source_files)     #  
				try:
					shutil.copy2(opls_coords,   source_files)
					#shutil.copy2(gromacs_coords, source_files)
					print "the source files have been successfully transferred to:", source_files
				except:
					a = None
	
		elif fftype == "Coordinates (*.pkl,*.yaml,*.pdb,*.xyz,*.mol,*.mol2...)":
			gromacs_params    = self.builder.get_object("9_window_entry_prmtop_system").get_filename()					#
			#gromacs_coords    = self.builder.get_object("9_window_entry_crd_new_system").get_filename()					#			
			self.project.load_coordinate_file_as_new_system(gromacs_params, self.dualLog)
			
			# BACKUP SOURCE FILES
			if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():

				source_files        = data_path+"/source_files"                   #  
				if not os.path.exists (source_files): os.mkdir (source_files)     # 
				try:
					shutil.copy2(gromacs_params,   source_files)
					#shutil.copy2(gromacs_coords, source_files)
					print "the source files have been successfully transferred to:", source_files
				except:
					a = None
									
				
		elif fftype == "PyMOL Object":
			data_path  	 = self.builder.get_object("9_window_data_path_finder_new_system").get_filename()
			#state    	 = int(self.builder.get_object("1window_main_import_state_from_pymol").get_text())
			state        = -1
			pymol_object = self.builder.get_object('9_window_entry_PyMOL_Object').get_text()

			
			if self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').get_active():
				label        = pymol_object + " XYZ file"
				file_out     = "PyMOL_object.xyz"	
				filename     = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, state)				
				self.project.load_coordinate_file_as_new_system( filename , self.dualLog)  # open coordinates as a new system  
				#self.project.increment_step()
				#self.project.export_frames_to_pymol('new', self.types_allowed , data_path)
				
				if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():
					source_files        = data_path+"/source_files"                   #  
					if not os.path.exists (source_files): os.mkdir (source_files)     #  
					try:
						shutil.copy2(filename,   source_files)
						print "the source files have been successfully transferred to:", source_files
					except:
						a =None

			if self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').get_active():
				file_out     = "PyMOL_object.pdb"
				filename     = pymol_export_PDB_to_file(pymol_object, data_path, file_out, state = -1)
				self.project.load_coordinate_file_as_new_system( filename , self.dualLog)  # open coordinates as a new system  

				if self.builder.get_object('9_window_checkbutton_BACKUP_source_files').get_active():
					source_files        = data_path+"/source_files"                   #  
					if not os.path.exists (source_files): os.mkdir (source_files)     #  
					try:
						shutil.copy2(filename,   source_files)
						print "the source files have been successfully transferred to:", source_files
					except:
						a = None
				
		'''
		cbox.append_text("AMBER")
		cbox.append_text("CHARMM")
		cbox.append_text("GROMACS")
		cbox.append_text("OPLS")
		cbox.append_text("pkl - pDynamo")
		cbox.append_text("yaml - pDynamo")
		cbox.append_text("Coordinates (*.pdb,*.xyz...)")
		cbox.append_text("PyMOL Object")
		'''
		
		nbModel_type = self.builder.get_object("9_window_nbmodel_comobobox_new_system").get_active_text()
		innerCutoff  = float(self.builder.get_object("9_window_innercutoff_entry_new_system").get_text())
		outerCutoff  = float(self.builder.get_object("9_window_outercutoff_entry_new_system").get_text())
		listCutoff   = float(self.builder.get_object("9_window_listcutoff_entry_new_system").get_text())
		kappa        = self.builder.get_object("9_window_kappa_entry_new_system").get_text()
		
		self.project.settings['nbModel_type'] = nbModel_type
		self.project.settings['ABFS_options'] = { "innerCutoff" : innerCutoff , "outerCutoff" : outerCutoff , "listCutoff"  : listCutoff }
		
		# nbModel applied
		self.project.set_nbModel_to_system()


		# pDynamo/PyMOL config !
		if self.builder.get_object('9_window_checkbutton_PDB_type').get_active():
			self.builder.get_object("1window_main_pdb_check_box").set_active(True)
			self.types_allowed['pdb'] = True
			#print "PDB"
		else:
			self.builder.get_object("1window_main_pdb_check_box").set_active(False)
			self.types_allowed['pdb'] = False
		
		if self.builder.get_object('9_window_checkbutton_XYZ_type').get_active():
			self.builder.get_object("1window_main_xyz_check_box").set_active(True)
			self.types_allowed['xyz'] = True
			#print "XYZ"
		else: 
			self.builder.get_object("1window_main_xyz_check_box").set_active(False)
			self.types_allowed['xyz'] = False
		
		if self.builder.get_object('9_window_checkbutton_MOL2_type').get_active():
			self.builder.get_object("1window_main_mol2_check_box").set_active(True)
			self.types_allowed['mol2'] = True
			#print "MOL2"
		else:
			self.builder.get_object("1window_main_mol2_check_box").set_active(False)
			self.types_allowed['mol2'] = False	



		print "\n\n\n\n\n\n"
		# nbModel incrementing the step
		self.project.increment_step()
	
		# Check System
		self.project.check_system(self.dualLog)
		
		# Loading the actual frame in pymol.
		self.project.export_frames_to_pymol('new', self.types_allowed , data_path)	
		
		self.project_name = None
		
		
	
		'''
		#-------------------#
		#     P R U N E     #
		#-------------------#
		if self.builder.get_object('9_window_checkbutton_PRUNE').get_active():
			file_in     = self.builder.get_object("9_window_load_prune_table_entry_new_system").get_filename()
			prune_table = load_table_from_file(file_in)
			
			self.project.put_prune_table(prune_table)                                   # prune
			
			self.project.increment_step()                                               # step
			
			self.project.check_system(self.dualLog)                                     # Check System
			
			self.project.export_frames_to_pymol('prn', self.types_allowed , data_path)	

		#-------------------#
		#       F I X       #
		#-------------------#
		if self.builder.get_object('9_window_checkbutton_FIX').get_active():	
			fix_table_file   = self.builder.get_object("9_window_load_fix_table_entry_new_system1").get_filename()					#			
			fix_table        = load_table_from_file(fix_table_file)
			pymol_put_table(fix_table, "fix")
			self.project.put_fix_table(fix_table)
			
			print "number of fixed atoms = " + str(len(fix_table))		

		#-------------------#
		#        Q C        #
		#-------------------#
		if self.builder.get_object('9_window_checkbutton_QC').get_active():	
			qc_table_file    = self.builder.get_object("9_window_load_qc_table_entry_new_system").get_filename()					#			
			qc_table         = load_table_from_file(qc_table_file)
			pymol_put_table(qc_table, "QC_atoms")
			self.project.put_qc_table(qc_table)
			print "number of atoms in quantum region= " + str(len(qc_table))
			print "please setup you QC parameters"
		'''
		
		#print 	"self.project.settings['data_path']", self.project.settings['data_path']
		#print   "data_path",                          data_path
		
		self.project.settings['data_path'] = data_path 
		#print "\n\n\n", data_path, "\n\n\n"
		
		#print 	"self.project.settings['data_path']", self.project.settings['data_path']
		#print   "data_path",                          data_path		
		
		filename = data_path + "/" + project_name
		#print "filename",  filename
				
		self.project.export_GTKDynamo_session_to_file(filename)		
		self.project_name = filename
		
		step       =  self.project.step
		process    = "new system"
		potencial  = self.project.settings["potencial"]
		energy     = " - "
		time       = " - " 
		self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
				
	def on_9window_COMBOBOX_MM_MODEL_CHANGE(self, menuitem, data=None):  # combobox event 
		fftype = self.builder.get_object("9_window_combobox_MM_model_new_system").get_active_text()
		
		if fftype == "AMBER":
			self.builder.get_object("9_window_xyzc_new_system").hide()
			self.builder.get_object("9_window_prm_opls_new_system").hide()
			self.builder.get_object("9_window_entry_prmtop_system").show()
			self.builder.get_object("9_window_chm_crd_label1_new_system").hide()

			self.builder.get_object("9_window_entry_crd_new_system").show()
			self.builder.get_object("9_window_psfx_crd_label_new_system").show()
			
			self.builder.get_object('9_window_prm_top_label_new_system').set_text("AMBER Param/ Topol file:")
			self.builder.get_object('9_window_psfx_crd_label_new_system').set_text("AMBER Coordinates File:")
			
			self.builder.get_object('9_window_entry_PyMOL_Object').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').hide()
				
		if fftype == "CHARMM":
			self.builder.get_object("9_window_xyzc_new_system").show()
			self.builder.get_object("9_window_prm_opls_new_system").hide()
			self.builder.get_object("9_window_entry_prmtop_system").show()
			self.builder.get_object("9_window_chm_crd_label1_new_system").show()
			
			self.builder.get_object("9_window_entry_crd_new_system").show()
			self.builder.get_object("9_window_psfx_crd_label_new_system").show()

			self.builder.get_object('9_window_prm_top_label_new_system').set_text("CHARMM Parameters:")
			self.builder.get_object('9_window_psfx_crd_label_new_system').set_text("CHARMM Topology:")
			
			self.builder.get_object('9_window_entry_PyMOL_Object').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').hide()
			
		if fftype == "GROMACS":
			self.builder.get_object("9_window_xyzc_new_system").hide()
			self.builder.get_object("9_window_prm_opls_new_system").hide()
			self.builder.get_object("9_window_entry_prmtop_system").show()
			self.builder.get_object("9_window_chm_crd_label1_new_system").hide()

			self.builder.get_object("9_window_entry_crd_new_system").show()
			self.builder.get_object("9_window_psfx_crd_label_new_system").show()

			self.builder.get_object('9_window_prm_top_label_new_system').set_text("GROMACS Param/Topol file(top):")
			self.builder.get_object('9_window_psfx_crd_label_new_system').set_text("GROMACS Coordinate file (gro):")
			
			self.builder.get_object('9_window_entry_PyMOL_Object').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').hide()
					
		if fftype == "OPLS":
			self.builder.get_object("9_window_xyzc_new_system").hide()
			self.builder.get_object("9_window_prm_opls_new_system").show()
			self.builder.get_object("9_window_entry_prmtop_system").hide()
			self.builder.get_object("9_window_chm_crd_label1_new_system").hide()

			self.builder.get_object("9_window_entry_crd_new_system").show()
			self.builder.get_object("9_window_psfx_crd_label_new_system").show()
			
			self.builder.get_object('9_window_prm_top_label_new_system').set_text("OPLS Param/Topol folder:")
			self.builder.get_object('9_window_psfx_crd_label_new_system').set_text("OPLS Coordinates:")
			
			self.builder.get_object('9_window_entry_PyMOL_Object').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').hide()
					
		if fftype == "Coordinates (*.pkl,*.yaml,*.pdb,*.xyz,*.mol,*.mol2...)":
			self.builder.get_object("9_window_xyzc_new_system").hide()
			self.builder.get_object("9_window_prm_opls_new_system").hide()
			self.builder.get_object("9_window_entry_prmtop_system").show()
			self.builder.get_object("9_window_chm_crd_label1_new_system").hide()
			self.builder.get_object("9_window_entry_crd_new_system").hide()
			self.builder.get_object("9_window_psfx_crd_label_new_system").hide()
			self.builder.get_object('9_window_prm_top_label_new_system').set_text("Coordinates:")
			
			self.builder.get_object('9_window_entry_PyMOL_Object').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').hide()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').hide()	
					
		if fftype == "PyMOL Object":
			self.builder.get_object("9_window_xyzc_new_system").hide()
			self.builder.get_object("9_window_prm_opls_new_system").hide()
			self.builder.get_object("9_window_entry_prmtop_system").hide()
			self.builder.get_object("9_window_chm_crd_label1_new_system").hide()
			self.builder.get_object("9_window_entry_crd_new_system").hide()
			self.builder.get_object("9_window_psfx_crd_label_new_system").hide()
			self.builder.get_object('9_window_prm_top_label_new_system').set_text("Object:")			
			
			self.builder.get_object('9_window_entry_PyMOL_Object').show()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_pdb').show()
			self.builder.get_object('9_window_PyMOL_OBJ_radiobutton_xyz').show()
			
	#============================#
	# -  10_window_NormalModes   #
	#============================#
	
	def on_10window_BUTTON_RUN_NORMAL_MOLDES(self, button, data=None):
		data_path  	  =  self.builder.get_object("1window_main_dataPath_finder").get_filename()												
		traj_name     =  self.builder.get_object('10_window_NMoldes_traj').get_text()
		mode          =  int(self.builder.get_object('10_window_NMoldes_Mode').get_text())
		cycles        =  int(self.builder.get_object('10_window_NMoldes_Cycles').get_text())
		frames        =  int(self.builder.get_object('10_window_NMoldes_Frames').get_text())
		temp          =  int(self.builder.get_object('10_window_NMoldes_temperature').get_text())
	
		t = self.project.run_NormalModes(data_path, traj_name, mode, cycles, frames, temp, self.dualLog)
		
		print "total time = ", t
		self.normal_modes_window.hide()
	
	#============================#	
	# -  11_window_VAGO          #
	#============================#
	
	#============================#	
	# -     13_window_merge      #
	#============================#
	
	def on_13window_BUTTON_RUN_MERGE_OBJECTS(self, button, data=None): 
	
		data_path  	 	= self.builder.get_object("1window_main_dataPath_finder").get_filename()
		
		obj1 =self.builder.get_object('13_window_entry_merge_obj01').get_text()
		obj2 =self.builder.get_object('13_window_entry_merge_obj02').get_text()
		obj3 =self.builder.get_object('13_window_entry_merge_obj03').get_text()
		text = [] 
		MERGE_OBJ_IN_PYMOL(data_path, obj1, obj2, obj3)
	
	#====================================#
	# -  14_window_import_coordinates  - # 
	#====================================#
	
	def on_14window_BUTTON_IMPORT_COORDINATES(self, button, data=None):  # 

		
		data_path 	=  self.builder.get_object("1window_main_dataPath_finder").get_filename()
		mode        =  self.builder.get_object('14_window_combobox_coordToSys_or_coordNewSys').get_active_text()
		file_in     =  self.builder.get_object("14_window_filechooserbutton1").get_filename()
		
		if mode == "Coordinates to System":
			self.project.load_coordinate_file_to_system(file_in, self.dualLog)
			self.project.increment_step()
			
			# JOB HISTORY
			step       =  self.project.step
			process    = "new coordinates"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
			

		if mode == "New System":
			self.project = DynamoProject()
			self.project.load_coordinate_file_as_new_system(file_in, self.dualLog)
			self.project.settings['coordinates'] = file_in	
			self.project.increment_step()
			self.project.check_system(self.dualLog)
			
			# JOB HISTORY
			step       =  self.project.step
			process    = "new system"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
			

			
		self.project.export_frames_to_pymol('new', self.types_allowed , data_path)	
	
	#===============================#
	# -  15_window_TLEAP_dialog1  - #
	#===============================#
	
	def on_15window_BUTTON_RUN_TLEAP(self, button, data=None):  # 
		data_path     = self.builder.get_object("1window_main_dataPath_finder").get_filename()	
		pymol_obj     = self.builder.get_object("15_window_TLEAP_entry_pdb_obj_in").get_text()
		ff_model      = self.builder.get_object("15_window_TLEAP_ff_model").get_active_text()
		ff_model_gly  = self.builder.get_object("15_window_TLEAP_ff_model_gly").get_active_text()
		system_name   = self.builder.get_object('15_window_TLEAP_entry_system_out').get_text()
		
		add_ions      = False
		neutralize    = False
		positive_type =  None
		negative_type =  None
		positive_num  =  None
		negative_num  =  None		
		
		if self.builder.get_object('15_window_TLEAP_check_tleap_ff_gaff').get_active():
			ff_model_gaff  =  True
		else:
			ff_model_gaff  =  False
		
		
		if self.builder.get_object('15_window_TLEAP_15_window_AMBERTOOLS_check_tleap_solvate').get_active():
			water_model =  self.builder.get_object('15_window_TLEAP_cbox_solvate_water_model').get_active_text()
			water_box   =  self.builder.get_object('15_window_TLEAP_solvate_radus').get_text()
		
		else:
			water_model = None
			water_box   = None		
			
		
		if self.builder.get_object('15_window_TLEAP_radiobutton_do_nothing').get_active():
			add_ions      =  False
			positive_type =  None
			negative_type =  None
			positive_num  =  None
			negative_num  =  None		
			
		elif self.builder.get_object('15_window_TLEAP_radiobutton_add_ions').get_active():
			add_ions      =  True
			positive_type =  self.builder.get_object('15_window_TLEAP_cbox1_IONIZE_positvie').get_active_text()
			negative_type =  self.builder.get_object('15_window_TLEAP_cbox1_IONIZE_negative').get_active_text()
			positive_num  =  self.builder.get_object('15_window_TLEAP_entry_addions_positive').get_text()
			negative_num  =  self.builder.get_object('15_window_TLEAP_entry_addions_negative').get_text()
			
			neutralize = False
			
		elif self.builder.get_object('15_window_TLEAP_radiobutton_neutralize').get_active():
			add_ions      =  True
			neutralize    =  True
			
			ionize = "neutral"
			pname = "NA"
			np    = "1"
			nname = "CL"
			nn    = "1"		
		

		pdb_file        = self.AmberProject.TLEAP_export_pdb_from_pymol( data_path, pymol_obj)  # export o pdb com o residuos modificados
		
		self.AmberProject.TLEAP_make_script( pdb_file, system_name, data_path, ff_model, ff_model_gly, ff_model_gaff,  water_model, water_box, add_ions, 	neutralize, positive_type,  negative_type, positive_num, negative_num)    		
		#self.TLEAP_window.hide()
		os.system("tleap -f "+data_path+"/leaprc")
		
		
		
		#'''---remove the log file generated in the GTKDynamo folder---'''
		try:
			os.rename("leap.log", data_path + "/AMBERTOOLS_outputs/leap.log")
		except:
			a = None
		#'''   ----------------------------------------------------   '''
		
		filein  = system_name+".top"
		fileout = system_name+".top"
		self.AmberProject.TLEAP_amber12_to_amber11_topology_converter (filein, fileout, data_path)
		
		
	def on_15window_BUTTON_ADD_EXTRA_FILES_TO_LIST(self, button, data=None):
		data_path = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		filein    = self.get_open_filename_amber()
		gaff_list = self.AmberProject.TLEAP_add_mol2_or_frcmod_to_gaff_list(filein)
		print gaff_list
		

		fin = ""
		for i in gaff_list:							#
			fname = i.split("/")					#
			fin = fin+ fname[-1]+"\n"		        #Writes only the file name of the loaded files into a gaff_list.list

		text = fin
		buff = self.builder.get_object('15_window_TLEAP_ff_text_frame').get_buffer()   #load buffer
		buff.set_text(text)													           #writes the file text in the buffer
		buff.set_modified(False)											           # 
		self.builder.get_object('15_window_TLEAP_ff_text_frame').set_sensitive(True)   #

	def on_15window_BUTTON_CLEAR_EXTRA_FILE_LIST(self, button, data=None):
		gaff_list = self.AmberProject.TLEAP_clear_gaff_list()
		buff = self.builder.get_object('15_window_TLEAP_ff_text_frame').get_buffer()
		buff.set_text("Empty list")
	
	def get_open_filename_amber(self, data = None):  # abre janela de procura
		data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		filename = None
		chooser = gtk.FileChooserDialog("Open File...", self.window,
										gtk.FILE_CHOOSER_ACTION_OPEN,
										(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
										 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		chooser.set_current_folder(data_path)
		response = chooser.run()
		if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
		chooser.destroy()
		return 	filename

	def on_15window_BUTTON_OPEN_MODIFY (self, button, data=None):
		""" Function doc """
		self.modify_window.run()
		self.modify_window.hide()

	#===============================#
	# -   16_window_ANTECHAMBER   - #
	#===============================#
	
	def on_16window_BUTTON_ANTECHAMBER_IMPORT_LIGAND (self, button, data=None):
		data_path        = self.builder.get_object("1window_main_dataPath_finder").get_filename()	
		obj_in           = self.builder.get_object("16_window_ANTECHAMBER_entry_pymol_obj").get_text()
		new_ligand_name  = self.builder.get_object("16_window_ANTECHAMBER_entry_new_name").get_text()
		
		change_resn_ID  = False
		add_H           = False
				
		if self.builder.get_object('16_window_ANTECHAMBER_checkbutton1_residue_code').get_active():
			change_resn_ID = True	
		if self.builder.get_object('16_window_ANTECHAMBER_checkbutton1_add_H').get_active():
			add_H  =  True
		
		print new_ligand_name
			
		lig = self.AmberProject.ANTECHAMBER_generate_ligand(new_ligand_name, data_path, obj_in, add_H, change_resn_ID)
		self.builder.get_object('16_window_ANTECHAMBER_entry1_molecule_code').set_text(lig)
		
		
		                                                #(self, new_ligand_name, data_path, obj_in, add_H, change_resn_ID)
	def on_16window_BUTTON_RUN_ANTECHAMBER(self, button, data=None):	
		data_path        = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		
		charge_model = self.builder.get_object('16_window_ANTECHAMBER_combobox_charge_antechamber').get_active_text()		#
		charge       = str(self.builder.get_object('16_window_ANTECHAMBER_entry_chrg_antechamber').get_value_as_int())		#
		multiplicity = str(self.builder.get_object('16_window_ANTECHAMBER_entry_mult_antechamber').get_value_as_int())		#
		
		pymol_FLAG   =  False	
		param_FLAG   =  False
		charge_FLAG  =  False	
					
		if self.builder.get_object('16_window_ANTECHAMBER_check_charges').get_active():
			charge_FLAG =  True	
		if self.builder.get_object('16_window_ANTECHAMBER_checkbutton_open_in_pymol').get_active():
			pymol_FLAG   =  True	
		if self.builder.get_object('16_window_ANTECHAMBER_checkbutton_auto_check_param').get_active():
			param_FLAG   =  True
		
		#new_lig = self.new_lig
		
		try:
			index,atomname,atomtype,charge_table = self.AmberProject.ANTECHAMBER_run_antechamber(data_path, charge, multiplicity, charge_model, charge_FLAG, pymol_FLAG, param_FLAG )
	                                          #(self, data_path, charge, multiplicity, charge_model, charge_FLAG, pymol_FLAG, param_FLAG, new_lig):

			
			self.on_16window_SETUP_ADD_DATA_TO_TREEVIEW(index,atomname,atomtype,charge_table)
			
			total_charge = self.on_16window_TREEVIEW_GET_TOTAL_CHARGE()
			self.builder.get_object('16_window_ANTECHAMBER_entry_total_charge').set_text(str(total_charge))
		except:
			return None
	def on_16window_SETUP_ADD_DATA_TO_TREEVIEW(self,index,atomname,atomtype,charge_table):
		model = self.builder.get_object("liststore2") #@+
		model.clear()
		n = 0
		for i in index:
			data = [index[n], atomname[n], atomtype[n],charge_table[n]]
			model.append( data)
			n = n +1

	def row_activated( self, tree, path, column):
		
		model    = tree.get_model() #@+
		iter     = model.get_iter( path) #@+
		index    = model.get_value( iter, 0) #@+
		atomtype = model.get_value( iter, 2) #@+
		

		
		if  atomtype[0] == 'c':
			atomname = "C"
		
		elif atomtype[0:2] == 'cl':
			atomname = "CL"
		
		if  atomtype[0] == 'h':
			atomname = "H"
		
		if  atomtype[0] == 'n':
			atomname = "N"
		
		if  atomtype[0] == 'f':
			atomname = "F"
					
		if  atomtype[0] == 'i':
			atomname = "I"
		
		if  atomtype[0] == 'b':
			atomname = "BR"

		if  atomtype[0] == 'o':
			atomname = "O"
		
		if  atomtype[0] == 'p':
			atomname = "P"
		
		if  atomtype[0] == 's':
			atomname = "S"			

		model2    = self.builder.get_object("liststore3") #@+
		model2.clear()
		atomlist = self.AmberProject.atomtype[atomname]
		
		
		for i in atomlist:
			model2.append(i)
		
		pymol_obj = self.AmberProject.ligand_name
		string   = 'zoom ('+pymol_obj+ ' and  index '+ index + ')'
		string2  = 'select ('+pymol_obj+ ' and  index '+ index + ')'
		
		cmd.do(string)
		cmd.do(string2)
		
	def on_16window_TREEVIEW_row_activated (self, tree, path, column):
		model     = tree.get_model() #@+
		iter      = model.get_iter( path) #@+
		atomtype1 = model.get_value( iter, 1) #@+
		print atomtype1
		
		model2       = self.builder.get_object("liststore2") #@+
		treeview     = self.builder.get_object("16_window_treeview1")
		selection    = treeview.get_selection()
		model2, iter = selection.get_selected()		
		
		atomtype2    = model2.get_value( iter, 2) #@+
		print atomtype2
		model2.set_value(iter, 2, atomtype1)
		
	def on_16window_TREEVIEW_text_edited( self, w, row, new_text):
		model          =  self.builder.get_object("liststore2")
		model[row][3]  = new_text
		total_charge   = self.on_16window_TREEVIEW_GET_TOTAL_CHARGE()
		self.builder.get_object('16_window_ANTECHAMBER_entry_total_charge').set_text(str(total_charge))

	def on_16_GET_MODEL_FROM_LISTSTORY(self):
		model        = self.builder.get_object("liststore2") #@+
		treeview     = self.builder.get_object("16_window_treeview1")
		
		index        = []
		atomname     = []
		atomtype     = []
		charge_table = []
		
		for i in model:
			index.append(i[0])
			atomname.append(i[1])
			atomtype.append(i[2])
			charge_table.append(i[3])	
					
			print i[0],i[1],i[2],i[3]
		
		return index,atomname,atomtype,charge_table
		
	def on_16window_BUTTON_SAVE_TOPOLOGIES(self, button, data=None):
		data_path        = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		index,atomname,atomtype,charge_table = self.on_16_GET_MODEL_FROM_LISTSTORY()
		
		self.AmberProject.ANTECHAMBER_edit_mol2_file(data_path,index,atomname,atomtype,charge_table)
		self.AmberProject.ANTECHAMBER_run_parmchk(data_path )
		
	def on_16window_TREEVIEW_GET_TOTAL_CHARGE(self):
		model     = self.builder.get_object("liststore2") #@+
		treeview  = self.builder.get_object("16_window_treeview1")
		charge    = 0.0 
	
		for i in model:
			charge = charge + float(i[3])
		print  "total charge", charge	
		return charge		
		
		
		
	#======================================#
	# -   17_window_SAVE_FRAME_dialog1   - #
	#======================================#		
	def on_17window_BUTTON_SAVE_FRAME(self, button, data=None):	
		self.GTKDynamo_and_Pymol_active_mode ()
		directory_save_file  = self.builder.get_object('17_window_SAVE_FRAME_directory_save_file').get_filename()
		type_                = self.builder.get_object('17_window_SAVE_FRAME_combobox_file_type').get_active_text()
		filename             = self.builder.get_object('17_window_SAVE_FRAME_save_frame').get_text()
		
		filename = directory_save_file+"/"+filename
		self.project.export_state_to_file ( filename, type_)
		print " Done ! "
	
	#======================================#
	# -     18_window_modify_residues    - #
	#======================================#		

	def on_18window_BUTTON_IMPORT_RESIDUE_INFORMATION(self, button, data=None):
		model = cmd.get_model("pk1")	
		index = []
		resn = None
		resi = None 
		
		for a in model.atom:
			resn = a.resn
			resi = a.resi
		self.builder.get_object('18_window_modify_entry_modify3').set_text(resi)
		self.builder.get_object('18_window_modify_entry_modify4').set_text(resn)

	def on_18window_BUTTON_ADD_CHANGES_TO_LIST(self, button, data=None):	
		data_path      = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		resi_number    = self.builder.get_object('18_window_modify_entry_modify3').get_text()
		resn_wild      = self.builder.get_object('18_window_modify_entry_modify4').get_text()
		resn_mutant    = self.builder.get_object('18_window_modify_entry_modify5').get_text()

		modify_list    = self.AmberProject.TLEAP_modify_addChangesToList( data_path, resi_number, resn_wild, resn_mutant)
		
		
		fin = ""
		for i in modify_list:							#
			fin = fin + i                		        #Just write the name of the uploaded files in a file called gaff_list.list
			
		text = fin
		buff = self.builder.get_object('18_window_modify_textview1_modify_ff_text_frame1').get_buffer()   #
		buff.set_text(text)													                              #
		buff.set_modified(False)											                              # 

	def on_18window_BUTTON_DELETE_LAST_ITEM_FROM_LIST(self, button, data=None):
		modify_list   = self.AmberProject.TLEAP_modify_DeleteLastItemFromList()
		
		if modify_list != False:
			fin = ""
			for i in modify_list:							#
				fin = fin + i                		        #Just write the name of the uploaded files in a file called gaff_list.list
				
			text = fin
			buff = self.builder.get_object('18_window_modify_textview1_modify_ff_text_frame1').get_buffer()   #
			buff.set_text(text)													                              #
			buff.set_modified(False)
		else:
			print "list is empty"

	
	def on_18window_BUTTON_CLEAN_LIST(self, button, data=None):
		self.AmberProject.TLEAP_modify_CLEAN_LIST( )
		buff = self.builder.get_object('18_window_modify_textview1_modify_ff_text_frame1').get_buffer()
		buff.set_text("Empty list")


	def on_18window_BUTTON_ADD_LINK_TO_LIST(self, button, data=None):	
		data_path      = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		atom1          = self.builder.get_object('18_window_modify_entry_modify1').get_text()
		atom2          = self.builder.get_object('18_window_modify_entry_modify2').get_text()
		#resn_mutant    = self.builder.get_object('18_window_modify_entry_modify5').get_text()

		link_list    = self.AmberProject.TLEAP_modify_addLinksToList(atom1, atom2)
		
		fin = ""
		for i in link_list:							#
			fin = fin + i                		        #Just write the name of the uploaded files in a file called gaff_list.list
			
		text = fin
		buff = self.builder.get_object('18_window_modify_textview1_modify_ff_text_frame3').get_buffer()   #
		buff.set_text(text)													                              #
		buff.set_modified(False)											                              # 


	def on_18window_BUTTON_DELETE_LAST_ITEM_FROM_LINK_LIST(self, button, data=None):
		link_list    = self.AmberProject.TLEAP_modify_DeleteLastItemFromLinkList()
		
		if link_list != False:
			fin = ""
			for i in link_list:							#
				fin = fin + i                		        #Just write the name of the uploaded files in a file called gaff_list.list
				
			text = fin
			buff = self.builder.get_object('18_window_modify_textview1_modify_ff_text_frame3').get_buffer()   #
			buff.set_text(text)													                              #
			buff.set_modified(False)
		else:
			print "list is empty"
		
	def on_18window_BUTTON_CLEAN_LINK_LIST(self, button, data=None):
		self.AmberProject.TLEAP_modify_CLEAN_LINK_LIST( )
		buff = self.builder.get_object('18_window_modify_textview1_modify_ff_text_frame3').get_buffer()
		buff.set_text("Empty list")


#	def on_18window_CHECK_BUTTON_LINK_ATOMS(self, button, data=None):
#		if self.builder.get_object('18_window_checkbutton_link_atoms').get_active():	
#			self.builder.get_object('18_window_modify_entry_modify1').set_sensitive(True)
#			self.builder.get_object('18_window_modify_label1_modify4').set_sensitive(True)
#			self.builder.get_object('18_window_modify_entry_modify2').set_sensitive(True)
#			self.builder.get_object('18_window_modify_button_modify2').set_sensitive(True)
#			self.builder.get_object('18_window_modify_frame1_modify_ff_text_frame3').set_sensitive(True)
#			self.builder.get_object('18_window_modify_button_modify_ff_clear_list2').set_sensitive(True)
#			self.builder.get_object('18_window_modify_button_modify_ff_addtolist2').set_sensitive(True)
#			self.builder.get_object('18_window_modify_CLEAN_LIST1').set_sensitive(True)
#		else:
#			self.builder.get_object('18_window_modify_entry_modify1').set_sensitive(False)
#			self.builder.get_object('18_window_modify_label1_modify4').set_sensitive(False)
#			self.builder.get_object('18_window_modify_entry_modify2').set_sensitive(False)
#			self.builder.get_object('18_window_modify_button_modify2').set_sensitive(False)
#			self.builder.get_object('18_window_modify_frame1_modify_ff_text_frame3').set_sensitive(False)
#			self.builder.get_object('18_window_modify_button_modify_ff_clear_list2').set_sensitive(False)
#			self.builder.get_object('18_window_modify_button_modify_ff_addtolist2').set_sensitive(False)
#			self.builder.get_object('18_window_modify_CLEAN_LIST1').set_sensitive(False)			
		#if qc_method in DFT:
		#	self.builder.get_object('1window_main_label58').set_sensitive(True)
		#else:
		#	self.builder.get_object('1window_main_label58').set_sensitive(False)
			
	#======================================#
	# -         19_window_S C A N        - #
	#======================================#

	def on_19window_IMPORT_PYMOL_DATA(self, button, data=None):
		mode        =  self.builder.get_object('19_window_SCAN_combobox_Reaction_coordiante2').get_active_text()
		
		
		if mode == "simple-distance":
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				distance_a1_a2 = str(distance_a1_a2)
				self.builder.get_object('19_window_SCAN_entry_param_DMINIMUM').set_text(distance_a1_a2)
				
				self.builder.get_object("19_window_SCAN_entry_cood1_ATOM1").set_text(str(atom1_index))
				self.builder.get_object("19_window_SCAN_entry_cood1_ATOM1_name").set_text(name1)
				self.builder.get_object("19_window_SCAN_entry_cood1_ATOM2").set_text(str(atom2_index))
				self.builder.get_object("19_window_SCAN_entry_cood1_ATOM2_name").set_text(name2)
			except:
				print texto_d1	
				return	
		if mode == "multiple-distance":			
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
			
				print "distance between atom 1 and atom 2: ",distance_a1_a2
				print "distance between atom 2 and atom 3: ",distance_a2_a3
				
				if self.builder.get_object("19_window_scan_checkbox_mass_weight").get_active():
					
					
					self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
					
					"""
					   R                    R
						\                  /
						 A1--A2  . . . . A3
						/                  \ 
					   R                    R
						 ^   ^            ^
						 |   |            |
						pk1-pk2  . . . . pk3
						   d1       d2	
					
					q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
					
					"""			
					
					DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
					self.builder.get_object('19_window_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nUsing mass weighted restraints"
					print "Sigma pk1_pk3", self.sigma_pk1_pk3
					print "Sigma pk3_pk1", self.sigma_pk3_pk1
					print "Estimated minimum distance",  DMINIMUM
					
				else:
					self.sigma_pk1_pk3 =  1.0
					self.sigma_pk3_pk1 = -1.0
					DMINIMUM = distance_a1_a2 - distance_a2_a3
					self.builder.get_object('19_window_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
					print "Sigma pk3_pk1", self.sigma_pk3_pk1
					print "Estimated minimum distance",  DMINIMUM			
			except:
				print texto_d2d1	
				return			
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM1").set_text(str(atom1_index))
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM1_name").set_text(name1)
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM2").set_text(str(atom2_index))
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM2_name").set_text(name2)
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM3").set_text(str(atom3_index))
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM3_name").set_text(name3)

	def on_19window_CHECKBOX_mass_weighted_restraints(self, button, data=None):
		try:
			name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
			name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
		except:
			print texto_d2d1
			return
			
		if self.builder.get_object("19_window_scan_checkbox_mass_weight").get_active():
			self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
			
			"""
			   R                    R
				\                  /
				 A1--A2  . . . . A3
				/                  \ 
			   R                    R
				 ^   ^            ^
				 |   |            |
				pk1-pk2  . . . . pk3
				   d1       d2	
			
			q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
			
			"""			
			DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
			self.builder.get_object('19_window_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nUsing mass weighted restraints"
			print "Sigma pk1_pk3", self.sigma_pk1_pk3
			print "Sigma pk3_pk1", self.sigma_pk3_pk1
			print "Estimated minimum distance",  DMINIMUM
			
		else:
			self.sigma_pk1_pk3 =  1.0
			self.sigma_pk3_pk1 = -1.0
			DMINIMUM = distance_a1_a2 - distance_a2_a3
			self.builder.get_object('19_window_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
			print "Sigma pk3_pk1", self.sigma_pk3_pk1
			print "Estimated minimum distance",  DMINIMUM	

	def on_19window_BUTTON_RUN_SCAN(self, button, data=None):
		data_path      = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		self.GTKDynamo_and_Pymol_active_mode () #BETA
		
		# . import parameters
		DINCREMENT      = float(self.builder.get_object('19_window_SCAN_entry_STEP_SIZE4').get_text())
		NWINDOWS        = int(self.builder.get_object('19_window_SCAN_entry_NWINDOWS4').get_text())
		DMINIMUM        = float(self.builder.get_object('19_window_SCAN_entry_param_DMINIMUM').get_text())
		FORCECONSTANT   = float(self.builder.get_object('19_window_SCAN_entry_FORCE4').get_text())

		max_int               = int(self.builder.get_object("19_window_SCAN_mim_param_entry_max_int1").get_text())
		log_freq              = None
		rms_grad              = float(self.builder.get_object("19_window_SCAN_mim_param_entry_rmsd_grad1").get_text())			
		mim_method			  = self.builder.get_object('26_window_scan2d_combobox2').get_active_text()
		
		# .  import trajectory parameters	
		traj            = self.builder.get_object('19_window_SCAN_mim_param_entry_TRAJECTORY1').get_text()
		if not os.path.exists (data_path + "/"+ traj): os.mkdir ( data_path + "/"+ traj)
		outpath = data_path + "/"+ traj	
		
		mode        =  self.builder.get_object('19_window_SCAN_combobox_Reaction_coordiante2').get_active_text()
		print "\n\n"
		print mode 
		

		if mode == "simple-distance":
			#name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
			
			ATOM1      = int(self.builder.get_object('19_window_SCAN_entry_cood1_ATOM1').get_text())
			ATOM1_name = self.builder.get_object('19_window_SCAN_entry_cood1_ATOM1_name').get_text()
			ATOM2      = int(self.builder.get_object('19_window_SCAN_entry_cood1_ATOM2').get_text())
			ATOM2_name = self.builder.get_object('19_window_SCAN_entry_cood1_ATOM2_name').get_text()
			
			print "\n\n         SCAN  MODE: ", mode       
			print "\n"
			print "  "+ATOM1_name+"   ->-  "+ATOM2_name
			print " pk1 --- pk2 "
			print "\n\n"			
			#print "distance between atom 1 and atom 2: ",distance_a1_a2
			print "DMINIMUM  : ",DMINIMUM

			
			x, y = self.project.run_SCAN ( outpath, 
											ATOM1,
											ATOM1_name, 
											ATOM2,
											ATOM2_name,											 
											DINCREMENT,
											NWINDOWS,
											FORCECONSTANT,
											DMINIMUM,
											max_int, 
											log_freq,
											rms_grad, 
											mim_method, self.dualLog) # 
			
		if mode == "multiple-distance":
#			name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
#			name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
			
			ATOM1      = int(self.builder.get_object('19_window_SCAN_entry_cood1_ATOM1').get_text())
			ATOM1_name = self.builder.get_object('19_window_SCAN_entry_cood1_ATOM1_name').get_text()
			ATOM2      = int(self.builder.get_object('19_window_SCAN_entry_cood1_ATOM2').get_text())
			ATOM2_name = self.builder.get_object('19_window_SCAN_entry_cood1_ATOM2_name').get_text()
			ATOM3      = int(self.builder.get_object('19_window_SCAN_entry_cood1_ATOM3').get_text())
			ATOM3_name = self.builder.get_object('19_window_SCAN_entry_cood1_ATOM3_name').get_text()

			print "\n\n"
			print "  "+ATOM1_name+"   ->-  "+ATOM2_name+"  -->-- "+ATOM3_name+"  "
			print " pk1 --- pk2 ---- pk3 \n"
			print "DMINIMUM  : ",DMINIMUM
			print "\n\n"						
			
			print 
			sigma_pk1_pk3 = self.sigma_pk1_pk3
			sigma_pk3_pk1 = self.sigma_pk3_pk1
			print sigma_pk3_pk1
			print sigma_pk1_pk3

			#"""
			x, y = self.project.run_SCAN_d1_d2(outpath, 
											  ATOM1,
											  ATOM1_name, 
											  ATOM2,
											  ATOM2_name, 
											  ATOM3,
											  ATOM3_name,
											  DINCREMENT,
											  NWINDOWS,         # ok
											  FORCECONSTANT,    # ok
											  DMINIMUM,         # ok
											  sigma_pk1_pk3, 
											  sigma_pk3_pk1,
											  max_int, 
											  log_freq,
											  rms_grad,
											  mim_method,
											  self.dualLog  )
			#"""

		self.SCAN_window.hide()  #  I M P O R T A N T , close the window.
		self.project.increment_step()
		self.render_plot(x, y)
		
		
	def on_19window_COMBOBOX_CHANGE_SCAN_MODE (self, menuitem, data=None):
		""" Function doc """
		
		method = self.builder.get_object('19_window_SCAN_combobox_Reaction_coordiante2').get_active_text()
		if method == "simple-distance":
			self.builder.get_object("19_window_SCAN_label_coord1_atom3").hide()
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM3").hide()
			self.builder.get_object("19_window_SCAN_label_cood1_ATOM3_name").hide()
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM3_name").hide()
			self.builder.get_object("19_window_scan_checkbox_mass_weight").hide()
			#self.builder.get_object('19_window_label1').set_text("Define atoms using pk1 and pk2 selections")
		if method == "multiple-distance":
			self.builder.get_object("19_window_SCAN_label_coord1_atom3").show()
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM3").show()
			self.builder.get_object("19_window_SCAN_label_cood1_ATOM3_name").show()
			self.builder.get_object("19_window_SCAN_entry_cood1_ATOM3_name").show()
			self.builder.get_object("19_window_scan_checkbox_mass_weight").show()

	#======================================#
	# -         20_window_GMX            - #
	#======================================#

	def on_20window_BUTTON_RUN_GMX_BUILDER (self, button, data=None):
		
		data_path      = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		system_name    = self.builder.get_object('20_window_GMX_entry_system_out').get_text()
		pymol_obj      = self.builder.get_object('20_window_GMX_entry_pdb_obj_in').get_text()
		
		ff_type        = self.builder.get_object('20_window_GMX_ff_type').get_active_text()
		water_type     = self.builder.get_object('20_window_GMX_cbox_solvate_water_type').get_active_text()
		diameter       = self.builder.get_object('20_window_GMX_solvate_diameter').get_text()
		conc           = self.builder.get_object('20_window_GMX_ionize_conc').get_text()       # concentration BOX
		
		pname = None
		np    = None
		nname = None
		nn    = None
		
		double = False
		if self.builder.get_object('20_window_GMX__check_GMX_double').get_active():
			double = True

		solvate = False
		if self.builder.get_object('20_window_GMX__check_GMX_solvate').get_active():
			solvate = True

		if self.builder.get_object('20_window_radiobutton1').get_active():
			ionize = None
		
		elif self.builder.get_object('20_window_radiobutton2').get_active():
			ionize = "custom"
			pname = self.builder.get_object('20_window_GMX_cbox1_IONIZE_positvie').get_active_text()
			np    = self.builder.get_object('20_window_GMX_entry_addions_positive').get_text()
			nname = self.builder.get_object('20_window_GMX_cbox1_IONIZE_negative').get_active_text()
			nn    = self.builder.get_object('20_window_GMX_entry_addions_negative').get_text()
			
		elif self.builder.get_object('20_window_radiobutton3').get_active():
			ionize = "neutral"
			pname = "NA"
			np    = "1"
			nname = "CL"
			nn    = "1"

		minimization  = False
		if self.builder.get_object('20_window_GMX_checkbutton_minimize').get_active():
			minimization  = True

		
		filein = self.GromacsProject.GMX_export_pdb_from_pymol(data_path, pymol_obj, ff_type)
		
		self.GromacsProject.GMX_make_pbd2gmx_run(data_path, 
												filein, 
												ff_type,     
												water_type,
												diameter,
												system_name,
												solvate,
												double,
												ionize,
												pname,
												np,
												nname,
												nn,
												minimization,
												conc)
		
	def on_20window_BUTTON_OPEN_MODIFY_GMX_DIALOG (self, button, data=None):
		""" Function doc """
		self.modify_GMX_window.run()
		self.modify_GMX_window.hide()	

	#======================================#
	# -       21_window_GMX -modify      - #
	#======================================#
	
	def on_21window_BUTTON_IMPORT_RESIDUE_INFORMATION(self, button, data=None):
		model = cmd.get_model("pk1")	
		index = []
		resn = None
		resi = None 
		
		for a in model.atom:
			resn = a.resn
			resi = a.resi
		self.builder.get_object('21_window_modify_entry_resi').set_text(resi)
		self.builder.get_object('21_window_modify_entry_resn').set_text(resn)			

	def on_21window_BUTTON_ADD_EXTRA_FILES_TO_LIST(self, button, data=None):	
		data_path      = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		resi_number    = self.builder.get_object('21_window_modify_entry_resi').get_text()
		resn_wild      = self.builder.get_object('21_window_modify_entry_resn').get_text()
		resn_mutant    = self.builder.get_object('21_window_modify_entry_resn2').get_text()

		modify_list    = self.GromacsProject.GMX_modify_addChangesToList( data_path, resi_number, resn_wild, resn_mutant)
		
		
		fin = ""
		for i in modify_list:							#
			fin = fin + i                		        #Just write the name of the uploaded files in a file called gaff_list.list
			
		text = fin
		buff = self.builder.get_object('21_window_modify_textview1_modify_ff_text_frame').get_buffer()    #
		buff.set_text(text)													                              #
		buff.set_modified(False)											                              # 

	def on_21window_BUTTON_CLEAN_LIST(self, button, data=None):
		self.GromacsProject.GMX_modify_CLEAN_LIST( )
		buff = self.builder.get_object('21_window_modify_textview1_modify_ff_text_frame').get_buffer()
		buff.set_text("Empty list")

	#======================================#
	# -       22_window_JOB HISTORY      - #
	#======================================#
	
	def insert_JOB_HISTORY_DATA (self, step, process, potencial, energy, time ):
		"""Step|Process|Potencial|Energy|Total_time"""
		model = self.builder.get_object("liststore1") #@+
		data  = [ str(step), process, potencial, energy, time]
		model.append( data)
		treeview = self.builder.get_object("22_window_treeview1")
		treeview.connect( "row-activated", self.row_activated)
		treeview.set_size_request( 400, 400)
	
	def novas_colunas(self, button, data=None):
		model = self.builder.get_object("liststore1") #@+
		data  = ['7', 'Minimization', 'QCMM', '-6500.12', '3:50']
		model.append( data)
		treeview = self.builder.get_object("22_window_treeview1")
		treeview.connect( "row-activated", self.row_activated)
		treeview.set_size_request( 400, 400)	

	def deleta_colunas(self, button, data=None):
		model = self.builder.get_object("liststore1") #@+
		#data  = ['7', 'Minimization', 'QCMM', '-6500.12', '3:50']
		treeview = self.builder.get_object("22_window_treeview1")

		selection = treeview.get_selection()
		model, iter = selection.get_selected()

		if iter:
			path = model.get_path(iter)[0]
			model.remove(iter)

			#del articles[ path ]	
		print path, model, iter

			
		
		treeview = self.builder.get_object("22_window_treeview1")
		treeview.connect( "row-activated", self.row_activated)
		treeview.set_size_request( 460, 400)

	#======================================#
	# -     23_window_QUICK_SCRIPT       - #
	#======================================#

	def run_quick_script(self, button, data=None):
		data_path  = self.builder.get_object("1window_main_dataPath_finder").get_filename()												
		
		buff = self.builder.get_object('23window_quick_script_textview1').get_buffer()
		#App.get_object('textview_quick_script').set_sensitive(False)
		text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
		#App.get_object('textview_quick_script').set_sensitive(True)
		buff.set_modified(False)

		# set the contents of the file to the text from the buffer
		fout = open(data_path + "/quick_script.py", "w")
		#else: fout = open(self.filename, "w")
		fout.write(text)
		fout.close()
		
		path = "run " + data_path + "/quick_script.py"
		cmd.do(path)
		if self.builder.get_object("23window_quick_script_checkbutton1").get_active():
			self.project.increment_step()
			self.project.export_frames_to_pymol('Qck', self.types_allowed , data_path)

			# JOB HISTORY
			step       =  self.project.step
			process    = "Quick scritp"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )

	#======================================#
	# -     24_window                    - #
	#======================================#

	def on_24window_BUTTON_RESCALE_CHARGES(self, button, data=None):	
		data_path       = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		selection       = self.builder.get_object('24window_entry1').get_text()
		total_charge    = int(self.builder.get_object('24window_entry2').get_text())
		output_filename = "chrg_table.index"
		
		index_table     = pymol_get_table(selection)
		charges         = self.project.system.energyModel.mmAtoms.AtomicCharges()
		
		charge_table    = []
		   
		for i in index_table:
			charge_table.append(charges[i])
			
		a = sum(charge_table)
		l = len(charge_table)
		frac = (total_charge - a)/l

		print "total charge = ", total_charge
		print "sum of total charges in the block = ", a
		print "fraction charges is = ", frac

		charges_new = []
		for i in charge_table:
			i = i + frac
			charges_new.append(i)
			
		print charges_new
		print sum(charges_new)
		
		
		charges.Print()
		n = 0
		for i in index_table:
			charges[i]=charges_new[n]
			n = n+1
		charges.Print()
		self.project.system.energyModel.mmAtoms.SetAtomicCharges(charges)

	#======================================#
	# -     25_window_UMBRELLA SAMPLING  - #
	#======================================#
	def on_25window_CHECKBOX_mass_weighted_restraints(self, button, data=None):
		try:
			name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
			name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
		except:
			print texto_d1
			print texto_d2d1
			return				
		if self.builder.get_object("25_window_umbrella_checkbox_mass_weight").get_active():
			self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
			
			"""
			   R                    R
				\                  /
				 A1--A2  . . . . A3
				/                  \ 
			   R                    R
				 ^   ^            ^
				 |   |            |
				pk1-pk2  . . . . pk3
				   d1       d2	
			
			q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
			
			"""			
			DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
			self.builder.get_object('25_window_umbrella_entry_param_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nUsing mass weighted restraints"
			print "Sigma pk1_pk3", self.sigma_pk1_pk3
			print "Sigma pk3_pk1", self.sigma_pk3_pk1
			print "Estimated minimum distance",  DMINIMUM
			
		else:
			self.sigma_pk1_pk3 =  1.0
			self.sigma_pk3_pk1 = -1.0
			DMINIMUM = distance_a1_a2 - distance_a2_a3
			self.builder.get_object('25_window_umbrella_entry_param_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
			print "Sigma pk3_pk1", self.sigma_pk3_pk1
			print "Estimated minimum distance",  DMINIMUM	

	def on_25window_IMPORT_PYMOL_DATA_1 (self, button, data=None):
		"""
		   R                    R
			\                  /
			 A1--A2  . . . . A3
			/                  \ 
		   R                    R
			 ^   ^            ^
			 |   |            |
			pk1-pk2  . . . . pk3
			   d1       d2	

		q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
		
		"""	
		
		mode        =  self.builder.get_object('25_umbrella_combobox1').get_active_text()
		
		self.sigma_pk1_pk3 = 0
		self.sigma_pk3_pk1 = 0

		if mode == "simple-distance":
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				distance_a1_a2 = str(distance_a1_a2)
				self.builder.get_object('25_window_umbrella_entry_param_DMINIMUM').set_text(distance_a1_a2)
				
				self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM1").set_text(str(atom1_index))
				self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM1_name").set_text(name1)
				self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM2").set_text(str(atom2_index))
				self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM2_name").set_text(name2)
				print '\nUsing simple distance\n'
				print "distance between atom 1 and atom 2: ",distance_a1_a2
			except:
				print texto_d1
			
		if mode == "multiple-distance":			
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
			
				print "distance between atom 1 and atom 2: ",distance_a1_a2
				print "distance between atom 2 and atom 3: ",distance_a2_a3
				
				if self.builder.get_object("25_window_umbrella_checkbox_mass_weight").get_active():
					
					
					self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
					
			
					
					DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
					self.builder.get_object('25_window_umbrella_entry_param_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nUsing mass weighted restraints"
					print "Sigma pk1_pk3", self.sigma_pk1_pk3
					print "Sigma pk3_pk1", self.sigma_pk3_pk1
					print "Estimated minimum distance",  DMINIMUM
					
				else:
					self.sigma_pk1_pk3 =  1.0
					self.sigma_pk3_pk1 = -1.0
					DMINIMUM = distance_a1_a2 - distance_a2_a3
					self.builder.get_object('25_window_umbrella_entry_param_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
					print "Sigma pk3_pk1", self.sigma_pk3_pk1
					print "Estimated minimum distance",  DMINIMUM	
			except:
				print texto_d2d1
				return			
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM1").set_text(str(atom1_index))
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM1_name").set_text(name1)
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM2").set_text(str(atom2_index))
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM2_name").set_text(name2)
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3").set_text(str(atom3_index))
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3_name").set_text(name3)

			
	def on_25window_COMBOBOX_CHANGE_REACTION_COORD_MODE (self, menuitem, data=None):
		""" Function doc """
		method = self.builder.get_object('25_umbrella_combobox1').get_active_text()
		if method == "simple-distance":
			self.builder.get_object("25_window_umbrella_SCAN_label_coord1_atom3").hide()
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3").hide()
			self.builder.get_object("25_window_umbrella_SCAN_label_cood1_ATOM3_name").hide()
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3_name").hide()
			self.builder.get_object("25_window_umbrella_checkbox_mass_weight").hide()
			#print texto_d1
			#self.builder.get_object('19_window_label1').set_text("Define atoms using pk1 and pk2 selections")
		if method == "multiple-distance":
			self.builder.get_object("25_window_umbrella_SCAN_label_coord1_atom3").show()
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3").show()
			self.builder.get_object("25_window_umbrella_SCAN_label_cood1_ATOM3_name").show()
			self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3_name").show()
			self.builder.get_object("25_window_umbrella_checkbox_mass_weight").show()
	
	def on_25window_COMBOBOX_CHANGE_MD_MODE (self, menuitem, data=None):
		MD_mode              =  self.builder.get_object('25_window_3_windowDynamics_Method_box').get_active_text()
		
		
		if MD_mode == "Velocity Verlet Dynamics":
			self.builder.get_object('25_window_collision_frequency').hide()
			self.builder.get_object('25_window_label_collision_freq').hide()
			self.builder.get_object('25_window_label_temp_scale').set_text('Temp Scale Frequency:')
			
		if MD_mode == "Leap Frog Dynamics":
			self.builder.get_object('25_window_collision_frequency').hide()
			self.builder.get_object('25_window_label_collision_freq').hide()
			self.builder.get_object('25_window_label_temp_scale').set_text('Temp coupling:')		
		if MD_mode == "Langevin Dynamics":		
			self.builder.get_object('25_window_collision_frequency').show()
			self.builder.get_object('25_window_label_collision_freq').show()
		""" Function doc """
					
	def on_25window_BUTTON_RUN_UMBRELLA(self, button, data=None):
		data_path      = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		
		self.GTKDynamo_and_Pymol_active_mode () #BETA
		
		# . import parameters
		DINCREMENT      = float(self.builder.get_object('25_window_umbrella_entry_STEP_SIZE').get_text())
		NWINDOWS        = int(self.builder.get_object('25_window_umbrella_entry_NWINDOWS').get_text())
		FORCECONSTANT   = float(self.builder.get_object('25_window_umbrella_entry_FORCE').get_text())
		traj_name       = self.builder.get_object('25_window_umbrella_entry_TRAJECTORY').get_text()
		DMINIMUM        = float(self.builder.get_object('25_window_umbrella_entry_param_DMINIMUM').get_text())
		
		
		# .  import trajectory parameters	
		
		if not os.path.exists (data_path + "/"+ traj_name): os.mkdir ( data_path + "/"+ traj_name)
		outpath = data_path + "/"+ traj_name
		
		# .  import MD parameters

		MDyn_dic             = {}
		MD_mode              =  self.builder.get_object('25_window_3_windowDynamics_Method_box').get_active_text()
		
		if MD_mode == "Velocity Verlet Dynamics":
			nsteps_EQ         = int(self.builder.get_object('25_window_steps_eq').get_text())
			nsteps_DC         = int(self.builder.get_object('25_window_steps_dc').get_text())
			temperature       = int(self.builder.get_object('25_window_temperature').get_text())
			temp_scale_freq   = int(self.builder.get_object('25_window_temp_scale_freq').get_text())
			timestep          = float(self.builder.get_object('25_window_timestep').get_text())
			trajectory_freq   = int(self.builder.get_object("25_window_traj_freq_dy").get_text())
			log_freq          = int(self.builder.get_object("25_window_log_freq_dy").get_text())
			seed              = int(self.builder.get_object('25_window_entry_seed_dy').get_text())
			coll_freq         = int(self.builder.get_object('25_window_collision_frequency').get_text())
			dualLog           = self.dualLog			
			
			MDyn_dic   =   {'MD_mode'         : MD_mode,
							'nsteps_EQ'       : nsteps_EQ,
							'nsteps_DC'       : nsteps_DC,
							'temperature'     : temperature,
							'temp_scale_freq' : temp_scale_freq,
							'timestep'        : timestep,
							'trajectory_freq' : trajectory_freq,
							'log_freq'        : log_freq,
							'seed'            : seed,
							'coll_freq'       : coll_freq}
			
		if MD_mode == "Leap Frog Dynamics":
			nsteps_EQ         = int(self.builder.get_object('25_window_steps_eq').get_text())
			nsteps_DC         = int(self.builder.get_object('25_window_steps_dc').get_text())
			temperature       = int(self.builder.get_object('25_window_temperature').get_text())
			temp_scale_freq   = int(self.builder.get_object('25_window_temp_scale_freq').get_text())
			timestep          = float(self.builder.get_object('25_window_timestep').get_text())
			trajectory_freq   = int(self.builder.get_object("25_window_traj_freq_dy").get_text())
			log_freq          = int(self.builder.get_object("25_window_log_freq_dy").get_text())
			seed              = int(self.builder.get_object('25_window_entry_seed_dy').get_text())
			coll_freq         = int(self.builder.get_object('25_window_collision_frequency').get_text())
			dualLog           = self.dualLog			
			
			MDyn_dic   =   {'MD_mode'             : MD_mode,
							'nsteps_EQ'           : nsteps_EQ,
							'nsteps_DC'           : nsteps_DC,
							'temperature'         : temperature,
							'temp_scale_freq'     : temp_scale_freq,
							'timestep'            : timestep,
							'trajectory_freq'     : trajectory_freq,
							'log_freq'            : log_freq,
							'seed'                : seed,
							'coll_freq'           : coll_freq,
							'temperatureCoupling' : 0.1 }	
				
		if MD_mode == "Langevin Dynamics":
			nsteps_EQ         = int(self.builder.get_object('25_window_steps_eq').get_text())
			nsteps_DC         = int(self.builder.get_object('25_window_steps_dc').get_text())
			temperature       = int(self.builder.get_object('25_window_temperature').get_text())
			temp_scale_freq   = int(self.builder.get_object('25_window_temp_scale_freq').get_text())
			timestep          = float(self.builder.get_object('25_window_timestep').get_text())
			trajectory_freq   = int(self.builder.get_object("25_window_traj_freq_dy").get_text())
			log_freq          = int(self.builder.get_object("25_window_log_freq_dy").get_text())
			seed              = int(self.builder.get_object('25_window_entry_seed_dy').get_text())
			coll_freq         = int(self.builder.get_object('25_window_collision_frequency').get_text())
			dualLog           = self.dualLog				
			MDyn_dic   =   {'MD_mode'             : MD_mode,
							'nsteps_EQ'           : nsteps_EQ,
							'nsteps_DC'           : nsteps_DC,
							'temperature'         : temperature,
							'timestep'            : timestep,
							'trajectory_freq'     : trajectory_freq,
							'log_freq'            : log_freq,
							'seed'                : seed,
							'coll_freq'           : coll_freq}

	
		# .  
	
		mode        =  self.builder.get_object('25_umbrella_combobox1').get_active_text()
		print mode

		if mode == "simple-distance":
			ATOM1      = int(self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM1").get_text())
			ATOM2      = int(self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM2").get_text())
			ATOM1_name = self.builder.get_object('25_window_umbrella_SCAN_entry_cood1_ATOM1_name').get_text()
			ATOM2_name = self.builder.get_object('25_window_umbrella_SCAN_entry_cood1_ATOM2_name').get_text()			
			
			
			print MDyn_dic
			x, y = self.project.run_umbrella_sampling (
												outpath, 
												ATOM1, 
												ATOM2,
												ATOM1_name,
												ATOM2_name, 
												DINCREMENT,
												NWINDOWS,
												FORCECONSTANT,
												DMINIMUM,
												traj_name, 
												MDyn_dic,
												dualLog )
		
			self.umbrella_window.hide()  #  I M P O R T A N T to close the window
			self.render_plot(x, y)
					
		if mode == "multiple-distance":
			ATOM1 = int(self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM1").get_text())
			ATOM2 = int(self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM2").get_text())
			ATOM3 = int(self.builder.get_object("25_window_umbrella_SCAN_entry_cood1_ATOM3").get_text())

			#name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
			#name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
			
			#print "\n\n"
			#print "  "+name1+"   ->-  "+name2+"  -->-- "+name3+"  "
			#print " pk1 --- pk2 ---- pk3 "
			#print "\n\n"			
			
			#print "distance between atom 1 and atom 2: ",distance_a1_a2
			#print "distance between atom 2 and atom 3: ",distance_a2_a3
			
			#sigma_pk1_pk3, sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
			
			#DMINIMUM = (distance_a1_a2 - distance_a2_a3)*-1
			
			#ATOM1    = atom1_index
			#ATOM2    = atom2_index
			#ATOM3    = atom3_index
	
			x, y = self.project.run_umbrella_sampling_d2_d1 (outpath, 
													  ATOM1, 
													  ATOM2, 
													  ATOM3,
													  DINCREMENT,
													  NWINDOWS,         # ok
													  FORCECONSTANT,    # ok
													  DMINIMUM,         # ok
													  self.sigma_pk1_pk3, 
													  self.sigma_pk3_pk1,
													  traj_name, 
													  MDyn_dic,
													  dualLog  )
		
		
			self.umbrella_window.hide()  #  I M P O R T A N T to close the window
			self.render_plot( x, y)
			
			# incrementing the step after Umbrella Sampling
			self.project.increment_step()
			
	#======================================#
	# -        26_window_SCAN 2D         - #
	#======================================#		

	def on_26window_CHECKBOX_mass_weighted_restraints_1(self, button, data=None):
		name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
		name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
		
		if self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord1").get_active():
			self.sigma_pk1_pk3_coord1, self.sigma_pk3_pk1_coord1 = compute_sigma_a1_a3 (name1, name3)
			
			"""
			   R                    R
				\                  /
				 A1--A2  . . . . A3
				/                  \ 
			   R                    R
				 ^   ^            ^
				 |   |            |
				pk1-pk2  . . . . pk3
				   d1       d2	
			
			q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
			
			"""			
			DMINIMUM =  (self.sigma_pk1_pk3_coord1 * distance_a1_a2) -(self.sigma_pk3_pk1_coord1 * distance_a2_a3*-1)
			self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nUsing mass weighted restraints"
			print "Sigma pk1_pk3", self.sigma_pk1_pk3_coord1
			print "Sigma pk3_pk1", self.sigma_pk3_pk1_coord1
			print "Estimated minimum distance",  DMINIMUM
			
		else:
			self.sigma_pk1_pk3_coord1 =  1.0
			self.sigma_pk3_pk1_coord1 = -1.0
			DMINIMUM = distance_a1_a2 - distance_a2_a3
			self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3_coord1
			print "Sigma pk3_pk1",      self.sigma_pk3_pk1_coord1
			print "Estimated minimum distance",  DMINIMUM	

	def on_26window_CHECKBOX_mass_weighted_restraints_2(self, button, data=None):
		name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
		name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
		
		if self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord2").get_active():
			self.sigma_pk1_pk3_coord2, self.sigma_pk3_pk1_coord2 = compute_sigma_a1_a3 (name1, name3)
			
			"""
			   R                    R
				\                  /
				 A1--A2  . . . . A3
				/                  \ 
			   R                    R
				 ^   ^            ^
				 |   |            |
				pk1-pk2  . . . . pk3
				   d1       d2	
			
			q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
			
			"""			
			DMINIMUM =  (self.sigma_pk1_pk3_coord2 * distance_a1_a2) -(self.sigma_pk3_pk1_coord2 * distance_a2_a3*-1)
			self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nUsing mass weighted restraints"
			print "Sigma pk1_pk3", self.sigma_pk1_pk3_coord2
			print "Sigma pk3_pk1", self.sigma_pk3_pk1_coord2
			print "Estimated minimum distance",  DMINIMUM
			
		else:
			self.sigma_pk1_pk3_coord2 =  1.0
			self.sigma_pk3_pk1_coord2 = -1.0
			DMINIMUM = distance_a1_a2 - distance_a2_a3
			self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').set_text(str(DMINIMUM))
			print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3_coord2
			print "Sigma pk3_pk1",      self.sigma_pk3_pk1_coord2
			print "Estimated minimum distance",  DMINIMUM

	def on_26window_IMPORT_PYMOL_DATA_1 (self, button, data=None):
		mode        =  self.builder.get_object('26_window_combobox_Reaction_coordiante1').get_active_text()
	
		if mode == "simple-distance":
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				distance_a1_a2 = str(distance_a1_a2)
				self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').set_text(distance_a1_a2)
				
				self.builder.get_object("26_window_scan2d_entry_ATOM1").set_text(str(atom1_index))
				self.builder.get_object("26_window_scan2d_entry_cood1_ATOM1_name").set_text(name1)
				self.builder.get_object("26_window_scan2d_entry_ATOM2").set_text(str(atom2_index))
				self.builder.get_object("26_window_scan2d_entry_cood1_ATOM2_name").set_text(name2)
			except:
				print texto_d1
				
		if mode == "multiple-distance":			
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
			
				print "distance between atom 1 and atom 2: ",distance_a1_a2
				print "distance between atom 2 and atom 3: ",distance_a2_a3
				
				if self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord1").get_active():
					
					
					self.sigma_pk1_pk3_coord1, self.sigma_pk3_pk1_coord1 = compute_sigma_a1_a3 (name1, name3)
					
					"""
					   R                    R
						\                  /
						 A1--A2  . . . . A3
						/                  \ 
					   R                    R
						 ^   ^            ^
						 |   |            |
						pk1-pk2  . . . . pk3
						   d1       d2	
					
					q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
					
					"""			
				
					DMINIMUM =  (self.sigma_pk1_pk3_coord1 * distance_a1_a2) -(self.sigma_pk3_pk1_coord1 * distance_a2_a3*-1)
					self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nUsing mass weighted restraints"
					print "Sigma pk1_pk3", self.sigma_pk1_pk3_coord1
					print "Sigma pk3_pk1", self.sigma_pk3_pk1_coord1
					print "Estimated minimum distance",  DMINIMUM
					
				else:
					self.sigma_pk1_pk3_coord1 =  1.0
					self.sigma_pk3_pk1_coord1 = -1.0
					DMINIMUM = distance_a1_a2 - distance_a2_a3
					self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3_coord1
					print "Sigma pk3_pk1", self.sigma_pk3_pk1_coord1
					print "Estimated minimum distance",  DMINIMUM				
			except:
				print texto_d2d1	
				return		
			self.builder.get_object("26_window_scan2d_entry_ATOM1").set_text(str(atom1_index))
			self.builder.get_object("26_window_scan2d_entry_cood1_ATOM1_name").set_text(name1)
			self.builder.get_object("26_window_scan2d_entry_ATOM2").set_text(str(atom2_index))
			self.builder.get_object("26_window_scan2d_entry_cood1_ATOM2_name").set_text(name2)
			self.builder.get_object("26_window_scan2d_entry_ATOM3").set_text(str(atom3_index))
			self.builder.get_object("26_window_scan2d_entry_cood1_ATOM3_name").set_text(name3)

			
	def on_26window_IMPORT_PYMOL_DATA_2 (self, button, data=None):
		mode        =  self.builder.get_object('26_window_combobox_Reaction_coordiante2').get_active_text()

		if mode == "simple-distance":
			try:
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				distance_a1_a2 = str(distance_a1_a2)
				self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').set_text(distance_a1_a2)
				
				self.builder.get_object("26_window_scan2d_entry_coord2_ATOM1").set_text(str(atom1_index))
				self.builder.get_object("26_window_scan2d_entry_cood2_ATOM1_name").set_text(name1)
				self.builder.get_object("26_window_scan2d_entry_coord2_ATOM2").set_text(str(atom2_index))
				self.builder.get_object("26_window_scan2d_entry_cood2_ATOM2_name").set_text(name2)
			except:
				print texto_d1
			
		if mode == "multiple-distance":
			try:						
				name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
				name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
			
				print "distance between atom 1 and atom 2: ",distance_a1_a2
				print "distance between atom 2 and atom 3: ",distance_a2_a3
				
				if self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord2").get_active():
					
					
					self.sigma_pk1_pk3_coord2, self.sigma_pk3_pk1_coord2 = compute_sigma_a1_a3 (name1, name3)
					
					"""
					   R                    R
						\                  /
						 A1--A2  . . . . A3
						/                  \ 
					   R                    R
						 ^   ^            ^
						 |   |            |
						pk1-pk2  . . . . pk3
						   d1       d2	
					
					q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
					
					"""			
					
					DMINIMUM =  (self.sigma_pk1_pk3_coord2 * distance_a1_a2) -(self.sigma_pk3_pk1_coord2 * distance_a2_a3*-1)
					self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nUsing mass weighted restraints"
					print "Sigma pk1_pk3", self.sigma_pk1_pk3_coord2
					print "Sigma pk3_pk1", self.sigma_pk3_pk1_coord2
					print "Estimated minimum distance",  DMINIMUM
					
				else:
					self.sigma_pk1_pk3_coord2 =  1.0
					self.sigma_pk3_pk1_coord2 = -1.0
					DMINIMUM = distance_a1_a2 - distance_a2_a3
					self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').set_text(str(DMINIMUM))
					
					print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3_coord2
					print "Sigma pk3_pk1", self.sigma_pk3_pk1_coord2
					print "Estimated minimum distance",  DMINIMUM	
			except:
				print texto_d2d1
				return			
			self.builder.get_object("26_window_scan2d_entry_coord2_ATOM1").set_text(str(atom1_index))
			self.builder.get_object("26_window_scan2d_entry_cood2_ATOM1_name").set_text(name1)
			self.builder.get_object("26_window_scan2d_entry_coord2_ATOM2").set_text(str(atom2_index))
			self.builder.get_object("26_window_scan2d_entry_cood2_ATOM2_name").set_text(name2)
			self.builder.get_object("26_window_scan2d_entry_coord2_ATOM3").set_text(str(atom3_index))
			self.builder.get_object("26_window_scan2d_entry_cood2_ATOM3_name").set_text(name3)
		

	def on_26window_COMBOBOX_COOD1(self, menuitem, data=None):
		""" Function doc """
		
		method = self.builder.get_object('26_window_combobox_Reaction_coordiante1').get_active_text()
		if method == "simple-distance":
			self.builder.get_object("26_window_scan2d_label_coord1_atom3").hide()
			self.builder.get_object("26_window_scan2d_entry_ATOM3").hide()
			self.builder.get_object("26_window_scan2d_label_cood1_ATOM3_name").hide()
			self.builder.get_object("26_window_scan2d_entry_cood1_ATOM3_name").hide()
			self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord1").hide()
			#print texto_d1
			#self.builder.get_object('19_window_label1').set_text("Define atoms using pk1 and pk2 selections")
		if method == "multiple-distance":
			self.builder.get_object("26_window_scan2d_label_coord1_atom3").show()
			self.builder.get_object("26_window_scan2d_entry_ATOM3").show()
			self.builder.get_object("26_window_scan2d_label_cood1_ATOM3_name").show()
			self.builder.get_object("26_window_scan2d_entry_cood1_ATOM3_name").show()
			self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord1").show()
			#print texto_d2d1	
	def on_26window_COMBOBOX_COOD2(self, menuitem, data=None):
		""" Function doc """
		
		method = self.builder.get_object('26_window_combobox_Reaction_coordiante2').get_active_text()
		if method == "simple-distance":
			self.builder.get_object("26_window_scan2d_label_coord2_atom3").hide()
			self.builder.get_object("26_window_scan2d_entry_coord2_ATOM3").hide()
			self.builder.get_object("26_window_scan2d_label_cood2_ATOM3_name").hide()
			self.builder.get_object("26_window_scan2d_entry_cood2_ATOM3_name").hide()
			self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord2").hide()
	
			#print texto_d1
			
			#self.builder.get_object('19_window_label1').set_text("Define atoms using pk1 and pk2 selections")
		if method == "multiple-distance":
			self.builder.get_object("26_window_scan2d_label_coord2_atom3").show()
			self.builder.get_object("26_window_scan2d_entry_coord2_ATOM3").show()
			self.builder.get_object("26_window_scan2d_label_cood2_ATOM3_name").show()
			self.builder.get_object("26_window_scan2d_entry_cood2_ATOM3_name").show()
			self.builder.get_object("26_window_scan2d_checkbox_mass_weight_coord2").show()
			#print texto_d2d1

			
	def on_26window_BUTTON_RUN_SCAN_2D(self, button, data=None):
		""" Function doc """
		data_path      =  self.builder.get_object("1window_main_dataPath_finder").get_filename()
		mode1          =  self.builder.get_object('26_window_combobox_Reaction_coordiante1').get_active_text()
		mode2          =  self.builder.get_object('26_window_combobox_Reaction_coordiante2').get_active_text()
		
		self.GTKDynamo_and_Pymol_active_mode () #BETA
		
		# . import parameters
		NWINDOWS1         = int(self.builder.get_object('26_window_scan2d_entry_coord1_NWINDOWS').get_text())
		NWINDOWS2         = int(self.builder.get_object('26_window_scan2d_entry_coord2_NWINDOWS').get_text())

		DMINIMUM1         = self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').get_text()
		DMINIMUM2         = self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').get_text()

		FORCECONSTANT1    = float(self.builder.get_object('26_window_scan2d_entry_coord1_FORCE_CONSTANT').get_text())
		FORCECONSTANT2    = float(self.builder.get_object('26_window_scan2d_entry_coord2_FORCE_CONSTANT').get_text())
		
		DINCREMENT1       = float(self.builder.get_object('26_window_scan2d_entry_coord1_STEP_SIZE').get_text())
		DINCREMENT2       = float(self.builder.get_object('26_window_scan2d_entry_STEP_SIZE2').get_text())
		

		sigma_pk1_pk3_coord1 = self.sigma_pk1_pk3_coord1 
		sigma_pk3_pk1_coord1 = self.sigma_pk3_pk1_coord1 
		
		sigma_pk1_pk3_coord2 = self.sigma_pk1_pk3_coord2 
		sigma_pk3_pk1_coord2 = self.sigma_pk3_pk1_coord2 
		

		if mode1 == "simple-distance":
			REACTION_COORD1 = {
								'mode'          :  mode1,
								'atom1'         :  int(self.builder.get_object('26_window_scan2d_entry_ATOM1').get_text()),
								'atom1_name'    :      self.builder.get_object('26_window_scan2d_entry_cood1_ATOM1_name').get_text(),
								'atom2'         :  int(self.builder.get_object('26_window_scan2d_entry_ATOM2').get_text()),
								'atom2_name'    :      self.builder.get_object('26_window_scan2d_entry_cood1_ATOM2_name').get_text(),
								'DMINIMUM1'     :  float(self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').get_text()),

								'DINCREMENT1'   : float(self.builder.get_object('26_window_scan2d_entry_coord1_STEP_SIZE').get_text()),
								'NWINDOWS1'     : int(self.builder.get_object('26_window_scan2d_entry_coord1_NWINDOWS').get_text()),
								'FORCECONSTANT1': float(self.builder.get_object('26_window_scan2d_entry_coord1_FORCE_CONSTANT').get_text())}
								#'DINCREMENT1'   : float(self.builder.get_object('26_window_scan2d_entry_coord1_STEP_SIZE').get_text())}
			
			
			atom1_name = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM1_name').get_text()
			atom2_name = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM2_name').get_text()
			
			YLABEL = " r( "+ atom1_name+ " - " + atom2_name + ")"
		
		if mode1 == "multiple-distance":	
			REACTION_COORD1 = {
								'mode'       : mode1,
								'atom1'      : int(self.builder.get_object('26_window_scan2d_entry_ATOM1').get_text()),
								'atom1_name' :     self.builder.get_object('26_window_scan2d_entry_cood1_ATOM1_name').get_text(),
								'atom2'      : int(self.builder.get_object('26_window_scan2d_entry_ATOM2').get_text()),
								'atom2_name' :     self.builder.get_object('26_window_scan2d_entry_cood1_ATOM2_name').get_text(),
								'atom3'      : int(self.builder.get_object('26_window_scan2d_entry_ATOM3').get_text()),
								'atom3_name' :     self.builder.get_object('26_window_scan2d_entry_cood1_ATOM3_name').get_text(),
								
								'sigma_pk1_pk3_coord1' : sigma_pk1_pk3_coord1,
								'sigma_pk3_pk1_coord1' : sigma_pk3_pk1_coord1,
								
								
								'DMINIMUM1'     :  float(self.builder.get_object('26_window_scan2d_entry_coord1_DMINIMUM').get_text()),

								'DINCREMENT1'   : float(self.builder.get_object('26_window_scan2d_entry_coord1_STEP_SIZE').get_text()),
								'NWINDOWS1'     : int(self.builder.get_object('26_window_scan2d_entry_coord1_NWINDOWS').get_text()),
								'FORCECONSTANT1': float(self.builder.get_object('26_window_scan2d_entry_coord1_FORCE_CONSTANT').get_text())}
								
			atom1_name = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM1_name').get_text()
			atom2_name = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM2_name').get_text()
			atom3_name = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM3_name').get_text()
			
			YLABEL = " r( "+ atom1_name+ " - " + atom2_name + " - " + atom3_name + ")"						
		
		if mode2 == "simple-distance":
			REACTION_COORD2 = {
								'mode'       : mode2,
								'atom1'      :   int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM1').get_text()),
								'atom1_name' :       self.builder.get_object('26_window_scan2d_entry_cood2_ATOM1_name').get_text(),
								'atom2'      :   int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM2').get_text()),
								'atom2_name' :       self.builder.get_object('26_window_scan2d_entry_cood2_ATOM2_name').get_text(),
								'DMINIMUM2'  : float(self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').get_text()),

								'DINCREMENT2'   : float(self.builder.get_object('26_window_scan2d_entry_STEP_SIZE2').get_text()),
								'NWINDOWS2'     :   int(self.builder.get_object('26_window_scan2d_entry_coord2_NWINDOWS').get_text()),
								'FORCECONSTANT2': float(self.builder.get_object('26_window_scan2d_entry_coord2_FORCE_CONSTANT').get_text())}
								#'DINCREMENT2'   : float(self.builder.get_object('26_window_scan2d_entry_STEP_SIZE2').get_text())}
			
			atom1_name = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM1_name').get_text()
			atom2_name = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM2_name').get_text()
			
			XLABEL = " r( "+ atom1_name+ " - " + atom2_name +")"
			
		if mode2 == "multiple-distance":	
			REACTION_COORD2 = {
								'mode'       : mode2,
								'atom1'      :   int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM1').get_text()),
								'atom1_name' :       self.builder.get_object('26_window_scan2d_entry_cood2_ATOM1_name').get_text(),
								'atom2'      :   int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM2').get_text()),
								'atom2_name' :       self.builder.get_object('26_window_scan2d_entry_cood2_ATOM2_name').get_text(),
								'atom3'      :   int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM3').get_text())   ,
								'atom3_name' :       self.builder.get_object('26_window_scan2d_entry_cood2_ATOM3_name').get_text(),
								'DMINIMUM2'  : float(self.builder.get_object('26_window_scan2d_entry_coord2_DMINIMUM').get_text()),

								'sigma_pk1_pk3_coord2' : sigma_pk1_pk3_coord2,
								'sigma_pk3_pk1_coord2' : sigma_pk3_pk1_coord2, 

								'DINCREMENT2'   : float(self.builder.get_object('26_window_scan2d_entry_STEP_SIZE2').get_text())           ,
								'NWINDOWS2'     : int(self.builder.get_object('26_window_scan2d_entry_coord2_NWINDOWS').get_text())        ,
								'FORCECONSTANT2': float(self.builder.get_object('26_window_scan2d_entry_coord2_FORCE_CONSTANT').get_text())}
			
			# ploting label 
			atom1_name = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM1_name').get_text()
			atom2_name = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM2_name').get_text()
			atom3_name = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM3_name').get_text()
			
			XLABEL = " r( "+ atom1_name+ " - " + atom2_name + " - " + atom3_name + ")"		
		
		
									
		#ATOM1             = int(self.builder.get_object('26_window_scan2d_entry_ATOM1').get_text())
		#ATOM2             = int(self.builder.get_object('26_window_scan2d_entry_ATOM2').get_text())
		#ATOM3             = int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM1').get_text())
		#ATOM4             = int(self.builder.get_object('26_window_scan2d_entry_coord2_ATOM2').get_text())


		#name1 = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM1_name').get_text()
		#name2 = self.builder.get_object('26_window_scan2d_entry_cood1_ATOM2_name').get_text()		
		#name3 = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM1_name').get_text()
		#name4 = self.builder.get_object('26_window_scan2d_entry_cood2_ATOM2_name').get_text()		
		
		
		#YLABEL = " r( "+ name1+ " - " + name2 + ")"
		#XLABEL = " r( "+ name3+ " - " + name4 + ")"
		
		
		max_int        = int(self.builder.get_object("26_window_scan2d_entry_max_int").get_text())
		log_freq       = 1
		rms_grad       = float(self.builder.get_object("26_window_scan2d_entry_rmsd_grad").get_text())			
		mim_method	   = self.builder.get_object('26_window_scan2d_combobox3').get_active_text()
		
		
		# .  import trajectory parameters	
		traj            = self.builder.get_object('26_window_scan2d_entry_mim_param_TRAJECTORY').get_text()
	
		if not os.path.exists (data_path + "/"+ traj): os.mkdir ( data_path + "/"+ traj)
		outpath = data_path + "/"+ traj	
		
		#mode        =  self.builder.get_object('19_window_combobox1_scan_method').get_active_text()
		mode = "scan 2D"
		print "\n\n"
		print mode 		
		
		
		if mode == "scan 2D":

			PARAMETERS = {	'max_int' : max_int, 
							'log_freq': log_freq,
							'rms_grad': rms_grad }
			
			X, X_norm = self.project.run_SCAN_2D_2  (
											  outpath, 
											  REACTION_COORD1,
											  REACTION_COORD2,
											  PARAMETERS,
											  mim_method,   
											  self.dualLog)			
			self.SCAN_window.hide()
			
			#-incrementing the step after SCAN2D-#
			self.project.increment_step()
			#------------------------------------#
			print X_norm
			
			self.SCAN_2D_window.hide()
			self.render_plot_matrix(X_norm, xlabel = XLABEL, ylabel = YLABEL  )
			
			#=============== generating the minimum energy reaction path ========================#
			#	plot 1D                                                                          #
			#														                             #
			#	lista - contain  the  energy valors 				                             #
			#	frame_list include the coordinates x and y (matrix)                              #
			#------------------------------------------------------------------------------------#
			
			lista , frame_list = self.minimum_path(X_norm)

			if not os.path.exists (outpath + "/MinimumPath"): os.mkdir (outpath + "/MinimumPath")
			MinimumPath = outpath + "/MinimumPath"	
			import shutil
			
			n = 0
			arq  = open(outpath+"/MinimumPath"+"/"+"process.log", "w")	                 #creates an process.log to save the minimum path energy data generated by the GTKDyn
			text = "----------  Generated by GTKDynamo  ----------\n\nThis proceeding might generate artifacts, the results should be interpreted with caution.\nFor further information, please acess: https://sites.google.com/site/gtkdynamo/ \n\nEnergy values in kJ/mol\n\n"
			
			
			#text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (coord2_ATOM1,     coord2_ATOM1_name)
			for i in frame_list:
				shutil.copy2(outpath + '/frame_'+i+'.pkl', MinimumPath+'/frame'+str(n)+'.pkl')
				
				frame_x_y = 'frame_'+i+'.pkl'
				frame_new = 'frame'+str(n)+'.pkl'
				energy    =  str(lista[n])
				
				string = '%15s   --->   %15s   =   %15s\n' % (frame_x_y, frame_new, energy)
				
				#string = 'frame_'+i+'.pkl   --->  frame'+str(n)+'.pkl    = '+ str(lista[n])+' kJ/mol\n'
				text = text + string
				n = n + 1

			#=====================================================================================#	
			arq.writelines(text)
			arq.close()
			
			frames = range(len(lista))
			self.render_plot( frames, lista )
			#render_plot(self, x, y, title = 'GTK Dynamo', xlabel = 'Frame', ylabel = 'Energy (kJ/mol)', grid_flag = True)
			return 0
            #(self, matrix, title = 'GTK Dynamo 2D SCAN', xlabel = 'r(3 - 4)', ylabel = 'r(1 - 2)'):
	
	
	def minimum_path(self,X):
		lista = []
		px = 0
		py = 0

		# rminimum path energy frames
		frame_list = []
		frame = str(px)+ "_" +str(py)
		frame_list.append(frame)


		print X[px][py]
		lista.append(X[px][py])
		while 1 != 0:
			try:
				p1 = X[px+1][py+0]
			except:
				p1 = 1000000000000000
			try:
				p2 = X[px+0][py+1]
			except:
				p2 = 1000000000000000
			try:	
				p3 = X[px+1][py+1]
			except:
				p3 = 1000000000000000		
			
			
			if p3 < p2 and p3 < p1:
				print p3
				px = px + 1
				py = py + 1
				lista.append(p3)

				frame = str(px)+ "_" +str(py)
				frame_list.append(frame)
				
			if p2 < p1 and p2 < p3:
				print p2
				px = px + 0
				py = py + 1
				lista.append(p2)

				frame = str(px)+ "_" +str(py)
				frame_list.append(frame)
				
			if p1 < p2 and p1 < p3:
				print p1
				px = px + 1
				py = py + 0
				lista.append(p1)

				frame = str(px)+ "_" +str(py)
				frame_list.append(frame)
				
				
			if p1 == 1000000000000000 and p2 == 1000000000000000 and p3 == 1000000000000000:
				break
		return lista , frame_list
	
	
	
	
	

	#==============================#
	#    27 - NBModel properties   # 
	#==============================#

	def  on_27window_BUTTON_APPLY_PROPERTIES(self, button, data=None):
		""" Function doc """
		
		nbModel_type = self.builder.get_object("27_window_nbmodel_comobobox_new_system").get_active_text()
		innerCutoff  = float(self.builder.get_object("27_window_innercutoff_entry_new_system").get_text())
		outerCutoff  = float(self.builder.get_object("27_window_outercutoff_entry_new_system").get_text())
		listCutoff   = float(self.builder.get_object("27_window_listcutoff_entry_new_system").get_text())
		kappa        = self.builder.get_object("27_window_kappa_entry_new_system").get_text()
		
		self.project.settings['nbModel_type'] = nbModel_type
		self.project.settings['ABFS_options'] = { "innerCutoff" : innerCutoff , "outerCutoff" : outerCutoff , "listCutoff"  : listCutoff }
		
		# nbModel applied
		self.project.set_nbModel_to_system()


	#==============================#
	#    29 - PDYNAMO SELECTION    # 
	#==============================#
	
	def on_29window_build_treeview(self):
		data_path      =  self.builder.get_object("1window_main_dataPath_finder").get_filename()
		treeview = self.builder.get_object("29_pdynamo_selection_treeview1")		
		model    = self.builder.get_object("29_pdynamo_selection_liststore1") 
		model.clear()
		
		PDBFile_FromSystem (data_path + "/my_system_full.pdb", self.project.system)
		AMBER_READ  = open (data_path + "/my_system_full.pdb", "r")

		for line in AMBER_READ:						
			line2 = line.split()				
			line1 = line[0:6]					
			if line1 == "ATOM  " or line1 == "HETATM" :	

				index   = line[6:11]	
				A_name  = line[11:16]	
				resn    = line[16:20] 	
				chain   = line[20:22]	
				resi    = line[22:26]	
				gap     = line[26:30]	
				x       = line[30:38]	
				y       = line[38:46]	
				z       = line[46:54]	
										
				b       = line[54:60]	
				oc      = line[60:66]	
				gap2    = line[66:76]	
				atom    = line[76:78] 	
				
				index2  = index.split()
				index2  = int(index2[0])			

						
				A_name2 = A_name.split()		
				A_name2 = A_name2[0]				


				resn2 = resn.split()
				resn2 = resn2[0]

				
				#chain2 = chain.split()
				#chain2 = chain2[0]

				
				resi2 = resi.split()
				resi2 = int(resi2[0])			

				
				atom2 = atom.split()
				atom2 = atom2[0]			
				if chain   == "  ":
					chain2 = 'A' 
				else:
					chain2 = chain.split()
					chain2 = chain2[0]
					
				lista  = ( index2, A_name2, resn2, chain2, resi2, atom2 )
				
				self.project.pdbInfo[index2] = [resn2, chain2, resi2, A_name2]
				model.append(lista)

	def on_29window_row_activated(self, tree, path, column):
		"""Function that activate the liststore and get the str_teste that will be use in the combobox_SELECTION_METHOD function"""

			
		model = self.builder.get_object("29_pdynamo_selection_liststore1") 
		treeview = self.builder.get_object("29_pdynamo_selection_treeview1")
		selection = treeview.get_selection()
		model, iter = selection.get_selected()
		
		str_teste = "%s:%s.%s:%s" %(model.get_value(iter, 3), model.get_value(iter, 2), model.get_value(iter, 4), model.get_value(iter, 1))
		self.builder.get_object('29_pdynamo_selection_entry1').set_text(model.get_value(iter, 3))
		self.builder.get_object('29_pdynamo_selection_entry2').set_text(model.get_value(iter, 2))
		self.builder.get_object('29_pdynamo_selection_entry3').set_text(model.get_value(iter, 4))
		self.builder.get_object('29_pdynamo_selection_entry4').set_text(model.get_value(iter, 1))
		
		index    = model.get_value( iter, 0) #@+
		
		pymol_obj = self.project.settings['last_pymol_id']
		string    = 'zoom ('+pymol_obj+ ' and  index '+ index + ')'
		string2   = 'select ('+pymol_obj+ ' and  index '+ index + ')'
		
		cmd.do(string)
		cmd.do(string2)		
		
		
	def on_29window_combobox_SELECTION_METHOD(self, button, data=None):
		"""Fucntion that permits select atoms from pDynamo arguments"""
		#system      = self.project.system
		
		model       = self.builder.get_object("29_pdynamo_selection_liststore1") 
		treeview    = self.builder.get_object("29_pdynamo_selection_treeview1")
		selection   = treeview.get_selection()
		model, iter = selection.get_selected()

		
		#str_teste = "*:%s.%s:%s" %(model.get_value(iter, 2), model.get_value(iter, 4), model.get_value(iter, 1))
		#self.builder.get_object('29_pdynamo_selection_entry1').set_text(model.get_value(iter, 3))
		#self.builder.get_object('29_pdynamo_selection_entry2').set_text(model.get_value(iter, 2))
		#self.builder.get_object('29_pdynamo_selection_entry3').set_text(model.get_value(iter, 4))
		#self.builder.get_object('29_pdynamo_selection_entry4').set_text(model.get_value(iter, 1))
		
		
		iter3 = self.builder.get_object('29_pdynamo_selection_entry1').get_text()
		iter2 = self.builder.get_object('29_pdynamo_selection_entry2').get_text()
		iter4 = self.builder.get_object('29_pdynamo_selection_entry3').get_text()
		iter1 = self.builder.get_object('29_pdynamo_selection_entry4').get_text()

		str_teste = "*:%s.%s:%s" %(iter2, iter4, iter1)
		
		import_type2    =   self.builder.get_object("29_pdynamo_selection_combobox2").get_active_text()

		import_type     = self.builder.get_object("29_pdynamo_selection_combobox1").get_active_text()
		selection_type  = self.builder.get_object("29_pdynamo_selection_combobox1").get_active_text()
		radius_distance = float(self.builder.get_object("29_pdynamo_selection_radius_distance_entry1").get_text())

		print str_teste
		pymolIndex   = AtomSelection.FromAtomPattern ( self.project.system, str_teste )
		pymolIndex	 = pymolIndex.Within ( radius_distance )
		
		
		
		if selection_type == "ByComponent":
			pymolIndex	  = pymolIndex.ByComponent()
			self.builder.get_object("selectionByAtomSelectionMode")
			
			pymolIndex	 = Selection ( pymolIndex )
			#self.project.system = PruneByAtom ( self.project.system, pymolIndex )

		
		if selection_type == "Complement":
			pymolIndex	 = pymolIndex.Complement()
			self.builder.get_object("selectionByAtomSelectionMode")
			
			pymolIndex	 = Selection ( pymolIndex )
			#self.project.system.DefineFixedAtoms ( pymolIndex )


		if selection_type == "ByLinearPolymer":
			pymolIndex	 = pymolIndex.ByLinearPolymer()
			self.builder.get_object("selectionByAtomSelectionMode")
			
			pymolIndex	 = Selection ( pymolIndex )		
		
		#print pymolIndex
		index_list = list(pymolIndex)

		if 	import_type2 == "Select in PyMOl":
			# export data to pymol 
			try:
				cmd.delete("sele")
			except:
				a = None

			pymol_put_table (index_list, "sele")
			pymol_id  = self.project.settings['last_pymol_id'] 
			string22  = 'select sele, ('+pymol_id+ ' and  sele )'
			cmd.do(string22)				

		if 	import_type2 == "FIX atoms":
			self.project.system.DefineFixedAtoms ( pymolIndex )
			# export data to pymol 
			try:
				cmd.delete("FIX_atoms")
			except:
				a = None
			
			self.project.settings['fix_table'] = index_list
			
			pymol_put_table (index_list, "FIX_atoms")
			
			pymol_id  = self.project.settings['last_pymol_id'] 
			string22  = 'select FIX_atoms, ('+pymol_id+ ' and  FIX_atoms )'
			cmd.do(string22)
			string5  = 'color grey80, FIX_atoms'
			cmd.do(string5)			
			
		if 	import_type2 == "PRUNE atoms":
			data_path      =  self.builder.get_object("1window_main_dataPath_finder").get_filename()
			self.project.system = PruneByAtom ( self.project.system, pymolIndex )
			
			# exporting data to pymol 
			self.project.increment_step()                                               # step
			self.project.check_system(self.dualLog)                                     # Check System
			self.project.export_frames_to_pymol('prn', self.types_allowed , data_path)	# Loading the actual frame in pymol.		
			# JOB HISTORY
			step       =  self.project.step
			process    = "prune system"
			potencial  = self.project.settings["potencial"]
			energy     = " - "
			time       = " - " 
			self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )
 		#cbox.append_text("FIX atoms")
		#cbox.append_text("QC region atoms")
		#cbox.append_text("PRUNE atoms")

	def on_29window_importResidueInformation(self, button, data=None):
		model = cmd.get_model("pk1")
		index = []
		resn = None
		resi = None 
		for a in model.atom:
			#resn = a.resn
			#resi = a.resi
			#print resn
			#print resi
			#print a.index
			index = a.index
			print  a.index, self.project.pdbInfo[index]    #  17 = ['TYR', 'P', 2, 'C']
			
			
			chain     = self.project.pdbInfo[index][1]
			resn      = self.project.pdbInfo[index][0]
			resi      = self.project.pdbInfo[index][2]
			atom_name = self.project.pdbInfo[index][3]
			
			self.builder.get_object('29_pdynamo_selection_entry1').set_text(chain)
			self.builder.get_object('29_pdynamo_selection_entry2').set_text(resn)
			self.builder.get_object('29_pdynamo_selection_entry3').set_text(str(resi))
			self.builder.get_object('29_pdynamo_selection_entry4').set_text(atom_name)
	 
 

	def on_29window_combobox_IMPORT_AS(self, menuitem, data=None):
		"""Function that set the type of selection"""
		
		import_type =   self.builder.get_object("29_pdynamo_selection_combobox2").get_active_text()

		if import_type == "FIX atoms":
			self.builder.get_object("29_pdynamo_selection_image1").set_from_file("lock3_50_50.png")

		if import_type == "QC region atoms":	
			self.builder.get_object("29_pdynamo_selection_image1").set_from_file("h2o3_50_50.png")

		if import_type == "PRUNE atoms":	
			self.builder.get_object("29_pdynamo_selection_image1").set_from_file("scissors3.png")



	#===========================#
	#    30 - PDYNAMO SAW       # 
	#===========================#

	def take_SAW_parameters(self):
		NEB_number_of_structures = int(self.builder.get_object('7_window_NEB_number_of_structures').get_text())
		NEB_maximum_interations  = int(self.builder.get_object('7_window_NEB_maximum_interations').get_text())
		NEB_grad_tol             = float(self.builder.get_object('7_window_NEB_grad_tol').get_text())
		trajectory_name          = self.builder.get_object('7_window_NEB__pd_traj_out').get_text()
		data_path  	 	         = self.builder.get_object("1window_main_dataPath_finder").get_filename()

		# reactants
		if self.builder.get_object('7_window_checkbutton_REACTANTS').get_active():
			reactants_file          = self.builder.get_object('7_window_filechooserbutton_REACTANTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('7_window_entry_REACTANTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "reactants_NEB.xyz"	
			reactants_file          = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)			
		
		
		# products
		if self.builder.get_object('7_window_checkbutton_PRODUCTS').get_active():
			products_file       = self.builder.get_object('7_window_filechooserbutton_PRODUCTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('7_window_entry_PRODUCTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "products_NEB.xyz"	
			products_file           = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)
		print      NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol , trajectory_name, data_path, reactants_file, products_file
		return     NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol , trajectory_name, data_path, reactants_file, products_file

	def on_30window_BUTTON_RUN_SAW(self, button, data=None):
		SAW_number_of_structures = int(self.builder.get_object('30_window_SAW_number_of_structures').get_text())
		SAW_maximum_interations  = int(self.builder.get_object('30_window_SAW_maximum_interations').get_text())
		SAW_gamma                = float(self.builder.get_object('30_window_SAW_gamma').get_text())
		trajectory_name          = self.builder.get_object('30_window_SAW_pd_traj_out').get_text()
		data_path  	 	         = self.builder.get_object("1window_main_dataPath_finder").get_filename()

	
		# reactants
		if self.builder.get_object('30_window_checkbutton_REACTANTS').get_active():
			print ""
			#reactants_file          = self.builder.get_object('30_window_filechooserbutton_REACTANTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('30_window_entry_REACTANTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "reactants_SAW.xyz"	
			reactants_file          = pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)			
		
		if self.builder.get_object('30_window_checkbutton_PRODUCTS').get_active():
			print ""
			#products_file       = self.builder.get_object('30_window_filechooserbutton_PRODUCTS').get_filename()
		else:
			pymol_object            = self.builder.get_object('30_window_entry_PRODUCTS').get_text()
			label       	        = pymol_object + " XYZ file"
			file_out                = "products_SAW.xyz"	
			products_file           =pymol_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)
		plot_flag  = False

		if self.builder.get_object('30_window_SAW_Check_print_graf').get_active():
			plot_flag  = True			
		
		x, y, t = self.project.run_SAW( reactants_file, products_file, 	data_path, SAW_number_of_structures, SAW_maximum_interations, SAW_gamma, trajectory_name, plot_flag, self.dualLog )
		                               #reactants_file, products_file, data_path, NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol, trajectory_name, plot_flag, dualLog ):
		     
		print "total time = ", t
			
		self.window_30_SAW.hide()  #  I M P O R T A N T E , se nao a janela nao fecha.
		self.render_plot( x, y)
		
		# incrementing the step after SAW
		self.project.increment_step()	
	"""
	def on_30window_CHECKBUTTON_REACTANTS(self, checkbutton, data=None):
		if self.builder.get_object("7_window_checkbutton_REACTANTS").get_active():
			self.builder.get_object("7_window_filechooserbutton_REACTANTS").show()
			self.builder.get_object("7_window_entry_REACTANTS").hide()
		else:
			self.builder.get_object("7_window_filechooserbutton_REACTANTS").hide()
			self.builder.get_object("7_window_entry_REACTANTS").show()

	def on_30window_CHECKBUTTON_PRODUCTS(self, checkbutton, data=None):
		if self.builder.get_object("7_window_checkbutton_PRODUCTS").get_active():
			self.builder.get_object("7_window_filechooserbutton_PRODUCTS").show()
			self.builder.get_object("7_window_entry_PRODUCTS").hide()
		else:
			self.builder.get_object("7_window_filechooserbutton_PRODUCTS").hide()
			self.builder.get_object("7_window_entry_PRODUCTS").show()		
	"""	
	
	
	"""
	def on_dialog_activate(self, menuitem, data=None):
		self.Dialog.run()
		self.merge_window.hide()
	"""		
		
		
		
	"""
	about_dialog = gtk.Dialog(title=None, parent=None, flags=DIALOG_MODAL, buttons=None)
	def close(dialog, response, editor):
		editor.about_dialog = None
		dialog.destroy()
		
	def delete_event(dialog, event, editor):
		editor.about_dialog = None
		return True	
	about_dialog.connect("response", close, self)
	about_dialog.connect("delete-event", delete_event, self)
		
	self.about_dialog = about_dialog
	about_dialog.show()
	"""		
	def on_about_menu_item_activate(self, menuitem, data=None):
		
		#       - Jose Fernando R Bachega  < Univesity of Sao Paulo - SP, Brazil                              >
		#       - Troy Wymore              < Pittsburgh Super Computer Center, Pittsburgh PA - USA            >
		#       - Martin Field             < Institut de Biologie Structurale, Grenoble, France               >		
		#       - Richard Garratt          < Univesity of Sao Paulo - SP, Brazil                              >
		#       - Luis Fernando S M Timmers< Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
		#       - Lucas Assirati           < Univesity of Sao Paulo - SP, Brazil                              >
		#       - Leonardo R Bachega       < University of Purdue - West Lafayette, IN - USA                  >
		
		if self.about_dialog: 
			self.about_dialog.present()
			return
		
		authors = [
		"Jose Fernando R Bachega   <ferbachega@gmail.com.com>",
		"Luis Fernando S M Timmers <luisfernandosaraiva@gmail.com>",
		"Troy Wymore               <wymoretw@ornl.gov>",
		"Martin J. Field           <martin.john.field@gmail.com>"
		]

		about_dialog = gtk.AboutDialog()
		about_dialog.set_transient_for(self.window)
		about_dialog.set_destroy_with_parent(True)
		about_dialog.set_name("GTKDynamo")
		about_dialog.set_version("0.1.7")
		about_dialog.set_copyright("Copyright \xc2\xa9 2013 J.F.R. Bachega")
		about_dialog.set_website("https://sites.google.com/site/gtkdynamo/")
		about_dialog.set_comments("A pDynamo interface")
		about_dialog.set_authors            (authors)
		#about_dialog.set_logo_icon_name     (gtk.STOCK_EDIT)
		about_dialog.set_logo(gtk.gdk.pixbuf_new_from_file("Logo100x100.png"))
		# callbacks for destroying the dialog
		def close(dialog, response, editor):
			editor.about_dialog = None
			dialog.destroy()
			
		def delete_event(dialog, event, editor):
			editor.about_dialog = None
			return True
					
		about_dialog.connect("response", close, self)
		about_dialog.connect("delete-event", delete_event, self)
		
		self.about_dialog = about_dialog
		about_dialog.show()
	#=====================#
	#    T O O L B A R    # 
	#=====================#
	# -  1_window -  main


		#self.project = DynamoProject()
		#cmd.reinitialize()
		

	def update_data_path_from_settings_to_GUI(self, data_path):
		#data_path = self.project.settings['data_path']
		#cmd.do('cd '+data_path)
		self.builder.get_object('1window_main_entry_prmtop').set_current_folder(data_path)				#
		self.builder.get_object('1window_main_entry_crd').set_current_folder(data_path)
		self.builder.get_object('1window_main_entry_prm_opls').set_current_folder(data_path)				#
		self.builder.get_object('1window_main_xyzc').set_current_folder(data_path)
		self.builder.get_object('9_window_data_path_finder_new_system').set_current_folder(data_path)
		#SAW
		#self.builder.get_object('filechooserbutton_reactants_SAW').set_current_folder(data_path)
		#self.builder.get_object('filechooserbutton_products_SAW').set_current_folder(data_path)
		#NEB
		#self.builder.get_object('filechooserbutton_reactants_NEB').set_current_folder(data_path)
		#self.builder.get_object('filechooserbutton_products_NEB').set_current_folder(data_path)
		
		#Import lists
		#self.builder.get_object('1window_main_load_QC_table_entry').set_current_folder(data_path)
		#self.builder.get_object('1window_main_load_fix_table_chooser_button').set_current_folder(data_path)
		
		#tleap
		#self.builder.get_object('filechooserbutton_tleap_ff_mol2').set_current_folder(data_path)
		#self.builder.get_object('filechooserbutton_tleap_pdb').set_current_folder(data_path)
		#self.builder.get_object('OPLS_TOP').set_current_folder(data_path)
		#self.builder.get_object('OPLS_PDB').set_current_folder(data_path)

		#save project - Definitions
		#self.builder.get_object('directory_Save_project').set_current_folder(data_path)
		#Load project - Definitions
		
		#self.builder.get_object('directory_Save_project').set_current_folder(data_path)
		#self.builder.get_object('import_coord_from_file').set_current_folder(data_path)
		
		
		#self.builder.get_object('entry_top_new_system').set_current_folder(data_path)				#
		#self.builder.get_object('entry_crd_new_system').set_current_folder(data_path)
		#self.builder.get_object('entry_top_opls_new_system').set_current_folder(data_path)				#
		#self.builder.get_object('xyzc_new_system').set_current_folder(data_path)
		#self.builder.get_object('data_path_finder_new_system').set_current_folder(data_path)

	# O P E N  - just  testing 

	def get_open_filename_log(self, data = None):  # abre janela de procura
		data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		filename = None
		chooser = gtk.FileChooserDialog("Open File...", self.window,
										gtk.FILE_CHOOSER_ACTION_OPEN,
										(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
										 gtk.STOCK_OPEN, gtk.RESPONSE_OK))

		filter = gtk.FileFilter()             #  adiciona o filtro de busca de arquivos
		filter.set_name("GTKDynamo logs - *.log")    #
		filter.add_mime_type("GTKDynamo logs")  #
		filter.add_pattern("*.log")

		chooser.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		
		chooser.add_filter(filter)	          # termina  - filtro de arquivos.
		chooser.set_current_folder(data_path)
		response = chooser.run()
		if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
		chooser.destroy()

		return filename	

	def get_open_filename(self, data = None):  # abre janela de procura
		data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		filename = None
		chooser = gtk.FileChooserDialog("Open File...", self.window,
										gtk.FILE_CHOOSER_ACTION_OPEN,
										(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
										 gtk.STOCK_OPEN, gtk.RESPONSE_OK))

		filter = gtk.FileFilter()             #  adiciona o filtro de busca de arquivos
		filter.set_name("GTKDynamo projects - *.gtkdyn")    #
		
		filter.add_mime_type("GTKDynamo projects")  #
		filter.add_pattern("*.gtkdyn")
		
		chooser.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("pDynamo pkl files  - *.pkl")
		filter.add_pattern("*.pkl")


		chooser.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("pDynamo yaml files  - *.yaml")
		filter.add_pattern("*.yaml")
		
		chooser.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		
		chooser.add_filter(filter)	          # termina  - filtro de arquivos.
		chooser.set_current_folder(data_path)
		response = chooser.run()
		if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
		chooser.destroy()

		return filename	

	# S A V E  - just  testing 
	
	def get_save_filename(self, data = None):  # abre janela de procura
		data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		filename = None
		chooser = gtk.FileChooserDialog("Save File...", self.window,
										gtk.FILE_CHOOSER_ACTION_SAVE,
										(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
										 gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		chooser.set_current_folder(data_path)
		response = chooser.run()
		if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
		chooser.destroy()

		return filename	


	def render_plot_matrix (self, matrix, title = 'GTK Dynamo 2D SCAN', xlabel = 'r(3 - 4)', ylabel = 'r(1 - 2)'):
		""" Function doc """
		from matplotlib.figure import Figure
		from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
		from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
		
		
		win = gtk.Window()
		win.connect("destroy", lambda x: gtk.main_quit())
		win.set_default_size(580,420)
		win.set_title(title)
		

		
		vbox = gtk.VBox()
		win.add(vbox)
				
		import matplotlib.pyplot as plt
		import matplotlib.cm as cm	
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		im = ax.imshow(matrix, cmap=cm.jet, interpolation='nearest')
		from pylab import contour
		from pylab import clabel

		c = contour(matrix, colors = 'k', linewidths = (1,))
		clabel(c, fmt = '%2.1f', colors = 'k', fontsize=14)
		
		from pylab import colorbar
		colorbar(im)
		

		
		#im1=ax.imshow([[1,2],[2, 3]])
		#plt.colorbar(im1, cax=ax, orientation="horizontal", ticks=[1,2,3])
		#ax.imshow(matrix, cmap=cm.jet, interpolation='nearest', extent=(-4.1,4.5,-4,4))
		
		from pylab import grid
		#ax.imshow(matrix, cmap=cm.jet, interpolation='bilinear')
		
		grid(True)
		
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		
		#cb = plt.colorbar(0,10)
		#cb.set_label('counts')		
		
		canvas = FigureCanvas(fig)  # a gtk.DrawingArea
		vbox.pack_start(canvas)
		toolbar = NavigationToolbar(canvas, win)
		vbox.pack_start(toolbar, False, False)


		win.show_all()
		gtk.main()		
	
	def render_plot        (self, x, y, title = 'GTK Dynamo', xlabel = 'Frame', ylabel = 'Energy (kJ/mol)', grid_flag = True):
		
		from matplotlib.figure import Figure
		from numpy import arange, sin, pi
		from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
		from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar


		win = gtk.Window()
		win.connect("destroy", lambda x: gtk.main_quit())
		win.set_default_size(580,420)
		win.set_title(title)

		vbox = gtk.VBox()
		win.add(vbox)
		
		fig = Figure(figsize=(5,4), dpi=100)
		ax = fig.add_subplot(111)
		ax.plot(x, y, 'ko',x, y,'k')
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.grid(grid_flag)
		

			
		canvas = FigureCanvas(fig)  # a gtk.DrawingArea
		vbox.pack_start(canvas)
		toolbar = NavigationToolbar(canvas, win)
		vbox.pack_start(toolbar, False, False)


		win.show_all()
		gtk.main()	
												
	
	def load_config_file(self):
		try:
			setup=open( "config.dynamo")
			for line in setup:
				line2 = line.split()
				if line2[0] == "project_folder":
					project_folder = line2[2]
					print project_folder
					self.builder.get_object("1window_main_dataPath_finder").set_current_folder(line2[2])
		except:
			project_folder = home
		return  project_folder

	def save_config_file(self):
		arq = open("config.dynamo", 'w')
		data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
		
	
		text=[]
		project_folder = "project_folder = "
		text.append(project_folder)
		text.append(data_path + "\n")
		arq.writelines(text)
		arq.close()
		#print "The file: config.dynamo, has been updeted"
		#print "your working folder is now: ", data_path	
		
	
	
	def debug_project_variables(self, data = None):
		print "\n\n\n        -------------- GTKDynamo Varable debuger ----------------\n\n"
		
		print "----- Project Variables -----\n"

		for i in self.project.settings:
			print "var     %15s   =   %1s" %(i , self.project.settings[i])
		#"\nATOM1                  =%15i  ATOM NAME1             =%15s" % (ATOM1,  ATOM1_name)

		print "\n\n\n----- GUI Variables -----\n"
		print self.home
		print self.scratch        
		print self.dualLog        
		print self.types_allowed  

      
		print "project", self.project        
		print self.filename       
		print self.about_dialog   
		print self.AmberProject   
		print self.GromacsProject 
		print self.new_lig        

		#GUI variables	
		print self.sigma_pk1_pk3 
		print self.sigma_pk3_pk1 

		print self.sigma_pk1_pk3_coord1 
		print self.sigma_pk3_pk1_coord1 
		print self.sigma_pk1_pk3_coord2 
		print self.sigma_pk3_pk1_coord2 		

		#PRoject variables
		print self.project_name  
		print self.script_step   
		
		
		
		
		
		
		
		
		
		
		
		
		

	def SETUP_COMBOBOXES (self):
		""" Function doc """
		builder = self.builder
		cbox = builder.get_object('1window_main_combobox_MM_model')   #  ----> combobox_MM_model
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("AMBER")
		cbox.append_text("CHARMM")
		cbox.append_text("GROMACS")
		cbox.append_text("OPLS")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)
		
		# N E W  S Y S T E M
		cbox = builder.get_object('9_window_combobox_MM_model_new_system')   #  ----> combobox_MM_model
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("AMBER")
		cbox.append_text("CHARMM")
		cbox.append_text("GROMACS")
		cbox.append_text("OPLS")
		#cbox.append_text("pkl - pDynamo")
		#cbox.append_text("yaml - pDynamo")
		cbox.append_text("Coordinates (*.pkl,*.yaml,*.pdb,*.xyz,*.mol,*.mol2...)")
		cbox.append_text("PyMOL Object")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		
		
		
		cbox = builder.get_object('9_window_nbmodel_comobobox_new_system')   #  ----> combobox_MM_model
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("NBModelFull")
		cbox.append_text("NBModelABFS")
		cbox.append_text("NBModelGABFS")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(1)		
		
		# NBModel properties
		
		cbox = builder.get_object('27_window_nbmodel_comobobox_new_system')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("NBModelFull")
		cbox.append_text("NBModelABFS")
		cbox.append_text("NBModelGABFS")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(1)			
		
		####################
		
		cbox = builder.get_object('1window_main_QC_FIX_PRUNE_combo') #  ----> qc_method_combobox
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("FIX atoms")
		cbox.append_text("QC region atoms")
		cbox.append_text("PRUNE atoms")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)
					
		####################
		
		cbox = builder.get_object('1window_main_qc_method_combobox') #  ----> qc_method_combobox
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		for i in self.mndo_list:
			cbox.append_text(i)
		'''
		cbox.append_text("am1")
		cbox.append_text("pm3")
		cbox.append_text("pm6")
		cbox.append_text("rm1")
		cbox.append_text("chops")
		#cbox.append_text("pddg")
		#cbox.append_text("pddg/pm3")
		'''
		for i in self.DFT_list:
			cbox.append_text(i)		
		'''
		cbox.append_text("DFT - demon, lda, 321g")
		cbox.append_text("DFT - demon, blyp, 321g")
		cbox.append_text("DFT - ahlrichs, lda, 631gs")
		cbox.append_text("DFT - ahlrichs, blyp, 631gs")
		cbox.append_text("DFT - weigend, lda, svp")
		cbox.append_text("DFT - weigend, blyp, svp")
		'''		
		cbox.append_text("ORCA - ab initio")
		#cbox.append_text("DFT - pDynamo")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)
			
		####################
		cbox = builder.get_object('1window_main_combobox_coordToSys_or_coordNewSys') #  ----> combobox_coordToSys_or_coordNewSys
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("Coordinates to System")
		cbox.append_text("New System")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)
		
		cbox = builder.get_object('14_window_combobox_coordToSys_or_coordNewSys')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("Coordinates to System")
		cbox.append_text("New System")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)				
		####################
		
	#  ===  combobox_methods_ORCA  ===
		cbox = builder.get_object('6_window_combobox1_ORCA_method')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
				
		for i in self.HF_list:
			cbox.append_text(i)
		for i in self.KS_list:
			cbox.append_text(i)	
		"""		
		# HF
		cbox.append_text("HF - Hartree-Fock")
	
		# MP2
		cbox.append_text("MP2")
		
		# DFT
		cbox.append_text("LDA    - Local density approximation")
		cbox.append_text("BLYP   - Becke '88 exchange and Lee-Yang-Parr correlation")
		cbox.append_text("mPWPW  - Modified PW exchange and PW correlation")
		cbox.append_text("mPWLYP - Modified PW exchange and LYP correlation")
		
		cbox.append_text("TPSSh - The hybrid version of TPSS")

		cbox.append_text("B3LYP - The popular B3LYP functional (20% HF exchange)")
		cbox.append_text("B3PW - The three parameter hybrid version of PW91")
		cbox.append_text("PW1PW - One parameter hybrid version of PW91")
		cbox.append_text("mPW1PW - One parameter hybrid version of mPWPW")
		cbox.append_text("mPW1LYP - One parameter hybrid version of mPWLYP")
		cbox.append_text("PBE0 - One parameter hybrid version of PBE")
		"""
		
		"""
		# DFT
		cbox.append_text("HFS Hartree-Fock-Slater Exchange only functional")
		cbox.append_text("LDA Local density approximation")
		cbox.append_text("VWN5 Vosko-Wilk-Nusair local density approx")
		cbox.append_text("VWN3 Vosko-Wilk-Nusair local density approx.")
		cbox.append_text("PWLDA Perdew-Wang parameterization of LDA")
		cbox.append_text("BP86 Becke '88 exchange and Perdew '86 correlation")
		cbox.append_text("BLYP Becke '88 exchange and Lee-Yang-Parr correlation")
		cbox.append_text("OLYP Handy's 'optimal' exchange and Lee-Yang-Parr correlation")
		cbox.append_text("GLYP Gill's '96 exchange and Lee-Yang-Parr correlation")
		cbox.append_text("XLYP The Xu and Goddard exchange and Lee-Yang-Parr correlation")
		cbox.append_text("PW91 Perdew-Wang '91 GGA functional")
		cbox.append_text("mPWPW Modified PW exchange and PW correlation")
		cbox.append_text("mPWLYP Modified PW exchange and LYP correlation")
		cbox.append_text("PBE Perdew-Burke-Erzerhoff GGA functional")
		cbox.append_text("RPBE 'Modified' PBE")
		cbox.append_text("REVPBE 'Revised' PBE")
		cbox.append_text("PWP Perdew-Wang '91 exchange and Perdew 86 correlation")
		
		# Hybrid 
		cbox.append_text("B1LYP The one-parameter hybrid Becke'88 exchange and LYP correlation (25% HF exchange)")
		cbox.append_text("B3LYP The popular B3LYP functional (20% HF exchange)")
		cbox.append_text("O3LYP The Handy hybrid functional")
		cbox.append_text("X3LYP The Xu and Goddard hybrid functional")
		cbox.append_text("B1P The one parameter hybrid version of BP86")
		cbox.append_text("B3P The three parameter hybrid version of BP86")
		cbox.append_text("B3PW The three parameter hybrid version of PW91")
		cbox.append_text("PW1PW One parameter hybrid version of PW91")
		cbox.append_text("mPW1PW One parameter hybrid version of mPWPW")
		cbox.append_text("mPW1LYP One parameter hybrid version of mPWLYP")
		cbox.append_text("PBE0 One parameter hybrid version of PBE")
		"""
		
		
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)      

		# - trajectory refine
		
		cbox = builder.get_object('31_window_combobox1_ORCA_method')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
				
		for i in self.HF_list:
			cbox.append_text(i)
		for i in self.KS_list:
			cbox.append_text(i)			
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		'''   
		#        o erro na inicializacao do programa:  
		#          
		#        /usr/lib/pymodules/python2.7/pymol/__init__.py:1259: GtkWarning: gtk_combo_box_real_get_active_text: 
		#        assertion `GTK_IS_LIST_STORE (combo_box->priv->model)' failed
		#
		#        ocorre neste ponto - nos demais cbox.set_active(0) da jalena 6_window_combobox3_ORCA_basis
		#		 obs: este erro nao esta prejudicando em nada o desempenho do programa
		'''
	
	
	#  ===  combobox_basis_ORCA  ===  
		cbox = builder.get_object('6_window_combobox3_ORCA_basis')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )

		cbox.append_text("3-21G Pople 3-21G")
		#cbox.append_text("3-21GSP Buenker 3-21GSP")
		#cbox.append_text("4-22GSP Buenker 4-22GSP")
		cbox.append_text("6-31G Pople 6-31G and its modifications")
		cbox.append_text("6-311G Pople 6-311G and its modifications")
		
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		

		# - trajectory refine
		
		cbox = builder.get_object('31_window_combobox3_ORCA_basis')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )

		cbox.append_text("3-21G Pople 3-21G")
		#cbox.append_text("3-21GSP Buenker 3-21GSP")
		#cbox.append_text("4-22GSP Buenker 4-22GSP")
		cbox.append_text("6-31G Pople 6-31G and its modifications")
		cbox.append_text("6-311G Pople 6-311G and its modifications")
		
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)


	#  ===  combobox_POLARIZATION_ORCA  ===  

		cbox = builder.get_object('6_window_combobox2_ORCA_POLARIZATION')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		
		cbox.append_text("No")
		cbox.append_text("*")
		cbox.append_text("**")
		cbox.append_text("(2d)")
		cbox.append_text("(2d,2p)")
		cbox.append_text("(2df)")
		cbox.append_text("(2df,2pd)")
		cbox.append_text("(3df)")
		cbox.append_text("(3df,3pd)")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)



		# - trajectory refine
		cbox = builder.get_object('31_window_combobox2_ORCA_POLARIZATION')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		
		cbox.append_text("No")
		cbox.append_text("*")
		cbox.append_text("**")
		cbox.append_text("(2d)")
		cbox.append_text("(2d,2p)")
		cbox.append_text("(2df)")
		cbox.append_text("(2df,2pd)")
		cbox.append_text("(3df)")
		cbox.append_text("(3df,3pd)")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)


	#  ===  combobox_DIFFUSE_ORCA  ===  

		cbox = builder.get_object('6_window_combobox2_ORCA_DIFFUSE')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )

		cbox.append_text("No")
		cbox.append_text("+")
		cbox.append_text("++")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)

		# - trajectory refine
		cbox = builder.get_object('31_window_combobox2_ORCA_DIFFUSE')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )

		cbox.append_text("No")
		cbox.append_text("+")
		cbox.append_text("++")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)

	#  ===  combobox_SCF_ORCA  ===  
		cbox = builder.get_object('6_window_combobox2_ORCA_SCF')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("NORMALSCF")
		cbox.append_text("LOOSESCF")
		cbox.append_text("SLOPPYSCF")
		cbox.append_text("STRONGSCF")
		cbox.append_text("TIGHTSCF")
		cbox.append_text("VERYTIGHTSCF")
		cbox.append_text("EXTREMESCF")
		cbox.append_text("SCFCONV6")
		cbox.append_text("SCFCONV7")
		cbox.append_text("SCFCONV8")			
		cbox.append_text("SCFCONV9")
		cbox.append_text("SCFCONV10")
		
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)


		# - trajectory refine
		cbox = builder.get_object('31_window_combobox2_ORCA_SCF')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("NORMALSCF")
		cbox.append_text("LOOSESCF")
		cbox.append_text("SLOPPYSCF")
		cbox.append_text("STRONGSCF")
		cbox.append_text("TIGHTSCF")
		cbox.append_text("VERYTIGHTSCF")
		cbox.append_text("EXTREMESCF")
		cbox.append_text("SCFCONV6")
		cbox.append_text("SCFCONV7")
		cbox.append_text("SCFCONV8")			
		cbox.append_text("SCFCONV9")
		cbox.append_text("SCFCONV10")
		
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)



	#  ===  Surface_window  ===  
		cbox = builder.get_object('8_window_combobox_surface')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("density")
		cbox.append_text("orbital")
		cbox.append_text("potential")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)	


	#  ===  combobox_Minimization_window  ===  
		cbox = builder.get_object('2_window_mim_Method_box')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("Conjugate Gradient")
		cbox.append_text("Steepest Descent")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)	


	#  ===  combobox_Molecular Dynamics  ===  

		cbox = builder.get_object('3_windowDynamics_Method_box')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store)
		cbox.append_text("Velocity Verlet Dynamics")
		cbox.append_text("Leap Frog Dynamics")
		cbox.append_text("Langevin Dynamics")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)

	#  ===  combobox_TLEAP ===  

		cbox = builder.get_object('15_window_TLEAP_ff_model')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("ff99SB")
		cbox.append_text("ff99SBildn")
		cbox.append_text("ff99SBnmr")
		cbox.append_text("ff99bsc0")
		cbox.append_text("ff99SB")
		cbox.append_text("ffAM1")
		cbox.append_text("ffPM3")
		cbox.append_text("ff02polEP")
		cbox.append_text("ff02pol")
		cbox.append_text("ff03")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)
		
		
		cbox = builder.get_object('15_window_TLEAP_ff_model_gly')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("GLYCAM_04EP")
		cbox.append_text("GLYCAM_06")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(1)

		cbox = builder.get_object('15_window_TLEAP_cbox_solvate_water_model')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("TIP3P")
		cbox.append_text("TIP4P")
		cbox.append_text("TIP5P")
		cbox.append_text("TIP6P")
		cbox.append_text("TIP7P")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)

		cbox = builder.get_object('15_window_TLEAP_cbox1_IONIZE_positvie')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("Na+")
		cbox.append_text("K+")
		cbox.append_text("Mg2+")
		cbox.append_text("Cs+")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)
		
		cbox = builder.get_object('15_window_TLEAP_cbox1_IONIZE_negative')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("Cl-")
		cbox.append_text("Br-")
		#cbox.append_text("Mg2+")
		#cbox.append_text("Cs+")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		
		# A N T E C H A M B E R 
		
		cbox = builder.get_object('16_window_ANTECHAMBER_combobox_charge_antechamber')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("AM1-BCC")
		cbox.append_text("RESP")
		cbox.append_text("Mulliken")
		cbox.append_text("Gasteiger")
		cbox.append_text("ESP-Kollman")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		
		# G M X
		"""	
		 1: AMBER03 protein, nucleic AMBER94 (Duan et al., J. Comp. Chem. 24, 1999-2012, 2003)
		 2: AMBER94 force field (Cornell et al., JACS 117, 5179-5197, 1995)
		 3: AMBER96 protein, nucleic AMBER94 (Kollman et al., Acc. Chem. Res. 29, 461-469, 1996)
		 4: AMBER99 protein, nucleic AMBER94 (Wang et al., J. Comp. Chem. 21, 1049-1074, 2000)
		 5: AMBER99SB protein, nucleic AMBER94 (Hornak et al., Proteins 65, 712-725, 2006)
		 6: AMBER99SB-ILDN protein, nucleic AMBER94 (Lindorff-Larsen et al., Proteins 78, 1950-58, 2010)
		 7: AMBERGS force field (Garcia & Sanbonmatsu, PNAS 99, 2782-2787, 2002)
		 8: CHARMM27 all-atom force field (with CMAP) - version 2.0
		14: OPLS-AA/L all-atom force field (2001 aminoacid dihedrals)
		"""		
		
		cbox = builder.get_object('20_window_GMX_ff_type')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("amber03")
		cbox.append_text("amber94")
		cbox.append_text("amber96")
		cbox.append_text("amber99")
		cbox.append_text("amber99sb")
		cbox.append_text("amber99sb-ildn")
		cbox.append_text("amberGS")
		cbox.append_text("charmm27")
		#cbox.append_text("oplsaa")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)

		"""	
		1: TIP3P   TIP 3-point, recommended
		2: TIP4P   TIP 4-point
		3: TIPS3P  CHARMM TIP 3-point with LJ on H's (note: twice as slow in GROMACS)
		4: SPC     simple point charge
		5: SPC/E   extended simple point charge
		6: None
		"""	
		
		cbox = builder.get_object('20_window_GMX_cbox_solvate_water_type')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("tip3p")
		cbox.append_text("tip4p")
		cbox.append_text("tip4p-ew")
		cbox.append_text("spc")
		cbox.append_text("spc/e")
		cbox.append_text("none")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		



		cbox = builder.get_object('20_window_GMX_cbox1_IONIZE_positvie')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("NA")
		cbox.append_text("K")
		cbox.append_text("MG")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		
		cbox = builder.get_object('20_window_GMX_cbox1_IONIZE_negative')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("CL")
		#cbox.append_text("BR")
		#cbox.append_text("MG")

		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)	

		
		
		# SAVE FRAME
		
		cbox = builder.get_object('17_window_SAVE_FRAME_combobox_file_type')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("xyz")
		cbox.append_text("pkl")
		cbox.append_text("yaml")
		cbox.append_text("pdb")
		cbox.append_text("cif")
		cbox.append_text("mol")
		cbox.append_text("mol2")
		cbox.append_text("crd")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(1)
		
		
		# SCAN 
		
		cbox = builder.get_object('19_window_SCAN_combobox_Reaction_coordiante2')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("simple-distance")
		cbox.append_text("multiple-distance")
		#cbox.append_text("umbrella d1")
		#cbox.append_text("scan 2D")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)				
		
		cbox = builder.get_object('26_window_combobox_Reaction_coordiante1')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("simple-distance")
		cbox.append_text("multiple-distance")
		#cbox.append_text("umbrella d1")
		#cbox.append_text("scan 2D")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)			
		
		cbox = builder.get_object('26_window_combobox_Reaction_coordiante2')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("simple-distance")
		cbox.append_text("multiple-distance")
		#cbox.append_text("umbrella d1")
		#cbox.append_text("scan 2D")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		

		cbox = builder.get_object('26_window_scan2d_combobox2')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("Conjugate Gradient")
		cbox.append_text("Steepest Descent")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)	

		cbox = builder.get_object('26_window_scan2d_combobox3')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model(store )
		cbox.append_text("Conjugate Gradient")
		cbox.append_text("Steepest Descent")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)	
		
		
		# UMBRELLA SAMPLING
		
		cbox = builder.get_object('25_umbrella_combobox1')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("simple-distance")
		cbox.append_text("multiple-distance")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)				
		
		cbox = builder.get_object('25_window_3_windowDynamics_Method_box')
		store = gtk.ListStore(gobject.TYPE_STRING)
		#print store
		cbox.set_model(store )
		cbox.append_text("Velocity Verlet Dynamics")
		cbox.append_text("Leap Frog Dynamics")
		cbox.append_text("Langevin Dynamics")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)		
		
		#---------------------------#
		#   29 pDynamo selections   #
		#---------------------------#

		cbox = builder.get_object('29_pdynamo_selection_combobox1')
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model( store )
		cbox.append_text("ByComponent")
		cbox.append_text("Complement")
		#cbox.append_text("ByEntity")
		#cbox.append_text("ByIsolate")
		#cbox.append_text("ByLinearPolymer")
		#cbox.append_text("ByRingSet")
		#cbox.append_text("ByBondedNeighbor")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)

		cbox = builder.get_object("29_pdynamo_selection_combobox2")
		store = gtk.ListStore(gobject.TYPE_STRING)
		cbox.set_model( store )
		cbox.append_text("Select in PyMOl")
		cbox.append_text("FIX atoms")
		#cbox.append_text("QC region atoms")
		cbox.append_text("PRUNE atoms")
		cell = gtk.CellRendererText()
		cbox.pack_start(cell, True)
		cbox.add_attribute(cell, 'text', 0)  
		cbox.set_active(0)




		
	def SETUP_HSCALE(self):
		#Hscale
		builder = self.builder
		scale = builder.get_object("4_window_hscale1")
		scale.set_range(0, 100)
		scale.set_increments(1, 10)
		scale.set_digits(0)	

	def SETUP_SPIN_BUTTONS (self):
		""" Function doc """
		# Pdynamo QC config 
		builder = self.builder
		adjustment1 = gtk.Adjustment(0.0, -500.0, 500.0, 1.0, 0.0, 0.0)
		adjustment2 = gtk.Adjustment(0.0, 1.0, 500.0, 1.0, 0.0, 0.0)
		entry_chrg = builder.get_object("1window_main_entry_chrg")
		entry_chrg.set_adjustment(adjustment1)
		entry_mult = builder.get_object("1window_main_entry_mult")
		entry_mult.set_adjustment(adjustment2)

		# Ambertools - Antechamber 
		adjustment3 = gtk.Adjustment(0.0, -500.0, 500.0, 1.0, 0.0, 0.0)
		adjustment4 = gtk.Adjustment(0.0, 1.0, 500.0, 1.0, 0.0, 0.0)		
		
		entry_chrg_ante = builder.get_object("16_window_ANTECHAMBER_entry_chrg_antechamber")
		entry_chrg_ante.set_adjustment(adjustment3)
		entry_mult_ante = builder.get_object("16_window_ANTECHAMBER_entry_mult_antechamber")
		entry_mult_ante.set_adjustment(adjustment4)
		
		# ORCA setup window
		adjustment_ORCA_pal = gtk.Adjustment(0.0, 1.0, 500.0, 1.0, 0.0, 0.0)
		SpinButton1_ORCA_pal = builder.get_object("6_window_SpinButton1_ORCA_pal")
		SpinButton1_ORCA_pal.set_adjustment(adjustment_ORCA_pal)	
	
	def SETUP_HIDE_WIDGETS(self):
		self.builder.get_object('7_window_filechooserbutton_REACTANTS').hide()
		self.builder.get_object('7_window_filechooserbutton_PRODUCTS').hide()
		self.builder.get_object("1window_main_import_coord_from_file").hide()
		self.builder.get_object("1window_main_entry_prm_opls").hide()
		self.builder.get_object("1window_main_import_table_from_file1").hide()		

		#self.builder.get_object('').hide()
		#self.builder.get_object('').hide()
		self.builder.get_object('30_window_filechooserbutton_REACTANTS').hide()
		self.builder.get_object('30_window_filechooserbutton_PRODUCTS').hide()
		self.builder.get_object('30_window_checkbutton_REACTANTS').hide()
		self.builder.get_object('30_window_checkbutton_PRODUCTS').hide()
		
		self.builder.get_object('9_window_checkbutton_MOL2_type').hide()
	def SETUP_TREEVIEW (self):
		# model creation
		#model = self.builder.get_object("liststore3") #@+
		#f = open('amberlist.txt', "r")
		#for line in f:
		#	line2 = line.split("|")
		#	data = []
			
		#	model.append(line2)
		#f.close()
		# the treeview
		#treeview = self.builder.get_object("22_window_treeview2")
		#treeview.connect( "row-activated", self.row_activated) #@+
		#treeview.set_size_request( 400, 400) 		
		treeview = self.builder.get_object("16_window_treeview1")
		treeview.connect( "row-activated", self.row_activated)	
		
		treeview = self.builder.get_object("16_window_treeview2")
		treeview.connect( "row_activated", self.on_16window_TREEVIEW_row_activated)

		#treeview = self.builder.get_object("4_window_treeview1")
		#treeview.connect( "row_activated", self.on_4_window_row_activated)
		
		model    = self.builder.get_object("liststore1") #@+
		treeview = self.builder.get_object("22_window_treeview1")
		treeview.connect( "row-activated", self.row_activated) #@+
		treeview.set_size_request( 400, 400)














	def __init__(self):
		threading.Thread.__init__(self)
		print 'intializing dynamo gui object'
		
		self.home           = os.environ.get('HOME')
		self.scratch        = os.environ.get('PDYNAMO_SCRATCH')
		
		self.dualLog        = DualTextLogFileWriter ( )
		#self.dualLog        = None
		
		self.types_allowed  = {'pdb':False, 'xyz':True, 'mol2':False}
		
		
		#pDynamo_project
		self.project        = DynamoProject()
		#self.pymol          = pymol_class()

		self.filename       = None
		self.about_dialog   = None
		
		#extensions
		self.AmberProject   = None
		self.new_lig        = None                      # ligand name used in the antechamber functions
		self.GromacsProject = None
		
		
		#plotclass
		self.plot           = None
		
		
		

		#GUI variables	
		self.sigma_pk1_pk3  = None
		self.sigma_pk3_pk1  = None	
		
		self.sigma_pk1_pk3_coord1  = None
		self.sigma_pk3_pk1_coord1  = None	
		self.sigma_pk1_pk3_coord2  = None
		self.sigma_pk3_pk1_coord2  = None			
		
		#Project variables
		self.project_name   = None    # project name - variable will be used when the routines save and save as are used
		self.script_step    = 1
		
		
				
		builder = gtk.Builder()
		builder.add_from_file("GTKDynamo.glade") 
		builder.connect_signals(self)
	
	

		self.open_window4   = False
		self.HistoryJob     = False
		self.TrajectoryTool = False
		self.QuickScript    = False

		
		#===========================================#
		#    W I D G E T S    C A L L B A C K S     #
		#===========================================#		
		# get the widgets which will be referenced in callbacks
		self.window               = builder.get_object("1window_main")
		self.min_windows          = builder.get_object("2_window_minimization")
		self.dyn_windows          = builder.get_object('3_window_molecular_dynamics')
		self.trj_tool_windows     = builder.get_object('4_window_trajectory_tool')
		self.load_trj_windows     = builder.get_object('5_window_Load_traj_window')
		self.setupORCA_window     = builder.get_object('6_window_ORCA_window')
		self.run_NEB_window       = builder.get_object('7_window_NEB_window')
		
		self.surf_Save_window     = builder.get_object('8_window_save_surface')
		self.new_prjct_window     = builder.get_object('9_window_new_project')
		
		self.normal_modes_window  = builder.get_object('10_window_NormalModes')
		#self.prune_system_window  = builder.get_object('11_window_prune_system')
		self.charge_window        = builder.get_object('12_window_charges')
		self.merge_window         = builder.get_object('13_window_merge')
		self.import_coord_window  = builder.get_object('14_window_import_coordinates')
		self.TLEAP_window         = builder.get_object('15_window_TLEAP_dialog1')
		self.ANTECHAMBER_window   = builder.get_object('16_window_ANTECHAMBER')
		self.SAVE_FRAME_dialog    = builder.get_object('17_window_SAVE_FRAME_dialog1')
		self.modify_window        = builder.get_object('18_window_modify_residues')
		self.SCAN_window          = builder.get_object('19_window_SCAN')
		self.GMX_window           = builder.get_object('20_window_GMX_dialog1')
		self.modify_GMX_window    = builder.get_object('21_window_modifly_GMX')
		self.charge_res_window    = builder.get_object('24_window_charge_rescale')
		self.umbrella_window      = builder.get_object('25_window_umbrella_sampling')
		self.SCAN_2D_window       = builder.get_object('26_window_scan2d_dialog1')
		self.window_27_nbmodel    = builder.get_object('27_window_dialog')
		self.window_29_selections = builder.get_object('29_pdynamo_selection_dialog1')
		self.window_30_SAW        = builder.get_object('30_window_SAW_dialog')
		self.window_31_Trj_refine = builder.get_object('31_window_dialog2')
		self.window_32_warning    = builder.get_object('32_window_warning_Error_message')
		self.window_33_message    = builder.get_object('33_window_messagedialog_warning')
		self.window_34_message    = builder.get_object('34_window_messagedialog_question')
		self.window_35_message    = builder.get_object('35_window_messagedialog_error')
		self.window_36_message    = builder.get_object('36_window_messagedialog_info')
		#self.Dialog               = builder.get_object('messagedialog1')
		self.builder = builder
		
		
		
		# MNDO list - pDynamo semi empirical methods
		
		self.mndo_list = ["am1",
						  "pm3",
						  "pm6",
						  "rm1",
						  "chops",
						  "recal"]
		
		
		# DFT list - pDynamo DFT methods
		
		self.DFT_list = ["DFT - demon, lda, 321g",
						 "DFT - demon, blyp, 321g",
						 "DFT - ahlrichs, lda, 631gs",
						 "DFT - ahlrichs, blyp, 631gs",
						 "DFT - weigend, lda, svp",
						 "DFT - weigend, blyp, svp"]
		# ORCA config
		
		self.HF_list = ["HF - Hartree-Fock",
						"MP2"]
						
		self.KS_list = ["LDA    - Local density approximation"                     ,
						"BLYP   - Becke '88 exchange and Lee-Yang-Parr correlation",
						"mPWPW  - Modified PW exchange and PW correlation"         ,
						"mPWLYP - Modified PW exchange and LYP correlation"        ,
						
						"TPSSh - The hybrid version of TPSS"                       ,

						"B3LYP - The popular B3LYP functional (20% HF exchange"   ,
						"B3PW - The three parameter hybrid version of PW91"       ,
						"PW1PW - One parameter hybrid version of PW91"            ,
						"mPW1PW - One parameter hybrid version of mPWPW"          ,
						"mPW1LYP - One parameter hybrid version of mPWLYP"        ,
						"PBE0 - One parameter hybrid version of PBE"]		
		#================#
		#     SETUP      #
		#================#
				
		
		self.SETUP_HSCALE()
		self.SETUP_HIDE_WIDGETS()
		self.SETUP_SPIN_BUTTONS()
		self.SETUP_TREEVIEW()		
		self.SETUP_COMBOBOXES()

		self.text_view = builder.get_object("23window_quick_script_textview1")
		self.text_view.modify_font(pango.FontDescription("monospace 10"))

		# hide widgets
		self.builder.get_object('7_window_filechooserbutton_REACTANTS').hide()
		self.builder.get_object('7_window_filechooserbutton_PRODUCTS').hide()
		self.builder.get_object("1window_main_import_coord_from_file").hide()
		self.builder.get_object("1window_main_entry_prm_opls").hide()
		self.builder.get_object("1window_main_import_table_from_file1").hide()
		
		#self.builder.get_object("1window_main_alignment_tab1").hide()
		#self.builder.get_object("1window_main_frame1").hide()
		
		#self.builder.get_object("9_window_frame23_preferences1").set_sensitive(False)
		self.window.show()
		
		# open config.dynamo 
		data_path = self.load_config_file()
		self.update_data_path_from_settings_to_GUI(data_path)
		self.AmberProject = AmberProject()
		#self.on_1window_CHECKBUTTON_PDB_XYZ_MOL2_FILE_TYPES()

		#-------------------------------------------------------------------------#				
		#                        checking types allowed                           #
		#                         rescrever esta parte                            #
		#-------------------------------------------------------------------------#		
		if self.builder.get_object("1window_main_xyz_check_box").get_active():
			self.types_allowed['xyz'] = True
		else: 
			self.types_allowed['xyz'] = False
		
		if self.builder.get_object("1window_main_pdb_check_box").get_active():
			self.types_allowed['pdb'] = True
		else:
			self.types_allowed['pdb'] = False
		
		if self.builder.get_object("1window_main_mol2_check_box").get_active():
			self.types_allowed['mol2'] = True
		else:
			self.types_allowed['mol2'] = False	
		#-------------------------------------------------------------------------#		
		
		
		self.sphere_scale          = 0.25   # = 0.25
		self.stick_radius          = 0.15   # = 0.15
		self.label_distance_digits = 4      # = 4
		self.mesh_width            = 0.3    # = 0.5
		
		cmd.set ('sphere_scale'         , self.sphere_scale)
		cmd.set ('stick_radius'         , self.stick_radius)
		cmd.set ('label_distance_digits', self.label_distance_digits)
		cmd.set ('mesh_width'           , self.mesh_width )
		cmd.set ("retain_order") # keep atom ordering
		
		#cmd.set ('sphere_scale'     , 0.25)   cmd.set ('sphere_scale'     , self.sphere_scale) 
		#cmd.set ('stick_radius'     , 0.15)   cmd.set ('stick_radius'     , self.stick_radius)
		#cmd.set ('label_distance_digits',4)   cmd.set ('label_distance_digits', self.label_distance_digits)
		#cmd.set ('mesh_width',         0.5)   cmd.set ('mesh_width',       self.mesh_width )
		
		
		print text1

	
	def run(self):
		#print "starting thread" 
		gtk.main()
		


gtk.gdk.threads_init()
print "Creating object"
gtk_dynamo = GTKDynamo()
gtk_dynamo.start()


'''


			# alert Dialog     -  when only one button will be showed

		#-------------------------------------------------------------------------------------------------------------------------------#
		# 
		#		 Message Dialog  -  when 2 buttons will be showed
		#  1 -create the warning message
		#  2 -hide the actual dialog - optional
		#  3 -show the message dialog
		#  4 -hide the message dialog
		#  5 -check the returned valor by the message dialog
		#  6 -do something
		#  7 -restore the actual dialog - optional	
		#-------------------------------------------------------------------------------------------------------------------------------#
			
			# 1 - creating a error message
			self.builder.get_object('32_window_warning_Error_message_label1').set_text("Error, the trajectory does not match with system in memory.")
			#print "Error, the trajectory does not match with system in memory."
			# creating a error message
			
			# 2 - step
			self.load_trj_windows.hide()
			
			# 3 step
			a = self.window_32_warning.run() #32_window_warning_Error_message
			
			# 4 step
			self.window_32_warning.hide()
			
			#print a
			# 7
			self.load_trj_windows.run()			
			
			
		#-------------------------------------------------------------------------------------------------------------------------------#
		# 
		#		 Message Dialog  -  when 2 buttons will be showed
		#  1 -create the warning message
		#  2 -hide the actual dialog - optional
		#  3 -show the message dialog
		#  4 -hide the message dialog
		#  5 -check the returned valor by the message dialog
		#  6 -do something
		#  7 -restore the actual dialog - optional	
		#-------------------------------------------------------------------------------------------------------------------------------#
		# creating a error message
		qc_table      = self.project.settings['qc_table']
		if qc_table == []:
			# 1 step
			#self.builder.get_object('33_window_message_label1').set_text("You have no atoms in your QC_list, would you like\nto add all the atoms of your system to the QC region.")
			self.builder.get_object('33_window_messagedialog_warning').format_secondary_text("Delete the system in memory?")
			
			# 2 step
			#self.load_trj_windows.hide() # hide the load_trj window
			
			# 3 step
			a = self.window_33_message.run()
			# 4 step
			self.window_33_message.hide()
			
			# 5 step
			#print a
			if a != -5:
				# 6 step
				return 0
			
			# 7 step
			#self.load_trj_windows.run()
		
		#-------------------------------------------------------------------------------------------------------------------------------#
'''

