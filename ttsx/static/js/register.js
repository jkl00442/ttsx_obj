// $(function(){
//
// 	var error_name = false;
// 	var error_password = false;
// 	var error_check_password = false;
// 	var error_email = false;
// 	var error_check = false;
//
//
//
// 	$('#user_name').blur(function() {
// 		check_user_name();
// 	});
//
// 	$('#pwd').blur(function() {
// 		check_pwd();
// 	});
//
// 	$('#cpwd').blur(function() {
// 		check_cpwd();
// 	});
//
// 	$('#email').blur(function() {
// 		check_email();
// 	});
//
// 	$('#allow').click(function() {
// 		if($(this).is(':checked'))
// 		{
// 			error_check = false;
// 			$(this).siblings('span').hide();
// 		}
// 		else
// 		{
// 			error_check = true;
// 			$(this).siblings('span').html('请勾选同意').show();
// 		}
// 	});
//
//
// 	function check_user_name(){
// 		var len = $('#user_name').val().length;
// 		if(len<5||len>20)
// 		{
// 			$('#user_name').next().html('请输入5-20个字符的用户名').show();
// 			error_name = true;
// 		}
// 		else
// 		{
// 			$('#user_name').next().hide();
//
//             $.get('/user/check_name_2/', {'u_name': $('#user_name').val()}, function (data) { // {'list':{'has':1}}
//                 // alert(data.list.has)
//                 if(data.list.has==1){
//                     $('#user_name').next('span').html('用户名已存在').show();
//                     error_name = true;
//                 }
//                 else{
//                     $('#user_name').next('span').html('用户名可用').show();
//                     error_name = false;
//                 }
//             });
// 			// error_name = false;
// 		}
// 	}
//
// 	function check_pwd(){
// 		var len = $('#pwd').val().length;
// 		if(len<8||len>20)
// 		{
// 			$('#pwd').next().html('密码最少8位，最长20位').show();
// 			error_password = true;
// 		}
// 		else
// 		{
// 			$('#pwd').next().hide();
// 			error_password = false;
// 		}
// 	}
//
//
// 	function check_cpwd(){
// 		var pass = $('#pwd').val();
// 		var cpass = $('#cpwd').val();
//
// 		if(pass!=cpass)
// 		{
// 			$('#cpwd').next().html('两次输入的密码不一致').show();
// 			error_check_password = true;
// 		}
// 		else
// 		{
// 			$('#cpwd').next().hide();
// 			error_check_password = false;
// 		}
//
// 	}
//
// 	function check_email(){
// 		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
//
// 		if(re.test($('#email').val()))
// 		{
// 			$('#email').next().hide();
// 			error_email = false;
// 		}
// 		else
// 		{
// 			$('#email').next().html('你输入的邮箱格式不正确').show();
// 			error_check_password = true;
// 		}
//
// 	}
//
//
// 	// 表单提交这个id根本没写
// 	$('#reg_form').submit(function() {
// 		check_user_name();
// 		check_pwd();
// 		check_cpwd();
// 		check_email();
//
// 		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
// 		{
// 			return true;
// 		}
// 		else
// 		{
// 			return false;
// 		}
//
// 	});
//
// });



$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;


	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#user_name').focus(function() {
		$(this).next().hide();
	});


	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#pwd').focus(function() {
		$(this).next().hide();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#cpwd').focus(function() {
		$(this).next().hide();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#email').focus(function() {
		$(this).next().hide();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		//数字字母或下划线
		var reg = /^[a-zA-Z0-9_]{5,15}$/;
		var val = $('#user_name').val();

		if(val==''){
			$('#user_name').next().html('用户名不能为空！').show();
			error_name = true;
			return;
		}

		if(reg.test(val))
		{
			$('#user_name').next().hide();
			// ajax获取这个用户名是否存在,用get就行
            $.get('/user/check_name_2/', {'u_name': $('#user_name').val()}, function (data) { // {'list':{'has':1}}
                // alert(data.list.has)
                if(data.list.has==1){
                    $('#user_name').next('span').html('用户名已存在').show();
                    error_name = true;
                }
                else{
                    $('#user_name').next('span').html('用户名可用').show();
                    error_name = false;
                }
            });
			// error_name = false;
		}
		else
		{
			$('#user_name').next().html('用户名是5到15个英文或数字，还可包含“_”').show();
			error_name = true;
		}

	}


	function check_pwd(){
		var reg = /^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,22}$/;
		var val = $('#pwd').val();

		if(val==''){
			$('#pwd').next().html('密码不能为空！').show();
			error_password = true;
			return;
		}

		if(reg.test(val))
		{
			$('#pwd').next().hide();
			error_password = false;
		}
		else
		{
			$('#pwd').next().html('密码是6到15位字母、数字，还可包含@!#$%^&*.~字符').show();
			error_password = true;
		}
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致').show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
		var val = $('#email').val();

		if(val==''){
			$('#email').next().html('邮箱不能为空！').show();
			error_email = true;
			return;
		}

		if(re.test(val))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确').show();
			error_email = true;
		}

	}


	$('.reg_form').submit(function() {

		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
		    $.post('register_2', {}, function (data) {

            });
			return true;
		}
		else
		{
			return false;
		}

	});
});