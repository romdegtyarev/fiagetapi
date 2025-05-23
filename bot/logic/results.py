import os
import matplotlib.pyplot as plt


def print_results(session):
    """
    Print the session result standings.

    :param session: A FastF1 session object.
    """
    results = session.results
    if results.empty:
        print("⚠ No session results available.")
        return

    print(f"\n🏁 {session.event['EventName']} — Session Results:\n")
    for _, row in results.iterrows():
        print(f"{row['Position']:>2}. {row['FullName']:<20} "
              f"({row['TeamName']}) — Grid: {row['GridPosition']}, "
              f"Points: {row['Points']}, Status: {row['Status']}")


def generate_results_image(session) -> str:
    """
    Generate an image of the session results in table format.

    :param session: A FastF1 session object.
    :return: str: Path to the saved image.
    """
    results = session.results
    if results.empty:
        raise ValueError("No session results to display")

    fig, ax = plt.subplots(figsize=(6, len(results) * 0.4))
    ax.axis('off')

    table = ax.table(
        cellText=results[['Position', 'FullName', 'TeamName', 'GridPosition', 'Points', 'Status']].values,
        colLabels=['Pos', 'Driver', 'Team', 'Grid', 'Pts', 'Status'],
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)

    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    stype = session.name.replace(' ', '_')
    path = f"data/results_{year}_{gp}_{stype}.png"

    os.makedirs("data", exist_ok=True)
    plt.savefig(path, bbox_inches='tight')
    return path
