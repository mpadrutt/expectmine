from setuptools import setup

setup(
    name="expectmine",
    version="0.0.1",
    packages=["expectmine"],
    install_requires=[
        "inflection",
        "Jinja2",
        "InquirerPy",
        "requests",
        "tqdm",
        "python-dotenv",
    ],
)
