# belso.utils.formats

class FORMATS:
    """
    A class that provides constants for supported schema providers.
    This allows for more readable code when specifying providers in the convert method.
    """
    # Core providers
    BELSO = "belso"

    # LLM providers
    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    MISTRAL = "mistral"
    LANGCHAIN = "langchain"

    # Serialization formats
    JSON = "json"
    XML = "xml"
    YAML = "yaml"

    @classmethod
    def get_all_formats(cls) -> list:
        """
        Get a list of all supported providers.\n
        ---
        ### Returns
        - `list`: a list of all provider constants.
        """
        return [
            cls.BELSO,
            cls.GOOGLE,
            cls.OPENAI,
            cls.ANTHROPIC,
            cls.OLLAMA,
            cls.HUGGINGFACE,
            cls.MISTRAL,
            cls.LANGCHAIN,
            cls.JSON,
            cls.XML,
            cls.YAML
        ]
