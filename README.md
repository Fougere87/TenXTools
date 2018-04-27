# 10xTools
Functions to access the molecule_info.h5 file from Cellranger and compute metrics from it.

You can find functions to read H5 molecule_info from cellRanger output in H5_reading.py file

To get reads metrics for a customized set of cells use the GetMetrics.py script. 
usage : GetMetrics.py -m <mol_info_file> -c <cell_file> -o <output>
where cell_file contains the barcodes of the cells you are interested in. 

Be cautious, using this function with a dataset containing 4000 cells sequenced @ 150 KReads/cell used 20GB of RAM

Thanks for using !
