import os
import matplotlib.pyplot as plt
from fastf1 import plotting


def generate_driver_styling_image(session, driver_abbr: str) -> str:
    """
    Generate a plot showing the driver's lap times, colored by tire compound.

    :param session: A FastF1 session object.
    :param driver_abbr: The abbreviation of the driver.
    :return: Path to the saved image.
    """
    # Retrieve laps data for the specified driver
    driver_laps = session.laps.pick_driver(driver_abbr).pick_quicklaps()
    if driver_laps.empty:
        print(f"⚠ No lap data available for driver {driver_abbr}.")
        return None

    # Convert lap times to seconds for plotting
    driver_laps['LapTimeSeconds'] = driver_laps['LapTime'].dt.total_seconds()

    # Ensure plotting uses FastF1's color scheme
    plotting.setup_mpl(misc_mpl_mods=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    compounds = driver_laps['Compound'].unique()
    for compound in compounds:
        compound_laps = driver_laps[driver_laps['Compound'] == compound]
        ax.plot(compound_laps['LapNumber'], compound_laps['LapTimeSeconds'],
                marker='o', linestyle='-', label=compound,
                color=plotting.COMPOUND_COLORS.get(compound, '#000000'))

    # Legend
    ax.legend(title="Compound")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    plt.tight_layout()

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/driver_styling_{year}_{gp}_{type}.png"

    # Close
    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
    plt.close(fig)
    return filename
