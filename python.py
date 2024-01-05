from flask import Flask, render_template, request
import csv
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename='flask_errors.log', level=logging.ERROR)

template= "./template"
appointments_csv = "./appointments.csv"
app = Flask(__name__, template_folder=template)


def save_to_csv(name, date, time):
    try:
        print(f"Before writing to CSV: {appointments_csv}")
        print(f"Name: {name}, Date: {date}, Time: {time}")

        with open(appointments_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, date, time])

        print("Successfully wrote to CSV")
    except FileNotFoundError:
        print(f"Error: CSV file not found at path: {appointments_csv}")
    except PermissionError:
        print(f"Error: Permission issue. Check if the script has write access to the CSV file.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def check_time_conflict(new_time, existing_time):
    new_start, new_end = parse_time_interval(new_time)
    existing_start, existing_end = parse_time_interval(existing_time)
    print(f"New start: {new_start}, New end: {new_end}")
    return new_start < existing_end and new_end > existing_start

def parse_time_interval(time_string):
    start_time = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
    end_time = start_time + timedelta(hours=1)
    return start_time, end_time


@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def book_appointment():
    try:
        if request.method == 'POST':
            name = request.form['name']
            date = request.form['date']
            time = request.form['time']
            
            # Check if the selected date is not in the past
            current_date = datetime.now()
            selected_date = datetime.strptime(date, '%Y-%m-%d')

            if selected_date < current_date:
                return "Please select a future date."

            # Check for time conflicts
            with open(appointments_csv, mode='r') as file:
                reader = csv.reader(file)
                print(f"Checking for time conflicts for {date} {time}")
                for row in reader:
                    existing_date_time = f"{row[1]} {row[2]}"
                    print(f"Checking against: {existing_date_time}")
                    if check_time_conflict(f"{date} {time}", existing_date_time):
                        print("Time conflict found")
                        return "Error: Two appointments cannot coincide within one hour."
                    else: 
                        print("No time conflicts found")
            # Save to CSV if all checks pass
            print("Saving to CSV")
            save_to_csv(name, date, time)
            return "Appointment booked successfully!"
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

    return render_template('newappoi.html')
@app.route('/home')
def wow():
    return render_template('landing2.html')
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')
if __name__ == '__main__':
    app.run(debug=True, port=8001)
