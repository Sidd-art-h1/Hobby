package com.sid.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.sid.models.User;

public interface User_Repository extends JpaRepository<User,Integer>{

	
	public User findByEmail(String email);

	
	@Query("select u from User u where u.firstname LIKE %:query% OR u.lastname LIKE %:query% OR u.email LIKE %:query%")
	public List<User> searchUser(@Param("query") String query);
}
