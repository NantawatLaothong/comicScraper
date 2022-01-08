#!/usr/bin/env python

import argparse
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import os
import time
import re

# url = 'https://readcomiconline.li/Comic/Life-is-Strange'


# Get command line args
def get_args():
    parser = argparse.ArgumentParser(description='Downloads comic from readcomiconline.li')
    parser.add_argument("comic", type=str, help="The name of the comic")
    args = parser.parse_args()
    return args


def convert_name(name):
    name = name.replace(' ', '-')
    return name


def get_webpage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req).read()
    return res


def get_issues(webpage):
    issues = []
    # pattern = '/Comic/Life-is-Strange/Issue-[0-9]?id=[0-9]'
    # pattern = '/Comic/Life-is-Strange/Issue-9?id=162387'
    soup = BeautifulSoup(webpage, 'html.parser')
    # return array
    divs = soup.findAll('div', attrs={'class': 'chapter'})
    for div in divs:
        link = div.find('a')
        # get all pages
        issues.append(link.get('href')+'/all')
    return issues
    # loop through array
    # print(match)
    # get a list of a tags in ul
    # links = match.findAll('a')
    # for link in links:
    #     issues.append('https://readcomiconline.li{}'.format(link.get('href')))
    # return issues
    # for a in match:
    #     links = ul.findAll('a')
    #     for a in links:
    #         print(a.get('href'))
    # print(match)
    # print(soup.prettify())
    # for link in soup.find_all('a'):
        # if(re.search(pattern, link.get('href'))):
            # issues.append(link.get('href'))
        # print(link.get('href'))
        # print('not found')
    # print(match)


def get_pages(url):
    # url = url + '&readType=1'
    webpage = get_webpage(url)
    pages = []
    soup = BeautifulSoup(webpage, 'html.parser')
    divs = soup.findAll('div',attrs={'class':'page-chapter'})
    for div in divs:
        imgs = div.findAll('img')
        for img in imgs:
            pages.append(img['data-original'])
    return pages
    # page = soup.prettify()
    # match = soup.find(id='divImage')
    # print(match)
    # print(page)


def get_image(url, filename):
    print('Downloading page: {}'.format(filename))
    image = get_webpage(url)
    time.sleep(1)
    urlretrieve(url, filename+'.jpg')


def create_directory(comic):
    folder_path = os.path.join(os.getcwd(), comic)

#     create the directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(comic)

    return folder_path

# return a list
def get_issue_text(issue):
    pattern = 'issue-\d{1,2}'
    issue = re.findall(pattern, issue)
    return issue

def download_pages(path, pages):
    number_of_pages = len(pages)
    counter = 1
    for page in pages:
        get_image(page, path + '/' + str(counter))
        counter += 1
    time.sleep(1)
    # print(number_of_pages)

def download_issues(issues, path):
    for issue in issues:
        # get issue
        issue_text = get_issue_text(issue)[0]
        comic_path = path + '/' + issue_text
        # print(comic_path)
        if not os.path.exists(comic_path):
            os.makedirs(comic_path)
        # print(issue)
        pages = get_pages(issue)
        download_pages(comic_path, pages)
        print('downloading {}'.format(issue_text))
    # os.makedirs()

def main():
    args = get_args()
    comic = convert_name(args.comic)
    url = 'https://xoxocomics.com/comic/' + comic
    webpage = get_webpage(url)
    issues = get_issues(webpage)
    # print(issues)
    # pages = get_pages('https://xoxocomics.com/comic/life-is-strange/issue-1/96012/all')
    # download_pages(pages)
    directory = create_directory(comic)
    download_issues(issues, directory)
    # get_issue_text(issues)
    return

# https://xoxocomics.com/comic/life-is-strange/issue-1/96012' first
# https://xoxocomics.com/comic/life-is-strange/issue-1/96012/all


if __name__ == "__main__":
    main()