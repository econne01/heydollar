from setuptools import setup, find_packages

setup(
    name = "heydollar",
    version = "0.2",
    url = 'https://github.com/econne01/heydollar',
    description = "Personal finance management that extends mint.com functionality",
    author = 'Eric Connelly',
    # packages = find_packages('src'),
    # package_dir = {'': 'src'},
    py_modules=['run_transaction_summary'],
    install_requires = [
        'Click>=6.0',
        # 'csv', # Should be included in Python 3
    ],
    entry_points='''
        [console_scripts]
        run_transaction_summary=run_transaction_summary:cli
    ''',
)
