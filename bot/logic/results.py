import matplotlib.pyplot as plt


def generate_results_image(session):
    results = session.results
    fig, ax = plt.subplots(figsize=(6, len(results) * 0.4))
    ax.axis('off')
    table = ax.table(
        cellText=results[['Position', 'FullName', 'TeamName', 'GridPosition', 'Points', 'Status']].values,
        colLabels=['Pos', 'Driver', 'Team', 'Grid', 'Pts', 'Status'],
        loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)
    path = f"data/{session.event['EventName'].replace(' ', '_')}_results.png"
    plt.savefig(path, bbox_inches='tight')
    return path
