import os
import matplotlib.pyplot as plt
import seaborn as sns
from fastf1 import plotting


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

    fig, ax = plt.subplots()
    for drv in laps['Driver'].unique()[:count]:
        lap = laps.pick_drivers(drv).pick_fastest()
        tel = lap.get_car_data().add_distance()
        ax.plot(tel['Distance'], tel['Speed'], label=drv)

    # Legend
    ax.legend()
    ax.set_title(f"🏁 Top {count} Fastest Laps")
    ax.set_xlabel("Distance, meters")
    ax.set_ylabel("Speed, km/h")

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/best_laps_{year}_{gp}_{type}.png"

    # Close
    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
    plt.close(fig)
    return filename


def generate_laptime_distribution_image(session) -> str:
    """
    Generate a violin plot showing the distribution of lap times for each driver.

    :param session: A FastF1 session object.?
    :return: Path to the saved image.
    """
    laps = session.laps.pick_quicklaps()
    if laps.empty:
        print("⚠ No fast laps available in this session.")
        return None

    # Convert lap times to seconds for plotting
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    # Ensure plotting uses FastF1's color scheme
    plotting.setup_mpl(misc_mpl_mods=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=laps, x='Driver', y='LapTimeSeconds', ax=ax, inner='quartile', scale='width')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Legend
    ax.legend()
    ax.set_title("🏁 Lap Time Distribution")
    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time, seconds")

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/laptime_distribution_{year}_{gp}_{type}.png"

    # Close
    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
    plt.close(fig)
    return filename
