import json
from ..feature.exam.exam_api import Exam, ExamCreateReq
from ..database import SessionLocal
from ..envConfig import Config
import os


def load_jsons():
    current_directory = os.getcwd()
    print(current_directory)
    files = [
        # current_directory+"/app/fixtures/exam_spring_2024.json",
        # current_directory+"/app/fixtures/exam_2024.json",
        # current_directory+"/app/fixtures/exam_2024_3.json"
        # current_directory
        # + "/app/fixtures/notion_temp.json"
        current_directory + "/app/fixtures/menu_wine_exam.json",
        current_directory + "/app/fixtures/warenannahme_lagerkennzahlen_exam.json",
        current_directory + "/app/fixtures/bedarfsermittlung_exam.json",
    ]

    print(Config.DATABASE_URL)
    for file_name in files:
        with open(file_name, "r") as json_file:
            print("Open file:", file_name)
            data = json.load(json_file)
            Exam.create(ExamCreateReq(**data), SessionLocal())


if __name__ == "__main__":
    load_jsons()
