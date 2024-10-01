import nfldpw.pbp as pbp
import nfldpw.pbp.cols as cols
import matplotlib.pyplot as plt
import seaborn
import pandas
import json


CACHE = "cache/"
YEARS = [
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
]


def punts(df: pandas.DataFrame) -> pandas.DataFrame:
    punt_play = df[cols.PlayType.header] == cols.PlayType.PUNT
    df = df[punt_play]
    df = df[[cols.Yardline100.header, cols.KickDistance.header]]
    return df


def formatter(label):
    label = int(float(label))
    if label % 10 == 0:
        return f"{int(label)}"
    else:
        return ""


def plot_data(df: pandas.DataFrame):
    ax = seaborn.barplot(
        df, x=cols.Yardline100.header, y=cols.KickDistance.header, errorbar=None
    )
    plt.title("Punt Distance by Yard Line")
    plt.xlabel("Yards to Goal")
    plt.ylabel("Punt Distance")
    ax.set_xticklabels([formatter(label.get_text()) for label in ax.get_xticklabels()])
    plt.savefig("figs/punt_yards")
    plt.show()


SAVES = "saves/"


def save_data(df: pandas.DataFrame):
    """
    Save the group by data in JSON format in the SAVES directory.
    """
    gb = df.groupby(by=[cols.Yardline100.header]).mean()
    gb_dict = {}
    for key in gb.index.values:
        gb_dict[key] = float(gb[gb.index == key].values[0][0])
    with open(SAVES + "punt_yards.json", "w") as file:
        json.dump(gb_dict, file)


df = pbp.get(YEARS, CACHE)
df = punts(df)
save_data(df)
plot_data(df)
