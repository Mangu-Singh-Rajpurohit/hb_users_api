"user strict"
function appProxyController($state, $interval, $window, UserSessionService, HeartBeatService)
{
	var vm = this;
	vm.session = UserSessionService;
	
	function onHeartBeatFailedForLoggedInUser()
	{
		$window.reload();
	}
	
	vm.checkHeartBeat = function(successcb, failurecb)
	{
		HeartBeatService.isSessionActive(successcb, failurecb);
	};
	
	vm.checkHeartBeatForLoggedInUser = function()
	{
		if (UserSessionService.isAuthenticated())
		{
			vm.checkHeartBeat(null, onHeartBeatFailedForLoggedInUser);
		}
	}
	
	vm.onInit = function()
	{
		vm.checkHeartBeat
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
	
	$interval(vm.checkHeartBeatForLoggedInUser, 15000);
}

angular.module("users_app.global_controllers", [])
	.controller("AppProxyController", ["$state", "$interval", "$window", "UserSessionService", "HeartBeatService", appProxyController]);
