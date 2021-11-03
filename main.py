# Lewis Koplon
# Professor Lazos
# ECE 578
# The Internet Topology
import matplotlib.pyplot as plot


# Section 2.1 AS Classification
def parse_file(file_name):
    as_types_count = [0, 0,
                      0]  # [transit/access, content, enterprise] we should see three different types of Autonomous Systems, in this such order
    file = open(file_name)
    as_counter = 0
    for line in file:
        if (line.startswith('#')):
            continue
        else:
            line = line.strip()
            split_line = line.split('|')
            if split_line[2].lower() == "transit/access":
                as_types_count[0] += 1
            elif split_line[2].lower() == "content":
                as_types_count[1] += 1
            elif split_line[2].lower() in ["enterprise", "enterpise"]:
                as_types_count[2] += 1
            as_counter += 1

    return as_types_count, as_counter


def pie_chart(amount):
    labels = "transit/access", "content", "enterprise"
    explode = (0, 0, 0)
    figure1, ax1 = plot.subplots()  # creating the figure
    ax1.pie(amount, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plot.show()  # showing the figure

def bar_graph(amount, total):
    labels = "transit/access", "content", "enterprise"
    percentages = [number/total for number in amount]
    figure1 = plot.figure()
    ax1 = figure1.subplots  # creating the figure
    plot.bar(labels, percentages)
    plot.ylabel('Percentage')
    plot.title('Percentage Distribution of Autonomous System Classes')

    plot.show()  # showing the figure

def as_classification():
    as_types_2021, as_count_2021 = parse_file("20210401.as2types.txt")
    as_types_2015, as_count_2015 = parse_file("20150801.as2types.txt")
    print("April 2021 as classes [transit/access, content, enterprise]:", as_types_2021, "total AS count",
          as_count_2021)
    pie_chart(as_types_2021)
    print("August 2015 as classes [transit/access, content, enterprise]:", as_types_2015, "total AS count",
          as_count_2015)
    bar_graph(as_types_2015, as_count_2015)


as_classification()
