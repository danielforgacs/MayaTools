### import ford_stabilizer_v0_8_1 as fstab
### reload(fstab)


"""
	---------------------------
	ford_stabilizer_v0_8_1 for Maya
	---------------------------
	v0.8.1
	---------------------------

	daniel forgacs / ford
	forgacs.daniel@gmail.com

	-------------------------------------------------------------------------
	help:	To add a second eye select a camera and press add eye.
			No need to look trough that eye.

	nuke_track_node:	1. select the locator / vertex / transform you want to stabilize in nuke
						2. add the camera to the selection
						3. execute "fstab.nuke_track_node()"
						4. copy paste track node to nuke

						it prints the track node for Nuke in the script editor.
						Nuke handles nodes and scripts from the clipboard.
						copy and paste the node line to Nuke. the nuke track node script
						starts with:

						"Tracker3 { track1 {{curve x1..."

						Works with only one transform selected. You don`t need
						to look through your render camera.

	-------------------------------------------------------------------------

	!!! DO NOT USE with cameras when camera offset is used !!!

	test environment:
		- maya 2011 x64, linux

	changelog:
	12 july 2012	- second eye works.

	11 july 2012	- basic stereo functions added.
						stereo stabiilizes to the center of the 2 eyes view

	05 july 2012	- Stereo started...

	20 june 2012	- nuke track generator bug fixed
						(test camera was left in the code)
					- Nuke track node now gets the frame range
						from render globals

	26 May 2012		- Camera class updated,
						turning stabilizer off
						works without selected camera

	23 May 2012		- new stabilizator, better selection handling
						code cleanup

	21 May 2012		- selection error fiexed:
						works with complicated camera hierarchy

	14 May 2012		- button colour changed,
					- code clean up

	13 May 2012		- code clean up
					- works with zoom lens

	knowns bugs:

	planned	developement:
		- stereo camera offset handling
		- stereo nuke track node

"""

import		maya.cmds	as		cmds
from		math		import	tan, radians
from		maya.mel	import	eval		as	meval

class Camera (object):
	def __init__ (self):
		# get camera from active pane. it must be a modelpanel
		_panel			= cmds.getPanel (withFocus = True)
		_typeOfPanel	= meval ('getPanel -typeOf ' + _panel)

		if _typeOfPanel == 'modelPanel':
			self.transform		= cmds.modelPanel (_panel, query = True, camera = True)
			self.transform		= cmds.ls (self.transform, long = True)[0]

			if cmds.nodeType (self.transform) != 'transform':
				self.transform	= cmds.listRelatives (self.transform, parent = 1)[0]

			self.shape			= cmds.listRelatives (self.transform, shapes = True)[0]
			self.shape			= cmds.ls (self.shape, long = True)[0]
			self.aperture_h		= cmds.camera (self.shape, query = True, horizontalFilmAperture = True)
			self.aperture_v		= cmds.camera (self.shape, query = True, verticalFilmAperture = True)
			self.fieldOfView_h	= cmds.camera (self.shape, query = True, horizontalFieldOfView = True)
			self.fieldOfView_v	= cmds.camera (self.shape, query = True, verticalFieldOfView = True)
		else:
			self.transform	= 'empty'
			self.shape		= 'empty'

	def reset_camera (self):
		cmds.setAttr (self.shape + '.horizontalFilmOffset', 0)
		cmds.setAttr (self.shape + '.verticalFilmOffset', 0)
		cmds.setAttr (self.shape + '.displayResolution', 1)
		cmds.setAttr (self.shape + '.displayFilmGate', 1)
		cmds.setAttr (self.shape + '.panZoomEnabled', 0)
		cmds.setAttr (self.shape + '.horizontalPan', 0)
		cmds.setAttr (self.shape + '.verticalPan', 0)
		cmds.setAttr (self.shape + '.zoom', 1)

def stabilizer (task):
	camera	= Camera()
	camera2	= Camera()
	point	= cmds.ls (selection = True, long = True)

	if task == 'end':
		# turn off stab
		expression		= str (cmds.expression ('stabilizator_expression', string = True, query = True)).split( '\n' )
		cmds.delete( 'stabilizator_expression' )
		camera.shape	= expression[0][2:]
		camera.reset_camera ()

		# check if there`s a second eye
		if cmds.nodeType( expression[1][2:] ) == 'camera':
			camera2.shape	= expression[1][2:]
			camera2.reset_camera ()

		cmds.button ('button_stabilizer',
					edit				= True,
					label				= 'stabilize',
					backgroundColor		= (0, 0.5, 0),
					command				= 'fstab.stabilizer("start")'
					)
		cmds.button( 'Stabilizer|cl|add_eye_btn',
					enable = False,
					edit = True,
					backgroundColor = (0.3, 0.3, 0.3)
					)

	else:
		# start stab
		if cmds.objExists ('stabilizator_expression'):
			# stabilizator exists
			expression		= str (cmds.expression ('stabilizator_expression', string = True, query = True))
			camera.shape	= expression[2:expression.find('#')]
			cmds.delete ('stabilizator_expression')
			cmds.select (camera.shape, replace = True)
			cmds.warning (('>>> STAB WAS TURNED ON. CHECK: ' + camera.shape + ' <<< FOR NONZERO OFFSET VALUES ::..'))

		else:
			if cmds.nodeType (point) != 'mesh' and cmds.nodeType (point) != 'transform' and len (point) == 0:
				# wrong selection
				cmds.warning ('..:: SELECT SOMETHING TO STABILIZE ::..')
			else:
				point = point[0]

				if point != camera.transform and point != camera.shape and camera.transform != 'empty':
					# stabilize
					cmds.setAttr( camera.shape + '.displayResolution', 0)
					cmds.setAttr( camera.shape + '.displayFilmGate', 0)

					expression = '// %s' % camera.shape
					expression += '\n// %s' % point
					expression += '\npython "import maya.cmds as cmds";'
					expression += '\npython "fov_h = cmds.camera (\'%s\', query = True, horizontalFieldOfView = True)";' % camera.shape
					expression += '\npython "fov_v = cmds.camera (\'%s\', query = True, verticalFieldOfView = True)";' % camera.shape
					expression += '\npython "aperture_h = cmds.camera (\'%s\', query = True, horizontalFilmAperture = True)";' % camera.shape
					expression += '\npython "aperture_v = cmds.camera (\'%s\', query = True, verticalFilmAperture = True)";' % camera.shape
					expression += '\n$pos =`python "fstab.get_normalized_screen_position(\'%s\',\'%s\',fov_h, fov_v,aperture_h,aperture_v)"`;' % (point, camera.transform)
					expression += '\nsetAttr "%s.horizontalFilmOffset" $pos[2];' % camera.shape
					expression += '\nsetAttr "%s.verticalFilmOffset" $pos[3];' % camera.shape

					# create expression
					cmds.expression		(name = 'stabilizator_expression', string = expression)

					# update GUI
					cmds.button			('button_stabilizer',
										edit			= True,
										label			="deStabilize",
										backgroundColor	= (1, 0, 0),
										command			= 'fstab.stabilizer("end")')
					cmds.button(		'Stabilizer|cl|add_eye_btn', enable = True, edit = True, backgroundColor = (0, 0.5, 0) )

				else:
					cmds.warning ('..:: CLICK IN THE PANE WITH THE CAMERA ::..')

def add_eye():
	print '#'*50
	ok				= True
	oldExpression	= cmds.expression( 'stabilizator_expression', string = True, query = True ).split( '\n' )
	expression		= [oldExpression[0][3:]]
	selection		= cmds.ls( selection = True, long = True )

	# check selection length
	if len( selection ) != 1:
		cmds.warning( '>>> SELECT THE SECOND CAMERA' )
		ok	= False

	# check if selection is camera
	if ok:
		camera2			= selection[0]
		cameraShape2	= cmds.listRelatives( selection, shapes = True, fullPath = True )[0]

		if cmds.nodeType( cameraShape2 ) == 'camera':
			cmds.warning( '>>> SELECTION IS NOT A CAMERA' )
			expression.append( '// %s' % cameraShape2 )
			offSet_h		= cmds.getAttr( cameraShape2 + '.horizontalFilmOffset')
			offSet_v		= cmds.getAttr( cameraShape2 + '.verticalFilmOffset')
			expression.append( '// %s' % offSet_h )
			expression.append( '// %s' % offSet_v )

		else:
			ok	= False

	print expression
	cmds.button( 'Stabilizer|cl|add_eye_btn', enable = False, edit = True, backgroundColor = (1, 0, 0) )

def get_normalized_screen_position	(point, camera, fieldOfView_h, fieldOfView_v, aperture_h, aperture_v):
	_pointWorldPos = cmds.xform (point, query = True, worldSpace = True, translation = True)
	_camWorldInverseMatrix = cmds.getAttr (camera + '.worldInverseMatrix')

	_posX = _pointWorldPos[0] * _camWorldInverseMatrix[0] + _pointWorldPos[1] * _camWorldInverseMatrix[4] + _pointWorldPos[2] * _camWorldInverseMatrix[8] + 1 * _camWorldInverseMatrix[12]
	_posY =	_pointWorldPos[0] * _camWorldInverseMatrix[1] + _pointWorldPos[1] * _camWorldInverseMatrix[5] + _pointWorldPos[2] * _camWorldInverseMatrix[9] + 1 * _camWorldInverseMatrix[13]
	_posZ = _pointWorldPos[0] * _camWorldInverseMatrix[2] + _pointWorldPos[1] * _camWorldInverseMatrix[6] + _pointWorldPos[2] * _camWorldInverseMatrix[10] + 1 * _camWorldInverseMatrix[14]

	_screenPosX = (_posX / -_posZ) / tan (radians (fieldOfView_h / 2)) / (2.0) + 0.5
	_screenPosY = (_posY / -_posZ) / tan (radians (fieldOfView_v / 2)) / (2.0) + 0.5

	_cameraFilmOffsetX = (_screenPosX - 0.5) * aperture_h
	_cameraFilmOffsetY = (_screenPosY - 0.5) * aperture_v

	# _screenPos is the normalized position in 2D camera space
	# export it to get 2D tracks for compositing softwares
	return [_screenPosX, _screenPosY, _cameraFilmOffsetX, _cameraFilmOffsetY]

def nuke_track_node():
	"""
	creates a nuke track node for the selected transform.
	selection order: trasnform, camera
	"""

	selection	= cmds.ls( selection = True )
	point		= selection[0]
	camera		= selection[1]
	cameraShape	= cmds.listRelatives( shapes = True )[0]
	aperture_h	= cmds.camera( camera, hfa=1, q=1)
	aperture_v	= cmds.camera( camera, vfa=1, q=1)
	trackNode	= 'Tracker3 { track1 {{curve x1 '
	tx			= ''
	ty			= ''
	startframe	= cmds.getAttr( "defaultRenderGlobals.startFrame" )
	endframe	= cmds.getAttr( "defaultRenderGlobals.endFrame" )

	for frame in range( startframe, endframe + 1 ):
		cmds.currentTime( frame )
		fov_h	= cmds.camera( camera, hfv=1, q=1)
		fov_v	= cmds.camera( camera, vfv=1, q=1)
		track	= get_normalized_screen_position( point, camera, fov_h, fov_v, aperture_h, aperture_v )
		tx		+= str( track[0] * 1280 ) + ' '
		ty		+= str( track[1] * 720 ) + ' '

	trackNode += tx + '} {curve x1 ' + ty + '}}}'
	print '#' * 50
	print '>>> tracker node, copy paste to nuke:'
	print trackNode

def gui ():
	try:	cmds.deleteUI ("Stabilizer")
	except: pass

	try:	cmds.windowPref("Stabilizer", remove = True)
	except: pass

	cmds.window( 'Stabilizer',
						sizeable			= True,
						resizeToFitChildren	= True,
						retain				= False,
						topLeftCorner		= (10, 700)
						)
	cmds.columnLayout	('cl')
	cmds.button( 'button_stabilizer',
						label				= "stabilize",
						width				= 120,
						backgroundColor		= (0, 0.5, 0),
						command				= 'fstab.stabilizer("start")'
						)
	cmds.button( 'add_eye_btn',
						enable				= False,
						label				= "add eye",
						width				= 120,
						backgroundColor		= (0.3, 0.3, 0.3),
						command				= 'fstab.add_eye()'
						)
	cmds.showWindow( 'Stabilizer' )

### MAIN ###############################
def main():
	gui()
