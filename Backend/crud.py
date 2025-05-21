# crud.py
import re
from models import sights, client1, food # Ensure all models are imported
from typing import List, Dict, Any
from schemas import SightSchema, clientIn # Ensure clientIn is imported
from sqlalchemy import String, and_, or_, select, text # Keep existing imports
from fastapi import status # Keep existing imports
from db import database # Ensure database is imported

async def clientSave(cl: clientIn):
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
        cTravelStartTime=cl.cTravelStartTime,
        cTravelEndTime=cl.cTravelEndTime,
        cReturnTravelPrf=cl.cReturnTravelPrf,
        cReturnBusType=cl.cReturnBusType,
        cReturnTrainCoach=cl.cReturnTrainCoach,
        cReturnTravelStartTime=cl.cReturnTravelStartTime,
        cReturnTravelEndTime=cl.cReturnTravelEndTime,
        cAccomodationPrf=cl.cAccomodationPrf,
        cLowType=cl.cLowType,
        cFoodSug=cl.cFoodSug,
        cFoodChoice=cl.cFoodChoice
    )
    await database.execute(query)
    # Assuming cId is BIGINT and client sends a unique Date.now()
    fetch_query = client1.select().where(client1.c.cId == cl.cId)
    result = await database.fetch_one(fetch_query)
    return dict(result) if result else None

async def get_processed_sightseeing_data(nsights: int, place: str, initial_price=10000):
    query = sights.select().where(sights.c.sDes == place)
    results = await database.fetch_all(query)
    actual_count = len(results)

    if actual_count == 0:
        return {
            "sightseeing_data": [],
            "message": "No sightseeing data available for the given destination."
        }

    limited_results = results[:nsights] if nsights > 0 else results
    sightseeing_list = []

    # Convert RowProxies to dicts once for easier access and modification if needed
    processed_results = [dict(row) for row in limited_results]

    for i_data in processed_results: # Iterate over list of dictionaries
        transport_price_str = i_data.get("sTransportPrice", "0") # Default to "0" if missing
        transport_parts = transport_price_str.split('to')
        tp = 0 # Initialize transport price for this sight

        try:
            if len(transport_parts) > 1:
                tp = ((int(transport_parts[0]) + int(transport_parts[1])) / 2) * 2
            elif transport_parts[0]: # Ensure it's not an empty string
                tp = int(transport_parts[0]) * 2
        except ValueError:
            # Handle cases where sTransportPrice is not a number or "XtoY"
            print(f"Warning: Could not parse sTransportPrice '{transport_price_str}' for sight {i_data.get('sPlace')}")
            tp = 0 # Default to 0 if parsing fails

        initial_price -= tp

        entry_fee_str = i_data.get("sEnfee", "")
        fee_match = re.search(r'\d+', entry_fee_str)
        fee = 0 # Initialize entry fee for this sight
        if fee_match:
            try:
                fee = int(fee_match.group())
            except ValueError:
                print(f"Warning: Could not parse sEnfee '{entry_fee_str}' for sight {i_data.get('sPlace')}")
                fee = 0 # Default to 0 if parsing fails
        initial_price -= fee

        sightseeing_list.append({
            "sId": i_data.get("sId"),
            "sPlace": i_data.get("sPlace"),
            "sLoc": i_data.get("sLoc"),
            "sTiming": i_data.get("sTiming"),
            "sEnfee": entry_fee_str, # Return original string
            "sBesttime": i_data.get("sBesttime"),
            "sDis": i_data.get("sDis"),
            "sTransport": i_data.get("sTransport"),
            "sTransportPrice (Doubled)": tp, 
            "sDes": i_data.get("sDes"),
            "remaining_price": initial_price 
        })

    return {
        # "requested_nsights": nsights,
        # "available_nsights": actual_count,
        "returned_nsights": len(sightseeing_list),
        "sightseeing_data": sightseeing_list
    }

async def get_processed_food(loc: str, suggest: bool, choice: str): # suggest is boolean from clientIn schema
    if not suggest: # If cFoodSug was false from frontend
        return {"message": "Food suggestion is not required by client.", "filtered_food": []}

    if not choice: # Handle cases where choice might be None or empty string from frontend
        return {"message": "Food choice (Veg/Non-Veg) not specified by client.", "filtered_food": []}

    query = food.select().where(food.c.fAdd == loc)
    results = await database.fetch_all(query)

    if not results:
        return {"message": f"No food records found for location '{loc}'.", "filtered_food": []}

    matched_records = []
    normalized_client_choice = choice.strip().upper()

    for item_row in results:
        item_dict = dict(item_row) # Convert RowProxy to dict for easier access
        db_food_item_string = item_dict.get("fItem", "") # Get fItem, default to empty string if None
        match = re.search(r'\((.*?)\)', db_food_item_string)
        if match:
            db_food_type = match.group(1).strip().upper()

            type_matches = False
            if normalized_client_choice == "VEG":
                if db_food_type == "V":  # Directly match "V" for Veg
                    type_matches = True
            elif normalized_client_choice == "NON-VEG":
                if db_food_type == "NV": # Directly match "NV" for Non-Veg
                    type_matches = True

            if type_matches:
                matched_records.append(item_dict)

    if matched_records:
        return {"filtered_food": matched_records}
    else:
        # Provide a more informative message based on the actual client choice
        if normalized_client_choice == "VEG":
            message = f"No food items marked with '(V)' found at location '{loc}' for your selection."
        elif normalized_client_choice == "NON-VEG":
            message = f"No food items marked with '(NV)' found at location '{loc}' for your selection."
        else:
            # This case might not be hit if frontend only sends "Veg" or "Non-Veg"
            message = f"No food records found for your specific choice '{choice}' at location '{loc}'."
        return {"message": message, "filtered_food": []}