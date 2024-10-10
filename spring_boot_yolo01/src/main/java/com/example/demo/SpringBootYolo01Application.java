package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
@ComponentScan(basePackages="spring.yolo")
@SpringBootApplication
public class SpringBootYolo01Application {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootYolo01Application.class, args);
	}

}
