import pandas as pd
import os

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    
    try:
        df = pd.read_csv(filename)
        # Convertir NaN a None o valores vacíos si es necesario, 
        # pero para compatibilidad con el resto del código, to_dict('records') suele ser suficiente.
        # Sin embargo, pandas infiere tipos, así que 'id' y 'edad' ya deberían ser int si el CSV está limpio.
        return df.to_dict('records')
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        return []

def save_csv(filename, data):
    if not data:
        # Si la lista está vacía, podríamos querer guardar un CSV vacío con cabeceras o no hacer nada.
        # El comportamiento original era retornar False.
        return False
    
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return True
    except Exception as e:
        print(f"Error al guardar CSV: {e}")
        return False
