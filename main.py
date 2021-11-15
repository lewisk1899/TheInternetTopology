# Lewis Koplon/Ramon Driesen
# Professor Lazos
# ECE 578
# The Internet Topology
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
import time


class AS:
    def __init__(self, number):
        self.number = number
        self.p2p = 0  # peer degree
        self.p2c = 0  # customer degree
        self.prov = 0  # provider degree
        self.glob = 0  # global degree
        self.customers = []
        self.peers = []
        self.providers = []
        self.prefix_space_size = 0


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

def histogram(as_list, title, _type):
    data = []
    bins_list = [0, 1, 2, 5, 101, 201, 1000]  # bins
    for as_i in as_list:
        if _type == 'Global':
            data.append(as_i.glob)
        elif _type == 'Customer':
            data.append(as_i.p2c)
        elif _type == 'Peer':
            data.append(as_i.p2p)
        elif _type == 'Provider':
            data.append(as_i.prov)
    hist, bin_edges = np.histogram(data, bins=bins_list)  # histogram
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
        as_1.peers.append(as_2)  # append peers to eachother
        as_2.peers.append(as_1)
    # it is just a customer to provider connection
    else:
        as_1.prov += 1
        as_1.customers.append(as_2)  # as1 is the provider to as2, therefore we will add as2 to as1s customer list
        as_2.providers.append(as_1)  # as2 is a provider
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
        if i > 500000:
            break
        print(i)

    return list_as_objects


def piechart_2(_as_list, title):
    data = [0, 0, 0]  # Enterprise, Content, Transit
    for _as in _as_list:
        if _as.p2p == 0 and _as.p2c == 0:
            data[0] += 1
        if _as.p2p >= 1 and _as.p2c == 0:
            data[1] += 1
        if _as.p2c >= 1:
            data[2] += 1
    pie_chart(data, title)


def find(as_number, as_list):
    for _as in as_list:  # go through the list of as
        if _as.number == as_number:  # find the matching as
            return _as  # return the as
        return None


def parse_prefix_file(file, as_list):
    file = open('prefixtest.txt')
    i = 0
    k = 0
    for line in file:
        line = (line.strip()).split('\t')  # [IP prefix, prefix length, AS]
        try:
            _as = find(int(line[2]), as_list)  # return the _as
        except _as is None:
            _as.prefix_space_size += int(line[1])
            print("AS number", line[2], "is not a valid AS")
            k += 1
        i += 1
        print(i)
        print(k)


def prefix_histogram(as_list, title):
    data = []
    for _as in as_list:
        data.append(_as.prefix_space_size)
    print(max(data))
    hist, bin_edges = np.histogram(data)  # histogram
    fig, ax = plt.subplots()
    ax.bar(range(len(hist)), hist, width=1, edgecolor='k')
    ax.set_xlabel('Space Size')  # x-axis title
    ax.set_ylabel('Frequency')  # y-axis title
    title = "IP Space Size Frequency"
    ax.set_title(title)  # title
    plt.show()


#################################################################################################################################
########################### Inference of Tier-1 ASes
def connected(clique, _as):
    connected = True
    for _as_from_clique in clique:
        if not ((_as in _as_from_clique.customers or _as in _as_from_clique.providers or _as in _as_from_clique.peers) and _as != _as_from_clique):
            print("AS:", str(_as.number), "NOT IN AS:", _as_from_clique.number)
            connected = False
        print("AS:", str(_as.number), "IS IN AS:", str(_as_from_clique.number))
    return connected


def proj2_c(as_list):
    for _as in as_list:
        print(_as.number, "and its degree ", _as.glob)
    as_list_sorted = sorted(as_list, key=lambda x: x.glob, reverse=True)  # sorted list (R)
    for _as in as_list_sorted:
        print(_as.number, "and its degree ", _as.glob)

    # clique portion
    as_list_sorted = as_list_sorted[:50]
    clique = [as_list_sorted.pop(0)] # clique as with highest global degree
    print("Clique length: ", str(len(clique)))
    index = 0
    for _as in as_list_sorted:
        if connected(clique, _as):  # check if any sort of connection in the clique
            clique.append(as_list_sorted.pop(index))  # connect to the clique if so
        index += 1
    # now we need to get the information of who belongs to what so we can build a table in google docs
    print("This is the length of the clique", str(len(clique)))
    tuple_list = []
    print("##############################Finding Pairs############################")
    for _as in clique:  # traverse through the cliques
        print("###############################AS NUMBER", str(_as.number), "############################")
        file = open("identifier.txt")
        for line in file:  # try to find the match in the files
            line = line.split('|')
            if str(_as.number) == line[0]:
                tuple_list.append((str(_as.number), line[3]))
        file.close()
        print(tuple_list)

    print("##################################Organization Mapping##############################################")
    for pair in tuple_list:
        file = open("oridtoname.txt", encoding="utf8")
        for line in file:
            line = line.split('|')
            # if we find the organization id in the file
            if pair[1] == line[0]:  # found organization id
                print("AS Number", pair[0], "belongs to", line[2])
        file.close()

#####################################
def get_data():
    # splitting the pickle file into a bunch of different files because the size of the one file is too large to be handled
    as_list = section_2b("20211001.as-rel2.txt")
    as_list_split = np.array_split(as_list, 5)
    try:
        with open('as_list_1.pkl', 'wb') as outp:
            pickle.dump(as_list_split[0], outp, pickle.HIGHEST_PROTOCOL)
        with open('as_list_2.pkl', 'wb') as outp:
            pickle.dump(as_list_split[1], outp, pickle.HIGHEST_PROTOCOL)
        with open('as_list_3.pkl', 'wb') as outp:
            pickle.dump(as_list_split[2], outp, pickle.HIGHEST_PROTOCOL)
        with open('as_list_4.pkl', 'wb') as outp:
            pickle.dump(as_list_split[3], outp, pickle.HIGHEST_PROTOCOL)
        with open('as_list_5.pkl', 'wb') as outp:
            pickle.dump(as_list_split[4], outp, pickle.HIGHEST_PROTOCOL)
        del as_list
    except MemoryError:
        print("AS List size: ", sys.getsizeof(as_list_split))
        i = 0
        for as_sub_list in as_list_split:
            print("AS sub list number ", str(i), "has a size of", sys.getsizeof(as_sub_list), "MB")
            i += 1


def load_data():
    x = []
    print(len(x))
    with open('as_list_1.pkl', 'rb') as inp:
        while True:
            try:
                x += list(pickle.load(inp))
            except EOFError:
                break
        inp.close()
        print(len(x))
    with open('as_list_2.pkl', 'rb') as inp:
        while True:
            try:
                x += list(pickle.load(inp))
            except EOFError:
                break
        inp.close()
        print(len(x))
    with open('as_list_3.pkl', 'rb') as inp:
        while True:
            try:
                x += list(pickle.load(inp))
            except EOFError:
                break
        inp.close()
        print(len(x))
    with open('as_list_4.pkl', 'rb') as inp:
        while True:
            try:
                x += list(pickle.load(inp))
            except EOFError:
                break
        inp.close()
        print(len(x))
    with open('as_list_5.pkl', 'rb') as inp:
        while True:
            try:
                x += list(pickle.load(inp))
            except EOFError:
                break
        inp.close()
        print(len(x))
    return x


def run():
    start_time = time.time()
    sys.setrecursionlimit(1000000)
    as_list = section_2b("20211001.as-rel2.txt")
    # choice = input(
    #     "Do you want to collect data or view the graphs of previously collected data? (y for collect data/n for view graphs)")
    # if choice.strip() == 'y':
    #     get_data()
    #     print("Data has been retrieved")
    # elif choice.strip() == 'n':
    #     as_list = load_data()
    #     print("Data has been loaded")
    #     print("Number of AS's:", str(len(as_list)))
    #     print(as_list[0].number)
    #     print(as_list[len(as_list) - 1].number)

    as_classification()
    list_obj = section_2b("testfor2b.txt")
    histogram(as_list, "Global Node Degree", 'Global')
    histogram(as_list, "Customer Degree", 'Customer')
    histogram(as_list, "Peer Degree", 'Peer')
    histogram(as_list, "Provider Degree", 'Provider')
    piechart_2(list_obj, 'Percentage Distribution of Autonomous System Classes in 2021 According to Link Traversal')
    parse_prefix_file('prefixtest.txt', as_list)
    prefix_histogram(as_list, "test")
    proj2_c(as_list)
    print("--- %s seconds ---" % (time.time() - start_time))


run()
