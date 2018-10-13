#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple blockchain implementation with mining
"""

import sys
import datetime
import hashlib

class Block:

    blockID = -1 # Genesis block is 0

    def __init__(self,prev_block_hash, data, timestamp, nonce = 0):
        self.prev_block_hash = prev_block_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.mine()
        Block.blockID += 1

    @staticmethod
    def create_genesis_block():
        return Block(prev_block_hash="0", data="0", timestamp=datetime.datetime.now())

    def build_header_bin(self):
        return (str(self.prev_block_hash) +
                str(self.timestamp)+
                str(self.data) +
                str(self.nonce)).encode()

    def mine(self, difficulty = 3):
        """Parameter:
                difficulty : defines mining difficulty
           Return value:
                hash of the mined block          
        """
        #difficulty_string = ''.join(['0' for x in range(difficulty)])
        difficulty_string = '0' * difficulty
        header_bin = self.build_header_bin()       
        inner_hash = hashlib.sha3_256(header_bin).hexdigest().encode()
        outer_hash = hashlib.sha3_256(inner_hash).hexdigest()
        while outer_hash[:difficulty] != difficulty_string:
            self.nonce += 1
            header_bin = self.build_header_bin()        
            inner_hash = hashlib.sha3_256(header_bin).hexdigest().encode()
            outer_hash = hashlib.sha3_256(inner_hash).hexdigest()
        return outer_hash

    def __str__(self):
        separator = 73 * '-'
        info1 = "|BlkID:"+ str(Block.blockID) + ", Nonce=" + str(self.nonce) + ", Timestamp: " + str(self.timestamp) + "\n"
        info2 = "|prev_hash " + str(self.prev_block_hash) + "\n"
        info3 = "|hash " + str(self.hash) 
        return "+" + separator + "+\n" + info1 + info2 + info3 


def main():
    # Initialize a blockchain with the genesis block
    block_chain = [Block.create_genesis_block()]
    print("The GENESIS block has been created")
    print(block_chain[0]) # display Genesis block

    # Add fake blocks for testing purpose
    num_blocks_to_add = 5

    for i in range(1, num_blocks_to_add + 1):
        block_chain.append(Block(block_chain[-1].hash,
                             "DataBlaBla",
                             datetime.datetime.now()))
        print(block_chain[i])

    return 0

if __name__ == '__main__':
    sys.exit(main())

