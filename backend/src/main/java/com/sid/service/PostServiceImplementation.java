package com.sid.service;


import java.time.LocalDateTime;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.sid.models.Post;
import com.sid.models.User;
import com.sid.repository.PostRepository;
import com.sid.repository.User_Repository;

@Service
public class PostServiceImplementation implements PostService{
	
	@Autowired
	PostRepository postRepository;
	@Autowired
	Userservice userService;
	@Autowired
	User_Repository userRepository;

	@Override
	public Post createNewPost(Post post, Integer userId) throws Exception {
		
		
		User user = userService.findUserbyid(userId);
		Post newPost = new Post();
		newPost.setCaption(post.getCaption());
		newPost.setImage(post.getImage());
		newPost.setCreatedAt(LocalDateTime.now());
		newPost.setVideo(post.getVideo());
		newPost.setUser(user);
		
		return postRepository.save(newPost);
	}

	@Override
	public String deletePost(Integer postId, Integer userId) throws Exception {
		Post post = findPostById(postId);
		User user = userService.findUserbyid(userId);
		
		if (post.getUser() == null || !post.getUser().getId().equals(user.getId())) {
			throw new Exception("you cannot delete this post");
		}
		
		postRepository.delete(post);
		return "Post deleted successfully";
	}

	@Override
	public List<Post> findPostByUserId(Integer userId) {
		
		return postRepository.findPostByUserId(userId);
	}

	@Override
	public Post findPostById(Integer postId) throws Exception {
		Optional<Post> otp = postRepository.findById(postId);
		if(otp.isEmpty()) {
			throw new Exception("post not found with id"+postId);
		}
		return otp.get();
	}

	@Override
	public List<Post> findAllPost() {
		return postRepository.findAll();
	}

	@Override
	public Post savedPost(Integer postId, Integer userId) throws Exception {
		Post post = findPostById(postId);
		User user = userService.findUserbyid(userId);
		
		if(user.getSavedPost().contains(post)) {
			user.getSavedPost().remove(post);
		}
		else user.getSavedPost().add(post);
		userRepository.save(user);
		return post;
	}

	@Override
	public Post likePost(Integer postId, Integer userId) throws Exception {
		Post post = findPostById(postId);
		User user = userService.findUserbyid(userId);
		
		if(post.getLiked().contains(user)) {
			post.getLiked().remove(user);
		}
		else {
			post.getLiked().add(user);
		}
		return postRepository.save(post);
	}
}
