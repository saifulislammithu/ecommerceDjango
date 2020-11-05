//Query All input fields
var form_fields = document.getElementsByTagName('input')
if(form_fields.length==2){
	form_fields[1].placeholder='Username..';	
	form_fields[2].placeholder='Enter password...';
		/* for (var field in form_fields){	
			form_fields[field].className += ' form-control'
		} */
}else{
	form_fields[1].placeholder='Username..';
	form_fields[2].placeholder='Email..';
	form_fields[3].placeholder='First Name..';
	form_fields[4].placeholder='Enter password...';
	form_fields[5].placeholder='Re-enter Password...';
}

for (var field in form_fields){
	form_fields[field].className += ' form-control'
	}