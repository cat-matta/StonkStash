
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
}

loginCall = data => {

}

