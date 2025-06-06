import matplotlib.pyplot as plt
from fastf1 import plotting
from fastf1.plotting import get_compound_color
from logic.utils import make_data_filename


def generate_driver_styling_image(session, driver_abbr: str) -> str:
    """
    Generate a plot showing the driver's lap times, colored by tire compound.

    :param session: A FastF1 session object.
    :param driver_abbr: The abbreviation of the driver.
    :return: Path to the saved image.
    """
    plt.style.use('dark_background')
    plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

    driver_laps = session.laps.pick_drivers(driver_abbr).pick_quicklaps().copy()
    if driver_laps.empty:
        print(f"⚠ No lap data available for driver {driver_abbr}.")
        return None
    driver_laps['LapTimeSeconds'] = driver_laps['LapTime'].dt.total_seconds()
    compounds = driver_laps['Compound'].unique()
    fig, ax = plt.subplots(figsize=(14, 8))
    for compound in compounds:
        laps = driver_laps[driver_laps['Compound'] == compound].sort_values('LapNumber')
        groups = (laps['LapNumber'].diff() != 1).cumsum()
        for _, seg in laps.groupby(groups):
            if len(seg) < 2:
                ax.scatter(seg['LapNumber'], seg['LapTimeSeconds'],
                           color=get_compound_color(compound, session),
                           edgecolor='black', linewidth=0.8, s=38, zorder=3)
            else:
                ax.plot(seg['LapNumber'], seg['LapTimeSeconds'],
                        marker='o', linestyle='-',
                        color=get_compound_color(compound, session),
                        label=compound if seg.index[0] == laps.index[0] else "",
                        zorder=2)
                ax.scatter(seg['LapNumber'], seg['LapTimeSeconds'],
                           color=get_compound_color(compound, session),
                           edgecolor='black', linewidth=0.8, s=38, zorder=3)

    handles, labels = ax.get_legend_handles_labels()
    new_labels, new_handles = [], []
    for h, l in zip(handles, labels):
        if l not in new_labels:
            new_labels.append(l)
            new_handles.append(h)
    ax.legend(new_handles, new_labels, title="Compound", fontsize=14, title_fontsize=14)
    ax.set_xlabel("Lap Number", fontsize=16)
    ax.set_ylabel("Lap Time (s)", fontsize=16)
    ax.set_title(f"{driver_abbr} Lap Times by Compound", fontsize=20, pad=15)
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    filename = make_data_filename("driver_styling", session)
    fig.savefig(filename, bbox_inches='tight', dpi=180)
    plt.close(fig)
    return filename
