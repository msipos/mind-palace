import setuptools

with open('requirements.txt', 'rt') as f:
    install_requires = f.read().split()

setuptools.setup(
    name="mind_palace",
    version="0.0.6",
    author="Maksim Sipos",
    author_email="msipos@mailc.net",
    description="Mind palace: mnemonic note taking system",
    long_description="Mind palace: mnemonic note taking system. Web application.",
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
)
