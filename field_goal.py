import nfldpw.pbp as pbp
import nfldpw.pbp.cols as cols
import matplotlib.pyplot as plt
import seaborn
import pandas


CACHE = "cache/"


def field_goals(df: pandas.DataFrame) -> pandas.DataFrame:
    fgs = df[cols.PlayType.header] == cols.PlayType.FIELD_GOAL
    df = df[fgs]
    df["fg_made"] = df[cols.FieldGoalResult.header] == cols.FieldGoalResult.MADE
    df = df[[cols.Yardline100.header, "fg_made"]]
    return df


def plot_data(df: pandas.DataFrame):
    seaborn.barplot(df, x=cols.Yardline100.header, y="fg_made", errorbar=None)
    plt.title("Field Goal Probability by Yards")
    plt.xlabel("Yards to Goal")
    plt.ylabel("Field Goal Probability")
    plt.xticks(ticks=range(0, 100, 10), labels=range(0, 100, 10))
    plt.xlim(0, 50)
    plt.savefig("figs/field_goal")
    plt.show()


df = pbp.get([2021, 2022, 2023], CACHE)
df = field_goals(df)
plot_data(df)
