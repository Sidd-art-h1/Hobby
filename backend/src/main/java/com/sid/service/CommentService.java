package com.sid.service;

import com.sid.models.comment;

public interface CommentService {
	
	public comment createComment (comment Comment,Integer postId, Integer userId) throws Exception;
	
	public comment findCommentById(Integer commentId)throws Exception;
	
	public comment likeComment(Integer CommentId, Integer userId) throws Exception;
	


}
