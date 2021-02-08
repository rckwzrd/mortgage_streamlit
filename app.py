import streamlit as st
import helper
import explore_monthly_payment

def main():
    st.title('Mortgage Modeler')
    data = dict()

    mode = st.sidebar.selectbox("Select Mode", ["Detailed Buy/Sell", "Explore Monthly Payment"])
    if mode == "Detailed Buy/Sell":
        st.sidebar.subheader("Detailed Buy Home")
        data = helper.buy_input(data)
        data = helper.total_payment(data)
        helper.buy_output(data)
        
        st.sidebar.subheader('Sell Home')
        data = helper.sell_input(data)
        data = helper.sell_cost(data)
        helper.sell_output(data)

        data = helper.comparison(data)
        helper.compare_output(data)

        st.write(data)

    elif mode == "Explore Monthly Payment":
        st.sidebar.subheader("Explore Monthly Payment")
        data = explore_monthly_payment.buy_input(data)
        st.subheader(f"Home price = ${data['home']:.2f}")
        data = explore_monthly_payment.model_monthly_payments(data)
        explore_monthly_payment.plot_payments(data)

        st.write(data)


if __name__ == '__main__':
    main()

