import nfldpw.pbp as pbp
import nfldpw.pbp.cols as cols
import matplotlib.pyplot as plt
import seaborn
import pandas
from matplotlib.ticker import FuncFormatter


CACHE = "cache/"


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
    Aggregate all 4th and 10 or greater to the same bucket.
    """
    df[cols.Ydstogo.header] = (df[cols.Ydstogo.header] < 13) * df[
        cols.Ydstogo.header
    ] + (df[cols.Ydstogo.header] >= 13) * 13
    return df


def formatter(x, tick):
    if x == 12:
        return "13+"
    else:
        return f"{int(x+1)}"


def plot_data(df: pandas.DataFrame):
    seaborn.barplot(df, x=cols.Ydstogo.header, y=cols.FirstDown.header, errorbar=None)
    plt.title("Probability of a 4th Down Conversion")
    plt.xlabel("Yards to go")
    plt.ylabel("Conversion Probability")
    plt.xlim(-0.8, 12.8)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))
    plt.savefig("figs/fourth_convert")
    plt.show()


df = pbp.get([2021, 2022, 2023], CACHE)
df = fourth_down(df)
df = fourth_agg_ten(df)
plot_data(df)
