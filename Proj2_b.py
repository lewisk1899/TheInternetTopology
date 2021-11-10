# Lewis Koplon/Ramon Driesen
# Professor Lazos
# ECE 578
# The Internet Topology
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

class AS:
    def __init__(self, number):
        self.number = number
        self.p2p = 0
        self.p2c = 0
        self.prov = 0
        self.glob = 0

def pie_chart(x, title):
    arr = []
    labels = "transit/access", "content", "enterprise"
    explode = (0, 0, 0)
    figure1, ax1 = plt.subplots()  # creating the figure
    ax1.pie(x, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90) # replaced amount with x
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    plt.show()  # showing the figure

def histogram(x, title):
    arr1 = []
    arr2 = []
    bins_list = [0, 1, 2, 5, 101, 201, 1000]
    for as_i in x:
        arr1.append(int(as_i.number))
        arr2.append(as_i.glob)
    plt.hist(arr2, bins=bins_list)
    plt.title(title)
    plt.show()

def inc_degree(as_i, classification, x):
    if (classification == '0'):
        as_i.p2p += 1            
    else:
        if (x is True): 
            as_i.prov += 1
        else:
            as_i.p2c += 1
    as_i.glob += 1

# Section 2.2 Topology Inference Through AS Links
def section_2b(filename):
    list_as = []
    list_as_objects = []
    file = open(filename)
    i = 0
    for line in file:
        if (not line.startswith('#')):
            line = line.strip()
            split_line = line.split("|")
            # we havent found this as in the list
            if (split_line[0] not in list_as):
                list_as.append(split_line[0])
                temp_as1 = AS(split_line[0])
                list_as_objects.append(temp_as1)
                inc_degree(temp_as1, split_line[2], True)
            else:
                # find the as in our object list
                for AutoSys1 in list_as_objects:
                    if (AutoSys1.number == split_line[0]):
                        temp_as1 = AutoSys1
                        inc_degree(temp_as1, split_line[2], True)
            # we havent found this as in the list
            if (split_line[1] not in list_as):
                list_as.append(split_line[1])
                temp_as2 = AS(split_line[1])
                list_as_objects.append(temp_as2)
                inc_degree(temp_as2, split_line[2], False)
            else:
                #find the as
                for AutoSys2 in list_as_objects:
                    if (AutoSys2.number == split_line[1]):
                        temp_as2 = AutoSys2
                        inc_degree(temp_as2, split_line[2], False)
        i += 1
        if (i <100000):
            continue 
        else:
            break

    return list_as_objects

def main():
    #test
    list_obj = section_2b("2bfile.txt")
    #list_obj = section_2b("testfor2b.txt")
    #histogram(list_obj, "Global Node Degree")
    histogram(list_obj, "Customer Degree")
    #histogram(list_obj, "Peer Degree")
    #histogram(list_obj, "Provider Degree")
    #pie_chart(list_obj, "Class Distribution of of ASes")
if __name__ == "__main__":
    main()