import nfldpw.pbp as pbp
import nfldpw.pbp.cols as cols
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn
import pandas
import json
import numpy


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
    new_cmap1 = truncate_colormap(plt.get_cmap("viridis"), 1.0, 0.45)
    fig, ax = plt.subplots()
    plt.imshow(data, aspect="auto", cmap=new_cmap1)
    plt.colorbar()
    ax.grid(which="major", axis="both", linestyle="-", color="k", linewidth=0)
    ax.set_xticks(numpy.arange(1, 99, 1))
    ax.set_xticklabels(
        [formatter_x(label.get_text()) for label in ax.get_xticklabels()]
    )
    ax.set_yticks(numpy.arange(1, 15, 1))
    ax.set_yticklabels(
        [formatter_y(label.get_text()) for label in ax.get_yticklabels()]
    )
    plt.title("Field Goal + Opponent Next Drive Expected Points")
    plt.xlabel("Yards to Goalline")
    plt.ylabel("Yards to 1st Down")
    plt.savefig("figs/fg_ep")
    plt.show()


def ep_senario(fg_prob: dict, posit_ep: dict, yardline: int, ydstogo: int) -> float:
    key = str(yardline) + ".0"
    opp_key = str(100 - yardline) + ".0"
    if key in fg_prob:
        return 3 * fg_prob[key] - posit_ep[opp_key] * (1 - fg_prob[key])
    else:
        return -posit_ep[opp_key]


def load_data_fg() -> dict:
    gb_dict = {}
    with open("saves/field_goal.json", "r") as file:
        gb_dict = json.load(file)
    return gb_dict


def load_data_field_pos() -> dict:
    gb_dict = {}
    with open("saves/field_position.json", "r") as file:
        gb_dict = json.load(file)
    return gb_dict


def create_data() -> numpy.ndarray:
    fg_prob = load_data_fg()
    posit_ep = load_data_field_pos()
    data = numpy.random.rand(15, 98)
    for togo in range(0, 15):
        for ydline in range(0, 98):
            data[togo][ydline] = ep_senario(fg_prob, posit_ep, ydline + 1, togo + 1)
    return data


data = create_data()
plot_data(data)
