from genesis import create_genesis_block
from newblock import next_block

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

num_of_blocks = 20

for _ in range(num_of_blocks):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print "Block #{} has been added to the blockchain.".format(block_to_add.index)
    print "Hash: {}".format(block_to_add.hash)
