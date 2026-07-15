package com.sid.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController	
public class HomeController {
	
	@GetMapping
	public String homeControllerHandler() {
		return"This is HomeController";
		
	}
	
	@GetMapping("/home")
	public String homeControllerHandler2() {
		return"This is HomeController 2";
		 
	}
	
	@GetMapping("/sid")
	public String homeControllerHandler3() {
		return"Hello Sid";
		
	}



}
