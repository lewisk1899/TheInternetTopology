# Lewis Koplon/Ramon Driesen
# Professor Lazos
# ECE 578
# The Internet Topology
import matplotlib.pyplot as plt
import numpy as np


class AS:
    def __init__(self, number):
        self.number = number
        self.p2p = 0  # peer degree
        self.p2c = 0  # customer degree
        self.prov = 0  # provider degree
        self.glob = 0  # global degree
        self.customers = []


# Section 2.1 AS Classification
def parse_file(file_name):
    as_types_count = [0, 0,
                      0]  # [transit/access, content, enterprise] we should see three different types of Autonomous Systems, in this such order
    file = open(file_name)
    as_counter = 0
    for line in file:
        if line.startswith('#'):  # this is useless information, so we wont count it for anything
            continue
        else:
            line = line.strip()  # get rid of newline
            split_line = line.split('|')  # split on the | as that is how the file is sectioned
            if split_line[2].lower() == "transit/access":  # count the t/a AS
                as_types_count[0] += 1
            elif split_line[2].lower() == "content":  # count the c AS
                as_types_count[1] += 1
            elif split_line[2].lower() in ["enterprise", "enterpise"]:  # count the e AS
                as_types_count[2] += 1
            as_counter += 1  # count the total AS

    return as_types_count, as_counter  # return for processing data


def pie_chart(amount, title):
    labels = "transit/access", "content", "enterprise"
    explode = (0, 0, 0)
    figure1, ax1 = plt.subplots()  # creating the figure
    ax1.pie(amount, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)  # Percentage Distribution of Autonomous System Classes in 2021
    plt.show()  # showing the figure


def bar_graph(amount, total):
    labels = "transit/access", "content", "enterprise"
    percentages = [number / total for number in amount]
    figure1 = plt.figure()
    ax1 = figure1.subplots  # creating the figure
    plt.bar(labels, percentages)
    plt.ylabel('Percentage')
    plt.title('Percentage Distribution of Autonomous System Classes in 2015')

    plt.show()  # showing the figure


def as_classification():
    as_types_2021, as_count_2021 = parse_file("20210401.as2types.txt")  # parsing the data sets from CAIDA
    as_types_2015, as_count_2015 = parse_file("20150801.as2types.txt")
    # printing findings and using them to create our needed graphs via matplotlib
    print("April 2021 as classes [transit/access, content, enterprise]:", as_types_2021, "total AS count",
          as_count_2021)
    pie_chart(as_types_2021, "Percentage Distribution of Autonomous System Classes in 2021")
    print("August 2015 as classes [transit/access, content, enterprise]:", as_types_2015, "total AS count",
          as_count_2015)
    bar_graph(as_types_2015, as_count_2015)


#############################################################################
# Section 2.2 Topology Inference Through AS Links

def histogram(x, title, type):
    arr2 = []
    bins_list = [0, 1, 2, 5, 101, 201, 1000]  # bins
    for as_i in x:
        if type == 'Global':
            arr2.append(as_i.glob)
        elif type == 'Customer':
            arr2.append(as_i.p2c)
        elif type == 'Peer':
            arr2.append(as_i.p2p)
        elif type == 'Provider':
            arr2.append(as_i.prov)
    hist, bin_edges = np.histogram(arr2, bins=bins_list)  # histogram
    fig, ax = plt.subplots()
    ax.bar(range(len(hist)), hist, width=1, edgecolor='k')
    ax.set_xlabel(title)  # x-axis title
    ax.set_ylabel('Number of Autonomous Systems')  # y-axis title
    title = 'Number of Autonomous Systems that hold ' + title
    ax.set_title(title)  # title
    ax.set_xticks(range(len(bins_list) - 1))
    ax.set_xticklabels(['{} - {}'.format(bins_list[i], bins_list[i + 1]) for i, j in enumerate(hist)])
    plt.show()


def inc_degree(as_1, as_2, classification):
    # it is just a peer to peer connection
    if classification == '0':
        as_1.p2p += 1
        as_2.p2p += 1
    # it is just a customer to provider connection
    else:
        as_1.prov += 1
        as_1.customers.append(as_2)  # as1 is the provider to as2, therefore we will add as2 to as1s customer list
        as_2.p2c += 1

    as_1.glob += 1
    as_2.glob += 1


def section_2b(filename):
    list_as = []
    list_as_objects = []
    file = open(filename)
    i = 0
    # go through line by line
    for line in file:
        # ignore the useless information
        if not line.startswith('#'):
            line = line.strip()  # process the line
            split_line = line.split("|")
            # we haven't found this as in the list
            if split_line[0] not in list_as:
                list_as.append(split_line[0])
                temp_as1 = AS(split_line[0])
                list_as_objects.append(temp_as1)
            else:
                # find the as in our object list
                for AutoSys1 in list_as_objects:
                    if AutoSys1.number == split_line[0]:
                        temp_as1 = AutoSys1
            # we haven't found this as in the list
            if split_line[1] not in list_as:
                list_as.append(split_line[1])
                temp_as2 = AS(split_line[1])
                list_as_objects.append(temp_as2)
            else:
                # find the as
                for AutoSys2 in list_as_objects:
                    if AutoSys2.number == split_line[1]:
                        temp_as2 = AutoSys2

            inc_degree(temp_as1, temp_as2, split_line[2])  # function to handle altering respective private variables

        i += 1
        if i > 1000:
            break

        print(i)

    return list_as_objects


def piechart_2(_as_list,title):
    data = [0, 0, 0]  # Enterprise, Content, Transit
    for _as in _as_list:
        if _as.p2p == 0 and _as.p2c == 0:
            data[0] += 1
        if _as.p2p >= 1 and _as.p2c == 0:
            data[1] += 1
        if _as.p2c >= 1:
            data[2] += 1
    pie_chart(data, title)


#################################################################################################################################

def run():
    as_classification()
    # test
    list_obj = section_2b("20211001.as-rel2.txt")
    # list_obj = section_2b("testfor2b.txt")
    histogram(list_obj, "Global Node Degree", 'Global')
    histogram(list_obj, "Customer Degree", 'Customer')
    histogram(list_obj, "Peer Degree", 'Peer')
    histogram(list_obj, "Provider Degree", 'Provider')

    piechart_2(list_obj, 'Percentage Distribution of Autonomous System Classes in 2021 According to Link Traversal')

run()