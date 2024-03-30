# Prices is an aarray where prices[i] is the price of a given stock on the ith day.
# I want to maximize my profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
# Returns the maximum profit I can achieve from this transaction. If I cannot achieve any profit, return 0.

def max_profit(prices:list) -> int:
    if len(prices) < 2:
        return 0
    min_price = prices[0]
    max_profit = 0
    for price in prices[1:]:
        if price < min_price:
            min_price = price 
        profit = price - min_price
        if profit > max_profit:
            max_profit = profit
    return max_profit
