import json
import csv_handler
import os

def convert():
    json_file = "usuarios.json"
    csv_file = "usuarios.csv"
    
    if not os.path.exists(json_file):
        print(f"El archivo {json_file} no existe.")
        return

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if csv_handler.save_csv(csv_file, data):
            print(f"Conversión exitosa: {csv_file} creado con {len(data)} registros.")
        else:
            print("Error al guardar el archivo CSV.")
            
    except Exception as e:
        print(f"Error durante la conversión: {e}")

if __name__ == "__main__":
    convert()
