from http.client import HTTPException
from aem import app
import uvicorn
from caching.CacheRedis import RedisManager

# from models.Models import BookingInteractionRequest
from services.models.Models import TriageInteractionRequest

# from services.HolidayBooking.ServiceBookHoliday import ServiceHolidayBooking
from services.service_triage_category.algos.pyreason.algo_triage_basic.AlgoTriageCategoryInteraction import (
    TriageCategoryBasic,
)
from utils.app_utils import app
from fastapi import Request
from utils.Utils import load_env_file


@app.post("/tools/triage", tags=["Triage"])
async def rate_response(
    request: Request, triage: TriageInteractionRequest
) -> TriageInteractionRequest:
    try:
        # Step 1. Setup Caching Manager
        load_env_file("dev.env")
        caching_manager = RedisManager()
        key = f"tools-triage-{triage.request_id}"

        # Step 2. Check for new or complete interaction request
        cached_bir_json = caching_manager.get_json(key)
        if cached_bir_json is None:
            caching_manager.save_json(key, triage.json())
        else:
            cached_bir = TriageInteractionRequest(**cached_bir_json)
            if cached_bir.complete:
                return cached_bir

        # Step 3. Interaction request is still WIP, so run booking service and cache result
        bir = TriageCategoryBasic().run_triage_algo(triage_interaction_request=triage)
        caching_manager.save_json(key, bir.json())

        return bir

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Rapid Debugging start app with this
    # uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)

    # For Docker Builds
    uvicorn.run(app, host="0.0.0.0", port=8002)
