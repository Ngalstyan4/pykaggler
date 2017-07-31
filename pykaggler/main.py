import requests
from getpass import getpass
from mechanicalsoup import Browser
import sys

LOGIN_URL = "http://www.kaggle.com/account/login"
CHUNK_SIZE = 512 * 1024
BAR_LENGTH = 80


class PyKaggler():
    def __init__(self):
        self.userSession = None

    def login(self, username, password=None):
        if password is None:
            password = getpass(prompt="Kaggle Password: ")
        browser = Browser()
        login_page = browser.get(LOGIN_URL)
        login_form = login_page.soup.select("#login-account")[0]
        login_form.select("#UserName")[0]['value'] = username
        login_form.select("#Password")[0]['value'] = password
        login_result = browser.submit(login_form, login_page.url)
        if len(login_result.soup.select('#standalone-signin .validation-summary-errors')) != 0:
            print("Something went wrong when trying to log you in\nHere is the error from Kaggle\n %s"
                  % login_result.soup.select('#standalone-signin .validation-summary-errors')[0].get_text())
        else:
            print("Logged in Successfully")
            self.userSession = browser

    def download(self, url, output_file_name):
        if self.userSession is None:
            print("Please login first")
            return False
        file_size = int(self.userSession.request('head', url).headers.get('Content-Length'))
        # Todo check if file is html/sth else
        r = self.userSession.get(url, stream=True)
        f = open(output_file_name, 'w')

        size = 0
        sys.stdout.write(' ' * 4)  # to have something to overwrite in the first iter
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):  # Reads 512KB at a time into memory
            if chunk:  # filter out keep-alive new chunks
                size += CHUNK_SIZE
                f.write(chunk)
                # percent_done = str(size * 100 / file_size) + '%'
                # percent_done = (4 - len(percent_done)) * ' ' + percent_done
                # sys.stdout.write('\b' * 4)
                # sys.stdout.write(percent_done)
                # sys.stdout.flush()
                percent_done = str(size * 100 / file_size)
                percent_done = (3 - len(percent_done)) * '' + percent_done
                sys.stdout.write('\b' * 4)
                sys.stdout.write(percent_done)
                sys.stdout.flush()

        sys.stdout.write("\n")
        f.close()
