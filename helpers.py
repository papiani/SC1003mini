import csv
import random
# implement scoring algo, assign diversity score to each group and eventually display it
heirarchy =[
    'School','Gender' ,'CGPA' # edit the order of this list to give priority of split
]
getindex = {
    'School' :2,
    'Gender' :4,
    'CGPA' :5
}

def load_raw_data(path): # returns a list of rows (list of lists) in the csv
    # Tutorial Group,Student ID,School,Name,Gender,CGPA
    rows = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if True: # placeholder for conditions to clean data if required later
                rows.append(row)
    return rows

def segregate(data,index): # returns a dict where key is index_of_segreation, value is a list of entries belonging to that index
    uniques = []
    sorted = {}
    for entry in data:
        if entry[index] not in uniques:
            uniques.append(entry[index])
            x = [entry]
            sorted[entry[index]] = x
        else:
            temp = sorted[entry[index]]
            temp.append(entry)
            sorted[entry[index]] = temp
    return sorted

def diversityscore(groupls, heirarchy=heirarchy, getindex = getindex): # returns diversity score of groups
    points = 0.005
    totalscore = 0
    for parameter in heirarchy:
        points -=0.001
        index = getindex[parameter]
        for grp in groupls:
            tempgrp = grp
            for person in grp:
                tempgrp.remove(person)
                for otherperson in tempgrp:
                    if person[index] != otherperson[index]: # this will not work for cgpa, need to add cgpa functionality # TODO
                        totalscore +=points
    return totalscore

def random_change(grpls):
    # change must be within the same tutorial group
    grpnum = random.randint(0,len(grpls)-1)
    person = random.randint(0,4) # pick rndom person
    otherperson = random.randint(0,4) # pick rndom person
    
    # make selection of options of people with the same tutorial grp and shuffle the list of options
    options = []
    index = -1
    for grp in grpls:
        index+=1
        if grp[0][0] == grpls[grpnum][person][0]: #same tg
            options.append((index,otherperson))
    grp2,person2= random.choice(options) # picked person to swap with

    # now do the swap
    tempperson1 = grpls[grpnum].pop(person)
    tempperson2 = grpls[grp2].pop(person2)
    grpls[grpnum].append(tempperson2)
    grpls[grp2].append(tempperson1)
    
    return grpls

def initialise_groups(raw_data):
    # YONG JIA HOMEWORK

