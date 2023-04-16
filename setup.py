from setuptools import setup, find_packages


with open("requirements.txt") as install_requires_file:
    install_requires = install_requires_file.read().strip().split("\n")


def get_version():
    _version = {}
    with open('research/_version.py') as fp:
        exec(fp.read(), _version)
    return _version['__version__']


setup(
    name='research',
    version=get_version(),
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=install_requires,
    url='https://github.com/Mmoncadaisla/pydata-gis-madrid',
    license='Apache License 2.0',
    author_email='mmoncadaisla@gmail.com',
    author='mmoncadaisla',
    description='PyData Madrid GIS - 2023'
)
