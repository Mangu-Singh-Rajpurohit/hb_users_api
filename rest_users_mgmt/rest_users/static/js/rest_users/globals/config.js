"user strict"
function serviceConfig($httpProvider, $qProvider, $stateProvider, $resourceProvider)
{
	$resourceProvider.defaults.stripTrailingSlashes = false;
	$qProvider.errorOnUnhandledRejections(false);
	$httpProvider.interceptors.push(function($q, $injector) 
	{
		return {
			'request': function(request) 
			{
				return request;
			},

			'response': function(response) 
			{
				return response;
			},
			
			'responseError' : function(response)
			{
				if (response.status == 401)
				{
					$injector.get('UserSessionService').onLogout();
					$injector.get('$state').go("login");
				}
				return $q.reject(response);
			}
		};
	});
    
	$stateProvider
		.state('proxy-state', {
			url: '/proxy',
			template: "<h3>Loading App...</h3>",
			controller: "AppProxyController",
			controllerAs: "vm"
		})
		.state('login', {
			url: '/login',
			templateUrl: "templates/login",
			controller: "LoginController",
			controllerAs: "vm"
		})
		.state('signup', {
			url: '/signup',
			templateUrl: "templates/signup",
			controller: "RegistrationController",
			controllerAs: "vm"
		})
		.state("landing", {
			url: '/landing',
			templateUrl: "templates/landing",
			controller: "LandingController",
			controllerAs: "vm"
		})
};

var app = angular.module('users_app', ["ui.router", "ngResource", 
			"users_app.services.globals", "users_app.global_controllers",
			"users_app.services", "users_app.controllers"]);
app.config(["$httpProvider", "$qProvider", "$stateProvider", "$resourceProvider", serviceConfig]);