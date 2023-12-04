from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text
from rasa_sdk.events import SlotSet
import mysql.connector
import random

class SaveSlotValuesAction(Action):
    def name(self) -> Text:
        return "action_save_slot_values"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 슬롯 값 추출
        user_budget = tracker.get_slot("user_budget")
        user_origin = tracker.get_slot("user_origin")
        user_brand = tracker.get_slot("user_brand")
        user_carType = tracker.get_slot("user_carType")
        user_engine = tracker.get_slot("user_engine")

        # 전역 변수에 슬롯 값 저장
        global global_budget, global_origin, global_brand, global_carType, global_engine, global_lower_bound, global_upper_bound
        global_budget = user_budget
        global_origin = user_origin
        global_brand = user_brand
        global_carType = user_carType
        global_engine = user_engine

        # 예산 범위에 해당하는 차량 조회를 위한 전역 변수 설정
        # 예산 범위는 15% 내외로 설정.
        global_lower_bound = int(user_budget) * 0.85
        global_upper_bound = int(user_budget) * 1.15

        return []

class ActionGetCarList(Action):
    def name(self) -> Text:
        return "action_get_list_all"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #전역 변수 참조 구문
        global global_lower_bound, global_upper_bound, global_budget, global_origin, global_brand, global_carType, global_engine
        
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

        query = f"SELECT * FROM Car WHERE Price >= {global_lower_bound} AND Price <= {global_upper_bound} AND Origin = '{global_origin}' AND Manufacturer LIKE '%{global_brand}%' AND CarType LIKE '{global_carType}' AND FuelType LIKE '{global_engine}' ORDER BY Manufacturer ASC, Price ASC"

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
            price = str(row[5])
            FuelType = row[6]

            car_info = "Brand: {:15s} | Origin: {:15s} | Model Name: {:20s} | Car Type: {:15s} | Price: {:15s} | Fuel Type: {:15s}".format(manufacturer, origin, model_name, CarType, price, FuelType)
            car_list.append(car_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 차량 목록을 바로 출력
        if car_list:
            car_list_text = "\n".join(car_list)
            dispatcher.utter_message(text=car_list_text)
            dispatcher.utter_message(text="\n \nWould you like recommendations for other vehicles that meet your budget and domestic/foreign criteria?")
        else:
            dispatcher.utter_message(text="There are no vehicle fits the criteria.\nCan I recommend vehicles that fall within your budget range and meet the domestic/foreign criteria?")

        return []

class ActionGetCarListSpare1(Action):
    def name(self) -> Text:
        return "action_get_list_Budget_andOrigin"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 전역 변수 참조 구문
        global global_lower_bound, global_upper_bound, global_budget, global_origin, global_brand, global_carType, global_engine
        
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

        query = f"SELECT * FROM Car WHERE Price >= {global_lower_bound} AND Price <= {global_upper_bound} AND Origin = '{global_origin}' ORDER BY Manufacturer ASC, Price ASC"

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
            price = str(row[5])
            FuelType = row[6]

            car_info = "Brand: {:15s} | Origin: {:15s} | Model Name: {:20s} | Car Type: {:15s} | Price: {:15s} | Fuel Type: {:15s}".format(manufacturer, origin, model_name, CarType, price, FuelType)
            car_list.append(car_info)


        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 차량 목록을 바로 출력
        if car_list:
            car_list_text = "\n".join(car_list)
            dispatcher.utter_message(text=car_list_text)
            dispatcher.utter_message(text="\n \nShall I show you all the vehicles available within your budget range?")
        else:
            dispatcher.utter_message(text="There are no vehicle fits the criteria.\nShall I recommend vehicles within your budget, even if they do not meet all the criteria?")

        return []

class ActionGetCarListSpare2(Action):
    def name(self) -> Text:
        return "action_get_list_Budget"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 전역 변수 참조 구문
        global global_lower_bound, global_upper_bound, global_budget, global_origin, global_brand, global_carType, global_engine
        
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

        query = f"SELECT * FROM Car WHERE Price <= {global_budget} ORDER BY Manufacturer ASC, Price ASC"

        # 쿼리 실행
        cursor.execute(query)

        # 조회한 차량 목록을 담을 리스트 생성
        car_list = []

        # 각 차량 정보를 리스트에 추가
        for row in random.sample(cursor.fetchall(), k = 10):
            car_id = row[0]
            manufacturer = row[1]
            origin = row[2]
            model_name = row[3]
            CarType = row[4]
            price = str(row[5])
            FuelType = row[6]

            car_info = "Brand: {:15s} | Origin: {:15s} | Model Name: {:20s} | Car Type: {:15s} | Price: {:15s} | Fuel Type: {:15s}".format(manufacturer, origin, model_name, CarType, price, FuelType)
            car_list.append(car_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 차량 목록을 바로 출력
        if car_list:
            car_list_text = "\n".join(car_list)
            dispatcher.utter_message(text=car_list_text)
        else:
            dispatcher.utter_message(text="\n \nPlease check to ensure that the budget is not insufficient.\n")

        return []