package com.sid.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.sid.models.Reels;
import com.sid.models.User;
import com.sid.repository.ReelsRepository;

@Service
public class ReelsServiceImplementations implements ReelsService{

	@Autowired
	private ReelsRepository reelsRepository;
	
	@Autowired
	private Userservice userService;
	
	
	@Override
	public Reels createReel(Reels reel, User user) {
		Reels createReel = new Reels();
		createReel.setTitle(reel.getTitle());
		createReel.setVideo(reel.getVideo());
		createReel.setUser(user);
		return reelsRepository.save(createReel);
	}

	@Override
	public List<Reels> findAllReels() {
		return reelsRepository.findAll();
	}

	@Override
	public List<Reels> findUsersReels(Integer userId) throws Exception {
	    userService.findUserbyid(userId);
	    return reelsRepository.findByUserId(userId);
	}

}
