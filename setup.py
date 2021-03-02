#from distutils.core import setup
from peco_spark.version import __version__
# setup(name='peco_spark',
#       version=
#       py_modules=['foo'],
#       )


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="peco_spark", # Replace with your own username
    version=__version__,
    author="Breadlysm",
    author_email="github@breadlysm.com",
    description="App to retrieve electric usage from peco and export it to influxdb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "confuse",
        "influxdb",
        "python-dotenv",
        "PyYAML",
        "requests",
        "selenium",
        "simplejson",
        "urllib3"
    ],
)