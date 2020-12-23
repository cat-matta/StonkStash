// Made 10/11/20
// The controller for Authentication of Users
const router = require('express').Router();
//const User = require('../models/User');
//const validateSignupInput = require("../validation/signup");
//const passport = require('../middlewares/authentication');


// A Fake signup route
router.post('/signup-v0', (req, res) => {

  try {
    res.status(201).json({msg: "Signup Successful"});
    //const { isValid, errors } = validateSignupInput(req.body)

    //if(!isValid) {
    //  throw(errors)
    //}

    /*User.create({
      username: req.body.username,
      email: req.body.email,
      password: req.body.password,
      phone_number: req.body.phonenumber
    })
      .then((user) => {

        // Shouldn't return the whole damn user!
        req.login(user, () => res.status(201).json(user));
      })
      .catch((err) => {
        const message = err["errors"][0]["message"]

        let errmsg = "Signup Error" 
        if(message == "email must be unique") {
          console.log("Email not Unique")
          errmsg = "Email already in use"
        } else if(message == "username must be unique") {
          console.log("Username not Unique")
          errmsg = "Username already in use"
        } else if(message == "phonenumber must be unique") {
          console.log("Phonenumber not Unique")
          errmsg = "Phone number already in use"
        } else if(message == "Validation len on password failed") {
          console.log("PW Too Short")
          errmsg = "Password too short."
        }      
        res.status(400).json({ msg: errmsg });
      }); */
    }
    catch(err) {
      console.log(err)
      res.status(400).json({msg: "Signup Error"})
    }
});

/*
router.post('/login',
  passport.authenticate('local'),
  (req, res) => {
	  /*
    console.log("Begin?")
    // If this function gets called, authentication was successful.
    // `req.user` contains the authenticated user.
   // console.log(req.user)
    res.json(req.user); 
	res.status(200).json({msg:"Login Successful"});
  }); */

// A Fake login route
 router.post('login-v0', (req, res) => {
	 res.status(200).json({msg:"Fake Login Successful"});
 });
 
// A Fake logout route
router.post('/logout-v0', (req, res) => {
  //req.logout();
  res.status(200).json({ message: "Fake Logout Successful" });
})

module.exports = router;

