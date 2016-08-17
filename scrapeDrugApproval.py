from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen, re

def getMonthlyLinksFromLandingPage(landingPageUrl, domain, depth):
	"This function returns the list of links from the page that has a similar document structure"
	validLinkComparator = ''.join(landingPageUrl[len(domain):].split('/')[:-1])
	#ucm050527
	#'http://www.fda.gov/Drugs/DevelopmentApprovalProcess/HowDrugsareDevelopedandApproved/DrugandBiologicApprovalReports/ANDAGenericDrugApprovals/ucm475633.htm'

	page = urlopen(landingPageUrl).read()
	soup = BeautifulSoup(page, parseOnlyThese=SoupStrainer('a'))

	print ("\n\n\nStart:")
	for link in soup:
		if 'href' in getattr(link, 'attrs', {}) and validLinkComparator == ''.join(link['href'].split('/')[:-1]) and 'default.htm' not in link['href'] and 'ucm050527' not in link['href']:
			print(domain[:-1] + link['href'])
			if depth > 1:
				getMonthlyLinksFromLandingPage(domain[:-1] + link['href'], domain, depth - 1)
			elif depth == 1:
				getDataFromPage(domain[:-1] + link['href'])



	return

def getDataFromPage(url):
	'''This function gets the data from the table on the page for each link'''
	page = urlopen(url).read()
	soup = BeautifulSoup(page, "html.parser")
	table_headers = []

	for tx in soup.find_all('th'):
		print(tx.encode('utf-8'))
		table_headers.append(tx.text)

	#Manually adding an empty first row in case it doesn't exist.
	# if table_headers[0] != u'\xa0':
	# 	table_headers.insert(0, u'\xa0')

	for tr in soup.find_all('tr')[1:]:
	    tds = tr.find_all('td')
	    row = ""
	    for column in range(len(table_headers)):
	    	print(column)
	    	print(table_headers)
	    	row = row + table_headers[column] + ": "
	    	row = row + tds[column].text + "\t"
	    print(row.encode('utf-8'))
	    # print "1: %s, 2: %s, 3: %s, %s" % \
	    #       (tds[0].text, tds[1].text, tds[2].text, tds[3].text)
	    # print tds


# print table_headers

def main():
	url = r'http://www.fda.gov/Drugs/DevelopmentApprovalProcess/HowDrugsareDevelopedandApproved/DrugandBiologicApprovalReports/ANDAGenericDrugApprovals/ucm050527.htm'
	domain = r'http://www.fda.gov/'

	getMonthlyLinksFromLandingPage(url, domain, 2) #assigning depth = 2 to indicate data is after two layers of web pages.

if __name__ == "__main__":
	main()
