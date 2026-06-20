import os


class Settings:

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "llama3.2:3b"
    )

    def validate(self):
        return True


settings = Settings()