package com.sid.service;

import java.time.LocalDateTime;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.sid.models.Post;
import com.sid.models.User;
import com.sid.models.comment;
import com.sid.repository.CommentRepository;
import com.sid.repository.PostRepository;


@Service
public class CommentServiceImplementation implements CommentService {

	@Autowired
	private PostService postService;
	
	@Autowired
	private Userservice userService;
	
	@Autowired
	private CommentRepository commentRepository;
	
	@Autowired
	private PostRepository postRepository;
	
	@Override
	public comment createComment(comment Comment, Integer postId, Integer userId) throws Exception {
		User user = userService.findUserbyid(userId);
		
		Post post = postService.findPostById(postId);

		Comment.setUser(user);
		Comment.setContent(Comment.getContent());
		Comment.setCreatedAt(LocalDateTime.now());
		
		comment savedcomment = commentRepository.save(Comment);
		post.getComments().add(savedcomment);
		postRepository.save(post);
		
		return savedcomment;
	}
	
	@Override
	public comment findCommentById(Integer commentId)throws Exception {
		Optional<comment> opt = commentRepository.findById(commentId);
		if(opt.isEmpty()) {
			throw new Exception("comment not exist");
		}
		return opt.get();
	}

	
	@Override
	public comment likeComment(Integer CommentId, Integer userId) throws Exception {
		comment Comment = findCommentById(CommentId);
		User user = userService.findUserbyid(userId);
		
		if(!Comment.getLiked().contains(user)) {
			Comment.getLiked().add(user);
		}
		else Comment.getLiked().remove(user);
		
		return commentRepository.save(Comment);

	
}

	
	}

