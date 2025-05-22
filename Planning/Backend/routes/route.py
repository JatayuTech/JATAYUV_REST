import logging
from fastapi import APIRouter, HTTPException
from schemas import clientIn # Assuming SightSchema is used within crud or for future use
import crud # Keep this import style if you prefer calling crud.function_name

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/saveClient")
async def save_client_route(client: clientIn): # Renamed for clarity, FastAPI uses function name for docs
    try:
        logger.info(f"Attempting to save client: {client.cName} for destination {client.cDes}")
        client_details_dict = await crud.clientSave(client)

        if not client_details_dict:
            logger.error(f"Failed to save client or retrieve details after saving for cId: {client.cId}")
            raise HTTPException(status_code=500, detail="Client save operation failed or client not found after save.")
        logger.info(f"Client saved successfully: {client_details_dict.get('cId')}")

        # Ensure necessary keys exist before proceeding
        required_keys = ["cNsightseeing", "cDes", "cFoodSug", "cFoodChoice"]
        for key in required_keys:
            if key not in client_details_dict:
                logger.error(f"Missing key '{key}' in client_details_dict after saving client cId: {client.cId}")
                raise HTTPException(status_code=500, detail=f"Internal server error: Missing critical client data ('{key}') after save.")

        logger.info(f"Fetching sightseeing data for: {client_details_dict['cDes']}, nsights: {client_details_dict['cNsightseeing']}")
        sightseeing_data = await crud.get_processed_sightseeing_data(
            nsights=client_details_dict["cNsightseeing"],
            place=client_details_dict["cDes"]
            # budget=client_details_dict.get("cBudget") # If you plan to use budget from client_details_dict
        )
        logger.info("Sightseeing data processed.")

        logger.info(f"Fetching food data for: {client_details_dict['cDes']}, suggest: {client_details_dict['cFoodSug']}, choice: {client_details_dict['cFoodChoice']}")
        food_data = await crud.get_processed_food(
            loc=client_details_dict["cDes"],
            suggest=client_details_dict["cFoodSug"],
            choice=client_details_dict["cFoodChoice"]
        )
        logger.info("Food data processed.")

        return [sightseeing_data, food_data]

    except HTTPException as http_exc:
        # Re-raise HTTPException as FastAPI will handle it appropriately
        raise http_exc
    except Exception as e:
        # Catch any other unexpected errors
        logger.exception(f"An unexpected error occurred in /saveClient endpoint for cId {client.cId if client else 'Unknown'}: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected internal server error occurred: {str(e)}")