import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Dominion Card API",
    version="1.2.0",
    author="Wes Buck",
    description="Dominion Kingdom Card API intended to power companion apps for the board game Dominion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesbuck/DominionCardAPI",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
