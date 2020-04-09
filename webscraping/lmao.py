import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)

url = 'https://datawrapper.dwcdn.net/H7PJn/8/'
text = requests.get(url).text
raw = (text.split('chartData: "')[1]).split('",')[0]

data = []
rows = raw.split('\\n')
header = rows[0].split('\\t')
for r in range(1,len(rows)):
	column = rows[r].split('\\t')
	site = {}
	for c in range(0,len(column)):
		site[header[c]] = column[c]
	data.append(site)

pp.pprint(data)