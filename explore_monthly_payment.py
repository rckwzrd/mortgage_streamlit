import streamlit as st
import numpy as np
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


def buy_input(data: dict):
    data['home'] = st.sidebar.number_input('Home Value:', value=350000.0, step=10000.0, format='%.2f')
    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')

    data['tax'] = st.sidebar.number_input('Yearly Tax:',value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insurance'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12 
    return data


def model_monthly_payments(data: dict):
    house_price = data["home"]
    rate = data["rate"]
    tax = data["tax"]
    hoa = data["hoa"]
    insurance = data["insurance"]

    term = float(30 * 12)
    periodic_rate = (1+rate)**(1/12) - 1

    dp = np.arange(0.0, 100000, 5000)
    loan = house_price - dp
    mp = np.zeros(dp.shape)

    for i in range(len(dp)):
        mp[i] = -1*np.pmt(periodic_rate, term, loan[i])

    total_mp = mp + tax + hoa + insurance

    df = pd.DataFrame({
        "loan": loan,
        "dp": dp,
        "mp": mp,
        "total_mp": total_mp
        }
    )

    data["monthly_payments"] = df

    return data


def plot_payments(data: dict):
    df = data["monthly_payments"]
    source = ColumnDataSource(data=df)

    TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"

    p = figure(tools=TOOLS)
    p.xaxis.axis_label = "Down Payment ($)"
    p.yaxis.axis_label = "Monthly Pyament ($)"

    p.line("dp", "mp", source=source)
    p.circle("dp", "mp", source=source)
    p.hover.tooltips = [
            ('down payment', '$@dp{0.2f}'),
            ('monthly payment',  '$@mp{0.2f}')
    ]

    # hover = HoverTool(
    #     tooltips=[
    #         ('down payment', '$@dp{%0.2f}'),
    #         ('monthly payment',  '$@mp{%0.2f}')
    #     ],
    #     mode='vline'
    # )

    # p.add_tools(hover)

    st.bokeh_chart(p, use_container_width=True)



