package com.sid.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.sid.models.User;
import com.sid.repository.User_Repository;
import com.sid.service.Userservice;

@RestController
public class UserController {
	
	@Autowired
	User_Repository userrepository;
	
	@Autowired
	Userservice userservice;
	

	
	@GetMapping("/api/users")
	public List<User> getUsers() {
		
		List<User> users = userrepository.findAll();
		return users;
	}



	@GetMapping("/api/users/{userId}")
	public User getUsersbyId(@PathVariable("userId")Integer id) throws Exception {
		User user = userservice.findUserbyid(id);
		return user;
		
	}
	
	

	@PutMapping("/api/users")
	public User updateUser(@RequestHeader("Authorization")String jwt,@RequestBody User user ) throws Exception{
		User reqUser = userservice.findUserByJwt(jwt);
		User updateduser = userservice.updateUser(user,reqUser.getId());
		return updateduser;
		

	}
	
	@PutMapping("/api/users/follow/{userId2}")
	public User followUserHandler(@RequestHeader("Authorization")String jwt, @PathVariable Integer userId2) throws Throwable {
		User reqUser = userservice.findUserByJwt(jwt);
		User user = userservice.followUser(reqUser.getId(), userId2);
		return user;
		
	}
	@GetMapping("/api/users/search")
	public List<User>searchUser(@RequestParam("query") String query){
		List<User> users = userservice.searchUser(query);
		return users;
	}
	@GetMapping("/api/users/profile")
	public User getUserFromToken(@RequestHeader("Authorization")String jwt) {
		
		//String email = 
		System.out.println("jwt  ----- "+jwt);
		User user =userservice.findUserByJwt(jwt);
		user.setPassword(null);
		return user;
	}
	
}

