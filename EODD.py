from bs4 import BeautifulSoup
import requests
import pandas as pd
import string
import os

# This list includes AMEX, ASX, CBOT, CFE, CME, COMEX, EUREX, FOREX, HKEX, INDEX, KCBT, LIFFE, LSE, MGEX, NASDAQ, NYBOT, OTCBB, SGX, TSX, TSXV, USMF, WCE

markets = ['AMEX', 'ASX', 'CBOT', 'CFE', 'CME', 'COMEX', 'EUREX', 'FOREX', 'HKEX', 'INDEX', 'KCBT', 'LIFFE', 'LSE', 'MGEX', 'NASDAQ', 'NYBOT', 'OTCBB', 'SGX', 'TSX', 'TSXV', 'USMF', 'WCE']
def download(market):
	#market = "LSE"
	urlIndex = "http://eoddata.com/stocklist/" + market + ".htm"

	contentIndex = requests.get(urlIndex).content
	soupIndex = BeautifulSoup(contentIndex,'html.parser')
	tableIndex = soupIndex.find('table', {'class': 'lett'})

	dataIndex = [[td.text.strip() for td in tr.findChildren('td')] 
	        for tr in tableIndex.findChildren('tr')]
	dataStr = ''.join(map(str,dataIndex))

	string = dataStr.replace(",","").replace("'","").replace(" ","").replace("[","").replace("]","")

	datalist = []
	for id in range(0,len(string)):
	    url = "http://eoddata.com/stocklist/" + market + "/" + string[id] + ".htm"
	    content = requests.get(url).content
	    soup = BeautifulSoup(content,'html.parser')
	    table = soup.find('table', {'class': 'quotes'})

	    data = [[td.text.strip() for td in tr.findChildren('td')] 
	            for tr in table.findChildren('tr')]
	    datalist.append(data)

	new = []
	for i in range(0,len(string)):
	    new.append(pd.DataFrame(datalist[i]))

	df = pd.concat(new)
	df.drop(df.index[0], inplace=True) # first row is empty
	df.columns = ['Code','Name','High','Low','Close','Volume','Change','','Change (%)','']
	df["Volume"] = pd.to_numeric(df["Volume"].str.replace(",",""))
	df.set_index('Code',inplace=True)
	try:
		os.stat(os.path.expanduser('~') + '/EODD/')
	except:
		os.mkdir(os.path.expanduser('~') + '/EODD/')

	df.to_csv(os.path.expanduser('~') + '/EODD/' + market + '.csv', encoding='utf-8')
