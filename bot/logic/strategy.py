import os
import matplotlib.pyplot as plt
from fastf1 import plotting
from fastf1.plotting import get_compound_color


def generate_strategy_image(session) -> str:
    """
    Generate a horizontal bar chart showing each driver's tire stints during the race.

    :param session: A FastF1 session object.
    :return: Path to the saved image.
    """
    plt.style.use('dark_background')
    plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

    stints = session.laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stint_info = stints.groupby(["Driver", "Stint", "Compound"])['LapNumber'].agg(['min', 'max', 'count']).reset_index()
    stint_info = stint_info.rename(columns={'count': 'StintLength', 'min': 'StartLap', 'max': 'EndLap'})
    drivers = stint_info["Driver"].unique()

    fig, ax = plt.subplots(figsize=(14, len(drivers) * 0.6 + 2))
    for i, drv in enumerate(drivers):
        stints = stint_info[stint_info["Driver"] == drv]
        label = drv
        for _, stint in stints.iterrows():
            color = get_compound_color(stint["Compound"], session)
            ax.barh(
                label,
                stint["StintLength"],
                left=stint["StartLap"],
                color=color,
                edgecolor="#333",
                height=0.7,
                align='center'
            )
            ax.text(
                stint["StartLap"] + stint["StintLength"] / 2,
                i,
                stint["Compound"][0],
                color='white',
                fontsize=10,
                ha='center',
                va='center',
                alpha=0.7
            )

    compounds = stint_info["Compound"].unique()
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=get_compound_color(comp, session), label=comp)
        for comp in compounds
    ]
    ax.legend(handles=legend_handles, title="Compound", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=12)

    ax.invert_yaxis()
    ax.set_xlabel("Lap", fontsize=16)
    ax.set_ylabel("Driver", fontsize=16)
    ax.set_title("Tire Strategy by Driver", fontsize=20, pad=15)
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()

    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/strategy_{year}_{gp}_{type}.png"

    os.makedirs("data", exist_ok=True)
    fig.savefig(filename, bbox_inches='tight', dpi=180)
    plt.close(fig)
    return filename
