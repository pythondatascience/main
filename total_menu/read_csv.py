import csv

csv_file_path = "menu_student.csv"

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # Read the first row (header)

    first_column_values = [row[4] for row in reader] #row[0] -> 첫번쨰 열을 읽음

print("첫 번째 열의 값:")
print(first_column_values)
