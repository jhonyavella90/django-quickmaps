import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path).read()

def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='django-quickmaps',
    version=find_version('quickmaps', '__init__.py'),
    description='Quick and easy way to handle geolocation data in a django '
                'application.',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Utilities',
    ],
    keywords=['django', 'maps', 'geolocation', 'location', 'DRY'],
    author='Daniel Barreto',
    author_email='daniel.barreto.n@gmail.com',
    url='http://github.com/volrath/django-quickmaps',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
