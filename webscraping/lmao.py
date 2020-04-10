import requests
import pprint
import csv

pp = pprint.PrettyPrinter(indent=4)

def main():
	data = database()

def database():
	url = 'https://datawrapper.dwcdn.net/H7PJn/8/'
	text = requests.get(url).text
	raw = (text.split('chartData: "')[1]).split('",')[0]
	raw = (raw.replace('\\n\\"','')).replace('\\"','') #bc fuck this

	data = []
	rows = raw.split('\\n')
	header = rows[0].split('\\t')

	num = 0
	for r in range(1,len(rows)):
		column = rows[r].split('\\t')
		site = {}
		for c in range(0,len(header)):
			site[header[c]] = column[c].strip()

		loc = ''
		if ('location' not in rows[r]):
			if site['Address'] != '' and ' ' in site['Address']:
				loc = site['Address']
				if site['City'] != '':
					loc += ' '+site['City']
				loc += ' '+site['State']
				loc = loc.replace(' ','+')
			elif site['Location'] != '':
				loc = site['Location']
				if site['City'] != '':
					loc += ' '+site['City']
				loc += ' '+site['State']
				loc = loc.replace(' ','+')

		if loc != '':
			try:
				lat,lon = location(loc)
				site['Latitude'] = lat
				site['Longitue'] = lon

				print('(%s,%s)' %(lat,lon))
				num += 1
				addToCSV(header, site, num)
				data.append(site)
			except:
				pass
	
	return data

def location(loc):
	loc_url = 'https://www.google.com/maps/search/'+loc
	loc = requests.get(loc_url).text
	return ((loc.split('center=')[1]).split('&amp')[0]).split('%2C')

def addToCSV(header, site, num):
	with open('database.csv', mode='a', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=header)
		if (num == 1):
			writer.writeHeader()
		writer.writerow(site)

if __name__ == '__main__':
	main()