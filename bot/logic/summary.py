def get_summary_text(session):
    laps = session.laps.pick_quicklaps()
    summary = f"Session: {session.event['EventName']} ({session.event['EventDate']})\n"
    summary += f"Fastest Lap: {laps.pick_fastest()['Driver']} – {laps.pick_fastest()['LapTime']}"
    return summary

def print_summary(session):
    print(get_summary_text(session))
