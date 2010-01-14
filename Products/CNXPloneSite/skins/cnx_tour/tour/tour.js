function show(divId, page) {

	if (page == 'software') {
		hideAll('software');
	}

	if (document.getElementById) {
		if (page == 'components') {
			document.getElementById('components-instructions').style.visibility = 'hidden';
		} else if (page == 'factory') {
			document.getElementById('factory-instructions').style.visibility = 'hidden';
		}
		document.getElementById(divId).style.visibility = 'visible';
	} else if (document.layers && document.layers[divId]) {
		if (page == 'components') {
			document.layers['components-instructions'].visibility = 'hidden';
		} else if (page == 'factory') {
			document.layers['factory-instructions'].visibility = 'hidden';
		}
		document.layers[divId].visibility = 'visible';
	}

	if ((page == 'components') && (divId != 'connexions')) {
		if (document.getElementById) {
			document.getElementById('mini_' + divId).style.backgroundColor = 'cc9900';
		} else if (document.layers && document.layers[divId]) {
			document.layers['mini_' + divId].backgroundColor = 'cc9900';
		}
	}

}

function hide(divId, page) {
	if (document.getElementById) {
		document.getElementById(divId).style.visibility = 'hidden';
		if (page == 'factory') {
			document.getElementById('factory-instructions').style.visibility = 'visible';
		} else if (page == 'components') {
			document.getElementById('components-instructions').style.visibility = 'visible';
		}
		if ((page == 'components') && (divId != 'connexions')) {
			document.getElementById('mini_' + divId).style.backgroundColor = '006699';
		}
	} else if (document.layers && document.layers[divId]) {
		document.layers[divId].visibility = 'hidden';
		if (page == 'factory') {
			document.layers['factory-instructions'].visibility = 'visible';
		} else if (page == 'components') {
			document.layers['components-instructions'].visibility = 'visible';
		}
		if (page == 'components') {
			document.layers['mini_' + divId].backgroundColor = '006699';
		}
	}
}

function getElementsByClassName(class_name) {
	var all_obj, ret_obj=new Array(), j=0;
	if (document.all) all_obj = document.all;
	else if(document.getElementsByTagName && !document.all) all_obj = document.getElementsByTagName("div");
	for(i=0; i<all_obj.length; i++) {
		if (all_obj[i].className == class_name) {
			ret_obj[j]=all_obj[i];
			j++;
		}
	}
	return ret_obj;
}

/*
function hideAll(class_name) {
	var obj = getElementsByClassName(class_name);
	for (i=0; i<obj.length; i++) {
		if (document.getElementById) {
			obj[i].style.visibility = 'hidden';
		} else if (document.layers) {
			obj[i].visibility = 'hidden';
		}
	}
}
*/

function hideAll(class_name) {
	for (i=0; i<SOFTWARE.length; i++) {
		if (document.getElementById) {
			document.getElementById(SOFTWARE[i]).style.visibility = 'hidden';
		} else if (document.layers) {
			document.layers[SOFTWARE[i]].visibility = 'hidden';
		}
	}
}

var SOFTWARE = new Array('modules','content_commons','authoring_tools','course_composer','annotations','roadmap');
