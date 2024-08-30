import pathlib

from gspread.auth import service_account


work_dir = pathlib.Path(__file__).parent.parent.parent.parent
credentials_path = work_dir / "credentials.json"

gc = service_account(
    filename=credentials_path,
)
