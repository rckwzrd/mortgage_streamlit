import streamlit as st

import numpy as np
import pandas as pd

import plotly.graph_objects as go

def buy_input(data: dict):
    h1 = st.sidebar.number_input('Home 1:', value=300000.0, step=10000.0, format='%.2f')
    h2 = st.sidebar.number_input('Home 2:', value=350000.0, step=10000.0, format='%.2f')
    h3 = st.sidebar.number_input('Home 3:', value=400000.0, step=10000.0, format='%.2f')
    data['home'] = [h1, h2, h3]

    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    data['tax'] = st.sidebar.number_input('Yearly Tax:',value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insr'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12 

    return data


def model_payments(data: dict):
    hp = data["home"]
    rate = data["rate"]
    tax = data["tax"]
    hoa = data["hoa"]
    insr = data["insr"]

    term = float(30 * 12)
    periodic_rate = (1+rate)**(1/12) - 1

    dp = np.arange(0.0, 100000, 10000)
    payments = {"down": dp}

    for h in hp:
        mp = np.zeros(dp.shape)

        for i in range(len(dp)):
            loan = h - dp[i]
            mp[i] = -1*np.pmt(periodic_rate, term, loan)

        mp = mp + tax + hoa + insr

        payments[f"{str(int(h))}"] = mp

    data["payments"] = pd.DataFrame(payments)

    return data


def plot_payments(data: dict):
    df = data["payments"]

    fig = go.Figure()

    for col in df.columns.values.tolist():

        if col != "down":
            trace = go.Scatter(
                x=df["down"],
                y=df[col],
                name=col,
                hovertemplate=f"{col}<extra></extra>"
            )

            fig.add_trace(trace)

    st.plotly_chart(fig)