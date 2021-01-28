

const requestFunctions = {
  /** Makes an http request to the backend to register a new user to the app,
   * @post  If registration successful, redirection to Login will be approved.
   * @param data  JSON; Data supplied by the User in order to register their new account.
   * @return  If success, a json object containing approval to proceed, Else, approval to show error message included in json.
   */
  signupCall = data => {
    fetch('/api/signup', {
      method: 'POST',
      body: data
    })
    .then(res => {
      const result = {
        success: true,
        error: false,
        errmsg: undefined,
        data: res.json()
      }
      return result;
    })
    .catch(err => {
      console.log(`Error Detected: ${err}.`);
      const result = {
        success: false,
        error: true,
        errmsg: err,
      }

      return result;
    })
  },

  loginCall = data => {

  }
}

export default requestFunctions;

