package com.sid.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sid.models.Post;

public interface PostRepository extends JpaRepository<Post,Integer> {

	Optional<Post> findById(Integer postId);

	List<Post> findPostByUserId(Integer userId);

	List<Post> findAll();

	Post save(Post post);

	void delete(Post post);



}
