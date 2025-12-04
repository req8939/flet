import csv
import os

def load_csv(filename):
    data = []
    if not os.path.exists(filename):
        return data
    
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convertir tipos si es necesario (ej. id y edad a int)
                if 'id' in row:
                    row['id'] = int(row['id'])
                if 'edad' in row:
                    row['edad'] = int(row['edad'])
                if 'fecha_nacimiento' in row:
                    row['fecha_nacimiento'] = row['fecha_nacimiento'].split('T')[0]
                data.append(row)
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
    
    return data

def save_csv(filename, data):
    if not data:
        return False
    
    try:
        fieldnames = list(data[0].keys())
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error al guardar CSV: {e}")
        return False
