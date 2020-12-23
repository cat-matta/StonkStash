const router = require('express').Router();
// top text?
router.get('/getUser', (req, res) => { 
	// DONT USE THIS IT MAKES NO SENSE IT WAS JUST FOR ROUTE TESTING AGAIN
	res.status(200).json({msg: "bababooey"});
	});
	
	
module.exports = router;
