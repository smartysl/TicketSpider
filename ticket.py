import requests
import re
import json
import argparse
class TicketCatcher:
    def __init__(self,fromcity,tocity,date):
        self.fromCity=fromcity
        self.toCity=tocity
        self.fromAirportCode=""
        self.toAirportCode=""
        self.findAirportCode()
        self.date=date
        self.originHtml=""
    def findAirportCode(self):
        html=requests.get("http://airport.anseo.cn/search/",params={"q":self.fromCity}).text
        code=re.findall(r'IATA CODE:(.+?)\"',html)[0]
        self.fromAirportCode=code
        html = requests.get("http://airport.anseo.cn/search/", params={"q": self.toCity}).text
        code = re.findall(r'IATA CODE:(.+?)\"', html)[0]
        self.toAirportCode = code
    def catchTicketPrice(self):
        url="http://flights.ctrip.com/itinerary/api/12808/products"
        data={"flightWay":"Oneway","classType":"ALL","hasChild":False,"hasBaby":False,"searchIndex":1,"airportParams":[{"dcity":self.fromAirportCode,"acity":self.toAirportCode,"dcityname":self.fromCity,"acityname":self.toCity,"date":self.date}]}
        jsonData=json.dumps(data).encode("utf-8")
        payloadHeader = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
            'Host': 'flights.ctrip.com',
            'origin': 'http://flights.ctrip.com',
            'Referer': 'http://flights.ctrip.com/itinerary/oneway/'
        }
        html=requests.post(url=url,data=jsonData,headers=payloadHeader).text
        self.originHtml=html
        return
    def parseTicketInfo(self):
        allData=[]
        jsonDatas=json.loads(self.originHtml)["data"]["routeList"]
        for jsonData in jsonDatas:
            jsonData=jsonData["legs"][0]
            try:
                requiredData={
                    "目的地机场:":jsonData["flight"]["arrivalAirportInfo"]["airportName"],
                    "起飞地机场:":jsonData["flight"]["departureAirportInfo"]["airportName"],
                    "航班号:":jsonData["flight"]["flightNumber"],
                    "航空公司:":jsonData["flight"]["airlineName"],
                    "起飞时间:":jsonData["flight"]["departureDate"],
                    "降落时间:":jsonData["flight"]["arrivalDate"],
                    "价格:":jsonData["cabins"][0]["price"]["price"]
                }
                allData.append(requiredData)
            except:
                pass
        jsonString=json.dumps(allData,indent=4,ensure_ascii=False)
        with open("flyTicket.txt","a") as f:
            f.write(jsonString)
            f.close()
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("fromCity")
    parser.add_argument("toCity")
    parser.add_argument("date")
    args=parser.parse_args()
    t=TicketCatcher(args.fromCity,args.toCity,args.date)
    t.catchTicketPrice()
    t.parseTicketInfo()