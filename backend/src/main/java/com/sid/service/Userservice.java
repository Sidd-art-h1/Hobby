package com.sid.service;

import java.util.List;

import com.sid.models.User;

public interface Userservice {

	public User registerUser(User user);
		
	public User findUserbyid(Integer userId) throws Exception;
	
	public User findUserByEmail(String email);
	
	public User followUser(Integer userId1, Integer userId2) throws Throwable;
	
	public User updateUser(User user,Integer userId) throws Exception;
	
	public List<User> searchUser(String query);
		
	public User findUserByJwt(String jwt);
		
}

