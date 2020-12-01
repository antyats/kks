from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='kokos',
    description='KoKoS helper tool',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Vyacheslav Boben',
    url='https://github.com/DarkKeks/kks',
    version='1.3.0-rc2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'configparser',
        'colorama',
        'tqdm',
        'beautifulsoup4',
    ],
    entry_points='''
        [console_scripts]
        kks=kks.cli:cli
    ''',
)
