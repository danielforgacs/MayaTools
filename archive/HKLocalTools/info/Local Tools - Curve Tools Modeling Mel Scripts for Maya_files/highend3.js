function getSelectedValue(dom_id) {
	select = document.getElementById(dom_id);
	opt = select.options[select.selectedIndex];
	return opt.value;
}

function toggle_visibility(dom_id) {
	obj = document.getElementById(dom_id);
	obj.style.display = obj.style.display == 'block' ? 'none' : 'block';
}