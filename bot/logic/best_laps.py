import matplotlib.pyplot as plt


def generate_best_laps_image(session):
    laps = session.laps.pick_quicklaps().sort_values(by='LapTime')
    fig, ax = plt.subplots()
    for drv in laps['Driver'].unique()[:5]:
        lap = laps.pick_driver(drv).pick_fastest()
        tel = lap.get_car_data().add_distance()
        ax.plot(tel['Distance'], tel['Speed'], label=drv)
    ax.legend()
    ax.set_title("5 быстрейших")
    ax.set_xlabel("Дистанция, метры")
    ax.set_ylabel("Скорость, км/ч")
    path = "data/best_laps.png"
    fig.savefig(path)
    return path


def print_best_laps(session):
    laps = session.laps.pick_quicklaps()
    print(laps.sort_values(by='LapTime')[['Driver', 'LapTime']].head())
