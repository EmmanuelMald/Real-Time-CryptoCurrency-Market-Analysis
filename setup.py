import setuptools

# Read dependencies from requirements.txt,
# requirements.txt is created when executing the make command
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="streaming-pipeline-crypto",
    version="1.0",
    install_requires=install_requires,  # Use the list read from requirements.txt
    packages=setuptools.find_packages(),
)
