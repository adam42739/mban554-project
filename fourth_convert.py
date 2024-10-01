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


FOURTH_GO_FOR_IT = [cols.PlayType.PASS, cols.PlayType.RUN]


def fourth_down(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Get only the plays where a team went for it on 4th down.
    """
    fourth = df[cols.Down.header] == 4
    go_for_it = df[cols.PlayType.header].isin(FOURTH_GO_FOR_IT)
    df = df[fourth & go_for_it]
    df = df[[cols.Ydstogo.header, cols.FirstDown.header]]
    return df


def fourth_agg_ten(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Aggregate all 4th and 15 or greater to the same bucket.
    """
    df[cols.Ydstogo.header] = (df[cols.Ydstogo.header] < 15) * df[
        cols.Ydstogo.header
    ] + (df[cols.Ydstogo.header] >= 15) * 15
    return df


def formatter(x, tick):
    if x == 14:
        return "15+"
    else:
        return f"{int(x+1)}"


def plot_data(df: pandas.DataFrame):
    seaborn.barplot(df, x=cols.Ydstogo.header, y=cols.FirstDown.header, errorbar=None)
    plt.title("Probability of a 4th Down Conversion")
    plt.xlabel("Yards to go")
    plt.ylabel("Conversion Probability")
    plt.xlim(-0.8, 14.8)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))
    plt.savefig("figs/fourth_convert")
    plt.show()


df = pbp.get(YEARS, CACHE)
df = fourth_down(df)
df = fourth_agg_ten(df)
plot_data(df)
