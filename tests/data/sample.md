The CTA policy template provides complete signal generation and delegation management functions, and users can develop their own strategies based on the template. The new policy can be placed in the file that the user runs (recommended), such as creating the strategies folder in the c:\users\administrator.vntrader directory; it can be placed in the vnpy\app\cta_strategy\strategies folder in the root directory.
note: The policy file naming is an underscore mode, such as boll_channel_strategy.py; and the strategy class naming is a camel, such as BollChannelStrategy.

The following is a demonstration of the strategy development steps through the BollChannelStrategy policy example:

### parameter settings

Define policy parameters and initialize policy variables. The policy parameter is a public property of the policy class. The user can call or change the policy parameter by creating a new instance.

For the rb1905 variety, users can create a BollChannelStrategy-based policy example, such as RB_BollChannelStrategy, boll_window can be changed from 18 to 30.

The method of creating a policy instance effectively implements a strategy to run multiple varieties, and its policy parameters can be adjusted by the characteristics of the variety.
```
    Boll_window = 18
    Boll_dev = 3.4
    Cci_window = 10
    Atr_window = 30
    Sl_multiplier = 5.2
    Fixed_size = 1

    Boll_up = 0
    Boll_down = 0
    Cci_value = 0
    Atr_value = 0

    Intra_trade_high = 0
    Intra_trade_low = 0
    Long_stop = 0
    Short_stop = 0
```

### Class initialization
initialization is divided into 3 steps:
- Inherit CTA policy template by super() method, pass CTA engine, policy name, vt_symbol, parameter setting in __init__() function.
- Call the K-line generation module: synthesize Tick data into 1 minute K-line data by time slicing, and then larger time period data, such as 15-minute K-line.
- Call the K-line time series management module: based on K-line data, such as 1 minute, 15 minutes, to generate the corresponding technical indicators.