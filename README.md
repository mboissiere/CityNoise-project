# CityNoise project 28095

This is a GitHub repository containing a program to visualize the evolution over time of air pollution levels, with given vehicle traffic and emissions model of choice.
The program is so far focused on the Södermalm area but could be made to change with time.

## Table of Contents
1. [SSH Clone](#ssh-clone)
2. [Installing Dependencies](#installing-dependencies)
3. [Running the Program](#running-the-program)
4. [Documentation](#documentation)


## Clone the project via SSH

To clone this project from GitHub, you can use a SSH key. 

Make sure you have Git installed on your machine.  If you do not know how to configure a SSH key, a tutorial is available on GitHub.

```bash
git clone git@github.com:mboissiere/CityNoise-project-28095.git
```

## Installing Dependencies

Before using the program, you need to install the required Python dependencies. We use `pip` to manage these dependencies. If you already have pip installed, you can proceed with the following steps. Otherwise, follow the instructions for your operating system below:

### Install pip (if not installed)

**On Linux/macOS:**

Python is usually pre-installed on Linux and macOS. Open a terminal and enter the following command to check if pip is installed:

```bash
pip --version
```

If you don't see version information, you need to install pip:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

**On Windows:**

Check if pip is installed by opening a command prompt:

```bash
pip --version
```

If pip is not installed, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer. Then, open a command prompt and navigate to the folder where you downloaded `get-pip.py`. Run the following command:

```bash
python get-pip.py
```

### Install project dependencies

After you have pip installed, navigate to the project directory and run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```


## Running the Program

To use the program, open and run the `main.py` file in the IDE of your choice.


## Documentation

To understand this program in more detail, please refer to the PDF provided in the `docs` folder.
Functionalities should normally be well commented, but feel free to add more docstrings if needed.
