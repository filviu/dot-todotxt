#!/usr/bin/python

""" TODO.TXT Bird's Eye View Reporter
USAGE:
    birdseye.py [todo.txt] [done.txt]

USAGE NOTES:
    Expects two text files as parameters, each of which formatted as follows:
    - One todo per line, ie, "call Mom"
    - with an optional project association indicated as such: "+projectname"
    - with the context in which the tasks should be completed, indicated as such: "@context"
    - with the task priority optionally listed at the front of the line, in parens, ie, "(A)"

    For example, 4 lines of todo.txt might look like this:

    +garagesale @phone schedule Goodwill pickup
    (A) @phone Tell Mom I love her
    +writing draft Great American Novel
    (B) smell the roses

    The done.txt file is a list of completed todos from todo.txt.

    See more on todo.txt here:
    http://todotxt.com


OUTPUT:
    Displays a list of:
    - working projects and their percentage complete
    - contexts in which open todos exist
    - contexts and projects with tasks that have been prioritized
    - projects which are completely done (don't have any open todos)

CHANGELOG:
    2016.03.17 - Update for Python 3. Tx, JonathanReeve!
    2006.07.29 - Now supports p:, p- and + project notation.  Tx, Pedro!
    2006.05.02 - Released
"""


import sys

__version__ = "1.2"
__date__ = "2006/05/02"
__updated__ = "2016/03/17"
__author__ = "Gina Trapani (ginatrapani@gmail.com)"
__copyright__ = "Copyright 2006 - 2016, Gina Trapani"
__license__ = "GPL"
__history__ = """
1.2 - Update for Python 3. Tx, JonathanReeve!
1.1 - Now supports p:, p- and + project notation.  Tx, Pedro!
1.0 - Released.
"""

def usage():
    print("USAGE:  %s [todo.txt] [done.txt]" % (sys.argv[0], ))

def printTaskGroups(title, taskDict, priorityList, percentages):
    print("")
    print("%s"% (title,))
    separator("-")
    if not taskDict:
        print("No items to list.")
    else:
        # sort the dictionary by value
        # http://python.fyxm.net/peps/pep-0265.html
        items = [(v, k) for k, v in list(taskDict.items())]
        items.sort()
        items.reverse()             # so largest is first
        items = [(k, v) for v, k in items]

        for item in items:
            if item[0] in priorityList:
                if item[0] not in percentages:
                    printTaskGroup(item[0], (0,0,0,-1), "*")
                else:
                    printTaskGroup(item[0], percentages[item[0]], "*")

        for item in items:
            if item[0] not in priorityList:
                if item[0] not in percentages:
                    printTaskGroup(item[0], (0,0,0,-1), " ")
                else:
                    printTaskGroup(item[0], percentages[item[0]], " ")

def printTaskGroup(dim, pctage, star):
    if pctage[3] > -1:
        progressBar = ""
        numStars = int(pctage[3]//10)
        progressBar = "=" * numStars
        numSpaces = 10 - numStars
        for n in range(numSpaces):
            progressBar += " "

        if pctage[3] > 9:
            displayTotal = " %d%%"% (pctage[3], );
        else:
            displayTotal = "  %d%%"% (pctage[3], );
        print("%s %s [%s] %s (%d/%d todos)"% (star, displayTotal, progressBar,  dim, pctage[1], pctage[2],))
    else:
        print("%s %s (%d/%d todos)"% (star, dim, pctage[1], pctage[2],))

def separator(c):
    sep = ""
    sep = c * 42
    print(sep)


def main(argv):
    # make sure you have all your args
    if len(argv) < 2:
        usage()
        sys.exit(2)

    # process todo.txt
    projects = {}
    contexts = {}
    projectPriority = []
    contextPriority = []
    completedTasks = {}
    for fn in [argv[0], argv[1]]:
        try:
            f = open (fn)
            for line in f:
                prioritized = False
                completed = False
                words = line.split()
                if words and words[0].startswith("("):
                    prioritized = True
                if words and words[0] == "x":
                    completed = True
                normalCount = 1 if not completed else 0
                completedCount = 0 if not completed else 1
                for word in words:
                    if word[0:2] == "p:" or word[0:2] == "p-" or word[0:1] == "+":
                        if word not in projects:
                            projects[word] = normalCount
                        else:
                            projects[word] = projects.setdefault(word,0)  + normalCount
                        if prioritized:
                            projectPriority.append(word)
                        if completed:
                            if word not in completedTasks:
                                completedTasks[word] = completedCount
                            else:
                                completedTasks[word] = completedTasks.setdefault(word, 0) + completedCount
                    if word[0:1] == "@":
                        if word not in contexts:
                            contexts[word] = normalCount
                        else:
                            contexts[word] = contexts.setdefault(word, 0)  + normalCount
                        if prioritized:
                            contextPriority.append(word)
                        if completed:
                            if word not in completedTasks:
                                completedTasks[word] = completedCount
                            else:
                                completedTasks[word] = completedTasks.setdefault(word, 0) + completedCount
            f.close()
        except IOError:
            print("ERROR:  The file named %s could not be read."% (argv[0], ))
            usage()
            sys.exit(2)

    # calculate percentages
    projectPercentages = {}
    projectsWithNoIncompletes = {}
    contextsWithNoIncompletes = {}
    src1 = [(k, v, True) for k,v in projects.items()]
    src2 = [(k, v, False) for k,v in contexts.items()]
    for it in (src1 + src2):
        project = it[0]
        openTasks = it[1]
        isProject = it[2]
        if project in completedTasks:
            closedTasks = completedTasks[project]
        else:
            closedTasks = 0
        totalTasks = openTasks + closedTasks
        percentage = (closedTasks*100) / totalTasks
        projectPercentages[project] = (openTasks, closedTasks, totalTasks, percentage)
        if openTasks == 0:
            if isProject:
                projects.pop(project, None)
                projectsWithNoIncompletes[project] = (0,0,0,0)
            else:
                contexts.pop(project, None)
                contextsWithNoIncompletes[project] = (0,0,0,0)



    #print "TODO.TXT Bird's Eye View Report %s"% ( datetime.date.today().isoformat(), )
    print("")
    print("TODO.TXT Bird's Eye View Report")

    separator("=")

    printTaskGroups("Projects with Open TODOs (done/total)", projects, projectPriority, projectPercentages)
    printTaskGroups("Contexts with Open TODOs (done/total)", contexts, contextPriority, projectPercentages)
    printTaskGroups("Completed Projects (No open TODOs)", projectsWithNoIncompletes, projectPriority, projectPercentages)
    printTaskGroups("Fulfilled Contexts (No open TODOs)", contextsWithNoIncompletes, projectPriority, projectPercentages)
    print("")
    print("* Projects and contexts with an asterisk next to them denote prioritized tasks.")
    print("Project with prioritized tasks are listed first, then sorted by number of open todos.")
    print("")




if __name__ == "__main__":
    main(sys.argv[1:])
