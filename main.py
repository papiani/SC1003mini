from helpers import *
from datatools import *
import copy
# initialise data tools
history = []
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
group_scores = {}
for i, grp in enumerate(initial):
    group_scores[i] = single_diversityscore(grp, heirarchy, getindex)

current_total_score = sum(group_scores.values())
initial_score = current_total_score

for epoch in range(1,10001):
    # Try a swap
    new_groups, grp1_idx, grp2_idx = random_change(initial)
    
    if new_groups is None:
        continue  # No valid swap found, try again
    
    
    # === DELTA SCORING - Only recalculate the 2 changed groups ===
    new_score_grp1 = single_diversityscore(new_groups[grp1_idx], heirarchy, getindex)
    new_score_grp2 = single_diversityscore(new_groups[grp2_idx], heirarchy, getindex)
    
    # Calculate new total by removing old scores and adding new scores
    new_total_score = (current_total_score 
                      - group_scores[grp1_idx]    # Remove old group 1 score
                      - group_scores[grp2_idx]    # Remove old group 2 score
                      + new_score_grp1            # Add new group 1 score
                      + new_score_grp2)           # Add new group 2 score
    
    # Accept if better (greedy hill-climbing)
    if new_total_score > current_total_score:
        # Accept the change
        current_groups = new_groups
        current_total_score = new_total_score
        
        # Update the cache for these two groups
        group_scores[grp1_idx] = new_score_grp1
        group_scores[grp2_idx] = new_score_grp2
        
        print(f"Epoch {epoch}: NEW BEST = {current_total_score:.2f} (+{current_total_score - initial_score:.2f})")
    
    # Record history for graph
    history.append((epoch, current_total_score))

time_linegraph(history)
final_tabulation(initial)

