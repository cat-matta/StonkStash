//Made 10/12/20
const axios = require('axios');

const urlPrefix = "https://finnhub.io/api/v1";

/** Makes an API call to get a price quote for a single stock.
 *@pre  The ticker symbol provided is valid/in play in the stonk market.
 *@post  Data regarding the given ticker symbol's prices will be returned.
 *@param  sym  A string, representing the ticker symbol the user wishes to investigate.
 *@return  A JSON of prices for the given stock, with Opening Price, Highest Daily Price, Daily Lowest
 *		Price, Current Price, Previous Closing Price, and Time (in ms), represented by the names
 *      'o', 'h', 'l', 'c', 'pc', and 't', respectively. If symbol is invalid or there is an issue,
 *      Undefined will be returned instead. */
function getStockQuote(sym) {
	// MAke call
	
	// validate the input?
	
	const apiCallUrl = urlPrefix + '/quote'
	axios({
		"method":"GET",
		"url": apiCallUrl,
		"params": {
			symbol: sym,
			token: process.env.FINNHUB_KEY
		}
	})
	.then(res => {
		console.log(res.data);
		return res.data;
	})
	.catch(err => { 
		console.log(err);
		return undefined;
	});
	// .then
	// .catch // stupid!
	
}


function setSubscription(dunno, lmao) {
	
}

function unsetSubscription(dunno, lmaoo) {
	
}