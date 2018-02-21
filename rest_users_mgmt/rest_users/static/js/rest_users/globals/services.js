"user strict"
function UserSessionService()
{
	var svc = this;
	svc.userDtls = null;
	svc.isLoggedIn = false;
	
	svc.getUserDtls = function()
	{
		return svc.userDtls;
	};
	
	svc.setUserDtls = function(userDtls)
	{
		svc.userDtls = userDtls;
	};
	
	svc.onLogin = function(resp)
	{
		svc.isLoggedIn = true;
		svc.setUserDtls(resp);
	};
	
	svc.isAuthenticated = function()
	{
		if (svc.isLoggedIn)
		{
			return true;
		}
		return false;
	};
	
	svc.cleanAuthenticationFlag = function()
	{
		svc.isLoggedIn = false;
	};
	
	svc.onLogout = function(resp)
	{
		svc.setUserDtls(null);
		svc.cleanAuthenticationFlag();
	};
};

function heartBeatService($resource)
{
	return $resource("/users/heartbeat/", {}, {
		isSessionActive: {
			method: "GET"
		}
	});
};

angular.module("users_app.services.globals", [])
		.service("UserSessionService", [UserSessionService])
		.service("HeartBeatService", ["$resource", heartBeatService]);
