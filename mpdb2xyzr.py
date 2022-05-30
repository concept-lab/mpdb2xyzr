#            MIT LICENSE

#   **  mpdb2xyzr  Copyright (C) 2022  Luca Gagliardi
#       Affiliation: CONCEPT LAB, Istituto Italiano di Tecnologia


# PREREQUISITE: provide an mpdb file OR install catdcd
# https://www.ks.uiuc.edu/Development/MDTools/catdcd/license.cgi?files/catdcd-4.0b.tar.gz



print("**PREREQUISITE: provide an mpdb file (or place a catdcd executable in the working directory)**")
import subprocess
import os
import re
import sys

def readPDB(inputFILE):
    comment =['#', 'CRYST[0-9]?','HEADER','HETATM']
    remark = ['REMARK']
    termination = ['TER', 'END', '\n']
    skip = comment+remark+termination
    skip = '(?:% s)' % '|'.join(skip)

    header = slice(0,4)
    number = slice(7,11)
    name = slice(13,16) #polarity
    resname = slice(17,20) #dummy resname
    chain = slice(21,22)
    resSeq = slice(22,27)
    coordIndx = slice(31,38)
    coordIndy = slice(39,46)
    coordIndz = slice(47,54)
    occupancy = slice(56,60)
    tempFactor = slice(62,66)
    segmentIdent = slice(67,76)
    element = slice(77,79)
    coord = []
    pdblines =[]
    try:
        inFile = open(inputFILE,'r')
        # print(pname+'_atm.pdb')
    except Exception:
        raise NameError("Cannot load PDB file")
    for line in inFile:
        if(re.match(skip,line)): 
            continue
        if (line[header]=='ATOM'):
            coord.append([float(line[coordIndx]),float(line[coordIndy]),float(line[coordIndz])])
            pdblines.append(line)
            # break
        else:
            pass
    # print(line,len(line))
    # print(line[header])
    # print(line[number])
    # print(line[name])
    # print(line[resname])
    # print(line[chain])
    # print(line[resSeq])
    # print(coord)
    # print(line[occupancy])
    # print(line[tempFactor])
    # print(line[segmentIdent])
    # print(line[element])

    inFile.close()

    return pdblines

def endCounter(inputFILE):
    termination = ['TER', 'END']
    termination ='(?:% s)' % '|'.join(termination)
    try:
        # print(structure+'.pdb')
        inFile = open(inputFILE,'r')
    except Exception:
        raise NameError("Cannot load MPDB file! The file must be provided (running catdcd)")
    
    n=0 
    for line in inFile:
        if(re.match(termination,line)): 
            n+=1
    inFile.close()

    return n

def readPQR(inputFILE):
    '''
    Returns radii list from pqr. We assume the ordering to be kept across frames..
    '''
    print("READING PQR..")
    try:
        # print(structure+'.pdb')
        inFile = open(inputFILE,'r')
    except Exception:
        raise NameError("Cannot load PQR file! The file must be provided")
    # try:
    #     # print(structure+'.pdb')
    #     _check = open(structure+'.pdb','r')
    # except Exception:
    #     raise NameError("Cannot load PDB file")
    comment =['#', 'CRYST[0-9]?']
    remark = ['REMARK']
    termination = ['TER', 'END', '\n']
    skip = comment+remark+termination
    skip = '(?:% s)' % '|'.join(skip)
    radii=[]
    for line in inFile:
        if(re.match(skip,line)): 
            pass
        else:
            #when containing chain info
            r = line.split()[10]
            try:
                r = float(r)
                # print(line)
                # print(r)
            except:
                #when not containing chain info
                r = line.split()[9]
                try:
                    r = float(r)
                    # print(line)
                    # print(r)
                except:
                    print("format problem")
                    print(line)
                    exit()
        if (r<0):
            print("format problem")
            print(line)
            exit()
        radii.append(r)

    inFile.close()
    
    return radii  
    



def main(argv):

    import numpy as np
    import getopt
    try:
        opts, args = getopt.getopt(argv,"h",["help","mpdb","rmMPDB"])
    except getopt.GetoptError:
        print ('uncorrect formatting of options')
        exit()
    onlyXYZR = True
    keepMPDB = True
    structName = None
    for opt, arg in opts:
        if opt in["-h","--help"]:
            print("Usage:\npython3 mpdb2xyzr.py \nThen the structure name (without format) must be inserted from command line.\nOptions:")
            print("--mpdb: the mpdb file is produced in a standard way by providing the working directory a TRR and PDB file (catdcd must also be in the working directory)")
            print("--rmMPDB: the mpdb file is removed after use (default False)")
            # print("--readMPDB: the mpdb file already exist in the current folder. catdcd is not called, and only a reference pqr must be provided")
            input('\n')
            exit()
        if opt in ["--mpdb"]:
            onlyXYZR = False 
        if opt in ["--rmMPDB"]:
            keepMPDB = False

    runFolder  = './'
    resultFolder = 'results/'
    isFolder = os.path.isdir(resultFolder)

    if not isFolder:
            subprocess.run(['mkdir',resultFolder])

    if(len(args[0])>0):
        inputName = args[0]
        match = re.match('([\w]*)',inputName) #accepts both <pqrname> <pqrname.pqr>, and mpdb
        structName = match.group(1)
    
    if (onlyXYZR):
        if structName is None:
            print("Provide a PQR and MPDB file in the working directory: <name>.pqr, <name>.mpdb")
            structName = input("Insert structure name\n")
        

    else:

        print("Insert structure name. Correctly prepare input in the working directory:\n A reference PDB file (<name>.pdb) and a TRR trajectory file must be provided (<name.trr>).")
        print("Provide also a PQR file: <name>.pqr")
        print("catdcd executable must be in the working directory")
        answ=input("CONTINUE? (y/n)")


        if(answ=='y'or answ==1):
            pass
        elif (answ=='n'):
            exit()
        else:
            exit("Invalid answer")
        if structName is None:
            structName = input("Insert structure name\n")
         
        # matchPDB =re.match("(.+)\.pdb",runFolder+structName)
        # if matchPDB:
        #     refPDB=matchPDB.groups()[0]
        #     print(refPDB)
        #     input()
        # else:
        #     exit("cannot find PDB file")

        # matchPQR =re.match("(.+)\.pqr",runFolder+structName)
        # if matchPQR:
        #     refPQR=matchPQR.groups()[0]
        # else:
        #     exit("cannot find PQR file")
        refPDB = runFolder+structName+'.pdb'
        refPQR = runFolder+structName+'.pqr'

        pdbLines = readPDB(refPDB)
        radii = readPQR(refPQR)
        nAtoms = len(radii)

        
        # print("CHECK consistency:", len(pdbLines))
        if(len(radii)!=len(pdbLines)):
            print("inconsistency between PQR and PDB files..")
            exit()
        
        print("Number of atoms per frame:",len(radii))
        print()

        outNAME = structName+'.mpdb'

        if os.path.isfile(structName+".trr"):
            fileTRAJECTORY=structName+".trr"
            print("Running catdcd. This process could take some minutes..")
            out = subprocess.check_output(['./catdcd', '-s',refPDB , '-o',outNAME, '-otype', 'pdb', '-trr', fileTRAJECTORY],cwd=runFolder,text=True)
        elif os.path.isfile(structName+".gro"):
            print("Running catdcd. This process could take some minutes..")
            out = subprocess.check_output(['./catdcd', '-s',refPDB , '-o',outNAME, '-otype', 'pdb', '-gro', fileTRAJECTORY],cwd=runFolder,text=True)
            fileTRAJECTORY=structName+".gro"
        else:
            exit("TRR or GRO trajectory files not found")

        print("\ncatdcd output:  ", out)
        print("*******************")

        match = re.search("(Total frames:\s*)(\d+)",out)
        if match:
            n_frames = float(match.group(2))
            print("n frames =", n_frames)
        else:
            exit("<ERROR>")

    ###### MAIN: build xyzr frames ######
    
    resultFolder = 'results/' + structName+'/'
    outNAME = runFolder+structName+'.mpdb'

    if(onlyXYZR):
        refPQR = runFolder+structName+'.pqr'#'examples/5HT3A_WT.pqr'
        radii = readPQR(refPQR)
        n_frames = endCounter(outNAME)
        print("Number of frames = ",n_frames)

    else:
        pass
    
    try:
        inFile = open(outNAME,'r')
    except:
        print("mpdb file not found!!")
        exit()
    
    isFolder = os.path.isdir(resultFolder)
    
    if not isFolder:
            subprocess.run(['mkdir',resultFolder])

    print("** mpdb file: ", outNAME)
    print("\nBuilding xyzr frames")

    
    # refPDB = runFolder+structName+'.pdb'#'examples/5HT3A_WT.pdb'
    
    # pdbLines = readPDB(refPDB)
    nAtoms = len(radii)
    print()
    # print("number of atoms per frame:",len(radii))
    # print("CHECK consistency:", len(pdbLines))
    # if(len(radii)!=len(pdbLines)):
    #     print("inconsistent number of radii provided (check PQR format!)")
    #     exit()

    #separate file from END to END keyword
    
    commentline =['#', 'CRYST[0-9]?']
    remark = ['REMARK']
    skip = commentline + remark + ['\n']
    skip = '(?:% s)' % '|'.join(skip)
    termination = ['TER', 'END']
    termination ='(?:% s)' % '|'.join(termination)
    # print(skip)
    coordIndx = slice(31,38)
    coordIndy = slice(39,46)
    coordIndz = slice(47,54)
    resultFolder = resultFolder+'frames_xyzr/'
    isFolder = os.path.isdir(resultFolder)
    if not isFolder:
            subprocess.run(['mkdir',resultFolder])

    
    padding = len(str(int(n_frames)))
            
    frameName = resultFolder+"{num:0{width}}.xyzr".format(num=1,width=padding)
    n = 1
    counter = 0
    coord = []
    lineNumber=0
    # lines = inFile.readlines()
    for line in inFile:
        if(re.match(skip,line)): 
            # print(line)
            continue
        if(re.match(termination,line)): 
            # print(line)
            #new frame save previous one
            print('saving frame: '+str(n))
            coord = np.array(coord)
            # print(coord.shape)
            if(coord.shape[0]!=nAtoms):
                print("<WARNING> unexpected number of atoms in frame "+str(n))
            np.savetxt(frameName,coord,delimiter='\t',header='Frame '+str(n)+', nAtoms= '+str(nAtoms),fmt='%10.4f')
            lineNumber = 0 
            n+=1
            frameName = resultFolder+"{num:0{width}}.xyzr".format(num=n,width=padding)
            coord=[]
            pass
        else:
            counter+=1
            try:
                coord.append([float(line[coordIndx]),float(line[coordIndy]),float(line[coordIndz]),float(radii[lineNumber])])
            except:
                print('FAILURE! : ')
                print(line)
                print(line[coordIndx])
                print(line[coordIndy])
                print(line[coordIndz])
                print(radii[lineNumber])
                break
            lineNumber +=1


    inFile.close()

    # print("Expected number of frames = ",int(counter/len(radii)))
    print("Check--> Number of frames: ",n-1,int(counter/len(radii)))
    if(keepMPDB):
        pass
        # print('mpdb file was displaced in ',resultFolder)
        # outNAME = resultFolder+structName+'.mpdb'
        # # isFile = os.path.isfile(outNAME)
        # # if not isFile:
        # subprocess.run(['mv',runFolder+structName+'.mpdb',outNAME])
    else:
        print('removing mpdb file')
        subprocess.run(['rm',runFolder+structName+'.mpdb'])
           


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nUser exit")
        exit()
