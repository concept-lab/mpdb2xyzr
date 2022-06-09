# mpdb2xyzr
Converts mpdb files to a set of frames in xyzr format given a reference PQR file.

## Prerequisites
 - Provide an mpdb trajectory file (recomended), or a functioning *catdcd* executable in the wotking directory together with a reference PDB file and a TRR file.

catdcd binary [here](https://www.ks.uiuc.edu/Development/MDTools/catdcd/license.cgi?files/catdcd-4.0b.tar.gz)

**Example of mpdb creation with catdcd**: 
./catdcd -s \<structureName\>.pdb  -o \<structureName\>.mpdb -otype pdb -trr \<structureName\>.trr

- pip install numpy and regex 

## Usage


**IMPORTANT** Provide also a reference PQR file (tipically, from the reference PDB file using softwares like *pdb2pqr*).

### Standard

In the working directory given \<structureName\>.pqr and  \<structureName\>.mpdb, run *python3 mpdb2xyzr.py \<structureName\>*

### Advanced

*python3 mpdb2xyzr.py --mpdb \<structureName\>*

Automatically generates the mpdb file by calling catdcd. catdcd must be present in the working directory together with
\<structureName\>.trr and \<structureName\>.pdb


Type *python3 mpdb2xyzr.py -h* or *--help* for more informations.

## Output
The script automatically creates a *results* folder containing a sub-folder named as the structure name (same as the mpdb and pqr filename).
Within this folder a folder containing all xyzr frames. Frames are numbered from 1 to max_frame with leading zeros padding.

## References
A. Raffo, L. Gagliardi, U. Fugacci, L. Sagresti, S. Grandinetti, G. Brancato S. Biasotti, W. Rocchia. "Chanalyzer: a computational geometry approach for the analysis of protein channel shape and dynamics", under review at Frontiers in Molecular Biosciences, 2022.
