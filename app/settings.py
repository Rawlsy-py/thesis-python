"""App Settings."""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic import BaseSettings


class Settings(BaseSettings):
    azure_key_vault_url: str
    database_url_secret_name: str
    database_username_secret_name: str
    database_password_secret_name: str

    class Config:
        env_file = ".env"


settings = Settings()

credential = DefaultAzureCredential()
secret_client = SecretClient(
    vault_url=settings.azure_key_vault_url, credential=credential
)


def get_database_credentials():
    database_url = secret_client.get_secret(settings.database_url_secret_name).value
    database_username = secret_client.get_secret(
        settings.database_username_secret_name
    ).value
    database_password = secret_client.get_secret(
        settings.database_password_secret_name
    ).value

    return {
        "database_url": database_url,
        "database_username": database_username,
        "database_password": database_password,
    }


# Usage example
if __name__ == "__main__":
    creds = get_database_credentials()
    print(creds)
