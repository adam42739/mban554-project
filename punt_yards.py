import nfldpw.pbp as pbp
import nfldpw.pbp.cols as cols
import matplotlib.pyplot as plt
import seaborn
import pandas
from matplotlib.ticker import FuncFormatter


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


df = pbp.get(YEARS, CACHE)
df = punts(df)
plot_data(df)
