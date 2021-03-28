import sqlite3
from openpyxl import load_workbook
import openpyxl

wb = load_workbook('attendance.xlsx')
sheet = wb["Sheet1"]
sheet.delete_rows(2, 10)
print("deleted")
wb.save('attendance.xlsx')

global conn, cursor
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
try:
    cursor.execute("delete from student;")
    print("delete data")
except sqlite3.Error as error:
    print("Failed to delete data into sqlite table", error)
finally:
    conn.commit()
    cursor.close()
    print("Sqlite3 connection closed")