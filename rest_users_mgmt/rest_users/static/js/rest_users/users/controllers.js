"user strict"
function loginController($window, $state, UserSessionService, UsersService)
{
	var vm = this;
	vm.username = "";
	vm.password = "";
	
	vm.onLoginSuccessful = function(resp)
	{
		$window.location.reload();
		//$state.go("landing");
		UserSessionService.onLogin(resp);
	};
	
	vm.onLoginFailed = function()
	{
		alert("Login Failed! Invalid username/password");
	};
	
	vm.validateCredentials = function()
	{
		if (!(vm.username && vm.username.replace(" ", "").length > 0))
		{
			alert("Invalid username");
			return false;
		}
		
		if (!(vm.password && vm.password.replace(" ", "").length > 0))
		{
			alert("Invalid password");
			return false;
		}
		
		return true;
		
	}
	
	vm.loginUser = function()
	{
		if (vm.validateCredentials())
		{
			UsersService.login({username: vm.username, password: vm.password}, 
				vm.onLoginSuccessful, vm.onLoginFailed);
		}
	};
};

function landingController(UserSessionService, UsersService)
{
	var vm = this;
	vm.session = UserSessionService;
	vm.apikey = "";
	
	vm.onApiKeyLoaded = function(resp)
	{
		vm.apikey = resp[0];
	};
	
	vm.onApiKeyRequestFailed = function()
	{
		alert("An error have occured, while requesting api keys");
	};
	
	vm.onInit = function()
	{
		UsersService.getApiKey(vm.onApiKeyLoaded, vm.onApiKeyRequestFailed);
	};
};

function registrationController($state, UsersService)
{
	var vm = this;
	vm.userDtls = {
		username: "",
		password: "",
		email: ""
	}
	
	vm.onRegistrationSuccess = function(resp)
	{
		alert("Your account has been registered successfully. An email has been sent to you for activation of account.");
		
	};
	
	vm.onRegistrationFailed = function(resp)
	{
		var msg = resp.detail || "An error have occured, while registering your account";
		alert(msg);
	};
	
	vm.registerUser = function()
	{
		UsersService.signup
		(
			vm.userDtls, 
			vm.onRegistrationSuccess,
			vm.onRegistrationFailed
		);
	};
};


function changePasswordController(UsersService)
{
	var vm = this;
	vm.passwordDtls = {
		current_password: "",
		new_password: "",
		confirmed_new_password: ""
	};
	
	vm.validatePasswords = function()
	{
		if (!vm.passwordDtls.current_password)
		{
			alert("Blank current password");
			return false;
		}
		
		else if (!vm.passwordDtls.new_password)
		{
			alert("Blank new password");
			return false;
		}
		
		else if (!vm.passwordDtls.confirmed_new_password)
		{
			alert("Blank confirm new password");
			return false;
		}
		
		else if (vm.passwordDtls.new_password != vm.passwordDtls.confirmed_new_password)
		{
			alert("New password and confirm passwords don't match");
			return false;
		}
		
		return true;
	};
	
	vm.onPasswordChange = function(resp)
	{
		alert("Password changed successfully");
	};
	
	vm.onPasswordChangeFailed = function(resp)
	{
		var msg = resp.detail || "An error have occured, while changing password";
		alert(msg);
	};
	
	vm.changePassword = function()
	{
		if (!vm.validatePasswords())
			return;

		UsersService.changePassword(vm.passwordDtls, vm.onPasswordChange, vm.onPasswordChangeFailed);
	};
};

angular.module("users_app.controllers", ["users_app.services", "users_app.services.globals"])
	.controller("LoginController", ["$window", "$state", "UserSessionService", "UsersService", loginController])
	.controller("LandingController", ["UserSessionService", "UsersService", landingController])
	.controller("RegistrationController", ["$state", "UsersService", registrationController])
	.controller("ChangePasswordController", ["UsersService", changePasswordController]);
