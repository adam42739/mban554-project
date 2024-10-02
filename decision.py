import fg_ep
import punt_ep
import fourth_ep
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy
from matplotlib.patches import Patch


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(numpy.linspace(minval, maxval, n)),
    )
    return new_cmap


def formatter_x(label):
    label = int(float(label))
    if (label + 1) % 10 == 0:
        return f"{int(label + 1)}"
    else:
        return ""


def formatter_y(label):
    label = int(float(label))
    if (label + 1) % 5 == 0:
        return f"{int(label + 1)}"
    else:
        return ""


def plot_data(data: numpy.ndarray):
    _colors = ["lightblue", "darkblue", "darkcyan", "white"]
    cmap = colors.ListedColormap(_colors)
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)
    ax.set_aspect("auto")
    labels = ["Field Goal", "Punt", "Go For It",]
    handles = [Patch(color=_colors[i], label=labels[i]) for i in range(len(labels))]
    ax.legend(handles=handles, bbox_to_anchor=(0.7, 1))
    ax.grid(which="major", axis="both", linestyle="-", color="k", linewidth=0)
    ax.set_xticks(numpy.arange(1, 99, 1))
    ax.set_xticklabels(
        [formatter_x(label.get_text()) for label in ax.get_xticklabels()]
    )
    ax.set_yticks(numpy.arange(1, 15, 1))
    ax.set_yticklabels(
        [formatter_y(label.get_text()) for label in ax.get_yticklabels()]
    )
    plt.title("4th Down Decision")
    plt.xlabel("Yards to Goalline")
    plt.ylabel("Yards to 1st Down")
    plt.savefig("figs/decision")
    plt.show()


def get_data() -> numpy.ndarray:
    fg = fg_ep.create_data()
    punt = punt_ep.create_data()
    fourth = fourth_ep.create_data()
    data = numpy.random.rand(15, 98)
    for i in range(0, 15):
        for j in range(0, 98):
            if i > j:
                data[i][j] = 3
            elif fg[i][j] > punt[i][j] and fg[i][j] > fourth[i][j]:
                data[i][j] = 0
            elif punt[i][j] > fg[i][j] and punt[i][j] > fourth[i][j]:
                data[i][j] = 1
            else:
                data[i][j] = 2
    return data


data = get_data()
plot_data(data)
