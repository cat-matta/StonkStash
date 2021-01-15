// Function for validating user input during the signup process
const hasLowerCase = new RegExp("(?=.*[a-z])");
const hasUpperCase = new RegExp("(?=.*[A-Z])");
const hasNumber = new RegExp("(?=.*[0-9])"); // double check to ensure thats right
const isEmail = new RegExp("/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/"); // sorry for length
const isEmpty = require("is-empty");


/* RETURNS: JSON with fields:
  errors: an object of all the errors generated from user input.
  isValid: a boolean, true if errors is empty, otherwise false */
module.exports = function SignupValidation(data) {

  /** 01/15/21: For now, everything here (the specified limitations) are a WORK IN PROGRESS
   * until we actually discuss and decide the whats and whys of registration field conditions.
   */

    let errors = {};

    // Convert empty fields to an empty string so we can use validator functions
    const username = !isEmpty(data.username) ? data.username : "";
    const email = !isEmpty(data.email) ? data.email : "";
    const email2 = !isEmpty(data.email2) ? data.email2 : "";
    const password = !isEmpty(data.password) ? data.password : "";
    const password2 = !isEmpty(data.password2) ? data.password2 : "";
    

    // Username Check
    if(username === "") {
      errors.username = "Username is a required field, cannot be empty.\n";
    }
    else if(username.len < 5 && username.len > 14) {
      errors.username = "Username are required to have at least 5 chars, and at most 14.\n";
    }

    // Email Check
    if(email === "") {
      errors.email = "Email is a required field, cannot be empty.\n";
    } else if(!isEmail.test(email)) {
      errors.email = "Email is not in the format of an email. Double check.\n";
    }

    // Email2 Check
    if(email2 !== email) { errors.email2 = "Confirm Email field doesn't match the Email field.\n"; }

    // Password Check
    if(password === "") {
      errors.password = "Password is a required field, cannot be empty.\n";
    } else {
      if(!hasLowerCase.test(password)) {
        const msg = "Password must contain a single lowercase character."
        errors.password = errors.password == undefined ? msg : errors.password += " " + msg;
      }
      if(!hasUpperCase.test(password)) {
        const msg = "Password must contain a single Uppercase character."
        errors.password = errors.password == undefined ? msg : errors.password += " " + msg;
      }
      if(!hasNumber.test(password)) {
        const msg = "Password must contain a single Numeric character."
        errors.password = errors.password == undefined ? msg : errors.password += " " + msg;
      }
    }

    // Password 2 Check
    if(password2 !== password) { errors.password2 = "Confirm Password field doesn't match the Password field.\n"; }

    if(!isEmpty(errors)) {
      console.log("One or more problems present with input.");
      console.log(errors);
    }

    return {
        errors,
        isValid: isEmpty(errors)
    };
}