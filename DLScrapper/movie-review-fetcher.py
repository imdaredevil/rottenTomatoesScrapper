from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep

driver = webdriver.Chrome('../chromedriver')
baseUrl = 'https://www.rottentomatoes.com/m/{movie}/reviews?type=user'
LIMIT = 20


def printMovieReview(review):
    for key in review.keys():
        print('---------------------------------------------')
        print(key,end=' : ')
        print(review[key])
    print('---------------------------------------------')


def getMovieReviews(movie):
    driver.get(baseUrl.format(movie=movie))
    nextPage = True
    reviewDicts = []
    while nextPage and len(reviewDicts) <= LIMIT:
        html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html5lib')
        reviews = soup.findAll('li',attrs = { 'class' : 'audience-reviews__item' })
        for review in reviews:
            reviewText = review.find('p', attrs = { 'class' : 'audience-reviews__review'})
            reviewerName = review.find('a', attrs = { 'class' : 'audience-reviews__name'})
            reviewScore = review.find('span', attrs = { 'class' : 'audience-reviews__score'})
            
            reviewDict = {}
            if reviewText:
                reviewDict['text'] = reviewText.text.replace('\n','').replace('  ','')
            if reviewerName:
                reviewDict['user'] = reviewerName.text.replace('\n','').replace('  ','')
            if reviewScore:
                full = reviewScore.findAll('span', attrs = { 'class' : 'star-display__filled'})
                half = reviewScore.findAll('span', attrs = { 'class' : 'star-display__half'})
                reviewDict['score'] = 0.5*len(half) + len(full)
            reviewDicts.append(reviewDict)
        try:  
            nextB = driver.find_element_by_class_name('js-prev-next-paging-next')
            nextB.click()
            sleep(5)
        except:
            nextPage = False
    driver.close()
    return reviewDicts

if __name__ == '__main__':
    if len(sys.argv) == 2:
        movie = sys.argv[-1]
        count = 0
        for review in getMovieReviews(movie):
            print('*********************************************')
            print("Movie Review - {0}".format(count))
            printMovieReview(review)
            count += 1
    else:
        print('The format is python <filename> <movie name>')