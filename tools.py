def create_reminder(text: str, time: str) -> str:
    """Creates a reminder with the given text at the given time.

    Args:
        text: What the reminder is about.
        time: When the reminder should trigger (e.g. '6pm', 'tomorrow 9am').
    """
    with open("reminders.txt", "a") as f:
        f.write(f"{time} - {text}\n")
    return f"Reminder set: '{text}' at {time}"


def list_reminders() -> str:
    """Lists all currently saved reminders."""
    try:
        with open("reminders.txt", "r") as f:
            content = f.read()
        return content if content else "No reminders yet."
    except FileNotFoundError:
        return "No reminders yet."