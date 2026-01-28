#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
诊断脚本 - 测试 AKShare 连接和可用函数
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import json
import sys

def test_network():
    """测试网络连接"""
    print("=" * 80)
    print("网络连接测试")
    print("=" * 80)

    # 测试1: 简单的股票数据获取
    print("\n测试1: 获取上证指数数据...")
    try:
        df = ak.stock_zh_index_spot()
        print(f"✓ 成功获取 {len(df)} 条数据")
        print("前5条数据:")
        print(df.head())
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def get_concept_list_direct():
    """直接获取概念列表"""
    print("\n" + "=" * 80)
    print("尝试获取概念板块列表")
    print("=" * 80)

    # 尝试东方财富概念板块
    print("\n1. stock_board_concept_name_em (东方财富概念板块)")
    try:
        df = ak.stock_board_concept_name_em()
        print(f"✓ 成功! {len(df)} 个概念板块")
        print(df.head())
        return df, "concept_em"
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 尝试东方财富行业板块
    print("\n2. stock_board_industry_name_em (东方财富行业板块)")
    try:
        df = ak.stock_board_industry_name_em()
        print(f"✓ 成功! {len(df)} 个行业板块")
        print(df.head())
        return df, "industry_em"
    except Exception as e:
        print(f"✗ 失败: {e}")

    return None, None

def get_sample_stocks():
    """获取样例成分股"""
    print("\n" + "=" * 80)
    print("测试获取成分股")
    print("=" * 80)

    # 使用已知的概念板块代码
    test_codes = [
        ("BK0729", "5G概念"),
        ("BK0481", "新能源汽车"),
        ("BK0450", "人工智能"),
    ]

    for code, name in test_codes:
        print(f"\n测试: {name} ({code})")
        try:
            stocks = ak.stock_board_concept_cons_em(symbol=code)
            print(f"✓ 成功获取 {len(stocks)} 只成分股")
            print(stocks.head(3))
        except Exception as e:
            print(f"✗ 失败: {e}")

if __name__ == "__main__":
    print(f"AKShare 版本: {akshare.__version__}")
    print(f"时间: {datetime.now()}")

    # 测试网络
    if not test_network():
        print("\n⚠ 网络连接可能存在问题")
        print("请检查:")
        print("1. 网络连接是否正常")
        print("2. 是否需要配置代理")
        print("3. 防火墙设置")
        sys.exit(1)

    # 获取概念列表
    concept_df, source = get_concept_list_direct()
    if concept_df is None:
        print("\n无法获取概念板块列表")
        sys.exit(1)

    # 获取样例成分股
    get_sample_stocks()

    print("\n" + "=" * 80)
    print("诊断完成")
    print("=" * 80)
