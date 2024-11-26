import argparse

from blockchain.blockchain import Blockchain


parser = argparse.ArgumentParser(description="To start Blockchain:")
parser.add_argument("difficulty", type=int, help="Block Mining Difficulty")
parser.add_argument("n_blocks", type=int, help="Number of blocks")


if __name__ == "__main__":

    args = parser.parse_args()
    
    difficulty = args.difficulty
    n_blocks = args.n_blocks
    
    blockchain = Blockchain(difficulty)

    for i in range(1, n_blocks+1):
        block = blockchain.create_block(f"Bloco: {i}")
        mined_block = blockchain.block_miner(block)
        blockchain.send_block(mined_block)


    print("\n###### BLOCKCHAIN ######")
    for _, obj in enumerate(blockchain.get_chain()):
        print(obj, end="\n\n")
