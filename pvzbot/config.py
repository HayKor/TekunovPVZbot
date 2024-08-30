from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
    )
    engine_echo: bool
    google_key: str
    bot_token: str
    database_url: str
    father_chat_id: int
    pvz_chat_id: int
    pvz_tech_chat_id: int
    pvz_attendance_chat_id: int


config = Config()
