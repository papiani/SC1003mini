from helpers import *

# read csv
raw_data = load_raw_data("records.csv") # in format TutorialGroup, StudentID ,School, Name ,Gender ,CGPA

# segregate by school, list for each sch
dictbysch = segregate(raw_data,2)

    

# within each sch segregate by gender, list, put all these lists in list called 'buckets'
# these groups are basically as distinct as can be from each other but within each bucket, they only differ by cgpa

#i did this work
# additional comments
