import re
import logging
from models import sights, client1, food
from typing import Dict, Any, Optional # List is not directly used as return type hint for these functions
from schemas import clientIn
from sqlalchemy.exc import SQLAlchemyError # For catching database-specific errors
from sqlalchemy import select # text, String, and_, or_ are not directly used here
from db import database

# Configure basic logging (if not already configured in a central place)
# logging.basicConfig(level=logging.INFO) # Usually configured once in main.py or a config file
logger = logging.getLogger(__name__)

async def clientSave(cl: clientIn) -> Optional[Dict[str, Any]]:
    try:
        insert_query = client1.insert().values(
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
        await database.execute(insert_query)
        logger.info(f"Client data inserted for cId: {cl.cId}")

        fetch_query = client1.select().where(client1.c.cId == cl.cId)
        result_row_proxy = await database.fetch_one(fetch_query)

        if result_row_proxy:
            logger.info(f"Client data fetched successfully after insert for cId: {cl.cId}")
            return dict(result_row_proxy) # Convert RowProxy to dict
        else:
            logger.warning(f"Could not fetch client data after insert for cId: {cl.cId}")
            return None
    except SQLAlchemyError as e:
        logger.exception(f"Database error during clientSave for cId {cl.cId}: {e}")
        return None # Or raise a custom DB error exception
    except Exception as e:
        logger.exception(f"Unexpected error during clientSave for cId {cl.cId}: {e}")
        return None # Or raise


async def get_processed_sightseeing_data(nsights: int, place: str, initial_price: int = 10000) -> Dict[str, Any]:
    try:
        query = sights.select().where(sights.c.sDes == place)
        results = await database.fetch_all(query)
        actual_count = len(results)

        if actual_count == 0:
            logger.info(f"No sightseeing data found for destination: {place}")
            return {
                "sightseeing_data": [],
                "message": f"No sightseeing data available for '{place}'.",
                "returned_nsights": 0
            }

        # Limit results: if nsights is 0 or negative, take all; otherwise, take up to nsights
        limited_results = results[:nsights] if nsights > 0 and nsights <= actual_count else results

        sightseeing_list = []
        processed_results = [dict(row) for row in limited_results] # Convert RowProxies to dicts

        for i_data in processed_results:
            transport_price_str = i_data.get("sTransportPrice", "0")
            tp = 0
            try:
                if 'to' in transport_price_str:
                    parts = transport_price_str.split('to')
                    tp = ((int(parts[0].strip()) + int(parts[1].strip())) / 2) * 2
                elif transport_price_str.strip(): # Ensure not empty after strip
                    tp = int(transport_price_str.strip()) * 2
            except ValueError:
                logger.warning(f"Could not parse sTransportPrice '{transport_price_str}' for sight {i_data.get('sPlace')}. Defaulting to 0.")
                tp = 0
            initial_price -= tp

            entry_fee_str = i_data.get("sEnfee", "")
            fee = 0
            fee_match = re.search(r'\d+', entry_fee_str)
            if fee_match:
                try:
                    fee = int(fee_match.group())
                except ValueError:
                    logger.warning(f"Could not parse sEnfee '{entry_fee_str}' for sight {i_data.get('sPlace')}. Defaulting to 0.")
                    fee = 0
            initial_price -= fee

            sightseeing_list.append({
                "sId": i_data.get("sId"),
                "sPlace": i_data.get("sPlace"),
                "sLoc": i_data.get("sLoc"),
                "sTiming": i_data.get("sTiming"),
                "sEnfee": entry_fee_str,
                "sBesttime": i_data.get("sBesttime"),
                "sDis": i_data.get("sDis"),
                "sTransport": i_data.get("sTransport"),
                "sTransportPrice (Doubled)": tp,
                "sDes": i_data.get("sDes"),
                "remaining_price": initial_price
            })

        logger.info(f"Processed {len(sightseeing_list)} sightseeing spots for {place}.")
        return {
            "returned_nsights": len(sightseeing_list),
            "sightseeing_data": sightseeing_list
        }
    except SQLAlchemyError as e:
        logger.exception(f"Database error during get_processed_sightseeing_data for place {place}: {e}")
        # Return a structured error or re-raise as a custom exception
        return {"message": f"A database error occurred while fetching sightseeing data for '{place}'.", "sightseeing_data": [], "returned_nsights": 0}
    except Exception as e:
        logger.exception(f"Unexpected error during get_processed_sightseeing_data for place {place}: {e}")
        return {"message": f"An unexpected error occurred while processing sightseeing data for '{place}'.", "sightseeing_data": [], "returned_nsights": 0}


async def get_processed_food(loc: str, suggest: bool, choice: Optional[str]) -> Dict[str, Any]:
    if not suggest:
        logger.info(f"Food suggestion not required for location: {loc}")
        return {"message": "Food suggestion is not required by client.", "filtered_food": []}

    if not choice: # Client chose 'Yes' for suggestions but didn't provide a choice (e.g., Veg/Non-Veg)
        logger.warning(f"Food suggestion requested for {loc}, but no choice (Veg/Non-Veg) provided.")
        return {"message": "Food choice (Veg/Non-Veg) not specified, though suggestions were requested.", "filtered_food": []}

    try:
        query = food.select().where(food.c.fAdd == loc)
        results = await database.fetch_all(query)

        if not results:
            logger.info(f"No food records found for location: {loc}")
            return {"message": f"No food records found for location '{loc}'.", "filtered_food": []}

        matched_records = []
        normalized_client_choice = choice.strip().upper()

        for item_row in results:
            item_dict = dict(item_row)
            db_food_item_string = item_dict.get("fItem", "")
            
            # Improved regex to be more flexible with spaces around parentheses
            match = re.search(r'\(\s*(V|NV|VEG|NON-VEG)\s*\)', db_food_item_string, re.IGNORECASE)
            
            if match:
                db_food_type = match.group(1).strip().upper()
                type_matches = False

                if normalized_client_choice == "VEG":
                    if db_food_type == "V" or db_food_type == "VEG":
                        type_matches = True
                elif normalized_client_choice == "NON-VEG": # Assuming frontend sends "Non-Veg"
                    if db_food_type == "NV" or db_food_type == "NON-VEG":
                        type_matches = True
                
                if type_matches:
                    matched_records.append(item_dict)
            # else:
            #     logger.debug(f"Item '{db_food_item_string}' at '{loc}' did not match type pattern or was not Veg/Non-Veg.")


        if matched_records:
            logger.info(f"Found {len(matched_records)} food items for choice '{choice}' at '{loc}'.")
            return {"filtered_food": matched_records}
        else:
            message = f"No food items matching your choice '{choice}' found at location '{loc}'."
            if normalized_client_choice == "VEG":
                message = f"No food items marked clearly as Veg ('(V)' or '(VEG)') found at location '{loc}'."
            elif normalized_client_choice == "NON-VEG":
                message = f"No food items marked clearly as Non-Veg ('(NV)' or '(NON-VEG)') found at location '{loc}'."
            logger.info(message)
            return {"message": message, "filtered_food": []}

    except SQLAlchemyError as e:
        logger.exception(f"Database error during get_processed_food for location {loc}, choice {choice}: {e}")
        return {"message": f"A database error occurred while fetching food data for '{loc}'.", "filtered_food": []}
    except Exception as e:
        logger.exception(f"Unexpected error during get_processed_food for {loc}, choice {choice}: {e}")
        return {"message": f"An unexpected error occurred while processing food data for '{loc}'.", "filtered_food": []}