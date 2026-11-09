"""Provider boundary: map only verified pronotepy capabilities here."""
from dataclasses import dataclass

class ConnectorUnavailable(Exception):
    pass

@dataclass
class PronoteConnector:
    client: object | None = None

    def connect(self, url: str, username: str, password: str) -> None:
        try:
            import pronotepy
            client = pronotepy.Client(url, username=username, password=password)
        except Exception as exc:
            # Do not expose provider internals or credentials to the frontend.
            raise ConnectorUnavailable("Connexion Pronote impossible. Vérifiez l’URL directe de l’espace élève et vos identifiants.") from exc
        if not getattr(client, "logged_in", False):
            raise ConnectorUnavailable("Pronote a refusé la connexion. Vérifiez vos identifiants ou le mode ENT de votre établissement.")
        self.client = client

    def ensure_connected(self) -> object:
        if self.client is None:
            raise ConnectorUnavailable("Connectez un compte Pronote pour consulter ces données.")
        return self.client
