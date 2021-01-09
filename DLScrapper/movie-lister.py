from bs4 import BeautifulSoup
import requests
import sys
baseURL = 'https://en.wikipedia.org/wiki/List_of_American_films_of_{year}'


def getSoup(year):
    url = baseURL.format(year = year)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getTableSize(table):
    rows = table.findAll('tr')
    firstRow = rows[0]
    cols = firstRow.findAll(['th','td'])
    m = 0
    for col in cols:
        if col.get('colspan'):
            m += int(col.get('colspan'))
        else:
            m += 1
    n = 0
    for row in rows:
        col = row.find(['th','td'])
        if col.get('rowspan'):
            n += int(col.get('rowspan'))
        else:
            n += 1
    return n,m
        

def getMovieList(year):
    soup = getSoup(year)
    movies = []
    tables = soup.findAll('table', attrs = { 'class' : 'wikitable'})
    for table in tables:
        n,m = getTableSize(table)
        dataTable = []
        for i in range(n):
            dataTable.append([])
            for j in range(m):
                dataTable[i].append('-')
        rows = table.findAll('tr')
        i = 0
        j = 0
        for row in rows:
            cols = row.findAll(['th','td'])
            for col in cols:
                while dataTable[i][j] != '-':
                    j+= 1
                    if j == m:
                        i += 1
                        j = 0
                r = 1
                if col.get('rowspan'):
                    r = int(col.get('rowspan'))
                c = 1
                if col.get('colspan'):
                    c = int(col.get('colspan'))
                for a in range(r):
                    for b in range(c):
                        dataTable[i + a][j + b] = col.text
        i = 0
        titleIndex = 0
        for header in dataTable[0]:
            if header == 'Title' or header == 'Title\n':
                titleIndex = i
            i += 1
        if titleIndex < 0:
            continue
        for row in dataTable[1:]:
            if row[titleIndex] != '-':
                movie = row[titleIndex]
                movie = movie.replace('\n','')
                movies.append(movie)
    return movies


if __name__ == '__main__':
    if len(sys.argv) == 2:
        year = sys.argv[-1]
        print(getMovieList(year))
    else:
        print('The format is python <filename> <year>')

    