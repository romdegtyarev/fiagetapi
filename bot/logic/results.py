import re
import fastf1
import matplotlib.pyplot as plt
import pandas as pd
from logic.utils import safe_name, make_data_filename


DRIVER_TRANSLATION = {
    "Charles Leclerc": "Шарль Леклер",
    "Lewis Hamilton": "Льюис Хэмилтон",
    "Oscar Piastri": "Оскар Пиастри",
    "Lando Norris": "Ландо Норрис",
    "Max Verstappen": "Макс Ферстаппен",
    "Liam Lawson": "Лиам Лоусон",
    "George Russell": "Джордж Расселл",
    "Kimi Antonelli": "Кими Антонелли",
    "Alexander Albon": "Алекс Элбон",
    "Carlos Sainz": "Карлос Сайнс",
    "Yuki Tsunoda": "Юки Цунода",
    "Isack Hadjar": "Айзек Хаджар",
    "Fernando Alonso": "Фернандо Алонсо",
    "Lance Stroll": "Лэнс Стролл",
    "Pierre Gasly": "Пьер Гасли",
    "Jack Doohan": "Джек Дуэн",
    "Franco Colapinto": "Франко Колапинто",
    "Esteban Ocon": "Эстебан Окон",
    "Oliver Bearman": "Оливер Берман",
    "Nico Hulkenberg": "Нико Хюлькенберг",
    "Gabriel Bortoleto": "Габриэль Бортолето",
}


def print_results(session) -> None:
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

    columns = ['Position', 'FullName', 'TeamName', 'GridPosition', 'Points', 'Status']
    data = results[columns].astype(str).values.tolist()
    col_labels = ['Pos', 'Driver', 'Team', 'Grid', 'Pts', 'Status']

    n_rows = len(data)
    n_cols = len(col_labels)
    cell_height = 0.5
    cell_width = 2.0

    fig_width = n_cols * cell_width
    fig_height = max(4, n_rows * cell_height * 0.9)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')

    header_color = "#24262b"
    cell_color = "#181a20"
    edge_color = "#444444"
    font_color = "#f3f3f3"
    header_font_color = "#ffe080"

    table = ax.table(
        cellText=data,
        colLabels=col_labels,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.1, 1.15)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(edge_color)
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(weight='bold', color=header_font_color)
            cell.set_height(cell_height * 0.9)
        else:
            cell.set_facecolor(cell_color)
            cell.set_text_props(color=font_color)
            cell.set_height(cell_height * 0.9)
    for key in table.get_celld():
        table.get_celld()[key].set_linewidth(1.2)

    filename = make_data_filename("result", session)
    fig.tight_layout(pad=0.3)
    fig.savefig(filename, bbox_inches='tight', dpi=180, facecolor="#181a20")
    plt.close(fig)
    return filename


def safe_int(val) -> int:
    try:
        return int(val) if pd.notna(val) else 0
    except Exception:
        return 0


def safe_float(val) -> float:
    try:
        return float(val) if pd.notna(val) else 0.0
    except Exception:
        return 0.0


def export_results_csv(session) -> str:
    """
    Export session results to a CSV compatible with Google Sheets F1 template.

    :param session: FastF1 session object (main race).
    :return: Path to the saved csv.
    """
    results = session.results
    if results.empty:
        print("⚠ No session results available.")
        return None

    event = session.event
    sprint_data = {}
    try:
        gp_event = event['EventName']
        sprint_session = fastf1.get_session(year, gp_event, 'Sprint')
        sprint_session.load()
        sprint_results = sprint_session.results
        if not sprint_results.empty:
            for _, row in sprint_results.iterrows():
                sprint_data[row['Abbreviation']] = {
                    "laps": int(row['Laps']),
                    "points": float(row['Points']),
                }
            print("🏁 Sprint session has been loaded.")
    except Exception as e:
        print(f"⚠ No sprint session results available: {e}.")

    rows = []
    gp_event = event['EventName']
    race_col_name = gp_event
    for _, row in results.iterrows():
        rus_name = DRIVER_TRANSLATION.get(row['FullName'], row['FullName'])
        laps_val = row['Laps'] if 'Laps' in row and pd.notna(row['Laps']) else 0
        abbreviation = row['Abbreviation']
        sprint_laps = safe_int(sprint_data.get(abbreviation, {}).get("laps", 0))
        sprint_points = safe_float(sprint_data.get(abbreviation, {}).get("points", 0))

        rows.append({
            race_col_name: rus_name,
            "Позиция на старте": safe_int(row.get('GridPosition', 0)),
            "Позиция на финише": safe_int(row.get('Position', 0)),
            "Круги": safe_int(laps_val),
            "Круги спринт": sprint_laps,
            "Очки": safe_float(row.get('Points', 0)),
            "Очки спринт": sprint_points
        })
    df = pd.DataFrame(rows)
    driver_order = list(DRIVER_TRANSLATION.values())
    df[race_col_name] = pd.Categorical(df[race_col_name], categories=driver_order, ordered=True)
    df = df.sort_values(by=race_col_name, kind='stable').reset_index(drop=True)

    filename = make_data_filename("result", session, "csv")
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename
