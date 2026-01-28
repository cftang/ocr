#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用 AKShare 多数据源获取概念板块及成分股数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import json
import time
import sys
import os

def get_all_concept_stocks():
    """
    获取所有概念板块及成分股 - 使用多个数据源
    """
    print("=" * 80)
    print("开始获取概念板块及成分股数据...")
    print("=" * 80)

    data_source = "东方财富"

    if os.path.exists("concept_boards1.csv"):
        concept_df = pd.read_csv("concept_boards1.csv", encoding="utf-8-sig")
    else:
        concept_df = ak.stock_board_concept_name_em()
        concept_df.to_csv("concept_boards1.csv", index=False, encoding="utf-8-sig")

    # 获取成分股
    print("\n获取成分股...")
    print(f"总板块数: {len(concept_df)}")

    existing_codes = set()
    output_file = "concept_stocks1.csv"
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file, usecols=['板块代码'], dtype={'板块代码': str})
            existing_codes = set(existing_df['板块代码'].astype(str))
            print(f"已存在 {len(existing_codes)} 个板块的数据，将跳过。")
        except Exception as e:
            print(f"读取现有文件失败 (将重新获取): {e}")

    all_concept_stocks = {}
    success_count = 0
    fail_count = 0

    for idx, row in concept_df.iterrows():
        # 获取板块代码和名称
        if '板块代码' in row:
            concept_code = str(row['板块代码'])
            concept_name = row['板块名称']
        else:
            # 尝试其他可能的字段名
            concept_code = str(row.get('symbol', row.get('code', row.get('id', idx))))
            concept_name = row.get('name', row.get('板块名称', f'板块{idx}'))

        if concept_code in existing_codes:
            # print(f"路过: {concept_name} ({concept_code})")
            continue

        try:
            print(f"[{idx+1}/{len(concept_df)}] {concept_name}...")

            # 根据数据源选择获取方法
            if data_source == "东方财富":
                stocks_df = ak.stock_board_concept_cons_em(symbol=concept_code)
            elif data_source == "东方财富行业":
                stocks_df = ak.stock_board_industry_cons_em(symbol=concept_code)
            else:
                stocks_df = None

            if stocks_df is not None and len(stocks_df) > 0:
                # 添加板块信息
                stocks_df['板块名称'] = concept_name
                stocks_df['板块代码'] = concept_code
                
                # 根据股票代码前缀添加市场标识 (SH/SZ/BJ)
                stocks_df['代码'] = stocks_df['代码'].apply(lambda x: 
                    'SH' + x if x.startswith(('60', '68', '90')) else 
                    'SZ' + x if x.startswith(('30', '00')) else 
                    'BJ' + x if x.startswith('92') else x)

                # 立即追加保存
                header = not os.path.exists(output_file)
                stocks_df.to_csv(output_file, mode='a', index=False, header=header, encoding="utf-8-sig")

                all_concept_stocks[concept_name] = {
                    'code': concept_code,
                    'count': len(stocks_df),
                    'stocks': [] # 不占用内存，已保存
                }
                print(f"✓ {concept_code} {concept_name} {len(stocks_df)} 只")
                success_count += 1
            else:
                print("✗ 无数据")
                fail_count += 1

            time.sleep(0.5)

        except Exception as e:
            print(f"✗ {str(e)[:50]}")
            fail_count += 1
            time.sleep(1)

    # 保存数据
    # (已在循环中增量保存)
    print(f"✓ 数据已增量保存到 {output_file}")

    # 统计
    print("\n" + "=" * 80)
    print("统计报告")
    print("=" * 80)
    print(f"本次获取: {len(all_concept_stocks)} 个板块")
    print(f"成功: {success_count}, 失败: {fail_count}")
    print(f"成分股总数: {sum(d['count'] for d in all_concept_stocks.values())}")
    print(f"平均每板块: {sum(d['count'] for d in all_concept_stocks.values()) / len(all_concept_stocks):.1f} 只")
    print("=" * 80)

    return all_concept_stocks

if __name__ == "__main__":
    try:
        import akshare
        print(f"AKShare 版本: {akshare.__version__}")
    except ImportError:
        print("错误: 请先安装: pip install akshare openpyxl")
        sys.exit(1)

    data = get_all_concept_stocks()
    if data:
        print("\n✓ 成功获取数据!")
    else:
        print("\n✗ 获取数据失败!")
