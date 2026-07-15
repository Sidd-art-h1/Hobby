package com.sid.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.sid.models.User;
import com.sid.models.comment;
import com.sid.service.CommentService;
import com.sid.service.Userservice;

@RestController
public class CommentController {
	@Autowired
	private CommentService commentService;
	@Autowired
	private Userservice userService;
	
	@PostMapping("/api/comments/post/{postId}")
	public comment createComment(@RequestBody comment Comment,@RequestHeader("Authorization") String jwt,@PathVariable("postId") Integer postId) throws Exception {
		User user = userService.findUserByJwt(jwt); 
		comment createdcomment = commentService.createComment(Comment, postId, user.getId());
		return createdcomment;
	}
	
	@PutMapping("/api/comments/like/{commentId}")
	public comment likeComment(@RequestHeader("Authorization") String jwt,@PathVariable("commentId") Integer commentId) throws Exception {
		User user = userService.findUserByJwt(jwt); 
		comment createdcomment = commentService.likeComment(commentId, user.getId());
		return createdcomment;
	}
	
	

}
