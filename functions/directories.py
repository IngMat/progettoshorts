import os
import datetime as dt


def weekly_directory(path):
    # Trova la data di oggi
    oggi = dt.datetime.now()

    days_shift = 7 - oggi.weekday()
    # Calcola il prossimo lunedì e la prossima domenica
    prossimo_lunedi = oggi + dt.timedelta(days=days_shift)
    prossima_domenica = prossimo_lunedi + dt.timedelta(days=6)

    # Formatta le date in un formato accettabile per i nomi delle cartelle
    lunedi_str = prossimo_lunedi.strftime('%Y-%m-%d')
    domenica_str = prossima_domenica.strftime('%Y-%m-%d')

    # Crea il nome della cartella
    nome_cartella = f'PostsDal{lunedi_str}al{domenica_str}'

    # Crea il percorso completo della cartella
    percorso_cartella = os.path.join(path, nome_cartella)

    # Crea la cartella
    os.makedirs(percorso_cartella, exist_ok=True)

    return percorso_cartella


def daily_directory(numero, percorso_base):
    # Mappa i numeri ai giorni della settimana
    giorni_settimana = {1: 'Lunedì', 2: 'Martedì', 3: 'Mercoledì', 4: 'Giovedì', 5: 'Venerdì', 6: 'Sabato', 7: 'Domenica'}

    # Trova la data di oggi
    oggi = dt.datetime.now()
    days_shift = (6+numero) - oggi.weekday()
    # Calcola il giorno della prossima settimana corrispondente al numero
    giorno_prossima_settimana = oggi + dt.timedelta(days=days_shift)

    # Formatta la data in un formato accettabile per i nomi delle cartelle
    giorno_str = giorno_prossima_settimana.strftime('%Y-%m-%d')

    # Crea il nome della cartella
    nome_cartella = f'PostDi{giorni_settimana[numero]}{giorno_str}'

    # Crea il percorso completo della cartella
    percorso_cartella = os.path.join(percorso_base, nome_cartella)

    # Crea la cartella
    os.makedirs(percorso_cartella, exist_ok=True)

    # Ritorna il percorso completo della cartella
    return percorso_cartella


def check_upper_directory(name):
    # Ottieni il percorso alla cartella padre
    parent_dir = os.path.dirname(os.getcwd())

    # Percorso alla cartella "input_video" che è una sottocartella della cartella padre
    directory = os.path.join(parent_dir, name)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory
