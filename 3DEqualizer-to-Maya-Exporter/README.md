3DEqualizer_to_Maya_exporter
============================

exports 3De projects as mel script and sources the script in maya.
	maya has to have an open communication port:
	
	commandPort -name ":6001";
	
	- the mel file is named after the 3De scene
	- it`s saved in the same folder as the 3De scene
	- the first frame is set based on the selected camera`s sequence
