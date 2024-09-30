import nfldpw.pbp as pbp
import matplotlib.pyplot as plt
import seaborn
import pandas


def expected_drive_points(plays: pandas.DataFrame):
    f10 = plays[
        (plays[pbp.cols.Down.header] == 1)
        & (
            (plays[pbp.cols.Ydstogo.header] == 10)
            | (
                (plays[pbp.cols.Yardline100.header] == plays[pbp.cols.Ydstogo.header])
                & (plays[pbp.cols.Yardline100.header] <= 10)
            )
        )
    ]
    f10 = f10[
        [
            pbp.cols.Yardline100.header,
            pbp.cols.FixedDriveResult.header,
        ]
    ]
    f10["drive_points"] = (
        7
        * (f10[pbp.cols.FixedDriveResult.header] == pbp.cols.FixedDriveResult.TOUCHDOWN)
        + 3
        * (
            f10[pbp.cols.FixedDriveResult.header]
            == pbp.cols.FixedDriveResult.FIELD_GOAL
        )
        - 2
        * (f10[pbp.cols.FixedDriveResult.header] == pbp.cols.FixedDriveResult.SAFETY)
        - 7
        * (
            f10[pbp.cols.FixedDriveResult.header]
            == pbp.cols.FixedDriveResult.OPP_TOUCHDOWN
        )
    )
    f10 = f10[[pbp.cols.Yardline100.header, "drive_points"]]

    seaborn.barplot(f10, x=pbp.cols.Yardline100.header, y="drive_points", errorbar=None)
    plt.title("Expected Drive Points by Starting Field Position")
    plt.xlabel("Expected Points")
    plt.ylabel("Points Scored")
    plt.xticks(ticks=range(0, 100, 10), labels=range(0, 100, 10))
    plt.savefig("figs/points_by_field_position")
    plt.show()


CACHE = "cache/"


plays = pbp.get([2021, 2022, 2023], CACHE)
expected_drive_points(plays)
