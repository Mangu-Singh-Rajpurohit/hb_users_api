"user strict"
function usersService($resource)
{
	return $resource("/users/", {}, {
		login: {
			url: "/users/session/",
			method: "POST"
		},
		signup: {
			url: "/users/signup/",
			method: "POST"
		},
		getApiKey: {
			url: "/users/token/",
			method: "GET",
			isArray: true
		}
	});
};

angular.module("users_app.services", ["ngResource"])
		.service("UsersService", ["$resource", usersService]);
