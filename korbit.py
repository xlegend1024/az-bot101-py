import requests
import json
import datetime

def orderdetils(data):
    msg =''

    for i in range(len(data)):
        price = float(data[i][0])
        amount = float(data[i][1])
        volume = float(price * amount)
        msg = msg + "Price: {0:06.2f} Amount: {1:06.2f} Vol: {2:06.2f} \n\r".format(price, amount,volume)

    return msg


def orderbookasks(pair):
    url = "https://api.korbit.co.kr/v1/orderbook"
    param1 = "currency_pair="+pair
    req = url + str('?') + param1
    res = requests.get(req)
    return orderdetils((res.json())['asks'])


def orderbookbids(pair):
    url = "https://api.korbit.co.kr/v1/orderbook"
    param1 = "currency_pair="+pair
    req = url + str('?') + param1
    res = requests.get(req)
    return orderdetils((res.json())['bids'])


def filldedorder(pair):
    url2 = 'https://api.korbit.co.kr/v1/transactions'
    param2 = 'currency_pair='+pair
    req = url2 + str('?') + param2
    res2=requests.get(req)
    data=res2.json()
    return filledorderdetail(data)

def filledorderdetail(data):
    stdprice = 0.0
    status = 'EQ'
    returnmsg=''

    for i in range(len(data)):
        #datetime.datetime.fromtimestamp(float(s)/1000.)
        dealtime = datetime.datetime.fromtimestamp(float(data[i]['timestamp'])/1000.0)
        tid = int(data[i]['tid'])
        price = float(data[i]['price'])
        amount = float(data[i]['amount'])
        if stdprice == 0.0:
            status = 'EQ'
            stdprice = price
        elif stdprice > price:
            status = 'UP'
            stdprice = price
        elif stdprice < price:
            status = 'DN'
            stdprice = price
        elif stdprice == price:
            status = 'EQ'
            stdprice = price
        
        msg = "{0} Price {1:06.2f} Amount {2:06.2f} Status: {3} ".format(dealtime, price, amount,status)
        returnmsg = returnmsg + msg + ' \n\r'
    return returnmsg
