import os
import matplotlib.pyplot as plt
from fastf1 import plotting


def generate_position_changes_image(session) -> str:
    """
    Generate a plot showing position changes for each driver during the race.

    :param session: A FastF1 session object.
    :return: Path to the saved image.
    """
    laps = session.laps
    if laps.empty:
        print("⚠ No laps available in this session.")
        return None

    # Get list of unique drivers
    drivers = laps['Driver'].unique()

    # Ensure plotting uses FastF1's color scheme
    plotting.setup_mpl(misc_mpl_mods=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    for driver in drivers:
        drv_laps = laps.pick_driver(driver)
        if drv_laps.empty:
            continue
        color = plotting.driver_color(driver)
        ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=driver, color=color)

    # Legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.invert_yaxis()
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks(range(1, 21))
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    plt.tight_layout()

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/position_changes_{year}_{gp}_{type}.png"

    # Close
    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
    plt.close(fig)
    return filename
