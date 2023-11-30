from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text
from rasa_sdk.events import SlotSet
import mysql.connector

class ActionGetCarList(Action):
    def name(self) -> Text:
        return "action_get_car_list"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 사용자의 예산 정보를 가져옵니다.
        user_budget = float(tracker.get_slot("user_budget"))
        if user_budget is None:
            dispatcher.utter_message(text="I can't find budget.")
            return []

        user_budget = float(user_budget)
        
        # MySQL 데이터베이스 연결 설정
        db_config = {
            'user': 'root',
            'password': 'porsche-718',
            'host': 'localhost',
            'port': '3306',
            'database': 'cardb'
        }
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 예산 범위에 해당하는 차량 조회를 위한 쿼리 작성
        query = f"SELECT * FROM Car WHERE Price <= {user_budget}"

        # 쿼리 실행
        cursor.execute(query)

        # 조회한 차량 목록을 담을 리스트 생성
        car_list = []

        # 각 차량 정보를 리스트에 추가
        for row in cursor.fetchall():
            car_id = row[0]
            manufacturer = row[1]
            origin = row[2]
            model_name = row[3]
            car_type = row[4]
            price = row[5]
            fuel_type = row[6]

            car_info = f"Car ID: {car_id}\nManufacturer: {manufacturer}\nOrigin: {origin}\nModel Name: {model_name}\nCar Type: {car_type}\nPrice: {price}\nFuel Type: {fuel_type}"
            car_list.append(car_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 차량 목록을 챗봇으로 전송
        if car_list:
            car_list_message = "\n".join(car_list)
            dispatcher.utter_message(text=f"List of cars within the budget:\n\n{car_list_message}")
        else:
            dispatcher.utter_message(text="There are no vehicles within the budget.")

        return []
