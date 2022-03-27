/**
 * all js
 */
 //var frontendtimeout = 60000
  //alert(frontendtimeout);
 	(function() {
			    var idlefunction = function() {
			          // what to do when mouse is idle
			         // alert("hi");
			    	window.location.replace(contextPath+"/logout");

			        }, idletimer,
			        idlestart = function() {idletimer = setTimeout(idlefunction,frontendtimeout);
			        //console.log("start");

			        },
			        idlebreak = function() {
			        	clearTimeout(idletimer);
			        	idlestart();
				       // console.log("break");

			        };
			    if( window.addEventListener){
			    	
			        document.documentElement.addEventListener("mousemove",idlebreak,true);

			    }
			    else{
			    	
			        document.documentElement.attachEvent("onmousemove",idlebreak,true);
			        
			    }
			})(); 