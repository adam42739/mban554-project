import nfldpw.pbp as pbp
import nfldpw.pbp.cols as cols
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas
import numpy


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
    df = df[[cols.PossessionTeam.header, "went_for_it"]]
    df = df.groupby(by=[cols.PossessionTeam.header]).mean()
    return df


df = pbp.get([2023], CACHE)
df = fourth(df)
df.to_csv("saves/fourth_team.csv")
