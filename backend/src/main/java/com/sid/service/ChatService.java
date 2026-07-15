package com.sid.service;

import java.util.List;

import com.sid.models.Chat;
import com.sid.models.User;

public interface ChatService {
	
	public Chat createChat(User reqUser,User user2);
	
	public Chat findChatById(Integer chatId) throws Exception;
	
	public List<Chat> findUsersChat(Integer userId);
}
