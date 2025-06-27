import os


class ConfigService:
    """Предоставляет доступ к конфигурации приложения."""

    def __init__(self):
        # Определяем корень проекта как родитель папки src
        config_dir = os.path.dirname(__file__)  # .../src/config
        src_dir = os.path.dirname(config_dir)  # .../src
        self._base_dir = os.path.dirname(src_dir)  # .../giftbot

    @property
    def telegram_token(self) -> str:
        return os.getenv("TELEGRAM_BOT_TOKEN", "")

    @property
    def openai_key(self) -> str:
        if os.getenv("DEBUG") == 'True':
            return os.getenv("OPENAI_API_TEST_KEY", "")
        else:
            return os.getenv("OPENAI_API_KEY", "")

    @property
    def firebase_credentials(self) -> str:
        # Берём из .env (или используем default в корне проекта)
        rel_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
        # Если путь не абсолютный — делаем его относительно base_dir
        if not os.path.isabs(rel_path):
            cred_path = os.path.join(self._base_dir, rel_path)
        else:
            cred_path = rel_path
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Не найден файл: {cred_path}")
        return cred_path

    @property
    def firebase_project_id(self) -> str:
        return os.getenv("FIREBASE_PROJECT_ID", "")

    @property
    def logging_file_path(self) -> str:
        debug_mode = os.getenv("DEBUG") == 'True'
        default_path = os.getenv("LOG_FILE_PATH")
        if not default_path:
            if debug_mode:
                default_path = os.path.join(os.getcwd(), "logs", "giftbot.log")
            else:
                default_path = os.path.join("/app", "logs", "giftbot.log")
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        return default_path
