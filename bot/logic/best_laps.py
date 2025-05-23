import os
import matplotlib.pyplot as plt


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
        raise ValueError("No lap data available")

    fig, ax = plt.subplots()
    for drv in laps['Driver'].unique()[:count]:
        lap = laps.pick_drivers(drv).pick_fastest()
        tel = lap.get_car_data().add_distance()
        ax.plot(tel['Distance'], tel['Speed'], label=drv)

    ax.legend()
    ax.set_title(f"Top {count} Fastest Laps")
    ax.set_xlabel("Distance, meters")
    ax.set_ylabel("Speed, km/h")

    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    stype = session.name.replace(' ', '_')
    path = f"data/best_laps_{year}_{gp}_{stype}.png"

    os.makedirs("data", exist_ok=True)
    fig.savefig(path)
    return path
