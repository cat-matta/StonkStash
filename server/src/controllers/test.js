// Made 10/11/20
// A route controller for testing api calls working, period.
const router = require('express').Router();

// Literally the test route
router.get('/routetest', (req, res) => {
	res.status(200).json({msg:"Successful API Call"});
})

module.exports = router;
