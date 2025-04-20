class PROVIDERS:
    """
    A class that provides constants for supported schema providers.
    This allows for more readable code when specifying providers in the translate method.

    Example usage:
    ```python
    from belso.translator import SchemaTranslator
    from belso.translator.providers import Provider

    # Convert a schema to OpenAI format
    openai_schema = SchemaTranslator.translate(my_schema, Provider.OPENAI)
    ```
    """
    # Core providers
    BELSO = "belso"

    # LLM providers
    GOOGLE = "google"
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    MISTRAL = "mistral"
    LANGCHAIN = "langchain"

    # Serialization formats
    JSON = "json"
    XML = "xml"

    @classmethod
    def get_all_providers(cls) -> list:
        """
        Get a list of all supported providers.

        Returns:
            list: A list of all provider constants.
        """
        return [
            cls.BELSO,
            cls.GOOGLE,
            cls.OPENAI,
            cls.AZURE_OPENAI,
            cls.ANTHROPIC,
            cls.OLLAMA,
            cls.HUGGINGFACE,
            cls.MISTRAL,
            cls.LANGCHAIN,
            cls.JSON,
            cls.XML
        ]
