import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-extlog',
    version='0.7',
    packages=['django_extlog'],
    include_package_data=True,
    license='MIT',
    description='Extended log for Django, that tracks changes in models.',
    url='https://github.com/AxiaCore/django-extlog',
    author='Vera Mazhuga',
    author_email='ctrl-alt-delete@live.ru',
    install_requires=[
        'django-extensions',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
