import requests
from bs4 import BeautifulSoup

def crawlContent(nPage):
    for i in range(nPage):
        url = "https://vnexpress.net"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser", from_encoding='utf-8')

        # find all article links in the homepage
        article_links = [a['href'] for a in soup.select('h3.title-news a[href]')]

        # loop through each article link and extract the content
        for link in article_links:
            article_req = requests.get(link)
            article_soup = BeautifulSoup(article_req.content, "html.parser")

            # extract the article title and content
            title = article_soup.find('h1', {'class': 'title-detail'})
            if title is None:
                break
            else:
                title = title.text.strip()
            content = article_soup.find('article', {'class': 'fck_detail'}).text.strip()

            print("Title:", title)
            print("Content:", content)
        break
        #update the URL to crawl the next page
        url = soup.select_one('.next-page')['href']


crawlContent(5)
