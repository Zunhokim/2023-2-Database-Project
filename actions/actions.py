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
        user_carType = tracker.get_slot("user_carType")
        user_engine = tracker.get_slot("user_engine")

        # 입력 정보가 DB에 없을 경우, 조건에 맞는 차량이 없다는 메시지 출력. 
        if user_budget is None:
            dispatcher.utter_message(text="There is no vehicle that meets the criteria.")
            return []
        elif user_origin is None:
            dispatcher.utter_message(text="There is no vehicle that meets the criteria.")
            return []
        elif user_brand is None:
            dispatcher.utter_message(text="There is no vehicle that meets the criteria.")
            return []

        # 슬롯에서 가져온 입력값을 변수에 저장하기
        user_budget = int(user_budget)
        user_origin = str(user_origin).capitalize()
        user_brand = str(user_brand)
        user_carType = str(user_carType)
        user_engine = str(user_engine)
        
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
        # 예산 범위는 15% 내외로 설정.
        lower_bound = user_budget * 0.85
        upper_bound = user_budget * 1.15

        query = f"SELECT * FROM Car WHERE Price >= {lower_bound} AND Price <= {upper_bound} AND Origin = '{user_origin}' AND Manufacturer LIKE '%{user_brand}%' AND CarType LIKE = '{user_carType}' AND FuelType LIKE = '{user_engine}'"

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
            CarType = row[4]
            price = row[5]
            FuelType = row[6]

            car_info = f"Brand: {manufacturer} | Origin: {origin} | Model Name: {model_name} | Car Type: {CarType} | Price: {price} | Fuel Type: {FuelType}"
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
