from setuptools import setup, find_packages

setup(
    name = "heydollar",
    version = "0.1",
    url = 'https://github.com/econne01/heydollar',
    description = "Personal finance management that extends mint.com functionality",
    author = 'Eric Connelly',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)