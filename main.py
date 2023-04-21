import requests
from bs4 import BeautifulSoup

def crawlContent(nPage):

    openai = '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'
    url = "https://vnexpress.net"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser", from_encoding='utf-8')

    # find all article links in the homepage
    article_links = [a['href'] for i, a in enumerate(soup.select('h3.title-news a[href]')) if i < nPage]
    print(article_links)
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
        content = [p.get_text() for p in article_soup.find_all('p')]
        string = ''.join(content)
        print("Title:", title)
        print("Content:", string)


crawlContent(7)
