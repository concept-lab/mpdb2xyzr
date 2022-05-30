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

