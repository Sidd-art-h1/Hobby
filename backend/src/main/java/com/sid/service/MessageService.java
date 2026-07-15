package com.sid.service;

import java.util.List;

import com.sid.models.Message;
import com.sid.models.User;

public interface MessageService {
	
	public Message createMessage(User user,Integer chatId, Message req) throws Exception;
	
	public List<Message> findChatsMessages(Integer chatId) throws Exception;



	
	
}
