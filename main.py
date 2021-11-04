# Lewis Koplon
# Professor Lazos
# ECE 578
# The Internet Topology
import matplotlib.pyplot as plot

class AS:
    def __init__(self, number):
        self.number = number
        self.customers = []
        self.providers = []
        self.peers = []

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


def pie_chart(amount):
    labels = "transit/access", "content", "enterprise"
    explode = (0, 0, 0)
    figure1, ax1 = plot.subplots()  # creating the figure
    ax1.pie(amount, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plot.title('Percentage Distribution of Autonomous System Classes in 2021')
    plot.show()  # showing the figure


def bar_graph(amount, total):
    labels = "transit/access", "content", "enterprise"
    percentages = [number / total for number in amount]
    figure1 = plot.figure()
    ax1 = figure1.subplots  # creating the figure
    plot.bar(labels, percentages)
    plot.ylabel('Percentage')
    plot.title('Percentage Distribution of Autonomous System Classes in 2015')

    plot.show()  # showing the figure


def as_classification():
    as_types_2021, as_count_2021 = parse_file("20210401.as2types.txt")  # parsing the data sets from CAIDA
    as_types_2015, as_count_2015 = parse_file("20150801.as2types.txt")
    # printing findings and using them to create our needed graphs via matplotlib
    print("April 2021 as classes [transit/access, content, enterprise]:", as_types_2021, "total AS count",
          as_count_2021)
    pie_chart(as_types_2021)
    print("August 2015 as classes [transit/access, content, enterprise]:", as_types_2015, "total AS count",
          as_count_2015)
    bar_graph(as_types_2015, as_count_2015)

# Section 2.2 Topology Inference Through AS Links
def parse_file_for_tree(filename):
    file = open(filename)
    AS_list = []
    for line in file:
        if not line.startswith('#'):
            line_split = line.strip().split('|') # p2c link: <provider-AS>|<customer-AS>| -1 |<source> or p2p link: <peer-AS>|<peer-AS>| 0 |<source>
            if line_split[0] not in AS_list:
                # create a new AS object and add it to the list
                temp_AS_1 = AS(line_split[0]) # create a new object
                AS_list.append(line_split[0]) # add to the list
            else:
                # find the autonomous system
            if line_split[2] not in AS_list:
                # create a new AS object and add it to the list
                temp_AS_2 = AS(line_split[2])  # create a new object
                AS_list.append(line_split[2])  # add to the list
            else:
                # find the autonomous system


# Execution Section
#as_classification()
