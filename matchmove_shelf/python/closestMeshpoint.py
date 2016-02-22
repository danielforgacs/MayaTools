#!/usr/bin/python2.6
# closestMeshpoint
# DLowenberg Mar 05, 2012
# v1.3


version = 'closestMeshpoint from maya v1.42'
print 'version= %s' %version

import sys
import os
import subprocess
import maya.OpenMaya as om
import maya.cmds as cmds
import math
import maya.mel as mel
import pymel.core as pm
from functools import partial


class LocIntersect():
    def __init__(self):
        self.rb1 = self.rb2 = self.rb3 = self.collection1 = ''
        self.sf_TextField = self.ef_TextField = ''
        self.mesh_list= list()
        self.loc_list = list()
        self.savedSel = list()

    def singleIntersect(self,cam):
        print ' '
        print 'mesh list is %s' %self.mesh_list
        positionDict ={}

        #Camera get Positon
        camPosition = cmds.xform (cam,q=1, ws=1, t=1)
        print 'camPosition is %s' %camPosition

        for mesh in self.mesh_list:
            '''
            connections = cmds.listConnections(mesh)
            for connection in connections:
                if cmds.objectType(connection)=='displayLayer':
                    if (cmds.getAttr(connection +'.visibility') ==1):
            '''
            parentofMesh=cmds.listRelatives(mesh,p=True, pa=True)
            if cmds.getAttr(parentofMesh[0] + ".visibility") ==True:
                    #print 'visbile mesh = %s' %parentofMesh[0]
                    traceMesh = mesh
                    useSmoothMesh = False
                    if cmds.getAttr(mesh+'.displaySmoothMesh') != 0:
                        useSmoothMesh = True
                        traceMesh = cmds.createNode('mesh', name='closestMeshpointTempMesh', parent=parentofMesh[0])
                        cmds.connectAttr(mesh+'.outSmoothMesh', traceMesh+".inMesh")
                    for item in self.loc_list:
                        print '\nLocator is %s : mesh is %s' %(item,mesh)
                        loc = item
                        loc_pos = cmds.xform (loc,q=1, ws=1, t=1)
                        #print '%s loc_pos is %s' %(loc,loc_pos)

                        rayDir = (float(loc_pos[0])-float(camPosition[0]),float(loc_pos[1])-float(camPosition[1]),float(loc_pos[2])-float(camPosition[2]))
                        #print 'rayDir is %s %s %s' %(rayDir[0],rayDir[1],rayDir[2])

                        new_pos = self.findMeshIntersection(traceMesh, camPosition, rayDir)
                        #print '\npositionDict is %s' %positionDict
                        if new_pos !=None:
                            if not positionDict.has_key(loc) :
                                positionDict[loc] = new_pos
                                print '%s %s added to Dict' %(loc,new_pos)
                            else:
                                newDistance=self.get_distance(camPosition,new_pos)
                                oldDistance=self.get_distance(camPosition,positionDict[loc])
                                if (newDistance < oldDistance):
                                    positionDict[loc] = new_pos
                                    print 'UPDATE positionDict is %s' %positionDict
                                else:
                                    print '%s %s Not added to Dict' %(loc,new_pos)
                        else:
                            print 'No intersection'
                    # Delete temporary smoothed mesh.
                    if useSmoothMesh:
                        cmds.delete(traceMesh)
            else:
                print '%s is not visible' % parentofMesh[0]
                
        print '\npositionDict is %s' %positionDict
        for loc,new_pos in positionDict.iteritems():
            print 'Moved locator %s to %s' %(loc,new_pos)
            cmds.xform(loc, t=new_pos, ws=True)
            cmds.setKeyframe( loc, at='translate')
        cmds.select(self.savedSel, replace=True)


        

    def findMeshIntersection(self,meshName, raySource, rayDir):
    	print 'meshName:%s'%meshName
        #       Create an empty selection list.
        selectionList = om.MSelectionList()

        #       Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #       Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #       Get the first item on the selection list (which will be our mesh)
        #       as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #       Create an MFnMesh functionset to operate on the node pointed to by
        #       the dag path.
        meshFn = om.MFnMesh(meshPath)

        #       Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint(raySource[0], raySource[1], raySource[2])

        #       Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector(rayDir[0], rayDir[1], rayDir[2])

        #       Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #       Set up a variable for each remaining parameter in the
        #       MFnMesh::closestIntersection call. We could have supplied these as
        #       literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 1000.0
        bothDirections = False
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #       Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #       Return the intersection as a Pthon list.
        if gotHit:
                print 'hitpoint is %s %s %s' %(hitPoint.x, hitPoint.y, hitPoint.z)
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None


    def get_distance(self,from_position,to_position):
        fX = from_position[0]
        fY = from_position[1]
        fZ = from_position[2]
        tX = to_position[0]
        tY = to_position[1]
        tZ = to_position[2]
        dX = tX - fX
        dY = tY - fY
        dZ = tZ - fZ
        distanceSquared = (dX * dX) + (dY * dY) + (dZ * dZ)
        distance = math.sqrt (distanceSquared)
        return distance

    def runClosestPoint(self,*args):

    	self.savedSel = cmds.ls(sl=True, long=True)

        #what is current camera?
        lookingThru = cmds.lookThru( q=True )
        #print lookingThru
        #print cmds.objectType (lookingThru)
        if (cmds.objectType (lookingThru) =="transform"):
            camShapes = cmds.listRelatives(lookingThru, path=True)
            camShape = camShapes[0]
        else:
            camShape=lookingThru
        
        print 'looking thru %s' %camShape

        # check it is a camera
        if camShape !=None:
            obj = str(cmds.objectType(camShape))
            print 'selected object is %s' %obj
        else:
            obj=''

        if (len(lookingThru)==0) or (obj != 'camera') or (obj==''):
            cmds.warning ('no camera looking thru')
            sys.exit()

        #if current camera contains the word "Shape", select its parent instead
        if lookingThru.find("Shape") != -1:
            lookingThruDad = cmds.listRelatives(lookingThru, p=True, path=True)
            lookingThru = lookingThruDad[0]
            print 'transform is %s' %lookingThru


        selected_nodes = cmds.ls(sl=True, l = True, type='transform')

        # if len(selected_nodes) > 0:
        #   loc_list = selected_nodes
        #   print 'Checking selected locators ...\n %s' %loc_list
        # else:
        #   print 'nothing selected'
        #   sys.exit()

        print "SELECTION is %s" % selected_nodes

        for node in selected_nodes:
            historyShape = cmds.listHistory(node)[0]
            tmpList=  historyShape.split('|')
            shapeNode = node+'|'+tmpList[len(tmpList)-1]
            print "SHAPE is %s" % shapeNode
            if cmds.nodeType(shapeNode) == 'locator':
                self.loc_list.append(node)
            elif cmds.nodeType(shapeNode) == 'mesh':
                self.mesh_list.append(shapeNode)

        # mesh_list=cmds.ls (type="mesh")

        stFrm = enFrm = 0
        sel = cmds.radioCollection(self.collection1,q = True,sl = True)
        if sel == self.rb1.split('|')[-1]:
            stFrm = int(cmds.intField(self.sf_TextField,q = True,v = True))
            enFrm = int(cmds.intField(self.ef_TextField,q = True,v = True))
            for i in range(stFrm, enFrm):
                cmds.currentTime(i)
                self.singleIntersect(lookingThru)  
        elif sel == self.rb2.split('|')[-1]:
            stFrm = int(cmds.playbackOptions( q = True,min = True ))
            enFrm = int(cmds.playbackOptions( q = True,max = True ))+1
            for i in range(stFrm, enFrm):
                cmds.currentTime(i)
                self.singleIntersect(lookingThru)  
        elif sel == self.rb3.split('|')[-1]:
            self.singleIntersect(lookingThru)
            print "single"
    def closestMeshpointGui(self):
        if cmds.window("closestMeshpointGui",exists = True):
            cmds.deleteUI("closestMeshpointGui")
        if(cmds.windowPref( 'closestMeshpointGui', exists=True )):
            cmds.windowPref( 'closestMeshpointGui', remove=True )
        _mainWindow = cmds.window("closestMeshpointGui",title="Project locator on mesh v1.42",widthHeight=(400, 223))
        cmds.columnLayout(adj = True)
        cmds.frameLayout( label='Help', borderStyle='out',collapsable = True)
        helpStr = "This tool raytrace projects a locator from the camera, onto a polygon(closest point on mesh)\n"+\
        "It is mainly intended to take 2.5D tracks from 3D Equalizer,etc, into Maya, for rotomation\n"+\
        "1. Select locator(s) that you wish to project, plus polygon to project onto\n"+\
        "2. Right click on view port of camera that you wish to project onto polygon through\n"+\
        "3. Select appropriate radio button for frame range"
        cmds.scrollField( editable=False, wordWrap=True, h = 120,text=helpStr )
        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 10), columnWidth=[(1, 120), (2, 120)])
        self.collection1 = cmds.radioCollection()
        self.rb1 = cmds.radioButton( label='Frame Range' )
        self.rb2 = cmds.radioButton( label='From Timeline' )
        self.rb3 = cmds.radioButton( label='Current Frame' )
        cmds.setParent('..')
        cmds.radioCollection( self.collection1, edit=True, select=self.rb1 )
        cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'left', 10), columnWidth=[(1, 120), (2, 120)])
        cmds.text( label='Start' )
        cmds.text( label='End' )
        self.sf_TextField = cmds.intField()
        self.ef_TextField = cmds.intField()
        cmds.setParent('..')
        cmds.button( label='Do it',command = self.runClosestPoint)
        cmds.setParent('..')
        cmds.showWindow( _mainWindow )
        onCmd = "import maya.cmds as cmds\ncmds.intField(\""+self.sf_TextField+"\",edit = True,enable = True)\ncmds.intField(\""+self.ef_TextField+"\",edit = True,enable = True)"
        offCmd = "import maya.cmds as cmds\ncmds.intField(\""+self.sf_TextField+"\",edit = True,enable = False)\ncmds.intField(\""+self.ef_TextField+"\",edit = True,enable = False)"
        cmds.radioButton( self.rb1,edit = True ,onCommand = onCmd,offCommand = offCmd)
        cmds.window("closestMeshpointGui",edit = True, widthHeight=(400, 223))
