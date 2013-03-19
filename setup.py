from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1.2'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'pyprof2calltree==1.1.0',
]

setup(name='django-depiction',
    version=version,
    description="Tooling for profiling Django applications, inspired by David Cramer",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    keywords='profile cprofile django middleware',
    author='Travis Chase, Rob Madole',
    author_email='<travis.chase@localbase.com>, <rob.madole@localbase.com>',
    url='http://github.com/robmadole/django-depiction',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={}
)
