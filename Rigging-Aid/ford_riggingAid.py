#	-----------------------------------
#	ford_riggingAid.py	- v0.6.2
#	ford_riggingAid_v0.6.2
#	-----------------------------------
#	daniel.forgacs
#	forgacs.daniel@gmail.com
#	daniel.forgacs@gmail.com
#	-----------------------------------
#
#	usage	-	1) put the script in a location which is in your PYTHONPATH environmental variable to let maya see the script, or add the path where the script is to your
#				maya.env file with the "PYTHONPATH" environmental variable
#				2) copy the icons in the maya preferences "icon" folder. If maya doesn`t find icons you have to set the icon path environmental variable. Search maya help for that.
#				3) source the script in a python tab in the script editor: import ford_riggingAid as fra
#				4) call GUI procedure: fra.rigAidGUI ()
#	-----------------------------------------------------------------------------------------------
#
#	description:
#		- creates and if geo/transform is selected snaps NURBS rig control icons. Controls are put in the "anim_control_set" quick selection set to
#			make it easy to select them in later use. All controls are single NURBS curves.
#		- if something is selected, controls are renamed after the selected object. If not, a general control name is given to the control
#		- controls are created with an offset group. The controls have zero transform values and the group`s name is the control`s name + "offSet"
#		- offset groups and controls can be transformed along any axis with 90 degree to fit into proper orientation. Direction selection determeines
#			wheather the control`s offset group should be rotated with -90 or +90 degrees
#		- objects can be convert into a control by selecting the object and an object to be controlled
#		- all rig controls can be zeroed out by pressing the zero button
#		- boneBreaker: creates a new joint between two joint exactly in the middle - the parent joint`s x axis should be oriented towards it`s child.
#		- one button selection for selected joint`s local rotation axis
#		- ford_createControlCurveCommand (): prints the single python command to create the selected curve created with any complex method
#	-----------------------------------------------------------------------------------------------
#
#	changeLog: 
#		2009. 01. 17.	- setup frame added, ribbon spine added
#		2009. 01. 17.	- new GUI and script cleanUp, boneBraker now works in all direction, number of bones can be choosen via the slider from 1 to 10,
#					there are now 2 locators: normal and NURBS, curve command display is now formatted
#		2009. 01. 17.	- new gui finished, full script cleanUp. Beacuse icons seem to be slow, and takes too much place, icons are dismissed
#		2009. 01. 17.	- GUI for ford_createControlCurveCommand () added
#		2009. 01. 15.	- script cleanUp, ford_controlPostProcess() added to all control creation functions
#		2009. 01. 13.	- ford_createControlCurveCommand added
#		2009. 01. 12.	- Linux window resizeing bug solved
#					- script cleanup
#					- ford_controlPostProcess added, script needs further cleanup
#		2009. 01. 11.	- orientation controls changed to ford_smartOrient
#					- ford_jointOrient deleted, use ford_smartOrient instead
#					- ford_orientControl deleted, use ford_smartOrient instead
#					- ford_smartOrient GUI added
#		2009. 01. 07.	- annotations added
#					- non single curve 4 arrowHead control removed
#					- auto delete windowPrefs if window doesn`t exists
#		2009. 01. 07.	- script cleanup,
#					- radioButtons added to select control offset group orientation direction
#		2009. 01. 06.	- script cleanup, 
#					- fixed: window width bug on linux
#					- fixed: control axis orientation selection error
#					- fixed: boneBreaker selection error
#		2009. 01. 01.	- ... and it all begins
#	-----------------------------------------------------------------------------------------------
#
#	known bugs:
#		- on calling ford_createControlCurveCommand () with empty selection
#			the handled exception deletes the window which calls ford_createControlCurveCommand
#			raising a maya error
#	-----------------------------------------------------------------------------------------------
#
#	test environment:
#		maya2009, winXP-32 SP3
#	-----------------------------------------------------------------------------------------------
#
#	planned development:
#		- choosable colour for rig controls, - choosable qick select sets and names, - autoDisplay scriptjob start / stop, - more flexible boneBreaker
# ______________________________________________________________________________

import	maya.cmds	as		cmds
import	maya.mel	as		mm
from	types		import	*

# main GUI
def	main	():
	# GUI variables
	symBtnWidth			=	36
	btnHeight			=	20
	gridCols			=	3
	winWidth			=	symBtnWidth	*	gridCols

	# check main GUI element existence
	if	cmds.window	('rigAid_window',	exists	=	True):	cmds.showWindow	('rigAid_window')
	
	else:
		# check template existences
		if	cmds.uiTemplate	('template_window',		exists	=	True):	cmds.deleteUI	('template_window',		uiTemplate	=	True)
		if	cmds.uiTemplate	('template_column',		exists	=	True):	cmds.deleteUI	('template_column',		uiTemplate	=	True)
		if	cmds.uiTemplate	('template_frame',		exists	=	True):	cmds.deleteUI	('template_frame',		uiTemplate	=	True)
		if	cmds.uiTemplate	('template_button',		exists	=	True):	cmds.deleteUI	('template_button',		uiTemplate	=	True)
		if	cmds.uiTemplate	('template_radioBtn',	exists	=	True):	cmds.deleteUI	('template_radioBtn',	uiTemplate	=	True)
		if	cmds.uiTemplate	('template_row',		exists	=	True):	cmds.deleteUI	('template_row',		uiTemplate	=	True)
		if	cmds.uiTemplate	('template_grid',		exists	=	True):	cmds.deleteUI	('template_grid',		uiTemplate	=	True)
		if	cmds.uiTemplate	('template_symButton',	exists	=	True):	cmds.deleteUI	('template_symButton',	uiTemplate	=	True)
		if	cmds.uiTemplate	('template_separator',	exists	=	True):	cmds.deleteUI	('template_separator',	uiTemplate	=	True)

		# create GUI templates
		cmds.uiTemplate		('template_window')
		cmds.uiTemplate		('template_column')
		cmds.uiTemplate		('template_frame')
		cmds.uiTemplate		('template_button')
		cmds.uiTemplate		('template_radioBtn')
		cmds.uiTemplate		('template_row')
		cmds.uiTemplate		('template_grid')
		cmds.uiTemplate		('template_symButton')
		cmds.uiTemplate		('template_separator')
		
		# define GUI templates
		cmds.window			(defineTemplate	=	'template_window',	sizeable	=	False,	toolbox	=	True,	resizeToFitChildren	=	True)
		cmds.columnLayout	(defineTemplate	=	'template_column')
		cmds.frameLayout	(defineTemplate	=	'template_frame',	borderVisible	=	True,	borderStyle	=	'etchedOut',
							collapsable	=	True,	preCollapseCommand	=	'cmds.window ( \'rigAid_window\', edit=1, height=1)')
		cmds.rowLayout		(defineTemplate	=	'template_row')
		cmds.gridLayout		(defineTemplate	=	'template_grid')
		cmds.symbolButton	(defineTemplate	=	'template_symButton',	width	=	symBtnWidth,
							height	=	symBtnWidth,	image	=	'ford_riggingAid__shelf.xpm')
		cmds.button			(defineTemplate	=	'template_button',	width	=	winWidth,	height	=	btnHeight,	align	=	'left',
							actOnPress	=	True)
		cmds.radioButton	(defineTemplate	=	'template_radioBtn',	align	=	'left',	recomputeSize	=	True)
		cmds.separator		(defineTemplate	=	'template_separator',	width	=	winWidth,
							height	=	2,	style	=	'in',	horizontal	=	True)

		# GUI layout
		cmds.window			('rigAid_window',	title	=	'ford`s rigAid',	useTemplate	=	'template_window',	retain	=	True)
		cmds.columnLayout	('master_column',	useTemplate	=	'template_column')
		cmds.frameLayout	('showHide_frame',	label	=	'showHide',	borderVisible	=	False,	useTemplate	=	'template_frame')
		cmds.columnLayout	('main_column',	useTemplate	=	'template_column')
		cmds.frameLayout	('frame_creation',	label	=	'creation',	useTemplate	=	'template_frame')
		cmds.columnLayout	('column_creation',	useTemplate	=	'template_column')
		cmds.gridLayout		('grid_creation',	useTemplate	=	'template_grid',	numberOfColumns	=	gridCols,
												cellWidthHeight	=	(symBtnWidth,	symBtnWidth))
		cmds.setParent		('main_column')
		cmds.frameLayout	('frame_orientation',	label	=	'orientation',	useTemplate	=	'template_frame')
		cmds.columnLayout	('column_orientation',	useTemplate	=	'template_column')
		cmds.gridLayout		('grid_orientButtons',	useTemplate	=	'template_grid',	numberOfColumns	=	2,
													cellWidthHeight	=	(winWidth	/	2,	symBtnWidth))
		cmds.setParent		('column_orientation')
		cmds.gridLayout		('grid_selectAxis',	useTemplate	=	'template_grid',	numberOfColumns	=	3,
												cellWidthHeight	=	(winWidth	/	3,	20))
		cmds.setParent		('main_column')
		cmds.frameLayout	('frame_control',	label	=	'control',	useTemplate	=	'template_frame')
		cmds.columnLayout	('column_control',	useTemplate	=	'template_column')
		cmds.setParent		('main_column')
		cmds.frameLayout	('frame_setup',	label	=	'setup',	useTemplate	=	'template_frame')
		cmds.columnLayout	('column_setup',	useTemplate	=	'template_column')

# >>> creation buttons <<< _______________________________________________________________________________________
		cmds.separator		(useTemplate	=	'template_separator'	)
		
		cmds.setParent		('grid_creation'	)
		cmds.setUITemplate	('template_symButton',	pushTemplate	=	True	)

		cmds.symbolButton	(command	='fra.create2Arrowhead()',			image	=	'ford_riggingAid__create2Arrowhead.xpm'	)
		cmds.symbolButton	(command	='fra.create4Arrowhead()',			image	=	'ford_riggingAid__create4Arrowhead.xpm'	)
		cmds.symbolButton	(command	='fra.createSphere()',				image	=	'ford_riggingAid__createSphere.xpm'	)
		cmds.symbolButton	(command	='fra.createNURBScube()',			image	=	'ford_riggingAid__createNURBScube.xpm'	)
		cmds.symbolButton	(command	='fra.createCircle()',				image	=	'ford_riggingAid__createCircle.xpm'	)
		cmds.symbolButton	(command	='fra.createSpherical4Arrowhead()',	image	=	'ford_riggingAid__createSpherical4Arrowhead.xpm')
		cmds.symbolButton	(command	='fra.createNURBSlocator()',		image	=	'ford_riggingAid__createNURBSlocator.xpm')
		cmds.symbolButton	(command	='fra.createLocator()',				image	=	'ford_riggingAid__createLocator.xpm'	)
		cmds.symbolButton	(command	='fra.createPiramyd()',				image	=	'ford_riggingAid__createPiramyd.xpm'	)
		cmds.symbolButton	(command	='fra.createCircle1Arrowhead()',	image	=	'ford_riggingAid__createCircle1Arrowhead.xpm')
		
		#
		cmds.setParent		(	'column_creation'	)
		cmds.setUITemplate	(	'template_button',	pushTemplate	=	True	)
		cmds.separator		(	useTemplate	=	'template_separator'	)
		cmds.button			(	label		=	'   convert2control',	command	=	'fra.convertToControl	()'	)
		cmds.separator		(	useTemplate	=	'template_separator'	)
		cmds.button			(	label		=	'   command4curve',		command	=	'fra.createCurveCommand	()'	)
		
# >>> orientation button / options <<< ________________________________________________________________________________

		#
		cmds.setParent		(	'grid_orientButtons'	)
		cmds.setUITemplate	(	'template_symButton',	pushTemplate	=	True	)
		cmds.symbolButton	(	'orientMinusButton',	command	=	'fra.smartOrient	(\'minus\')',	width	=	winWidth	/	2,
								image	=	'ford_riggingAid__orientXminus.xpm'	)
		cmds.symbolButton	(	'orientPlusButton',		command	=	'fra.smartOrient	(\'plus\')',	width	=	winWidth	/	2,
								image	=	'ford_riggingAid__orientXplus.xpm'	)

		#
		cmds.setParent		(	'grid_selectAxis'	)
		cmds.setUITemplate	(	'template_radioBtn',	pushTemplate	=	True	)
		
		cmds.radioCollection(	'radioCollection_axis'			)
		cmds.radioButton	(	'X',		label	=	'X',		select	=	True,
								onCommand	=	'fra.setButtonIcon	()'	)
		cmds.radioButton	(	'Y',		label	=	'Y',		
								onCommand	=	'fra.setButtonIcon	()'	)
		cmds.radioButton	(	'Z',		label	=	'Z',
								onCommand	=	'fra.setButtonIcon	()'	)
		
		#
		cmds.setParent		(	'column_orientation'	)
		cmds.separator		(	useTemplate	=	'template_separator'	)
		cmds.checkBox		(	'check_keepShape',	label	=	'keepShape',	align	=	'left',	changeCommand	=	'fra.setButtonIcon	()'	)

# >>> control buttons <<< ________________________________________________________________________________________
		cmds.setUITemplate		(	'template_button',				pushTemplate	=	True	)
		cmds.setParent			(	'column_control'				)
		cmds.separator			(	useTemplate	=	'template_separator'	)
		cmds.intSlider			(	'boneNum',
									width		=	winWidth,
									minValue	=	1,
									maxValue	=	10,
									value		=	1,
									dragCommand	=	
									'''cmds.button	(	'button_boneBreaker',
														edit	=	True,
														label	=	'bone breaker #'	+
																	str	(	cmds.intSlider (	'boneNum',	
																								query=1, 
																								value=1)	),
														width	=	'''	+	str	(	winWidth	)	+	''')'''	)
																					
		cmds.button				(	'button_boneBreaker',	
									label	=	'   bone breaker #' + str	(	cmds.intSlider ('boneNum', query=1, value=1)	),
									command	=	'fra.splitJoint		()'	)
		cmds.separator			(	useTemplate	=	'template_separator'	)
		cmds.button				(	label			=	'   zero all',		command	=	'fra.resetControls	()'	)
		cmds.button				(	label			=	'   select LRA',	command	=	'fra.selectLRA		()'	)
		cmds.button				(	label			=	'   hide LRA',		command	=	'fra.hideLRA		()'	)

# >>> control buttons <<< ________________________________________________________________________________________
		cmds.setParent			(	'column_setup'						)

		cmds.separator			(	useTemplate	=	'template_separator'	)
		cmds.button				(	label	=	'   ribbon',	command	=	'fra.setupRibbon	()'	)
		cmds.button				(	label	=	'   strechy',	command	=	'fra.setupStrechy	()'	)
		

# >>> show GUI <<< _______________________________________________________________________________________________
		cmds.showWindow			(	'rigAid_window'	)

# _____________________________________________________________________________________________________
#	<<< function library >>>
# ________________________________________________________________________________________________________

# >>>	setButtonIcon
def	setButtonIcon	():
	_width			=	cmds.gridLayout			(	'grid_selectAxis',		query	=	True,	width	=	True	)
	_axis			=	cmds.radioCollection	(	'radioCollection_axis',	query	=	True,	select	=	True	)
	_keepShape		=	cmds.checkBox			(	'check_keepShape',		query	=	True,	value	=	True	)
	
	if	_keepShape:	_keepShape	=	'KeepShape'
	else:			_keepShape	=	''
	
	cmds.symbolButton		(	'orientMinusButton',	edit	=	True,	width	=	_width	/	2,
								image	=	'ford_riggingAid__orient'+_axis+'minus'+_keepShape+'.xpm'	)
	cmds.symbolButton		(	'orientPlusButton',		edit	=	True,	width	=	_width	/	2,
								image	=	'ford_riggingAid__orient'+_axis+'plus'+_keepShape+'.xpm'	)

# >>> selects selected joints Local Rotation Axis, deselects non joint objects <<< __________________________________
def	selectLRA	():
	_selection		=	cmds.ls		(	selection	=	True	)
	cmds.select						(	clear		=	True	)
	
	for	_obj	in	_selection:
		if	(	cmds.nodeType	(	_obj	)	==	'joint'	):
			try:	cmds.select	(	_obj	+	'.rotateAxis',	add	=	True	)
			except	TypeError:	continue

# >>> Hides all visible Local Axis <<< ____________________________________________________________________
def	hideLRA	():
	_selCurrent		=	cmds.ls	(	selection		=	True,	long		=	True	)
	cmds.select 				(	allDagObjects	=	True,	hierarchy	=	True,	add	=	True	)
	_selList 		= 	cmds.ls	(	selection		=	True,	long		=	True	)

	for	_k	in	_selList:
		try:
			cmds.setAttr	(	_k	+	'.displayLocalAxis',	0	)
		except	RuntimeError:	continue

	if len(_selCurrent) > 0:	cmds.select	(	_selCurrent,	replace	=	True	)
	else:						cmds.select	(					clear	=	True	)

# >>> splits bone <<< __________________________________________________________________________________________
#			print; print; print '>>> SO FAR SO GOOD'; print # <<< DEBUG ONLY LINE, CAN BE DELETED <<< ##########
def	splitJoint	():
	_newBoneNum	= cmds.intSlider	('boneNum',	query	= 1,	value	= 1)
	_bone		= cmds.ls	(selection	= 1,	long	= 1)
	_childJoint	= cmds.listRelatives	(children	= 1)

	if (len (_bone)	> 0) and (type(_childJoint) is not NoneType) \
	and (cmds.nodeType(_bone[0]) == 'joint') and (cmds.nodeType(_childJoint) == 'joint'):
		
		_childTranslateX	=	cmds.getAttr	(	_childJoint[0]	+	'.translateX'	)
		_childTranslateY	=	cmds.getAttr	(	_childJoint[0]	+	'.translateY'	)
		_childTranslateZ	=	cmds.getAttr	(	_childJoint[0]	+	'.translateZ'	)

		_newX				=	_childTranslateX	/	(	_newBoneNum	+	1.0	)
		_newY				=	_childTranslateY	/	(	_newBoneNum	+	1.0	)
		_newZ				=	_childTranslateZ	/	(	_newBoneNum	+	1.0	)

		for	_k	in	range	(	_newBoneNum):
			_bone	=	cmds.insertJoint	(	_bone	)
			cmds.toggle	(localAxis		=1)
			cmds.xform	(_bone	+	'.scalePivot',	_bone	+	'.rotatePivot',
						relative	=	1,	objectSpace	=	1,	translation	=	(	_newX,	_newY,	_newZ	)	)

		for	_k	in	range	(	_newBoneNum	):	cmds.pickWalk	(	direction	=	'up'	)
	
	else:	raiseWarning	(	'select a bone! You can do it!'	)

# resets all controls in the anim_control_set to their initial state <<< __________________________________
def	resetControls	():
	if	(	cmds.objExists	(	'anim_control_set'	)	==	True	):
		cmds.select		(	'anim_control_set',	replace	=	True	)
		cmds.xform		(	translation	=	(	0,	0,	0),
							rotation	=	(	0,	0,	0)	)

# >>> locks scale and visibility and hides in channel box <<< _____________________________________________________
def	lockHideAttributes	(	_node	):	# <<< string
	cmds.setAttr	(	_node	+	'.scaleX',		keyable	=	False,	channelBox	=	False	)
	cmds.setAttr	(	_node	+	'.scaleY',		keyable	=	False,	channelBox	=	False	)
	cmds.setAttr	(	_node	+	'.scaleZ',		keyable	=	False,	channelBox	=	False	)
	cmds.setAttr	(	_node	+	'.visibility',	keyable	=	False,	channelBox	=	False	)

# >>> postprocess created control <<< ___________________________________________________________________________
def	postProcessControl	(	_control,	_function,	_controlled	):	# <<< string, string, list
	lockHideAttributes	(	_control	)

	if (cmds.objExists('anim_control_set') == False):	cmds.createNode('objectSet',name='anim_control_set',skipSelect=True)

	cmds.sets	(	_control,	addElement	=	'anim_control_set'	)
	cmds.toggle	(	localAxis				=	1	)

	if	len	(	_controlled	)	==	0:
		_control	=	cmds.rename	(	'_'	+	_function	+	'_control'	)
		_control	=	cmds.group	( 	world	=	1,	name	=	'_'	+	_function	+	'_control_offSet'	)
		cmds.move					(	0,	0,	0,	_control	+	'.rotatePivot',	_control	+	'.scalePivot'	)

		lockHideAttributes	(	_control	)

	else:
		_k				=	_controlled[0].rfind	(	'|'	)
		_control		=	_controlled[0][_k+1:]
		cmds.rename		(	_control	+	'_'	+	_function	+	'_control'	)
		_control		=	cmds.group	(	world	=	1,	name	=	_control	+	'_'	+ _function	+	'_control_offSet'	)
		cmds.move			(	0, 0, 0, _control + '.rotatePivot', _control + '.scalePivot' )

		lockHideAttributes	(	_control	)

		cmds.select		(	_controlled[0],	toggle	=	True	)
		cmds.parent		()
		cmds.xform		(	translation	=	(	0,	0,	0	),	rotation	=	(	0,	0,	0	)	)
		cmds.parent		(	world		= 	1	)
	
	cmds.pickWalk	(	direction	=	"down"	)

# >>> warnings <<< ________________________________________________________________________
def	raiseWarning	(	_waning	):	# <<< string
	mm.eval	('setCommandLineVisible (1);')
	mm.eval ('warning "..:: '	+	_waning	+	'::..";')

#	print; print; print '>>> SO FAR SO GOOD'; print # <<< DEBUG ONLY LINE, CAN BE DELETED <<< ##########
# >>> orent joint, controls and control groups <<< ______________________________________________
def	smartOrient	(	_direction	):
	_axis	=	cmds.radioCollection	(	'radioCollection_axis',	query	=	True,	select	=	True	)

	if		_axis	==	'axisX':	_axis	=	0
	elif	_axis	==	'axisY':	_axis	=	1
	else:							_axis	=	2

	#_direction	=	cmds.radioCollection	(	'radioCollection_direction',	query	=	True,	select	=	True	)

	if		_direction	==	'plus':		_direction	=	1
	else:								_direction	=	-1

	_keepShape	=	cmds.checkBox	(	'check_keepShape',	query	=	True,	value	=	True	)
	_selList	=	cmds.ls			(					selection	=	True,	long	=	True	)
									
	_rotation	=	[	(	90	*	_direction,	0,	0	),
						(	0,	90	*	_direction,	0	),
						(	0,	0,	90	*	_direction	)	]
						

	if	len	(	_selList	)	>	0:
		for	_selected	in	_selList:
			if	cmds.nodeType	(	_selected	)	==	'joint':
				cmds.select		(	_selected	+	'.rotateAxis',		replace	=	True	)
				cmds.xform		(	rotation	=	_rotation[_axis],	relative	=	True	)
			
			elif	cmds.nodeType	(	_selected	)	==	'transform':
				_offsetGroup	=	cmds.listRelatives	(	parent	=	True	)

				if	_offsetGroup	!=	None:
					cmds.xform	(	_offsetGroup[0],	rotation	=	_rotation[_axis],
									relative	=	True,	objectSpace		=	True	)

					if	_keepShape:
						mm.eval		(	'SelectCurveCVsAll;'	)
						cmds.xform	(	rotation	=	(_rotation[_axis][0]	*	-1,
														_rotation[_axis][1]	*	-1,	
														_rotation[_axis][2]	*	-1	),
										relative	=	True,	objectSpace	=	True	)
				else:	raiseWarning	(	'Group selected'	)
			else:	raiseWarning	(	'this works only on control transForms and joints'	)
			cmds.select ( _selList )
	else:	raiseWarning	(	'Nothing selected'	)

# >>> prints the python command for the selected curve <<< _________________________________________________________
def	createCurveCommand	():
	_curve		=	cmds.ls	(	selection	=	True,	long	=	True	)

	if	len(_curve)	>	0:
		_curve				=	_curve[0]
		_numOfCVs			=	cmds.getAttr	(	_curve	+	'.degree'	)	+	cmds.getAttr	(	_curve	+	'.spans'	)
		_info				=	cmds.createNode	(	'curveInfo'	)
		cmds.connectAttr	(	_curve	+	'.worldSpace',	_info	+	'.inputCurve'	)
		_knotVector			=	cmds.getAttr	(	_info	+	'.knots[*]'	)
		cmds.delete			(	_info	)
		_cvList				=	[]
		_degree				=	cmds.getAttr	(	_curve	+	'.degree'	)

		for	_i	in	range	(_numOfCVs):	_cvList	=	_cvList + cmds.getAttr (_curve + '.cv[' + str(_i) + ']' )

		_curveCommand	=	(	'cmds.curve	(	degree	=	'	+	str	(	_degree	)	+	',	point	=	'	\
							+	str	( _cvList	)	+	', knot	=	'	+	str	(	_knotVector	)	+	'	)'	)

		_curveCommand	=	_curveCommand.replace ( ' ', '\t' )
		_curveCommand	=	_curveCommand.replace ( '[', '[\t' )
		_curveCommand	=	_curveCommand.replace ( ']', '\t]' )
		_curveCommand	=	_curveCommand.replace ( '])', ']\t)' )
		_curveCommand	=	_curveCommand.replace ( '),', '),\n\t\t\t\t\t' )
		_curveCommand	=	_curveCommand.replace ('point', '\n\t\t\tpoint')
		_curveCommand	=	_curveCommand.replace ('knot', '\n\t\t\tknot')

		if	cmds.window	(	'curveCommandGUI',	exists	=	True ):	cmds.deleteUI	(	'curveCommandGUI'	)

		cmds.window			(	'curveCommandGUI',	title	=	'..:: curve command ::..',
							resizeToFitChildren	=	True,	topLeftCorner	=	(	500,	100	),
							width				=	600,	height			=	200	)
		cmds.paneLayout		(	'pane_curveCommand',			configuration	=	'single'	)
		cmds.scrollField	(	'scroll_curveCommand',			wordWrap		=	True,
							editable			=	False,	text			=	_curveCommand	)
		cmds.showWindow		(	'curveCommandGUI' )
	else:
		raiseWarning		('hmmmm...')

# __________________________________________________________________________________________
#	<<< control library >>>
# ___________________________________________________________________________________________

# >>> converts selected to control <<< ________________________________________________________________
def	convertToControl	():
	_controlled		=	cmds.ls		(	selection	=	True,	long	=	True	)

	if	len	(	_controlled	)	==	2:
		cmds.select		(	_controlled[0],	replace	=	True	)
		_control		=	_controlled[0]
		del				_controlled[0]

		postProcessControl	(	_control,	'rotate',	_controlled	)

	else:
		raiseWarning	(	'select the new controller and an object to be controlled'	)

# >>> creates NURBS circle control <<< _________________________________________________________________
def createCircle ():
	_controlled	=	cmds.ls			(	long	=	True,	selection	=	True	)
	_control	=	cmds.circle		(	radius	=	3,	normal	=	(	1,	0,	0	),	
										constructionHistory	=	False	)

	postProcessControl				(	_control[0],	'rotate',	_controlled	)

# >>> creates NURBS locator control <<< _______________________________________________________________
def createNURBSlocator ():
	_controlled		=	cmds.ls		(	long	=	True,	selection	=	True	)
	_control		=	cmds.curve	(	degree	=	1,	point	=	[(0,0,0),(0,0,-5),(0,0,0),(5,0,0),(0,0,0),
														(0,0,5),(0,0,0),(-5,0,0),(0,0,0),(0,5,0),(0,0,0),(0,-5,0)])
	
	postProcessControl				(	_control,	'translate',	_controlled	)

# creates a NURBS arrow control with 1 arrowHead <<< __________________________________________________________
def create2Arrowhead ():
	_controlled		=	cmds.ls		(	long	=	True,	selection	=	True	)
	_control		=	cmds.curve	(	degree	=	1,		point=[(0,3,1),(0,3,2),(0,6,0),(0,3,-2),(0,3,-1),
															(0,-3,-1),(0,-3,-2),(0,-6,0),(0,-3,2),(0,-3,1),(0,3,1)]	)

	postProcessControl				(	_control,	'translate',	_controlled	)

# >>> creates a NURBS arrow control with 4 arrowHead <<< _____________________________________________________________
def create4Arrowhead ():
	_controlled		=	cmds.ls		(	long	=	True,	selection	=	True	)
	_control		=	cmds.curve	(	degree	=	1,		point		=[(0,1,1),(0,3,1),(0,3,2),(0,6,0),(0,3,-2),
															(0,3,-1),(0,1,-1),(0,1,-3),(0,2,-3),(0,0,-6),
															(0,-2,-3),(0,-1,-3),(0,-1,-1),(0,-3,-1),(0,-3,-2),
															(0,-6,0),(0,-3,2),(0,-3,1),(0,-1,1),(0,-1,3),
															(0,-2,3),(0,0,6),(0,2,3),(0,1,3),(0,1,1)]	)
	
	postProcessControl				(	_control,	'translate',	_controlled	)

# >>> creates a NURBS cube <<< ____________________________________________________________________________________
def	createNURBScube	():
	_controlled		=	cmds.ls		(	long	=	True,	selection	=	True	)
	_control		=	cmds.curve	(	degree	=	1,		point		=	[(2,2,2),(2,2,-2),(2,-2,-2),(2,-2,2),(2,2,2),
																			(-2,2,2),(-2,-2,2),(2,-2,2),(2,2,2),(-2,2,2),
																			(-2,2,-2),(-2,-2,-2),(-2,-2,2),(-2,2,2),
																			(-2,2,-2),(2,2,-2),(2,-2,-2),(-2,-2,-2)]	)
	
	postProcessControl				(	_control,	'translate',	_controlled	)

# >>> creates NURBS piramyd <<< _______________________________________________________________________________________
def	createPiramyd	():
	_controlled		=	cmds.ls		(	long	=	True,	selection	=	True	)
	_control		=	cmds.curve	(	degree	=	1,		point		=	[(-2,0,0),(-5,3,0),(-5,0,-3),(-2,0,0),
																			(-5,-3,0),(-5,0,-3),(-2,0,0),(-5,0,3),
																			(-5,3,0),(-2,0,0),(-5,-3,0),(-5,0,3)]	)

	postProcessControl				(	_control,	'translate',	_controlled	)

# creates a circular rotate icon with one arrow head <<< __________________________________________________________________
def createCircle1Arrowhead	():
	_controlled			=	cmds.ls		(	long	=	True,	selection	=	True	)
	_curveList			=	[]
	_control			=	cmds.circle (	normal	=	(	1,	0,	0	),	radius	=	2,	sweep	=	300,
											constructionHistory	=	False	)
	_curveList.append					(	_control[0]	)
	_control			=	cmds.circle	(	normal	=	(	1,	0,	0	),	radius	=	3,	sweep	=	300,
											constructionHistory =	False	)
	_curveList.append					(	_control[0]	)
	_control 			=	cmds.curve	(	degree	=	1,	point	=	[(0,3,0),(0,3.5,0),(0,2.5,-2),(0,1.5,0),(0,2,0)]	)
	_curveList.append					(	_control	)
	_control = cmds.curve				(	degree	=	1,	point	=	[(0,1.5,-2.598076),(0,1,-1.732051)]	)
	_curveList.append					(	_control )

	for	_k	in	_curveList:		cmds.select	(	_k,	add	=	True	)
	_control			=	cmds.attachCurve	()

	for	_k	in	_curveList:		cmds.select	(	_k,	add	=	True	)

	cmds.select		(	_control[0],	deselect	=	True	)
	cmds.delete		()
	cmds.select		(	_control[0]	)
	
	postProcessControl				(	_control[0],	'rotate',	_controlled	)

# >>> create single NURBS curve sphere <<< ___________________________________________________________________________________
def createSphere ():
	_controlled			=	cmds.ls	(	long	=	True,	selection	=	True	)
	_curveList			=	[]
	# create arcs
	_arc				=	cmds.createNode		(	'makeTwoPointCircularArc'	)
	cmds.setAttr		(	_arc	+	'.pt1',	0,	3,	0	)
	cmds.setAttr		(	_arc	+	'.pt2',	-3,	0,	0	)
	cmds.setAttr		(	_arc	+	'.dv',	0,	0,	1	)
	cmds.setAttr		(	_arc	+	'.radius',	3	)
	_curve				=	cmds.createNode		(	'nurbsCurve'	)
	_curve				=	cmds.listRelatives	(	_curve,	parent	=	True	)
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc',	_curve[0]	+	'.cr'	)
	#
	_arc				=	cmds.createNode	(	'makeTwoPointCircularArc'	)
	cmds.setAttr		(	_arc	+	'.pt1',	3,	0,	0	)
	cmds.setAttr		(	_arc	+	'.pt2', 0, 3, 0 )
	cmds.setAttr		(	_arc	+	'.dv', 0, 0, 1 )
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append 	(	_curve )
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', -3, 0, 0 )
	cmds.setAttr		(	_arc	+	'.pt2', 0, -3, 0 )
	cmds.setAttr		(	_arc	+	'.dv', 0, 0, 1 )
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0, -3, 0 )
	cmds.setAttr		(	_arc	+	'.pt2', 3, 0, 0 )
	cmds.setAttr		(	_arc	+	'.dv', 0, 0, 1 )
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0,3,0 )
	cmds.setAttr		(	_arc	+	'.pt2', 0,0,3 )
	cmds.setAttr		(	_arc	+	'.dv', 1,0,0 )
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve )
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0,0,-3)
	cmds.setAttr		(	_arc	+	'.pt2', 0,3,0)
	cmds.setAttr		(	_arc	+	'.dv', 1,0,0 )
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0,-3,0)
	cmds.setAttr		(	_arc	+	'.pt2', 0,0,-3)
	cmds.setAttr		(	_arc	+	'.dv', 1,0,0)
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0,0,3)
	cmds.setAttr		(	_arc	+	'.pt2', 0,-3,0)
	cmds.setAttr		(	_arc	+	'.dv', 1,0,0)
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	( _arc + '.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0,0,-3)
	cmds.setAttr		(	_arc	+	'.pt2', -3,0,0)
	cmds.setAttr		(	_arc	+	'.dv', 0,1,0)
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 3,0,0)
	cmds.setAttr		(	_arc	+	'.pt2', 0,0,-3)
	cmds.setAttr		(	_arc	+	'.dv', 0,1,0)
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve )
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', 0,0,3)
	cmds.setAttr		(	_arc	+	'.pt2', 3,0,0)
	cmds.setAttr		(	_arc	+	'.dv', 0,1,0)
	cmds.setAttr		(	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve	)
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )
	#
	_arc				=	cmds.createNode	( 'makeTwoPointCircularArc' )
	cmds.setAttr		(	_arc	+	'.pt1', -3,0,0)
	cmds.setAttr		(	_arc	+	'.pt2', 0,0,3)
	cmds.setAttr		( 	_arc	+	'.dv', 0,1,0)
	cmds.setAttr		( 	_arc	+	'.radius', 3 )
	_curve				=	cmds.createNode	( 'nurbsCurve' )
	_curve				=	cmds.listRelatives	( _curve, parent = True )
	_curveList.append	(	_curve )
	cmds.connectAttr	(	_arc	+	'.oc', _curve[0] + '.cr' )

	cmds.select			(	clear	=	True	)
	for	_c	in	range	(	len	(	_curveList	)	-1	):
		cmds.select		(	_curveList[_c],	toggle	=	True	)

	cmds.delete			( 	constructionHistory	=	True	)
	cmds.attachCurve	(	constructionHistory	=	False,	replaceOriginal	=	True,	keepMultipleKnots	=	True,
							method	=	0,	blendKnotInsertion	=	False,	parameter	=	0.1	)
	cmds.delete			( 	constructionHistory	=	True	)
	cmds.select			(	_curveList[0],	_curveList[11],	replace	=	True	)

	cmds.delete			( 	constructionHistory	=	True	)
	cmds.attachCurve	(	constructionHistory	=	False,	replaceOriginal	=	True,	keepMultipleKnots	=	True,
							method	=	0,	blendBias	=	0.5,	blendKnotInsertion	=	False,	parameter	=	0.1	)
	cmds.delete			( 	constructionHistory	=	True	)
	cmds.select			(	_curveList[0],	replace	=	True	)
	
	_control			=	cmds.rename	(	_curveList[0],	'_rotation_control'	)

	for	_c	in	range	(	len	(	_curveList	)	-1	):
		cmds.select	(	_curveList[_c+1],	replace	=	True	)
		cmds.delete	()

	cmds.select			(	_control	)

	postProcessControl	(	_control,	'rotate',	_controlled	)

# >>> creates spherical arrow <<< _________________________________________________________________________________
def	createSpherical4Arrowhead	():
	_controlled		=	cmds.ls		(	long	=	True,	selection	=	True	)
	_baseCurve		=	cmds.curve	( 	degree	=	1,	point	=	[	(0,1,1),(0,3,1),(0,3,2),(0,6,0),(0,3,-2),(0,3,-1),
										(0,1,-1),(0,1,-3),(0,2,-3),(0,0,-6),(0,-2,-3),(0,-1,-3),(0,-1,-1),(0,-3,-1),
										(0,-3,-2),(0,-6,0),(0,-3,2),(0,-3,1),(0,-1,1),(0,-1,3),(0,-2,3),(0,0,6),(0,2,3),
										(0,1,3),(0,1,1)	]	)
	_tempSphere		=	cmds.sphere	(	radius	=	7,	axis	=	(	0,	1,	0	),	sections	=	4,
										startSweep	=	270,	endSweep	=	90,	constructionHistory	=	0	)
	_control 		=	cmds.projectCurve	(	_baseCurve,	_tempSphere,
												constructionHistory	=	False,	direction	=	(	1,	0,	0	),	)
	_control		=	cmds.duplicateCurve	(	_control,	constructionHistory	=	True,	object	=	True	)
		
	cmds.delete		(	_tempSphere	)
	cmds.delete		(	_baseCurve	)
	
	postProcessControl	(	_control[0],	'rotate',	_controlled	)

# >>> creates locator <<< ____________________________________________________________________________________________
def	createLocator	():
	_controlled		=	cmds.ls			(	long	=	True,	selection	=	True	)
	_control		=	cmds.createNode	(	'locator'	)
	_control		=	cmds.listRelatives	(	parent	=	True	)
	
	postProcessControl	(	_control[0],	'translate',	_controlled	)

# __________________________________________________________________________________________
#	<<< setup library >>>
# _________________________________________________________________________________________

# >>> ribbon spine <<< _______________________________________________________________________
def setupRibbon ():
	# >>> get ribbon plane, plane shape, V spans, follicle position distance
	_planeShape = cmds.listRelatives(shapes=True)[0]	# <<< get ribbon NURBS plane Shape
	_k = _planeShape.rfind('|')
	_planeShape = _planeShape[_k+1:]	# <<< get ribbon NURBS plane nice name
	_spansV=cmds.getAttr(_planeShape+'.spansV')	# <<< get ribbon NURBS plane V spans
	_posV = (1.0/_spansV)/2	# <<< follicle start position on plane in V
	_spineJoint_ = []	# <<< spine joint list
	_folli_ = []	# <<< follicle list

	# >>> create & position follicle/Vspan, create & position parented-joint/follicle
	for _k in range(_spansV):
		_follicleShape = cmds.createNode ('follicle')
		_follicle = cmds.listRelatives(parent=True)
		_follicle = _follicle[0]
		_folli_.append(_follicle)
		_spineJoint_.append (cmds.createNode('joint', parent=_follicle))
		cmds.toggle (localAxis=True)

		cmds.connectAttr(_planeShape+'.worldMatrix[0]', _follicleShape+'.inputWorldMatrix', force=True)
		cmds.connectAttr(_planeShape+'.local', _follicleShape+'.inputSurface', force=True)
		cmds.connectAttr(_follicle+'.outTranslate', _follicle+'.translate', force=True)
		cmds.connectAttr(_follicle+'.outRotate', _follicle+'.rotate', force=True)
		cmds.setAttr(_follicleShape+'.parameterU', 0.5)
		cmds.setAttr(_follicleShape+'.parameterV', _posV)
		_posV = _posV+(1.0/_spansV)	# <<< follicle position

	# >>> create plane skin joints
	_skinJoint_=[]	# <<< plane skin joints list

	_joint=cmds.createNode('joint')
	_skinJoint_.append(_joint)
	cmds.xform(translation=(2,3,0))
	cmds.setAttr(_joint+'.jointOrient', 0,0,-90)
	cmds.toggle (localAxis=True)

	_joint=cmds.createNode('joint', parent=_joint)
	cmds.xform(translation=(0.5,0,0))
	cmds.setAttr(_joint+'.jointOrient', 0,0,90)
	cmds.toggle (localAxis=True)

	_joint=cmds.createNode('joint')
	_skinJoint_.append(_joint)

	cmds.xform(translation=(2,-3,0))
	cmds.setAttr(_joint+'.jointOrient', 0,0,90)
	cmds.toggle (localAxis=True)

	_joint=cmds.createNode('joint', parent=_joint)
	cmds.xform(translation=(0.5,0,0))
	cmds.setAttr(_joint+'.jointOrient', 0,0,-90)
	cmds.toggle (localAxis=True)

	_joint=cmds.createNode('joint')
	_skinJoint_.append(_joint)
	cmds.xform(translation=(2,0,0))
	cmds.toggle (localAxis=True)

	# >>> create & parent locator-groups - position, aim, upVector + 1 offSet
	_locatorPos_ = []	# <<< position locator list
	_locatorAim_ = []	# <<< aim locator list
	_locatorUp_ = []	# <<< upVector locator list
	print _joint
	_joint = 0	# <<< position locator list start, middle, end joint ID in _spineJoint_
	_step = len(_spineJoint_)/2

	for _l in range(3):	# <<< create position locators
		_locator=cmds.createNode('locator')
		cmds.setAttr(_locator+'.localScaleX', 0.35)
		cmds.setAttr(_locator+'.localScaleY', 0.35)
		cmds.setAttr(_locator+'.localScaleZ', 0.35)
		_locator=cmds.listRelatives(parent=True)
		_locatorPos_.append(_locator[0])
		cmds.toggle (_locator[0], localAxis=True)
		_pos=cmds.xform (_spineJoint_[_joint], query=True, worldSpace=True, translation=True)
		print _spineJoint_
		cmds.xform (_locatorPos_[_l], absolute=True, worldSpace=True, translation=_pos)
		_joint = _joint+_step

		for _k in range(2):
			_locator=cmds.createNode('locator')# <<< create aim & up locators
			cmds.setAttr(_locator+'.localScaleX', 0.2)
			cmds.setAttr(_locator+'.localScaleY', 0.2)
			cmds.setAttr(_locator+'.localScaleZ', 0.2)

			_locatorTrans=cmds.listRelatives(parent=True)
			cmds.toggle (_locatorTrans[0], localAxis=True)
			if _k == 0:
				_locatorAim_.append(_locatorTrans[0])
			else:
				_locatorUp_.append(_locatorTrans[0])

			cmds.pickWalk(direction='up')
			cmds.select(_locatorPos_[_l], add=True)
			cmds.parent()
			cmds.select (_locator, replace=True)
			cmds.pickWalk (direction='up')
		
			if _k==1:
				cmds.xform (objectSpace=True, translation=(2,0,0))
			else:
				cmds.xform (objectSpace=True, translation=(0,0,0))

	# >>> create middle offset locator
	cmds.select (_locatorPos_[1], replace=True)
	cmds.pickWalk(direction='down')
	_locator=cmds.pickWalk(direction='right')
	_locator=_locator[0]
	cmds.createNode('locator')	# <<< create middle offset locator
	_midOffSet=cmds.pickWalk(direction='up')
	_midOffSet=_midOffSet[0]
	cmds.setAttr('.localScaleX', 0.2)
	cmds.setAttr('.localScaleY', 0.2)
	cmds.setAttr('.localScaleZ', 0.2)
	cmds.pickWalk(direction='up')
	cmds.toggle (localAxis=True)
	cmds.select (_locator, add=True)
	cmds.parent () 
	cmds.xform (translation=(0,0,0))

	# >>> constrain locators
	cmds.pointConstraint (_locatorPos_[0], _locatorPos_[2], _locatorPos_[1])	# <<< middle pos constrain

	cmds.aimConstraint (_locatorPos_[2], _locatorAim_[0], aimVector=(0,1,0),
		upVector=(1,0,0), worldUpType='object', worldUpObject=_locatorUp_[0])

	cmds.aimConstraint (_locatorPos_[0], _locatorAim_[2], aimVector=(0,-1,0),
		upVector=(1,0,0), worldUpType='object', worldUpObject=_locatorUp_[2])

	cmds.aimConstraint (_locatorPos_[2], _locatorAim_[1], aimVector=(0,1,0),
		upVector=(1,0,0), worldUpType='object', worldUpObject=_locatorUp_[1])

	cmds.pointConstraint (_locatorUp_[0], _locatorUp_[2], _locatorUp_[1])

	# >>> parent & position skin-joints, position locators
	cmds.parent(_skinJoint_[0], _locatorAim_[2])
	cmds.xform(translation=(0,0,0))

	cmds.parent(_skinJoint_[1], _locatorAim_[0])
	cmds.xform(translation=(0,0,0))

	cmds.parent(_skinJoint_[2], _midOffSet)
	cmds.xform(translation=(0,0,0))

	_posV = cmds.xform (_folli_[0], query=True, translation=True)
	_k = cmds.xform (_folli_[1], query=True, translation=True)
	_step = _posV[1]-_k[1]
	_step = _step/2

	cmds.xform(_locatorPos_[0], relative=True, translation=(0,_step,0))
	cmds.xform(_locatorPos_[2], relative=True, translation=(0,-_step,0))

	# >>> select palne & skinJoint for skinning
	cmds.select(_skinJoint_)
	cmds.select(_planeShape, add=True)

	mm.eval('warning "..:: u can bind skin now ::..";')

# >>>	strechy-t : make joints strechy for selected spline IK handle <<< _________________________________________
def	setupStrechy	():
	# >>>	get IK from selection, get start/end joints & IK curve, determine strechy joints
	_IK				=	cmds.ls					(selection	=	True)[0]
	_IKcurve		=	cmds.listConnections	(_IK	+	'.inCurve',				destination	=	True)[0]
	_startJoint		=	cmds.listConnections	(_IK	+	'.startJoint',			destination	=	True)[0]
	_endEffector	=	cmds.listConnections	(_IK	+	'.endEffector',			destination	=	True)[0]
	_endJoint		=	cmds.listConnections	(_endEffector	+	'.translateX',	destination	=	True)[0]
	cmds.select									(_endJoint,	hierarchy	=	True)
	_jointsTrash	=	cmds.ls					(selection	=	True)
	cmds.select									(_startJoint,	hierarchy	=	True)
	_strachyJoints_	=	cmds.ls					(selection	=	True)
	_strachyJoints_	=	_strachyJoints_[:len	(_strachyJoints_)	-	len	(_jointsTrash)-1]
	
	# >>>	setup utility nodes
	_curveInfo		=	cmds.arclen			(_IKcurve,	constructionHistory	=	True)
	_condtition		=	cmds.createNode		('condition')
	_startLength	=	cmds.getAttr		(_curveInfo	+	'.arcLength')
	_currentLength	=	cmds.createNode		('multiplyDivide')
	cmds.setAttr							(_currentLength	+	'.operation',	2)
	cmds.setAttr							(_currentLength	+	'.input2X',	_startLength)
	cmds.setAttr							(_condtition	+	'.firstTerm',	_startLength)
	cmds.setAttr							(_condtition	+	'.operation',	4)
	cmds.connectAttr						(_curveInfo		+	'.arcLength',	_currentLength	+	'.input1X',	force	=	True)
	cmds.connectAttr						(_curveInfo		+	'.arcLength',	_condtition	+	'.secondTerm',	force	=	True)
	cmds.connectAttr						(_currentLength	+	'.outputX',	_condtition	+	'.colorIfTrueR',	force	=	True)

	# >>>	connect calculated scale to joints
	for	_j	in	_strachyJoints_:
		cmds.connectAttr					(_condtition	+	'.outColorR',	_j	+	'.scaleX',	force	=	True)