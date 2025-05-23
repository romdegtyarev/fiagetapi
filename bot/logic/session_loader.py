import fastf1


def load_session(year: int, gp: str, sess_type: str):
    """
    Load a Formula 1 session using FastF1.

    :param year: Season year.
    :param gp: Grand Prix name.
    :param sess_type: Session type.
    :return: A loaded FastF1 session object.
    """
    session = fastf1.get_session(year, gp, sess_type)
    session.load()
    return session
