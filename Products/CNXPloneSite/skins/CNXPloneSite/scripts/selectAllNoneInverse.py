        function checkAll(formname,fieldname) {
          for (var j = 0; j <= document.forms[formname].length; j++) {
            box = document.forms[formname].elements[j];
            if ((box) && (box.name == fieldname) && (box.checked == false)) {
              box.checked = true;
            }
          }
        }
  
        function checkNone(formname,fieldname) {
          for (var j = 0; j <= document.forms[formname].length; j++) {
            box = document.forms[formname].elements[j];
            if ((box) && (box.name == fieldname) && (box.checked == true)) {
              box.checked = false;
            }
          }
        }
  
        function checkInverse(formname,fieldname) {
          for (var j = 0; j <= document.forms[formname].length; j++) {
            box = document.forms[formname].elements[j];
            if ((box) && (box.name == fieldname)) {
              box.checked = !box.checked;
            }
          }
        }
