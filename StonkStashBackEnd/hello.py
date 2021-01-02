##import sciencestuff as coolbeans
import numpy as np ## feel free to comment this out



'''okay so to calculate the volitility i need you to use these functions with the csv file. I will also provide a definition.

Volitiy is basically how risky a stock is, does it have huge risk? or low risk? thats what volitily will tell us. Below will be a function to help us find volitilty.

Here's a link just in case
https://www.investopedia.com/terms/v/volatility.asp
if you have any questions let me know
DO NOT I REPEAT , DO NOT GO ON WALL ST BETS I SWEAR TO GOD

'''

def riskyboi(arr): ##it will take a list as a input
    riskystocks = np.array(arr);## we basically created a numpy array with np.array
    riskyboicalc = np.std(riskystocks); ## Standard deviation for the array
    '''for this, it should be a simple calculation. All we need is the standard deviation. Also we're gonna be a little conserviative for risk factor. 
    if the std deviation is above 0.5 thats high risk
    else if its lower than 0.5 its low risk '''
    if(riskyboicalc >= 0.5):
        return "This stock is high risk";
    else:
        return "This stock is low risk";

def sharesbought(arr): ##how many shares bought
    volume = np.array(arr);##this will come from the volume dataset
    bought = np.mean(volume);##since its an array we need the average for time period
    return bought;

###BELOW IS JUST TESTS
list = [1,2,3,4,5] 

g = riskyboi(list)
print(g)
g = sharesbought(list)
print(g)
    


print("Hello World")
