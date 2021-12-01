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


## Code Quality:



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
