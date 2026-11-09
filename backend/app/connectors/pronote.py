"""Provider boundary: map only verified pronotepy capabilities here."""
from dataclasses import dataclass

class ConnectorUnavailable(Exception):
    pass

@dataclass
class PronoteConnector:
    client: object | None = None

    def connect(self, url: str, username: str, password: str) -> None:
        # ENT/CAS flows are institution-specific: never guess or bypass them.
        # Add a documented pronotepy login flow here when it is verified.
        raise ConnectorUnavailable("La connexion à cet établissement n’est pas encore configurée.")

    def ensure_connected(self) -> object:
        if self.client is None:
            raise ConnectorUnavailable("Connectez un compte Pronote pour consulter ces données.")
        return self.client
