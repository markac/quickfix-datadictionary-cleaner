from setuptools import setup

setup(
    name='quickfix_datadictionary_cleaner',
    version='1.0',
    packages=['quickfix_datadictionary_cleaner'],
    entry_points={
        'console_scripts': [
            'quickfix_datadictionary_cleaner = quickfix_datadictionary_cleaner.quickfix_datadictionary_cleaner:main'
        ]
    },
)
