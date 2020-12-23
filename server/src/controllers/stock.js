// Made 10/12/20
// Controller relating to stock data (unsure yet if local info or finnhub data calls)
const router = require('express').Router();

// api/stocks/getUserStocks  POST
/** Used to get a User's currently owned stocks.
 *@pre  A valid User has arrived at the Dashboard Page.
 *@post  An array of the User's owned stocks will be returned.
 *@param  user_id  The DB id of the given user (NOT FINAL)    
 *@return  An array of owned stocks is returned if User exists AND
 *		they own stock. Otherwise, return undefined.
*/
router.post('/getUserStocks', (req, res) => {
	
	
	const dummyStocks = [
		{ symbol: 'ATX', qty: 100, lastPrice: 5 },
		{ symbol: 'DUB', qty: 200, lastPrice: 20 } 
		];
	const dummyRetData = {  
		stocks: dummyStocks,
		msg: "Successful Stonk Retrieval"};
	res.status(200).json(dummyRetData);
});
module.exports = router;
