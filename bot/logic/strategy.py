import os
import matplotlib.pyplot as plt
from fastf1 import plotting


def generate_strategy_image(session) -> str:
    """
    Generate a horizontal bar chart showing each driver's tire stints during the race.

    :param session: A FastF1 session object.
    :return: Path to the saved image.
    """
    # Retrieve laps data
    stints = session.laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})

    drivers = session.drivers
    drivers = list(dict.fromkeys(drivers))

    # Ensure plotting uses FastF1's color scheme
    plotting.setup_mpl(misc_mpl_mods=False)
    fig, ax = plt.subplots(figsize=(10, len(drivers) * 0.5))
    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]
        previous_stint_end = 0
        for _, row in driver_stints.iterrows():
            stint_color = plotting.COMPOUND_COLORS.get(row["Compound"], "#000000")
            ax.barh(driver, row["StintLength"], left=previous_stint_end, color=stint_color, edgecolor="black")
            previous_stint_end += row["StintLength"]

    # Legend
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=color) for color in plotting.COMPOUND_COLORS.values()],
              labels=plotting.COMPOUND_COLORS.keys(),
              title="Compound",
              bbox_to_anchor=(1.05, 1),
              loc='upper left')
    ax.invert_yaxis()
    ax.set_xlabel("Lap")
    ax.set_ylabel("Driver")
    plt.tight_layout()

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/strategy_{year}_{gp}_{type}.png"

    # Close
    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
    plt.close(fig)
    return filename
