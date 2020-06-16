# Testnet trade generator

This small script can be used to generate trade on [spot testnet](https://testnet.binance.vision)

## How it works
- fetch all symbols
- query the last price from production site
- generate trade in testnet
- validate the trade amount

## How to run

```python

# install package
pip install -r requirements.txt


KEY=xxxxx SECRET=xxxxxx python generator.py

```

## Maybe issue

This script is not smart enough to adjust the order qty automatically based on balance. So you might see account balance insufficient error.

```shell
> show me the money
```

## License

MIT
