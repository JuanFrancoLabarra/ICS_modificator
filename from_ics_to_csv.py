import pandas as pd
import os

# Función para extraer los eventos del archivo ICS
def extract_events(file_name):
    events = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        event = {}
        for line in lines:
            if line.startswith('BEGIN:VEVENT'):
                event = {}
            elif line.startswith('END:VEVENT'):
                events.append(event)
                event = {}
            else:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key, value = parts
                    event[key] = value.strip()
    return events



# Función para transformar los eventos en una tabla de Pandas
def events_to_df(events):
    df = pd.DataFrame(events)
    df = change_date_format(df)
    return df

def change_date_format(df):
    for col in df.columns:
        if col.startswith("DT"):
            df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

# Llamar a las funciones para transformar el archivo ICS en una tabla de Pandas
events = extract_events('MiHorario.ics')
df = events_to_df(events)
delete_file('file.csv')
df.to_csv('file.csv', index=False)
