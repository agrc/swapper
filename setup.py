import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swapper", # Replace with your own username
    version="1.0.1",
    author="Zach Beck",
    author_email="zbeck@utah.gov",
    description="Move data from one SDE database to another with minimal downtime",
    url="https://github.com/agrc/swapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'docopt==0.6.*',
        'python-dotenv==0.10.*'
    ],
    entry_points={"console_scripts": ["swapper = swapper.__main__:main"]}
)
