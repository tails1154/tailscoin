import unittest

from tailscoin.core import Blockchain, Transaction, Wallet


class BlockchainTests(unittest.TestCase):
    def test_mining_and_transfer(self):
        chain = Blockchain(difficulty=1, reward=100)
        miner, receiver = Wallet(), Wallet()
        chain.mine(miner.address)
        chain.add_signed(Transaction(miner.address, receiver.address, 25), miner)
        chain.mine(miner.address)
        self.assertEqual(chain.balance(receiver.address), 25)
        self.assertTrue(chain.is_valid())


    def test_tampering_is_detected(self):
        chain = Blockchain(difficulty=1)
        wallet = Wallet()
        chain.mine(wallet.address)
        chain.chain[1].transactions[0]["amount"] = 999999
        self.assertFalse(chain.is_valid())

