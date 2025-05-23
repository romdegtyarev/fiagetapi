def get_summary_text(session) -> str:
    """
    Generate a brief textual summary of the session.

    :param session: A FastF1 session object.
    :return: str: Summary text.
    """
    summary = f"\n🏁 {session.event['EventName']} — Session Results:\n"
    return summary


def print_summary(session):
    """
    Print a brief summary of the session.

    :param session: A FastF1 session object.
    """
    print(get_summary_text(session))
