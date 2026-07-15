package com.sid.models;

import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonIgnore;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class Message {
	@Id
	@GeneratedValue(strategy =  GenerationType.AUTO)
	private Integer id;
	
	private String content;
	private String image;
	@ManyToOne
	private User user;
	@JsonIgnore
	@ManyToOne
	private Chat chat;
	
	
	public Integer getId() {
		return id;
	}


	public void setId(Integer id) {
		this.id = id;
	}


	public User getUser() {
		return user;
	}


	public void setUser(User user) {
		this.user = user;
	}


	public Chat getChat() {
		return chat;
	}


	public void setChat(Chat chat) {
		this.chat = chat;
	}


	private LocalDateTime timestamp;


	public String getContent() {
		return content;
	}


	public Message() {
		
	}

	

	public Message(Integer id, String content, String image, User user, Chat chat, LocalDateTime timestamp) {
		super();
		this.id = id;
		this.content = content;
		this.image = image;
		this.user = user;
		this.chat = chat;
		this.setTimestamp(timestamp);
	}


	public void setContent(String content) {
		this.content = content;
	}


	public String getImage() {
		return image;
	}


	public void setImage(String image) {
		this.image = image;
	}


	public LocalDateTime getTimestamp() {
		return timestamp;
	}


	public void setTimestamp(LocalDateTime timestamp) {
		this.timestamp = timestamp;
	}


	

}
