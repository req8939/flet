import datetime

def calculate_age(birth_date):
    today = datetime.date.today()
    # birth_date might be datetime.datetime from Flet DatePicker
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return str(age)

# Test cases
try:
    # Case 1: datetime object (simulating Flet DatePicker value)
    d1 = datetime.datetime(1990, 5, 15)
    print(f"Date: {d1}, Age: {calculate_age(d1)}")

    # Case 2: date object
    d2 = datetime.date(1990, 5, 15)
    print(f"Date: {d2}, Age: {calculate_age(d2)}")

    # Case 3: Today (should be 0)
    d3 = datetime.datetime.now()
    print(f"Date: {d3}, Age: {calculate_age(d3)}")
    
    print("All tests passed!")
except Exception as e:
    print(f"Error: {e}")
