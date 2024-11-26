import streamlit as st
import graphviz
from blockchain.blockchain import Blockchain

def blockchain_to_graph(blockchain):

    dot = graphviz.Digraph()
    chain = blockchain.get_chain()

    for block in chain:
        block_id = block['id']
        sequency = block['payload']['sequency']
        hash_value = block['header']['hash']
        previous_hash = block['payload']['previous_hash']
        

        dot.node(
            block_id, 
            f"Block #{sequency}\nHash: {hash_value[:8]}\nNonce: {block['header']['nonce']}\n"
        )
        

        if previous_hash:
            previous_block_id = next(
                (b['id'] for b in chain if b['header']['hash'] == previous_hash), None
            )
            if previous_block_id:
                dot.edge(previous_block_id, block_id)

    return dot

def main():
    st.title("Visualização da Blockchain")
    st.write("Grafo para visualização dos blocos.")


    blockchain = Blockchain()

    st.header("Grafo da Blockchain")
    dot = blockchain_to_graph(blockchain)
    st.graphviz_chart(dot.source)

if __name__ == "__main__":
    main()
