import argparse

from .core import Blockchain, Transaction, Wallet


def main() -> None:
    parser = argparse.ArgumentParser(description="TailsCoin demo CLI")
    parser.add_argument("command", choices=["demo", "wallet"])
    args = parser.parse_args()
    if args.command == "wallet":
        wallet = Wallet()
        print(f"address={wallet.address}\nsecret={wallet.secret}")
        return
    chain, miner = Blockchain(), Wallet()
    chain.mine(miner.address)
    print("TailsCoin is alive!", miner.address, "balance=", chain.balance(miner.address))
    print("chain valid=", chain.is_valid(), "height=", len(chain.chain))

