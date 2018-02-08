# -*- coding: utf-8 -*-
import json
import datetime as date

import sys
from flask import Flask
from flask import request
from pip._vendor import requests

from block import Block
from genesis import create_genesis_block

node = Flask(__name__)

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
blockchain = []
node_transactions = []
peer_nodes = []
mining = True

@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_transaction = request.get_json()
        node_transactions.append(new_transaction)
        print "New Transaction:\n"
        print "FROM: {}\n".format(new_transaction['from'])
        print "TO: {}\n".format(new_transaction['to'])
        print "AMOUNT: {}\n".format(new_transaction['amount'])
        return "Transaction submission successful.\n"

@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain)-1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    node_transactions.append(
        {
            "from" : "network",
            "to" : miner_address,
            "amount" : 1
        }
    )
    new_block_data = {
        "proof-of-work" : proof,
        "transactions" : list(node_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    node_transactions[:] = []
    mined_block = Block(new_block_index,
                        new_block_timestamp,
                        new_block_data,
                        last_block_hash)
    blockchain.append(mined_block)
    return json.dumps(
        {
            "index" : new_block_index,
            "timestamp" : str(new_block_timestamp),
            "data" : new_block_data,
            "hash" : last_block_hash
        }
    ) + "\n"

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    # 同时整除7和last_proof
    while not (incrementor % 7 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/blocks', methods=['GET'])
def get_blocks():
    ret = []
    for block in consensus():
        ret.append({
            "index" : str(block.index),
            "timestamp" : str(block.timestamp),
            "data" : str(block.data),
            "hash" : block.hash
        })
    return json.dumps(ret)

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    global blockchain
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    return update_blockchain(longest_chain)

def update_blockchain(src):
    if len(src) <= len(blockchain):
        return blockchain
    ret = []
    for b in src:
        ret.append(Block(b['index'], b['timestamp'], b['data'], b['hash']))
    return ret

@node.route('/add_peer', methods=['GET'])
def add_peer():
    host = request.args['host'] if 'host' in request.args else 'localhost'
    port = request.args['port']
    peer = host + ':' + port
    peer_nodes.append(peer)
    print "Peer added: {}".format(peer)
    return True

def main():
    port = 5000
    if len(sys.argv) > 1:
        port = sys.argv[1]
    blockchain.append(create_genesis_block())
    node.run(port=port)

if __name__ == '__main__':
    main()
