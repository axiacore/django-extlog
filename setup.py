import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-extlog',
    version='0.1',
    packages=['extlog'],
    include_package_data=True,
    license='MIT',
    description='Extended log for Django, that tracks changes in models.',
    long_description=README,
    url='https://github.com/AxiaCore/django-extlog',
    author='Vera Mazhuga',
    author_email='ctrl-alt-delete@live.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
