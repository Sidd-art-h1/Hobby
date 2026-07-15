package com.sid.models;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;

@Entity
@Table(name ="userdata")
public class User {
	
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Integer id;
	private String firstname;
	private String lastname;
	private String email;
	private String password;
	private List<Integer>followers = new ArrayList<>();
	private List<Integer> following = new ArrayList<>();
	@JsonIgnore
	@ManyToMany
	private List<Post>savedPost = new ArrayList<>();
	private String gender;
	public User() {
		
	}



	public User(Integer id, String firstname, String lastname, String email, String password, List<Integer> followers,
			List<Integer> following, List<Post> savedPost, String gender) {
		super();
		this.id = id;
		this.firstname = firstname;
		this.lastname = lastname;
		this.email = email;
		this.password = password;
		this.followers = followers;
		this.following = following;
		this.savedPost = savedPost;
		this.gender = gender;
	}





	public Integer getId() {
		return id;
	}


	public void setId(Integer id) {
		this.id = id;
	}


	public String getFirstname() {
		return firstname;
	}

	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}

	public String getLastname() {
		return lastname;
	}

	public void setLastname(String lastname) {
		this.lastname = lastname;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}


	public List<Integer> getFollowers() {
		return followers;
	}


	public void setFollowers(List<Integer> followers) {
		this.followers = followers;
	}


	public List<Integer> getFollowing() {
		return following;
	}


	public void setFollowing(List<Integer> following) {
		this.following = following;
	}


	public String getGender() {
		return gender;
	}


	public void setGender(String gender) {
		this.gender = gender;
	}


	public List<Post> getSavedPost() {
		return savedPost;
	}


	public void setSavedPost(List<Post> savedPost) {
		this.savedPost = savedPost;
	}
	
	
}
