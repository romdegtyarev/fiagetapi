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

    print("\n🏁 Session Results:\n")
    for _, row in results.iterrows():
        print(f"{row['Position']:>2}. {row['FullName']:<20} ({row['TeamName']}) — Grid: {row['GridPosition']}, Points: {row['Points']}, Status: {row['Status']}")


def generate_results_image(session) -> str:
    """
    Generate an image of the session results in table format.

    :param session: A FastF1 session object.
    :return: Path to the saved image.
    """
    results = session.results
    if results.empty:
        print("⚠ No session results available.")
        return None

    fig, ax = plt.subplots(figsize=(6, len(results) * 0.4))
    table = ax.table(
        cellText=results[['Position', 'FullName', 'TeamName', 'GridPosition', 'Points', 'Status']].values,
        colLabels=['Pos', 'Driver', 'Team', 'Grid', 'Pts', 'Status'],
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)

    # Legend
    ax.axis('off')

    # Save file
    event = session.event
    year = event['EventDate'].year
    gp = event['EventName'].replace(' ', '_')
    type = session.name.replace(' ', '_')
    filename = f"data/result_{year}_{gp}_{type}.png"

    # Close
    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
    plt.close(fig)
    return filename
