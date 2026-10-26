package com.sid.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.sid.config.JwtProvider;
import com.sid.models.User;
import com.sid.repository.User_Repository;

@Service
public class UserserviceImplementation implements Userservice{
	
	@Autowired
	User_Repository userRepository;

	@Override
	public User registerUser(User user) {
		User newUser = new User();
		newUser.setEmail(user.getEmail());
		newUser.setFirstname(user.getFirstname());
		newUser.setLastname(user.getLastname());
		newUser.setPassword(user.getPassword());
		
		User saveduser = userRepository.save(newUser);
		return saveduser;
	}

	@Override
	public User findUserbyid(Integer userId) throws Exception {
		Optional<User> user = userRepository.findById(userId);
		if(user.isPresent()) return user.get();
		throw new Exception("User Doesn't Exist with User-ID  "+userId); 
	}

	@Override
	public User findUserByEmail(String email) {
		User user = userRepository.findByEmail(email);
		return user;
	}

	@Override
	public User followUser(Integer reqUserId, Integer userId2) throws Exception {
		if (reqUserId.equals(userId2)) {
			throw new Exception("You cannot follow yourself");
		}
		User reqUser = findUserbyid(reqUserId);
		User user2 = findUserbyid(userId2);
		if (user2.getFollowers().contains(reqUser.getId())) {
			user2.getFollowers().remove(reqUser.getId());
			reqUser.getFollowing().remove(user2.getId());
		} else {
			user2.getFollowers().add(reqUser.getId());
			reqUser.getFollowing().add(user2.getId());
		}
		
		userRepository.save(reqUser);
		userRepository.save(user2);
		
		return reqUser;
	}

	@Override
	public User updateUser(User user,Integer userId) throws Exception {
		Optional<User> user1 = userRepository.findById(userId);

		if(user1.isEmpty()) throw new Exception("Such a User Doesn't exist with id "+userId);
		
		User Olduser = user1.get();
		
		if(user.getFirstname()!=null) Olduser.setFirstname(user.getFirstname());
		if(user.getLastname()!=null) Olduser.setLastname(user.getLastname());
		if(user.getPassword()!=null) Olduser.setPassword(user.getPassword());
		if(user.getEmail()!=null) Olduser.setEmail(user.getEmail());
		if(user.getGender()!=null) Olduser.setGender(user.getGender());
		
		
		User Updateduser = userRepository.save(Olduser);
		return Updateduser;

	}

	@Override
	public List<User> searchUser(String query) {
		return userRepository.searchUser(query);
	}
	
	@Override
	public User findUserByJwt(String jwt) {
		String email = JwtProvider.getEmailFromJwtToken(jwt);
		
		User user  = userRepository.findByEmail(email);
		return user;

	}
	
	

}
