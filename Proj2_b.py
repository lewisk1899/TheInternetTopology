# Lewis Koplon/Ramon Driesen
# Professor Lazos
# ECE 578
# The Internet Topology
import matplotlib.pyplot as plot

class AS:
    def __init__(self, number):
        self.number = number
        self.p2p = 0
        self.p2c = 0
        self.glob = 0

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


def inc_degree(as_i, classification):
    if (classification == '0'):
        as_i.p2p += 1
        as_i.glob += 1
    else: 
        as_i.p2c += 1
        as_i.glob += 1

# Section 2.2 Topology Inference Through AS Links
def section_2b(filename):
    list_as = []
    list_as_objects = []
    file = open(filename)
    for line in file:
        if not line.startswith('#'):
            line = line.strip()
            split_line = line.split("|")
            # we havent found this as in the list
            if split_line[0] not in list_as:
                list_as.append(split_line[0])
                temp_as1 = AS(split_line[0])
                list_as_objects.append(temp_as1)
                inc_degree(temp_as1, split_line[2])
            else:
                # find the as in our object list
                for AutoSys1 in list_as_objects:
                    if AutoSys1.number == split_line[0]:
                        temp_as1 = AutoSys1
                        inc_degree(temp_as1, split_line[2])
            # we havent found this as in the list
            if split_line[1] not in list_as:
                list_as.append(split_line[1])
                temp_as2 = AS(split_line[1])
                list_as_objects.append(temp_as2)
                inc_degree(temp_as2, split_line[2])
            else:
                #find the as
                for AutoSys2 in list_as_objects:
                    if AutoSys2.number == split_line[1]:
                        temp_as2 = AutoSys2
                        inc_degree(temp_as2, split_line[2])

    return list_as_objects

def main():
    #test
    list_obj = section_2b("testfor2b.txt")
    for x in list_obj:
        print('AS: ', x.number, ' p2p connections: ', x.p2p)

if __name__ == "__main__":
    main()