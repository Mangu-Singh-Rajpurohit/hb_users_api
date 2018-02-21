"user strict"
function appProxyController($state, UserSessionService, HeartBeatService)
{
	var vm = this;
	vm.session = UserSessionService;
	vm.onInit = function()
	{
		HeartBeatService.isSessionActive
		(
			function(res)
			{
				UserSessionService.onLogin(res);
				$state.go("landing");
			}, 
			function(res)
			{
				if (res.status != 401)
				{
					alert("An internal server has occured, Please try after sometime.");
				}
			}
		);
	};
}

angular.module("users_app.global_controllers", [])
	.controller("AppProxyController", ["$state", "UserSessionService", "HeartBeatService", appProxyController]);
