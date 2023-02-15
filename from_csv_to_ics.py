import pandas as pd
import os

# Función para convertir la tabla de Pandas en eventos
def df_to_events(df):
    events = []
    for i, row in df.iterrows():
        event = {}
        for key, value in row.items():
            event[key] = value
        events.append(event)
    return events


# Función para escribir los eventos en un archivo ICS
def write_events_to_ics(events, file_name):
    with open(file_name, 'w') as file:
        file.write('BEGIN:VCALENDAR\n')
        file.write('VERSION:2.0\n')
        for event in events:
            file.write('BEGIN:VEVENT\n')
            for key, value in event.items():
                file.write(f'{key}:{value}\n')
            file.write('END:VEVENT\n')
        file.write('END:VCALENDAR\n')


def change_date_format(df):
    for col in df.columns:
        if col.startswith("DT"):
            df[col] = pd.to_datetime(df[col]).dt.strftime("%Y%m%dT%H%M%SZ")
    return df


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


# Leer la tabla de Pandas desde el archivo CSV
df = pd.read_csv('file.csv', encoding="ISO-8859-1")
df = change_date_format(df)

# Llamar a las funciones para transformar la tabla de Pandas en un archivo ICS
events = df_to_events(df)
delete_file('calendar.ics')
write_events_to_ics(events, 'calendar.ics')
