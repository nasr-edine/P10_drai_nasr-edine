# Projet 

Développez un programme logiciel en Python

## Installation

<!-- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar. -->
clone repository locally
```bash
git clone https://github.com/nasr-edine/P4_drai_nasr-edine.git
```
Create a virtual environment in root folder of project 
```bash
python -m venv env
```

Activate virtual environment
```bash
source ./env/bin/activate
```
Install dependencies
```bash
pip3 install -r requirements.txt
```
## Usage

execute the python script below for starting the chess game management software:
```python
python main.py
```
### Folder Structure with db.json created

    .
    ├── main.py                    # python file for run the chess game management software
    ├── model/                     # The central component of the pattern.
    ├── view/                      # Any representation of information
    ├── controller/                # Accepts input and converts it to commands for the model or view
    ├── flake-report/              # generating HTML reports of flake8 violations
    ├── db.json                    # Content list of all players and tournaments created by the script
    ├── requirements.txt           # for install all dependencies necessary for this project
    └── README.md

### How to check style code ?

##### Consulting HTML reports of flake8 violations

To generate flake8 report, type command below
> :warning: **If you use this command**: exclude virtual environment from flake8

```bash
flake8 --format=html --htmldir=flake-report --exclude=env
```


* open flake-report/index.html file with your browser
 
* click on the link below to consult the last report:
  * [Flake8 report](https://htmlpreview.github.io/?https://github.com/nasr-edine/P4_drai_nasr-edine/blob/master/flake-report/index.html)

##### In command line
```bash 
flake8 main.py controller model view 
```