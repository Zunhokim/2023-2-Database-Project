from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text
from rasa_sdk.events import SlotSet
import mysql.connector

class ActionGetCarList(Action):
    def name(self) -> Text:
        return "action_get_car_list"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 사용자의 입력 정보를 가져옵니다.
        user_budget = tracker.get_slot("user_budget")
        user_origin = tracker.get_slot("user_origin")
        user_brand = tracker.get_slot("user_brand")

        if user_budget is None:
            dispatcher.utter_message(text="There is no vehicle that meets the criteria.")
            return []
        elif user_origin is None:
            dispatcher.utter_message(text="There is no vehicle that meets the criteria.")
            return []
        elif user_brand is None:
            dispatcher.utter_message(text="There is no vehicle that meets the criteria.")
            return []

        user_budget = int(user_budget)
        user_origin = str(user_origin).capitalize()
        user_brand = str(user_brand)
        
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
        lower_bound = user_budget * 0.85
        upper_bound = user_budget * 1.15

        query = f"SELECT * FROM Car WHERE Price >= {lower_bound} AND Price <= {upper_bound} AND Origin = '{user_origin}' AND cturer LIKE '%{user_brand}%'"

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

            car_info = f"Brand: {manufacturer} | Origin: {origin} | Model Name: {model_name} | Car Type: {car_type} | Price: {price} | Fuel Type: {fuel_type}"
            car_list.append(car_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 차량 목록을 바로 출력
        if car_list:
            car_list_text = "\n".join(car_list)
            dispatcher.utter_message(text=car_list_text)
        else:
            dispatcher.utter_message(text="There are no vehicle fits the criteria.")

        return []
