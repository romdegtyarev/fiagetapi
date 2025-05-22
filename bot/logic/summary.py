def get_summary_text(session):
    summary = f"Сессия: {session.event['EventName']} ({session.event['EventDate']})\n"
    return summary


def print_summary(session):
    print(get_summary_text(session))
