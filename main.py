from helpers import *
from datatools import *
import copy
# initialise data tools
epochvdiversity = []
# read csv
raw_data = load_raw_data("records.csv") # in format TutorialGroup, StudentID ,School, Name ,Gender ,CGPA
# initialise lists, not going to be random
groupings = initialise_groups(raw_data)
# increase diveristy of groups thru random changes
heirarchy = ['School','Gender','CGPA']
indexes = {
    "Tutorial Group":0,
    "Student ID":1,
    "School":2,
    "Name":3,
    "Gender":4,
    "CGPA":5
}
initial = groupings.copy()

initial_diversity_score = diversityscore(initial,heirarchy,indexes)

epochcounter = 0
while epochcounter<10000:
    print(f"Epoch: {epochcounter}")
    epochcounter+=1
    epochvdiversity.append((epochcounter,initial_diversity_score))
    alternative = random_change(initial)
    alternative_diversity_score = diversityscore(alternative,heirarchy,indexes)
    if alternative_diversity_score>initial_diversity_score: # add randomness to this
        print('-----------------------CHANGE--------------------')
        print(f"{alternative_diversity_score} is greater than {initial_diversity_score}")
        initial = copy.deepcopy(alternative)
        initial_diversity_score = alternative_diversity_score
print(epochvdiversity)
time_linegraph(epochvdiversity)



# additional comments
