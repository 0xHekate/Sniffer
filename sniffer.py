import decimal
import json
import os
import shutil
import sys
from datetime import datetime, timedelta
from web3 import Web3
import time
import requests

DEFAULT_GAS = 700000
DEFAULT_GAS_GWEI = '6'

# @TODO: save addresses to env file
WBNB_CONTRACT = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
BUSD_CONTRACT = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
PCSW_CONTRACT = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
PCSW_FACTORY_CONTRACT = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'

# @TODO: save abis to external directory
PCSW_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
PCSW_FACTORY_ABI = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
PCPAIR_ABI = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
ERC20_ABI = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]';
ERC20_FEE_ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"BuyBackEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokenAmount","type":"uint256"}],"name":"RewardLiquidityProviders","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountIn","type":"uint256"},{"indexed":false,"internalType":"address[]","name":"path","type":"address[]"}],"name":"SwapETHForTokens","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountIn","type":"uint256"},{"indexed":false,"internalType":"address[]","name":"path","type":"address[]"}],"name":"SwapTokensForETH","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"afterPreSale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"buyBackEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"buyBackUpperLimitAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deadAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"marketingAddress","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"marketingDivisor","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minimumTokensBeforeSwapAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"prepareForPreSale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setBuyBackEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"buyBackLimit","type":"uint256"}],"name":"setBuybackUpperLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_marketingAddress","type":"address"}],"name":"setMarketingAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"divisor","type":"uint256"}],"name":"setMarketingDivisor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxAmount","type":"uint256"}],"name":"setMaxTxAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_minimumTokensBeforeSwap","type":"uint256"}],"name":"setNumTokensSellToAddToLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]';

#private key
HEXDATA = ''

#public address
SENDER_ADDRESS = ''


# @TODO: use blockbuilder such as flashbots
_web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
_last_nonce = 0
_tokens = {}
_sellPercentage = 68
_pairContract = {}
_current_quota = ""
_buy_price = ""
_last_price = 0



def saveFile(tokens):
    os.remove('tokens.json');
    with open('tokens.json', 'w') as f:
        f.write(json.dumps(tokens))
        f.close()


def getTokens():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '2',
        'cryptocurrency_type': 'tokens',
        'sort': 'date_added',
        #   'sort_dir': 'asc'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '-YOUR-CMC-API-KEY-',
    }

    response = requests.get(url, headers=headers, params=parameters)

    if not response.ok:
        print("Can't find tokens")
        exit(1)

    data = response.json()['data']

    tokens = [d for d in data if d['platform'] and d['platform']['symbol'] == 'BNB']

    print(tokens)
    if not os.path.exists('tokens.json'):
        tokenFile = open('tokens.json', "w")
        tokenFile.write(json.dumps(data))
        tokenFile.close()

    return tokens


def getPrice(target=WBNB_CONTRACT, token=BUSD_CONTRACT):
    pair = getFactoryContract().functions.getPair(_web3.toChecksumAddress(target),
                                                  _web3.toChecksumAddress(token)).call()
    pairContract = getPairContract(pair)
    reserve0, reserve1, blockTimeStampLast = pairContract.functions.getReserves().call()
    decimals0 = getTokenContract(token).functions.decimals().call()
    token0 = str.lower(pairContract.functions.token0().call())

    if token0 == WBNB_CONTRACT:
        q = (reserve0 / 10 ** decimals0) / reserve1
        spot = '{:.20f}'.format(q)
    else:
        q = reserve1 / (reserve0 / 10 ** decimals0)
        spot = '{:.20f}'.format(_web3.fromWei(q, 'ether'))
    return spot


def getPairContractCached(target=WBNB_CONTRACT, token=BUSD_CONTRACT):
    global _pairContract

    if _pairContract.get(token) == None:
        pair = getFactoryContract().functions.getPair(_web3.toChecksumAddress(target),
                                                      _web3.toChecksumAddress(token)).call()
        x = {token: getPairContract(pair)}
        _pairContract.update(x)

    return _pairContract[token]


def getTokenPaidPrice(token):
    prefixed = [filename for filename in os.listdir('buy') if filename.startswith(token)]
    print(prefixed)
    with open('buy/' + prefixed[0]) as json_file:
        data = json.load(json_file)

    return data['price']


def createSellFile(token, price, balance, growth, txn, status):
    prefixed = [filename for filename in os.listdir('buy') if filename.startswith(token)]
   # os.rename('buy/' + prefixed[0], 'buy/' + 'selled_' + prefixed[0])
    with open('buy/' + prefixed[0]) as f:
        to_insert = json.load(f)
        a_dict = {
            'sold_for': price,
            'sold_at': datetime.utcnow().isoformat(),
            'balance_sold': str(balance),
            'growth': growth,
            'txn': txn,
            'status': status,
        }

        to_insert.update(a_dict)

        filename = 'sell/' + prefixed[0]

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(to_insert, f, ensure_ascii=False, indent=4)


def priceWatcher(decimals0, token0, pairContract, target=WBNB_CONTRACT, token=BUSD_CONTRACT, limitSell=70):
    reserve0, reserve1, blockTimeStampLast = pairContract.functions.getReserves().call()

    if token0 == WBNB_CONTRACT:
        q = (reserve0 / 10 ** decimals0) / reserve1
        print('{:.20f}'.format(q))
        priceQuote = '{:.20f}'.format(q)
        q = decimal.Decimal(q)
    else:
        q = reserve1 / (reserve0 / 10 ** decimals0)
        q = _web3.fromWei(q, 'ether')
        print('{:.20f}'.format(q))
        priceQuote = '{:.20f}'.format(q)

    # 0.00000000000000000322
    # percentageGrowth = (100 * (q - decimal.Decimal(_buy_price)) / q)

    # ((PV/PC)-1)*100 formula calcular percentual
    percentageGrowth = ((q / decimal.Decimal(_buy_price)) - 1) * 100

    print('Percentage')
    percentage = '{0:.2f}'.format(percentageGrowth) + '%'

    print(percentage)

    if percentageGrowth > decimal.Decimal(limitSell):
        sellValue = getBalance(SENDER_ADDRESS, token)
        approveSell(token=token, value=sellValue)
        waitTransaction(12)
        txn = sell(sell=token, get=target, value=sellValue)
        txnStatus = _web3.eth.get_transaction_receipt(txn)

        if txnStatus['status'] == 0:
            print('WARNING SELL FAILED, TRYING WITHOUT FEE SUPPORT')
            txn = sellWithFees(sell=token, get=target, value=sellValue)
            txnStatus = _web3.eth.get_transaction_receipt(txn)
            if txnStatus['status'] == 0:
                print('SELL RETRY FAILED, STRANGE TOKENOMICS ALERT')

        createSellFile(token, priceQuote, sellValue, percentage, _web3.toHex(txn), txnStatus['status'])
        exit(200)

def monitorPrice(target=WBNB_CONTRACT, token=BUSD_CONTRACT, tick=0):
    pairContract = getPairContractCached(target, token)
    reserve0, reserve1, blockTimeStampLast = pairContract.functions.getReserves().call()
    decimals0 = getTokenContract(token).functions.decimals().call()
    token0 = str.lower(pairContract.functions.token0().call());

    global _buy_price
    if _buy_price == "":
        _buy_price = getTokenPaidPrice(token)

    if token0 == WBNB_CONTRACT:
        q = (reserve0 / 10 ** decimals0) / reserve1
        t = q
        print('{:.20f}'.format(q))
    else:
        q = reserve1 / (reserve0 / 10 ** decimals0)
        print('{:.20f}'.format(_web3.fromWei(q, 'ether')))
        t = _web3.fromWei(q, 'ether')

    t += (t / 10) * tick

    print(_buy_price)
    print('{:.20f}'.format(t))
    percentageGrowth = ((t / decimal.Decimal(_buy_price)) - 1) * 100

    if percentageGrowth > 99:
        sellValue = getBalance(SENDER_ADDRESS, token)
        approveSell(token=token, value=sellValue)
        waitTransaction(10)
        sell(sell=token, get=WBNB_CONTRACT, value=sellValue)
        exit(200)

    return True


def getNewTokens():
    with open('tokens.json') as json_file:
        data = json.load(json_file)

    fileIds = []
    for token in data:
        fileIds.append(token['id']);

    global _tokens
    _tokens = getTokens()

    # print(getTokens())
    # exit()
    apiIds = []
    for token in _tokens:
        apiIds.append(token['id']);

    return list(set(apiIds) - set(fileIds))


def getTokenFromList(id):
    for token in _tokens:
        if token['id'] == id:
            return token


def updateTokenMap(tokenInfo):
    f = open("tokens.json", "r")
    x = json.loads(f.read())
    x.append(tokenInfo)
    saveFile(x)


def createBuyFile(time, tokenInfo, buytotal, gas, gas_gwei, txn):
    name = tokenInfo['name']
    symbol = tokenInfo['symbol']
    slug = tokenInfo['slug']
    address = tokenInfo['platform']['token_address']
    quote = tokenInfo['quote']

    print('FOUND NEW TOKEN')
    print(tokenInfo['name'])

    price = getPrice(WBNB_CONTRACT, address)

    print('TOKEN PRICE')
    print(price)

    buyObject = {
        "name": name,
        "symbol": symbol,
        "slug": slug,
        "address": address,
        "price": price,
        "time": time,
        "paid": buytotal,
        "gas": gas,
        "gas_gwei": gas_gwei,
        "server_quote": quote,
        "txn": _web3.toHex(txn),
    }

    filename = 'buy/' + address + '-' + symbol + '.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(buyObject, f, ensure_ascii=False, indent=4)


def main():
    paying = 0.05
    foundNewTokens = True

    # print(getNewTokens())
    # exit

    while foundNewTokens:
        print("Passou 1")
        for tokenId in getNewTokens():
            tokenData = getTokenFromList(tokenId)
            print("Passou")
            txn = buy(
                tokenData['platform']['token_address'],
                WBNB_CONTRACT,
                paying,
                DEFAULT_GAS,
                '5',
            )

            createBuyFile(
                datetime.utcnow().isoformat(),
                tokenData,
                paying,
                DEFAULT_GAS,
                DEFAULT_GAS_GWEI,
                txn
            )

            updateTokenMap(tokenData)

        timetoexec = 5

        nextTime = datetime.now() + timedelta(minutes=timetoexec)

        print('Next Round ' + str(nextTime))
        time.sleep(60 * timetoexec)


def getBalance(address=SENDER_ADDRESS, token=WBNB_CONTRACT):
    if token == WBNB_CONTRACT:
        return _web3.eth.get_balance(SENDER_ADDRESS)
    else:
        token_contract = _web3.eth.contract(_web3.toChecksumAddress(token), abi=ERC20_ABI)
    return token_contract.functions.balanceOf(address).call()


def waitTransaction(seconds=10):
    print("esperando por " + str(seconds) + " segundos")
    time.sleep(seconds)


def getNonce():
    _web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
    #  print('Version web3' + _web3.eth.blockNumber)
    global _last_nonce
    if _last_nonce != 0:
        _last_nonce += 1
        print("nonce ->" + str(_last_nonce))
        return _last_nonce
    else:
        _last_nonce = _web3.eth.get_transaction_count(SENDER_ADDRESS)
        print("nonce ->" + str(_last_nonce))
        return _last_nonce


def getPairContract(address):
    return _web3.eth.contract(address=address, abi=PCPAIR_ABI)


def getFactoryContract():
    return _web3.eth.contract(address=PCSW_FACTORY_CONTRACT, abi=PCSW_FACTORY_ABI)


def getRouterContract():
    return _web3.eth.contract(address=PCSW_CONTRACT, abi=PCSW_ABI)


def getTokenContract(token=BUSD_CONTRACT):
    return _web3.eth.contract(address=_web3.toChecksumAddress(token), abi=ERC20_ABI)

def getTokenContractFee(token=BUSD_CONTRACT):
    return _web3.eth.contract(address=_web3.toChecksumAddress(token), abi=ERC20_FEE_ABI)


def getBalances(folder='buy/', forced=False):
    path_to_json = folder
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for contract in json_files:
        with open(folder + contract) as f:
            data = json.load(f)

        if not forced:
            if 'balance' in data:
                continue

        address = contract.split('-')[0]
        balance = getBalance(SENDER_ADDRESS, address)
        a_dict = {'balance': balance}
        data.update(a_dict)

        print(data['name'] + ' balance is ' + str(balance))

        with open(folder + contract, 'w') as f:
            json.dump(data, f, indent=4)


def approveSell(token=BUSD_CONTRACT, value=0, gas=250000, gas_price='5'):
    if value == 0:
        return False

    txn = getTokenContract(token).functions.approve(getRouterContract().address, value).buildTransaction({
        'from': SENDER_ADDRESS,
        'nonce': getNonce(),
        'gas': gas,
        'gasPrice': _web3.toWei(gas_price, 'gwei'),
    })

    txnID = _web3.eth.send_raw_transaction(
        _web3.eth.account.sign_transaction(txn, private_key=HEXDATA).rawTransaction
    )

    print('approved')
    print('approve https://bscscan.com/tx/' + _web3.toHex(txnID))
    waitTransaction(10)

    return True


def sell(sell=BUSD_CONTRACT, get=WBNB_CONTRACT, value=0, gas=250000, gas_wei='5'):
    txn = getRouterContract().functions.swapExactTokensForETH(
        value,
        0,
        [_web3.toChecksumAddress(sell), _web3.toChecksumAddress(get)],
        SENDER_ADDRESS,
        (int(time.time()) + 10000)
    ).buildTransaction({
        'from': SENDER_ADDRESS,
        'gas': gas,
        'gasPrice': _web3.toWei(gas_wei, 'gwei'),
        'nonce': getNonce(),
    })

    txnID = _web3.eth.send_raw_transaction(
        _web3.eth.account.sign_transaction(txn, private_key=HEXDATA).rawTransaction
    )

    print('sell https://bscscan.com/tx/' + _web3.toHex(txnID))

    return txnID


def sellWithFees(sell=BUSD_CONTRACT, get=WBNB_CONTRACT, value=0, gas=350000, gas_wei='6'):
    txn = getRouterContract().functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
        value,
        0,
        [_web3.toChecksumAddress(sell), _web3.toChecksumAddress(get)],
        SENDER_ADDRESS,
        (int(time.time()) + 10000)
    ).buildTransaction({
        'from': SENDER_ADDRESS,
        'gas': gas,
        'gasPrice': _web3.toWei(gas_wei, 'gwei'),
        'nonce': getNonce(),
    })

    txnID = _web3.eth.send_raw_transaction(
        _web3.eth.account.sign_transaction(txn, private_key=HEXDATA).rawTransaction
    )

    waitTransaction(12)

    print('sell https://bscscan.com/tx/' + _web3.toHex(txnID))
    return txnID


def buy(buy=BUSD_CONTRACT, using=WBNB_CONTRACT, value=0.0, gas=DEFAULT_GAS, gas_wei=DEFAULT_GAS_GWEI):
    if value == 0:
        print("Passou 2")
        return False

    txn = getRouterContract().functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        0,  # 20295708854660 set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
        [_web3.toChecksumAddress(using), _web3.toChecksumAddress(buy)],
        SENDER_ADDRESS,
        (int(time.time()) + 10000)
    ).buildTransaction({
        'from': SENDER_ADDRESS,
        'value': _web3.toWei(value, 'ether'),  # This is the Token(BNB) amount you want to Swap from
        'gas': gas,
        'gasPrice': _web3.toWei(gas_wei, 'gwei'),
        'nonce': getNonce(),
    })
    txnID = _web3.eth.send_raw_transaction(
        _web3.eth.account.sign_transaction(txn, private_key=HEXDATA).rawTransaction
    )
    print(_web3.toHex(txnID))

    return txnID


def cleanBuy():
    folder = 'buy/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def seller(token, limitSell=70):
    pairContract = getPairContractCached(WBNB_CONTRACT, token)
    decimals0 = getTokenContract(token).functions.decimals().call()
    token0 = str.lower(pairContract.functions.token0().call());

    global _buy_price
    if _buy_price == "":
        _buy_price = getTokenPaidPrice(token)

    while True:
        priceWatcher(decimals0, token0, pairContract, WBNB_CONTRACT, token, limitSell)
        time.sleep(5)

if __name__ == "__main__":
    print('Sniffer alpha v0a')

    if len(sys.argv) > 1:
        if sys.argv[1] == '-b':
            getBalances()
        if sys.argv[1] == '-bf':
            getBalances(folder='buy/', forced=True)
        elif sys.argv[1] == '-s':
            token = sys.argv[2]
            limitSell = sys.argv[3]
            seller(token, limitSell)
        elif sys.argv[1] == '-bt':
            token = sys.argv[2]
            #tx = buy(token, WBNB_CONTRACT, 0.0027,700000,'6')

            #trying fee detection
            fee = getTokenContractFee('0xc1168b7b85b2bbc8a5c73c007b74e7523b2da209').functions._burne().call()
            print(fee)
            #token_symbol1 = token_contract1.functions.symbol().call()
            #print('sell https://bscscan.com/tx/' + _web3.toHex(tx))
        elif sys.argv[1] == '-st':
            token = sys.argv[2]
            total = getBalance(SENDER_ADDRESS, token)
            approveSell(token, total)
            tx = sellWithFees(sell=token, get=WBNB_CONTRACT, value=total, gas=350000, gas_wei='6')
        elif sys.argv[1] == '-cbsure':
            nextTime = datetime.now() + timedelta(minutes=15)
            print(nextTime)
    else:
        main()
# python sniffer -b
# python sniffer.py -s 0x3a23f43aaed213209a6143cb91a00674caa767e6 100
# 0.000045979142745243 TIKI

# 0.00000000000000000454000