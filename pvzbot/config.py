from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
    )
    bot_token: str
    father_chat_id: int
    pvz_chat_id: int
    pvz_tech_chat_id: int
    database_url: str


config = Config()
