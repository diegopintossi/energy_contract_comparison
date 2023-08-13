"""
Tool to compare the costs from two gas & electricity contracts.
"""

import streamlit as st

st.title('Energy contracts comparison')

with st.sidebar:
    nr_contracts = st.radio('Number of contracts to be compared:', [2, 3, 4])
    names = []
    for i in range(nr_contracts):
        names.append(st.text_input(f'Supplier {i+1} name:'))
    gas_consumption = st.slider(
        'Indicate the yearly gas consumption [m3]:', 0, 2500
    )
    electricity_consumption_norm = st.slider(
        'Indicate the yearly electricity consumption (normal) [kWh]:', 0, 3500
    )
    electricity_consumption_low = st.slider(
        'Indicate the yearly electricity consumption (low) [kWh]:', 0, 3500
    )
    solar_panels = st.radio('Solar panels:', ['Yes', 'No'])
    if solar_panels == 'Yes':
        teruglevering = st.slider(
            'Indicate the yearly electricity fed into the grid [kWh]:', 0, 4000
        )
    else:
        teruglevering = 0


def contract_input_output(column, name):
    """
    Function storing the sequence of commands related to all inputs and outputs
    for each contract to be compared.
    """
    with column:
        st.markdown(f'#### {name}')
        # INPUTS
        st.divider()
        st.markdown('##### GAS')
        gas_EUR_m3 = st.number_input(
            'Price per m3', 0.0, 2.5, step=0.001, value=1.25,
            key=f'GAS_price_m3_{column}'
        )
        gas_EUR_fixed = st.number_input(
            'Fixed monthly price', 0.0, 12.5, step=0.001, value=5.99,
            key=f'GAS_price_fixed_{column}'
        )
        st.divider()
        st.markdown('##### ELECTRICITY')
        electr_EUR_kWh_high = st.number_input(
            'Price per kWh (high)', 0.0, 2.5, step=0.001, value=0.40,
            key=f'ELECTR_price_kWh_high_{column}'
        )
        electr_EUR_kWh_low = st.number_input(
            'Price per kWh (high)', 0.0, 2.5, step=0.001, value=0.38,
            key=f'ELECTR_price_kWh_low_{column}'
        )
        electr_EUR_fixed = st.number_input(
            'Fixed monthly price', 0.0, 12.5, step=0.001, value=5.99,
            key=f'ELECTR_price_fixed_{column}'
        )
        teruglevering_EUR_kWh = st.number_input(
            'Price per kWh (PV generation)', 0.0, 2.5, step=0.001, value=0.08,
            key=f'ELECTR_price_PV_{column}'
        )
        
        # OUTPUTS
        st.divider()

        total_gas_bill = 240.17 + 12 * gas_EUR_fixed + gas_consumption * gas_EUR_m3
        st.metric(
            label='Total yearly gas costs:',
            value=f'{total_gas_bill:.2f} €'
        )

        total_electric = electricity_consumption_norm + electricity_consumption_low
        excess_PV = max(0, teruglevering - total_electric)
        PV_saldering = min(total_electric, teruglevering)
        high_electr_ratio = electricity_consumption_norm / total_electric if total_electric > 0 else 1
        net_electr_norm = max(0, electricity_consumption_norm - high_electr_ratio * PV_saldering)
        net_electr_low = max(0, electricity_consumption_norm - (1 - high_electr_ratio) * PV_saldering)
        total_electric_bill = 346.39 - 596.86 + 12 * electr_EUR_fixed \
                        + net_electr_norm * electr_EUR_kWh_high \
                        + net_electr_low * electr_EUR_kWh_low \
                        - excess_PV * teruglevering_EUR_kWh
        st.metric(
            label='Total yearly electricity costs:',
            value=f'{total_electric_bill:.2f} €'
        )
        
        st.divider()
        total = total_electric_bill + total_gas_bill
        st.metric(
            label='Total yearly energy costs:',
            value=f'{total:.2f} €'
        )
        monthly = total / 12
        st.metric(
            label='Monthly payment:',
            value=f'{monthly:.2f} €'
        )


if nr_contracts == 2:
    col1, col2 = st.columns(nr_contracts)
    with col1:
        contract_input_output(col1, names[0])
    with col2:
        contract_input_output(col2, names[1])
elif nr_contracts == 3:
    col1, col2, col3 = st.columns(nr_contracts)
    with col1:
        contract_input_output(col1, names[0])
    with col2:
        contract_input_output(col2, names[1])
    with col3:
        contract_input_output(col3, names[2])
else:
    col1, col2, col3, col4 = st.columns(nr_contracts)
    with col1:
        contract_input_output(col1, names[0])
    with col2:
        contract_input_output(col2, names[1])
    with col3:
        contract_input_output(col3, names[2])
    with col4:
        contract_input_output(col4, names[3])
