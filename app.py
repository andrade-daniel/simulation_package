import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from ftfy import fix_encoding

from src.run_sim.sim_function import Simulation
from src.visualization.plots import *

# '''
# Com base na package Ciw
# '''

# functions
@st.cache(suppress_st_warning = True)
def weird_division(n, d):
    ''' function to avoid warnings for division by zero '''
    return n / d if d else 0

@st.cache(suppress_st_warning = True)
def mean_queue_length(recs, max_sim_time, warm_up_time):
    arrival_time_stamps = [
        (r.arrival_date, r.queue_size_at_arrival + 1)
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    exit_time_stamps = [
        (r.exit_date, r.queue_size_at_departure)
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    time_stamps = arrival_time_stamps + exit_time_stamps + [(0, 0)]
    time_stamps.sort(key=lambda r: r[0])
    numerator = sum(
        [
            time_stamps[i][1] * (time_stamps[i][0] - time_stamps[i - 1][0])
            for i in range(1, len(time_stamps))
            if time_stamps[i][0] > warm_up_time
        ]
    )
    mean_queue_length = numerator / (max_sim_time - warm_up_time)
    return mean_queue_length

img = Image.open('img/logo_ticapp_black_500px.png')

st.sidebar.image(img,
use_column_width=False, width=200)

st.title(fix_encoding('Simulação'))


# sliders

number_of_servers = st.sidebar.slider(fix_encoding('Selecione o nº de mesas'),
0, 100, step=1, value=0)

service_mins_per_server = st.sidebar.slider(fix_encoding('Selecione o tempo médio de serviço (mins)'),
0, 60, step=1, value=0)

arrivals_per_hour = st.sidebar.slider(fix_encoding('Selecione o nº médio de chegadas por hora'),
0, 1000, step=50, value=0)

max_hrs_time = st.sidebar.slider(fix_encoding('Selecione o tempo a simular (hrs)'),
0, 12, step=1, value=0)


params = {
    "number_of_servers": number_of_servers,
    "arrivals_per_hour": arrivals_per_hour,
    "service_mins_per_server": service_mins_per_server,
    #'warm_up_time': 10,
    "max_hrs_time": max_hrs_time,
    "arrival_distribution": "Exponential",
}  # between Exponential, Gamma or Weibull


can_submit = [value for key, value in params.items() if key != 'arrival_distribution' and value != 0]

if can_submit and len(can_submit) == 4:
    number_of_servers_sel = params["arrivals_per_hour"] / (
    params["number_of_servers"] * (60 / params["service_mins_per_server"])
)
    submit = st.sidebar.button('Correr simulação!')
else:
    submit = None
    st.write('Comece por selecionar os parâmetros')

if submit:

    total_nr_servers = np.arange(1, 101)

    if not can_submit:
        st.write('Selecione parâmetros!')
    else:
        for s in total_nr_servers:
            tt = params["arrivals_per_hour"] / (s * (60 / params["service_mins_per_server"]))
            if tt < 1:
                break

        if params["number_of_servers"] < s and params['max_hrs_time'] > 0:
            
            warning_msg =  f"AVISO: Aumente o número de mesas, de forma a obter um sistema estável. \nMantendo os restantes parâmetros constantes, o número mínimo de mesas deverá ser: {s}."
        else:
            warning_msg = None

        if warning_msg:
            st.write(warning_msg)
            st.write(f"Neste momento, existem {round(number_of_servers_sel, 3)} vezes mais cidadãos a chegar do que a sair do sistema.")
            st.write("Significa que o sistema teria uma fila que cresce infinitamente, tornando-se maior quanto maior for o tempo de simulação, levando a um aumento dos tempos de espera.")

    # Set simulation parameters
    sim = Simulation(**params)

    # Run simulation!
    if 0 not in can_submit:
        with st.spinner('Aguarde um pouco...'):
            Q = sim.simulate_waiting_time()

    st.subheader('Resultados')
    
    # Extract simulation results
    server_busy_time = Q.transitive_nodes
    recs = Q.get_all_records()

    # filter warm-up time of t mins
    # if sim.number_of_servers > 1:
    #     warm_up_time = 60
    # else:
    #     warm_up_time = 0

    # warm_up_time = 60
    warm_up_time = 1
    # cooldown = sim.max_hrs_time*60 - 1
    cooldown = 11
    recs = [r for r in recs if r.arrival_date > warm_up_time and r.arrival_date < cooldown]
    # recs = [r for r in recs]

    waits = [
        r.waiting_time
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    # waits = [r.waiting_time for r in recs]
    waits = [k * 60 for k in waits]
    average_waits = weird_division(sum(waits), len(waits))


    # extract results

    servicetimes = [
        r.service_time * 60
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    
    mean_service_time = weird_division(sum(servicetimes), len(servicetimes))
    enddates = [
        r.service_end_date
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    startdates = [
        r.service_start_date
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    queue_sizes_at_arrival = [
        r.queue_size_at_arrival
        for r in recs
        if r.arrival_date > warm_up_time and r.arrival_date < cooldown
    ]
    completed_custs = len([r for r in recs if r.arrival_date < cooldown])


    # Plot results
    plot_params = {
        k: params[k]
        for k in params.keys()
        if k in ["number_of_servers", "arrivals_per_hour"]
    }
    
    if len(waits) == 0:
        st.write('Aumente o número de horas para simulação (> 1 hora)!')
    elif len(waits) > 0:
        st.table(pd.DataFrame({'Cidadãos servidos por hora': np.floor(60/sim.service_mins_per_server),
        'Tempo médio de espera (mins)': round(average_waits, 2),
        'Tempo máximo de espera (mins)': round(np.max(waits), 2),
        'Utilização Sistema (recomendado < 0.8)': [
            round(k.server_utilisation, 2)
            for k in server_busy_time
        ][0],
        'Cidadãos servidos': completed_custs}, index=['']))

    # plot_waiting_mean(waits, average_waits, mean_service_time, **plot_params)
    st.header('Distribuição tempos espera')
    
    plot_waiting_mean(waits, average_waits)

    st.pyplot()
    plt.clf()

    # Plot queue sizes
    queue_sizes_at_arrival = [r.queue_size_at_arrival for r in recs if r.arrival_date > warm_up_time and r.arrival_date < cooldown]
    
    st.header('Tamanho da fila em cada chegada')
    st.line_chart(queue_sizes_at_arrival, height=2)
    # pd.Series(queue_sizes_at_arrival).plot()
    # # plt.title(f'Tamanho da fila em cada chegada')
    # st.pyplot()
    plt.clf()

    st.success('Concluído!')

submit_extra = st.button('Parabéns TicAPP!')
if submit_extra:
    st.balloons()
