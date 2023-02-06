from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List:
    file = open('requirements.txt','r')
    req_list:List[str] = file.readlines()
    for idx, lib  in enumerate(req_list):
        req_list[idx] = lib.replace('\n','')

    return req_list

setup(
	name = 'Money-Launderying-Prevention',
	version='0.0.1',
	author='saikumar',
	author_email='sai680513@gmail.com',
	packages=find_packages(),
    install_requires=get_requirements()


)