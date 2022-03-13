import time
import json

from datetime import date
from pathlib import Path

import robin_stocks.robinhood as rh
import alpaca_trade_api

from environ import Env

from stockze.example_app.utils.tradingview_ta_ratings import tradingview_ta_analysis, tradingview_ta_sell
from stockze.example_app.utils.final_rating import final_rating

env = Env()
ROOT = Path(__file__).resolve(strict=True).parent.parent.parent.parent
testing_bool = env.bool("TESTING", default=True)
alpaca = alpaca_trade_api.REST()

try:
    upcoming_earnings = json.load(open(f"{ROOT}/data/upcoming_earnings.json"))
except:
    upcoming_earnings = {}


def get_cash():
    if not testing_bool:
        cash = float(rh.account.build_user_profile()['cash'])
        time.sleep(float(env('RH_SLEEP')))
    elif testing_bool:
        # alpaca is **very** slow updating wallet so i keep track on my own
        cash = float(json.load(open(f"{ROOT}/data/wallet.json")))
    return cash


def set_testing_cash():
    account = alpaca.get_account()
    cash = float(account.cash)
    json.dump(cash, open(f"{ROOT}/data/wallet.json", "w"))


def get_current_holdings():
    if not testing_bool:
        try:
            current_holdings_dict = rh.account.build_holdings()
            time.sleep(float(env('RH_SLEEP')))
        except:
            current_holdings_dict = {}
    elif testing_bool:
        try:
            current_holdings_dict = {}
            portfolio = alpaca.list_positions()
            for position in portfolio:
                current_holdings_dict[position.symbol] = {
                    "average_buy_price": position.avg_entry_price,
                    "quantity": position.qty,
                    "equity": position.market_value,
                    "equity_change": position.unrealized_pl,
                    "percent_change": position.unrealized_plpc,
                    "price": position.current_price,
                }
            time.sleep(float(env('AL_SLEEP')))
        except:
            current_holdings_dict = {}
    return current_holdings_dict


def projected_winners(max_buys):
    potential_buys = {}
    for ticker in upcoming_earnings:
        print(ticker)
        try:
            upcoming_earnings[ticker]['tradingview_ta'] = tradingview_ta_analysis(
                ticker, upcoming_earnings[ticker]['exchange']
            )
            upcoming_earnings[ticker]['overall_score'] = final_rating(
                upcoming_earnings[ticker]
            )
            potential_buys[ticker] = upcoming_earnings[ticker]
        except:
            pass
    sorted_projected_winners = sorted(
        potential_buys, key=lambda x: (
            potential_buys[x]['overall_score']
        ),
        reverse=True
    )
    return sorted_projected_winners[:max_buys]


def top_movers(grab_len):
    potential_buys = {}
    top_movers_dict = {}
    top_movers_list = rh.markets.get_top_movers()  # len = 20
    time.sleep(float(env('RH_SLEEP')))
    for mover in top_movers_list:
        ticker = mover['symbol']
        print(ticker)
        try:
            top_movers_dict[ticker]['tradingview_ta'] = tradingview_ta_analysis(ticker, exchange=False)
            top_movers_dict[ticker]['overall_score'] = final_rating(ticker)
            potential_buys[ticker] = top_movers_dict[ticker]
        except:
            pass
    sorted_projected_winners = sorted(
        potential_buys, key=lambda x: (
            potential_buys[x]['overall_score']
        ),
        reverse=True
    )
    return sorted_projected_winners[:grab_len]


def profitable_holdings(current_holdings_dict, min_profit):
    profitable_holds = []
    for ticker in current_holdings_dict:
        if bool(float(current_holdings_dict[ticker]['equity_change']) >= min_profit):
            profitable_holds.append(ticker)
    return profitable_holds


def projected_loss_soon(ticker):
    try:
        return tradingview_ta_sell(ticker, upcoming_earnings[ticker]['exchange'])
    except:
        return tradingview_ta_sell(ticker, None)


def earnings_coming_soon(ticker):
    if ticker in upcoming_earnings:
        try:
            return bool(upcoming_earnings[ticker]['date'] == date.today().strftime("Y-%m-%d"))
        except:
            return True
    else:
        return False


def monetary_allocation_experiment_one(buy_list):
    cash = get_cash()
    print('current cash: $', cash)
    return round(float(cash/len(buy_list)))


def monetary_allocation_experiment_two(pie_slicer=0.33):
    cash = get_cash()
    print('current cash: $', cash)
    return round(float(cash*pie_slicer))


def purchasing_power(min_purchase_power=0.10):
    cash = get_cash()
    print('current cash: $', cash)
    return cash >= min_purchase_power
