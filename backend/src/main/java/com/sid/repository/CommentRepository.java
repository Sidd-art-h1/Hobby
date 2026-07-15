package com.sid.repository;
import org.springframework.data.jpa.repository.JpaRepository;

import com.sid.models.comment;

public interface CommentRepository extends JpaRepository<comment,Integer>{

}
