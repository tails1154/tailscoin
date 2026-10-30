# TailsCoin 🐕

TailsCoin is a tiny, runnable meme-coin blockchain written in Python. It includes proof-of-work mining, wallets, signed demo transactions, balances, a JSON node API, and tests.

> Educational software. This is not production cryptocurrency software, a secure wallet, or financial advice. The first protocol uses HMAC-backed demo signatures and a single-node in-memory ledger; do not use it for real money or secrets.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
tailscoin demo
PYTHONPATH=src python -m unittest discover -s tests -v
```

Start the node:

```bash
tailscoind
open http://127.0.0.1:8333
curl -X POST http://127.0.0.1:8333/wallet
curl http://127.0.0.1:8333/chain
```

The API exposes `POST /wallet`, `POST /transactions`, `POST /mine`, `GET /chain`, and `GET /balance?address=...`.

## Roadmap

Before calling this a public cryptocurrency: replace the demo signing scheme with audited asymmetric cryptography, persist the ledger, add peer-to-peer consensus and fork choice, validate all transaction replay rules, add rate limits and key protection, and get an independent security review.

