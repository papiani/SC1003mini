import csv
import random
import copy
import os
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

def single_diversityscore(single_grp, heirarchy=['School','Gender','CGPA'], getindex={'School':2,'Gender':4,'CGPA':5}):
    points = 0.5
    totalscore = 0
    for parameter in heirarchy:
        points -= 0.1
        index = getindex[parameter]
        for i, person in enumerate(single_grp):
            for j in range(i + 1, len(single_grp)):  # Only compare with people after current
                otherperson = single_grp[j]
                if parameter == 'CGPA':
                    totalscore += points * (abs(float(person[index]) - float(otherperson[index])))
                if person[index] != otherperson[index]:
                    totalscore += points
    return totalscore

def random_change(groups):
    
    grpc1 = copy.deepcopy(groups)
    
    # Pick a random group and person
    grpnum = random.randint(0, len(grpc1) - 1)
    group = grpc1[grpnum]
    
    if not group:
        return None, None, None  # Skip empty group
    
    person_idx = random.randint(0, len(group) - 1)
    person = group[person_idx]
    tutorial_group = person[0]  # Tutorial group is in column 0
    
    # Find all candidates in other groups with the same tutorial group
    options = []
    for i, grp in enumerate(grpc1):
        for j, candidate in enumerate(grp):
            if i == grpnum and j == person_idx:
                continue  # Skip the same person
            if candidate[0] == tutorial_group:
                options.append((i, j))
    
    if not options:
        return None, None, None  # No valid swap
    
    # Pick a random candidate and perform the swap
    grp2_idx, person2_idx = random.choice(options)
    
    # Perform the swap
    grpc1[grpnum][person_idx], grpc1[grp2_idx][person2_idx] = grpc1[grp2_idx][person2_idx], grpc1[grpnum][person_idx]
    
    return grpc1, grpnum, grp2_idx


def initialise_groups(raw_data):
    # randomly generate grps of 5, list of lists
    grpls = []
    sorted = segregate(raw_data,0) # sorts into dicts of ppl within same tg
    for tg,grp in sorted.items():
        maxed = len(grp) # num of ppl in specific tg
        grpsize = 5
        i = 0
        while i + grpsize < len(grp):
            newgrp = grp[i:i + grpsize]
            i = i + grpsize
            grpls.append(newgrp)
    return grpls

def final_tabulation(grpls):
    if os.path.exists('output.csv'):
        os.remove('output.csv')
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        counter = 0
        for grp in grpls:
            # Tutorial Group,Student ID,School,Name,Gender,CGPA
            header = [f'GROUP {counter} - TG','Student ID','School','Name','Gender','CGPA']
            writer.writerow(header)
            for person in grp:
                writer.writerow(person)
            counter+=1
        




