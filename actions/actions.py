# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import algo
import webbrowser


#class ActionSaveName(Action):
#    def name(self) -> Text:
#        return "action_save_name"
#    def run(self, dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        global nam
#        nam = tracker.get_slot('name')
#        print("*************** name saved: ")
#        print(nam)
#        #askWeight = ""
#        dispatcher.utter_message(template="utter_presentation_of_bot",
#                                 Name=nam)
#        return []

class ActionSaveAgeAskWeight(Action):
    def name(self) -> Text:
        return "action_save_age_ask_weight"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ageMsg = str(tracker.latest_message['text'])
        global age
        for s in ageMsg.split():
            if s.isdigit():
                age = s
                break
        print("***********  age")
        print(age)
        if not age:
            age =25
        askWeight = "Perfet, and what's your actual weight in kg?"
        dispatcher.utter_message(text=askWeight)
        return []


class ActionSaveHeight(Action):
    def name(self) -> Text:
        return "action_save_height"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        heightMsg = str(tracker.latest_message['text'])
        global height
        for s in heightMsg.split():
            if s.isdigit():
                height = s
                break
        if not height:
            height = 183
        dispatcher.utter_message()
        return []

class ActionSaveWeightAskHeight(Action):
    def name(self) -> Text:
        return "action_save_weight_ask_height"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        weightMsg = str(tracker.latest_message['text'])
        global weight
        for s in weightMsg.split():
            if s.isdigit():
                weight = s
                break
        if not weight:
            weight = 76
        askHeight = "OK. Now tell me what is your height in cm?"
        dispatcher.utter_message(text=askHeight)
        return []

class ActionSaveGender(Action):
    def name(self) -> Text:
        return "action_save_gender"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global gender
        #user_event = tracker.events[-1]
        #user_event = next(e for e in reversed(tracker.events) if e["event"] == "bot")

        gender = tracker.get_slot('gs')

        print("########### Gender")
        print(gender)
        #gender = str(tracker.latest_message['text'])
        #askWeight = ""
        dispatcher.utter_message(template="utter_asking_effort")
        return []


class ActionSaveActivity(Action):
    def name(self) -> Text:
        return "action_save_effort"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global activity
        activity = tracker.get_slot('as')
        print("########### activity")
        print(activity)
        #gender = str(tracker.latest_message['text'])
        #askWeight = ""
        dispatcher.utter_message(template="action_results")
        return []


class ActionAskingEffort(Action):
    def name(self) -> Text:
        return "action_results"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #age = tracker.get_slot('age')
        print("*****************")
        print(age)
        print(weight)
        print(height)
        print(gender)
        print(activity)
        height_m = float(height)/100.0
        print("########## height en M ###")
        print(height_m)
        BMI = float(weight)/(height_m)**2
        if BMI < 18.5:
            BMI_result = "Underweight"
        elif BMI >= 18.5 and BMI <= 24.9:
            BMI_result = "Healthy Weight"
        elif BMI >= 25.0 and BMI <= 29.9:
            BMI_result = "Overweight"
        else:
            BMI_result = "Obesity"
        print("**********BMI : ****")
        print(BMI)
        if gender == "male":
            IBW = 50 + (0.91 * (float(height)-152.4))
        if gender == "female":
            IBW = 45.5  + (0.91 * (float(height)-152.4))

        #TDEE = algo.calc_tdee("name", float(weight), float(height), int(age), gender, activity)
        #TDEE = float(TDEE)
        #breakfast = algo.bfcalc(TDEE)
        #snack1 = algo.s1calc(TDEE)
        #lunch = algo.lcalc(TDEE)
        #snack2 = algo.s2calc(TDEE)
        #dinner = algo.dcalc(TDEE)
        #snack3 = algo.s3calc(TDEE)


        BMI_last_result = "👉 According to the BMI factor, you are in " + BMI_result + "\n"
        IBW_last_result = "👉 The ideal weight for you is " + str(round(IBW, 2)) + " kg \n"
        #TDEE_last_result = "* A rocommendation meal plan for you : \n -Breakfast: {} \n -Snack1: {} \n -Lunch: {} \n -Snack2: {} \n -Dinner: {} \n -Snack3: {}".format(breakfast, snack1, lunch, snack2, dinner, snack3)

        all_results = BMI_last_result + IBW_last_result
        last_msg= "So after my analysis, below is your report 🧾: \n " + all_results
        dispatcher.utter_message(template="utter_asking_showing_report",
                                 msg=last_msg)
        return []

class ActionMealPlanRec(Action):
    def name(self) -> Text:
        return "action_meal_plan_rec"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #global activity
        #activity = tracker.get_slot('as')
        #print("########### activity")
        #print(activity)
        #gender = str(tracker.latest_message['text'])
        #askWeight = ""
        TDEE = algo.calc_tdee("name", float(weight), float(height), int(age), gender, activity)
        TDEE = float(TDEE)
        breakfast = algo.bfcalc(TDEE)
        snack1 = algo.s1calc(TDEE)
        lunch = algo.lcalc(TDEE)
        snack2 = algo.s2calc(TDEE)
        dinner = algo.dcalc(TDEE)
        snack3 = algo.s3calc(TDEE)
        TDEE_last_result = "A meal plan recommendation for you is : \n ✔Breakfast: {} \n ✔Snack1: {} \n ✔Lunch: {} \n ✔Snack2: {} \n ✔Dinner: {} \n ✔Snack3: {}".format(breakfast, snack1, lunch, snack2, dinner, snack3)

        dispatcher.utter_message(text=TDEE_last_result)
        return []
