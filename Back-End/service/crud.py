# crud.py
from datetime import date
import re
from Models.models import sights, client1, food,transport,accomdation1
from typing import List, Dict, Any
from DAO.schemas import SightSchema, clientIn 
from sqlalchemy import String, and_, or_, select, text 
from fastapi import status 
from DAO.db import database 
from helper.helper import ReplacePrice,parse_db_time_string,combine_with_date,matching,normalize_text
valid_trains={
    "Visakhapatnam":"VSKP",
    "Tirupathi":"TPTY",
    "Hyderabad":"SC"
}

async def clientSave(cl: clientIn):
    reference_date = date.today()
    query = client1.insert().values(
        cId=cl.cId,
        cName=cl.cName,
        cSrc=cl.cSrc,
        cDes=cl.cDes,
        cTotalDays=cl.cTotalDays,
        cBudget=cl.cBudget,
        cNsightseeing=cl.cNsightseeing,
        cTravelPrf=cl.cTravelPrf,
        cBusType=cl.cBusType,
        cTrainCoach=cl.cTrainCoach,
        cTravelStartTime=combine_with_date(cl.cTravelStartTime, reference_date),
        cTravelEndTime=combine_with_date(cl.cTravelEndTime, reference_date),
        cReturnTravelPrf=cl.cReturnTravelPrf,
        cReturnBusType=cl.cReturnBusType,
        cReturnTrainCoach=cl.cReturnTrainCoach,
        cReturnTravelStartTime=combine_with_date(cl.cReturnTravelStartTime, reference_date),
        cReturnTravelEndTime=combine_with_date(cl.cReturnTravelEndTime, reference_date),
        cAccomodationPrf=cl.cAccomodationPrf,
        cLowType=cl.cLowType,
        cFoodSug=cl.cFoodSug,
        cFoodChoice=cl.cFoodChoice
    )
    return await database.execute(query)

async def getTransportPlan(cl: clientIn):
    outbound_filtered_by_time_and_type = [] 
    return_filtered_by_time_and_type = []

    # --- Outbound (source to destination) ---
    if cl.cTravelPrf == "Bus":
        outbound_base_conditions = [
            transport.c.Tsrc == cl.cSrc,
            transport.c.Tdes == cl.cDes,
            transport.c.TypeofRoute == cl.cTravelPrf+"-Route"
        ]
        q1 = select(transport).where(and_(*outbound_base_conditions))
        all_outbound_records = await database.fetch_all(q1)
        if all_outbound_records:
            for rec_dict in all_outbound_records:
                rec = dict(rec_dict) 
                passes_time_filter = True 
            
                db_dep_time_str = rec.get("Tdepa")
                db_dep_time = parse_db_time_string(db_dep_time_str)

                if db_dep_time is None: 
                    if cl.cTravelStartTime or cl.cTravelEndTime: 
                        passes_time_filter = False 
                else:
                    if cl.cTravelStartTime:
                        if db_dep_time < cl.cTravelStartTime:
                            passes_time_filter = False
                    if passes_time_filter and cl.cTravelEndTime:
                        if db_dep_time > cl.cTravelEndTime:
                            passes_time_filter = False
            
                if not passes_time_filter:
                    continue 
                passes_type_filter = True 
                if cl.cBusType:
                    if not matching(str(rec.get("Ttype","")), cl.cBusType):
                        passes_type_filter = False
            
                if passes_type_filter:
                    outbound_filtered_by_time_and_type.append(rec)
    else:
        if cl.cSrc in valid_trains and cl.cDes in valid_trains:
            short_src = valid_trains[cl.cSrc]
            short_des = valid_trains[cl.cDes]
            outbound_base_conditions = [
                transport.c.Tsrc == short_src,
                transport.c.Tdes == short_des,
                transport.c.TypeofRoute == cl.cTravelPrf+"-Route"
            ]
            q1 = select(transport).where(and_(*outbound_base_conditions))
            all_outbound_records = await database.fetch_all(q1)

            if all_outbound_records:
                for rec_dict in all_outbound_records:
                    rec = dict(rec_dict) 
                    passes_time_filter = True 
                    passes_type_filter = True 
                    db_dep_time_str = rec.get("Tdepa")
                    db_dep_time = parse_db_time_string(db_dep_time_str) 

                    if db_dep_time is None: 
                        if cl.cTravelStartTime or cl.cTravelEndTime: 
                            passes_time_filter = False
                    else:
                        if cl.cTravelStartTime:
                            if db_dep_time < cl.cTravelStartTime:
                                passes_time_filter = False
                        if passes_time_filter and cl.cTravelEndTime: 
                            if db_dep_time > cl.cTravelEndTime:
                                passes_time_filter = False
                    if passes_time_filter and passes_type_filter:
                        rec["Tprice"] =ReplacePrice(rec.get("Tprice"),cl.cTrainCoach)
                        outbound_filtered_by_time_and_type.append(rec)
        else:
            outbound_filtered_by_time_and_type.append("Train Details not found as per destination")

    # --- Return (destination to source) ---

    if cl.cReturnTravelPrf == "Bus":
        return_base_conditions = [
            transport.c.Tsrc == cl.cDes,
            transport.c.Tdes == cl.cSrc,
            transport.c.TypeofRoute == cl.cReturnTravelPrf+"-EnRoute"
        ]
        q2 = select(transport).where(and_(*return_base_conditions))
        all_return_records = await database.fetch_all(q2)

        
        if all_return_records:
            for rec_dict in all_return_records:
                rec = dict(rec_dict)
                passes_time_filter = True
                db_dep_time_str = rec.get("Tdepa")
                db_dep_time = parse_db_time_string(db_dep_time_str)

                if db_dep_time is None: 
                    if cl.cReturnTravelStartTime or cl.cReturnTravelEndTime: 
                        passes_time_filter = False 
                else:
                    if cl.cReturnTravelStartTime:
                        if db_dep_time < cl.cReturnTravelStartTime:
                            passes_time_filter = False
                    if passes_time_filter and cl.cReturnTravelEndTime:
                        if db_dep_time > cl.cReturnTravelEndTime:
                            passes_time_filter = False

                if not passes_time_filter:
                    continue

            # 2. Bus Type Filtering (Python)
                passes_type_filter = True
                if cl.cReturnBusType:
                    if not matching(str(rec.get("Ttype","")), cl.cReturnBusType):
                        passes_type_filter = False
            
                if passes_type_filter:
                    return_filtered_by_time_and_type.append(rec)
    else:
        if cl.cSrc in valid_trains and cl.cDes in valid_trains:
            short_src = valid_trains[cl.cSrc]
            short_des = valid_trains[cl.cDes]
            return_base_conditions = [
                transport.c.Tsrc == short_des,
                transport.c.Tdes == short_src,
                transport.c.TypeofRoute == cl.cReturnTravelPrf+"-EnRoute"
            ]
            q2 = select(transport).where(and_(*return_base_conditions))
            all_return_records = await database.fetch_all(q2)

            return_filtered_by_time_and_type = [] 

            if all_return_records:
                for rec_dict in all_return_records:
                    rec = dict(rec_dict) # 
                    passes_time_filter = True 
                    passes_type_filter = True 
                    db_dep_time_str = rec.get("Tdepa") 
                    db_dep_time = parse_db_time_string(db_dep_time_str) 

                    if db_dep_time is None:
                        if cl.cReturnTravelStartTime or cl.cReturnTravelEndTime: 
                            passes_time_filter = False
                    else:
                        if cl.cReturnTravelStartTime: 
                            if db_dep_time < cl.cReturnTravelStartTime:
                                passes_time_filter = False
                        if passes_time_filter and cl.cReturnTravelEndTime: 
                            if db_dep_time > cl.cReturnTravelEndTime:
                                passes_time_filter = False
                    if passes_time_filter and passes_type_filter:
                        rec["Tprice"] =ReplacePrice(rec.get("Tprice"),cl.cReturnTrainCoach)
                        return_filtered_by_time_and_type.append(rec)
        else:
           return_filtered_by_time_and_type.append("Train Details not found as per destination")


    outbound_data = outbound_filtered_by_time_and_type
    return_data = return_filtered_by_time_and_type
    has_outbound_data = bool(outbound_data) 
    has_return_data = bool(return_data)   
    Route_details=[]
    Enroute_details=[]

    if has_outbound_data and has_return_data:
        final_len = min(len(outbound_data), len(return_data))
        Route_details=(outbound_data[:final_len])
        Enroute_details=(return_data[:final_len])
    elif has_outbound_data:
        Route_details.extend(outbound_data)
        Enroute_details="No Details found for Return requirements"
    elif has_return_data:
        Enroute_details.extend(return_data)
        Route_details="No Details found for Route Requirements"
    else:
       Route_details="No Details found for Route Requirements"
       Enroute_details="No Details found for Return requirements"

    return Route_details,Enroute_details

    
    
async def get_processed_sightseeing_data(nsights:int,place:str,initial_price=10000):
        query = sights.select().where(sights.c.sDes ==place)
        results = await database.fetch_all(query)
        actual_count = len(results)
        if nsights == 0:
            return {
                "message": "No sightseeing data available for the given destination."
            }
        limited_results = results[:nsights] if nsights > 0 else results
        return {"sight seeing ":limited_results}
        

        
async def get_processed_food(loc: str, suggest: int, choice: str):
    if not suggest: 
        return {"message": "Food suggestion is not required by client.", "filtered_food": []}

    if not choice: 
        return {"message": "Food choice (Veg/Non-Veg) not specified by client.", "filtered_food": []}

    query = food.select().where(food.c.fAdd == loc)
    results = await database.fetch_all(query)

    if not results:
        return {"message": f"No food records found for location '{loc}'.", "filtered_food": []}

    matched_records = []
    normalized_client_choice = choice.strip().upper()

    for item_row in results:
        item_dict = dict(item_row) 
        db_food_item_string = item_dict.get("fItem", "") 
        match = re.search(r'\((.*?)\)', db_food_item_string)
        if match:
            db_food_type = match.group(1).strip().upper()

            type_matches = False
            if normalized_client_choice == "VEG":
                if db_food_type == "V":  
                    type_matches = True
            elif normalized_client_choice == "NON-VEG":
                if db_food_type == "NV": 
                    type_matches = True

            if type_matches:
                matched_records.append(item_dict)

    if matched_records:
        return {"filtered_food": matched_records}
    else:
        if normalized_client_choice == "VEG":
            message = f"No food items marked with '(V)' found at location '{loc}' for your selection."
        elif normalized_client_choice == "NON-VEG":
            message = f"No food items marked with '(NV)' found at location '{loc}' for your selection."
        else:
            message = f"No food records found for your specific choice '{choice}' at location '{loc}'."
        return {"message": message, "filtered_food": []}

async def get_accomdation_Low_Medium_High(place:str,acc:str):
    if acc=="Low":
        new_acc="Low-Budget"
    elif acc == "Medium":
        new_acc = "Medium-Budget"
    else:
        new_acc = "High-Budget"

    query = accomdation1.select().where(
        accomdation1.c.aDes == place,   
        accomdation1.c.aHoteltype == new_acc
    )
    res = await database.fetch_all(query)

    if not res:
        return {"message": f"No Acc records found for location '{place}'."}
    return res
