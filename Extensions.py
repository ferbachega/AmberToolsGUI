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
from pymol import *

# OTHER TOOLS (amber tools  and pdbtools)
def MERGE_OBJ_IN_PYMOL(data_path, obj1, obj2, obj3):
	text = []
	
	tmp = data_path+"/tmp"
	if not os.path.exists ( tmp ): os.mkdir ( tmp ) 
	
	cmd.save(tmp+"/tmp_obj01.pdb", obj1, 1, "pdb")
	cmd.save(tmp+"/tmp_obj02.pdb", obj2, 1, "pdb")
	
	
	file_in = open(tmp+"/tmp_obj01.pdb", 'r')   # open the first object (OBJ1)
	
	for line in file_in:
		print line
		line2=line.split()
		if line2[0] == "HETATM":                # select lines that start with HETATM
			text.append(line)                   # save lines
		elif line2[0] == "ATOM":                # select lines that start with ATOM
			text.append(line)	                # save lines
			
			 
	file_in = open(tmp+"/tmp_obj02.pdb", 'r')   # open the second object (OBJ2)
	for line in file_in:
		print line
		line2=line.split()
		if line2[0] == "HETATM":
			text.append(line)
		elif line2[0] == "ATOM":
			text.append(line)	
	
	arq = open(tmp+"/"+obj3+".pdb", 'w')        # open the third object (OBJ3), and save objects OBJ1 and OBJ2 in the OBJ3
	arq.writelines(text)
	arq.close()
	 
	os.remove(tmp+"/tmp_obj01.pdb")	        	# removing intermediate files
	os.remove(tmp+"/tmp_obj02.pdb")	        	#
	
	cmd.load(tmp+"/"+obj3+".pdb")               # call chama obj3 no pymol
	
def TLEAP_modify_importResidueInformation():
	model = cmd.get_model("pk1")
	index = []
	resn = None
	resi = None 
	for a in model.atom:
		resn = a.resn
		resi = a.resi
	return resn, resi





def GMX_top_modify (filein, fileout, reductor ):
	arq =  open(filein, "r")
	text = [] 
	for line in arq:
		line2 = line.split()
		
		if len(line2) == 2:
			if line2[0] == "SOL" :                   
				number = int(line2[1])
				number =  number - (reductor)
				line = line2[0] + "      " + str(number)
				text.append(line)
		else:
			text.append(line)
	
	arq.close()
	
	arq2 = open(fileout, 'w')
	arq2.writelines(text)
	arq2.close()	
		
	""" Function doc """
	


#============================#
#                            #
#       A  M  B  E  R        #
#                            #
#============================#
	
class AmberProject:
	def __init__ (self):
		#==================#
		#    T L E A P     #
		#==================#    
		self.gaff_list             = []
		self.text_tleap_modify     = []	
		self.text_tleap_links      = []  # text list  - linked atoms
		self.tleap_modify_resn     = []
		self.tleap_modify_resi     = []
		self.tleap_modify_resn_new = []
		self.tleap_link_atoms      = []  # list linked atoms  ex: SS bonds. 
		
		#=========================#
		#  A N T E C H A M B E R  #
		#=========================#  		
		self.ligand_name       = None
		self.new_ligand_name_full  = None
		
		self.atomtype = {
						'C'    :[
								['C','c','Sp2 C carbonyl group'],
								['C','c1','Sp C'],
								['C','c2','Sp2 C'],
								['C','c3','Sp3 C'],
								['C','ca','Sp2 C in pure aromatic systems'],
								['C','cp','Head Sp2 C that connect two rings in biphenyl sys'], 
								['C','cq','Head Sp2 C that connect two rings in biphenyl sys. identical to cp'],
								['C','cc','Sp2 carbons in non-pure aromatic systems'],
								['C','cd','Sp2 carbons in non-pure aromatic systems, identical to cc'],
								['C','ce','Inner Sp2 carbons in conjugated systems'],
								['C','cf','Inner Sp2 carbons in conjugated systems, identical to ce'],
								['C','cg','Inner Sp carbons in conjugated systems'],
								['C','ch','Inner Sp carbons in conjugated systems, identical to cg'],
								['C','cx','Sp3 carbons in triangle systems'],
								['C','cy','Sp3 carbons in square systems'],
								['C','cu','Sp2 carbons in triangle systems'],
								['C','cv','Sp2 carbons in square systems'],
								['C','cz','Sp2 carbon in guanidine group']
								],
								
						'H'   : [
								['H','h1','H bonded to aliphatic carbon with 1 electrwd. group'], 
								['H','h2','H bonded to aliphatic carbon with 2 electrwd. group'],  
								['H','h3','H bonded to aliphatic carbon with 3 electrwd. group'],  
								['H','h4','H bonded to non-sp3 carbon with 1 electrwd. group'],  
								['H','h5','H bonded to non-sp3 carbon with 2 electrwd. group'],  
								['H','ha','H bonded to aromatic carbon'],
								['H','hc','H bonded to aliphatic carbon without electrwd. group'], 
								['H','hn','H bonded to nitrogen atoms'], 
								['H','ho','Hydroxyl group'],  
								['H','hp','H bonded to phosphate'],
								['H','hs','Hydrogen bonded to sulphur'],
								['H','hw','Hydrogen in water'],  
								['H','hx','H bonded to C next to positively charged group'],
								],

						'F'   : [
								['F','f','Fluorine'], 
								],
								
						'CL'  : [
								['CL','cl','Chlorine'], 
								],

						'BR'  : [        
								['BR','br','Bromine'], 
								],
								
						'I'   : [    
								['I','i','Iodine'], 
								],
								
						'N'   : [       
								['N','n','Sp2 nitrogen in amide groups'],
								['N','n1','Sp N'],
								['N','n2','aliphatic Sp2 N with two connected atoms'], 
								['N','n3','Sp3 N with three connected atoms'], 
								['N','n4','Sp3 N with four connected atoms'], 
								['N','na','Sp2 N with three connected atoms'], 
								['N','nb','Sp2 N in pure aromatic systems'],
								['N','nc','Sp2 N in non-pure aromatic systems'], 
								['N','nd','Sp2 N in non-pure aromatic systems, identical to nc'],
								['N','ne','Inner Sp2 N in conjugated systems'], 
								['N','nf','Inner Sp2 N in conjugated systems, identical to ne'],
								['N','nh','Amine N connected one or more aromatic rings'],
								['N','no','Nitro N'],
								],


						'O'	  : [
								['O','o','Oxygen with one connected atom'], 
								['O','oh','Oxygen in hydroxyl group'], 
								['O','os','Ether and ester oxygen'], 
								['O','ow','Oxygen in water'], 
								],
								
						'P'   : [
								['P','p2','Phosphate with two connected atoms'],
								['P','p3','Phosphate with three connected atoms, such as PH3'], 
								['P','p4','Phosphate with three connected atoms, such as O=P(CH3)2'], 
								['P','p5','Phosphate with four connected atoms, such as O=P(OH)3'], 
								['P','pb','Sp2 P in pure aromatic systems'],
								['P','pc','Sp2 P in non-pure aromatic systems'], 
								['P','pd','Sp2 P in non-pure aromatic systems, identical to pc'], 
								['P','pe','Inner Sp2 P in conjugated systems'], 
								['P','pf','Inner Sp2 P in conjugated systems, identical to pe'], 
								['P','px','Special p4 in conjugated systems'], 
								['P','py','Special p5 in conjugated systems'], 
								],
								
						'S'   : [
								['S','s','S with one connected atom'],
								['S','s2','S with two connected atom, involved at least one double bond'],
								['S','s4','S with three connected atoms'],
								['S','s6','S with four connected atoms'], 
								['S','sh','Sp3 S connected with hydrogen'],
								['S','ss','Sp3 S in thio-ester and thio-ether'], 
								['S','sx','Special s4 in conjugated systems'], 
								['S','sy','Special s6 in conjugated systems']
								]
								}

	#==================#
	#    T L E A P     #
	#==================#


	def TLEAP_export_pdb_from_pymol(self, data_path, pymol_obj):
		tmp_path = data_path + '/tmp'

		if not os.path.exists( tmp_path ): 
			os.mkdir(tmp_path)
			
		cmd.save(tmp_path+"/file_teste.pdb", pymol_obj, 1, "pdb")				#	file that will be exportd with pymol
																		        #	filein = "/home/fernando/Documents/GTK_Dynamo/GTK_Dynamo0.0.2.16_GTK2.18/1bx4.pdb"
																				
		arq =  open(tmp_path+"/file_teste.pdb","r")								

			
		text  = []					     		# variable where the PDB file will be rewritten	
												#
												#
												#                  HETATM 1884  O   HOH A 372      21.952   9.654  -3.812  1.00 50.58           O
		for line in arq:						#	exemplo, line: ATOM  85830  CLA CLA I 154    -106.883-110.916-110.774  1.00  0.00      ION CL
			line2 = line.split()				#   	                             		'    '									'          line[76:78]
			line1 = line[0:6]					#												  li[30:38]
			#if line2[0] == "CRYST1":			#														  li[38:46]									
			#	print line2[0:-1]				#																  li[46:54]
			#	print line
			if line1 == "ATOM  ":				# 	line1  is the variable that presents the string "ATOM  " or "HETATM"
				index   = line[6:11]			#	indice
				A_name  = line[11:16]			#	atom name     ex" CA "
				resn    = line[16:20] 			#	residue name   ex" LYS"
				chain   = line[20:22]			#   chain    ex " A"
				resi    = line[22:26]			#   residue number
				gap     = line[26:30]			#	gap between residue number and coordinates
				x       = line[30:38]			#	coordinate X
				y       = line[38:46]			#	coordinate Y
				z       = line[46:54]			#	coordinate Z
												#
				b       = line[54:60]			#	B-factor
				oc      = line[60:66]			#	Occupancy
				gap2    = line[66:76]			#	gap between Occupancy and atomic type'    '
				atom    = line[76:78] 			# 	atomic type


				resi2 = resi.split()
				resi2 = resi2[0]			
				
				A_name2 = A_name.split()		#	split variable A_name
				A_name2 = A_name2[0]			#	tranforms into a string
				
				resn2 = resn.split()
				resn2 = resn2[0]



				n = 0   #	open counter
				if 	self.tleap_modify_resi != []:
					for i in self.tleap_modify_resi:							#	check if the residue is compatible with the 
						i = int(i)										        #	modified residues list
						if int(resi2) == i:								        #	if =:
							if resn2 == self.tleap_modify_resn[n]:			    #				if the residue name is =:
								resn = (" "+self.tleap_modify_resn_new[n])	    #											entao o nome do residuo eh alterado
								#print resn 							        #	
						n = n+1											        


				
				# Cloreto
				if A_name2 == "CL":		#modify the atom name
					A_name = " Cl- "	#
					
				if resn2   == "CL":		#modify the residue name
					resn   = " Cl-"		#
				
				#sodio	
				if A_name2 == "NA":
					A_name = " Na+ "
					
				if resn2   == "NA":
					resn   = " Na+"
				
				#Magnesio
				if A_name2 == "MG":
					A_name = " MG2 "
					
				if resn2   == "MG":
					resn   = " MG2"			
				
				#print "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				string = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				text.append(string+'\n' )
				
			if line1 == "HETATM":				# 	line1  is the variable that presents the string "ATOM  " ou "HETATM"
				index   = line[6:11]			#	Same process  (take a lot of variables of the PDB files)
				A_name  = line[11:16]			#
				resn    = line[16:20] 			#
				chain   = line[20:22]
				resi    = line[22:26]
				gap     = line[26:30]
				x       = line[30:38]
				y       = line[38:46]
				z       = line[46:54]
				
				b       = line[54:60]		
				oc      = line[60:66]
				gap2    = line[66:76]
				atom    = line[76:78] 			# '    '
				
				
				resi2 = resi.split()
				resi2 = resi2[0]			
				
				A_name2 = A_name.split()		  
				A_name2 = A_name2[0]			
				
				resn2 = resn.split()			#	split variable rens2   
				resn2 = resn2[0]				#	transforms in " ALA" >  "ALA"   


				n = 0												    
				for i in self.tleap_modify_resi:					     
					i = int(i)										    
					if int(resi2) == i:								    
						if resn2 == self.tleap_modify_resn[n]:			
							resn = (" "+self.tleap_modify_resn_new[n])	
							#print resn 							    	
					n = n+1											    

				
				# Cloreto
				if A_name2 == "CL":		
					A_name = " Cl- "	
					
				if resn2   == "CL":		
					resn   = " Cl-"		
				
				#sodio	
				if A_name2 == "NA":
					A_name = " Na+ "
					
				if resn2   == "NA":
					resn   = " Na+"
				
				#Magnesio
				#if A_name2 == "MG":
				#	A_name = " MG2 "
					
				if resn2   == "MG":
					resn   = " MG2"			
						
				#print "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				string = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				text.append(string+'\n')
				#print string
				
			if line1 == "TER   ":
				text.append(line + "\n")
				
		arq2 = open(tmp_path+"/file_teste.pdb", 'w')
		arq2.writelines(text)
		arq2.close()	
		return tmp_path+"/file_teste.pdb"
		
	def TLEAP_add_mol2_or_frcmod_to_gaff_list(self, filein):
		self.gaff_list.append(filein)													
		return self.gaff_list

	def TLEAP_clear_gaff_list(self):
		self.gaff_list=[]
		print "gaff_list =  empty"
		return self.gaff_list

	def TLEAP_make_script(self,
						pdb_file	,		# pdb  including modifications   str	
						system_name,        # system name (file out)         str  
						data_path,          # data path                      str
						ff_model,           # ff model - ff99SB              str
						ff_model_gly,       # glycan type  ex glycam 06      str
						ff_model_gaff,      # include gaff?               True/False
						water_model,        # water - TIP3P                  str
						water_box,          # include waterbox ?          True/False
						add_ions,           # include ions?               True/False
						neutralize,         # neutralize total charge ?   True/False
						positive_type,      # add ions Ex Na+                str
						negative_type,		# add ions Ex Cl-                str
						positive_num,       # number of positive ions        int
						negative_num):        
		text=[]
		# ff_model
		text.append("source leaprc."+ff_model+"\n")
		print "source leaprc."+ff_model+"\n"
		
		
		# ff_model_gly
		if ff_model_gly != None:
			print "source leaprc."+ff_model_gly+"\n"
		
		# ff_model_gaff
		if ff_model_gaff == True:
			text.append("source leaprc.gaff\n")
			for i in self.gaff_list:
				print i 
				file_in = i
				file_in2 = i.split("/")
				file_in2 = file_in2[-1]
				file_in2 = file_in2.split(".")
				print "residue name: ", file_in2[-2]
				print "file type: ", file_in2[-1]
				file_type =file_in2[-1]
				
				if file_type == "mol2":
					text.append(file_in2[-2]+" = loadmol2 "+file_in+"\n")
				if file_type  == "frcmod":
					text.append("loadamberparams "+file_in+"\n")
				if file_type  == "prep":
					text.append("loadamberprep "+file_in+"\n")
	
		
		text.append("system = loadpdb " + pdb_file +"\n")
		#text.append("system = loadpdb "+dataPath+"/file_teste.pdb\n")
		
		for link in self.tleap_link_atoms:
			text.append(link + "\n")
		
		
		#water_model = App.get_object('cbox_tleap_solvate_water_model').get_active_text()
		
		if water_model != None:
			text.append("solvatebox system " + water_model +"BOX " + water_box + "\n")
		
		if add_ions == True:	
			if neutralize == True:
				text.append("addions system Cl- 0\n")
				text.append("addions system Na+ 0\n")
			else:
				#print "use 'just neutralize charges' "
				text.append("addions system " + negative_type + " " + negative_num + " \n")
				text.append("addions system " + positive_type + " " + positive_num + " \n")


				#positive_type = add ions Ex Na+                str
				#negative_type = add ions Ex Cl-                str
				#positive_num  = number of positive ions        int
				#negative_num): 
		
		text.append("saveamberparm system " +data_path+"/"+system_name+".top " +data_path+"/"+system_name+".crd \n")
		
		text.append("quit \n")
		arq = open(data_path+"/leaprc", 'w')
		arq.writelines(text)
		arq.close()
	
	def TLEAP_modify_addChangesToList(self, data_path,resi_number,resn_wild, resn_mutant):
		AMBERTOOLS_outputs = data_path+"/AMBERTOOLS_outputs"
		if not os.path.exists ( AMBERTOOLS_outputs ): os.mkdir ( AMBERTOOLS_outputs )
		
		
		self.text_tleap_modify.append(resi_number+"   "+resn_wild+"  >  "+ resn_mutant+ "\n")
		

		self.tleap_modify_resi.append(resi_number)
		self.tleap_modify_resn.append(resn_wild)
		self.tleap_modify_resn_new.append(resn_mutant)

		return self.text_tleap_modify


	def TLEAP_modify_DeleteLastItemFromList(self):
		try: 
			self.tleap_modify_resi.pop(-1)
			self.tleap_modify_resn.pop(-1)
			self.tleap_modify_resn_new.pop(-1)
			self.text_tleap_modify.pop(-1)
			return self.text_tleap_modify
		except:
			return False

	def TLEAP_modify_CLEAN_LIST(self):
		self.text_tleap_modify     = []	
		self.tleap_modify_resn     = []
		self.tleap_modify_resi     = []
		self.tleap_modify_resn_new = []
		return self.text_tleap_modify
		
		
		
		
		
	def TLEAP_modify_addLinksToList(self, atom1, atom2):
		#AMBERTOOLS_outputs = data_path+"/AMBERTOOLS_outputs"
		#if not os.path.exists ( AMBERTOOLS_outputs ): os.mkdir ( AMBERTOOLS_outputs )
		
		#bond system.30.SG system.51.SG
		
		bond = "bond system."+atom1+".SG system."+atom2+".SG"
		
		self.tleap_link_atoms.append(bond)
		self.text_tleap_links.append(atom1 + "   link  "+ atom2 + "\n")
		
		return self.text_tleap_links





	def TLEAP_modify_DeleteLastItemFromLinkList(self):
		try:
			self.tleap_link_atoms.pop(-1)
			self.text_tleap_links.pop(-1)
			return self.text_tleap_links
		except:
			return False


	def TLEAP_modify_CLEAN_LINK_LIST(self):
		self.tleap_link_atoms      = []	
		self.text_tleap_links      = []

		return self.text_tleap_links







	def TLEAP_amber12_to_amber11_topology_converter (self, filein, fileout, data_path):
		filein = open(data_path+"/"+filein, 'r')
		text   = []
		print_line = True

		for line in filein:
			line2 = line.split()
			try:
				if line2[0] == '%FLAG':
					if   line2[1] == 'ATOMIC_NUMBER':
						print 'excluding flag:', line
						print_line = False

					elif   line2[1] == 'SCEE_SCALE_FACTOR':
						print 'excluding flag:', line
						print_line = False

					elif   line2[1] == "SCNB_SCALE_FACTOR":
						print 'excluding flag:', line
						print_line = False			

					elif   line2[1] == 'IPOL':
						print 'excluding flag:', line
						print_line = False
			
					else:
						print_line = True	
						#print print_line
			except:
				a= None
			if print_line == True:
				text.append(line)

		fileout = open(data_path+"/"+fileout, 'w')
		fileout.writelines(text)
		fileout.close()
		
		""" Function doc """
		
	#=============================#
	#    A N T E C H A M B E R    #
	#=============================#
				
	def ANTECHAMBER_generate_ligand(self, new_ligand_name, data_path, obj_in, add_H, change_resn_ID):
		AMBERTOOLS_outputs = data_path+"/AMBERTOOLS_outputs"
		if not os.path.exists ( AMBERTOOLS_outputs ): os.mkdir ( AMBERTOOLS_outputs )
		
		if  add_H == True:
			cmd.h_add(obj_in)
		
		cmd.save(AMBERTOOLS_outputs+"/lig.pdb", obj_in, 1, "pdb")
		
		file_in = open(AMBERTOOLS_outputs+"/lig.pdb", 'r')
		text = []
		
		#new_ligand_name = App.get_object('entry2_antechamber_new_name').get_text()
		if change_resn_ID == True:
			file_in = open(AMBERTOOLS_outputs+"/lig.pdb", 'r')		                 	# read the PDB tmp file = lig.pdb change or add the residue name
																						# add the residue into a chain X
			for line in file_in:														#
				line2 =  line.split()													#
				if len(line2) == 12:													#
					if line2[0] == "ATOM":												#
						line2[3] = new_ligand_name
						print   'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s'% (int(line2[1]),line2[2],line2[3],line2[4],line2[5],float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),float(line2[10]),line2[11])
						linha = 'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s\n'% (int(line2[1]),line2[2],line2[3],line2[4],line2[5],float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),float(line2[10]),line2[11])
						text.append(linha)
					if line2[0] == "HETATM":
						line2[3] = new_ligand_name
						print   'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s'% (int(line2[1]),line2[2],line2[3],line2[4],line2[5],float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),float(line2[10]),line2[11])
						linha = 'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s\n'% (int(line2[1]),line2[2],line2[3],line2[4],line2[5],float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),float(line2[10]),line2[11])
						text.append(linha)
				if len(line2) == 11:
					if line2[0] == "ATOM":
						line2[3] = new_ligand_name
						chain = "X"
						print   'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s'% (int(line2[1]),line2[2],line2[3],chain,line2[4],float(line2[5]),float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),(line2[10]))
						linha = 'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s\n'% (int(line2[1]),line2[2],line2[3],chain,line2[4],float(line2[5]),float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),(line2[10]))
						text.append(linha)
					if line2[0] == "HETATM":
						line2[3] = new_ligand_name
						chain = "X"
						print   'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s'% (int(line2[1]),line2[2],line2[3],chain,line2[4],float(line2[5]),float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),(line2[10]))
						linha = 'ATOM  %5i%5s %3s %s %3s    %8.3f%8.3f%8.3f  %4.2f %5.2f          %2s\n'% (int(line2[1]),line2[2],line2[3],chain,line2[4],float(line2[5]),float(line2[6]),float(line2[7]),float(line2[8]),float(line2[9]),(line2[10]))
						text.append(linha)		
						
			arq2 = open(AMBERTOOLS_outputs+"/"+new_ligand_name+".pdb", 'w')
			arq2.writelines(text)
			arq2.close()	
		else:									#				
			#text=[]							#				
			for line in file_in:				# When the ligand name is not specified by the user,
				print line						#will be used the original name exported by the pymol
				line2=line.split()				#
				if line2[0] == "HETATM":
					new_ligand_name = line2[3]
					#print line2[3]
					text.append(line)
				elif line2[0] == "ATOM":
					new_ligand_name = line2[3]
					#print line2[3]
					text.append(line)
			print "\n\nyour ligand name is: ",new_ligand_name
			arq = open(AMBERTOOLS_outputs+"/"+new_ligand_name+".pdb", 'w')
			arq.writelines(text)
			arq.close()	
			
		self.ligand_name =  new_ligand_name
		return  new_ligand_name


	def ANTECHAMBER_run_antechamber(self, data_path, charge, multiplicity, charge_model, charge_FLAG, pymol_FLAG, param_FLAG):
		new_ligand_name = self.ligand_name
		print new_ligand_name
		
		AMBERTOOLS_outputs = data_path+"/AMBERTOOLS_outputs"
		if not os.path.exists ( AMBERTOOLS_outputs ): os.mkdir ( AMBERTOOLS_outputs )

		try:
			os.rename(AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2",AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2.backup")
		except:
			a = None
			
			
		if charge_model == "AM1-BCC":
			charge_method =  "bcc"
			
		else:											#running antechamber
			return "only AM1-BCC is avaliable"			#
		
		print "Charge model: ",charge_model
		print "Charge:       ",charge
		print "Multiplicity: ",multiplicity
		
		os.system("antechamber -i "+AMBERTOOLS_outputs+"/"+new_ligand_name+".pdb -fi pdb -o "+AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2 "+" -fo mol2  -c "+ charge_method + " -nc "+str(charge)+" -m "+ str(multiplicity))
		print "done"							
				
		try:
			os.rename("ANTECHAMBER_AC.AC0", AMBERTOOLS_outputs+ "/ANTECHAMBER_AC.AC0")
		except:
			a = None
		try:
			os.rename("ANTECHAMBER_AM1BCC.AC", AMBERTOOLS_outputs+ "/ANTECHAMBER_AM1BCC.AC")
		except:
			a = None
		try:
			os.rename("ANTECHAMBER_AC.AC", AMBERTOOLS_outputs+ "/ANTECHAMBER_AC.AC")
		except:
			a = None
		try:
			os.rename("ANTECHAMBER_AM1BCC_PRE.AC", AMBERTOOLS_outputs+ "/ANTECHAMBER_AM1BCC_PRE.AC")
		except:
			a = None
		try:
			os.rename("ANTECHAMBER_BOND_TYPE.AC", AMBERTOOLS_outputs+ "/ANTECHAMBER_BOND_TYPE.AC")
		except:
			a = None
		try:
			os.rename("ANTECHAMBER_BOND_TYPE.AC0", AMBERTOOLS_outputs+ "/ANTECHAMBER_BOND_TYPE.AC0")
		except:
			a = None
		try:
			os.rename("ATOMTYPE.INF", AMBERTOOLS_outputs+ "/ATOMTYPE.INF")
		except:
			a = None
		try:
			os.rename("sqm.in", AMBERTOOLS_outputs+ "/sqm.in")
		except:
			a = None
		try:
			os.rename("sqm.out", AMBERTOOLS_outputs+ "/sqm.out")
		except:
			a = None

		try:
			if charge_FLAG == True:
				file_in =  open(AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2", 'r')
				texto         =  []
				charge_table  =  []
				atomname      =  []
				index         =  []
				atomtype      =  []
				
				for line in file_in:							#
					#print line									#
					line2=line.split()							# identify the MOL2 file lines that presents the charge and atomic types
					if len(line2) == 9:							#
						float_check = line2[-1].split(".")		#
						if len(float_check)== 2:
							print line
							charge_table.append(line2[-1])
							index.append(line2[0])
							atomname.append(line2[1])
							atomtype.append(line2[5])
							#charge_table.append(line2[-1])
				n = 0			
				for i in index:
					print i,atomtype[n],charge_table[n]
					n = n+1
					
				total_charge = float(charge)						    
				for i in charge_table:									# the total charge of the system is checked
					total_charge - float(i)							
				print "\n\nThe total charge_table is: ", total_charge	

				
				if pymol_FLAG == True: 	#
					try:
						cmd.delete(new_ligand_name)
					except:
						a =None
					
					cmd.load(AMBERTOOLS_outputs+"/"+new_ligand_name+".pdb")					
					
					string = "label "+new_ligand_name+",index,name"							
					cmd.do(string)															
					string = "show sticks, "+new_ligand_name
					cmd.do(string)															
					cmd.disable("all")
					cmd.enable(new_ligand_name)
					#string = "show spheres,"+new_ligand_name
					#cmd.do(string)															

					#for line in file_in:													
					#	line
				if param_FLAG == True:
					self.ANTECHAMBER_run_parmchk(data_path)

			return index,atomname,atomtype,charge_table
		except:
			file_out = open(AMBERTOOLS_outputs+ "/sqm.out")
			for i in file_out:
				print i 
			return None

	def ANTECHAMBER_edit_mol2_file(self, data_path, new_index, new_atomname, new_atomtype, new_charge_table):
		new_ligand_name = self.ligand_name
		print new_ligand_name
		
		AMBERTOOLS_outputs = data_path+"/AMBERTOOLS_outputs"
		if not os.path.exists ( AMBERTOOLS_outputs ): os.mkdir ( AMBERTOOLS_outputs )
		
		text      = []
				
		print new_index, new_atomname, new_atomtype, new_charge_table
		
		
		index     = []
		atomname  = []
		x         = []
		y         = []
		z         = []
		atomtype  = []					
		resi      = []
		resn      = []
		charge    = []
		
		
		file_in =  open(AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2", 'r')
		
		n = 0
		
		for line in file_in:							
			line2=line.split()							
			if len(line2) == 9:	
				float_check = line2[-1].split(".")		
				if len(float_check)== 2:
					print index
					index.append(line2[0])
					atomname.append(line2[1])
					x.append(line2[2])
					y.append(line2[3])
					z.append(line2[4])
					atomtype.append(line2[5])					
					resi.append(line2[6])
					resn.append(line2[7])
					charge.append(line2[8])
					#print "%7s%4s%15s%10s%10s%3s%9s%4s%14s" %('1', 'CL1', '26.7460', '104.7550', '31.1500', 'cl', '600', 'DCE', '-0.181400')
					
					X        = line2[2]
					Y        = line2[3]
					Z        = line2[4]
					RESI     = line2[6]
					RESN     = line2[7]
					
					string = "%7s%4s%15s%10s%10s%3s%9s%4s%14s\n" % (new_index[n], new_atomname[n],X,Y,Z, new_atomtype[n],RESI,RESN,new_charge_table[n])
					text.append(string)

					n = n +1
				else:
					text.append(line)
			else:
				text.append(line)

		file_in =  open(AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2", 'w')
		file_in.writelines(text)
		file_in.close()

	def ANTECHAMBER_run_parmchk(self, data_path ):
		new_ligand_name = self.ligand_name
		
		AMBERTOOLS_outputs = data_path+"/AMBERTOOLS_outputs"
		if not os.path.exists ( AMBERTOOLS_outputs ): os.mkdir ( AMBERTOOLS_outputs )
			
		print "now runing parmchk\n"
		os.system("parmchk -i " + AMBERTOOLS_outputs+"/"+new_ligand_name+".mol2 " + " -f mol2 -o "+AMBERTOOLS_outputs+"/"+new_ligand_name+".frcmod")
		file_in = open(AMBERTOOLS_outputs+"/"+new_ligand_name+".frcmod", 'r')

		for line in file_in:
			print line
		print "\n done \n"




#===============================#
#                               #
#      G  R  O  M  A  C  S      #
#                               #
#===============================#



class GromacsProject:
	""" 
	 1: AMBER03 protein, nucleic AMBER94 (Duan et al., J. Comp. Chem. 24, 1999-2012, 2003)
	 2: AMBER94 force field (Cornell et al., JACS 117, 5179-5197, 1995)
	 3: AMBER96 protein, nucleic AMBER94 (Kollman et al., Acc. Chem. Res. 29, 461-469, 1996)
	 4: AMBER99 protein, nucleic AMBER94 (Wang et al., J. Comp. Chem. 21, 1049-1074, 2000)
	 5: AMBER99SB protein, nucleic AMBER94 (Hornak et al., Proteins 65, 712-725, 2006)
	 6: AMBER99SB-ILDN protein, nucleic AMBER94 (Lindorff-Larsen et al., Proteins 78, 1950-58, 2010)
	 7: AMBERGS force field (Garcia & Sanbonmatsu, PNAS 99, 2782-2787, 2002)
	 8: CHARMM27 all-atom force field (with CMAP) - version 2.0
	 9: GROMOS96 43a1 force field
	10: GROMOS96 43a2 force field (improved alkane dihedrals)
	11: GROMOS96 45a3 force field (Schuler JCC 2001 22 1205)
	12: GROMOS96 53a5 force field (JCC 2004 vol 25 pag 1656)
	13: GROMOS96 53a6 force field (JCC 2004 vol 25 pag 1656)
	14: OPLS-AA/L all-atom force field (2001 aminoacid dihedrals)
	15: [DEPRECATED] Encad all-atom force field, using full solvent charges
	16: [DEPRECATED] Encad all-atom force field, using scaled-down vacuum charges
	17: [DEPRECATED] Gromacs force field (see manual)
	18: [DEPRECATED] Gromacs force field with hydrogens for NMR
	"""

	def __init__ (self):
		
		self.pdb_modify      = []	
		self.modify_resn     = []
		self.modify_resi     = []
		self.resn_new        = []
		
		self.gaff_list             = []
		self.text_GMX_modify     = []	
		self.GMX_modify_resn     = []
		self.GMX_modify_resi     = []
		self.GMX_modify_resn_new = []		
		
		mdout = """;
		;	File 'mdout.mdp' was generated
		;	By user: fernando (1000)
		;	On host: Bahamuth
		;	At date: Wed Jan 16 02:00:50 2013
		;

		; VARIOUS PREPROCESSING OPTIONS
		; Preprocessor information: use cpp syntax.
		; e.g.: -I/home/joe/doe -I/home/mary/roe
		include                  = 
		; e.g.: -DPOSRES -DFLEXIBLE (note these variable names are case sensitive)
		define                   = -DFLEXIBLE

		; RUN CONTROL PARAMETERS
		integrator               = steep
		; Start time and timestep in ps
		tinit                    = 0
		dt                       = 0.002
		nsteps                   = 20
		; For exact run continuation or redoing part of a run
		init_step                = 0
		; Part index is updated automatically on checkpointing (keeps files separate)
		simulation_part          = 1
		; mode for center of mass motion removal
		comm-mode                = Linear
		; number of steps for center of mass motion removal
		nstcomm                  = 10
		; group(s) for center of mass motion removal
		comm-grps                = 

		; LANGEVIN DYNAMICS OPTIONS
		; Friction coefficient (amu/ps) and random seed
		bd-fric                  = 0
		ld-seed                  = 1993

		; ENERGY MINIMIZATION OPTIONS
		; Force tolerance and initial step-size
		emtol                    = 1000
		emstep                   = 0.01
		; Max number of iterations in relax_shells
		niter                    = 20
		; Step size (ps^2) for minimization of flexible constraints
		fcstep                   = 0
		; Frequency of steepest descents steps when doing CG
		nstcgsteep               = 1000
		nbfgscorr                = 10

		; TEST PARTICLE INSERTION OPTIONS
		rtpi                     = 0.05

		; OUTPUT CONTROL OPTIONS
		; Output frequency for coords (x), velocities (v) and forces (f)
		nstxout                  = 100
		nstvout                  = 100
		nstfout                  = 0
		; Output frequency for energies to log file and energy file
		nstlog                   = 100
		nstcalcenergy            = -1
		nstenergy                = 100
		; Output frequency and precision for .xtc file
		nstxtcout                = 0
		xtc-precision            = 1000
		; This selects the subset of atoms for the .xtc file. You can
		; select multiple groups. By default all atoms will be written.
		xtc-grps                 = 
		; Selection of energy groups
		energygrps               = 

		; NEIGHBORSEARCHING PARAMETERS
		; nblist update frequency
		nstlist                  = 10
		; ns algorithm (simple or grid)
		ns_type                  = grid
		; Periodic boundary conditions: xyz, no, xy
		pbc                      = xyz
		periodic_molecules       = no
		; nblist cut-off        
		rlist                    = 1.0
		; long-range cut-off for switched potentials
		rlistlong                = -1

		; OPTIONS FOR ELECTROSTATICS AND VDW
		; Method for doing electrostatics
		coulombtype              = PME
		rcoulomb-switch          = 0
		rcoulomb                 = 1.0
		; Relative dielectric constant for the medium and the reaction field
		epsilon_r                = 1
		epsilon_rf               = 1
		; Method for doing Van der Waals
		vdw-type                 = Cut-off
		; cut-off lengths       
		rvdw-switch              = 0
		rvdw                     = 1.4
		; Apply long range dispersion corrections for Energy and Pressure
		DispCorr                 = No
		; Extension of the potential lookup tables beyond the cut-off
		table-extension          = 1
		; Seperate tables between energy group pairs
		energygrp_table          = 
		; Spacing for the PME/PPPM FFT grid
		fourierspacing           = 0.12
		; FFT grid size, when a value is 0 fourierspacing will be used
		fourier_nx               = 0
		fourier_ny               = 0
		fourier_nz               = 0
		; EWALD/PME/PPPM parameters
		pme_order                = 4
		ewald_rtol               = 1e-5
		ewald_geometry           = 3d
		epsilon_surface          = 0
		optimize_fft             = yes

		; IMPLICIT SOLVENT ALGORITHM
		implicit_solvent         = No

		; GENERALIZED BORN ELECTROSTATICS
		; Algorithm for calculating Born radii
		gb_algorithm             = Still
		; Frequency of calculating the Born radii inside rlist
		nstgbradii               = 1
		; Cutoff for Born radii calculation; the contribution from atoms
		; between rlist and rgbradii is updated every nstlist steps
		rgbradii                 = 1
		; Dielectric coefficient of the implicit solvent
		gb_epsilon_solvent       = 80
		; Salt concentration in M for Generalized Born models
		gb_saltconc              = 0
		; Scaling factors used in the OBC GB model. Default values are OBC(II)
		gb_obc_alpha             = 1
		gb_obc_beta              = 0.8
		gb_obc_gamma             = 4.85
		gb_dielectric_offset     = 0.009
		sa_algorithm             = Ace-approximation
		; Surface tension (kJ/mol/nm^2) for the SA (nonpolar surface) part of GBSA
		; The value -1 will set default value for Still/HCT/OBC GB-models.
		sa_surface_tension       = -1

		; OPTIONS FOR WEAK COUPLING ALGORITHMS
		; Temperature coupling  
		tcoupl                   = No
		nsttcouple               = -1
		nh-chain-length          = 10
		; Groups to couple separately
		tc-grps                  = 
		; Time constant (ps) and reference temperature (K)
		tau-t                    = 
		ref-t                    = 
		; Pressure coupling     
		Pcoupl                   = No
		Pcoupltype               = Isotropic
		nstpcouple               = -1
		; Time constant (ps), compressibility (1/bar) and reference P (bar)
		tau-p                    = 1
		compressibility          = 
		ref-p                    = 
		; Scaling of reference coordinates, No, All or COM
		refcoord_scaling         = No
		; Random seed for Andersen thermostat
		andersen_seed            = 815131

		; OPTIONS FOR QMMM calculations
		QMMM                     = no
		; Groups treated Quantum Mechanically
		QMMM-grps                = 
		; QM method             
		QMmethod                 = 
		; QMMM scheme           
		QMMMscheme               = normal
		; QM basisset           
		QMbasis                  = 
		; QM charge             
		QMcharge                 = 
		; QM multiplicity       
		QMmult                   = 
		; Surface Hopping       
		SH                       = 
		; CAS space options     
		CASorbitals              = 
		CASelectrons             = 
		SAon                     = 
		SAoff                    = 
		SAsteps                  = 
		; Scale factor for MM charges
		MMChargeScaleFactor      = 1
		; Optimization of QM subsystem
		bOPT                     = 
		bTS                      = 

		; SIMULATED ANNEALING  
		; Type of annealing for each temperature group (no/single/periodic)
		annealing                = 
		; Number of time points to use for specifying annealing in each group
		annealing_npoints        = 
		; List of times at the annealing points for each group
		annealing_time           = 
		; Temp. at each annealing point, for each group.
		annealing_temp           = 

		; GENERATE VELOCITIES FOR STARTUP RUN
		gen-vel                  = no
		gen-temp                 = 300
		gen-seed                 = 173529

		; OPTIONS FOR BONDS    
		constraints              = none
		; Type of constraint algorithm
		constraint-algorithm     = Lincs
		; Do not constrain the start configuration
		continuation             = no
		; Use successive overrelaxation to reduce the number of shake iterations
		Shake-SOR                = no
		; Relative tolerance of shake
		shake-tol                = 0.0001
		; Highest order in the expansion of the constraint coupling matrix
		lincs-order              = 4
		; Number of iterations in the final step of LINCS. 1 is fine for
		; normal simulations, but use 2 to conserve energy in NVE runs.
		; For energy minimization with constraints it should be 4 to 8.
		lincs-iter               = 1
		; Lincs will write a warning to the stderr if in one step a bond
		; rotates over more degrees than
		lincs-warnangle          = 30
		; Convert harmonic bonds to morse potentials
		morse                    = no

		; ENERGY GROUP EXCLUSIONS
		; Pairs of energy groups for which all non-bonded interactions are excluded
		energygrp_excl           = 

		; WALLS                
		; Number of walls, type, atom types, densities and box-z scale factor for Ewald
		nwall                    = 0
		wall_type                = 9-3
		wall_r_linpot            = -1
		wall_atomtype            = 
		wall_density             = 
		wall_ewald_zfac          = 3

		; COM PULLING          
		; Pull type: no, umbrella, constraint or constant_force
		pull                     = no

		; NMR refinement stuff 
		; Distance restraints type: No, Simple or Ensemble
		disre                    = No
		; Force weighting of pairs in one distance restraint: Conservative or Equal
		disre-weighting          = Conservative
		; Use sqrt of the time averaged times the instantaneous violation
		disre-mixed              = no
		disre-fc                 = 1000
		disre-tau                = 0
		; Output frequency for pair distances to energy file
		nstdisreout              = 100
		; Orientation restraints: No or Yes
		orire                    = no
		; Orientation restraints force constant and tau for time averaging
		orire-fc                 = 0
		orire-tau                = 0
		orire-fitgrp             = 
		; Output frequency for trace(SD) and S to energy file
		nstorireout              = 100
		; Dihedral angle restraints: No or Yes
		dihre                    = no
		dihre-fc                 = 1000

		; Free energy control stuff
		free-energy              = no
		init-lambda              = 0
		delta-lambda             = 0
		foreign_lambda           = 
		sc-alpha                 = 0
		sc-power                 = 0
		sc-sigma                 = 0.3
		nstdhdl                  = 10
		separate-dhdl-file       = yes
		dhdl-derivatives         = yes
		dh_hist_size             = 0
		dh_hist_spacing          = 0.1
		couple-moltype           = 
		couple-lambda0           = vdw-q
		couple-lambda1           = vdw-q
		couple-intramol          = no

		; Non-equilibrium MD stuff
		acc-grps                 = 
		accelerate               = 
		freezegrps               = 
		freezedim                = 
		cos-acceleration         = 0
		deform                   = 

		; Electric fields      
		; Format is number of terms (int) and for all terms an amplitude (real)
		; and a phase angle (real)
		E-x                      = 
		E-xt                     = 
		E-y                      = 
		E-yt                     = 
		E-z                      = 
		E-zt                     = 

		; User defined thingies
		user1-grps               = 
		user2-grps               = 
		userint1                 = 0
		userint2                 = 0
		userint3                 = 0
		userint4                 = 0
		userreal1                = 0
		userreal2                = 0
		userreal3                = 0
		userreal4                = 0
		"""

		PME_em = """;
		;	Energy minimizing
		;	3 jul 2006
		;
		cpp                 =  /lib/cpp
		define              =  -DFLEXIBLE
		constraints         =  none
		integrator          =  steep
		dt                  =  0.002
		nsteps              =  20
		ns_type             =  grid
		rlist               =  1.0
		coulombtype         =  PME 
		rcoulomb            =  1.0
		rvdw                =  1.4
		fourierspacing      =  0.12
		fourier_nx          =  0
		fourier_ny          =  0
		fourier_nz          =  0
		pme_order           =  4
		ewald_rtol          =  1e-5
		optimize_fft        =  yes
		;
		;	Energy minimizing stuff
		;
		;  
		emtol               =  1000
		emstep              =  0.01
		"""

		arq = open("PME_em.mdp", "w")
		arq.writelines(PME_em)
		arq.close()

		arq = open("mdout.mdp", "w")
		arq.writelines(mdout)
		arq.close()
			
	def GMX_modify_addChangesToList(self, data_path, resi_number, resn_wild, resn_mutant):
		""" Function doc """
		GMX_outputs = data_path+"/GMX_outputs"
		if not os.path.exists ( GMX_outputs ): os.mkdir (GMX_outputs)
		
		
		self.text_GMX_modify.append(resi_number+"   "+resn_wild+"  >  "+ resn_mutant+ "\n")
		

		self.GMX_modify_resi.append(resi_number)
		self.GMX_modify_resn.append(resn_wild)
		self.GMX_modify_resn_new.append(resn_mutant)

		return self.text_GMX_modify		
	
	def GMX_modify_CLEAN_LIST(self):
		self.text_GMX_modify     = []	
		self.GMX_modify_resn     = []
		self.GMX_modify_resi     = []
		self.GMX_modify_resn_new = []
		return self.text_GMX_modify

	def GMX_export_pdb_from_pymol(self, data_path, pymol_obj, ff_type):
		
		GMX_outputs = data_path+"/GMX_outputs"
		if not os.path.exists ( GMX_outputs ): os.mkdir (GMX_outputs)
		cmd.save(GMX_outputs+"/tmp.pdb", pymol_obj, 1, "pdb")
		
		
																		        #	filein = "/home/fernando/Documents/GTK_Dynamo/GTK_Dynamo0.0.2.16_GTK2.18/1bx4.pdb"
																				# 	outros dados podem ser extraidos, como CRYST1
		arq =  open(GMX_outputs+"/tmp.pdb","r")							#	abrindo o arquivo que o pymol exporta
																				#

		text  = []					     		
		for line in arq:						
			line2 = line.split()				
			line1 = line[0:6]					
			#if line2[0] == "CRYST1":																	  li[38:46]									
			#	print line2[0:-1]																				  li[46:54]
			#	print line
			if line1 == "ATOM  " :				
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


				resi2 = resi.split()
				resi2 = resi2[0]			
				
				A_name2 = A_name.split()		
				A_name2 = A_name2[0]			
				
				resn2 = resn.split()
				resn2 = resn2[0]


				n = 0   #	abre o contador
				if 	self.GMX_modify_resi != []:
					for i in self.GMX_modify_resi:							
						i = int(i)									        
						if int(resi2) == i:							        
							if resn2 == self.GMX_modify_resn[n]:		    
								resn = (" "+self.GMX_modify_resn_new[n])   	
								#print resn 						     	    	
						n = n+1										         	
		
				print "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				string = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				text.append(string+'\n' )



			if  line1 == "HETATM":				
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


				resi2 = resi.split()
				resi2 = resi2[0]			
				
				A_name2 = A_name.split()		
				A_name2 = A_name2[0]			
				
				resn2 = resn.split()
				resn2 = resn2[0]


				n = 0   #	abre o contador
				if 	self.GMX_modify_resi != []:
					for i in self.GMX_modify_resi:							
						i = int(i)									        
						if int(resi2) == i:							        
							if resn2 == self.GMX_modify_resn[n]:		    
								resn = (" "+self.GMX_modify_resn_new[n])   	
								#print resn 						     	    	
						n = n+1										         	


				
				print "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				string = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s"% (line1, index, A_name, resn, chain, resi, gap, x, y, z, b, oc, gap2, atom)
				text.append(string+'\n' )
				
			if line1 == "TER   ":
				text.append(line + "\n")



				
		arq2 = open(GMX_outputs+"/tmp.pdb", 'w')
		arq2.writelines(text)
		arq2.close()	
		return GMX_outputs+"/tmp.pdb"	
	
	def GMX_make_pbd2gmx_run(self, 
								data_path, 
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
								conc):                 # concentration flag
									
		GMX_outputs = data_path+"/GMX_outputs"
		if not os.path.exists ( GMX_outputs ): os.mkdir (GMX_outputs)
		
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
		"""	
		1: TIP3P   TIP 3-point, recommended
		2: TIP4P   TIP 4-point
		3: TIPS3P  CHARMM TIP 3-point with LJ on H's (note: twice as slow in GROMACS)
		4: SPC     simple point charge
		5: SPC/E   extended simple point charge
		6: None
		"""	
		#GMX_outputs+"/file_teste.pdb"
		
		
		arq_pdb  = open(filein, "r" )
		pdbFile  = arq_pdb.read()

		pdbFile = pdbFile.replace ("HETATM","ATOM  ")
		
		

		if ff_type == "charmm27": 
			pdbFile = pdbFile.replace("K   K ","POT POT")
			pdbFile = pdbFile.replace("CS   CS"," CES CES") 
			pdbFile = pdbFile.replace("CA   CA"," CAL CAL") 					
			pdbFile = pdbFile.replace("ZN   ZN"," ZN  ZN2") 					# Modifies IONS name and format to be recognized by the CHARMM27 force filed
			pdbFile = pdbFile.replace("CL   CL"," CLA CLA")  					
			pdbFile = pdbFile.replace("NA   NA"," SOD SOD") 					
			pdbFile = pdbFile.replace("MG   MG"," MG  MG") 

		else:	
			pdbFile = pdbFile.replace("K   K ","K   K  ")   
			pdbFile = pdbFile.replace("RB   RB"," Rb  RB ")
			pdbFile = pdbFile.replace("CS   CS"," Cs  CS ")
			pdbFile = pdbFile.replace("LI   LI"," Li  LI ") 					# Modifies IONS name and format to be recognized by the AMBER force field															
			pdbFile = pdbFile.replace("ZN   ZN"," Zn  ZN ")														
			pdbFile = pdbFile.replace("CL   CL"," CL  CL ")
			pdbFile = pdbFile.replace("NA   NA"," Na  NA ") 	
			pdbFile = pdbFile.replace("MG   MG"," Mg  MG ") 																								


		"""
		ARQUIVO PDB:
		PADRAO = 	HETATM 2772  O6  M0N A 901      14.124  35.511  -6.573  1.00 32.43           O
		
					HETATM 4900  POT K   B 336      20.651 108.233  29.391  0.45 42.58           K 	
					HETATM 4900  POT POT B 336      20.651 108.233  29.391  0.45 42.58           K 	
					HETATM 2750  MG  MG  A 907      18.474  34.751  -7.471  1.00 23.57          MG 		
					HETATM 2750  CL  CL  A 907      18.474  34.751  -7.471  1.00 23.57          NA
					HETATM 2750 LI    LI A 907      18.474  34.751  -7.471  1.00 23.57          LI
					HETATM 2750 ZN    ZN A 907      18.474  34.751  -7.471  1.00 23.57          ZN
					HETATM 2750 RB    RB A 907      18.474  34.751  -7.471  1.00 23.57          RB
					HETATM 2750 CS    CS A 907      18.474  34.751  -7.471  1.00 23.57          CS
					HETATM 2750 CL    CL A 907      18.474  34.751  -7.471  1.00 23.57          CL
		"""


		arq_pdb2 = open(filein, "w")
		arq_pdb2.write( pdbFile )
		
		print pdbFile
		
		arq_pdb.close()
		arq_pdb2.close()
		
		if double == True:
			
			try:
				os.system ("rm " + GMX_outputs+"/*#*")
				
			except:
				a = None
			try:
				os.system ("rm " + GMX_outputs+"/tmp_*")
			except:
				a = None
			os.system ( "pdb2gmx_d -f " + filein + ' -water ' + water_type + " -ff " + ff_type + " -p " + GMX_outputs+"/tmp " + " -o " + GMX_outputs+"/tmp")
			
			#diameter = 1.2
	
			
			
			if solvate == True:
				os.system ( "editconf_d -f " + GMX_outputs+"/tmp.gro " + "-bt cubic -d " + str(diameter) + " -c -o " + GMX_outputs+"/tmp_editconf" )
				os.system ( "genbox_d -cp " + GMX_outputs+"/tmp_editconf" + " -cs -p " + GMX_outputs+"/tmp.top "+ "-o " +  GMX_outputs+"/tmp" )
				os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro"+ " -p " + GMX_outputs+"/tmp.top " + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )                                            
			else:
				os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro"+ " -p "     + GMX_outputs+"/tmp.top " + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
				
			if solvate == True:
				if ionize == "custom":
					os.system ( 'echo "SOL" | genion_d -s ' + GMX_outputs+'/tmp.tpr -p ' + GMX_outputs+ '/tmp.top ' + ' -np ' + np + ' -pname ' + pname + ' -nn ' + nn+ ' -nname ' + nname +  ' -rmin 0.6 -norandom -o ' + GMX_outputs+'/tmp')
					filein   = GMX_outputs+"/tmp.top"
					fileout  = GMX_outputs+"/tmp.top"
					reductor = int(nn) + int(np)
					print "reductor", reductor
					
					#GMX_top_modify (filein, fileout, reductor )
					
					os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
				if ionize == "neutral":
					os.system ( 'echo "SOL" | genion_d -s '  + GMX_outputs+ '/tmp.tpr -p ' + GMX_outputs+'/tmp.top ' + ' -conc ' + conc + ' -neutral -rmin 0.6 -norandom -o ' + GMX_outputs+'/tmp')
					os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
				
				if ionize == None:
					os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
	
	
	
	
	
				
			if minimization == True:
				os.system ( "mdrun_d -v -s " + GMX_outputs+"/tmp.tpr" + " -e " + GMX_outputs+"/tmp" + " -c "+ GMX_outputs+"/tmp" + " -o " + GMX_outputs+"/tmp" )
				os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -pp " + GMX_outputs+"/tmp_processed.top" )
				print "coordinates / topology = OK "
				
				os.rename(GMX_outputs+"/tmp.gro",        data_path + "/" + system_name + ".gro")
				os.rename(GMX_outputs+"/tmp_processed.top", data_path + "/" + system_name + ".top")
				
			else:
				os.system ( "grompp_d -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro"+ " -p " +      GMX_outputs+"/tmp.top " + " -pp " + GMX_outputs+"/tmp_processed.top" )
				print "coordinates / topology = OK "
				
				os.rename(GMX_outputs+"/tmp.gro",           data_path + "/" + system_name + ".gro")
				os.rename(GMX_outputs+"/tmp_processed.top", data_path + "/" + system_name + ".top")		
			os.system ("mv *# " + GMX_outputs)
			
		
		else:
				
			try:
				os.system ("rm " + GMX_outputs+"/*#*")
				
			except:
				a = None
			try:
				os.system ("rm " + GMX_outputs+"/tmp_*")
			except:
				a = None
			os.system ( "pdb2gmx -f " + filein + ' -water ' + water_type + " -ff " + ff_type + " -p " + GMX_outputs+"/tmp " + " -o " + GMX_outputs+"/tmp")
			
			#diameter = 1.2
	
			
			
			if solvate == True:
				os.system ( "editconf -f " + GMX_outputs+"/tmp.gro " + "-bt cubic -d " + str(diameter) + " -c -o " + GMX_outputs+"/tmp_editconf" )
				os.system ( "genbox -cp " + GMX_outputs+"/tmp_editconf" + " -cs -p " + GMX_outputs+"/tmp.top "+ "-o " +  GMX_outputs+"/tmp" )
				os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro"+ " -p " + GMX_outputs+"/tmp.top " + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )                                            
			else:
				os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro"+ " -p "     + GMX_outputs+"/tmp.top " + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
				
			if solvate == True:
				if ionize == "custom":
					os.system ( 'echo "SOL" | genion -s ' + GMX_outputs+'/tmp.tpr -p ' + GMX_outputs+ '/tmp.top ' + ' -np ' + np + ' -pname ' + pname + ' -nn ' + nn+ ' -nname ' + nname +  ' -rmin 0.6 -norandom -o ' + GMX_outputs+'/tmp')
					filein   = GMX_outputs+"/tmp.top"
					fileout  = GMX_outputs+"/tmp.top"
					reductor = int(nn) + int(np)
					print "reductor", reductor
					
					#GMX_top_modify (filein, fileout, reductor )
					
					os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
				if ionize == "neutral":
					os.system ( 'echo "SOL" | genion -s '  + GMX_outputs+ '/tmp.tpr -p ' + GMX_outputs+'/tmp.top ' + ' -conc ' + conc + ' -neutral -rmin 0.6 -norandom -o ' + GMX_outputs+'/tmp')
					os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
				
				if ionize == None:
					os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -o " +  GMX_outputs+"/tmp > "+  GMX_outputs+"/log.log" )
	
	
	
	
	
				
			if minimization == True:
				os.system ( "mdrun -v -s " + GMX_outputs+"/tmp.tpr" + " -e " + GMX_outputs+"/tmp" + " -c "+ GMX_outputs+"/tmp" + " -o " + GMX_outputs+"/tmp" )
				os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro" + " -p "   + GMX_outputs+"/tmp.top" + " -pp " + GMX_outputs+"/tmp_processed.top" )
				print "coordinates / topology = OK "
				
				os.rename(GMX_outputs+"/tmp.gro",        data_path + "/" + system_name + ".gro")
				os.rename(GMX_outputs+"/tmp_processed.top", data_path + "/" + system_name + ".top")
				
			else:
				os.system ( "grompp -f PME_em.mdp -c " + GMX_outputs+"/tmp.gro"+ " -p " +      GMX_outputs+"/tmp.top " + " -pp " + GMX_outputs+"/tmp_processed.top" )
				print "coordinates / topology = OK "
				
				os.rename(GMX_outputs+"/tmp.gro",           data_path + "/" + system_name + ".gro")
				os.rename(GMX_outputs+"/tmp_processed.top", data_path + "/" + system_name + ".top")		
			os.system ("mv *# " + GMX_outputs)
		
		if ff_type == "charmm27":
		
			tranquera = open( data_path + "/" + system_name + ".top", "r" )													
			topology  = tranquera.read()								# IONS of the CHARMM27 force field

			topology = topology.replace("OH          1", "")																				 
			topology = topology.replace("1       OC          1       OH          O1       1      -1.32", "")									  
			topology = topology.replace("2       H           1       OH          H1       1      0.32", "")											  
			topology = topology.replace("1   2   1       0.09700 456056   ; hydroxyl bond", "")												  	
			topology = topology.replace("MG          1", "")																						 
			topology = topology.replace("1              MG          MG       1      2   ", "")													   	
			topology = topology.replace("K           1", "")																				     	
			topology = topology.replace("1       POT         1       K           K        1      1 ", "")									 		
			topology = topology.replace("CS          1", "")																						 	
			topology = topology.replace("1       CES         1       CS          CS       1      1", "")													 
			topology = topology.replace("CA          1", "")																							 	
			topology = topology.replace("1       CAL         1       CA          CA       1      2", "")										 		
			topology = topology.replace("ZN          1", "")																								 
			topology = topology.replace("1              ZN          ZN       1      -2   ", "")														 
			topology = topology.replace("[ moleculetype ] ; added by Bjelkmar Jan 2010, from c32b1/toppar/stream/toppar_water_ions.str\n; molname   nrexcl\n\n\n[ atoms ]\n; id    at type     res nr  residu name at name  cg nr  charge   mass\n\n\n\n[ bonds ]\n;i  j   funct   length  force.c.", "")
			topology = topology.replace("[ moleculetype ]\n; molname   nrexcl\n\n\n[ atoms ]\n; id    at type     res nr  residu name at name  cg nr  charge", "")

			topology2 = open(data_path + "/" + system_name + ".top", "w")
			topology2.write ( topology )
			
			print "CHARMM27 FORCE FIELD"
			
			tranquera.close()
			topology2.close()
			
		else:
			
			tranquera = open( data_path + "/" + system_name + ".top", "r" )		# IONS of the AMBER force field
			topology  = tranquera.read()																			        				
			topology = topology.replace("IB+             1       ; big positive ion", "")
			topology = topology.replace("1       IB              1       IB+             IB       1      1.00000", "")
			topology = topology.replace("CA              1", "")
			topology = topology.replace("1       C0              1       CA              CA       1      2.00000", "")
			topology = topology.replace("MG              1", "")
			topology = topology.replace("1              MG              MG       1      2.00000", "")
			topology = topology.replace("K               1", "")
			topology = topology.replace("1              K               K        1      1.00000", "")
			topology = topology.replace("RB              1", "")
			topology = topology.replace("1       Rb              1       RB              RB       1      1.00000", "")
			topology = topology.replace("CS              1", "")
			topology = topology.replace("1       Cs              1       CS              CS       1      1.00000", "")
			topology = topology.replace("LI              1", "")
			topology = topology.replace("1       Li              1       LI              LI       1      1.00000", "")
			topology = topology.replace("ZN              1", "")
			topology = topology.replace("1       Zn              1       ZN              ZN       1      2.00000", "")
			topology = topology.replace("[ moleculetype ]\n; molname       nrexcl\n\n\n[ atoms ]\n; id    at type         res nr  residu name     at name  cg nr  charge", "")

			topology2 = open( data_path + "/" + system_name + ".top", "w" )
			topology2.write ( topology )

			tranquera.close()
			topology2.close()
			
			
			print "GENERAL AMBER FORCE FIELD"
			
			self.GMX_clean_tmp_files()
			
	def GMX_clean_tmp_files(self):
		try:
			os.remove('topol.tpr' )
			os.remove('mdout.mdp' )	
			os.remove('posre.itp' )
			os.remove('PME_em.mdp')
			os.remove('md.log'    )

		except:
			a = None
			
