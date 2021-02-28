#!/usr/bin/env python3

from typing import Dict, List
import json


WEI_IN_ETHER = 1000000000000000000
WEI_IN_GWEI = 1000000000
def eth_to_wei(amount: float) -> int:
    return int(amount * WEI_IN_ETHER)
def gwei_to_wei(amount: float) -> int:
    return int(amount * WEI_IN_GWEI)
def wei_to_eth(amount: int) -> float:
    return float(amount) / WEI_IN_ETHER
def wei_to_usdt(amount: int) -> float:
    return float(amount) / 1e6

AVAX_FIXED_GAS_LIMIT = 100000000
AVAX_FIXED_GAS_PRICE = gwei_to_wei(470)


# Various important addresses, all on AVAX mainnet
wavax_token_address = '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'
png_token_address   = '0x60781C2586D68229fde47564546784ab3fACA982'
link_token_address  = '0xB3fe5374F67D7a22886A0eE082b2E2f9d2651651'
eth_token_address   = '0xf20d962a6c8f70c731bd838a3a388D7d48fA6e15'
uni_token_address   = '0xf39f9671906d8630812f9d9863bBEf5D523c84Ab'
aave_token_address  = '0x8cE2Dee54bB9921a2AE0A63dBb2DF8eD88B91dD9'
usdt_token_address  = '0xde3A24028580884448a5397872046a019649b084'
wbtc_token_address  = '0x408D4cD0ADb7ceBd1F1A1C33A0Ba2098E1295bAB'
dai_token_address   = '0xbA7dEebBFC5fA1100Fb055a87773e1E99Cd3507a'

pangolin_router_address = '0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106'
pangolin_factory_address = '0xefa94DE7a4656D787667C749f7E1223D71E9FD88'

pangolin_router_address = '0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106'
pangolin_factory_address = '0xefa94DE7a4656D787667C749f7E1223D71E9FD88'

pgl_pair_eth_avax_address = '0x1aCf1583bEBdCA21C8025E172D8E8f2817343d65'
pgl_pair_link_avax_address = '0xbbC7fFF833D27264AaC8806389E02F717A5506c9'
pgl_pair_usdt_avax_address = '0x9EE0a4E21bd333a6bb2ab298194320b8DaA26516'
pgl_pair_wbtc_avax_address = '0x7a6131110B82dAcBb5872C7D352BfE071eA6A17C'
pgl_pair_dai_avax_address = '0x17a2E8275792b4616bEFb02EB9AE699aa0DCb94b'
pgl_pair_aave_avax_address = '0x5F233A14e1315955f48C5750083D9A44b0DF8B50'
pgl_pair_png_avax_address = '0xd7538cABBf8605BdE1f4901B47B8D42c61DE0367'
pgl_pair_sushi_avax_address = '0xd8B262C0676E13100B33590F10564b46eeF652AD'
pgl_pair_yifi_avax_address = '0x7A886B5b2F24eD0Ec0B3C4a17b930E16d160BD17'
pgl_pair_uni_avax_address = '0x92dC558cB9f8d0473391283EaD77b79b416877cA'
pgl_pair_png_link_address = '0x7313835802C6e8CA2A6327E6478747B71440F7a4'


avax_png_pool_rewards_address = "0x8FD2755c6ae7252753361991bDcd6fF55bDc01CE"
avax_link_pool_rewards_address = "0x7d7eCd4d370384B17DFC1b4155a8410e97841B65"
png_link_pool_rewards_address = "0x4Ad6e309805cb477010beA9fFC650cB27C1A9504"

with open('pangolinRouterABI.json','r') as pangolinRouterABIFile:
    pangolin_router_abi: List[Dict] = json.load(pangolinRouterABIFile)
with open('pangolinFactoryABI.json','r') as pangolinFactoryABIFile:
    pangolin_factory_abi: List[Dict] = json.load(pangolinFactoryABIFile)
with open('pangolinPairABI.json','r') as PangolinPairABIFile:
    pangolin_pair_abi: List[Dict] = json.load(PangolinPairABIFile)

with open('stakingRewardsABI.json','r') as StakingRewardsABIFile:
    staking_rewards_abi: List[Dict] = json.load(StakingRewardsABIFile)

with open('IERC20ABI.json','r') as IERC20ABIFile:
    ierc20_abi: List[Dict] = json.load(IERC20ABIFile)


token_list = [ wavax_token_address, png_token_address, link_token_address, eth_token_address, uni_token_address, aave_token_address, usdt_token_address, wbtc_token_address, dai_token_address ]
token_address_human_names_dict: Dict[str, str] = {
        wavax_token_address: 'WAVAX', 
        png_token_address:   'PNG', 
        link_token_address:  'LINK', 
        eth_token_address:   'ETH', 
        uni_token_address:   'UNI', 
        aave_token_address:  'AAVE', 
        usdt_token_address:  'USDT', 
        wbtc_token_address:  'WBTC', 
        dai_token_address:   'DAI'
}
human_names_token_address_dict: Dict[str, str] = {
        'WAVAX': wavax_token_address, 
        'PNG': png_token_address, 
        'LINK': link_token_address, 
        'ETH': eth_token_address, 
        'UNI': uni_token_address, 
        'AAVE': aave_token_address, 
        'USDT': usdt_token_address, 
        'WBTC': wbtc_token_address, 
        'DAI': dai_token_address
}

