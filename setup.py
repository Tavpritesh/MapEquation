from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'


with open('requires.txt') as f:
    install_requires = f.read().splitlines()

setup(name='MapEquation',
    version=version,
    description="Implementation of the MapEquation algorithm with networkx",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Graph',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
    ],
    keywords='graph, community detection',
    author='Vincent Gauthier',
    author_email='pub@luxbulb.org',
    url='http://complex.luxbulb.org',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    test_suite='nose.collector',
    entry_points={
        'console_scripts':
            ['MapEquation=mapequation:main']
    }
)
