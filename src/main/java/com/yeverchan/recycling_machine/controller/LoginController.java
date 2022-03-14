package com.yeverchan.recycling_machine.controller;


import com.yeverchan.recycling_machine.domain.User;
import com.yeverchan.recycling_machine.repository.UserRepository;
import com.yeverchan.recycling_machine.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Controller
public class LoginController {

    @Autowired
    UserService userService;


    @GetMapping("/login")
    public String getLoginPage() {
        return "login";
    }

    @PostMapping("/login")
    public String login(String id, String password, HttpServletRequest request, HttpServletResponse response) {

        if(!loginCheck(id, password)){
            return "redirect:/?false";
        }


        return "redirect:/";
    }

    private boolean loginCheck(String id, String password){
//        try{
//            User user = null;
//            user = userService.getUser(id);
//            return user != null && user.getPassword().equals(password);
//        } catch (Exception e){
//            e.printStackTrace();
//            return false;
//        }

        return true;
    }
}
