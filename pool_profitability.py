#!/usr/bin/env python3

from web3 import Web3
import web3
import json
from typing import List, Dict
from web3.middleware import geth_poa_middleware
from web3.types import RPCEndpoint
import logging
from avax_common import *

# Change these to see your own numbers!
LINK_PUT_IN = 1000000000000000000
PNG_PUT_IN =  1000000000000000000
AVAX_PUT_IN = 1000000000000000000
MY_ADDRESS = "0xDEADBEEF6969cafebabe01234567890042031337"

GAS_PAID_TO_DO_STUFF = 1234567
TXFEES_PAID_TO_DO_STUFF = GAS_PAID_TO_DO_STUFF * AVAX_FIXED_GAS_PRICE


if __name__=='__main__':
    logging.basicConfig(filename='pool_profitability.log', level=logging.DEBUG)
    # Change to https://api.avax.network/ext/bc/C/rpc if you don't have access to your own node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9650/ext/bc/C/rpc')) 
    avax_png_pool_rewards_contract = w3.eth.contract(address=avax_png_pool_rewards_address, abi=staking_rewards_abi) # type: ignore
    avax_link_pool_rewards_contract = w3.eth.contract(address=avax_link_pool_rewards_address, abi=staking_rewards_abi) # type: ignore
    png_link_pool_rewards_contract = w3.eth.contract(address=png_link_pool_rewards_address, abi=staking_rewards_abi) # type: ignore

    wavax_contract = w3.eth.contract(address=wavax_token_address, abi=ierc20_abi) # type: ignore
    link_contract = w3.eth.contract(address=link_token_address, abi=ierc20_abi) # type: ignore
    png_contract = w3.eth.contract(address=png_token_address, abi=ierc20_abi) # type: ignore

    avax_png_pool_contract = w3.eth.contract(address=pgl_pair_png_avax_address, abi=pangolin_pair_abi) # type: ignore
    avax_link_pool_contract = w3.eth.contract(address=pgl_pair_link_avax_address, abi=pangolin_pair_abi) # type: ignore
    png_link_pool_contract = w3.eth.contract(address=pgl_pair_png_link_address, abi=pangolin_pair_abi) # type: ignore

    my_pgl_avax_png_tokens = avax_png_pool_rewards_contract.functions.balanceOf(MY_ADDRESS).call()
    my_pgl_avax_link_tokens = avax_link_pool_rewards_contract.functions.balanceOf(MY_ADDRESS).call()
    my_pgl_png_link_tokens = png_link_pool_rewards_contract.functions.balanceOf(MY_ADDRESS).call()

    print('PGL AVAX_PNG: ', wei_to_eth(my_pgl_avax_png_tokens))
    print('PGL AVAX_LINK: ', wei_to_eth(my_pgl_avax_link_tokens))
    print('PGL PNG_LINK: ', wei_to_eth(my_pgl_png_link_tokens))
    print()

    earned_avax_png_png_amount = avax_png_pool_rewards_contract.functions.earned(MY_ADDRESS).call()
    earned_avax_png_link_amount = avax_link_pool_rewards_contract.functions.earned(MY_ADDRESS).call()
    earned_png_png_link_amount = png_link_pool_rewards_contract.functions.earned(MY_ADDRESS).call()
    print('Earned PNG from AVAX_PNG POOL: ',  wei_to_eth(earned_avax_png_png_amount))
    print('Earned PNG from AVAX_LINK POOL: ', wei_to_eth(earned_avax_png_link_amount))
    print('Earned PNG from PNG_LINK POOL: ',  wei_to_eth(earned_png_png_link_amount))
    print()

    # png_reserve, avax_reserve, last_block_timestamp = avax_png_pool_contract.functions.getReserves().call()
    # print('PGL PNG_AVAX_PNG AVAX Reserves: ', wei_to_eth(avax_reserve))
    # print('PGL PNG_AVAX_PNG PNG Reserves: ', wei_to_eth(png_reserve))



    # Amount got back calculation taken from referencing
    # burn function in PangolinPair.sol: 
    #uint liquidity = balanceOf[address(this)];
    #amount0 = liquidity.mul(balance0) / _totalSupply; // using balances ensures pro-rata distribution
    #amount1 = liquidity.mul(balance1) / _totalSupply; // using balances ensures pro-rata distribution
    total_supply_pgl_avax_png_tokens  = avax_png_pool_contract.functions.totalSupply().call()
    total_supply_pgl_avax_link_tokens = avax_link_pool_contract.functions.totalSupply().call()
    total_supply_pgl_png_link_tokens  = png_link_pool_contract.functions.totalSupply().call()

    avax_png_pool_all_liquidity_avax = wavax_contract.functions.balanceOf(pgl_pair_png_avax_address).call()
    avax_png_pool_all_liquidity_png  =   png_contract.functions.balanceOf(pgl_pair_png_avax_address).call()
    avax_png_pool_amount_avax_received = (my_pgl_avax_png_tokens * avax_png_pool_all_liquidity_avax) / total_supply_pgl_avax_png_tokens
    avax_png_pool_amount_png_received =  (my_pgl_avax_png_tokens * avax_png_pool_all_liquidity_png ) / total_supply_pgl_avax_png_tokens

    print('AVAX_PNG_POOL AVAX Got Back From Withdraw: ', wei_to_eth(avax_png_pool_amount_avax_received))
    print('AVAX_PNG_POOL PNG  Got Back From Withdraw: ', wei_to_eth(avax_png_pool_amount_png_received))

    avax_link_pool_all_liquidity_avax = wavax_contract.functions.balanceOf(pgl_pair_link_avax_address).call()
    avax_link_pool_all_liquidity_link =  link_contract.functions.balanceOf(pgl_pair_link_avax_address).call()
    avax_link_pool_amount_avax_received = (my_pgl_avax_link_tokens * avax_link_pool_all_liquidity_avax) / total_supply_pgl_avax_link_tokens
    avax_link_pool_amount_link_received = (my_pgl_avax_link_tokens * avax_link_pool_all_liquidity_link) / total_supply_pgl_avax_link_tokens

    print('AVAX_LINK AVAX Got Back From Withdraw: ', wei_to_eth(avax_link_pool_amount_avax_received))
    print('AVAX_LINK LINK Got Back From Withdraw: ', wei_to_eth(avax_link_pool_amount_link_received))

    png_link_pool_all_liquidity_png =  png_contract.functions.balanceOf(pgl_pair_png_link_address).call()
    png_link_pool_all_liquidity_link= link_contract.functions.balanceOf(pgl_pair_png_link_address).call()
    png_link_pool_amount_png_received =  (my_pgl_png_link_tokens * png_link_pool_all_liquidity_png)  / total_supply_pgl_png_link_tokens
    png_link_pool_amount_link_received = (my_pgl_png_link_tokens * png_link_pool_all_liquidity_link) / total_supply_pgl_png_link_tokens

    print('PNG_LINK PNG Got Back From Withdraw: ', wei_to_eth(png_link_pool_amount_png_received))
    print('PNG_LINK LINK Got Back From Withdraw: ', wei_to_eth(png_link_pool_amount_link_received))


    print()
    print('TOTALS')
    avax_withdrawn = avax_png_pool_amount_avax_received + avax_link_pool_amount_avax_received
    link_withdrawn = avax_link_pool_amount_link_received + png_link_pool_amount_link_received
    png_withdrawn = avax_png_pool_amount_png_received + png_link_pool_amount_png_received 
    png_rewards = earned_avax_png_png_amount + earned_avax_png_link_amount + earned_png_png_link_amount
    print('AVAX: ', wei_to_eth(avax_withdrawn))
    print('LINK: ', wei_to_eth(link_withdrawn))
    print('PNG: ', wei_to_eth( png_withdrawn + png_rewards))


    pangolin_router_contract = w3.eth.contract(address=pangolin_router_address, abi=pangolin_router_abi) # type: ignore
    path_link_avax = [ link_token_address,  wavax_token_address ]
    path_avax_png =  [ png_token_address,   wavax_token_address ]
    path_avax_usdt = [ wavax_token_address, usdt_token_address ]
    path_png_usdt =  [ png_token_address,   usdt_token_address ]
    path_link_usdt = [ link_token_address,  wavax_token_address, usdt_token_address ]


    avax_from_link_amount = (pangolin_router_contract.functions.getAmountsOut(int(link_withdrawn), path_link_avax).call())[1]
    avax_from_png_amount =  (pangolin_router_contract.functions.getAmountsOut(int(png_withdrawn + png_rewards), path_avax_png).call())[1]
    usdt_from_converted_avax_amount = (pangolin_router_contract.functions.getAmountsOut(int(avax_withdrawn + avax_from_link_amount + avax_from_png_amount), path_avax_usdt).call())[1]
    print()
    print('Current value converted all to AVAX ', wei_to_eth(avax_withdrawn + avax_from_link_amount + avax_from_png_amount))
    print('Current value converted all to USDT ', wei_to_usdt(usdt_from_converted_avax_amount))


    avax_net = avax_withdrawn - AVAX_PUT_IN - TXFEES_PAID_TO_DO_STUFF
    link_net = link_withdrawn - LINK_PUT_IN
    png_net  = png_withdrawn + png_rewards - PNG_PUT_IN
    png_net_nostake = png_withdrawn - PNG_PUT_IN

    usdt_from_avax_net_amount     = (pangolin_router_contract.functions.getAmountsOut(int(abs(avax_net)), path_avax_usdt).call())[1]
    usdt_from_link_net_amount     = (pangolin_router_contract.functions.getAmountsOut(int(abs(link_net)), path_link_usdt).call())[2]
    usdt_from_png_net_amount      = (pangolin_router_contract.functions.getAmountsOut(int(abs(png_net)),  path_png_usdt).call())[1]
    usdt_from_png_nostake_amount  = (pangolin_router_contract.functions.getAmountsOut(int(abs(png_net_nostake)),  path_png_usdt).call())[1]

    if avax_net < 0:
        usdt_from_avax_net_amount = usdt_from_avax_net_amount * -1
    if link_net < 0:
        usdt_from_link_net_amount = usdt_from_link_net_amount * -1
    if png_net < 0:
        usdt_from_png_net_amount = usdt_from_png_net_amount * -1
    if png_net_nostake < 0:
        usdt_from_png_nostake_amount = usdt_from_png_nostake_amount * -1

    print()
    print('AVAX NET RESULT: {:.18f} ${:.2f}'.format(wei_to_eth(avax_net), wei_to_usdt(usdt_from_avax_net_amount)))
    print('LINK NET RESULT: {:.18f} ${:.2f}'.format(wei_to_eth(link_net), wei_to_usdt(usdt_from_link_net_amount)))
    print('PNG NET RESULT:  {:.18f} ${:.2f}'.format(wei_to_eth(png_net),  wei_to_usdt(usdt_from_png_net_amount)))
    print('PNG NET NO STAKING RESULT: {:.18f} ${:.2f}'.format(wei_to_eth(png_net_nostake), wei_to_usdt(usdt_from_png_nostake_amount)))

    print('USDT NET RESULT: ${:.2f}'.format( wei_to_usdt(usdt_from_png_net_amount + usdt_from_link_net_amount + usdt_from_avax_net_amount)))



