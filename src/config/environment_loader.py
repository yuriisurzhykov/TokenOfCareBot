from dotenv import load_dotenv


class EnvironmentLoader:
    """Загружает переменные окружения из .env."""

    @staticmethod
    def load() -> None:
        load_dotenv()
