import csv
import random
import copy
import os
import matplotlib.pyplot as plt

def load_raw_data(path): # returns a list of rows (list of lists) in the csv
    # Tutorial Group,Student ID,School,Name,Gender,CGPA
    rows = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if True: # placeholder for conditions to clean data if required later
                rows.append(row)
    return rows

def segregate(data,index): # returns a dict where key is index_of_segregation, value is a list of entries belonging to that index
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

def initialise_groups(raw_data):
    # randomly generate grps of 5, list of lists
    groups_list = []
    sorted = segregate(raw_data,0) # sorts into dicts of ppl within same tutorial group
    for tut_grp,grp in sorted.items():
        maxed = len(grp) # num of ppl in specific tutorial group
        group_size = 5
        i = 0
        while i + group_size < maxed:
            new_grp = grp[i:i + group_size]
            i = i + group_size
            groups_list.append(new_grp)
    return groups_list
# initialise data tools
history = []
# read csv
raw_data = load_raw_data("records.csv") # in format TutorialGroup, StudentID, School, Name, Gender, CGPA
# initialise lists of 5 randomly
groupings = initialise_groups(raw_data)
# increase diversity of groups thru random changes
hierarchy = ['School','Gender','CGPA']

get_index = {
    "Tutorial Group":0,
    "Student ID":1,
    "School":2,
    "Name":3,
    "Gender":4,
    "CGPA":5
}


def single_diversity_score(single_grp, hierarchy = hierarchy, get_index = get_index):
    points = 0.5
    total_score = 0
    for parameter in hierarchy:
        points -= 0.1
        index = get_index[parameter]
        for i, person in enumerate(single_grp):
            for j in range(i + 1, len(single_grp)):  # Only cmp with people after current
                other_person = single_grp[j]
                if parameter == 'CGPA':
                    total_score += points * (abs(float(person[index]) - float(other_person[index])))
                if person[index] != other_person[index]:
                    total_score += points
    return total_score

def random_change(groups):
    
    group_copy = copy.deepcopy(groups)
    
    # Pick a rnd group and person
    group_num = random.randint(0, len(group_copy) - 1)
    group = group_copy[group_num]
    
    if not group:
        return None, None, None  # Skip empty group
    
    person_index = random.randint(0, len(group) - 1)
    person = group[person_index]
    tutorial_group = person[0]  # Tutorial group is in column 0
    
    # Find all candidates in other groups with the same tutorial group
    options = []
    for i, grp in enumerate(group_copy):
        for j, candidate in enumerate(grp):
            if i == group_num and j == person_index:
                continue  # Skip the same person
            if candidate[0] == tutorial_group:
                options.append((i, j))
    
    if not options:
        return None, None, None  # No valid swap
    
    # Pick a random candidate and perform the swap
    group2_index, person2_index = random.choice(options)
    
    # Perform the swap
    group_copy[group_num][person_index], group_copy[group2_index][person2_index] = group_copy[group2_index][person2_index], group_copy[group_num][person_index]
    
    return group_copy, group_num, group2_index


def swap_groups(new_groups, grp1_idx, grp2_idx, current_total_score, group_scores):
    # Only recalculate the 2 changed groups
    new_score_grp1 = single_diversity_score(new_groups[grp1_idx], hierarchy, get_index)
    new_score_grp2 = single_diversity_score(new_groups[grp2_idx], hierarchy, get_index)
    
    # Calculate new total by removing old scores and adding new scores
    new_total_score = (current_total_score 
                      - group_scores[grp1_idx]    # Remove old group 1 score
                      - group_scores[grp2_idx]    # Remove old group 2 score
                      + new_score_grp1            # Add new group 1 score
                      + new_score_grp2)           # Add new group 2 score
    
    # Acp if better 
    if new_total_score > current_total_score:
        current_total_score = new_total_score
        
        # Update the scores for these two groups
        group_scores[grp1_idx] = new_score_grp1
        group_scores[grp2_idx] = new_score_grp2
        return current_total_score, True
    return current_total_score, False     
        

def final_tabulation(groups_list):
    if os.path.exists('output.csv'):
        os.remove('output.csv')
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        counter = 0
        for grp in groups_list:
            # Tutorial Group,Student ID,School,Name,Gender,CGPA
            header = [f'GROUP {counter} - TG','Student ID','School','Name','Gender','CGPA']
            writer.writerow(header)
            for person in grp:
                writer.writerow(person)
            counter += 1

def time_linegraph(data):
    x_values =[]
    y_values =[]
    for x,y in data:
        x_values.append(x)
        y_values.append(y)

    # Create the line chart
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='blue')

    # Add labels and title
    plt.xlabel('Run-cycles or "Epochs"')
    plt.ylabel('Diversity Score')
    plt.title('Diversity over runtime')

    # Show the chart
    plt.grid(True)
    plt.tight_layout()
    plt.show()

initial = groupings.copy()
group_scores = {}
for i, grp in enumerate(initial):
    group_scores[i] = single_diversity_score(grp, hierarchy, get_index)

current_total_score = sum(group_scores.values())
initial_score = current_total_score

for epoch in range(1,10001):
    # Try a swap
    new_groups, grp1_idx, grp2_idx = random_change(initial)
    
    if new_groups is None:
        continue  # No valid swap found, try again

    current_total_score, accepted = swap_groups(new_groups, grp1_idx, grp2_idx, current_total_score, group_scores)
    if accepted:
        initial = new_groups

    print(f"Epoch {epoch}: Diversity Score = {current_total_score:.2f}")
    # Record history for graph
    history.append((epoch, current_total_score))

time_linegraph(history)
final_tabulation(initial)

