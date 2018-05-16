"""
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
#		Special thanks to:
#       - Lucas Assirati           < Univesity of Sao Paulo - SP, Brazil                              >
#       - Leonardo R Bachega       < University of Purdue - West Lafayette, IN - USA                  >
#       - Richard Garratt          < Univesity of Sao Paulo - SP, Brazil                              >
#
#
#		
"""  

import sys
import os
import gtk
import pango
import gobject


from random import Random
from math import *



from pBabel           import *
from pCore            import * 
from pMolecule        import * 
from pMoleculeScripts import *
from pymol import *


atomic_dic = { 
			'Ac':227.028,
			'Al':26.9815,
			'Am':243    , 	
			'Sb':121.757,
			'Ar':39.948 , 
			'As':74.9215,
			'At':210    , 	
			'Ba':137.327,
			'Bk':247    , 	
			'Be':9.01218,
			'Bi':208.980,
			'Bh':262    , 	
			'B' :10.811 , 
			'Br':79.904 ,
			'Cd':112.411,
			'Ca':40.078 ,
			'Cf':251    , 	
			'C' :12.011 , 
			'Ce':140.115,
			'Cs':132.905,
			'Cl':35.4527,
			'Cr':51.9961,
			'Co':58.9332,
			'Cu':63.546 ,
			'Cm':247 	,
			'Db':262 	,
			'Dy':162.50 ,
			'Es':252 	,
			'Er':167.26 ,
			'Eu':151.965,
			'Fm':257 	,
			'F'	:18.9984,
			'Fr':223 	,
			'Gd':157.25 ,
			'Ga':69.723 ,
			'Ge':72.61  ,
			'Au':196.966,
			'Hf':178.49 ,
			'Hs':265 	,
			'He':4.00260,
			'Ho':164.930,
			'H' :1.00794,
			'In':114.82 ,
			'I' :126.904,
			'Ir':192.22 ,
			'Fe':55.847 ,
			'Kr':83.80  ,
			'La':138.905,
			'Lr':262 	,	
			'Pb':207.2  ,
			'Li':6.941  ,
			'Lu':174.967,
			'Mg':24.3050,
			'Mn':54.9380,
			'Mt':266 	,
			'Md':258 	,
			'Hg':200.59 ,
			'Mo':95.94  ,
			'Nd':144.24 ,
			'Ne':20.1797,
			'Np':237.048,
			'Ni':58.6934,
			'Nb':92.9063,
			'N' :14.0067,
			'No':259 	,
			'Os':190.2  ,
			'O' :15.9994,
			'Pd':106.42 ,
			'P' :30.9737,
			'Pu':244 	,
			'Po':209 	,
			'K' :39.0983,
			'Pr':140.907,
			'Pm':145 	,
			'Pa':231.035,
			'Ra':226.025,
			'Rn':222 	,
			'Re':186.207,
			'Rh':102.905,
			'Rb':85.4678,
			'Ru':101.07 ,
			'Rf':261 	,
			'Sm':150.36 ,
			'Sc':44.9559,
			'Sg':263 	,
			'Se':78.96  ,
			'Si':28.0855,
			'Ag':107.868,
			'Na':22.9897,
			'Sr':87.62  ,
			'S' :32.066 ,
			'Ta':180.947,
			'Tc':217,
			'Te':127.60, 
			'Tb':158.925,
			'Tl':204.383,
			'Th':232.038,
			'Tm':168.934,
			'Sn':118.710,
			'Ti':47.88  ,
			'W' :183.85 ,
			'U' :238.028,
			'V' :50.9415,
			'Xe':131.29 ,
			'Yb':173.04 ,
			'Y' :88.9058,
			'Zn':65.39  ,
			'Zr':91.224 ,
			
			"H" : 1.0 ,
			"C" : 12.0,
			"O" : 16.0,
			"N" : 14.0,			
			"F" : 19.0,
			"P" : 31.0,		
			"S" : 32.1,
			"Cl": 35.0,
			"CL": 35.0,
			"cl": 35.0,
			"Br": 79.9,
			"BR": 79.9,	
			"I" : 126.0}

SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


def back_orca_output(output_path, step):
	try:
		SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
		#os.rename(SCRATCH + "/job.out", output_path+'/orca_step' + str(step) + ".out" )
		#os.rename(SCRATCH + "/job.gbw", output_path+'/orca_step' + str(step) + ".gbw" )
		#print   "Saving orca output: ", output_path+'/orca_step' + str(step) + ".out"

		os.rename(SCRATCH + "/job.out", output_path+'/step_' + str(step) + "_orca_output.out" )
		os.rename(SCRATCH + "/job.gbw", output_path+'/step_' + str(step) + "_orca_output.gbw" )
		print   "Saving orca output:", output_path+'/step_' + str(step)  + "_orca_output.out"
	except:
		a = None
	
class DualTextLogFileWriter ( TextLogFileWriter ):
	  
    def Text ( self, text ):
        """Text."""
        if self.isActive and ( text is not None ): 
            self.file.write ( text )
            log_out = open("log.gui.txt", "a") # RWM / Bachega
            log_out.write(text)                # redirects output to a log text file
            log_out.close()                    #


def get_file_type (filename):
	file_type = filename.split('.')
	return file_type[-1]

def add_file_type_suffix (filename, type_):
	
	file_type = get_file_type (filename)

	if file_type == type_:
		return filename
	else:
		return filename+'.'+type_




#SCAN functions

""" distance and others"""

def distance_a1_a2(Xa,Ya,Za,Xb,Yb,Zb):
	dist = ((float(Xa) -float(Xb))**2  + (float(Ya) -float(Yb))**2  + (float(Za) -float(Zb))**2)**0.5
	return dist

def import_ATOM1_ATOM2(pka,pkb):
	""" Function doc """
	atom1 = cmd.get_model(pka)
	for a in atom1.atom:
		idx1        = a.index
		atom1_index = int(idx1) -1
		#name1       = a.name
		name1       = a.symbol
		atom1       = idx1	
		X1 = a.coord[0]
		Y1 = a.coord[1]
		Z1 = a.coord[2]	
		#print "Atom1: ", name1,",  index: ",idx1, ", Coordinates: ",X1,Y1,Z1	

	atom2 = cmd.get_model(pkb)
	for a in atom2.atom:
		idx2        = a.index
		atom2_index = int(idx2) -1
		#name2       = a.name
		name2       = a.symbol
		atom2       = idx2
		X2 = a.coord[0]
		Y2 = a.coord[1]
		Z2 = a.coord[2]
		#print "Atom2: ", name2,",  index: ",idx2, ", Coordinates: ",X2,Y2,Z2
	
	distance  = distance_a1_a2(X1,Y1,Z1,X2,Y2,Z2)
	#print "Distance  atom1 ---> atom2  = ", distance 
	return name1 , atom1_index, name2,  atom2_index, distance

def compute_sigma_a1_a3 (pk1_name, pk3_name):

	""" example:
		pk1 ---> pk2 ---> pk3
		 N  ---   H  ---  O	    
		 
		 where H is the moving atom
		 calculation only includes N and O ! 
	"""
	
	mass1 = atomic_dic[pk1_name]
	mass3 = atomic_dic[pk3_name]
	
	sigma_pk1_pk3 =  mass1/(mass1+mass3)
	#print "sigma_pk1_pk3: ",sigma_pk1_pk3
	
	sigma_pk3_pk1 =  mass3/(mass1+mass3)
	sigma_pk3_pk1 = sigma_pk3_pk1 *-1
	
	#print "sigma_pk3_pk1: ", sigma_pk3_pk1
	
	return sigma_pk1_pk3, sigma_pk3_pk1

	#===================================================#
	#             I M P O R T  F I L E S                #
	#===================================================#

def load_table_from_file(file_in):  # to import the old GTKDynamo selections tables 
	
	file_in = open( file_in, 'r')
	table   = []
	
	for line in file_in:
		line2 = line.split(",")
		for i in line2:
			i = int(i)
			table.append(i)
	file_in.close()
	return table

# opem logfile

def parse_log_file(log_file):                              #    L O G    R E A D E R
	matrix_lines  =   []
	log = open( log_file , "r")

	for line in log:
		linex = line.split()
		
		try:                                      # Check if the Log is Molecular Dynamics
			if linex[0] == "Time":
				if linex[1] == "Total":
					Time = []
					Total_energy = []
					Kinetic_Energy = []
					Potential_Energy = []
					Temperature = []
								
					for line in log:
						line2 = line.split()
						lengh = len(line2)
						
						if lengh == 5:
							tipo = line2[0].split(".")
							lengh = len(tipo)
							if lengh == 2:
								
								try:
									Time.append(float(line2[0]))
									Total_energy.append(float(line2[1]))
									Kinetic_Energy.append(float(line2[2]))
									Potential_Energy.append(float(line2[3]))
									Temperature.append(float(line2[4]))
				
								except:
									print " "
			#print_graf2(Time,Total_energy,Kinetic_Energy,Potential_Energy,Temperature)
		except:
			a = None
		
		
		try:                                      # Check if the Log is SAW process
			if linex[1] == "Self-Avoiding":
				if linex[2] == "Walk":
					print "SAW"   
					Structure = []
					Energy = []
					for line in log:
						#print line
						line2 = line.split()
						lengh = len(line2)
						
						if lengh == 4:
							tipo = line2[0].split(".")
							lengh = len(tipo)
							if lengh == 1:
								
								try:
									n = 0
									Structure.append(float(line2[0]))
									Energy.append(float(line2[1]))
								except:
									print " "
						if lengh == 2:
							tipo = line2[0].split(".")
							lengh = len(tipo)
							if lengh == 1:
								
								try:
									n = 0
									Structure.append(float(line2[0]))
									Energy.append(float(line2[1]))
								except:
									print " "						
							

				return Structure,Energy
		except:
			a = None
			
		try:
			if linex[1] == "Conjugate-Gradient":   # Check if the Log is a log of a minimization process
				interact = []
				Function = []
				RMS_Grad = []
				Mac_Grad = []
				RMS_disp = []
				MAS_Disp = []

				for line in log:
					line2 = line.split()
					lengh = len(line2)

					if lengh == 6:
						try:
							n = 0
							interact.append(float(line2[0]))
							Function.append(float(line2[1]))
							RMS_Grad.append(float(line2[2]))
							Mac_Grad.append(float(line2[3]))
							RMS_disp.append(float(line2[4]))
							MAS_Disp.append(float(line2[5]))

						except:
							print " "
				return interact, Function

		except:
			a = None


		try:
			if linex[1] == "Steepest-Descent":   # Check if the Log is a log of a minimization process
				interact = []
				Function = []
				RMS_Grad = []
				Mac_Grad = []
				RMS_disp = []
				MAS_Disp = []

				for line in log:
					line2 = line.split()
					lengh = len(line2)

					if lengh == 6:
						try:
							n = 0
							interact.append(float(line2[0]))
							Function.append(float(line2[1]))
							RMS_Grad.append(float(line2[2]))
							Mac_Grad.append(float(line2[3]))
							RMS_disp.append(float(line2[4]))
							MAS_Disp.append(float(line2[5]))

						except:
							print " "
				return interact, Function

		except:
			a = None










		
		#n = 0 
		try:                                      # Check if the Log is a NEB process
			if linex[0] == "Growing":
				if linex[1] == "String":  
					Structure = []
					Energy = []
					Energy_absolut = []
					EnergyKcal = []
					for line in log:
						print line
						line2 = line.split()
						lengh = len(line2)
						n = 0
						
						if lengh == 5:
							tipo = line2[0].split(".")
							tipo2= line2[1].split(".")
							tipo3= line2[2].split(".")
							
							
							lengh = len(tipo)
							lengh2 = len(tipo2)
							lengh3 = len(tipo3)
							if lengh == 1:
								if 	lengh2 == 2:
									if lengh3 == 2: 
										try:
											n = 0
											Energy_absolut.append(float(line2[1]))											
											
											Structure.append(float(line2[0]))
											Energy.append(float(line2[1]) - Energy_absolut[0])
											
											EnergyKcal.append((float(line2[1]) - Energy_absolut[0])*0.23923445  )

										except:
											print " "	
							n = 1

				return Structure,Energy
				
		except:
			a = None



		try:                                      # Check if the Log is a Self-Diffusion Function process
			if linex[0] == "Self-Diffusion":
				if linex[1] == "Function":  
					Structure = []
					Energy = []
					for line in log:
						#print line
						line2 = line.split()
						lengh = len(line2)
						if lengh == 2:
							tipo = line2[0].split(".")
							lengh = len(tipo)
							if lengh == 1:
								try:
									n = 0
									Structure.append(float(line2[0]))
									Energy.append(float(line2[1]))
								except:
									print " "
				return Structure, Energy
		except:
			a = None
		
		
		
		try:                                      # Check if the Log is a UMBRELLA SAMPLING process
			if linex[0] == "Potential":
				if linex[1] == "of":
					if linex[2] == "Mean": 
						print linex[0],linex[1],  linex[2]
						ReactionCoord = []
						PDF           = []
						PMF           = []
						for line in log:
							line2 = line.split()
							lengh = len(line2)
							if lengh == 3:
								tipo = line2[0].split(".")
								lengh = len(tipo)
								if lengh == 2:
									try:
										n = 0
										ReactionCoord.append(float(line2[0]))
										PDF.append(float(line2[1]))
										PMF.append(float(line2[2]))
									except:
										print " "
					return ReactionCoord, PMF
		except:
			a = None

		
		#------------------------ GTKDynamo SCAN Multiple-Distance ----------------------
		#      [0]                  [1]      [2]        [3]                 [4]
		try:                                      # Check if the Log is a SCAN process of the GTKDYN
			if linex[1] == "GTKDynamo":
				if linex[2] == "SCAN":
					if linex[3] == 'Multiple-Distance':
						print linex[2],linex[3]
						Frame      = []
						PK1_PK2    = []
						PK2_PK3    = []
						Energy     = []
						
						for line in log:
							line2 = line.split()
							lengh = len(line2)
							
							if lengh == 4:
								print line
								try:
									Frame.append(float(line2[0]))
									Energy.append(float(line2[-1]))
								except:
									a = None
					return Frame, Energy
		except:
			a = None



		#------------------------ GTKDynamo SCAN  Simple-Distance -----------------------
		#      [0]                  [1]      [2]        [3]                 [4]
		try:                                      # Check if the Log is a SCAN process of the GTKDYN
			if linex[1] == "GTKDynamo":
				if linex[2] == "SCAN":
					if linex[3] == 'Simple-Distance':
						print linex[2],linex[3]
						Frame      = []
						PK1_PK2    = []
						Energy     = []
						
						for line in log:
							line2 = line.split()
							lengh = len(line2)
							
							if lengh == 3:
								print line
								try:
									Frame.append(float(line2[0]))
									Energy.append(float(line2[-1]))
								except:
									a = None
					return Frame, Energy
		except:
			a = None		
		
		'''
		--------------------------------------------------------------------------------
		--                                                                            --
		--                          GTKDynamo SCAN  2D                                --
		[0]                            [1]    [2]  [3]                              [4]
		--                                                                            --
		--------------------------------------------------------------------------------

		----------------------- Coordinate 1 - Simple-Distance -------------------------
		ATOM1                  =              1  ATOM NAME1             =             Br
		ATOM2                  =              2  ATOM NAME2             =              C
		NWINDOWS               =             20  FOCE CONSTANT          =     4000.00000
		DMINIMUM               =        1.94753  DINCREMENT             =        0.05000
		--------------------------------------------------------------------------------
		----------------------- Coordinate 2 - Simple-Distance -------------------------
		ATOM1                  =              2  ATOM NAME1             =              C
		ATOM2                  =              0  ATOM NAME2             =             Cl
		NWINDOWS               =             25  FOCE CONSTANT          =     4000.00000
		DMINIMUM               =        2.86655  DINCREMENT             =       -0.05000
		--------------------------------------------------------------------------------
		
		MATRIX2         0.00000000          0.28827311          1.02210627          2.36403063  
		MATRIX2         0.09029504          0.36777736          1.07893998          2.37828860  
		MATRIX2         0.78146785          1.00737346          1.64857823          2.86669789  
		
		try:                                      # Check se o Log eh processo SCAN 2D do GTKDYN
			print line
			if line == "--                          GTKDynamo SCAN  2D                                --":
				return "matrix", "2d scan"
		except:
			a = None
		'''
		try:                                      # Check if the Log is a SCAN2D process of the GTKDYN
			i             =   0
			j             =   0
			
			#matrix_lines  =   []
			 
			if linex[0] == "MATRIX2":
				#print linex
				i = len(linex) - 1
				j = j + 1
				
				
				for line in log:
					lineX = line.split()
					mline = []
					if lineX[0] == "MATRIX2":
						for a in lineX:
							if a == "MATRIX2":
								a = None
							else:
								mline.append(float(a))
								
						#print mline
					matrix_lines.append(mline)
				
				#print matrix_lines
				
				
				
				import numpy as np
				X = np.array(matrix_lines)
				#print X
				return "matrix", X
		except:
			a = None
	#print matrix_lines
	#print X

#-------------------#
#   export tables   #
#-------------------#

def write_table_in_text(table, table_name):
	if len(table) != 0:
		string  = table_name + "   = ["
		for i in table:
			string  =  string+str(i)
			if i == table[-1]:
				string  =  string+"]\n"
			else:
				string  =  string+","
	
	else:
		string  = table_name+"   = []\n"
	return string 

def write_table_in_text2(table): 
	if len(table) != 0:
		string  = "["
		for i in table:
			string  =  string+str(i)
			if i == table[-1]:
				string  =  string+"]"
			else:
				string  =  string+","
	return string

def write_table_in_text3(tables, table_name):
	if len(tables) != 0:
		string  = table_name + "   = [\n"
		#print string
		for table in tables:
			string  =  string + "                ["
			for i in table:
				string  =  string+str(i)
				if i == table[-1]:
					string  =  string+"],\n"
				else:
					string  =  string+","
			#print string
			if table == tables[-1]:
				string  =  string + "                ]\n\n"
		print string
	else:
		string  = table_name+"   = []\n"

	return string
	
def gtkdin_PDBFile_ToCoordinates3(filein):		 # gtkdin_PDBFile_ToCoordinates3 function reads a PDB file and rewrites as a XYZ
	#data_path=App.get_object('data_path_finder').get_filename()				
	arq =  open(filein, "r")												#
																			#
	atom_type = []															#
	coord_x = []															#
	coord_y = []															#
	coord_z = []															#
																			#
	text_out = []							#	
											#
	for line in arq:						#	example, line: ATOM  85830  CLA CLA I 154    -106.883-110.916-110.774  1.00  0.00      ION CL
		line2 = line.split()				#   	                             														   line[76:78]
											#												  li[30:38]
		if line2[0] == "CRYST1":			#														  li[38:46]									
			print line2[0:-1]				#																  li[46:54]
											#
		if line2[0] == "ATOM":
			atom = line[76:78]
			atom_type.append(atom)				
			text_out.append(atom)			

			#x
			x = line[30:38]
			coord_x.append(x)
			text_out.append(x + "   ")			#saves the coordinate x
			
			#y
			y = line[38:46]
			coord_y.append(y)
			text_out.append(y + "   ")			#saves the coordinate y
			
			#z 
			z = line[46:54]
			coord_z.append(z)
			text_out.append(z + " \n")			#saves the coordinate z
			#print atom, x, y, z
	arq.close()
	lengh   = str(len(atom_type))						 # number of atoms
	header  = lengh+"\nGTK DYNAMO PDD to XZY \n"		 # writes the header of the XYZ file
	arq_out = open("tmp_out.xyz", "w")		 # creates a XYZ file
	arq_out.writelines(header) 							 # writes the XYZ file header
	arq_out.writelines(text_out)						 # writes the coordinates in the XYZ file
	arq_out.close()
	file_out ="tmp_out.xyz"					# generated file path
	return file_out										# returns the generated file path


	#===================================================#
	#             I M P O R T  F I L E S                #
	#===================================================#
	
def COMPLETE_residues_gromacs(sele_table, gromacs_coords, data_path):   # Complete selected residues - gromacs system
	t0=time.time ()									
	chain_table = [] 								# table with the selected atom chains
	text        = []						 
																	
	arq = open(gromacs_coords , "r")                #	open the initial .gro file

#
#   - sele_table  -  index of atoms selected by pymol
#	
#						How a .gro file works:
#
#                  25468SOL    HW281376   6.847   8.789   8.771  2.5044 -1.8931 -0.4731
#	      			   1MET      N    1   5.067   2.923   4.794 -0.6615 -0.0525  0.2568
#   	           line[0:5]	-index       		        
#						line[5:8]	-resn			 
#						   line[8:15]	-A_name
#								 line[15:20]	-resi
#																  
# 	

	resi_list   = []		# residue number
	resn_list   = []		# residue name
	index_list  = []		# index - tmp
	
	index_table = []		# index of the atoms that will be selected 	
	n = 1
	for line in arq:
		if n > 3:
			#funcao
			try:
				index   = line[15:20]			#	index            ex   "   11"
				resn    = line[5:8]				#	residue name     ex     "LYS"
				A_name  = line[8:15]			#	atom name        ex "    HG1"
				resi    = line[0:5]				#	residue number   ex   "  160"
												#
				
				
				index2 = index.split() 			# 	eliminates the spaces in the index variable "   11"  --> "11"
				#print index2[0]
				index2 = int(index2[0])			

				resi2 = resi.split()			
				resi2 = int(resi2[0])			
					
				A_name2 = A_name.split()		
				A_name2 = A_name2[0]			
				
				resn2 = resn.split()			
				resn2 = resn2[0]	
				
				if  resi_list  == []:
					resi_list.append(resi2)
					resn_list.append(resn2)
					index_list.append(index2)
					#print index_list
					
				elif resi2 == resi_list[-1]:
					resi_list.append(resi2)
					resn_list.append(resn2)
					index_list.append(index2)
					#print index_list
				
				elif resi2 != resi_list[-1]:
					#print index_list
					for a in sele_table:
						for b in index_list: 
							if int(a) == int(b):
								for c in index_list:
									index_table.append(c)	
															
															
															
															
					resi_list  = []				
					resn_list  = []				 
					index_list = []				
					index_list2 = []			

					resi_list.append(resi2)		
					resn_list.append(resn2)		
					index_list.append(index2)	
			except:
				a = None
		
		n = n+1

	t0=time.time () -t0
	print "Total time = ", t0
	print index_table					#	print a table index_table with the atoms that should be selected by the pymol
	
	return index_table

def COMPLETE_residue(sele_table, pdb_file, data_path):	                # Complete the selected residues
	t0=time.time ()									
	
	arq         = open(pdb_file, "r")             					#
	
	chain_table = [] 								
	text        = []	
	resi_list   = []
	resn_list   = []
	index_list  = []	
	
	resn_table  = [] 
	index_table = []
	resi_table  = [0]						
											#				   HETATM63481  H2  WAT  1969       9.601  14.007  17.182  0.00  0.00           H   -->Amber
											#                  HETATM 1884  O   HOH A 372      21.952   9.654  -3.812  1.00 50.58           O
											#				         line[6:11] 					 -  index
											#						      line[11:16]  				 -  A_name
											#								  line[16:20]  			 -  resn
											#									   line[20:22] 		 -  chain
											#										 line[22:26] 	 -  resi
											
	for line in arq:						#	      		   ATOM  85830  CLA CLA I 154    -106.883-110.916-110.774  1.00  0.00      ION CL	-->Charmm
		line2 = line.split()				#   	                             		'    '									'          line[76:78]
		line1 = line[0:6]					#												  li[30:38]
		#if line2[0] == "CRYST1":			#														  li[38:46]									
		#	print line2[0:-1]				#																  li[46:54]
		#	print line
		if line1 == "ATOM  ":				
		
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

			index2 = index.split() 
			index2 = int(index2[0])

			resi2 = resi.split()
			resi2 = int(resi2[0])			
				
			A_name2 = A_name.split()		
			A_name2 = A_name2[0]			
			
			resn2 = resn.split()
			resn2 = resn2[0]
			#print index2, A_name2, resi2, resn2

			print index2,resi2, A_name2, resn2
	
			if  resi_list  == []:
				resi_list.append(resi2)
				resn_list.append(resn2)
				index_list.append(index2)
				#print index_list
				
			elif resi2 == resi_list[-1]:
				resi_list.append(resi2)
				resn_list.append(resn2)
				index_list.append(index2)
				#print index_list
			elif resn2 != resn_list[-1]:
				#print index_list
				for a in index_list:
					if a in sele_table:
						for b in index_list:
							index_table.append(b)
			#	if resi_list in element_list
			#	for a in sele_table:
			#		for b in index_list:
			#			if a == b:
			#				for c in index_list:
			#					index_table.append(c)
								
				resi_list  = []
				
				resn_list  = []
				index_list = []	
				resi_list.append(resi2)
				resn_list.append(resn2)
				index_list.append(index2)

		if line1 == "HETATM":				
			
			
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

			index2 = index.split() 
			index2 = int(index2[0])

			resi2 = resi.split()
			resi2 = int(resi2[0])			
				
			A_name2 = A_name.split()		
			A_name2 = A_name2[0]			
			
			resn2 = resn.split()
			resn2 = resn2[0]
			#print index2, A_name2, resi2, resn2

			
	
			if  resi_list  == []:
				resi_list.append(resi2)
				resn_list.append(resn2)
				index_list.append(index2)
				#print index_list
				
			elif resi2 == resi_list[-1]:
				resi_list.append(resi2)
				resn_list.append(resn2)
				index_list.append(index2)
				#print index_list
			elif resi2 != resi_list[-1]:
				#print index_list
				for a in index_list:
					if a in sele_table:
						for b in index_list:
							index_table.append(b)

#				for a in sele_table:
#					for b in index_list:
#						if a == b:
#							for c in index_list:
#								index_table.append(c)
								
				resi_list  = []
				
				resn_list  = []
				index_list = []	
				resi_list.append(resi2)
				resn_list.append(resn2)
				index_list.append(index2)
	
	t0=time.time () -t0
	#os.remove(dataPath+"/gtk_dyn_tmp.pdb")
	
	print index_table
	print "\n\n"
	print "Done!"									
	print "Total time = ", t0					
	return index_table

def COMPLETE_residue_from_PDB(arq, table):
	text   = []					     		                            # variable that rewrites the PDB file.	
	arq =  open(arq, "r")
	res_before = None
	res_after  = None
	
	resi_selection = []
	
	index_list = []
	atoms_list = []
	resi_list  = []
	resn_list  = []
											#
											#
											#                  HETATM 1884  O   HOH A 372      21.952   9.654  -3.812  1.00 50.58           O
	for line in arq:						#	exemplo, line: ATOM  85830  CLA CLA I 154    -106.883-110.916-110.774  1.00  0.00      ION CL
		line2 = line.split()				#   	                             		'    '									'          line[76:78]
		line1 = line[0:6]					#												  li[30:38]
		#if line2[0] == "CRYST1":			#														  li[38:46]									
		#	print line2[0:-1]				#																  li[46:54]
		#	print line		
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
			#self.index_list.append(index2)
			
			
			
			A_name2 = A_name.split()		#	quebra a variavel A_name
			A_name2 = A_name2[0]			#	tranforma em uma string				
			#self.atoms_list.append(A_name2)
			
			resi2 = resi.split()
			resi2 = int(resi2[0])			
			#self.resi_list.append(resi2)
			
			resn2 = resn.split()
			resn2 = resn2[0]
			#self.resn_list.append(resn2)				
			
			
			if res_before == None:
				res_before = resi2
				#print  resi2
			if resi2 == res_before:
				index_list.append(index2)
				#print  resi2
				
			if resi2 != res_before:
				#print  resi2
				for i in table:
					if i in index_list:
						for  atoms in index_list:
							resi_selection.append(atoms)
				index_list = []
				index_list.append(index2)
							#print  resi2
							
				res_before = resi2
				

			#print index2, resi2, resn2
	
	
	
	
	for i in table:								
		if i in index_list:
			for  atoms in index_list:
				resi_selection.append(atoms)
				index_list = []
	
	#print resi_selection
	return resi_selection



class DynamoProject:
	def __init__(self):
		self.settings = {'project_name'	  : 'my_project',
							'force_field' : None        ,
							'parameters'  : None        ,
							'topology'    : None         ,
							'coordinates' : None   ,
							'nbModel_type': 'NBModelABFS' ,
							'nbModel' 	  : NBModelABFS( ),
							'ABFS_options': { "innerCutoff" : 8.0 , "outerCutoff" : 12.0 , "listCutoff"  : 13.5 },
							'prune_table' : [] ,
							'fix_table'   : [] ,
							'qc_table'    : [] ,
							
							'QCMM'		  : "No"   ,
							'potencial'   : None   ,
							'qc_method'   : None   ,
							'charge'      : None   ,
							'multiplicity': None   ,
							'density_tol' : None   ,                    
							'Maximum_SCF' : None   , 
							'ORCA_method' : None   ,
							'ORCA_SCF'    : None   ,
							'ORCA_basis'  : None   ,
							'ORCA_pal'    : None   ,					
							'kappa'	      : None   ,
							'data_path'   : None   ,
							'last_step'   : None   ,
							'last_frame'   : None  ,
							'last_pymol_id': None  , 
							'pymol_session':None   }
			

		self.system = None
		self.dynamo_system = None
		self.pymol = None
		self.step = 0
		self.trajectory = None
		self.log_writer = None
		self.pdbInfo    = {}
		
		
	def set_AMBER_MM(self, amber_params, amber_coords, dualLog):
		self.system              = AmberTopologyFile_ToSystem  ( amber_params, dualLog )		
		self.system.coordinates3 = AmberCrdFile_ToCoordinates3 ( amber_coords,  dualLog )
		self.settings['force_field']   = "AMBER"
		self.settings['parameters']    = amber_params
		self.settings['coordinates']   = amber_coords
		self.settings['potencial']     = "MM"

	def set_CHARMM_MM(self, charmm_params, charmm_topologies, dualLog):
		
		parameters      = CHARMMParameterFiles_ToParameters ([(charmm_params)],  dualLog )
		self.system     = CHARMMPSFFile_ToSystem ( os.path.join (charmm_topologies), isXPLOR = True, log = dualLog, parameters = parameters)		
		self.settings['force_field']   = "CHARMM"
		self.settings['parameters']    = charmm_params
		self.settings['topology']      = charmm_topologies
		self.settings['potencial']     = "MM"	
		
	def set_GROMACS_MM(self, gromacs_params, gromacs_coords, dualLog):
		parameters               = GromacsParameters_ToParameters (gromacs_params,  log =  dualLog)
		self.system              = GromacsDefinitions_ToSystem    (gromacs_params,  log =  dualLog, parameters = parameters)
#		self.system.coordinates3 = GromacsCrdFile_ToCoordinates3  (gromacs_coords,  log =  dualLog)
		self.system.coordinates3 = GromacsCrdFile_Process         (gromacs_coords,  system = self.system,  log =  dualLog)

		self.settings['force_field'] = "GROMACS"
		self.settings['potencial']   = "MM"	
		self.settings['parameters']    = gromacs_params
		self.settings['coordinates']   = gromacs_coords
				
	def set_OPLS_MM(self, opls_params, opls_coords,  dualLog):

		path_levels = opls_params.split("/") 
		path = "/"      

		for level in path_levels:                                    
			if level != path_levels[-1]:   # "if the parameters directory is included, does not consider"
				path =  path + '/' + level  

		print "Your path is ", path
		print "your parameters are: ", path_levels[-1]

		mmModel = MMModelOPLS ( path_levels[-1], path = path)

		file_type = opls_coords.split(".")
		file_type = file_type[-1]

		if file_type == "mol":
			self.system = MOLFile_ToSystem (os.path.join (opls_coords), log = dualLog )
		
		elif file_type == "pdb":
			self.system = PDBFile_ToSystem (opls_coords, log = dualLog, modelNumber = 1, useComponentLibrary = True)
		
		elif file_type == "mol2":
			self.system = MOL2File_ToSystem (os.path.join (opls_coords), log = dualLog )		
		
		
		
		self.system.DefineMMModel ( mmModel )

		self.settings['force_field'] = "OPLS"
		self.settings['potencial']   = "MM"	
		self.settings['parameters']    = opls_params 
		self.settings['coordinates']   = opls_coords
		return self.system			
		
	def set_nbModel_to_system(self):	
		ABFS_options = self.settings['ABFS_options']
		nbModel      = self.settings['nbModel_type']

		if nbModel == 'NBModelFull':	
			nbModel = NBModelFull( )
			self.system.DefineNBModel ( nbModel )
		
		elif nbModel == 'NBModelABFS':	
			nbModel = NBModelABFS( )
			self.system.DefineNBModel ( NBModelABFS ( **ABFS_options ) )
		
		elif nbModel ==  'NBModelGABFS':
			nbModel = NBModelGABFS( )
			self.system.DefineNBModel ( NBModelGABFS ( **ABFS_options ) )	
		
		self.settings['nbModel'] = nbModel

	def put_prune_table(self, prune_table):
		self.system = PruneByAtom (self.system, Selection(prune_table))
		self.settings['prune_table'].append(prune_table) 
				
	def put_fix_table(self, fix_table):
		self.system.DefineFixedAtoms(Selection(fix_table))
		self.settings['fix_table'] = fix_table
		
	def put_qc_table(self, qc_table):
		self.settings['qc_table'] = qc_table
		self.settings['QCMM'] = 'yes'

	def increment_step(self):
		self.step = self.step + 1
		self.settings['last_step'] = self.step
		
	def complete_by_component (self, pymol_selection):
		""" Function doc """
		
		selection       = AtomSelection ( system = self.system, selection = pymol_selection )
		newSelection = Selection ( selection.ByComponent ( ) )
		new_list = list(newSelection)
		return new_list
				
	def export_frames_to_pymol(self, prefix, types_allowed , data_path):
		tmp_path = data_path + '/tmp'
		if not os.path.exists( tmp_path ): 
			os.mkdir(tmp_path)
		
		#creating a xyz file - coordienate reference 

		
		
		if types_allowed['xyz'] == True:
			type_ = 'xyz'
			pymol_id = prefix+'_'+type_+'_step'+str(self.step)
			tmp_file = os.path.join(tmp_path, add_file_type_suffix(pymol_id, type_))
			self.export_state_to_file(tmp_file, type_)
			try:
				cmd.delete(pymol_id)
			except:
				a = None
			cmd.load(tmp_file)
			if self.settings['qc_table'] != []:
				pymol_put_table  (self.settings['qc_table'], "QC_atoms")
				string2  = 'select QC_atoms, ('+pymol_id+ ' and  QC_atoms )'
				cmd.do(string2)
				cmd.show( "stick", "QC_atoms" )
				cmd.show( "sphere", "QC_atoms" )
								
			if self.settings['fix_table'] != []:
				pymol_put_table  (self.settings['fix_table'], "FIX_atoms")
				string22  = 'select FIX_atoms, ('+pymol_id+ ' and  FIX_atoms )'
				cmd.do(string22)
				string5  = 'color grey80, FIX_atoms'
				cmd.do(string5)							
		
		
		if types_allowed['pdb'] == True:
			type_ = 'pdb'
			pymol_id = prefix+'_'+type_+'_step'+str(self.step)
			tmp_file = os.path.join(tmp_path, add_file_type_suffix(pymol_id, type_))
			self.export_state_to_file(tmp_file, type_)
			try:
				cmd.delete(pymol_id)
			except:
				a = None
			cmd.load(tmp_file)
			if self.settings['qc_table'] != []:
				pymol_put_table  (self.settings['qc_table'], "QC_atoms")
				string2  = 'select QC_atoms, ('+pymol_id+ ' and  QC_atoms )'
				cmd.do(string2)
				cmd.show( "stick", "QC_atoms" )
				cmd.show( "sphere", "QC_atoms" )
								
			if self.settings['fix_table'] != []:
				pymol_put_table  (self.settings['fix_table'], "FIX_atoms")
				string22  = 'select FIX_atoms, ('+pymol_id+ ' and  FIX_atoms )'
				cmd.do(string22)
				string5  = 'color grey80, FIX_atoms'
				cmd.do(string5)			
			
			
			tmp_file = os.path.join (tmp_path,"tmp.xyz")
			self.export_state_to_file(tmp_file, "xyz")
			
			
			#starts here
			filein = open(tmp_file, 'r')
			n = 0
			new_coord = []
			for line in filein:
				line2 = line.split()
				if n > 1:
					x = float(line2[1])	
					y = float(line2[2])
					z = float(line2[3])
					new_coord.append([ x, y, z])
				n = n + 1

			#print "\n xyz  coordienates"
			#for i in new_coord :
			#	print i 
					
			model3 = cmd.get_model(pymol_id)
			#print "\n pdb  coordienates"

			n = 0
			for a in model3.atom:
				#print a.coord[0], a.coord[1], a.coord[2] 
				a.coord[0] =  new_coord[n][0]
				a.coord[1] =  new_coord[n][1]
				a.coord[2] =  new_coord[n][2]
				n = n + 1

			#print "\n new xyz  coordienates"
			#for a in model3.atom:
			#	print a.coord[0], a.coord[1], a.coord[2] 

			#print new_coord

			cmd.load_model(model3, "_tmp")
			cmd.update(pymol_id, "_tmp")
			cmd.delete("_tmp")			
		
		self.settings['last_pymol_id'] = pymol_id
		cmd.disable("all")
		cmd.enable(pymol_id)
		
		
		"""
		for type_ in types_allowed.keys():
			if types_allowed[type_] == True:
				
				pymol_id = prefix+'_'+type_+'_step'+str(self.step)
				
				tmp_file = os.path.join(tmp_path, add_file_type_suffix(pymol_id, type_))
				
				self.export_state_to_file(tmp_file, type_)

				try:
					cmd.delete(pymol_id)
				except:
					a = None

				cmd.load(tmp_file)
				
				if self.settings['qc_table'] != []:
					#cmd.do("set sphere_scale, 0.25")
					#cmd.do("set stick_radius, 0.15")
					
					#cmd.set ('sphere_scale'     , 0.25)
					#cmd.set ('stick_radius'     , 0.15)
					#cmd.set ('label_distance_digits',4)
					#cmd.set ('mesh_width',         0.5)						
					
					pymol_put_table  (self.settings['qc_table'], "QC_atoms")
					
					#string   = 'zoom ('+pymol_id+ ' and  QC_atoms )'
					#cmd.do(string)
					
					#cmd.select('QC_atoms', selection)
					
					
					string2  = 'select QC_atoms, ('+pymol_id+ ' and  QC_atoms )'
					cmd.do(string2)
					
					#string3  = 'show sticks, QC_atoms'
					#string4  = 'show spheres, QC_atoms'
					#cmd.do(string3)
					#cmd.do(string4)
					
					cmd.show( "stick", "QC_atoms" )
					cmd.show( "sphere", "QC_atoms" )
									
				if self.settings['fix_table'] != []:
					pymol_put_table  (self.settings['fix_table'], "FIX_atoms")
					string22  = 'select FIX_atoms, ('+pymol_id+ ' and  FIX_atoms )'
					cmd.do(string22)

					string5  = 'color grey80, FIX_atoms'
					cmd.do(string5)
				
				self.settings['last_pymol_id'] = pymol_id
				cmd.disable("all")
				cmd.enable(pymol_id)
				
				'''
				if self.settings['qc_table'] != []:
					cmd.do("set sphere_scale, 0.25")
					cmd.do("set stick_radius, 0.15")
					pymol_put_table  (self.settings['qc_table'], "QC_atoms")
					#string   = 'zoom ('+pymol_id+ ' and  QC_atoms )'
					#cmd.do(string)
					string2  = 'select QC_atoms, ('+pymol_id+ ' and  QC_atoms )'
					cmd.do(string2)
					string3  = 'show sticks, QC_atoms'
					string4  = 'show spheres, QC_atoms'
					cmd.do(string3)
					cmd.do(string4)
				'''
		"""
				
	def export_state_to_file (self, filename, type_):

		filename = add_file_type_suffix (filename, type_)

		if type_   == "xyz":
			XYZFile_FromSystem ( filename, self.system )
		
		elif type_ == "pdb":
			PDBFile_FromSystem ( filename, self.system )

		
		elif type_ == "mol2":
			MOL2File_FromSystem ( filename, self.system )
		
		elif type_ == "pkl":
			try:
				XMLPickle ( filename, self.system )
			
			except:
				Pickle ( filename, self.system )

		elif type_ == "yaml":
			YAMLPickle ( filename, self.system )
		
		
		elif type_ == "mol":
			MOLFile_FromSystem ( filename, self.system )

		elif filetype == "cif":
			mmCIFFile_FromSystem ( filename, self.system )

		elif type_ == "psf":
			CHARMMPSFFile_FromSystem( filename, self.system )

		elif  type_ == "crd":
			AmberCrdFile_FromSystem( filename, self.system )

		else:
			print "file type not supported"

	def load_force_field(self, force_field, dualLog ):

		self.system = force_field.load(self.system, dualLog)
		
		self.settings['force_field'] = force_field.get_field_type()

		self.system.DefineNBModel (self.settings['nbModel'] )
		self.system.Summary ( dualLog )

	def load_coordinate_file_to_system(self, filename, dualLog):
		type_ = get_file_type (filename)
		print type_
		
		if type_ == "xyz":
			self.system.coordinates3 = XYZFile_ToCoordinates3 ( os.path.join (filename),  dualLog )

		elif type_ == "pdb":                                                                                                            # When the coordinate file is a PDB
			filename = gtkdin_PDBFile_ToCoordinates3(filename)                                                                  # Uses the gtkdin_PDBFile_ToCoordinates3 functions - converts a PDB to XYZ
			self.system.coordinates3 = XYZFile_ToCoordinates3 ( os.path.join (filename),  dualLog )                                                  # imports the xyz file
			os.remove("tmp_out.xyz")                                            
		
		elif type_ == "xpk":
			try:
				self.system.coordinates3 = Unpickle (filename)
			except:
				self.system.coordinates3 = XMLUnpickle (filename)		
		
		elif type_ == "pkl":
			try:
				self.system.coordinates3 = Unpickle (filename)
			except:
				self.system.coordinates3 = XMLUnpickle (filename)

		elif type_ == "yaml":
			self.system.coordinates3 = YAMLUnpickle (filename)


		elif type_ == "chm":  
			self.system.coordinates3 = CHARMMCRDFile_ToCoordinates3 ( os.path.join ( filename ),  dualLog ) 

		elif type_ == "crd":
			self.system.coordinates3 = AmberCrdFile_ToCoordinates3 ( os.path.join (filename),  dualLog )

		elif type_ == "mol":
			self.system.coordinates3 = MOLFile_ToCoordinates3( os.path.join ( filename),  log = dualLog )
		else:
			return "ops!"

		#self.system.Summary(  dualLog )

		return type_
		
	def load_coordinate_file_as_new_system(self, filename, dualLog):
		type_ = get_file_type (filename)
		print type_
		print filename
		#gtk_dynamo.project.system =  XYZFile_ToSystem( /home/fernando/tmp/tmp.xyz, dualLog)

		if type_ == "xyz":
			self.system      = XYZFile_ToSystem(  filename ,  dualLog )

		elif type_ == "pdb":                                                                                                            # Quando o arquivo de coordenadas eh um PDB
			self.system      = PDBFile_ToSystem(  filename ,  log =  dualLog )                                                  # importa o arquivo xyz gerado pela funcao anterior

		elif type_ == "cif":  
			self.system      = mmCIFFile_ToSystem ( filename  ,  dualLog ) 

		elif type_ == "mop":
			self.system      = MopacInputFile_ToSystem( filename  ,  dualLog )

		elif type_ == "mol":
			self.system      = MOLFile_ToSystem( filename , log =   dualLog )
		
		
		# --- pkl ---
		
		elif type_ == "pkl":
			self.system      = Unpickle( filename )		
			try:
				self.settings['fix_table'] = self.system.hardConstraints.fixedAtoms
				#print 'fix_table = :',self.settings['fix_table']
			except:
				a = None			
			
			try:
				qc_table                   = list( self.system.energyModel.qcAtoms.QCAtomSelection ( ) )	
				boundaryAtoms              = list( self.system.energyModel.qcAtoms.BoundaryAtomSelection ( ))
				
				self.settings['boundaryAtoms'] = boundaryAtoms
				#print 'qc_table : '  , qc_table
				print 'boundaryAtoms', (boundaryAtoms)
				
				qc = []
				for l in qc_table:
					if l in boundaryAtoms:
						print l
					else:
						qc.append(l)				
				
				self.settings['qc_table'] = qc
				
				print 'qc_table : ',self.settings['qc_table']
			except:
				print "System has no QC atoms"		
		
		
		# --- yaml ---
		
		elif type_ == "yaml":
			self.system      = YAMLUnpickle( filename )		
			
			try:
				self.settings['fix_table'] = list(self.system.hardConstraints.fixedAtoms)
				print 'fix_table = :',self.settings['fix_table']
			except:
				a = None
			
			try:
				qc_table                   = list( self.system.energyModel.qcAtoms.QCAtomSelection ( ) )	
				boundaryAtoms              = list( self.system.energyModel.qcAtoms.BoundaryAtomSelection ( ))
				
				self.settings['boundaryAtoms'] = boundaryAtoms
				#print 'qc_table : '  , qc_table
				print 'boundaryAtoms', (boundaryAtoms)
				
				qc = []
				for l in qc_table:
					if l in boundaryAtoms:
						print l
					else:
						qc.append(l)				
				
				self.settings['qc_table'] = qc
				
				print 'qc_table : ',self.settings['qc_table']
			except:
				print "System has no QC atoms"	


 
		else:
			return "ops!"
		try:
			self.system.Summary(  dualLog )
		except:
			print "system empty"
		
		return type_	
					
	def set_qc_parameters_MNDO(self, qc_method, charge, multiplicity, qc_table, dualLog):
		nbModel = self.settings['nbModel']
		qcModel = QCModelMNDO (qc_method )
		self.system.electronicState = ElectronicState  ( charge = charge, multiplicity = multiplicity )
		
		if len(qc_table) != 0:
			Qgroup = Selection (qc_table)
			self.system.DefineQCModel ( qcModel, dualLog, qcSelection = Qgroup)
			self.system.DefineNBModel ( nbModel )
			self.system.Summary ( dualLog )
			self.settings['potencial'] = "QCMM"
			self.settings['QCMM']      = 'yes'	
		else:
			self.system.DefineQCModel ( qcModel )
			self.system.Summary ( dualLog )

			self.settings['potencial'] = "QC"
			self.settings['QCMM']      = 'no'

		self.system.Summary( dualLog )
	
	def set_qc_parameters_DFT(self, qc_method, charge, multiplicity, qc_table, converger, densityBasis, functional, orbitalBasis , dualLog):
		nbModel = self.settings['nbModel']
		qcModel = QCModelDFT (converger = converger, densityBasis = densityBasis,    functional = functional,  orbitalBasis = orbitalBasis  )
		
		self.system.electronicState = ElectronicState  ( charge = charge, multiplicity = multiplicity )
		if len(qc_table) != 0:
			Qgroup = Selection (qc_table)
			self.system.DefineQCModel ( qcModel,  dualLog, qcSelection = Qgroup)
			#self.system.DefineNBModel ( nbModel )
			self.settings['potencial'] = "QCMM"
			self.settings['QCMM']      = 'yes'		
		else:
			self.system.DefineQCModel ( qcModel )
			self.settings['potencial'] = "QC"
			self.settings['QCMM']      = 'no'
						
		self.system.Summary ( dualLog )

#	def set_qc_parameters_ORCA(self, qc_method, charge, multiplicity, qc_table, ORCA_method, ORCA_SCF, ORCA_basis, ORCA_pal, dualLog ):
	def set_qc_parameters_ORCA(self, qc_method, charge, multiplicity, qc_table, orca_string, ORCA_pal, dualLog ):

		nbModel = NBModelABFS( )
		PAL         = "PAL"+str(ORCA_pal)
		
		print "number of processor = ", PAL
		
		if ORCA_pal == 1:
			#qcModel = QCModelORCA (ORCA_method+":"+ORCA_basis, ORCA_SCF)
			qcModel = QCModelORCA (orca_string)
		else:
			qcModel = QCModelORCA (orca_string, PAL )
			

		if len(qc_table) != 0:
			Qgroup = Selection (qc_table)
			self.system.DefineQCModel ( qcModel,  dualLog, qcSelection = Qgroup)
			nbModel = NBModelORCA ( )
			self.system.DefineNBModel ( nbModel )
			self.system.Summary ( dualLog )
			
			self.settings['potencial'] = "QCMM"
			self.settings['QCMM']  	 = "yes"
		else:
			self.system.DefineQCModel ( qcModel )
			self.system.Summary (dualLog )

			self.settings['potencial'] = "QC"
			self.settings['QCMM']      = 'no'	
		self.system.electronicState           = ElectronicState  ( charge = charge, multiplicity = multiplicity )
		
	def check_system(self, dualLog):  # CHECK SYSTEM
		self.system.Summary(log = dualLog)
		print "GTKDynamo is now connected to object: ", self.settings['last_pymol_id']

	def check_energy(self, data_path, dualLog):  # CHECK ENERGY
		t_initial = time.time()
		energy = self.system.Energy(log = dualLog)
		dipolo = self.system.DipoleMoment ()
		t_final = time.time()
		total_time  = t_final - t_initial
		print "Total time = : ", t_final - t_initial
		
		output_path = data_path+"/tmp"                           
		if not os.path.exists (output_path): os.mkdir (output_path)         
		step        = self.step + 1
		print "Total energy = : ", energy
		print "\n"
		back_orca_output(output_path, step)
		
		return energy, total_time
		

	#-------------------------------------#
	#   minimization_Conjugate Gradient   #
	#-------------------------------------#

	def run_minimization(self,
						data_path,
						trajectory_name,
						max_int,
						log_freq,
						trajectory_freq,
						rms_grad,
						method,                  # method type, such as conjugate grad
						output_traj_flag,
						amber_traj_flag,
						dualLog):

		self.system.Summary(dualLog)

		try:
			os.rename('log.gui.txt','log.gui.old')
		except:
			a = None
		
		t_initial = time.time()

		self.system.Summary(dualLog)

		if output_traj_flag:  # if is true:
			traj_file_path = os.path.join ( data_path, trajectory_name)
			
			if amber_traj_flag:
				trajectory = AmberTrajectoryFileWriter(traj_file_path, self.system )
			else:
				trajectory = SystemGeometryTrajectory(traj_file_path, self.system, mode = "w" )

			
			ConjugateGradientMinimize_SystemGeometry (self.system,
														log                  = dualLog,
														logFrequency         = log_freq,
														trajectories         = [(trajectory, trajectory_freq)],
														maximumIterations    = max_int,
														rmsGradientTolerance = rms_grad)

			t_final = time.time()

			log_filename = data_path+'/'+trajectory_name+'/'+'process.log'
			output_path  = data_path+'/'+trajectory_name
			step         = self.step + 1 
			try:
				os.rename('log.gui.txt', log_filename)
			except:
				a = None
			
			#backup orca
			back_orca_output(output_path, step)
			"""
			try:
				SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
				tmp_path = data_path+'/'+trajectory_name
				os.rename(SCRATCH + "/job.out", tmp_path+'/orca_step' + str(self.step+1) + ".out" )
				print "Saving orca output: ",  tmp_path+'/orca_step' + str(self.step+1) + ".out"
			except:
				a = None
			"""


			x,y = parse_log_file (log_filename)
		else:
			ConjugateGradientMinimize_SystemGeometry (self.system,
							log                  = dualLog,
							logFrequency         = log_freq,
							maximumIterations    = max_int,
							rmsGradientTolerance = rms_grad)


				
			t_final = time.time()
				
			log_filename = data_path+'/'+'process.log'
			output_path  = data_path+'/tmp'
			step         = self.step +1 
			
			#backup loga file
			try:
				os.rename('log.gui.txt', log_filename)
			except:
				a = None
			
			#backup orca
			back_orca_output(output_path, step)
			
			"""
			try:
				SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
				#data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
				tmp_path = data_path + '/tmp'
				if not os.path.exists( tmp_path ): 
					os.mkdir(tmp_path)
					
				os.rename(SCRATCH + "/job.out", tmp_path+'/orca_step' + str(self.step +1) + ".out" )
				print "Saving orca output: ",  tmp_path+'/orca_step'  + str(self.step +1) + ".out"
			except:
				a = None		
			"""					
					
					
			x,y = parse_log_file (log_filename)
	
		return x,y,(t_final - t_initial)

	
	
	#-----------------------------------#
	#   minimization_Steepest_Descent   #
	#-----------------------------------#
	
	
	
	def run_minimization_Steepest_Descent (self,
											data_path       ,
											trajectory_name ,

											functionStep    ,
											pathStep        ,   
											max_int         ,   # maximun number of interactions 

											log_freq        ,   # print log frequence
											trajectory_freq ,   # Trajectory frequence
											rms_grad        ,
											method          ,
											output_traj_flag,   # save trajectory yes - no ?
											amber_traj_flag ,   # amber output traj
											dualLog):
	
		
		self.system.Summary(dualLog)

		try:
			os.rename('log.gui.txt','log.gui.old')
		except:
			a = None
		
		t_initial = time.time()

		self.system.Summary(dualLog)

		if output_traj_flag:  # if is true:
			traj_file_path = os.path.join ( data_path, trajectory_name)
			
			if amber_traj_flag:
				trajectory = AmberTrajectoryFileWriter(traj_file_path, self.system )
			else:
				trajectory = SystemGeometryTrajectory(traj_file_path, self.system, mode = "w" )

			
			SteepestDescentMinimize_SystemGeometry (self.system,
														log                  = dualLog,
														logFrequency         = log_freq,
														trajectories         = [(trajectory, trajectory_freq)],
														maximumIterations    = max_int,
														rmsGradientTolerance = rms_grad)

			t_final = time.time()

			log_filename = data_path+'/'+trajectory_name+'/'+'process.log'
			output_path  = data_path+'/'+trajectory_name
			step         = self.step + 1 
			try:
				os.rename('log.gui.txt', log_filename)
			except:
				a = None
			
			#backup orca
			back_orca_output(output_path, step)
			"""
			try:
				SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
				tmp_path = data_path+'/'+trajectory_name
				os.rename(SCRATCH + "/job.out", tmp_path+'/orca_step' + str(self.step+1) + ".out" )
				print "Saving orca output: ",  tmp_path+'/orca_step' + str(self.step+1) + ".out"
			except:
				a = None
			"""


			x,y = parse_log_file (log_filename)
		else:
			SteepestDescentMinimize_SystemGeometry (self.system,
							log                  = dualLog,
							logFrequency         = log_freq,
							maximumIterations    = max_int,
							rmsGradientTolerance = rms_grad)


				
			t_final = time.time()
				
			log_filename = data_path+'/'+'process.log'
			output_path  = data_path+'/tmp'
			step         = self.step +1 
			
			#backup loga file
			try:
				os.rename('log.gui.txt', log_filename)
			except:
				a = None
			
			#backup orca
			back_orca_output(output_path, step)
			
			"""
			try:
				SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
				#data_path  	 = self.builder.get_object("1window_main_dataPath_finder").get_filename()
				tmp_path = data_path + '/tmp'
				if not os.path.exists( tmp_path ): 
					os.mkdir(tmp_path)
					
				os.rename(SCRATCH + "/job.out", tmp_path+'/orca_step' + str(self.step +1) + ".out" )
				print "Saving orca output: ",  tmp_path+'/orca_step'  + str(self.step +1) + ".out"
			except:
				a = None		
			"""					
		
		
#		else:
#			SteepestDescentPath_SystemGeometry ( self.system,                     \
#												 log = dualLog,                   \
#												 functionStep      = functionStep,\
#												 logFrequency      = log_freq,    \
#												 maximumIterations = max_int,     \
#												 pathStep          = pathStep,    \
#												 saveFrequency     = trajectory_freq,   \
#												 useMassWeighting  = True         )
#			t_final = time.time()
#			log_filename = data_path+'/'+'process.log'
#			try:
#				os.rename('log.gui.txt', log_filename)
#			except:
#				a = None
#			
#			output_path  = data_path+'/tmp'
#			step         = self.step + 1 
#			#backup orca
#			back_orca_output(output_path, step)				
			
			x,y = parse_log_file (log_filename)
		
		return x,y,(t_final - t_initial)	
        """ adicionar
        SteepestDescentMinimize_SystemGeometry   ( system,                        \
                                                   maximumIterations    = 300   , \
                                                   logFrequency         = 1     , \
                                                   stepSize             = 1.0e-3, \
                                                   rmsGradientTolerance = 2.0,    \
                                                   trajectories           = [ ( trajectory, 1 ) ] )	
        """

	def run_dynamics(self,
			data_path,
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
			dualLog):

		rng = Random()
		rng.seed(seed)

		self.system.Summary(dualLog)
		
		os.rename("log.gui.txt", "log.gui.old")
		self.system.Summary ( dualLog )
		
		t_initial = time.time ()
		
		trajectory = SystemGeometryTrajectory ( os.path.join ( data_path,trajectory_name), 
							self.system, mode = "w" )

		if method == "Velocity Verlet Dynamics":
			VelocityVerletDynamics_SystemGeometry(self.system,
								trajectories         =[ ( trajectory, trajectory_freq) ],
								rng                       =   rng,
								log                       =   dualLog, 
								logFrequency              =   log_freq,
								steps                     =   nsteps,
								timeStep                  =   timestep,
								temperatureScaleFrequency =   temp_scale_freq,
								temperatureScaleOption    =   "constant",
								temperatureStart          =   temperature )
		
		elif method == "Leap Frog Dynamics":
			LeapFrogDynamics_SystemGeometry(self.system,
								trajectories        =[ ( trajectory, trajectory_freq) ],
								log                 = dualLog,
								logFrequency        = log_freq,
								rng                 = rng, 
								pressure            = 1.0,
								pressureCoupling    = 2000.0,
								steps               = nsteps,
								timeStep            = timestep,
								temperature         = 300.0, 
								temperatureCoupling = 0.1 
								)
		
		elif method == "Langevin Dynamics":
			LangevinDynamics_SystemGeometry (self.system, 
							trajectories         =[ ( trajectory, trajectory_freq) ],
							collisionFrequency = coll_freq, 
							log                = dualLog, 
							logFrequency       = log_freq, 
							steps              =  nsteps, 
							temperature        = temperature, 
							rng                = rng, 
							timeStep           = timestep )
		else:
			print "Select a method"

		t_final = time.time()

		log_file = data_path+ "/"+ trajectory_name + "/"+"process.log"

		os.rename('log.gui.txt',log_file)

	def run_NEB(self, reactants_file, products_file, data_path, NEB_number_of_structures, NEB_maximum_interations, NEB_grad_tol, trajectory_name, plot_flag, dualLog ):
		     
	
		try:
			os.rename('log.gui.txt','log.gui.old')
		except:
			a = None

		t_initial = time.time()
		
		reactants = XYZFile_ToCoordinates3(os.path.join ( reactants_file ), log = dualLog  )
		products  = XYZFile_ToCoordinates3(os.path.join ( products_file ), log = dualLog )
	# . Create a starting trajectory.
		trajectoryPath = (data_path + "/"+trajectory_name )
		GrowingStringInitialPath ( self.system, NEB_number_of_structures, reactants, products, trajectoryPath, log = dualLog )

	# . Pathway.
		trajectory = SystemGeometryTrajectory ( trajectoryPath, self.system, mode = "a+" )
		NudgedElasticBandSplineOptimize_SystemGeometry ( self.system, trajectory, log = dualLog, maximumIterations = NEB_maximum_interations, rmsGradientTolerance = NEB_grad_tol )
		#print NEB_data
		trajectory.Close ( )
		
		t_final = time.time()
		try:
			os.rename("log.gui.txt", trajectoryPath + "/"+"process.log")
		except:
			a = None
		
		
		#loading grafic
		if plot_flag:
			log_filename = trajectoryPath + "/"+"process.log"
			x,y = parse_log_file (log_filename)
			return x,y,(t_final - t_initial)
				










	def run_SAW(self, reactants_file, products_file, data_path, SAW_number_of_structures, SAW_maximum_interations, SAW_gamma, trajectory_name, plot_flag, dualLog ):
		try:
			os.rename('log.gui.txt','log.gui.old')
		except:
			a = None

		t_initial = time.time()
		
		reactants = XYZFile_ToCoordinates3(os.path.join ( reactants_file ), log = dualLog  )
		products  = XYZFile_ToCoordinates3(os.path.join ( products_file ), log = dualLog )
	
		# . Create a starting trajectory.
		trajectory = SystemGeometryTrajectory.LinearlyInterpolate ( os.path.join ( data_path, trajectory_name), self.system, SAW_number_of_structures, reactants, products )

	
		# . Pathway.
		SAWOptimize_SystemGeometry ( self.system,                                    \
									 trajectory,                                     \
									 log = dualLog,                                  \
									 gamma             = SAW_gamma,                  \
									 maximumIterations = SAW_maximum_interations     )	
	
		#print NEB_data
		trajectory.Close ( )
		
		t_final = time.time()
		trajectoryPath = os.path.join ( data_path, trajectory_name)

		try:
			os.rename("log.gui.txt", trajectoryPath + "/"+"process.log")
		except:
			a = None
		
		#loading grafic
		if plot_flag:
			log_filename = trajectoryPath + "/"+"process.log"
			x,y = parse_log_file (log_filename)
			return x,y,(t_final - t_initial)



















	def run_NormalModes(self, data_path, traj_name, mode, cycles, frames, temp, dualLog):
		
		self.system.Summary ( dualLog )	
		os.rename("log.gui.txt", "log.gui.old")
		
		t0=time.time ()
		
		self.system.Summary ( dualLog )

		NormalModes_SystemGeometry ( self.system, log = dualLog, modify = "project" )

		# . Create an output trajectory.
		trajectory = SystemGeometryTrajectory ( os.path.join ( data_path, traj_name ),self.system, mode = "w" )
		
		# . Generate a trajectory for one of the modes.
		NormalModesTrajectory_SystemGeometry ( self.system,       \
										       trajectory,        \
										       mode   =  mode,    \
										       cycles = cycles,   \
										       frames = frames,   \
										       temperature = temp )
		t0 = time.time () -t0
		#print normal
		os.rename("log.gui.txt", data_path+ "/"+ traj_name + "/"+"process.log")		
		return t0
		
	def run_SCAN (self, 
					outpath, 
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
					mim_method, 
					dualLog ):
		""" SCAN em uma dimensao """
		
		# recording data
		X_general = []
		Y_general = []
		
      # arquivo final
		
		self.system.Summary(dualLog)
		os.rename("log.gui.txt", "log.gui.old")
		self.system.Summary ( dualLog )		
		
		
		os.rename("log.gui.txt", (outpath+"/process.log"))
		arq = open(outpath+ "/"+"process.log", "a")		
		text = ""
		text = text + "\n------------------------ GTKDynamo SCAN  Simple-Distance -----------------------"
		
		text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (ATOM1,  ATOM1_name)
		text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s" % (ATOM2,  ATOM2_name)			
			
		text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15i" % (NWINDOWS,  FORCECONSTANT)            
		text = text + "\nDMINIMUM               =%15.5f  MAX INTERACTIONS       =%15i" % (DMINIMUM,  max_int)
		text = text + "\nSTEP SIZE              =%15.7f  RMS GRAD               =%15.7f"  % (DINCREMENT, rms_grad)
		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n\n------------------------------------------------------"
		text = text + "\n       Frame    distance pK1 - pK2         Energy     "
		text = text + "\n------------------------------------------------------"
		
		
		DINCREMENT    =   DINCREMENT
		# . Define the atom indices.
		
		# . Define a constraint container and assign it to the system.
		constraints = SoftConstraintContainer ( )
		self.system.DefineSoftConstraints ( constraints )

		if mim_method == 'Conjugate Gradient':
			

			for i in range ( NWINDOWS ):
		
				distance = DINCREMENT * float ( i ) + DMINIMUM
				scModel    = SoftConstraintEnergyModelHarmonic ( distance, FORCECONSTANT )
				constraint = SoftConstraintDistance ( ATOM1, ATOM2, scModel )
				constraints["ReactionCoord"] = constraint			
					
				# . Optimization.
				
				self.system.Summary ( dualLog )	
				os.rename("log.gui.txt", "log.gui.old")		
				self.system.Summary ( dualLog )
				
				print 'Step : ',i
				ConjugateGradientMinimize_SystemGeometry ( self.system,
															log = dualLog,
															logFrequency         = 1, \
															maximumIterations    = max_int, \
															rmsGradientTolerance = rms_grad )
				os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
				
				x,y = parse_log_file (outpath+ "/"+"tmp.log")
				
				#appending text
				#text = text + str(i) + "        "
				
				X_general.append(i)
				Y_general.append(y[-1])
				
				real_distance = self.system.coordinates3.Distance (ATOM1, ATOM2,)
				
				#appending text
				#text = text + str(real_distance) + "       "
				#appending text
				#text = text + str(y[-1]) + "\n"
				
				text = text + "\n%9i       %13.12f       %13.12f"% (int(i), float(real_distance), float(y[-1]))
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				
				output_path  = outpath
				step         = self.step + i
				#backup orca
				back_orca_output(output_path, step)	
				
			self.system.DefineSoftConstraints ( None )
			
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			
			return X_general, Y_general
		
		elif mim_method == 'Steepest Descent':
			

			for i in range ( NWINDOWS ):
		
				distance = DINCREMENT * float ( i ) + DMINIMUM
				scModel    = SoftConstraintEnergyModelHarmonic ( distance, FORCECONSTANT )
				constraint = SoftConstraintDistance ( ATOM1, ATOM2, scModel )
				constraints["ReactionCoord"] = constraint			
					
				# . Optimization.
				
				self.system.Summary ( dualLog )	
				os.rename("log.gui.txt", "log.gui.old")		
				self.system.Summary ( dualLog )
				
				SteepestDescentMinimize_SystemGeometry ( self.system,
															log = dualLog,
															logFrequency         = 1, \
															maximumIterations    = max_int, \
															rmsGradientTolerance = rms_grad )
				os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
				
				x,y = parse_log_file (outpath+ "/"+"tmp.log")
				
				#appending text
				#text = text + str(i) + "        "
				
				X_general.append(i)
				Y_general.append(y[-1])
				
				real_distance = self.system.coordinates3.Distance (ATOM1, ATOM2,)
				
				#appending text
				#text = text + str(real_distance) + "       "
				#appending text
				#text = text + str(y[-1]) + "\n"
				
				text = text + "\n%9i       %13.12f       %13.12f"% (int(i), float(real_distance), float(y[-1]))
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )

				output_path  = outpath
				step         = self.step + i
				#backup orca
				back_orca_output(output_path, step)	

			self.system.DefineSoftConstraints ( None )
			
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			
			return X_general, Y_general
		
	def run_SCAN_d1_d2 (self, 
					  outpath, 
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
					  dualLog):


		print "DMINIMUM"     ,DMINIMUM
		print "NWINDOWS"     ,NWINDOWS
		print "DINCREMENT"   ,DINCREMENT
		print "FORCECONSTANT",FORCECONSTANT

		# recording data
		X_general = []
		Y_general = []

		self.system.Summary(dualLog)
		os.rename("log.gui.txt", "log.gui.old")
		self.system.Summary ( dualLog )		
		
		
		os.rename("log.gui.txt", (outpath+"/process.log"))
		arq = open(outpath+ "/"+"process.log", "a")		
		text = ""

		text = text + "\n------------------------ GTKDynamo SCAN Multiple-Distance ----------------------"	
		
		text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (ATOM1, ATOM1_name)
		text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s" % (ATOM2, ATOM2_name)
		text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s" % (ATOM3, ATOM3_name)		
		
		text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15i" % (NWINDOWS,  FORCECONSTANT)            
		text = text + "\nDMINIMUM               =%15.5f  MAX INTERACTIONS       =%15i" % (DMINIMUM,  max_int)
		text = text + "\nSTEP SIZE              =%15.7f  RMS GRAD               =%15.7f"  % (DINCREMENT, rms_grad)
		text = text + "\nSigma atom1 - atom3    =%15.5f  Sigma atom3 - atom1    =%15.5f" % (sigma_pk1_pk3, sigma_pk3_pk1)		

		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n\n---------------------------------------------------------------------------"
		text = text + "\n      Frame    distance pK1 - pK2    distance pK2 - pK3         Energy     "
		text = text + "\n---------------------------------------------------------------------------"
		


		DINCREMENT    =   DINCREMENT
		
				
		# . Define a constraint container and assign it to the system.
		constraints = SoftConstraintContainer ( )
		self.system.DefineSoftConstraints ( constraints )

		if mim_method == 'Conjugate Gradient':

			for i in range ( NWINDOWS ):

			# Calculate the new reaction coordinate restraint
				
				rxncoord = DMINIMUM + DINCREMENT * float ( i )
				scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
				constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
				#constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, 1.0], [ATOM2, ATOM3, -1.0]], scmodel )

				constraints["ReactionCoord"] = constraint
					
				# . Optimization.
				self.system.Summary ( dualLog )	
				
				os.rename("log.gui.txt", "log.gui.old")		
				
				self.system.Summary ( dualLog )
				
				ConjugateGradientMinimize_SystemGeometry ( self.system,
															log = dualLog,
															logFrequency         = 1, \
															maximumIterations    = max_int, \
															rmsGradientTolerance = rms_grad )
				
				os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
				
				x,y = parse_log_file (outpath+ "/"+"tmp.log")
				
				#appending text
				#text = text + str(i) + "        "
				
				X_general.append(i)
				Y_general.append(y[-1])
				
				real_distance1 = self.system.coordinates3.Distance (ATOM1, ATOM2,)
				real_distance2 = self.system.coordinates3.Distance (ATOM2, ATOM3,)
				
				#appending text
				#text = text + str(real_distance) + "       "
				#appending text
				#text = text + str(y[-1]) + "\n"
				text = text + "\n%9i       %13.12f        %13.12f      %13.12f"% (int(i), float(real_distance1), float(real_distance2), float(y[-1]))
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
			
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			
			self.system.DefineSoftConstraints ( None )
			return X_general, Y_general	

		elif mim_method == 'Steepest Descent':

			for i in range ( NWINDOWS ):

			# Calculate the new reaction coordinate restraint
				
				rxncoord = DMINIMUM + DINCREMENT * float ( i )
				scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
				constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
				constraints["ReactionCoord"] = constraint
					
				# . Optimization.
				self.system.Summary ( dualLog )	
				
				os.rename("log.gui.txt", "log.gui.old")		
				
				self.system.Summary ( dualLog )
				
				SteepestDescentMinimize_SystemGeometry ( self.system,
															log = dualLog,
															logFrequency         = 1, \
															maximumIterations    = max_int, \
															rmsGradientTolerance = rms_grad )
				
				os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
				
				x,y = parse_log_file (outpath+ "/"+"tmp.log")
				
				#appending text
				#text = text + str(i) + "        "
				
				X_general.append(i)
				Y_general.append(y[-1])
				
				real_distance1 = self.system.coordinates3.Distance (ATOM1, ATOM2,)
				real_distance2 = self.system.coordinates3.Distance (ATOM2, ATOM3,)
				
				#appending text
				#text = text + str(real_distance) + "       "
				#appending text
				#text = text + str(y[-1]) + "\n"
				text = text + "\n%9i       %13.12f        %13.12f      %13.12f"% (int(i), float(real_distance1), float(real_distance2), float(y[-1]))
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
			
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			
			self.system.DefineSoftConstraints ( None )
			return X_general, Y_general	


	def run_SCAN_2D_2 (self, 
					  outpath, 
					  REACTION_COORD1,
					  REACTION_COORD2,
					  PARAMETERS,
					  mim_method,    
					  dualLog):
		
		'''
		Este eh a funcao de SCAN 2D que esta em USO.
		
		'''
		#-----------------#
		#   REAC COORD 1  #
		#-----------------#
		
		self.system.Summary(dualLog)
		os.rename("log.gui.txt", "log.gui.old")
		self.system.Summary ( dualLog )		
		os.rename("log.gui.txt", (outpath+"/process.log"))
		arq = open(outpath+ "/"+"process.log", "a")		
		mode1 = REACTION_COORD1['mode']

		text = ""
		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n--                                                                            --"
		text = text + "\n--                          GTKDynamo SCAN  2D                                --"
		text = text + "\n--                                                                            --"
		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n"
		
		if mode1 == 'simple-distance':
			coord1_ATOM1            = REACTION_COORD1['atom1']
			coord1_ATOM1_name       = REACTION_COORD1['atom1_name']
			coord1_ATOM2            = REACTION_COORD1['atom2']
			coord1_ATOM2_name       = REACTION_COORD1['atom2_name']
			coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS1']
			coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM1']
			coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT1']
			coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT1']
			
			text = text + "\n----------------------- Coordinate 1 - Simple-Distance -------------------------"												
			text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (coord1_ATOM1,     coord1_ATOM1_name)
			text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s" % (coord1_ATOM2,     coord1_ATOM2_name)
			text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15.5f" % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    			
			text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    			
			text = text + "\n--------------------------------------------------------------------------------"
			
		if mode1 == "multiple-distance":
			coord1_ATOM1            = REACTION_COORD1['atom1']
			coord1_ATOM1_name       = REACTION_COORD1['atom1_name']
			coord1_ATOM2            = REACTION_COORD1['atom2']
			coord1_ATOM2_name       = REACTION_COORD1['atom2_name']	
			coord1_ATOM3            = REACTION_COORD1['atom3']
			coord1_ATOM3_name       = REACTION_COORD1['atom3_name']	
			coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS1']
			coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM1']
			coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT1']
			coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT1']

			coord1_sigma_pk1_pk3    = REACTION_COORD1['sigma_pk1_pk3_coord1']
			coord1_sigma_pk3_pk1    = REACTION_COORD1['sigma_pk3_pk1_coord1']


			#coord1_sigma_pk1_pk3, coord1_sigma_pk3_pk1 = compute_sigma_a1_a3 (coord1_ATOM1_name, coord1_ATOM3_name)
			
			text = text + "\n--------------------- Coordinate 1 - Multiple-Distance -------------------------"												
			text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (coord1_ATOM1,     coord1_ATOM1_name)
			text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s" % (coord1_ATOM2,     coord1_ATOM2_name)
			text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s" % (coord1_ATOM3,     coord1_ATOM3_name)
			text = text + "\nSIGMA ATOM1/ATOM3      =%15.5f  SIGMA ATOM3/ATOM1      =%15.5f" % (coord1_sigma_pk1_pk3, coord1_sigma_pk3_pk1) 
			text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15.5f" % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    			
			text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    			
			text = text + "\n--------------------------------------------------------------------------------"
	

		#-----------------#
		#   REAC COORD 2  #
		#-----------------#
				
		mode2 = REACTION_COORD2['mode']
		#print REACTION_COORD2
		#print "mode2: ", mode2
		
		if mode2 == 'simple-distance':
			coord2_ATOM1            = REACTION_COORD2['atom1']
			coord2_ATOM1_name       = REACTION_COORD2['atom1_name']
			coord2_ATOM2            = REACTION_COORD2['atom2']
			coord2_ATOM2_name       = REACTION_COORD2['atom2_name']
			coord2_NWINDOWS2        = REACTION_COORD2['NWINDOWS2']
			coord2_DMINIMUM2        = REACTION_COORD2['DMINIMUM2']
			coord2_FORCECONSTANT2   = REACTION_COORD2['FORCECONSTANT2']
			coord2_DINCREMENT2      = REACTION_COORD2['DINCREMENT2']
			
			text = text + "\n----------------------- Coordinate 2 - Simple-Distance -------------------------"												
			text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (coord2_ATOM1,     coord2_ATOM1_name)
			text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s" % (coord2_ATOM2,     coord2_ATOM2_name)
			text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15.5f" % (coord2_NWINDOWS2, coord2_FORCECONSTANT2)    			
			text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord2_DMINIMUM2, coord2_DINCREMENT2)    			
			text = text + "\n--------------------------------------------------------------------------------"
			text = text + "\n"
		
		if mode2 == "multiple-distance":
			coord2_ATOM1            = REACTION_COORD2['atom1']
			coord2_ATOM1_name       = REACTION_COORD2['atom1_name']
			coord2_ATOM2            = REACTION_COORD2['atom2']
			coord2_ATOM2_name       = REACTION_COORD2['atom2_name']	
			coord2_ATOM3            = REACTION_COORD2['atom3']
			coord2_ATOM3_name       = REACTION_COORD2['atom3_name']	
			coord2_NWINDOWS2        = REACTION_COORD2['NWINDOWS2']
			coord2_DMINIMUM2        = REACTION_COORD2['DMINIMUM2']
			coord2_FORCECONSTANT2   = REACTION_COORD2['FORCECONSTANT2']
			coord2_DINCREMENT2      = REACTION_COORD2['DINCREMENT2']	
			
			coord2_sigma_pk1_pk3    = REACTION_COORD2['sigma_pk1_pk3_coord2']
			coord2_sigma_pk3_pk1    = REACTION_COORD2['sigma_pk3_pk1_coord2']			
			
			#coord2_sigma_pk1_pk3, coord2_sigma_pk3_pk1 = compute_sigma_a1_a3 (coord2_ATOM1_name, coord2_ATOM3_name)
			
			text = text + "\n--------------------- Coordinate 2 - Multiple-Distance -------------------------"												
			text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (coord2_ATOM1,     coord2_ATOM1_name)
			text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s" % (coord2_ATOM2,     coord2_ATOM2_name)
			text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s" % (coord2_ATOM3,     coord2_ATOM3_name)
			text = text + "\nSIGMA ATOM1/ATOM3      =%15.5f  SIGMA ATOM3/ATOM1      =%15.5f" % (coord2_sigma_pk1_pk3, coord2_sigma_pk3_pk1) 
			text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15.5f" % (coord2_NWINDOWS2, coord2_FORCECONSTANT2)    			
			text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord2_DMINIMUM2, coord2_DINCREMENT2)    			
			text = text + "\n--------------------------------------------------------------------------------"
			text = text + "\n"	


		max_int               = PARAMETERS['max_int']
		log_freq              = PARAMETERS['log_freq']
		rms_grad              = PARAMETERS['rms_grad']		
		#system_backup         = self.system    
		
		#------------------------------#
		import numpy as np
		X = 0*np.random.rand (coord1_NWINDOWS1, coord2_NWINDOWS2)
		#------------------------------#

		# . Define a constraint container and assign it to the system.
		
		constraints  = SoftConstraintContainer ( )
		self.system.DefineSoftConstraints ( constraints)
		
		#self.system.Summary ( dualLog )
		
		print REACTION_COORD1
		print REACTION_COORD2
		
		if mim_method == 'Conjugate Gradient':
		
			for i in range ( coord1_NWINDOWS1 ):
				#self.system = system_backup  
				# Calculate the new reaction coordinate restraint
				if mode1 == 'simple-distance':
					rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float   ( i )
					scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )
					constraint   = SoftConstraintDistance         ( coord1_ATOM1, coord1_ATOM2, scModel )
					constraints["ReactionCoord"] = constraint
				
				if mode1 == "multiple-distance":
					rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )
					scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )
					constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1, coord1_sigma_pk1_pk3], [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]], scmodel )
					constraints["ReactionCoord"] = constraint			
					
				text = text + "\nMATRIX1 "


				for j in range (coord2_NWINDOWS2):
					if mode2 == 'simple-distance':
						rxncoord2    = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )
						scModel2     = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )
						constraint2  = SoftConstraintDistance          (coord2_ATOM1, coord2_ATOM2, scModel2)
						constraints["ReactionCoord2"] = constraint2				
					
					if mode2 == "multiple-distance":
						rxncoord2     = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )
						scmodel2      = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )
						constraint2   = SoftConstraintMultipleDistance ([[coord2_ATOM2, coord2_ATOM1, coord2_sigma_pk1_pk3], [coord2_ATOM2, coord2_ATOM3, coord2_sigma_pk3_pk1]], scmodel2 )
						constraints["ReactionCoord2"] = constraint2
					

					self.system.Summary ( dualLog )	
					os.rename("log.gui.txt", "log.gui.old")		
					self.system.Summary ( dualLog )
					
					print 'Step : ',i,j
					
					ConjugateGradientMinimize_SystemGeometry ( self.system,
																log = dualLog,
																logFrequency         = log_freq , \
																maximumIterations    = max_int  , \
																rmsGradientTolerance = rms_grad )
					try:
						XMLPickle ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )
					except:
						Pickle    ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )		
					
					
					distance_a3_a4 = self.system.coordinates3.Distance (coord2_ATOM1, coord2_ATOM2)
					
					os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
					x,y = parse_log_file (outpath+ "/"+"tmp.log")
					
					X[i][j] = y[-1]
					text = text + "%18.8f  " % (X[i][j]) 	
			
			#X_norm = 0*np.random.rand (coord1_NWINDOWS1, coord2_NWINDOWS2)
			
			# creating a normalized matrix
			X_norm = X - np.min(X)
			
			n1 = coord1_NWINDOWS1
			n2 = coord2_NWINDOWS2
			
			text = text + "\n\n"
			
			for i in range(n1):
				text = text + "\nMATRIX2 "
				for j in range(n2):
					text = text + "%18.8f  " % (X_norm[i][j])
			
			
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			self.system.DefineSoftConstraints ( None )
			return X, X_norm
		
		elif mim_method == 'Steepest Descent':
		
			for i in range ( coord1_NWINDOWS1 ):
				#self.system = system_backup  
				# Calculate the new reaction coordinate restraint
				if mode1 == 'simple-distance':
					rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float   ( i )
					scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )
					constraint   = SoftConstraintDistance         ( coord1_ATOM1, coord1_ATOM2, scModel )
					constraints["ReactionCoord"] = constraint
				
				if mode1 == "multiple-distance":
					rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )
					scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )
					constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1, coord1_sigma_pk1_pk3], [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]], scmodel )
					constraints["ReactionCoord"] = constraint			
					
				text = text + "\nMATRIX1 "


				for j in range (coord2_NWINDOWS2):
					if mode2 == 'simple-distance':
						rxncoord2    = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )
						scModel2     = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )
						constraint2  = SoftConstraintDistance          (coord2_ATOM1, coord2_ATOM2, scModel2)
						constraints["ReactionCoord2"] = constraint2				
					
					if mode2 == "multiple-distance":
						rxncoord2     = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( i )
						scmodel2      = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )
						constraint2   = SoftConstraintMultipleDistance ([[coord2_ATOM2, coord2_ATOM1, coord2_sigma_pk1_pk3], [coord2_ATOM2, coord2_ATOM3, coord2_sigma_pk3_pk1]], scmodel2 )
						constraints["ReactionCoord2"] = constraint2
					

					self.system.Summary ( dualLog )	
					os.rename("log.gui.txt", "log.gui.old")		
					self.system.Summary ( dualLog )
					
					print 'Step : ',i,j
					SteepestDescentMinimize_SystemGeometry ( self.system,
																log = dualLog,
																logFrequency         = log_freq , \
																maximumIterations    = max_int  , \
																rmsGradientTolerance = rms_grad )
					try:
						XMLPickle ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )
					except:
						Pickle    ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )		
					
					
					distance_a3_a4 = self.system.coordinates3.Distance (coord2_ATOM1, coord2_ATOM2)
					
					os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
					x,y = parse_log_file (outpath+ "/"+"tmp.log")
					
					try:
						X[i][j] = y[-1]
					except:
						X[i][j] = 0
					text = text + "%18.8f  " % (X[i][j]) 	
			
			#X_norm = 0*np.random.rand (coord1_NWINDOWS1, coord2_NWINDOWS2)
			
			# creating a normalized matrix
			X_norm = X - np.min(X)
			
			n1 = coord1_NWINDOWS1
			n2 = coord2_NWINDOWS2
			
			text = text + "\n\n"
			
			for i in range(n1):
				text = text + "\nMATRIX2 "
				for j in range(n2):
					text = text + "%18.8f  " % (X_norm[i][j])
			
			
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			self.system.DefineSoftConstraints ( None )
			return X, X_norm

	''' esta funcao esta obsoleta
	
	def run_SCAN_2D  (self, 
					  outpath, 
					  ATOM1, 
					  ATOM2, 
					  ATOM3,
					  ATOM4,
					  
					  NAME1,
					  NAME2,
					  NAME3,
					  NAME4,
	  
					  DINCREMENT1,
					  DINCREMENT2,
					  mim_method,
					  NWINDOWS1,
					  NWINDOWS2,
					  FORCECONSTANT1,
					  FORCECONSTANT2, 
					  DMINIMUM1,     
					  DMINIMUM2,
					  PARAMETERS,    
					  dualLog):
		
		if DMINIMUM1 == "AUTO":
			DMINIMUM1 = self.system.coordinates3.Distance (ATOM1, ATOM2)
		else:
			DMINIMUM1 = float(DMINIMUM1)
			 
		if DMINIMUM2 == "AUTO":
			DMINIMUM2 = self.system.coordinates3.Distance (ATOM3, ATOM4)		
		else:
			DMINIMUM2 = float(DMINIMUM2)
			
		print "Atom 1 : ",ATOM1
		print "Atom 2 : ",ATOM2
		print "Atom 3 : ",ATOM3
		print "Atom 4 : ",ATOM4
		
		print "DINCREMENT1 :"   ,DINCREMENT1
		print "DINCREMENT2 :"   ,DINCREMENT2
		 
		print "NWINDOWS1  : "   ,NWINDOWS1
		print "NWINDOWS2  : "   ,NWINDOWS2
		
		print "FORCECONSTANT1 : ",FORCECONSTANT1
		print "FORCECONSTANT2 : ",FORCECONSTANT2

		print "DMINIMUM1  : "   ,DMINIMUM1
		print "DMINIMUM2  : "   ,DMINIMUM2


		max_int               = PARAMETERS['max_int']
		log_freq              = PARAMETERS['log_freq']
		rms_grad              = PARAMETERS['rms_grad']		
	
		
		# .starting log file.............................#
		
		self.system.Summary(dualLog)
		os.rename("log.gui.txt", "log.gui.old")
		self.system.Summary ( dualLog )		
		os.rename("log.gui.txt", (outpath+"/process.log"))
		arq = open(outpath+ "/"+"process.log", "a")		
		text = ""
		
		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n--                                                                            --"
		text = text + "\n--                          GTKDynamo SCAN  2D                                --"
		text = text + "\n--                                                                            --"
		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n"
		text = text + "\n-------------------------------- Coordinate 1 ----------------------------------"												
		text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (ATOM1,     NAME1)
		text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s" % (ATOM2,     NAME2)
		text = text + "\nNWINDOWS1              =%15i  FOCE CONSTANT1         =%15.5F" % (NWINDOWS1, FORCECONSTANT1)            
		text = text + "\nDMINIMUM1              =%15.5f  DINCREMENT1            =%15.5f" % (DMINIMUM1,DINCREMENT1)
		text = text + "\n-------------------------------- Coordinate 2 ----------------------------------"												
		text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s" % (ATOM3,     NAME3)
		text = text + "\nATOM4                  =%15i  ATOM NAME4             =%15s" % (ATOM4,     NAME4)
		text = text + "\nNWINDOWS2              =%15i  FOCE CONSTANT2         =%15.5f" % (NWINDOWS2, FORCECONSTANT2)            
		text = text + "\nDMINIMUM2              =%15.5f  DINCREMENT2            =%15.5f" % (DMINIMUM2,DINCREMENT2)
		text = text + "\n--------------------------------------------------------------------------------"
		text = text + "\n"
		
			
		#------------------------------#
		
		import numpy as np
			
		X = 0*np.random.rand (NWINDOWS1,NWINDOWS2)
		
		#------------------------------#



		# . Define a constraint container and assign it to the system.
		
		constraints  = SoftConstraintContainer ( )
		constraints2 = SoftConstraintContainer ( )
		
		self.system.DefineSoftConstraints ( constraints)
		#self.system.DefineSoftConstraints ( constraints2 )
		
		self.system.Summary ( dualLog )
		
		system_backup = self.system

		
		if mim_method == 'Conjugate Gradient':
		
			for i in range ( NWINDOWS1 ):
				self.system = system_backup

				# Calculate the new reaction coordinate restraint
				rxncoord     = DMINIMUM1 + DINCREMENT1 * float   ( i )
				scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT1 )
				
				constraint   = SoftConstraintDistance ( ATOM1, ATOM2, scModel )
				constraints["ReactionCoord"] = constraint
				
				#distance_a1_a2 = self.system.coordinates3.Distance (ATOM1, ATOM2)
				
				text = text + "\nMATRIX "
				for j in range (NWINDOWS2):
					rxncoord2   = DMINIMUM2 + DINCREMENT2 * float ( j )
					scModel2    = SoftConstraintEnergyModelHarmonic ( rxncoord2, FORCECONSTANT2 )
					
					constraint2 = SoftConstraintDistance ( ATOM3, ATOM4, scModel2)
					constraints["ReactionCoord2"] = constraint2				

					self.system.Summary ( dualLog )	
					os.rename("log.gui.txt", "log.gui.old")		
					self.system.Summary ( dualLog )
					
					ConjugateGradientMinimize_SystemGeometry ( self.system,
																log = dualLog,
																logFrequency         = log_freq , \
																maximumIterations    = max_int  , \
																rmsGradientTolerance = rms_grad )
					try:
						XMLPickle ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )
					except:
						Pickle    ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )		
					
					
					distance_a3_a4 = self.system.coordinates3.Distance (ATOM3, ATOM4)
					
					os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
					x,y = parse_log_file (outpath+ "/"+"tmp.log")
					
					X[i][j] = y[-1]
					text = text + "%18.8f  " % (X[i][j]) 	
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			return X
		
		elif mim_mehtod2 == 'Steepest Descent':

			for i in range ( NWINDOWS1 ):
				self.system = system_backup

				# Calculate the new reaction coordinate restraint
				rxncoord     = DMINIMUM1 + DINCREMENT1 * float   ( i )
				scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT1 )
				
				constraint   = SoftConstraintDistance ( ATOM1, ATOM2, scModel )
				constraints["ReactionCoord"] = constraint
				
				#distance_a1_a2 = self.system.coordinates3.Distance (ATOM1, ATOM2)
				
				text = text + "\nMATRIX "
				for j in range (NWINDOWS2):
					rxncoord2   = DMINIMUM2 + DINCREMENT2 * float ( j )
					scModel2    = SoftConstraintEnergyModelHarmonic ( rxncoord2, FORCECONSTANT2 )
					
					constraint2 = SoftConstraintDistance ( ATOM3, ATOM4, scModel2)
					constraints["ReactionCoord2"] = constraint2				

					self.system.Summary ( dualLog )	
					os.rename("log.gui.txt", "log.gui.old")		
					self.system.Summary ( dualLog )
					
					SteepestDescentMinimize_SystemGeometry ( self.system,
																log = dualLog,
																logFrequency         = log_freq , \
																maximumIterations    = max_int  , \
																rmsGradientTolerance = rms_grad )
					try:
						XMLPickle ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )
					except:
						Pickle    ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), self.system.coordinates3 )		
					
					
					distance_a3_a4 = self.system.coordinates3.Distance (ATOM3, ATOM4)
					
					os.rename("log.gui.txt",  outpath+ "/"+"tmp.log")
					x,y = parse_log_file (outpath+ "/"+"tmp.log")
					
					X[i][j] = y[-1]
					text = text + "%18.8f  " % (X[i][j]) 	
			#print text
			text = str(text)
			arq.writelines(text)
			
			arq.close()
			return X

	'''
	 
	def run_umbrella_sampling (self, 
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
							dualLog ):
		""" simple SCAN, restricted coordinate """
		
		
		
		
		DINCREMENT    =   DINCREMENT
		# . Define the atom indices.
		
		# . Define a constraint container and assign it to the system.
		constraints = SoftConstraintContainer ( )
		self.system.DefineSoftConstraints ( constraints )

		for i in range ( NWINDOWS ):
	
			distance = DINCREMENT * float ( i ) + DMINIMUM
			scModel    = SoftConstraintEnergyModelHarmonic ( distance, FORCECONSTANT )
			constraint = SoftConstraintDistance ( ATOM1, ATOM2, scModel )
			constraints["ReactionCoord"] = constraint			
				
			# . Optimization.

			#--------------------------------------------------------------------------------#
			rng = Random ( )
			rng.seed ( 291731 + i )
			# . Equilibration.
			
			
			MD_mode = MDyn_dic['MD_mode']
	
	
	
			
			#----------------------------#
			#    "Leap Frog Dynamics"    #
			#----------------------------#
						
			if MD_mode == "Leap Frog Dynamics":			
				
				logFrequency        = MDyn_dic['log_freq']
				steps               = MDyn_dic['nsteps_EQ']
				temperature         = MDyn_dic['temperature']
				temperatureCoupling = MDyn_dic['temperatureCoupling']
				timeStep            = MDyn_dic['timestep']
				
				# . Equilibration.
				LeapFrogDynamics_SystemGeometry ( self.system,                               \
												  logFrequency        = logFrequency,        \
												  rng                 = rng,                 \
												  steps               = steps,               \
												  temperature         = temperature,         \
												  temperatureCoupling = temperatureCoupling, \
												  timeStep            = timeStep  )

				# . Data-collection.
				trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), self.system, mode = "w" )
				
				steps               = MDyn_dic['nsteps_DC']
				LeapFrogDynamics_SystemGeometry ( self.system,                               \
												  logFrequency        = logFrequency,        \
												  rng                 = rng,                 \
												  steps               = steps,               \
												  temperature         = temperature,         \
												  temperatureCoupling = temperatureCoupling, \
												  timeStep            = timeStep,
												  trajectories        = [ ( trajectory, 1 ) ] )
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )

											  


			#----------------------------------#
			#    "Velocity Verlet Dynamics"    #
			#----------------------------------#
			
			if MD_mode == "Velocity Verlet Dynamics":
				
				logFrequency        = MDyn_dic['log_freq']
				steps               = MDyn_dic['nsteps_EQ']
				temperature         = MDyn_dic['temperature']
				timeStep            = MDyn_dic['timestep']
				temp_scale_freq     = MDyn_dic['temp_scale_freq']
				
				# . Equilibration.
				VelocityVerletDynamics_SystemGeometry(self.system,
													rng                       =   rng,
													log                       =   dualLog, 
													logFrequency              =   logFrequency,
													steps                     =   steps,
													timeStep                  =   0.001,
													temperatureScaleFrequency =   temp_scale_freq,
													temperatureScaleOption    =   "constant",
													temperatureStart          =   temperature )

				# . Data-collection.
				steps               = MDyn_dic['nsteps_DC']
				trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), self.system, mode = "w" )
				VelocityVerletDynamics_SystemGeometry(self.system,
													trajectories              =[ ( trajectory, 1) ],
													rng                       =   rng,
													log                       =   dualLog, 
													logFrequency              =   logFrequency,
													steps                     =   steps,
													timeStep                  =   0.001,
													temperatureScaleFrequency =   temp_scale_freq,
													temperatureScaleOption    =   "constant",
													temperatureStart          =   temperature )
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )


			
			#---------------------------#
			#    "Langevin Dynamics"    #
			#---------------------------#
			
			if MD_mode ==  "Langevin Dynamics":
				
				logFrequency        = MDyn_dic['log_freq']
				steps               = MDyn_dic['nsteps_EQ']
				temperature         = MDyn_dic['temperature']
				timeStep            = MDyn_dic['timestep']
				coll_freq           = MDyn_dic['coll_freq']
				# . Equilibration.
				LangevinDynamics_SystemGeometry (self.system, 
								logFrequency              =   logFrequency,
								log                       =   dualLog,
								rng                       =   rng,
								steps                     =   steps,
								timeStep                  =   0.001,
								collisionFrequency        = coll_freq, 
								temperature               = temperature)
												
				# . Data-collection.
				steps               = MDyn_dic['nsteps_DC']
				trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), self.system, mode = "w" )
				
				LangevinDynamics_SystemGeometry (self.system, 
								trajectories              =[ ( trajectory, 1) ],
								logFrequency              =   logFrequency,
								log                       =   dualLog,
								rng                       =   rng,
								steps                     =   steps,
								timeStep                  =   0.001,
								collisionFrequency        = coll_freq, 
								temperature               = temperature)
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )								
			
			
			#-----------------------------------------------------------------------------------------------------------#								

		fileNames = glob.glob ( os.path.join ( outpath, traj_name+"*.trj" ) )
		trajectories = []
		for fileName in fileNames:
			trajectories.append ( SystemSoftConstraintTrajectory ( fileName, self.system, mode = "r" ) )


		self.system.Summary ( dualLog )	
		os.rename("log.gui.txt", "log.gui.old")		
		self.system.Summary ( dualLog )
		
		
		
		
		# LOG FILE 
		#os.rename("log.gui.txt", (outpath+"/process.log"))
		arq = open("log.gui.txt", "a")
		
		# outpath, 
		# ATOM1, 
		# ATOM2, 
		# DINCREMENT,
		# NWINDOWS,
		# FORCECONSTANT,
		# DMINIMUM,
		# traj_name, 
		# MDyn_dic,
		# dualLog ):
		
		text = ""
		text = text + "\n------------------------ GTKDynamo SCAN  Simple-Distance -----------------------"
		
		text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (ATOM1,  ATOM1_name)
		text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s" % (ATOM2,  ATOM2_name)			
			
		text = text + "\nNWINDOWS               =%15i  FOCE CONSTANT          =%15i" % (NWINDOWS,  FORCECONSTANT)            
		#text = text + "\nDMINIMUM               =%15.5f  MAX INTERACTIONS       =%15i" % (DMINIMUM,  max_int)
		#text = text + "\nSTEP SIZE              =%15.7f  RMS GRAD               =%15.7f"  % (DINCREMENT, rms_grad)
		text = text + "\n--------------------------------------------------------------------------------"
		#text = text + "\n\n------------------------------------------------------"
		#text = text + "\n       Frame    distance pK1 - pK2         Energy     "
		#text = text + "\n------------------------------------------------------"	
		
		text = str(text)
		arq.writelines(text)
		
		arq.close()		
		
		
		# . Calculate the PMF.	
		WHAMEquationSolver ( trajectories,          \
							 log         = dualLog, \
							 bins        = 100,     \
							 temperature = 300.0 )		
		
		self.system.DefineSoftConstraints ( None )
		os.rename("log.gui.txt",  outpath+ "/"+"process.log")
		x,y = parse_log_file (outpath+ "/"+"process.log")
		return x,y

	def run_umbrella_sampling_d2_d1 (self, 
								  outpath, 
								  ATOM1, 
								  ATOM2, 
								  ATOM3,
								  DINCREMENT,
								  NWINDOWS,         # ok
								  FORCECONSTANT,    # ok
								  DMINIMUM,         # ok
								  sigma_pk1_pk3, 
								  sigma_pk3_pk1,
								  traj_name, 
							      MDyn_dic,
							      dualLog ):


		print "DMINIMUM"     ,DMINIMUM
		print "NWINDOWS"     ,NWINDOWS
		print "DINCREMENT"   ,DINCREMENT
		print "FORCECONSTANT",FORCECONSTANT
				
		# . Define a constraint container and assign it to the system.
		constraints = SoftConstraintContainer ( )
		self.system.DefineSoftConstraints ( constraints )

		for i in range ( NWINDOWS ):

		# Calculate the new reaction coordinate restraint
			
			rxncoord = DMINIMUM + DINCREMENT * float ( i )
			scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
			constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
			constraints["ReactionCoord"] = constraint
			
			# . Optimization.

			#--------------------------------------------------------------------------------#
			rng = Random ( )
			rng.seed ( 291731 + i )
			# . Equilibration.
			
			
			MD_mode = MDyn_dic['MD_mode']
			if MD_mode == "Leap Frog Dynamics":			
				
				logFrequency        = MDyn_dic['log_freq']
				steps               = MDyn_dic['nsteps_EQ']
				temperature         = MDyn_dic['temperature']
				temperatureCoupling = MDyn_dic['temperatureCoupling']
				timeStep            = MDyn_dic['timestep']
				
				# . Equilibration.
				LeapFrogDynamics_SystemGeometry ( self.system,                               \
												  logFrequency        = logFrequency,        \
												  rng                 = rng,                 \
												  steps               = steps,               \
												  temperature         = temperature,         \
												  temperatureCoupling = temperatureCoupling, \
												  timeStep            = timeStep  )

				# . Data-collection.
				trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), self.system, mode = "w" )
				
				steps               = MDyn_dic['nsteps_DC']
				LeapFrogDynamics_SystemGeometry ( self.system,                               \
												  logFrequency        = logFrequency,        \
												  rng                 = rng,                 \
												  steps               = steps,               \
												  temperature         = temperature,         \
												  temperatureCoupling = temperatureCoupling, \
												  timeStep            = timeStep,
												  trajectories        = [ ( trajectory, 1 ) ] )
											  
			#--------------------------------------------------------------------------------#
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )

			
			if MD_mode == "Velocity Verlet Dynamics":
				
				logFrequency        = MDyn_dic['log_freq']
				steps               = MDyn_dic['nsteps_EQ']
				temperature         = MDyn_dic['temperature']
				timeStep            = MDyn_dic['timestep']
				temp_scale_freq     = MDyn_dic['temp_scale_freq']
				
				# . Equilibration.
				VelocityVerletDynamics_SystemGeometry(self.system,
													rng                       =   rng,
													log                       =   dualLog, 
													logFrequency              =   logFrequency,
													steps                     =   steps,
													timeStep                  =   0.001,
													temperatureScaleFrequency =   temp_scale_freq,
													temperatureScaleOption    =   "constant",
													temperatureStart          =   temperature )

				# . Data-collection.
				steps               = MDyn_dic['nsteps_DC']
				trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), self.system, mode = "w" )
				VelocityVerletDynamics_SystemGeometry(self.system,
													trajectories              =[ ( trajectory, 1) ],
													rng                       =   rng,
													log                       =   dualLog, 
													logFrequency              =   logFrequency,
													steps                     =   steps,
													timeStep                  =   0.001,
													temperatureScaleFrequency =   temp_scale_freq,
													temperatureScaleOption    =   "constant",
													temperatureStart          =   temperature )
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )

			
			if MD_mode ==  "Langevin Dynamics":
				
				logFrequency        = MDyn_dic['log_freq']
				steps               = MDyn_dic['nsteps_EQ']
				temperature         = MDyn_dic['temperature']
				timeStep            = MDyn_dic['timestep']
				coll_freq           = MDyn_dic['coll_freq']
				# . Equilibration.
				LangevinDynamics_SystemGeometry (self.system, 
								logFrequency              =   logFrequency,
								log                       =   dualLog,
								rng                       =   rng,
								steps                     =   steps,
								timeStep                  =   0.001,
								collisionFrequency        = coll_freq, 
								temperature               = temperature)
												
				# . Data-collection.
				steps               = MDyn_dic['nsteps_DC']
				trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), self.system, mode = "w" )
				
				LangevinDynamics_SystemGeometry (self.system, 
								trajectories              =[ ( trajectory, 1) ],
								logFrequency              =   logFrequency,
								log                       =   dualLog,
								rng                       =   rng,
								steps                     =   steps,
								timeStep                  =   0.001,
								collisionFrequency        = coll_freq, 
								temperature               = temperature)
				
				try:
					XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
				except:
					Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )	



		fileNames = glob.glob ( os.path.join ( outpath, traj_name+"*.trj" ) )
		trajectories = []
		for fileName in fileNames:
			trajectories.append ( SystemSoftConstraintTrajectory ( fileName, self.system, mode = "r" ) )

		self.system.Summary ( dualLog )	
		os.rename("log.gui.txt", "log.gui.old")		
		self.system.Summary ( dualLog )
		# . Calculate the PMF.
		WHAMEquationSolver ( trajectories,          \
							 log         = dualLog, \
							 bins        = 100,     \
							 temperature = 300.0 )		
		
		os.rename("log.gui.txt",  outpath+ "/"+"process.log")
			
		self.system.DefineSoftConstraints ( None )


	def load_trajectory_to_system(self, first, last, stride, traj_name, new_pymol_object, export_type):
		
		i = 0 
		i = i + first
		outPath = ( traj_name )
		print first, last, stride
		
		trajectory = SystemGeometryTrajectory (traj_name, self.system, mode = "r" )
		i = 0
		a = 0
		i = i + first
	
		while trajectory.RestoreOwnerData ( ):
			if export_type == 'pdb':
				if a == i:
					PDBFile_FromSystem ( os.path.join ( outPath, new_pymol_object +".pdb" ), self.system)
					cmd.load( os.path.join ( outPath, new_pymol_object +".pdb"))
					i = i + stride
					print "loading file: ",i
				if a == last:
					break
				a=a+1
			else:
				if a == i:
					XYZFile_FromSystem ( os.path.join ( outPath, new_pymol_object +".xyz" ), self.system)
					cmd.load( os.path.join ( outPath, new_pymol_object +".xyz"))
					i = i + stride
					print "loading file: ",i
				if a == last:
					break
				a=a+1	
	
	def import_GTKDynamo_definitions_to_settings(self,
										project_name ,
										force_field  ,
										parameters   ,
										topology     ,
										coordinates  ,
										nbModel_type ,
										ABFS_options , 
										prune_table  ,
										fix_table    ,
										qc_table     ,
										QCMM         , 
										qc_method    ,
										charge       , 
										multiplicity ,
										density_tol  ,                    
										Maximum_SCF  ,
										ORCA_method  ,
										ORCA_SCF     ,
										ORCA_basis   ,
										ORCA_pal     ,
										data_path    ,
										last_step    ,
										last_frame   ,
										pymol_session):
			self.settings['project_name'] = project_name
			self.settings['force_field']  = force_field
			self.settings['parameters']   = parameters
			self.settings['topology']     = topology
			self.settings['coordinates']  = coordinates
			self.settings['nbModel_type'] = nbModel_type
			self.settings['ABFS_options'] = ABFS_options
			self.settings['prune_table']  = [] #prune_table
			self.settings['fix_table']    = fix_table
			self.settings['qc_table']     = qc_table
			self.settings['QCMM']         = QCMM
			self.settings['qc_method']    = qc_method
			
			if self.settings['qc_method'] != None:
				self.settings['charge']       = charge
				self.settings['multiplicity'] = multiplicity
			
			#if  #qc_method[0:3]  
			if	self.settings['qc_method']  == 'DFT':
				self.settings['density_tol'] = density_tol                     
				self.settings['Maximum_SCF'] = Maximum_SCF				
			
			if self.settings['qc_method'] == "ORCA - ab initio":
				self.settings['ORCA_method'] = ORCA_method
				self.settings['ORCA_SCF']    = ORCA_SCF
				self.settings['ORCA_basis']  = ORCA_basis
				self.settings['ORCA_pal']    = ORCA_pal
			
			self.settings['data_path']     = data_path
			self.settings['last_step']     = last_step
			self.settings['last_frame']    = last_frame
			self.settings['pymol_session'] = pymol_session 
  
			return True 


	
	def export_GTKDynamo_session_to_file(self, full_name):
		arq          = open(full_name + ".gtkdyn", 'w')
		text         = []
		project_name = self.settings['project_name']
		
		

		
		#writes the working folder string based on the full_name that is determined by the user#
		fullpath     = full_name.split("/")
		fullpath.pop(-1)
		fullPATH     = ""
		for i in fullpath:
			fullPATH = fullPATH + i
			fullPATH = fullPATH + "/"
		#----------------------------------------------------------------------------------------#
		
		
		
		
		# HEADER
		header       = "# GTKDynamo 0.1 - project file\n\n"
		text.append(header)		
		
		#old way to write the working folder
		'''
		# data path
		if self.settings['data_path'] == None: 
			#data_path = os.environ.get('HOME')
			
			string =     "data_path     = " + "'" + self.settings['data_path']+ "'\n"
			text.append(string)
		else:
			string =     "working_folder = " + "'" + self.settings['data_path']+ "'\n"
			text.append(string)		
		'''
		
		# working folder
		string =     "working_folder = " + "'" + fullPATH+ "'\n"
		text.append(string)	

		# XML
		try:
			XMLPickle ( full_name + ".pkl", self.system )
		
		except:
			Pickle ( full_name + ".pkl", self.system )
		
		string =     "system         = " + "'" + full_name + ".pkl" + "'\n"
		text.append(string)
		
		
		# pymol	
		cmd.save(full_name + ".pse")
		string =     "pymol_session  = " + "'" + full_name + ".pse" + "'\n"
		text.append(string)

		# last step		
		string =     "last_step      = " + str(self.step)+ "\n"
		text.append(string)		
		
		
		# last pymol id 
		try:
			string =     "last_pymol_id  = " + "'" + self.settings['last_pymol_id'] + "'\n"
		except:
			string =     "last_pymol_id  = None"
		text.append(string)	
		
		
		arq.writelines(text)
		arq.close()				
		
	
	"""
	def export_GTKDynamo_definitions_to_files(self, full_name):
		arq          = open(full_name + ".gtkdyn", 'w')
		text         = []
		project_name = self.settings['project_name']
		
		header       = "# GTKDynamo 0.1 - project file\n\n"
		text.append(header)
	
		string       =     "\n#   System parameters \n\n"
		text.append(string)			
		
		#if self.settings['project_name'] == None:
		#	string = "project_name  = " = "'" + 'my_project' + "'\n"
			
		#else:
		
		string = "project_name  = " + "'" + self.settings['project_name']+ "'\n"
		text.append(string)
		
		if self.settings['force_field'] == None:
			string = "force_field   = " + "None\n"
			text.append(string)
		else:	
			string = "force_field   = " + "'" + self.settings['force_field']+ "'\n"
			text.append(string)
		
		if self.settings['parameters'] == None:
			string = "parameters    = " + "None\n"
			text.append(string)	
		else:
			string = "parameters    = " + "'" + self.settings['parameters']+ "'\n"
			text.append(string)	

		if self.settings['topology']   == None:
			string = "topology      = " + "None\n"
			text.append(string)	
		else:
			string = "topology      = " + "'" + self.settings['topology']+ "'\n"
			text.append(string)	
		
		if self.settings['coordinates']   == None:
			XYZFile_FromSystem(full_name + ".xyz" ,self.system)	
			string =     "coordinates   = " + "'" + full_name + ".xyz" + "'\n"
			text.append(string)
		else:
			string = "coordinates   = " + "'" + self.settings['coordinates']+ "'\n"
			text.append(string)	
				
		string = "nbModel_type  = " + "'" + self.settings['nbModel_type']+ "'\n"
		text.append(string)	
		
		if self.settings['nbModel_type'] == 'NBModelFull':
			string = "ABFS_options  = None\n"
			text.append(string)
		else:
			string = "ABFS_options  = " + "{ 'innerCutoff'" + ':' +  str(8.0) +", 'outerCutoff' :" + str(12.0) + ", 'listCutoff'  :" + str(13.5) +  "}" + "\n\n"
			text.append(string)
		
		
		prune_table = self.settings['prune_table']
		string      = write_table_in_text3(prune_table,   "prune_table")
		text.append(string)
				
			
		fix_table = self.settings['fix_table']
		string      = write_table_in_text(fix_table,   "fix_table  ")
		text.append(string)		                        
		
		qc_table = self.settings['qc_table']
		string      = write_table_in_text(qc_table, "qc_table   ")
		text.append(string)                          
	
	
			
		string = "QCMM          = " + "'" + self.settings['QCMM']+ "'\n\n"
		text.append(string)
		
		# QC_METHOD 
		
		if self.settings['qc_method']   == None:
			string  = "qc_method     = " + "None\n"
			text.append(string)
			string  = "charge        = " + "None\n"
			text.append(string)
			string  = "multiplicity  = " + "None\n"
			text.append(string)
		else:
			string = "charge        = " + str(self.settings['charge']) + "\n"
			text.append(string)
			string = "multiplicity  = " + str(self.settings['multiplicity'])+ "\n"
			text.append(string)
			string = "qc_method     = " + "'" +(self.settings['qc_method'])+ "'\n"
			text.append(string)
		
		
		# DFT - pDynamo 
		
		string =     "\n#   DFT - pDynamo - only \n\n"
		text.append(string)		
		string = "density_tol   = " + str(self.settings['density_tol']) + "\n"
		text.append(string)
		string = "Maximum_SCF   = " + str(self.settings['Maximum_SCF'])+ "\n"		
		text.append(string)

		#ORCA parameters 

		string =     "\n#   ORCA parameters \n\n"
		text.append(string)		
		
		qc_method = self.settings['qc_method']
		if qc_method == "ORCA - ab initio":
			string = "ORCA_method   = " + "'" + self.settings['ORCA_method']+ "'\n"
			text.append(string)
			string = "ORCA_SCF      = " + "'" + self.settings['ORCA_SCF']+ "'\n"
			text.append(string)
			string = "ORCA_basis    = " + "'" + self.settings['ORCA_basis']+ "'\n"
			text.append(string)
			string = "ORCA_pal      = " + str(self.settings['ORCA_pal'])+ "\n"
			text.append(string)
		else:
			string = "ORCA_method   = " + "None\n"
			text.append(string)
			string = "ORCA_SCF      = " + "None\n"
			text.append(string)
			string = "ORCA_basis    = " + "None\n"
			text.append(string)
			string = "ORCA_pal      = " + "None\n"
			text.append(string)			
			

		#GTKDynamo parameters


		string =     "\n#   GTKDynamo parameters \n\n"
		text.append(string)
				
		string =     "last_step     = " + str(self.step)+ "\n"
		text.append(string)		
		if self.settings['data_path'] == None: 
			string =     "data_path     = None\n"
			text.append(string)
		else:
			string =     "data_path     = " + "'" + self.settings['data_path']+ "'\n"
			text.append(string)		
		
		
		XYZFile_FromSystem(full_name + ".xyz" ,self.system)	
		string =     "last_frame    = " + "'" + full_name + ".xyz" + "'\n"
		text.append(string)
			
		cmd.save(full_name + ".pse")
		string =     "pymol_session = " + "'" + full_name + ".pse" + "'\n"
		text.append(string)
		
		arq.writelines(text)
		arq.close()		
	"""	 
	
	"""
	def save_config (self, data_path):
		print	data_path,  " --->   passo 1"
		
		os.system("rm .config.dynamo")
		filein = open("config.dynamo", 'w')
		
		print filein
		
		text=""
		text +="project_folder = "
		text += data_path + "\n"
		
		print text
		
		filein.write(text)
		filein.close()
		
		print "The file: config.dynamo, has been updeted"
		print "the new datapath folder is: ", text
	"""
			#=================================#
			#             P Y M O L           #
			#=================================#

"""
class pymol_class:
	def __init__ (self):
		
		self.pymol_config = {
							'sphere_scale'         : "0.25",
							'stick_radius'         : "0.15",
							'label_distance_digits': 4
							}
							
		cmd.set ('sphere_scale'     , 0.25)
		cmd.set ('stick_radius'     , 0.15)
		cmd.set ('label_distance_digits',4)
"""
	
def pymol_get_table         (selection):                        # Pymol  ---table---> GTKDynamo
	'''	
	# antiga - pymol_get_table
	# extrai um selecao do pymol na forma de tabela
	'''
		
	model    = cmd.get_model(selection)
	table    = []
	n = 1 
	for atom in model.atom:
		ids   = atom.index
		py_id = int(ids) -1
		table.append(py_id)
		ids   = str(ids)
		n = n+1
	print  table
	return table

def pymol_put_table         (table, selection):                 # pDynamo ---table---> Pymol
	'''
	# antiga - pymol_put_table        
	# adiciona uma selecao no pymol a partir de uma tabela do dynamo
	# obs: existe no dynamo o vetor comeca no intem 0        
	'''	
	selection_string = selection +", index "			        # selection that will be generated in the pymol
	n = 0												        #
	n_limit = 0									    	        #
	limit = len(table)        
											        
	for i in table:                                             #
		selection_string = selection_string + "+" + str(i +1)	#
		n = n + 1												#
		n_limit = n_limit + 1									#
		if n == 100:											#
			cmd.select(selection, selection_string)				# generates the pymol selection
			n = 0 												#
			selection_string = selection + ", index "			#
																#	
		if n_limit == limit:									#
			cmd.select(selection, selection_string)
			n = 0 
			selection_string = selection + ", index "		


def pymol_export_PDB_to_file(obj, data_path, file_out, state = -1):
	tmp         = data_path+"/tmp"                          
	if not os.path.exists ( tmp ): os.mkdir ( tmp )         
	file_path   = os.path.join (tmp, file_out)
	
	
	FILE        = file_path 
	#  cmd.save("/home/fernando/Desktop/gordo.pdb", "obj01", -1, "pdb")
	cmd.save(FILE, obj, state, "pdb")
	return FILE
	
	
def pymol_export_XYZ_to_file(obj, label, data_path, file_out, state): #export pymol coordinates to a XYZ file
	'''	
	# antiga      -  pymol_export_XYZ_file
	# obj,       -  pymol object
	# label,     -  second line in the XYZ file "header"
	# data_path, -  working folder
	# file_out   -  file out name
	'''	
	tmp         = data_path+"/tmp"                          
	if not os.path.exists ( tmp ): os.mkdir ( tmp )         

	text        = []                                        # buffer -  list of strings  									
	file_path   = os.path.join (tmp, file_out)              # fullpath 
	arq         = open(file_path, 'w')	
	s           = " "

	pymol_obj   = cmd.get_model(obj, state)                 # importing pymol selection
	model_split = pymol_obj.atom	

	for i in model_split:
		line = [] 		
		idx = i.name			                                          
		X = i.coord[0]			                                          
		Y = i.coord[1]			                                          
		Z = i.coord[2]			                                          
		line = idx +"     " + str(X)+ "     "+ str(Y)+ "     " + str(Z)   
		text.append(line + "\n")										  
	
	header = len(text)							
	arq.writelines(str(header) + "\n")			
	#print header								#
	header2 = label             				
	arq.writelines(header2+ "\n")
	#print header2
	#for i in text:								
	#	print i									#	
	arq.writelines(text)	
	arq.close()				
	
	return file_path

def get_pymol_id_from_file (filename):
	file_split = filename.split('.')
	file_id    = (file_split[0]).split('/')
	return file_id[-1]

def take_pymol_selection(pymol_selection):      
	sele_table = []
	model = cmd.get_model(pymol_selection)		# importing selection
	n = 1 										#	
	for a in model.atom:						#	building table sele_table
		index = a.index                         #   selection index
		name  = a.name							
		sele_table.append(index)

	print "\n\n"
	print "sele table",sele_table							
	return sele_table


