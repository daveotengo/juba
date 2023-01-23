        //alert("hi")
        getUserList();



        function getUserList(){

       	// $("#loading").show();


          $.ajax({
              'url': "api/users",
              'method': "GET",

              'contentType': 'application/json'
          }).done( function(data) {

         	// $("#loading").hide();

              $('#datatable-keytable').dataTable( {
            	 // "scrollY": 500,
                   "scrollX": true,
                   "processing": true,

                   "destroy":true,

                   "pageLength": 10,

                   "aaData": data,

                    keys: true ,

                    dom: 'lBfrtip',
                   buttons: [
                       'copy', 'csv', 'excel', 'pdf', 'print'
                   ],

                   "order": [ 0, "desc" ],

                  "columns": [

                 	  { "data": "id" },

                      { "data": "name" },

                      { "data": "email" },

                      { "data": "username" },

                      { "data": "access" },


//                      { "data": "roles.0.name" },

//                      { "data": "department.departmentName" },
//
//                      { "data": "twofAuth" },
//
//                      { "data": "pwReset" },
//
//                      { "data": "blocked" },
//
//                      { "data": "lastLogin" },

                      { "data": "register_date" },

                      {	"data": null }



                  ]
              ,

							  "columnDefs": [

								  { "targets": -1, "data": null, "defaultContent":"<button class='btn btn-default btn-sm update' style='background-color:#5eba7d' onclick='getUserById(this)' >"
										+"<i class='fa fa-pencil fa-fw' style='color:#ffffff' ></i>"
										+"</button>"

										//onclick='deleteUser(this)'

									 +"<button  class='btn btn-default btn-sm save' style='background-color:#f44336'  onclick='triggerDeleteDialogue(this)'   >"
											+"<i class='fa fa-trash fa-fw' style='color:#ffffff' ></i>"
									+"</button>"


									 /* 	+"<button class='btn btn-default btn-sm hi'   onclick='closed(this)'  style='display:none' >"
										+"<i class='fa fa-close fa-fw'></i>"
										+"</button>" */

								  },

									{
										 targets: [5],
									 "render": function(data){
				                         return moment(data).format("YYYY-MM-DD HH:mm:ss")
				                     },
				                    }


			                     ]

              })



          });

          }


     function showBtnAdd(e){
     //alert("hi");
		 	$('button#btnAdd').show();
		    $('button#btnUpdate').hide();
		    //showing password and confirmpassword
		    $("#passConf").show();

		    $("#password").attr('required');
		    $("#confirmPassword").attr('required');

		    //reseting input fields
		    $('#signupForm')[0].reset();


	 }


	   function updateUser(e){

        	/* var row = $(e).closest('tr')[0];
			var id = $(row).find('td:eq(0)').val();
			alert(id); */

            /*
            var name= $(row).find('input:eq(1)').val();
			var nameArray = new Array();
			nameArray = name.split("   "); */

			///alert("eii");

			 $("#loading").show();

             //alert("ooo");

			 var id = $.trim($("#inputId").val());

			 //alert(id);


	       	 var name=$("#name").val();

//	       	 var lastName=$("#lastName").val();

	       	 var email=$("#email").val();

	       	 var username=$("#username").val();


//	       	 var phoneNumber=$("#phoneNumber").val();


//	       	 var confirmEmail=$("#confirmEmail").val();


//	       	 var password=$("#password").val();
//	       	 var confirmPassword=$("#confirmPassword").val();
	       	 var role=$("#role").val();


	       	 //var roleId=$("#role").val();

//	       	 var roleText=$("#role option:selected" ).text();
//
//	       	 var twofAuthStatus=$("#twofAuthStatus").val();
//
//	       	 var blockStatus=$("#blockStatus").val();
//
//
//	       	// alert(roleText);
//
//
//	       	 var	roleObject = {
//	       			id: roleId,
//		            name: roleText
//		        }
//	       	 var department=$("#department").val();

	       	/* var departmentId=$("#department").val();


	       var	departmentObject = {
		            departmentId: departmentId,
		            departmentName: ""
		        } */


	            var UserObj = {};
	            UserObj["name"] = name;

//	            UserObj["firstName"] = firstName;
//	            UserObj["lastName"] = lastName;
	            UserObj["email"] = email;

//	            UserObj["phoneNumber"] = phoneNumber;
	            UserObj["username"] = username;

//	            UserObj["confirmEmail"] = confirmEmail;
//	            UserObj["password"] = null;
//	            UserObj["confirmPassword"] = null;

	            UserObj["access"] = role;

//	            UserObj["roleObject"] = roleObject;

//	            UserObj["department"] = department;

	            UserObj["id"] = id;

//	            if(twofAuthStatus=="true"){
//
//		            UserObj["isTwofAuth"] = true;
//
//	            }else{
//
//		            UserObj["isTwofAuth"] = false;
//
//	            }
//
//	            if(blockStatus=="true"){
//
//	            	UserObj["isBlocked"] = true;
//
//	            }else{
//
//	            	UserObj["isBlocked"] = false;
//
//	            }

//	            UserObj["clientIp"]=$("#clientIp").val();



	           // && password!="" && confirmPassword!=""

		if(name!="" && username!="" && email!=""  && role!="" ){



            var updateData = $.ajax({
                type: "POST",
                url: "/api/users/user/update",
                data: JSON.stringify(UserObj),
                contentType : 'application/json',
                success: function(data){


                    //alert("User Updated Successfully");

                	//alert(data);

                  	$("#loading").hide();

           		 	$('#con-close-modal').modal('hide');
                    /* reload form */

    				// getUserList();
   				 //getUserList();

           			swal({
                        title: "Updated!",
                        text: "Your record has been Updated.",
                        type: "success",
                        showCancelButton: false,
                        confirmButtonText: "Ok",
                        closeOnConfirm: true
                    }, function(){


		   				 getUserList();

    					//alert("hi");

                        //swal("Deleted!", "Your imaginary file has been deleted.", "success");
                    });
                }
            });
          /*   saveData.success(function() { alert("post was successfull"); });
            saveData.error(function() { alert("Something went wrong"); }); */
            }
            }








		function getUserById(e) {

			/* 	var row = $(e).closest('tr')[0];
				var id = $(row).find('td:eq(0)').text();

				 $("#inputId").val(id); */

			var row = $(e).closest('tr')[0];
			var id = $(row).find('td:eq(0)').text();


			$.ajax({

				url : "/api/users/user/" + id,
				method : 'POST'
			}).then(
					function(data) {

						$('.modal-title').text("Update User");


					    $('#signupForm')[0].reset();


//						  $("#password").removeAttr("name");
//
//						  $("#password").removeAttr("required");
//
//
//						  $("#confirmPassword").removeAttr("required");

						 $('#con-close-modal').modal({
				      		 // $(this).find('#dateInput').focus();

				        	  //  show: 'false'
				         		});


						  $("#inputId").val(data.id);

				       	 $("#name").val(data.name);

//				       	  $("#lastName").val(data.lastName);

				       	 $("#email").val(data.email);

				       	 //$("#phoneNumber").val(data.phoneNumber);

				       	 $("#username").val(data.username);


				       	$("#passConf").hide();


				       /* 	$("#password").val("");
				       	 $("#confirmPassword").val(""); */
/*
				       	$("#password").val(data.password);
				       	 $("#confirmPassword").val(data.password); */

				       //	$("select#role").val(data.role);


				       //	$("select#department").val("hi");

				       	//$("select#department option[value="+data.department.departmentId+"]").attr('selected','selected');
				       	 //var role=$("#role").val();

							    $('button#btnAdd').hide();
							    $('button#btnUpdate').show();

							    //$("select#role").removeAttr('selected');

							   // $("select#role option[value="+data.roles[0].id+"]").attr('selected','selected');
//							   $("select#department").val(data.department.departmentId);
//
//							    $("select#role").val(data.roles[0].id);
//							    var twofAuthstats;
//
//							    if(data.twofAuth==true){
//
//							    	twofAuthstats="true";
//
//							    }else{
//
//							    	twofAuthstats="false";
//
//							    }
//
//							    $("select#twofAuthStatus").val(twofAuthstats);
//
//							    var blockstats;
//							    if(data.blocked==true){
//
//							    	blactstats="true";
//
//							    }else{
//
//							    	blactstats="false";
//
//							    }
//
//							    $("select#blockStatus").val(blactstats);

							    //alert(data.blocked);
							/* for(int x=0;x<;x++){
					    		$("select#role option[value="+data.roles[x].id+"]").attr('selected','selected');
							} */


						$.each(data, function(index, item) {


							/* var cron = document.getElementById('cronInput');
							var date = document.getElementById('dateInput');

							if (cron != null) {
								cron.style.display = 'block';
								 date.style.display = 'none';
							} else if (date != null) {
								date.style.display = 'block';
								 cron.style.display = 'none';
							} */

							/* var row = $(e).closest('tr')[0];
							var id = $(row).find('td:eq(0)').text();
							var info = $(row).find('a.info1').text();
							$(row).find('a.info1').html('');
							$('[data-toggle="tooltip"]').tooltip();
							$(row).find('.info1 p').attr('style',"display:inline");
							$(row).find('label.info1').html(
											' <div>JobName : ' + data.name+ '; </div>'
											+ " <div>  Job Description : "+data.jobDescription + "; </div>  "
											+ ' <div>  Subject : '+ data.subject +'; </div>  '
											+ " <div>  Message : " + data.text+'; </div>  '
											+ " <div>  Reciepient(s) : "+ data.to + ';  </div>   '
											+ ' <div>  CcReciepient(s) : '+ data.cc + ';  </div>  '
											+ ' <div>  BccReciepient(s) : '+ data.bcc + '; </div> '
											+ ' <div>  Attachment(s) : '+ data.attachments+ ';    </div>  '
											+ '<div>  Trigger Description : '+ data.triggers[0].triggerDescription + '</div>  '
											+ ' <div>  ' + 'Cron : '+ data.triggers[0].cron+'; </div>  '
											+ ' <div>  ' + 'Date : '+ data.triggers[0].when+'; </div>  ');

							console.log(info); */
						});
					});

		}



        /*  $('#sawarning').click(function(){
        	 alert("hi");
             swal({
                 title: "Are you sure?",
                 text: "You will not be able to recover this imaginary file!",
                 type: "warning",
                 showCancelButton: true,
                 confirmButtonColor: "#DD6B55",
                 confirmButtonText: "Yes, delete it!",
                 closeOnConfirm: false
             }, function(){

            	 deleteUser(this);
             });
         }); */
        function triggerDeleteDialogue(e){


        	    swal({
                    title: "Are you sure?",
                    text: "You will not be able to recover this record!",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Delete!",
                    closeOnConfirm: false
                }, function(){

                	deleteUser(e);

                	// swal("Deleted!", "Your record has been deleted.","success");

               	 //deleteUser(e);

                });

         }

	/* 	deleting user */
			function deleteUser(e) {
				 var row = $(e).closest('tr')[0];
				var id = $(row).find('td:eq(0)').text();
				//var id=  $("#input").val();
				//alert(id);
				$.ajax({
					url : "/api/users/user/delete/" + id,
					method : 'POST'

				}).done(function(resultData) {

					//alert(resultData);

					//swal("Deleted!", "Your record has been deleted.", "success"){

		   				// getUserList();


					//}

					swal({
                         title: "Deleted!",
                         text: "Your record has been Deleted.",
                         type: "success",
                         showCancelButton: false,
                         confirmButtonText: "Ok",
                         closeOnConfirm: true
                     }, function(){


		   				 getUserList();

     					//alert("hi");

                         //swal("Deleted!", "Your imaginary file has been deleted.", "success");
                     });

					 //getUserList();
					//$(row).remove();
				});
			}







		function addUser(e){

       	 $("#loading").show();



       	// var firstName=$("#firstName").val();

       	 //var lastName=$("#lastName").val();
       	 var name=$("#name").val();


       	 var email=$("#email").val();

       	 //var phoneNumber = $("#phoneNumber").val();
       	 var username = $("#username").val();


       	 //var blockStatus=$("#blockStatus").val();

       	 //var twofAuthStatus = $("#twofAuthStatus").val();



       	 //var confirmEmail=$("#confirmEmail").val();


       	 //var password=$("#password").val();
       	 //var confirmPassword=$("#confirmPassword").val();

       	 var role=$("#role").val();

       	 //var roleId=$("#role").val();

//       	 var roleText=$("#role option:selected" ).text();
//
//
//       	 var	roleObject = {
//       			id: roleId,
//	            name:roleText
//	        }
//
//       	var department=$("#department").val();
       //	var departmentId=$("#department").val();


      /*  var	departmentObject = {
	            departmentId: departmentId,
	            departmentName: ""
	        } */


            var UserObj = {};

//            UserObj["firstName"] = firstName;
//            UserObj["lastName"] = lastName;
            UserObj["name"] = name;

            UserObj["email"] = email;

//            UserObj["phoneNumber"] = phoneNumber;

            UserObj["username"] = username;



//            if(blockStatus=="true"){
//
//                UserObj["blocked"] = true;
//
//            }else{
//
//                UserObj["blocked"] = false;
//
//            }
//
//            if(twofAuthStatus=="true"){
//
//            	UserObj["twofAuth"] = true;
//
//            }else{
//
//            	UserObj["twofAuth"] = false;
//
//            }

            //UserObj["confirmEmail"] = confirmEmail;
           // UserObj["password"] = password;
           // UserObj["confirmPassword"] = confirmPassword;
            UserObj["access"] = role;

//            UserObj["roleObject"] = roleObject;
//
//            UserObj["department"] = department;
//
//            UserObj["clientIp"]=$("#clientIp").val();




			if(name!="" && username!="" && email!="" && role!=""){

            $.ajax({
                'url': "/api/users/user",

                'method': "POST",

                'data': JSON.stringify(UserObj),

                'contentType' : 'application/json',


            }).done( function(data) {

        		//$('#id').html("Count");
            	//alert(data.status);

           	 $("#loading").hide();

    		 $('#con-close-modal').modal('hide');

    		var tp
    		 if(data.status=="00"){

    			 tp = "success"

    		 }else{

    			 tp = "warning"
    		 }
    		 console.log(tp);
    		// getUserList();

    			swal({
                         title: "Alert!",
                         text: data.message,
                         type: tp,
                         showCancelButton: false,
                         confirmButtonText: "Ok",
                         closeOnConfirm: true
                     }, function(){

                    	 getUserList();
		   				// getUserList();

     					//alert("hi");

                         //swal("Deleted!", "Your imaginary file has been deleted.", "success");
                     });

    		// getUserList();

            });

			}

            }