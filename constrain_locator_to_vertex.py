#! python2

__author__		= 'forgacs.daniel@gmail.com'
__version__		= 'v1'


'''
create and constrain a locator to a vertex with an expression
'''


import maya.cmds as cmds


def	constrain_locator_to_vertex	():
	vertex		= cmds.ls (selection = True)[0]
	geo			= vertex[:vertex.rfind('.')]
	locator		= cmds.createNode	('locator')
	locator		= cmds.listRelatives (locator, parent = True)[0]
	locator		= cmds.rename (locator, 'locator_vertexConstrained')
	#locator		= cmds.pickWalk (direction = 'up')[0]
	cmds.expression	(name = locator, string	='''
float $BBoxSize = '''	+	geo	+	'''.boundingBoxMinX;\n
float $vertexWorldPos[3] = `pointPosition -world '''		+	vertex	+	'''`;\n'''	+
locator	+	'''.translateX = $vertexWorldPos[0];\n'''	+
locator	+	'''.translateY = $vertexWorldPos[1];\n'''	+
locator	+	'''.translateZ = $vertexWorldPos[2];'''	)