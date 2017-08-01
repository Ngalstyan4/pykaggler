import requests
from getpass import getpass
from mechanicalsoup import Browser
import sys

LOGIN_URL = "http://www.kaggle.com/account/login"
COMPETITION_PAGE = "https://www.kaggle.com/c/%s/data"
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
        if validate_url(url) is False:
            return False
        content_type = self.userSession.request('head', url).headers.get("Content-Type")
        if "html" in content_type:
            if not query_yes_no("The link seems to point to an HTML page, Are you sure you want to download this? "):
                return False

        file_size = int(self.userSession.request('head', url).headers.get('Content-Length'))

        r = self.userSession.get(url, stream=True)
        f = open(output_file_name, 'w')

        size = 0
        sys.stdout.write(' ' * 4)  # to have something to overwrite in the first iter
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):  # Reads 512KB at a time into memory
            if chunk:  # filter out keep-alive new chunks
                size += min(CHUNK_SIZE, file_size)
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


def validate_url(url):
    # todo extensive url validation
    if type(url) is not str:
        print("URL has to be a string %s provided" % type(url))
        return False
    if not (url.startswith("http://www.kaggle.com/") or url.startswith("https://www.kaggle.com/")):
        print("URL has to start with http://www.kaggle.com/ or https://www.kaggle.com/")
        return False
    return True


def query_yes_no(question):
    valid = {"yes": True, "y": True,
             "no": False, "n": False}

    while True:
        sys.stdout.write(question + "[y/n]")
        choice = raw_input().lower()

        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
