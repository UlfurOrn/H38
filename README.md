# H38
Verklegt 1 - Hópur 38

## Setup:
First of all you need to clone the repository. After that you can
follow the following steps to setup the project:
* `python -m venv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

and now you have setup everything you need to run the project.


## Running:
To run the project you must first activate the virtual environment
if you have not already:
* `source venv/bin/activate`

Now you can run the project by running the following commands:
* `cd src`
* `python main.py`


## Git
Working with git can be hard at the start. So here is a brief rundown
of the git workflow:
* `git add <filename>` or `git add .` to add all changed files
* `git commit -m "message"`
* `git push` to push changes online

The above is used to save changes in code. But we do not want to
disrupt other peoples work so we will be using git branches!

To create a new branch run the following:
* `git checkout -b "branch-name"`
* `git push` (and then copy paste the message)

To switch branches run the following:
* `git checkout <branch-name>`

To get changes to a branch run the following:
* `git pull`

Most, if not all, of the above can be done through the IDE directly.
You can read about that here: https://code.visualstudio.com/docs/editor/versioncontrol


## Code Quality:
It can be hard to maintain a coherent style across a project when working
in a group. To help with this, we have added several packages to make sure
we are following the python formatting standard, and even some automatic
formatters and optimizers to do this for us. These packages and how to use
them is listed below:
* flake8 - flake8 is a package that checks whether we are following the
PEP8 standard, which is the python coding standard, in our project.
    * `cd src`
    * `flake8`
* black - black is an auto formatter created by people at facebook. It
automatically formats every file in the project to a specific style which
has been designed to be as readable as possible.
    * `cd src`
    * `black -l 120 .`
* isort - isort is a package that orders imports to the PEP8 standard, this
includes alphabetical order and more.
    * `cd src`
    * `isort -l 120 .`
* pre-commit - pre-commit is a package that enables to run git hooks on every
commit. This allows us to run the above packages for example before ever
letting our code out of our computers.
    * `pre-commit install`
    * Use GIT as usual
