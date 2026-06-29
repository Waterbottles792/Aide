from setuptools import find_packages, setup

setup(
    name="aide",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24",
        "rich>=13.0",
        "textual>=0.86.0",
        "ddgs>=2.0",
        "beautifulsoup4>=4.12",
    ],
    entry_points={"console_scripts": ["aide=aide.cli:main"]},
)
