# Blog: Describing the engineering process of my 4th year project for DCU.
## The project involves recognising human activity using SAX and machine learning techniques.

**Shane Creedon**  
**Student ID: 15337356**  
**4th year Computer Applications and Software Engineering student in DCU**  

## Blog Post #1 | Proposal Submission and Upcoming Goals | 04/11/2018

The basis for the project is recognising human activity using wearable sensor technology based on 
Symbolic Aggregate Approximation (SAX) and Machine Vision.

After discussing the idea with Tomas in great detail, we both agreed to work together on this project as part of my 4th year project.
With the idea in mind, I constructed the proposal documented due for both Tomas and my presentation supervisors.
The proposal specified all the nitty-gritty details of the project and I hope gave clear insight into what we are trying to achieve.

I sent the document to Tomas for review and discussion the idea with the project presentation supervisors (Darragh & Mark)
who all thankfully approved the idea and allowed me to move forward.

My next primary goal is to set up Continuous Integration (CI) practices for my projects GitLab either using the GitLab
built-in CI tools or use something like Jenkins / Teamcity.

Week 9 requires the completion of my functional specification which needs to be ~25 pages in length describing the project
in great detail using both easy to understand language and UML diagrams depicting the technical structure.   

Currently it is week 7, I will aim to get these above two steps complete within the next week.

## Blog Post #2 | Development of the functional specification | 1/12/2018

Like most students, I have began working on my Function Specification discussing my project
idea in great detail. Within the specification, I discuss:
- An introduction section, where I overview the project and why we are building it.

- Section two provides a *General Description* of the product/system functions.
  It is in this section I detail a high-level abstract look at the individual functions our application will perform.
  I try my best to be as thorough as possible through the document while offering visualisations of the functionality for
  a stronger conceptual understanding.
  This section also discusses the many constraints my system will face throughout its development.

-  Section three will discuss all of the functions of the system in great, great detail.
   Each function will have a description, criticality overview, technical issues faced, 
   dependencies on other requirements and other details that many offer insight into the function.

- Section 4 looks at the system architecture and how the overall system will piece together.
  I offer visualisations here constructed on behalf of showing how system components tie with one another.

- Section 5 looks at the high-level design / abstract view of the system. 
  Within the section displayed are 3 Data-Flow Diagrams showing how data moves around individual components.
  There is also a minimalistic conceptual class diagram of how the application classes will interact.
  Finally, there is a use case diagram showing how a particular user may interact with the system.

- Section 6 shows the schedule of project activities over the course of the project timeline.
  I showcase a Gantt Chart diagram to display this information.

- Section 7 is a list of references I made use of when developing the project idea.

The blog is written in [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).
Markdown is a simple text-based mark-up language.

## Blog Post #3 | Week 12 - End of Semester One | 18/12/2018

Not much progress has been made on the project since I finished the functional specification back
in week 7/8. Other modules have taken up my time however, I have been doing some research on the topic
of Human Activity Recognition(HAR) and Machine Learning. In addition, i've looked into libraries
and possible design choices I could take when developing my application.

I came across and interesting article on how SAX (Symbolic Aggregate Approximation) can be implemented
within Java and I may use this to aid my development within Python. Google Scholar has been helpful for
finding Machine Learning related articles in the field. I have been looking a lot into **Supervised Learning**
research papers and methods to optimise convolutional neural networks for image classification.
Now, I will take some time off to spend with my family over christmas but once January hits, I will
be back in the books for the exams.

## Blog Post #4 | Examination Period | 06/1/2019

Happy new year to those reading and a happy christmas as well. I had been researching the project over the last
few days and coding some small prototypes to grasp how I was going to build the proclaimed software specified in the 
functional specification. With the DCU exams in several days time, I have decided to but the project on the back seat
while I focus thoroughly on my exams.

## Blog Post #5 | Beginning development of the project | 26/01/2019

Returning back from a week-long trip, I have started working on the project. I initially wanted to understand how
I was going to build a desktop application using Python. I looked into several different libraries which seemed to
offer the ability to do so. Eventually after enough research, I decided to go with PyQt5, which is based on QT. Qt is set of cross-platform C++ libraries that implement high-level APIs for accessing many aspects of modern desktop and mobile systems.

Additionally, I looked into how to convert a `.py` file into a `.exe` file for end-users which I managed to come across
a magical library for this exact purpose: **PyInstaller**. PyInstaller allows me to convert a .py file into a .exe file
along with a `.spec` configuration file for how the .exe file is run. 

## Blog Post #6 | Symbolic Aggregate Approximation | 28/01/2019

The project directory structure has been created. I have created a small template website which is intended
to host the download link for the application. In addition, the SAX python file (symbolic_aggregate_approximation.py)
was created and coded up to convert the PPG exercise data sets into a string of characters.

For example:
`cccccaabbcbcabbddddbbabdbebebeeeebdabdbdbaa`

The string above is just a simple example, the real string would be FAR FAR longer, representative of an hour in time.
We have long strings like this for all 4 activities: *Walk/Run/Low Resistance Bike/High Resistance Bike*

## Blog Post #7 | Bitmap Generation | 29/01/2019

With the ability to generate SAX strings from the PPG data sets, the next step was to convert these strings into images.
To do this, I found a library online called: `text-to-image`. This library allowed me to convert a subsequence of letters
from the SAX string into a grey-scale pixel-based image. Specifically, the images are 32 pixels in size and after generating
all the images for each SAX string for each activity, the **total number of available training images is greater than 10,000**.

This grey-scale image approach may not be the optimal approach for this problem and for convolutional neural network training but,
I will address this with my supervisor and I will research online and find out whatever the best approach is for image classification
in relation to the technique of Symbolic Aggregate Approximation(SAX).