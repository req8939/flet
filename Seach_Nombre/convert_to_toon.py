
import json
import toon_handler

def convert():
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if toon_handler.save_toon("usuarios.toon", data):
            print("Conversion successful: usuarios.json -> usuarios.toon")
        else:
            print("Conversion failed.")
            
    except FileNotFoundError:
        print("usuarios.json not found.")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    convert()
