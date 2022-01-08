from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup 
import os 
import time 
import re


def get_image(url, issue_text, filename):
    # if the file doesn't exist then download
    if not os.path.exists(filename + '.jpg'):
        try:
            print('Downloading: {}, Path: {}'.format(issue_text, filename))
            image = get_webpage(url)
            time.sleep(1)
            urlretrieve(url, filename+'.jpg')
        except Exception:
            pass
    else:
        return


def get_webpage(url):
    try:
        web_req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_res = urlopen(web_req).read()
    except Exception:
        print('something happened in get_webpage')    
        # print('something failed in get_webpage()')
    return web_res


class Comic:

    def __init__(self, name):
        self.name = name.replace(' ', '-')
        self.url = 'https://xoxocomics.com/comic/' + self.name.replace(' ', '-')
        self.issue_links = []
        self.issues = []
        
    def get_directory(self, path=os.getcwd()):
        folder_path = os.path.join(path, self.name)

    #     create the directory if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(self.name.replace(' ', '-'))

        return folder_path

    def get_name(self):
        return self.name

    # return issues links
    def get_issue_links(self):
        soup = BeautifulSoup(get_webpage(self.get_url()), 'html.parser')
        divs = soup.findAll('div', attrs={'class': 'chapter'})
        for div in divs:
            link = div.find('a')
            # get all pages
            self.issue_links.append(link.get('href')+'/all')
        return self.issue_links

    def get_url(self):
        return self.url

    def create_issues(self):
        for link in self.issue_links:
            self.issues.append(Issue(link))
        return self.issues

    def download_issues(self, path):
        for issue in self.issues:
            # get issue
            issue_text = issue.get_issue_text()[0]
            comic_path = path + '/' + issue_text
            if not os.path.exists(comic_path):
                os.makedirs(comic_path)
            pages = issue.get_pages()
            issue.download_pages(comic_path, pages)
            print('downloading {}'.format(issue_text))


class Issue(Comic):
    def __init__(self, url):
        self.url = url
        self.text = self.get_issue_text()
        self.pages = []

    def get_url(self):
        return self.url

    def get_pages(self):
        # url = url + '&readType=1'
        webpage = get_webpage(self.get_url())
        soup = BeautifulSoup(webpage, 'html.parser')
        divs = soup.findAll('div',attrs={'class':'page-chapter'})
        for div in divs:
            imgs = div.findAll('img')
            for img in imgs:
                self.pages.append(img['data-original'])
        return self.pages    

    # return a list
    def get_issue_text(self):
        pattern = 'issue-\d{1,2}'
        issue = re.findall(pattern, self.url)
        return issue

    def download_pages(self, path, pages):
        number_of_pages = len(self.pages)
        counter = 1
        for page in pages:
            get_image(page, self.get_issue_text()[0], path + '/' + str(counter))
            counter += 1
        time.sleep(1)
        # print(number_of_pages)


if __name__ == "__main__":
    comic = Comic('life is strange')
    comic.get_issue_links()
    path = comic.get_directory()
    issues = comic.create_issues()
    comic.download_issues(path)
    # for issue in issues:
    #     print(issue.text)
    #     print(issue.get_pages())

    
