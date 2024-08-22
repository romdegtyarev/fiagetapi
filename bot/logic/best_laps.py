import os
import matplotlib.pyplot as plt
import seaborn as sns
from fastf1 import plotting
from fastf1.plotting import get_driver_color


def print_best_laps(session, count: int = 5):
    """
    Print the top fastest laps from the session.

    :param session: A FastF1 session object.
    :param count: Number of top laps to display.
    """
    laps = session.laps.pick_quicklaps()
    if laps.empty:
        print("⚠ No fast laps available in this session.")
        return

    print(f"\n🏁 Top {count} Fastest Laps:\n")
    print(laps.sort_values(by='LapTime')[['Driver', 'LapTime']].head(count))


def generate_best_laps_image(session, count: int = 5) -> str:
    """
    Generate a speed-over-distance chart for the top fastest laps.

    :param session: A FastF1 session object.
    :param count: Number of unique drivers to display.
    :return: Path to the saved image.
    """
    laps = session.laps.pick_quicklaps().sort_values(by='LapTime')
    if laps.empty:
        print("⚠ No fast laps available in this session.")
        return None

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 7))
    for drv in laps['Driver'].unique()[:count]:
        lap = laps.pick_drivers(drv).pick_fastest()
        tel = lap.get_car_data().add_distance()
        color = get_driver_color(drv, session)
        ax.plot(tel['Distance'], tel['Speed'], label=drv, linewidth=2, color=color)

    # Legend
    ax.legend(fontsize=14, framealpha=0.8, facecolor="#222", edgecolor="#444")
    ax.set_title(f"Top {count} Fastest Laps", fontsize=20, pad=15)
    ax.set_xlabel("Distance, meters", fontsize=16)
    ax.set_ylabel("Speed, km/h", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/best_laps_{year}_{gp}_{type}.png"

    os.makedirs("data", exist_ok=True)
    fig.savefig(filename, bbox_inches='tight', dpi=180)
    plt.close(fig)
    return filename


def generate_laptime_distribution_image(session) -> str:
    """
    Generate a violin plot showing the distribution of lap times for each driver.

    :param session: A FastF1 session object.
    :return: Path to the saved image.
    """
    laps = session.laps.pick_quicklaps()
    if laps.empty:
        print("⚠ No fast laps available in this session.")
        return None

    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    plt.style.use('dark_background')
    plotting.setup_mpl(misc_mpl_mods=False)
    driver_codes = sorted(laps['Driver'].unique())
    palette = {drv: get_driver_color(drv, session) for drv in driver_codes}
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.violinplot(
        data=laps,
        x='Driver', y='LapTimeSeconds', ax=ax,
        inner='quartile', scale='width', linewidth=2,
        palette=palette, order=driver_codes
    )
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    ax.set_title("Lap Time Distribution", fontsize=20, pad=15)
    ax.set_xlabel("Driver", fontsize=16)
    ax.set_ylabel("Lap Time, seconds", fontsize=16)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/laptime_distribution_{year}_{gp}_{type}.png"

    os.makedirs("data", exist_ok=True)
    fig.savefig(filename, bbox_inches='tight', dpi=180)
    plt.close(fig)
    return filename
