package com.sid.service;

import java.util.List;

import com.sid.models.Reels;
import com.sid.models.User;

public interface ReelsService {
	
	public Reels createReel(Reels reel,User user);
	
	public List<Reels> findAllReels();
	
	public List<Reels> findUsersReels(Integer userId) throws Exception;
	


}
