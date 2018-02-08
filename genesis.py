import datetime as date
import block as blk

def create_genesis_block():
    return blk.Block(0, date.datetime.now(), {
        "proof-of-work" : 7,
        "transactions" : None
    }, "0")