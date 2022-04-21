"""Packaging setup script."""

from setuptools import setup, find_packages
import versioneer
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="ytad",
    long_description=README,
    long_description_content_type='text/markdown',
    description="A tool for adding YouTube video like/dislike counts to video descriptions.",
    url="https://github.com/SpencerPao/YouTube_Automation",
    author="Spencer Pao",
    author_email="business.inquiry.spao@gmail.com",
    license="MIT",
    package_dir={'': 'ytad'},
    packages=find_packages(where='ytad'),
    entry_points={"console_scripts": ["ytauto=YouTube_Automation.cli:cli"]},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "jupyter",
        "pandas",
        "python-dotenv",
        "google-api-python-client",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "boto3",
        "pytz",
    ],
)
