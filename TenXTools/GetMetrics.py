import TenXTools
import sys, getopt

import h5py
import time
import numpy as np
import pandas as pd
import gc


def convertBCs(bcs) :
    """Take in input the uint64 barcodes from molecule_info file and convert it as nucleotide sequences"""
    code = "ACGT"
    barc=0
    bcs_str=[]
    for bc in bcs :
        if bc != barc :
            barc = bc
            binRep = np.binary_repr(bc, width=64)
            bc_str = ""
            for i in range(0,len(binRep),2):
                bitSet = str(binRep[i]+binRep[i+1])
                bc_str = bc_str+code[int(bitSet,2)]
        bcs_str.append(bc_str[-16::1])
    return bcs_str

def CellsNamesToInt(cellsName):
    """Convert barcode nucleotide sequences from 10x and convert it to uint64 format"""
    ret = []
    code = {"A":0,"C":1,"G":2, "T":3}
    for name in cellsName :
        binRep =''.join([np.binary_repr(code[l], width=2) for l in name])
        numRep = int(binRep,2)
        ret.append(numRep)
    return ret

def read_10x_h5(path2file, cellsNum):
    """Reads a molecule_info file from 10x and returns a pandas DataFrame with reads, unmapped_reads, nonconf_reads and read_counts for selected cells in uint64 dtype"""
    with h5py.File(path2file,'r') as hf:
        print('List of arrays in this file: \n', list(hf.keys()))
        start = time.time()
        bc = pd.Series(np.array(hf.get('barcode')))
        reads = pd.Series(hf.get('reads'),)
        nonconf_reads = pd.Series(hf.get('nonconf_mapped_reads'))
        unmap_reads = pd.Series(hf.get('unmapped_reads'))

        #TABLE = pd.DataFrame([bc,gene,np.int64(reads),nonconf_reads,unmap_reads,map_pos==1])
        stop = time.time()

    print('reading file and converting barcodes took ' + str(stop-start))
    goodLines = bc.isin(cellsNum)
    TABLE=pd.DataFrame()
    start = time.time()
    TABLE['bc']=bc[goodLines]
    TABLE['reads']=reads[goodLines]
    TABLE['nonconf_reads']=nonconf_reads[goodLines]
    TABLE['unmap_reads']=unmap_reads[goodLines]
    TABLE['read_counts']=reads[goodLines]+nonconf_reads[goodLines]+unmap_reads[goodLines]
    stop = time.time()

    print('pandaifying took ' + str(stop-start))

    start = time.time()
    TABLE = TABLE.groupby('bc').sum()
    stop = time.time()
    print('Aggregating took ' + str(stop-start))
    gc.collect()
    return TABLE


def main(args=None):

    args = sys.argv[1:]

    mol_info_file = ''
    cells_names_file = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(args,"hm:c:o:",["mol_info_file=","cell_file=", "output="])
    except getopt.GetoptError:
        print('GetMetrics.py -m <mol_info_file> -c <cell_file> -o <output>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('GetMetrics.py -m <mol_info_file> -c <cell_file> -o <output>')
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

    mol_info_aggr = mol_info.groupby("bc").sum()

    mol_info_aggr.index = convertBCs(mol_info_aggr.index)

    with open(outputfile, "w") as f :
        mol_info_aggr.to_csv(f)

if __name__ == "__main__":
    main()
