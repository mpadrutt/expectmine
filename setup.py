from setuptools import setup, find_packages

setup(
    name="expectmine",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "inflection",
        "Jinja2",
        "InquirerPy",
        "requests",
        "tqdm",
        "python-dotenv",
    ],
)
