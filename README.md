# Project

Create a secure RESTful API using Django REST

## Installation

clone repository locally

```bash
git clone https://github.com/nasr-edine/P10_drai_nasr-edine.git
```

Move to the P10_drai_nasr-edine root folder with:

```bash
cd P10_drai_nasr-edine
```

Create a virtual environment in root folder of project

```bash
python3 -m venv env
```

Activate virtual environment

```bash
source ./env/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Make Migration

```bash
django mm
```

Migrate

```bash
django m
```

You can create a super user in command line:

```bash
django csu
```

## Usage

Run the Django Server:

```bash
django r
```

<!-- todo: How to use postman -->

Access to API documentation:
[https://documenter.getpostman.com/view/5359695/TzscpSp5](https://documenter.getpostman.com/view/5359695/TzscpSp5)

### Folder Structure

    .
    ├── tracking_system_project/     # django project folder
    ├── setup.cfg                    # customise rules for flake8
    ├── projects/                    # Content project app
    ├── issues/                      # Content issues app
    ├── requirements.txt             # dependencies for this project
    └── README.md
