list1 = [1,2,3,4,5,6,7,8,9,10]
list2 = [6,7,8,9,10,11,12,13,14,15]

unique_to_list2 = list(set(list2) - set(list1))

print(unique_to_list2)