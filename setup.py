from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pace_downloader",
    version="0.0.1",
    packages=find_packages(),  # finds pace_downloader/
    install_requires=[
        "earthaccess>=0.6.0",
        "rich",
        "tqdm",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "pace-download = pace_downloader.cli:main",
        ],
    },
    author="Chinmay Deval",
    description="PACE data downloader with bounding boxes, daily/monthly modes, and CLI.",
    url="https://github.com/devalc/pace-mvp-api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
