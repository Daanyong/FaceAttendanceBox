from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import date

app = Flask(__name__)

# CSV 파일에서 출석 정보를 읽어오는 함수
def read_attendance_from_csv(file_path):
    attendance_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row:  # 비어있는 행을 방지
                    name, date, status = row
                    attendance_data.append({'name': name, 'date': date, 'status': status})
    except Exception as e:
        print(f"CSV 파일 읽기 오류: {e}")
    return attendance_data

# 출석 상태를 업데이트하는 함수
def update_attendance_in_csv(file_path, name, status):
    rows = []
    try:
        # CSV 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row:
                    if row[0] == name:  # 이름이 일치하는 경우 출석 상태 업데이트
                        row[2] = status
                    rows.append(row)

        # 업데이트된 데이터를 다시 CSV 파일에 저장
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(rows)
    except Exception as e:
        print(f"CSV 파일 업데이트 오류: {e}")

@app.route('/')
def index():
    # CSV 파일 경로 설정
    csv_file_path = 'students.csv'
    
    # CSV에서 출석 정보 읽어오기
    attendances = read_attendance_from_csv(csv_file_path)

    return render_template('result_professor.html', attendances=attendances)

# 출석 상태를 변경하는 라우트
@app.route('/update_attendance', methods=['POST'])
def update_attendance():
    name = request.form['name']
    status = request.form['status']
    csv_file_path = 'students.csv'
    
    # 출석 상태를 CSV 파일에서 업데이트
    update_attendance_in_csv(csv_file_path, name, status)
    
    # 업데이트 후 다시 출석 결과 페이지로 리다이렉트
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
