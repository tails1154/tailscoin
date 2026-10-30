import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .core import Blockchain, Transaction, Wallet

CHAIN = Blockchain()
WALLETS: dict[str, Wallet] = {}


class Handler(BaseHTTPRequestHandler):
    def _send(self, payload: dict, status: int = 200) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/chain":
            self._send(CHAIN.to_dict())
        elif parsed.path == "/balance":
            address = parse_qs(parsed.query).get("address", [""])[0]
            self._send({"address": address, "balance": CHAIN.balance(address)})
        else:
            self._send({"error": "not found"}, 404)

    def do_POST(self) -> None:
        try:
            raw_body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            body = json.loads(raw_body) if raw_body else {}
            if self.path == "/wallet":
                wallet = Wallet()
                WALLETS[wallet.address] = wallet
                self._send({"address": wallet.address, "secret": wallet.secret}, 201)
            elif self.path == "/mine":
                block = CHAIN.mine(body["miner"])
                self._send({"block": block.__dict__})
            elif self.path == "/transactions":
                wallet = WALLETS[body["sender"]]
                CHAIN.add_signed(Transaction(body["sender"], body["recipient"], int(body["amount"])), wallet)
                self._send({"status": "queued"}, 201)
            else:
                self._send({"error": "not found"}, 404)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            self._send({"error": str(exc)}, 400)

    def log_message(self, *_args) -> None:
        pass


def main() -> None:
    server = HTTPServer(("127.0.0.1", 8333), Handler)
    print("TailsCoin node listening on http://127.0.0.1:8333")
    server.serve_forever()

