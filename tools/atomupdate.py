"""
ATOM anim export / import
has a lot's of problems and restrictions.

selection on import has to match
selection on export, etc...

this script exports all selected
objects anim to separated files
and imports it to the selected nodes.
"""


import pymel.core as pm


def get_selection(prefix=''):
	sel = pm.ls(selection=True)
	new_sel = [pm.PyNode(prefix + node.name()) for node in sel]

	return (sel, new_sel)

def export_atom(node):
	pass


def import_atom(node):
	pass


def export_all_anim(sel):
	for node in sel:
		export_atom(node)


def import_all_anim(sel, new_sel):
	for k, node in enumerate(sel):
		import_atom(new_sel[k])



def main():
	sel, new_sel = get_selection('new_')

	export_all_anim(sel)
	import_all_anim(sel, new_sel)

	pm.select(new_sel)


if __name__ == '__main__':
	main()