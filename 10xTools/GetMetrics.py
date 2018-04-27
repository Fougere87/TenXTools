#!/usr/bin/python

import sys, getopt

def main(argv):
   mol_info_file = ''
   cells_names_file = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hm:c:o:",["mol_info_file=","cell_file=", "output="])
   except getopt.GetoptError:
      print 'test.py -m <mol_info_file> -c <cell_file>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -m <mol_info_file> -c <cell_file> -o <output>'
         sys.exit()
     elif opt in ("-m", "--mol_info_file"):
         mol_info_file = arg
     elif opt in ("-c", "--cell_names"):
         cells_names_file = arg
    elif opt in ("-o", "--out"):
        outputfile = arg
   print('molecule_info file is ', mol_info_file)
   print('Cells file is ', cells_names_file)
   print('Output file is ', outputfile)


   with open(cells_names_file, "r") as cell_file :
       cells = cell_file.readlines()

   cells_ok = [n[0:16:1] for n in cells]

   mol_info = read_10x_h5(mol_info_file, CellsNamesToInt(cells_ok))

   mol_info_aggr = mol_info_aggr = mol_info.groupby("bc").sum()

   mol_info_aggr.index = convertBCs(mol_info_aggr.index)

   with open(outputfile, "w") as f :
    mol_info_aggr.to_csv(f)

if __name__ == "__main__":
   main(sys.argv[1:])



with open("../TE16/cells_TE16_1.txt", "r") as cell_file :
    cells = cell_file.readlines()

cells_ok = [n[0:16:1] for n in cells]

CellsNamesToInt(cells_ok)

mol_info = read_10x_h5("../TE16/Raw_data/TE16_1/molecule_info.h5")
