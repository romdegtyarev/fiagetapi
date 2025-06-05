import os
import re
import fastf1
import matplotlib.pyplot as plt
import pandas as pd


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


def safe_name(s: str) -> str:
    return re.sub(r'\W+', '_', s)


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

    fig, ax = plt.subplots(figsize=(6, len(results) * 0.4))
    table = ax.table(
        cellText=results[['Position', 'FullName', 'TeamName', 'GridPosition', 'Points', 'Status']].values,
        colLabels=['Pos', 'Driver', 'Team', 'Grid', 'Pts', 'Status'],
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)

    ax.axis('off')

    event = session.event
    year = event['EventDate'].year
    gp = safe_name(event['EventName'])
    type_name = safe_name(session.name)
    filename = f"data/result_{year}_{gp}_{type_name}.png"

    os.makedirs("data", exist_ok=True)
    fig.savefig(filename)
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
    year = event['EventDate'].year
    gp = safe_name(event['EventName'])
    type_name = safe_name(session.name)
    filename = f"data/result_{year}_{gp}_{type_name}.csv"

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

    os.makedirs("data", exist_ok=True)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename
