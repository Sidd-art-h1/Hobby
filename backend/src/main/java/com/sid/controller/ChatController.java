package com.sid.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.sid.models.Chat;
import com.sid.models.User;
import com.sid.request.CreateChatRequest;
import com.sid.service.ChatService;
import com.sid.service.Userservice;

@RestController
public class ChatController {
	@Autowired
	private ChatService chatService;
	
	@Autowired
	private Userservice userService;
	
	@PostMapping("/api/chats")
	public Chat createChat(@RequestHeader("Authorization")String jwt,@RequestBody CreateChatRequest req) throws Exception {
		User reqUser = userService.findUserByJwt(jwt);
		User user2 = userService.findUserbyid(req.getUserId());
		Chat chat = chatService.createChat(reqUser, user2);
		
		return chat;
	}
	
	@GetMapping("/api/chats")
	public List<Chat> findUsersChat(@RequestHeader("Authorization")String jwt) {
		User user = userService.findUserByJwt(jwt);
		List<Chat> chat = chatService.findUsersChat(user.getId());
		return chat;
	}
	
	
}
