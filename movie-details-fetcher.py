from bs4 import BeautifulSoup
import requests
import sys
import re

def getSoup(url):
    response = requests.get(url)
    if response.status_code < 200 or response.status_code >= 300:
        return None
    html = response.content
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getMovieDetails(url):
    details = {}
    soup = getSoup(url)
    if not soup:
        return 'Wrong link'
    synopsisDiv = soup.find('div', attrs = { 'id' : 'movieSynopsis'})
    if synopsisDiv:
        details['synopsis'] = synopsisDiv.text.replace('\n','').replace('  ','')
    movieInfoDivs = soup.findAll('li', attrs = { 'data-qa': 'movie-info-item'})
    print(len(movieInfoDivs))
    for movieInfoDiv in movieInfoDivs:
        labelDiv = movieInfoDiv.find('div', attrs = { 'data-qa': 'movie-info-item-label'})
        valueDiv = movieInfoDiv.find('div', attrs = { 'data-qa': 'movie-info-item-value'})
        if labelDiv and valueDiv:
            label = labelDiv.text
            label = re.sub(r'[^\w]', '', label)
            details[label] = valueDiv.text.replace('\n','').replace('  ','')
    return details

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[-1]
        print(getMovieDetails(url))
    else:
        print('The format is python <filename> <movie name>')

