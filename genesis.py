import datetime as date
import block as blk

def create_genesis_block():
    return blk.Block(0, date.datetime.now(), "Genesis Block", "0")