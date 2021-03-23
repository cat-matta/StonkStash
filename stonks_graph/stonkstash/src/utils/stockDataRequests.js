/** Acquire the data to display on the Dashboard Graph.
 *  @param  symbol  {String}  The stock's ticker symbol
 *  @param  resolution  {String}  {1,5,15,30,60,D,W,M}
 *  @param  endDate  {string??}  The end date of the time period, in "YYYY-MM-DD" format (?)
 *  @param  period  {String}  A character representing the length of the time period desired for display {w, m, q, s, y}
 */
async function getStockInfo(symbol, resolution, endDate, period) {
    
    let result = {};
    await fetch('/stock' + `?symbol=${symbol}&res=${resolution}&end=${endDate}&period=${period}`, {
        method: 'GET',
        headers : { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
           }
    })
    .then(res => {
        console.log(res.json());
        result = {
            success: true,
            error: false,
            errMsg: undefined,
            data: res
        }
    })
    .catch(err => {
        console.log(`Error Detected: ${err}.`);
        result = {
            success: false,
            error: true,
            err: "Something is wrong"
        }
    })

    return result;
}

module.exports = { getStockInfo };