import requests
from getpass import getpass


class PyKaggler():
    def __init__(self):
        self.credentials = None

    def login(self, username, password=None):
        if password is None:
            print ("haha")
            password = getpass(prompt="Kaggle Password: ")
        self.credentials = {"UserName": username, "Password": password}

    def download(self, url, output_file_name):
        if not self.credentials:
            print("Please login first")
            return False
        r = requests.post(url=url, data=self.credentials)
        f = open(output_file_name, 'w')
        for chunk in r.iter_content(chunk_size=512 * 1024):  # Reads 512KB at a time into memory
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
        f.close()

