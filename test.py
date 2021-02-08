# %%
def model_payments(data:dict):
    # make np array of down payments in thousands
    down_payments = np.arange(0.0, 100000, 1000)
    periodic_rate = (1+data['rate'])**(1/12) - 1
    term = float(30 * 12)
    monthly_payments = -1*np.pmt(data['rate_periodic'], data['term'], data['loan'])

    return data

# %%
import numpy as np
import pandas as pd

def model_monthly_payments():
    house_price = 350000
    rate =0.0325
    tax = 5000
    hoa = 100
    insurance = 1000

    term = float(30 * 12)
    periodic_rate = (1+rate)**(1/12) - 1

    dp = np.arange(0.0, 100000, 1000)
    loan = house_price - dp
    mp = np.zeros(dp.shape)

    for i in range(len(dp)):
        mp[i] = -1*np.pmt(periodic_rate, term, loan[i])

    total_mp = mp + tax + hoa + insurance

    merged = np.column_stack((loan, dp, mp, total_mp))
    print(merged.shape)
    df = pd.DataFrame(
        (loan, dp, mp, total_mp), 
        columns=["Loan", "Down_Pay", "Prnpl_Int", "Total"]
    )
    print(df.info())


model_monthly_payments()


# %%

# %%
