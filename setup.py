from setuptools import setup, find_packages

setup(
    name="expectmine",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    scripts=['bin/cli.py'],
    install_requires=[
        "inflection",
        "Jinja2",
        "InquirerPy",
        "requests",
        "tqdm",
        "python-dotenv",
    ],
)
