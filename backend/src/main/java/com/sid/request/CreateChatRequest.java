package com.sid.request;

public class CreateChatRequest {


	private Integer userId;

	public Integer getUserId() {
		return userId;
	}

	public void setUserId(Integer userId) {
		this.userId = userId;
	}

	public CreateChatRequest(Integer userId) {
		super();
		this.userId = userId;
	}

	public CreateChatRequest() {
		
	}
}
