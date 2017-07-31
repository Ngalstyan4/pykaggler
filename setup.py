from setuptools import setup
from setuptools import find_packages

setup(
    name='pykaggler',
    packages=find_packages(exclude=['test', 'test.*']), version='0.1',
    description='This is a simple utility that allows Kaggle competitors to download/unpack/use and submit results to Kaggle without l',
    author='Narek Galstyan and Davit Khechoyan',
    author_email='davkhech@gmail.com',
    url='https://github.com/Ngalstyan4/pykaggler',
    download_url='-----------',
    keywords=['kaggle', 'downloader', 'datasets'],
    install_requires=[
        'requests',
    ],
    classifiers=[],
)
