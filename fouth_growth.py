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


FOURTH_GO_FOR_IT = [cols.PlayType.PASS, cols.PlayType.RUN]


def fourth(df: pandas.DataFrame) -> pandas.DataFrame:
    df = df[df[cols.Down.header] == 4]
    df["went_for_it"] = df[cols.PlayType.header].isin(FOURTH_GO_FOR_IT)
    df = df[[cols.Season.header, "went_for_it"]]
    df = df.groupby(by=[cols.Season.header]).mean()
    return df


def plot_data(df: pandas.DataFrame):
    seaborn.barplot(df, x=cols.Season.header, y="went_for_it", errorbar=None)
    plt.title("Probability of Going for it by Year")
    plt.xlabel("Year")
    plt.ylabel("Probability")
    plt.xticks(rotation=45)
    plt.savefig("figs/forth_growth", bbox_inches="tight", dpi=300)
    plt.show()


df = pbp.get(YEARS, CACHE)
df = fourth(df)
print(df.head())
plot_data(df)
