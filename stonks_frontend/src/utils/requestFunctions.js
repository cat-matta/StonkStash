


/** Makes an http request to the backend to register a new user to the app,
 * @post  If registration successful, redirection to Login will be approved.
 * @param data  JSON; Data supplied by the User in order to register their new account.
 * @return  If success, a json object containing approval to proceed, Else, approval to show error message included in json.
 */
async function signupCall(data) {
  let result = {};
  await fetch('/api/signup', {
    method: 'POST',
    body: data
  })
  .then(res => {
    //console.log(res.json())
    result = {
      success: true,
      error: false,
      errmsg: undefined,
      data: res
    }
  })
  .catch(err => {
    console.log(`Error Detected: ${err}.`);
    result = {
      success: false,
      error: true,
      errmsg: err,
    }
  })
  //console.log(`Result is: below`);
  //console.log(result)
  return result; /* ATTENTION: PUT THE RETURNS HERE, NOT INSIDE THE CHAINED FUNCTIONS. DONT SCRATCH YOUR HEAD FOR HOURS OVER THIS */
}

async function loginCall(data) {

};

module.exports = { signupCall, loginCall };

