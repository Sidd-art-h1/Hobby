package com.sid.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.sid.config.JwtProvider;
import com.sid.models.User;
import com.sid.repository.User_Repository;
import com.sid.request.LoginRequest;
import com.sid.response.AuthResponse;
import com.sid.service.CustomUserDetailsService;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;

@RestController
@RequestMapping("/auth")
public class AuthController {

	@Autowired
	private User_Repository userRepository; 
	@Autowired
	private PasswordEncoder passwordEncoder;
	@Autowired
	private CustomUserDetailsService customUserDetails;
	
	@PostMapping("/signup")
	public AuthResponse createUser(@RequestBody User user) throws Exception {
		
		User isExist = userRepository.findByEmail(user.getEmail());
		
		if(isExist!=null) {
			throw new Exception("this email is already used with another account");
		}
		User newUser = new User();
		newUser.setEmail(user.getEmail());
		newUser.setFirstname(user.getFirstname());
		newUser.setLastname(user.getLastname());
		newUser.setPassword(passwordEncoder.encode(user.getPassword()));
		
		User saveduser = userRepository.save(newUser);
		
		Authentication authentication = new UsernamePasswordAuthenticationToken(saveduser.getEmail(),saveduser.getPassword());
		String token = JwtProvider.generateToken(authentication);
		AuthResponse res = new AuthResponse(token,"Register Success");
		return res;
}
	@PostMapping("/signin")
	public AuthResponse signin(@RequestBody LoginRequest loginRequest) throws Exception {
		Authentication authentication = authenticate(loginRequest.getEmail(), loginRequest.getPassword());
		String token = JwtProvider.generateToken(authentication);
		AuthResponse res = new AuthResponse(token,"Login Success");
		return res;
	} 
	
	private Authentication authenticate (String email, String password) throws Exception {
		UserDetails userDetails = customUserDetails.loadUserByUsername(email);
		
		if(userDetails == null) {
			throw new BadCredentialsException("invalid username");
		}
		if(!passwordEncoder.matches(password,userDetails.getPassword())) {
			throw new BadCredentialsException("password not matched");
		}
		
		return new UsernamePasswordAuthenticationToken(userDetails,null,userDetails.getAuthorities());
	}
}
