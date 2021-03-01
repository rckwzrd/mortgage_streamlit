import streamlit as st

import numpy as np
import numpy_financial as npf
import pandas as pd


def buy_input(data: dict):
    h1 = st.sidebar.number_input('Home 1:', value=275000.0, step=10000.0, format='%.2f')
    h2 = st.sidebar.number_input('Home 2:', value=325000.0, step=10000.0, format='%.2f')
    h3 = st.sidebar.number_input('Home 3:', value=350000.0, step=10000.0, format='%.2f')
    data['home'] = [h1, h2, h3]

    data['term'] = st.sidebar.number_input('Term:', value=30, step=5)
    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    data['tax'] = st.sidebar.number_input('Yearly Tax:', value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insr'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12

    return data


def model_payments(data: dict):
    hp = data["home"]
    rate = data["rate"]
    tax = data["tax"]
    hoa = data["hoa"]
    insr = data["insr"]
    term = float(data["term"] * 12)

    periodic_rate = (1+rate)**(1/12) - 1

    dp = np.arange(0.0, 110000, 10000)
    payments = {"DOWN_PMT": dp}

    for h in hp:
        mp = np.zeros(dp.shape)

        for i in range(len(dp)):
            loan = h - dp[i]
            mp[i] = -1*npf.pmt(periodic_rate, term, loan)

        mp = mp + tax + hoa + insr

        payments[f"{str(int(h))}"] = mp

    data["payments"] = pd.DataFrame(payments)

    return data


def highlight(df):
    if df["DOWN_PMT"] == 50000:
        return ['color: blue']*4
    else:
        return ['color: black']*4


def model_output(data):
    st.subheader("Home List Prices:")
    st.text(f"Home 1: ${data['home'][0]}")
    st.text(f"Home 2: ${data['home'][1]}")
    st.text(f"Home 3: ${data['home'][2]}")

    st.subheader("Parameters")
    st.text(f"Term: {data['term']} years")
    st.text(f"Interest Rate: {data['rate']}% APR")
    st.text(f"Tax: ${data['tax']*12} per year")
    st.text(f"HOA: ${data['hoa']} per month")
    st.text(f"Insurance: ${data['insr']:.2f} per month")

    st.subheader("Payment Range")
    df = data["payments"]
    st.write(df.style.apply(highlight, axis=1).format("${0:,.0f}"))

    st.subheader("Payment Difference")
    diff_df = pd.DataFrame(df.diff().mean().abs()).T
    st.write(diff_df.style.format("${0:,.0f}"))
