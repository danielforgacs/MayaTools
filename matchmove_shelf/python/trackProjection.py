import os, string, fnmatch, re, sys, shutil
import maya.cmds as mc
import maya.mel as mel

###################################################################################
######################## CREATE PROJECTION TEXTURE ################################
###################################################################################

def createMayaTexture():

    global imageDirectory, fileName, start, end, rx, ry

    ##### get head object, image plane and camera #########################
    head = mc.ls(sl=True)[0]
    cams = mc.listCameras(p=True); cams.remove('persp'); cam = cams[0]
    camShape = mc.listRelatives(cams, type='camera')[0]
    imagePlane = mc.listConnections(camShape, type='imagePlane')[0]
    imagePath = mc.getAttr(imagePlane + '.imageName')
    print '\n\nHead object ...', head, '\nRender camera....', cam, '\nImage plane....', imagePlane

    ##### create shader, shading engine, projection, file, 2dtexture #########
    myShader = mc.shadingNode('surfaceShader', n='projectionShader', asShader=True)
    myShaderSG = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name="projectionShaderSG")
    projectionNode = mc.shadingNode('projection', asUtility=True)
    fileNode = mc.shadingNode('file', asTexture=True)
    place2dTexture = mc.shadingNode('place2dTexture', asTexture=True)

    ###### connect objects up ############################################
    mc.connectAttr(myShader + ".outColor", myShaderSG + ".surfaceShader")
    mc.connectAttr(projectionNode + '.outColor' , myShader + '.outColor')
    mc.connectAttr(place2dTexture + '.coverage' , fileNode + '.coverage')
    mc.connectAttr(fileNode + '.outColor',  projectionNode + '.image')
    mc.connectAttr(camShape + '.message' , projectionNode + '.linkedCamera')

    ###### assign shader to head ##############
    mc.select(head)
    mel.eval('sets -e -forceElement '+ myShaderSG + ';')
    print 'assigned...', myShaderSG, '...to ...', head

    ###### set projection node settings #############
    mc.setAttr((projectionNode + '.projType'), 8)
    mc.setAttr((projectionNode + '.fitFill'), 0)

    ###### convert to texture ########################
    for frame in xrange(start, end+1):
        mc.currentTime(frame, e=True)
        seqImageDirname, seqImageBasename = os.path.split(imagePath)
        im = seqImageBasename.split('.')

        if len(im) == 3:
            seqname, padding, ext = im
            paddedBy = len(padding)
            seqImageBasename = seqname +'.' +  str(frame).zfill(paddedBy) + '.' + ext
        seqImageName = os.path.join(seqImageDirname, seqImageBasename)
        mc.setAttr((fileNode + '.fileTextureName'), seqImageName, type ="string")

        newImageName = (imageDirectory + fileName + '.' + str(frame).zfill(4) +'.jpg' )
        file = mc.convertSolidTx(myShader, head, bm='extend', fil="jpg" , rx=rx, ry=ry, fin=newImageName)
        print 'created....', newImageName
        mc.delete(file)

    ##### snap shot of uv's ############################
    uvfilePath = (imageDirectory + fileName + "UVs.jpg")
    mc.uvSnapshot( o=True, n=uvfilePath, ff="jpg", xr=rx, yr=ry )
    mel.eval('sets -e -forceElement initialShadingGroup;')

    ###### remove the shader, shading engine, projection, file, 2dtexture #########
    mc.delete(myShader); mc.delete(myShaderSG); mc.delete(projectionNode); mc.delete(fileNode); mc.delete(place2dTexture)

###################################################################################
############################# MIAIN PROCESS #######################################
###################################################################################

def makeProjectionTexture():
    global imageDirectory, fileName, start, end, rx, ry

    imageDirectory = mc.textFieldButtonGrp("outputPBfile",q=True,text=True) + '/'
    fileName =  mc.textFieldGrp("imageName",q=True,text=True)
    print 'OUTPUT DIRECTORY:' ,imageDirectory
    print 'IMAGE NAME:', fileName

    res = mc.optionMenuGrp("outputSize", q=True, v=True)
    if not res == "Custom":
        ry = int(res.split('x')[0])
        rx = int(res.split('x')[1])
    if res == "Custom":
        ry = mc.intFieldGrp("customHW", q=True, value1=True)
        rx = mc.intFieldGrp("customHW", q=True, value2=True)
    print 'HEIGHT:', ry, 'WIDTH:', rx

    frames = mc.intFieldGrp("frameRange",q=True,v=True)
    start = frames[0]; end = frames[1]
    print 'START:', start, 'END:', end
    origStart = start

    if mc.ls(sl=True) == []:
        print "nothing selected!"

    if not mc.ls(sl=True) == []:
        createMayaTexture()
        print 'files saved to ', imageDirectory

    ###### open sequence and UV comped over #########

    if mc.window("projectTextureWindow", exists=True):
        mc.deleteUI("projectTextureWindow", window=True)

    window = mc.window( title="Created Projection UVs" )
    mc.columnLayout( adjustableColumn=True )
    mc.text( label=('Created Projections in ' + imageDirectory))
    mc.button( label='OK', w=500, command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( window )

##############################################################################
######################### enable custom ######################################
##############################################################################

def changeRes(test):
    res = mc.optionMenuGrp("outputSize", q=True, v=True)
    if fnmatch.fnmatch("Custom", res):
        mc.intFieldGrp( "customHW", e=True, en=True )
    if not fnmatch.fnmatch("Custom", res):
        mc.intFieldGrp( "customHW",e=True, en=False )

##############################################################################
################################ CREATE WINDOW ###############################
##############################################################################

def createProjectionUI():

    fileName = mc.file( query=True, sn=True, shn=True).split('.')[0]
    imageDirectory = mc.workspace(q=True, fullName=True) + '/images'
    start = mc.playbackOptions( q=True, min=True )
    end = mc.playbackOptions( q=True, max=True )
    res = ''


    if mc.window("projectTextureWindow", exists=True):
        mc.deleteUI("projectTextureWindow", window=True)
    window = mc.window("projectTextureWindow")


    mc.window("projectTextureWindow", edit=True,  resizeToFitChildren=True, sizeable=True, title="Projection Creator v0.7.1", widthHeight=[650, 250])
    mc.formLayout("mainFormLayout", nd=100)
    mc.scrollLayout("mainScrollLayout", horizontalScrollBarThickness=0)
    mc.columnLayout(adjustableColumn=True, columnAttach=("both", 4))
    mc.setParent ('..')
    mc.frameLayout("playblastQT", label="File Information", borderStyle="etchedIn", w=616, labelVisible=True, borderVisible=True, collapsable=False, en=True, cl=False)



    def doSetOutputFile():
        playblastFile = mc.fileDialog2(fileMode=3, caption="Save Quicktime", okc='Accept', dialogStyle=2)
        mc.textFieldGrp("outputPBfile",e=True,text=playblastFile[0])
    mc.textFieldButtonGrp("outputPBfile", height=22, cl3=("right" , "left", "left"), cw3=(80 , 500,20), label="Output Dir: ",
    buttonLabel="...",it=imageDirectory,  bc=doSetOutputFile,  annotation="Set the output directory")
    mc.rowLayout( numberOfColumns = 2, cw2 = (220, 175))
    mc.setParent ('..')


    ############################# set output from input ######################################
    mc.textFieldGrp("imageName", height=22, cl3=("right" , "left", "left"), cw3=(80 , 500,20), label="Images Name: ", it=fileName)
    mc.rowLayout( numberOfColumns = 2, cw2 = (220, 175))
    mc.setParent ('..')


    ################################## codec settings ########################################
    mc.frameLayout(label="FrameRange" , borderStyle="etchedIn" , w=616, labelVisible=True , borderVisible=True , collapsable=False)
    mc.rowLayout( numberOfColumns = 2, cw2 = (70, 75))
    mc.text(label="")
    mc.intFieldGrp("frameRange", numberOfFields=2, cw2=(20 , 20), label='Start / End:',  value1=start, value2=end )
    mc.setParent ('..')


    ################################# output size ############################################
    mc.frameLayout(label="Output Size" , borderStyle="etchedIn" ,  w=616, labelVisible=True , borderVisible=True , collapsable=False)
    mc.rowLayout( numberOfColumns = 3, cw3 = (40, 15, 100))
    mc.text(label="")
    mc.optionMenuGrp("outputSize", cc=changeRes, l="Output Size: ", cw2=(77, 180), w=195)
    sizeList =("4096x4096","2048x2048", "1024x1024", "512x512","256x256","Custom")
    for size in sizeList:
        mc.menuItem (label=size)
    mc.optionMenuGrp("outputSize", e=True, v="1024x1024")
    mc.intFieldGrp("customHW", numberOfFields=2, label='Height/Width:', value1=1024, value2=768, en=0 )
    mc.setParent ('..')


    ####################################################################################################

    mc.setParent ('..')
    mc.setParent ('..')
    mc.setParent ('..')
    mc.setParent ('..')
    mc.setParent ('..')
    mc.setParent ('..')
    mc.setParent ('..')

    mc.columnLayout("buttonColumnLayout", adj=True , columnAttach=("both" , 4) , rowSpacing=4)
    mc.rowLayout (numberOfColumns=3 , cw=(20, 145) , cl3=("center" , "center" , "center"), cat=(2 , "right" , 0), adj=2)
    mc.text(label="" , width=5 , height=26 )
    mc.button (label="Create Image Sequence" , width=175 , height=26 , annotation="Creates the image file" , command="trackProjection.makeProjectionTexture()")
    mc.setParent ('..')
    mc.setParent ('..')


    mc.formLayout ("mainFormLayout",e= True, af = ("buttonColumnLayout", "bottom", 0))
    mc.formLayout ("mainFormLayout",e= True, af = ("buttonColumnLayout", "left", 2))
    mc.formLayout ("mainFormLayout",e= True,af = ("buttonColumnLayout" , "right" , 2))
    mc.formLayout ("mainFormLayout",e= True,ac = ("mainScrollLayout" , "bottom", 0, "buttonColumnLayout"))
    mc.formLayout ("mainFormLayout",e= True,af = ("mainScrollLayout", "top" ,5))
    mc.formLayout ("mainFormLayout",e= True,af = ("mainScrollLayout", "left", 5))
    mc.formLayout ("mainFormLayout",e= True,af = ("mainScrollLayout" , "right" , 5))
    mc.showWindow("projectTextureWindow")

