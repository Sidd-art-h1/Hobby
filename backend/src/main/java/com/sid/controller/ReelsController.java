package com.sid.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.sid.models.Reels;
import com.sid.models.User;
import com.sid.service.ReelsService;
import com.sid.service.Userservice;

@RestController
public class ReelsController {
	
	@Autowired
	private ReelsService reelsService;
	@Autowired
	private Userservice userService;
	
	@PostMapping("/api/reels")
	public Reels createReels(@RequestBody Reels reel, @RequestHeader("Authorization")String jwt) {
		User reqUser = userService.findUserByJwt(jwt);
		Reels createdReels = reelsService.createReel(reel, reqUser);
		return createdReels;
	}
	
	@GetMapping("/api/reels")
	public List<Reels> findReels( @RequestHeader("Authorization")String jwt) {
		List<Reels> Reels = reelsService.findAllReels();
		return Reels;
	}
	
	@GetMapping("/api/reels/user/{userId}")
	public List<Reels> findUsersReels( @PathVariable Integer userId) throws Exception {

		List<Reels> Reels = reelsService.findUsersReels(userId);
		return Reels;
	}
	
}
