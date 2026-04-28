import os
import csv
import json

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print("File found: students.csv")
            return True
        else:
            print("Error: students.csv not found.")
            return False

    def create_output_folder(self):
        print("Checking output folder...")
        if not os.path.exists("output"):
            os.makedirs("output")
            print("Output folder created: output/")
        else:
            print("Output folder already exists: output/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("\nLoading data...")
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.students = list(reader)
            print("Data loaded successfully:", len(self.students), "students")
            return self.students
        except:
            print("Error loading data.")
            return []

    def preview(self, n=5):
        if not self.students:
            return
        print("\nFirst", n, "rows:")
        print("-" * 30)
        for i in range(min(n, len(self.students))):
            s = self.students[i]
            print(s['student_id'], "|", s['age'], "|", s['gender'], "|",
                  s['country'], "| GPA:", s['GPA'])
        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        gpas = []
        high_performers = 0

        for student in self.students:
            try:
                gpa = float(student['GPA'])
                gpas.append(gpa)
                if gpa > 3.5:
                    high_performers = high_performers + 1
            except:
                continue

        if not gpas:
            return {}

        self.result = {
            "total_students": len(self.students),
            "average_gpa": round(sum(gpas) / len(gpas), 2),
            "max_gpa": max(gpas),
            "min_gpa": min(gpas),
            "high_performers": high_performers
        }
        return self.result

    def print_results(self):
        print("\n" + "-" * 30)
        print("GPA Analysis")
        print("-" * 30)
        if not self.result:
            print("No data")
            return
        print("Total students :", self.result["total_students"])
        print("Average GPA :", self.result["average_gpa"])
        print("Highest GPA :", self.result["max_gpa"])
        print("Lowest GPA :", self.result["min_gpa"])
        print("Students GPA>3.5 :", self.result["high_performers"])
        print("-" * 30)


class ResultSaver:
    def __init__(self, result):
        self.result = result

    def save_json(self):
        try:
            with open("output/result.json", 'w', encoding='utf-8') as f:
                data = {"analysis": "GPA Statistics"}
                data.update(self.result)
                json.dump(data, f, indent=4)
            print("\nResult saved to output/result.json")
        except:
            print("Error saving JSON")




def lambda_map_filter_demo(students):
    print("\n" + "-" * 30)
    print("Lambda / Map / Filter")
    print("-" * 30)

    high_gpa = list(filter(lambda s: float(s['GPA']) > 3.8, students))
    print("GPA > 3.8 :", len(high_gpa))

    gpa_values = list(map(lambda s: float(s['GPA']), students))
    print("GPA values (first 5) :", gpa_values[:5])

    hard_workers = list(filter(lambda s: float(s.get('study_hours_per_day', 0)) > 4, students))
    print("study_hours_per_day > 4 :", len(hard_workers))




def main():
    fm = FileManager("students.csv")
    if not fm.check_file():
        return
    fm.create_output_folder()

    dl = DataLoader("students.csv")
    dl.load()
    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result)
    saver.save_json()


    lambda_map_filter_demo(dl.students)

    print("\nВсе части Practice 4, 5 и 6 выполнены!")


if __name__ == "__main__":
    main()