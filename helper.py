def checkCoin(pair):
    if 'upusdt' in pair.lower():
        return False
    elif 'downusdt' in pair.lower():
        return False
    else: return True

coin='BTCDOWNUSDT'

print(checkCoin(coin))
