from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    '''
    this function will return the list of requirements
    '''
    HYPEN_E_DOT = '-e .'
    requirements = []
    with open(file_path, "rb") as file_obj:
        content = file_obj.read()
        # decode the byte string using UTF-16 (LE) encoding
        decoded_content = content.decode('utf-16-le')
        requirements = decoded_content.split('\x00')
        requirements = [req.strip().replace("\n","").replace("\r",",") for req in requirements if req.strip()]
        # join all the strings in the list
        all_requirements = ''.join(requirements)
        # remove the BOM character if it's present
        all_requirements = all_requirements.lstrip('\ufeff')
        # split the string by comma to get the list of requirements
        requirements = all_requirements.split(',')
        # strip whitespace from each requirement
        requirements = [req.strip() for req in requirements]
        if HYPEN_E_DOT not in requirements:
            requirements.append(HYPEN_E_DOT)

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
name='Money-launderying-Prevention',
version='0.0.1',
author='Saikumar',
author_email='sai680513@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)
