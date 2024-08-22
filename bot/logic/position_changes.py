import os
import matplotlib.pyplot as plt
from fastf1 import plotting
from fastf1.plotting import get_driver_color


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

    drivers = laps['Driver'].unique()

    plt.style.use('dark_background')
    plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')
    fig, ax = plt.subplots(figsize=(14, 7))

    for driver in drivers:
        try:
            drv_laps = laps.pick_drivers(driver)
            if drv_laps.empty:
                continue
            color = get_driver_color(driver, session)
            ax.plot(
                drv_laps['LapNumber'], drv_laps['Position'],
                label=driver, color=color, linewidth=2
            )
        except Exception as e:
            print(f"Skipped driver {driver} due to error: {e}")
            continue

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14, framealpha=0.8)
    ax.invert_yaxis()
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks(range(1, 21))
    ax.set_xlabel('Lap', fontsize=16)
    ax.set_ylabel('Position', fontsize=16)
    ax.set_title("Position Changes During Race", fontsize=20, pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/position_changes_{year}_{gp}_{type}.png"

    os.makedirs("data", exist_ok=True)
    fig.savefig(filename, bbox_inches='tight', dpi=180)
    plt.close(fig)
    return filename
