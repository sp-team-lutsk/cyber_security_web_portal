import urllib.request
import brotli
from .models import News
from bs4 import BeautifulSoup

headers = {"Host": "glavcom.ua",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
           "Accept": "text/css,*/*;q=0.1",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate, br",
           "DNT": "1",
           "Connection": "keep-alive",
           "Cookie": "cfduid=d96a511dc113177453717c58ea2a775381566151570; xs=cec6ad7a6605ef7a5cb3dcb813cdb835; sa_userid=0; cbtYmTName=WSJ7MD17Y3toazg4Om84YThsO2s7bWw8eyQ4; 5183af98523bb467d9fc4781603dd09d=9abcd682a463cfd524eb5926652b4e83", }

burl = "https://glavcom.ua/tags/ministerstvo-osviti-i-nauki.html"
glavcom = "https://glavcom.ua/tags/ministerstvo-osviti-i-nauki/"
pingvin = "https://pingvin.pro/category/gadgets/news-gadgets?"
intnews = "https://www.itnews.com"
########################################################################################################
def get_html(url):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = brotli.decompress(response.read())

    return content.decode('utf-8')


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('ul', class_='pagination')
    return int(paggination.find_all('a')[-2].text)


def parse(html):
    projects = []
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('ul', class_='list')

    for nev in div.find_all('li'):
        for a in nev.find_all('a'):
            photo ='https://glavcom.ua' + nev.find('img').get('src')
            headerr = nev.a.text.replace('\n', '')
            opis = nev.find('div', class_="header").text
            link = 'https://glavcom.ua' + nev.find('a').get('href')

        projects.append({
            'image1': photo,
            'title': headerr,
            'description': opis,
            'read_more': link
        })

    for project in projects:
        print(project)

    return projects

def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')

    pages = soup.find_all('ul', class_='pagination').find_all('a')[-1].get('href')

    print('pages')
#######################################################################################################

def get_html2(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_page_count2(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('ul', class_='pagination')
    return int(paggination.find_all('li')[-2].text)

def parse2(html):
    projects = []
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', id='main', role='main', class_='row')

    for nev in div.find_all('div', class_='col-lg-4 col-md-6 cat2content'):
        #nev return all news boxes
        mcols = nev.find_all('div')[1:]

        photo = nev.find('div', class_='card-image').find('a').find('img').get('src')
        headerr = nev.find('div', class_='card-body').h3.text.replace('\n', '')
        opis = nev.find('div', class_='card-body').p.text.replace('\n', '').replace('[…]', '')
        link = nev.find('div', class_='card-body').find('a', class_='card-link').get('href').replace('\n', '')
        #mcols return all card image and card body`

        projects.append({
            'image1': photo,
            'title': headerr,
            'description': opis,
            'read_more': link
        })

    for project in projects:
        print(project)

    return projects


def get_pages2(html):
    soup = BeautifulSoup(html, 'html.parser')

    pages = soup.find_all('ul', class_='pagination').find_all('a',class_='page_numbers')[-1].get('href')

    print('pages')

########################################################################################################

def get_html3(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse3(html):
    projects = []
    soup = BeautifulSoup(html, 'html.parser')
#################################################################
    body = soup.find('section', class_='bodee')
    first=body.find('div', class_='top-story')
    second=body.find('div', class_='item-info')
    third=body.find('div', class_='read-more-link')

    photo=first.find('figure').find('a').find('img').get('src')

    projects.append({
        'image1': photo,
        'title': second.find('div').a.text,
        'description': second.p.text,
        'read_more': 'https://www.itnews.com'+third.find('a').get('href')

    })
#################################################################
    all_news=body.find('div', class_='newsfeed news-col1')
    for new in all_news.find_all('div', class_='news-item'):

        unic_im=new.find('figure').find('a').find('img').get('data-original')
        unic_hed=new.find('div', class_="hed").find('div', class_='title').a.text
        unic_bot=new.p.text
        unic_read='https://www.itnews.com'+new.find('div', class_='read-more-link').find('a').get('href')

        projects.append ({
            'image1':unic_im,
            'title': unic_hed,
            'description': unic_bot,
            'read_more': unic_read
        })
#################################################################
    main_second_col=body.find('div', class_='newsfeed news-col2')
    for second_col in  main_second_col.find_all('div', class_='news-item'):
        unic_im2 = second_col.find('figure').find('a').find('img').get('data-original')
        unic_hed2 = second_col.find('div', class_="hed").find('div', class_='title').a.text
        unic_bot2 = second_col.p.text
        unic_read2 ='https://www.itnews.com'+ second_col.find('div', class_='read-more-link').find('a').get('href')

        projects.append({
            'image1': unic_im2,
            'title': unic_hed2,
            'description': unic_bot2,
            'read_more': unic_read2
        })
#################################################################
    for project in projects:
        print(project)

    return projects

def save(projects):
    for project in projects:
        News.objects.create(
                title=project['title'],
                description=project['description'],
                news_link=project['read_more'],
                images_link=project['image1'])


def main():
    projects = []

    print('Glavcom:')

    total_pages = get_page_count(get_html(burl))

    print('%d all_pages...' % total_pages)

    for page in range(1, total_pages):
        print('\nPars %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        projects.extend(parse(get_html(glavcom + 'p%d.html' % page)))

    print('\nPingvin.pro:')

    total_pages2 = get_page_count2(get_html2(pingvin))

    print('%d all_pages...' % total_pages2)

    for page2 in range(1, 11):
        print('\nPars %d%% (%d/%d)' % (page2 / total_pages2 * 100, page2, total_pages2))
        projects.extend(parse2(get_html2(pingvin + "page=%d" % page2)))

    print('\nIntnews:')

    projects.extend(parse3(get_html3(intnews)))

    save(projects)


if __name__ == '__main__':
    main()

CRONJOBS = [
    ('00 16  *   *   6', 'ext_news.cron.CronParse'),
]