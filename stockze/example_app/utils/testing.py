from environ import Env

from stockze.example_app.utils.crawl_earnings_whispers import CrawlEarningsWhispers
from stockze.example_app.utils.stockze_main import stockze_main

env = Env()

def test_one():
    CrawlEarningsWhispers()
    stockze_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    stockze_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    stockze_main(
        buy_time=False, hold_time=False, sell_time=True
        )

def test_two():
    CrawlEarningsWhispers()
    stockze_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    stockze_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    stockze_main(
        buy_time=False, hold_time=False, sell_time=True
        )

def test_three():
    stockze_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    stockze_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    stockze_main(
        buy_time=False, hold_time=False, sell_time=True
        )


def test_four():
    stockze_main(
        buy_time=True, hold_time=False, sell_time=False
        )
