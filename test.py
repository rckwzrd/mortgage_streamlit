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

def model_monthly_payments(data):

    house_price = float(350000)
    rate = 0.0325
    term = float(30 * 12)
    periodic_rate = (1+rate)**(1/12) - 1

    down_payments = np.arange(0.0, 100000, 1000)
    loan_amount = house_price - down_payments
    monthly_payments = np.zeros(down_payments.shape)

    for i in range(len(down_payments)):
        monthly_payments[i] = -1*np.pmt(periodic_rate, term, loan_amount[i])
        print(monthly_payments[i])

    data["down_payments"] = down_payments
    data["monthly_payments"] = monthly_payments

    return data

# %%
