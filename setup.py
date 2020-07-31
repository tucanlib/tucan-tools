import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tucan_tools",
    version="0.0.1",
    author="TucanLib",
    author_email="info@davidgengenbach.de",
    description="Library to extract grades and the Vorlesungsverzeichnis from TuCan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tucanlib/tucan-tools",
    packages=setuptools.find_packages(),
    install_requires=[
        'MechanicalSoup>=0.6.0',
        'notify2>=0.3.1',
        'matplotlib>=3.1.3',
        'dbus-python>=1.2.16'
    ],
    scripts=['tucan_tools/grades_extractor.py'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.5',
)
