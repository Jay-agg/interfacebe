# -*- coding: utf-8 -*-
"""Finance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pydoGTnqcpH9OsAEfYFwt3qLsjM4a5e6
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from schema import Base, Order, Summary, DashboardMetrics

# Create SQLAlchemy engine
engine = create_engine("sqlite:///./finance.db", echo=True)

# Load data into the database
def load_data_to_db():
    # Load Orders
    df.to_sql(Order.__tablename__, engine, if_exists='replace', index=False)

    # Load Summary
    summary_df.to_sql(Summary.__tablename__, engine, if_exists='replace', index=False)

    # Load Dashboard Metrics
    dashboard_metrics = [
        {'metric_name': 'Previous Month Order', 'metric_value': len(df[df['status'] == 'Previous Month Order'])},
        {'metric_name': 'Order & Payment Received', 'metric_value': len(df[df['status'] == 'Order & Payment Received'])},
        {'metric_name': 'Payment Pending', 'metric_value': len(df[df['status'] == 'Payment Pending'])},
        {'metric_name': 'Tolerance rate breached', 'metric_value': 3},  # Placeholder value
        {'metric_name': 'Return', 'metric_value': len(df[df['status'] == 'Return'])},
        {'metric_name': 'Negative Payout', 'metric_value': len(df[df['status'] == 'Negative Payout'])}
    ]
    dashboard_metrics_df = pd.DataFrame(dashboard_metrics)
    dashboard_metrics_df.to_sql(DashboardMetrics.__tablename__, engine, if_exists='replace', index=False)

if __name__ == "__main__":
    """Finance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pydoGTnqcpH9OsAEfYFwt3qLsjM4a5e6
"""
merchant_tax = pd.read_excel('Merchant Tax Report (MTR) Sheet - Hiring.xlsx')

merchant_tax.head()

merchant_tax.info()

merchant_tax.isna().sum()

merchant_tax['Transaction Type'].unique()

merchant_tax = merchant_tax[merchant_tax['Transaction Type'] != 'Cancel']
merchant_tax['Transaction Type'] = merchant_tax['Transaction Type'].replace({'Refund':'Return','FreeReplacement':'Return'})

merchant_tax['Transaction Type'].unique()

payment_report = pd.read_csv('Payment Report Sheet - Hiring - Sheet1.csv')

payment_report.head()

payment_report.isna().sum()

payment_report.info()

payment_report['type'].unique()

payment_report.rename(columns={'type':'Payment Type'},inplace=True)

payment_report.rename(columns={'order id':'Order Id','description':'P_Description','total':'Net Amount'},inplace=True)

payment_report.rename(columns={'date/time':'Payment Date'},inplace=True)

payment_report = payment_report[payment_report['Payment Type'] != 'Transfer\n']

payment_report['Payment Type'] = payment_report['Payment Type'].replace({
    'Adjustment\n': 'Order',
    'FBA Inventory Fee\n': 'Order',
    'Fulfilment Fee Refund': 'Order',
    'Service Fee\n': 'Order',
    'Refund\n': 'Return',
    'Order\n': 'Order'
})

payment_report['Payment Type'].unique()

payment_report['Transaction Type'] = 'Payment'

all_columns = ['Order Id','Transaction Type','Payment Type','Invoice Amount','Net Amount','P_Description','Order Date','Payment Date']
merchant_tax_reindexed = merchant_tax.reindex(columns=all_columns).fillna('')
payment_report_reindexed = payment_report.reindex(columns=all_columns).fillna('')
concatenated_df = pd.concat([merchant_tax_reindexed, payment_report_reindexed],axis=0, ignore_index=True)

concatenated_df.head()

concatenated_df['Net Amount'] = pd.to_numeric(concatenated_df['Net Amount'], errors='coerce')

concatenated_df['P_Description'].unique()

df = concatenated_df.copy()

summary_df = concatenated_df[concatenated_df['Order Id'] !=''].groupby('P_Description')['Net Amount'].sum().reset_index()

summary_df = summary_df.rename(columns={'Net Amount': 'SUM of Net Amount'})

summary_df.drop(index=summary_df[summary_df['SUM of Net Amount'] == 0].index, inplace=True)
summary_df

df['Shipment Invoice Amount'] = df.apply(
    lambda row: row['Invoice Amount'] if row['Transaction Type'] == 'Shipment' else None,
    axis=1
)
df['Payment Net Amount'] = df.apply(
    lambda row: row['Net Amount'] if row['Transaction Type'] == 'Payment' else None,
    axis=1
)

df.replace('', np.nan, inplace=True)

# Removal Order IDs
removal_order_ids = df[df['Order Id'].str.len() == 10]

# Return
return_orders = df[(df['Transaction Type'] == 'Return') & (df['Invoice Amount'].notna())]

# Negative Payout
negative_payout = df[(df['Transaction Type'] == 'Payment') & (df['Net Amount'] < 0)]

# Order & Payment Received
order_payment_received = df[
    df['Order Id'].notna() &
    df['Payment Net Amount'].notna() &
    df['Shipment Invoice Amount'].notna()
]

# Order Not Applicable but Payment Received
order_not_applicable_payment_received = df[
    df['Order Id'].notna() &
    df['Payment Net Amount'].notna() &
    df['Shipment Invoice Amount'].isna()
]

# Payment Pending
payment_pending = df[
    df['Order Id'].notna() &
    df['Shipment Invoice Amount'].notna() &
    df['Payment Net Amount'].isna()
]

removal_order_ids

load_data_to_db()