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


def first_drive(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Get only plays that occur on 1st and 10 OR 1st and goal where the yards to the goaline is less than 10.
    """
    first_down = df[cols.Down.header] == 1
    yards10 = df[cols.Ydstogo.header] == 10
    and_goal = df[cols.Yardline100.header] == df[cols.Ydstogo.header]
    yardsless10 = df[cols.Yardline100.header] <= 10
    df = df[first_down & (yards10 | (and_goal & yardsless10))]
    df = df[
        [
            cols.Yardline100.header,
            cols.FixedDriveResult.header,
        ]
    ]
    return df


def compute_drive_points(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Compute the points scored on the given drive.

    ```
    = 7 * (FixedDriveResult == TOUCHDOWN)
    + 3 * (FixedDriveResult == FIELD_GOAL)
    - 2 * (FixedDriveResult == SAFETY)
    - 7 * (FixedDriveResult == OPP_TOUCHDOWN)
    ```

    """
    df["drive_points"] = (
        7 * (df[cols.FixedDriveResult.header] == cols.FixedDriveResult.TOUCHDOWN)
        + 3 * (df[cols.FixedDriveResult.header] == cols.FixedDriveResult.FIELD_GOAL)
        - 2 * (df[cols.FixedDriveResult.header] == cols.FixedDriveResult.SAFETY)
        - 7 * (df[cols.FixedDriveResult.header] == cols.FixedDriveResult.OPP_TOUCHDOWN)
    )
    return df[[cols.Yardline100.header, "drive_points"]]


def formatter(label):
    label = int(float(label))
    if label % 10 == 0:
        return f"{int(label)}"
    else:
        return ""


def plot_data(df: pandas.DataFrame):
    ax = seaborn.barplot(df, x=cols.Yardline100.header, y="drive_points", errorbar=None)
    plt.title("Expected Drive Points by Starting Field Position")
    plt.xlabel("Yards to Goal")
    plt.ylabel("Expected Points")
    ax.set_xticklabels([formatter(label.get_text()) for label in ax.get_xticklabels()])
    plt.savefig("figs/points_by_field_position")
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
    with open(SAVES + "field_position.json", "w") as file:
        json.dump(gb_dict, file)


df = pbp.get(YEARS, CACHE)
df = first_drive(df)
df = compute_drive_points(df)
save_data(df)
plot_data(df)
