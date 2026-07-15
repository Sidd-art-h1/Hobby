package com.sid.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.sid.models.Post;
import com.sid.models.User;
import com.sid.response.ApiResponse;
import com.sid.service.PostService;
import com.sid.service.Userservice;

@RestController
public class PostController {
	@Autowired
	PostService postService;
	@Autowired
	Userservice userservice;
	
	@PostMapping("/api/posts")
	public ResponseEntity<Post> createPost(@RequestBody Post post,@RequestHeader("Authorization")String jwt) throws Exception{
		User reqUser =userservice.findUserByJwt(jwt);
		Post createdPost = postService.createNewPost(post, reqUser.getId());
		return new ResponseEntity<>(createdPost,HttpStatus.ACCEPTED);
		
	}
	@DeleteMapping("/api/posts/{postId}")
	public ResponseEntity<ApiResponse> deletePost(@PathVariable Integer postId,@RequestHeader("Authorization")String jwt ) throws Exception{
		User reqUser = userservice.findUserByJwt(jwt);
		String message = postService.deletePost(postId, reqUser.getId());
		ApiResponse res = new ApiResponse(message,true);
		return new ResponseEntity<ApiResponse>(res,HttpStatus.OK);
	}
	@GetMapping("/api/post/{postId}")
	public ResponseEntity<Post>findPostByIdHandler(@PathVariable Integer postId) throws Exception{
		Post post = postService.findPostById(postId);
		return new ResponseEntity<Post>(post,HttpStatus.ACCEPTED);
	}
	@GetMapping("/api/post/user/{userId}")
	public ResponseEntity<List<Post>> findUsersPost(@PathVariable Integer userId) throws Exception{
		List<Post>posts = (List<Post>) postService.findPostByUserId(userId);
		return new ResponseEntity<List<Post>>(posts,HttpStatus.OK);
		
	}
	@GetMapping("/api/posts")
	public ResponseEntity<List<Post>> findAllPost(){
		List<Post>posts = postService.findAllPost();
		return new ResponseEntity<List<Post>>(posts,HttpStatus.OK);
		
	}
	@PutMapping("/api/posts/save/{postId}")
	public ResponseEntity<Post> savedPostHandler(@PathVariable Integer postId,@RequestHeader("Authorization")String jwt) throws Exception {
		User reqUser = userservice.findUserByJwt(jwt);
	    Post post = postService.savedPost(postId, reqUser.getId());

	    return new ResponseEntity<Post>(post, HttpStatus.ACCEPTED);
	}

	@PutMapping("/api/posts/like/{postId}")
	public ResponseEntity<Post> likedPostHandler( @PathVariable Integer postId,@RequestHeader("Authorization")String jwt) throws Exception {
		User reqUser = userservice.findUserByJwt(jwt);
	    Post post = postService.likePost(postId, reqUser.getId());

	    return new ResponseEntity<Post>(post, HttpStatus.ACCEPTED);
	}
}
