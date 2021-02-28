#!/usr/bin/env python3

from web3 import Web3
import web3
import json
from typing import List, Dict
from web3.middleware import geth_poa_middleware
from web3.types import RPCEndpoint
import logging
from avax_common import *


token_graph_dict = {
        'WAVAX': [ 'PNG', 'LINK', 'ETH', 'UNI', 'AAVE', 'USDT', 'WBTC', 'DAI' ],
        'PNG':   [ 'WAVAX', 'LINK', 'ETH', 'UNI', 'AAVE', 'USDT', 'WBTC', 'DAI' ],
        'LINK':  [ 'WAVAX', 'PNG' ],
        'ETH':   [ 'WAVAX', 'PNG', 'USDT', 'WBTC' ],
        'UNI':   [ 'WAVAX', 'PNG' ],
        'AAVE':  [ 'WAVAX', 'PNG' ],
        'USDT':  [ 'WAVAX', 'PNG', 'ETH', 'DAI' ],
        'WBTC':  [ 'WAVAX', 'PNG', 'ETH' ],
        'DAI':   [ 'WAVAX', 'PNG', 'USDT' ]
}


def find_out_current_pairs(token_list: List[str], pangolin_factory_contract):
    for token_a in token_list:
        for token_b in token_list:
            if token_a == token_b:
                continue
            pair_address = pangolin_factory_contract.functions.getPair(token_a, token_b).call()
            if str(pair_address) != '0x0000000000000000000000000000000000000000':
                out_string = '{} -> {}'.format(token_address_human_names_dict[token_a], token_address_human_names_dict[token_b])
                print(out_string)

def find_all_trades_len_4_wavax(do_print: bool) -> List[List[str]]:
    retlist = []
    start_token = 'WAVAX'
    for token_trade_a in token_graph_dict[start_token]:
        for token_trade_b in token_graph_dict[token_trade_a]:
            if token_trade_b == start_token:
                continue
            else:
                for token_trade_c in token_graph_dict[token_trade_b]:
                    if token_trade_c == start_token:
                        if do_print:
                            print('{} -> {} -> {} -> {}'.format(start_token, token_trade_a, token_trade_b, token_trade_c))
                        trade = [ human_names_token_address_dict[start_token], human_names_token_address_dict[token_trade_a], human_names_token_address_dict[token_trade_b], human_names_token_address_dict[token_trade_c] ]
                        retlist.append(trade)
    return retlist



def find_all_trades_len_4(do_print: bool) -> List[List[str]]:
    retlist = []
    for start_token in token_graph_dict:
        for token_trade_a in token_graph_dict[start_token]:
            for token_trade_b in token_graph_dict[token_trade_a]:
                if token_trade_b == start_token:
                    continue
                else:
                    for token_trade_c in token_graph_dict[token_trade_b]:
                        if token_trade_c == start_token:
                            if do_print:
                                print('{} -> {} -> {} -> {}'.format(start_token, token_trade_a, token_trade_b, token_trade_c))
                            trade = [ human_names_token_address_dict[start_token], human_names_token_address_dict[token_trade_a], human_names_token_address_dict[token_trade_b], human_names_token_address_dict[token_trade_c] ]
                            retlist.append(trade)
    return retlist

def path_to_human_readable(path: List[str]) -> str:
    human_path = []
    for addr in path:
        human_path.append(token_address_human_names_dict[addr])
    separator = ' -> '
    return separator.join(human_path)

if __name__=='__main__':
    logging.basicConfig(filename='crappy_arbitrage.log', level=logging.DEBUG)
    # Change to https://api.avax.network/ext/bc/C/rpc if you don't have access to your own node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9650/ext/bc/C/rpc'))
    #w3.middleware_onion.inject(avalanche_middleware, layer=0)
    #print(w3.eth.get_block('latest'))
    #pangolin_factory_contract = w3.eth.contract(address=pangolin_factory_address, abi=pangolin_factory_abi) # type: ignore
    pangolin_router_contract = w3.eth.contract(address=pangolin_router_address, abi=pangolin_router_abi) # type: ignore
    # wavax_contract = w3.eth.contract(address=wavax_token_address, abi=ierc20_abi) # type: ignore
    # print(wavax_contract.functions.totalSupply().call())
    all_possible_paths = find_all_trades_len_4_wavax(False)
    for path in all_possible_paths:
        try:
            amountsOut = pangolin_router_contract.functions.getAmountsOut(eth_to_wei(30), path).call() #.buildTransaction({'chainId': 43114, 'gas': AVAX_FIXED_GAS_PRICE, 'gasPrice': AVAX_FIXED_GAS_PRICE})
            if amountsOut[0] < amountsOut[3]:
                profit = int(amountsOut[3]) - int(amountsOut[0])
                print('{} - PROFIT: {:.18f}'.format(path_to_human_readable(path), wei_to_eth(profit)))
            else: 
                profit = int(amountsOut[3]) - int(amountsOut[0])
                print('{} - LOSS: {:.18f}'.format(path_to_human_readable(path), wei_to_eth(profit)))
        except web3.exceptions.ContractLogicError as e:
            if str(e) == "execution reverted: PangolinLibrary: INSUFFICIENT_INPUT_AMOUNT":
                print("INSUFFICIENT_INPUT_AMOUNT: {}".format(path_to_human_readable(path)))
                continue
            else:
                raise
