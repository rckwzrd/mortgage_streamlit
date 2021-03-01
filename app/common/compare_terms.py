import streamlit as st

import numpy as np
import numpy_financial as npf
import pandas as pd

def input_terms(data: dict):
    data['home'] = st.sidebar.number_input('Home Value:', value=350000.0, step=10000.0, format='%.2f')
    data['down'] = st.sidebar.number_input('Downpayment:', value=50000.0, step=5000.0, format='%.2f')
    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')

    return data


def model_terms(data: dict):
    hp = data['home']
    dp = data['down']
    rate = data['rate']

    loan = hp - dp
    data["loan"] = loan
    periodic_rate = (1+rate)**(1/12) - 1

    terms = np.arange(5, 35, 5)
    principal = np.full(terms.shape, loan)
    interest = np.zeros(terms.shape)
    total = np.zeros(terms.shape)

    for i in range(len(terms)):
        term = terms[i] * 12
        payment = -1*npf.pmt(periodic_rate, term, loan)
        total[i] = payment * term
        interest[i] = total[i] - loan

    data["terms"] = pd.DataFrame(
        data={
            "term": terms,
            "loan": principal,
            "interest": interest,
            "total": total
        }
    )

    data["terms"] = data["terms"].style.format({
        "term": "{:}yr",
        "loan": "${0:,.0f}",
        "interest": "${0:,.0f}",
        "total": "${0:,.0f}"
    })

    return data


def highlight(df):
    if df["term"] == 30:
        return ['color: red']*4
    elif df["term"] == 15:
        return ['color: blue']*4
    else:
        return ['color: black']*4


def model_output(data):
    st.subheader("Parameters")
    st.text(f"Home Price: ${data['home']}")
    st.text(f"Down Payment: ${data['down']}")
    st.text(f"Loan Principal: ${data['loan']}")
    st.text(f"Interest Rate: {data['rate']}% APR")

    st.subheader("Mortgage Term Payments")
    df = data["terms"].apply(highlight, axis=1)
    st.write(df)
