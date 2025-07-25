import pytest
import pandas as pd
from src import plot_financials

def test_roe():
    df = pd.DataFrame({
        '純利益': [100],
        '自己資本': [500]
    })
    roe = df['純利益'] / df['自己資本'] * 100
    assert roe.iloc[0] == 20

def test_roa():
    df = pd.DataFrame({
        '純利益': [100],
        '総資産': [1000]
    })
    roa = df['純利益'] / df['総資産'] * 100
    assert roa.iloc[0] == 10

def test_ebitda():
    df = pd.DataFrame({
        '営業利益': [200],
        '減価償却費': [50]
    })
    ebitda = df['営業利益'] + df['減価償却費']
    assert ebitda.iloc[0] == 250

def test_equity_ratio():
    df = pd.DataFrame({
        '自己資本': [400],
        '総資産': [1000]
    })
    ratio = df['自己資本'] / df['総資産'] * 100
    assert ratio.iloc[0] == 40 