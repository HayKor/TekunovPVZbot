from datetime import datetime

from config import config
from gspread.client import Client


def convert_date(date_str: str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    month_names = [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]
    month_name = month_names[dt.month - 1]
    year_str = str(dt.year)[-2:]  # get the last 2 digits of the year
    return f"{month_name}{year_str}"


def get_workers_dict(
    *,
    g_client: Client,
    date: str,
) -> dict[str, str]:
    """
    Get a dictionary of workers from a Google Sheets worksheet.

    Parameters:
    g_client (Client): A Google API client instance.
    date (str): A date string in the format `YYYY-MM-DD`, e.g. `2024-08-18`.

    Returns:
    dict: A dictionary where keys are point names and values are worker names or telegram nicknames (if such exists).
    """

    sh = g_client.open_by_key(config.google_key)

    day = date.split("-")[-1]
    date = convert_date(date)
    worksheet = sh.worksheet(date)

    points = worksheet.col_values(1)  # Always first column
    workers = worksheet.col_values(2 * int(day))
    zipped = zip(points, workers)

    res = {}
    for key, value in zipped:
        key, value = str(key), str(value)
        res[key] = value.split()[-1] if "@" in value else value

    return res
