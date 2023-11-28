# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# from rasa_sdk import Tracker
# from rasa_sdk.events import SlotSet
# from rasa_sdk.executor import CollectingDispatcher
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action

# class ActionSaveUserName(Action):

#   def name(self) -> Text:
#     return "action_save_user_name"

#   async def run(
#     self,
#     dispatcher: CollectingDispatcher,
#     tracker: Tracker,
#     domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#     user_name = tracker.latest_message['text']
#     return [SlotSet("user_name", user_name)]

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text

import mysql.connector

class ActionGetCarList(Action):
    def name(self) -> Text:
        return "action_get_car_list"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 사용자의 예산 정보를 가져옵니다.
        user_budget = float(tracker.get_slot("budget"))
        if user_budget is None:
            dispatcher.utter_message(text="예산 정보를 찾을 수 없습니다.")
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
            dispatcher.utter_message(text=f"예산 내의 차량 목록:\n\n{car_list_message}")
        else:
            dispatcher.utter_message(text="예산 내에 해당하는 차량이 없습니다.")

        return []
