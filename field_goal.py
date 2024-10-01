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


def field_goals(df: pandas.DataFrame) -> pandas.DataFrame:
    fgs = df[cols.PlayType.header] == cols.PlayType.FIELD_GOAL
    df["fg_made"] = df[cols.FieldGoalResult.header] == cols.FieldGoalResult.MADE
    df = df[fgs]
    df = df[[cols.Yardline100.header, "fg_made"]]
    return df


def formatter(x, tick):
    if x % 10 == 9 or x == 0:
        return f"{int(x+1)}"
    else:
        return ""


def plot_data(df: pandas.DataFrame):
    seaborn.barplot(df, x=cols.Yardline100.header, y="fg_made", errorbar=None)
    plt.title("Field Goal Probability by Yards")
    plt.xlabel("Yards to Goal")
    plt.ylabel("Field Goal Probability")
    plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))
    plt.savefig("figs/field_goal")
    plt.show()


df = pbp.get(YEARS, CACHE)
df = field_goals(df)
plot_data(df)
