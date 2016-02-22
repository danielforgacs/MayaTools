import maya.cmds as cmds, os, time


############### update list #########################################

def updateList(update):
    cmds.textScrollList('filelistNames', e=True, ra=True)    
    fileDirectory = cmds.textFieldButtonGrp('fileDirect', q=True, text=True)
    prefix = cmds.textFieldGrp('prefix', q=True, text=True)
    newName = cmds.textFieldGrp("newNam", q=True, text=True)
    paddedBy = cmds.intFieldGrp("paddedBy", q=True, v=True)[0]
    
    files = []
    for filesName in os.listdir(fileDirectory):
        if prefix in filesName:
            files.append(filesName)               
    files.sort()
    
################## gather files and sort and filter #########################
    
    fileAppend = []  
    nameOrDate = cmds.radioButtonGrp( "nameOrDate", q=True,  sl=1)
 
 
###### sort by name 
    count = 1
    if nameOrDate == 1:        
        for fil in files:
            newFileName = fil + "  to  " + newName + "." +  str(count).zfill(paddedBy) + os.path.splitext(fil)[1]
            fileAppend.append(newFileName)
            count += 1
      
####### sort by date
    if nameOrDate == 2: 
        timeArray= []      
        for fil in files:
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fileDirectory + "/" + fil)
            timeMade = time.ctime(mtime); times = str(timeMade).split(" ")[4].replace(":","")
            new = (int(times), fil);  timeArray.append(new)            
        timeArray.sort()
        
        
####### sort by frame number 
    if nameOrDate == 3: 
        timeArray = []
        for fil in files:
            new = []; noExt = os.path.splitext(fil)[0]
            while noExt[-1:].isdigit():
                noExt = noExt[:-1]
                       
            number = os.path.splitext(fil)[0].split(noExt)
            new.append(int(number[1]));  new.append(fil); timeArray.append(new)

        timeArray.sort()

        fileAppend = []
        for filName in timeArray:
            newFileName = filName[1] + "  to  " + newName + "." +  str(count).zfill(paddedBy) + os.path.splitext(filName[1])[1]
            fileAppend.append(newFileName); count += 1

        
        
#######  add to list
        for tme in timeArray:
            newFileName = tme[1] + "  to  " + newName + "." +  str(count).zfill(paddedBy) +  os.path.splitext(tme[1])[1]
            fileAppend.append(newFileName)
            count += 1
    cmds.textScrollList('filelistNames', e=True, append=fileAppend)   

##################################################################################################################


                
    
##################################################################################################################

def renameFiles(renameF):
    fileDirectory = cmds.textFieldButtonGrp('fileDirect', q=True, text=True)
    fileListToRename = cmds.textScrollList('filelistNames', q=True, ai=True) 
    moveOrCopy = cmds.checkBox( "moveOrCopy", q=True , v=True)
    for filesToRename in fileListToRename:
        source = fileDirectory + "/" + filesToRename.split("  ")[0]
        destination = fileDirectory + "/" + filesToRename.split("  ")[2]
        if moveOrCopy == 0:
            cmds.sysFile( source, move=destination )
            print ("Renamed......" + source + "....to...." + destination)
             
        if moveOrCopy == 1:
            cmds.sysFile( source, copy=destination )
            print ("Copied......" + source + "....to...." + destination) 
                
                
                
                            
##################################################################################################################
########################################### RENAMER GUI #########################################################

def renamer():
    windows = cmds.window( t="renameFiles", iconName='Short Name', widthHeight=(200, 55) )
    cmds.columnLayout()
    cmds.frameLayout( l="Find Files Information", borderStyle='in' , bgc = (0,0.35,1) )
    cmds.rowLayout( numberOfColumns=2, columnWidth2=(80, 1))
    cmds.text(l = "  Select Folder:")

    def setFilePath():
        filename = cmds.fileDialog2(fileMode=3, caption="Import Image")
        cmds.textFieldButtonGrp('fileDirect', e=True, text=filename[0])
        firstFile = os.path.splitext(os.listdir(filename[0])[0])[0]
        cmds.textFieldGrp('newNam', e=True, text=firstFile)
                
        updateList("update")
    cmds.textFieldButtonGrp('fileDirect', text='', bl='Find Directory', bc=setFilePath)
    cmds.setParent( '..' )
    
    
    cmds.rowLayout( numberOfColumns=3, columnWidth3=(80, 247, 30))
    cmds.text(l = " File Contains:")
    cmds.textFieldGrp("prefix", text='', cc=updateList)
    cmds.checkBox( "moveOrCopy", label='Copy' )
    cmds.setParent( '..' )
    
    
    cmds.rowLayout( numberOfColumns=4, columnWidth4=(80, 207, 30, 100))
    cmds.text(l =  "      New Name:")
    cmds.textFieldGrp("newNam", w=207, text='', cc=updateList)
    cmds.intFieldGrp("paddedBy", v1=4, w=30, cc=updateList)
    cmds.text(l = " Number Padding")  
    cmds.setParent( '..' )
    
    
    cmds.frameLayout( l="Files Information", borderStyle='in' , bgc = (0,0.518,0) )
    cmds.rowLayout( numberOfColumns=2, columnWidth2=(120, 247))
    cmds.text(l =  "           Sort By:  ")
    cmds.radioButtonGrp( "nameOrDate", numberOfRadioButtons=3, sl=1, labelArray3=['Name', 'Date', 'Frame'] , cc=updateList)
    cmds.setParent( '..' )
    
    cmds.columnLayout()
    
    cmds.paneLayout()
    cmds.textScrollList('filelistNames', numberOfRows=8, w=410, allowMultiSelection=True, showIndexedItem=4 )
    cmds.setParent( '..' )
    cmds.button( label="Rename Files", w=410, bgc=(1,0,0), c=renameFiles )
    cmds.showWindow( windows)

