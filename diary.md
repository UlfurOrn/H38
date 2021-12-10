# Diary

## Week 1:

### Monday, 22 November:
Today, after the morning lecture, we will start by getting to know the
team and the project itself. After that we will start work on collecting
requirements and perform a user analysis.

* Guðmundur:
    * User analysis and requirements
* Kolbeinn:
    * Requirements
* Kristófer:
    * MIA
* Smári:
    * Requirements
* Úlfur:
    * User analysis and requirements

There was not much work done on this day. Most of the day went into
getting to know each other and the project. We have however started
on gathering the requirements and found our target group for this
solution.


### Tuesday, 23 November:
Today, we will convert our requirements into use cases. Once we have
a broad overview of the use cases for the system we will start
designing the flow of the user interface. If we have time we will
start designing the interface as well.

* Guðmundur:
    * Use cases and use case diagram
* Kristófer:
    * MIA
* Kolbeinn:
    * Use cases
* Ríkharður (New member!):
    * UI Flow
* Smári:
    * Use cases
* Úlfur:
    * Use cases and UI flow, also started to explore designs
    for windows


Today, we were able to mostly complete writing the use cases. Each
one maps to a requirement and they were also placed in a use case
diagram. Once we got a broad overview of the use cases we started
to design the UI flow. When we got further along with both tasks
we started to experiment with UI designs.


### Wednesday, 24 November:
Today we will finish the use cases and start work on the design of
the program itself. We will be creating wireframes for every, or
at least close to every, window that the system will have. We will
also start creating the class diagrams for the three layers of the
system.

* Guðmundur:
    * Worked on the UI flow diagram and class diagram for the database.
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Finished UI Flow and worked on Use Cases
* Smári:
    * Use cases
* Úlfur:
    * Created initial draft of the look of many of the screens. Designed
    the database layer and initial draft of the other two.

We were able to finish the use cases and gotten far with the wireframes.
Most of the wireframes for the most important screens have been finished
apart from a few important ones dealing with the work requests and
reports. The class diagram has been started and mostly finished for the
database and the other two layers have gotten some love as well.


### Thursday, 25 November:
Today we will clean up work done on the other days and finish what is
left. This is mostly the class diagrams, window design and some stragglers
in the use cases. We will also start work on detailing what each method
in the logic layer should do. This is to hopefully increase our work
throughput in the following weeks.

* Guðmundur:
    * Worked on window designs for a fair number of windows and class diagrams.
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Worked on Class diagram and Use cases.
* Smári:
    * State diagram
* Úlfur:
    * Today I continued a bit with the class diagrams. After getting a
    better idea of it's structure I started work on explaining what each
    method in the logic layer should do. Finished about half of that.


Most of the puzzle pieces for the report are now ready. We just need to do
some cleanup and fixing. We left some design decisions, mostly regarding B
requirements, for tomorrow. We also started using Asana, a ticketing system,
to keep ourselves organized.


### Friday, 26 November:
We will start the day by filling Asana with all the tasks required for the
report. This will give us a better overview of what has been done and what
we still need to finish. We will also finish deciding on these design
decisions we mentioned above. Put the puzzle pieces together into a
complete report.

* Guðmundur:
    * Continued working on wireframes and UI flow. Also participated in writing 
    the design report.
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Class diagram finished and worked on the design report.
* Smári:
    * "Beutifying" Report
* Úlfur:
    * Created all the tasks in Asana. Most of the day went into the last
    design decisions and creating wireframes and details for them. Finished
    the day further detailing the logic layer and reviewing the report.

Last design day finished!! The week went mostly well, some days better than others.
We have a finished product that should (hopefully) not need to be changed all that
much. We will possibly do some more prep work over the weekend, like adding tickets
to Asana, but we will try to relax as well :)


## Week 2:

### Monday, 29 November:
Today is the first day of programming!! Well, to be more clear, this is the first
day we are allowed to program. Most of the day will probably go into setup. This
includes getting Github setup for everyone and setting up some code quality
packages. If we have enough time we will start with the database and prototype
the other two layers.

* Guðmundur:
    * Set up git virtual environment in VSC and got to know how to operate with git.
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Created and finished employee and contractor logic. Started on report logic.
* Smári:
    *
* Úlfur:
    * Today I came in a bit early to setup the git repository. Added linting, pre
    commit hooks and some more stuff to have the best code quality we can. Then I
    helped those that needed with connecting to the git repository. I had some
    extra time throughout the day so I started and finished the main database
    class and added two models for employees and locations that are now working.

Today we were able to setup the git repository and get most of us working on the
project. The database layer has mostly been finished, only needing some cleanup
as we discover any problems.


### Tuesday, 30 November:
Today we will finish getting everyone into git and start work on the logic layer
along with some rudimentary UI. By the end of today we would like to have the logic
for employees and locations mostly finished, and if there is time we will also work
on the logic for contractors, reports, etc...


* Guðmundur:
    * Made a model class for property, facility, contractor, report and request
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Continued work on report logic. Finished by the end of the day.
* Smári:
    *
* Úlfur:
    * Today I used the prototyping from the others to start work on creating a
    skeleton of the logic layer. I created a Paginator helper class that will be
    used to paginate results for the UI. After that I implemented the logic for
    employees and locations.

Today we were able to mostly finish the logic layer as well as setup a small prototype
for the UI. The logic layer is missing some of the filter and search options as well
as some specifics. We will build upon this in the next days and when needed.


### Wednesday, 1 December:
Today we will be putting most of our effort into the UI. We will try to get some of the
basic windows working, for example the main menu and the list windows. Some of us will
also be working on the database layer and logic layer, fixing any bugs or issues that
pop up.

* Guðmundur:
    * worked on logic classes for properties, requests and facilities.
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Refined report logic. Added in contractors.
* Smári:
    * Put the window designs into python, focusing on employees and locations. I
    experimented with a couple of ways of implementing classes and function for the UI,
    building on the code Úlfur wrote.
* Úlfur:
    * Today I had to go to work to put out some fires. To make up for it I worked till
    late yesterday and put in some hours after work today. I was able to finish the
    Window baseclass late last night and today I created the Main Menu and Employee
    list windows.

Today we were able to get some of the UI working!!! Not much else happened, in the
project itself, other than some fixes and improvements here and there.


### Thursday, 2 December:
Today we will be creating as many of the different window types needed as possible.
This means creating the View, Create and Update windows. We don't necessarily expect to
be able to finish them all, but hopefully we get far. We will also, again, be working
on adding the missing functionality for the logic and database layers.

* Guðmundur:
    * Worked on filtering methods for employees and properties
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Added in search function into list method. Added into all but one logic because of missing file. Will be added later.
* Smári:
    * Continued with python and experimenting ways to implement the UI.
* Úlfur:
    * Today I added a README to the project. I did this to explain the setup of the
    project, how to run the project, explaining the git workflow we are using and
    explaining the packages we are using to increase code quality. I also implemented
    the View and Create window superclasses as well as implementing subclasses of them
    for employees.

Today we were able to finish many of the needed window types. Employees can now be viewed
and created from the UI. Search and filter functionality has been implemented for some of
the logic layer and will be finished tomorrow.


### Friday, 3 December:
The goal of today is to get every aspect of the employee and location windows setup and
running. This includes, list, view, create, update, select functionality and more. We will
need to finish the Update superclass and any others needed.

* Guðmundur:
    * Made a few subclasses for ViewWindow
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Search options polished a bit. Implemented a function to display all the buttons in a fixed format so they would look nicer.
* Smári:
    *
* Úlfur:
    * Today I implemented the Update superclass as well as refactored a big chunk of the
    window logic. This allows us to reuse even more code and there is still some more that
    can be done in this area. I also finished connecting all the window logic so that we
    have a complete working system for employees and locations (for the most part).

Employee and logic UI is finished!! (almost)
This gives us a solid foundation moving into the next week.


## Week 3:

### Monday, 6 December:
Today we will continue with working on the windows, implementing windows for properties
and facilities. We will also be working on the authentication system. If we have extra time
we will be starting on the contractor logic.

* Guðmundur:
    *
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Authentication funtionality was worked on.
* Smári:
    *
* Úlfur:
    *


### Tuesday, 7 December:


* Guðmundur:
    * worked on SearchWindow Superclass
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Verification in logic where it applies was implemented. Made to verify inputs when creating or editing things to the database.
* Smári:
    *
* Úlfur:
    *


### Wednesday, 8 December:


* Guðmundur:
    *
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Working on trying to combine all validators into one file/location. Polished up some other functions
* Smári:
    *
* Úlfur:
    *


### Thursday, 9 December:


* Guðmundur:
    *
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    * Made a welcome window for the beginning of the program. Added window state into the program 
      so that in some scenarios some buttons are removed where not needed. Started working on the final report.
* Smári:
    *
* Úlfur:
    *


### Friday, 10 December:


* Guðmundur:
    *
* Kristófer:
    *
* Kolbeinn:
    *
* Ríkharður:
    *
* Smári:
    *
* Úlfur:
    *
