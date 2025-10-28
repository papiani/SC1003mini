import matplotlib.pyplot as plt

def time_linegraph(data):
    x_values =[]
    y_values =[]
    for x,y in data:
        x_values.append(x)
        y_values.append(y)

    # Create the line chart
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='blue')

    # Add labels and title
    plt.xlabel('Run-cycles or "Epochs"')
    plt.ylabel('Diversity Score')
    plt.title('Diversity over runtime')

    # Show the chart
    plt.grid(True)
    plt.tight_layout()
    plt.show()
