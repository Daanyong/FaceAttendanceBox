from flask import Flask, jsonify, render_template
import mysql.connector
import csv
from datetime import date

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='xxx.xxx.xxx.xxx',
        user='xxxx',
        password='xxxxxxxx',
        database='attendance'
    )

# 학생 정보를 DB에 추가하고 기본 출결 상태를 '결석'으로 설정하는 함수
def add_students_to_db(file_path, subject):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        today = date.today()

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                name = row[0].strip()  # 학생 이름 (CSV 파일의 첫 번째 열)

                # 이름이 비어있지 않을 경우 추가
                if name:
                    # 학생이 이미 있는지 확인
                    check_query = f"SELECT * FROM {subject} WHERE name = %s AND date = %s"
                    cursor.execute(check_query, (name, today))
                    result = cursor.fetchone()

                    if not result:
                        # 해당 학생이 없으면 기본 상태 '결석'으로 추가
                        insert_query = f"INSERT INTO {subject} (name, date, status) VALUES (%s, %s, %s)"
                        cursor.execute(insert_query, (name, today, 'no'))
                        print(f"{name}의 기본 출결 정보가 {subject} 테이블에 추가되었습니다.")

        connection.commit()

    except mysql.connector.Error as err:
        print(f"에러: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 출석 정보를 업데이트하는 함수
def save_attendance_to_db(subject, name, status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        today = date.today()

        check_query = f"SELECT * FROM {subject} WHERE name = %s AND date = %s"
        cursor.execute(check_query, (name, today))
        result = cursor.fetchone()

        if result:
            update_query = f"UPDATE {subject} SET status = %s WHERE name = %s AND date = %s"
            cursor.execute(update_query, (status, name, today))
            print(f"{name}의 출결 정보가 {subject} 테이블에서 업데이트되었습니다.")
        else:
            insert_query = f"INSERT INTO {subject} (name, date, status) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name, today, status))
            print(f"{name}의 출결 정보가 {subject} 테이블에 저장되었습니다.")

        connection.commit()

    except mysql.connector.Error as err:
        print(f"에러: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 텍스트 파일에서 이름을 읽어와 출결을 저장
def process_attendance(file_path, subject):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            name = line.strip()
            if name:
                save_attendance_to_db(subject, name, 'yes')

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT name, date, status FROM algorithm"
        cursor.execute(query)
        results = cursor.fetchall()

        return render_template('result.html', attendances=results)

    except mysql.connector.Error as err:
        return f"Database error: {err}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # 1. 모든 학생의 기본 출결 정보를 'no' 상태로 DB에 추가
    csv_file_path = 'students.csv'
    subject = 'algorithm'
    add_students_to_db(csv_file_path, subject)

    # 2. 출결 정보를 업데이트
    attendance_file_path = 'result.txt'
    process_attendance(attendance_file_path, subject)

    app.run(host='0.0.0.0', port=5000, debug=True)
