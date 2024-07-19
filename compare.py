import uvicorn
from fastapi import FastAPI, HTTPException, Request, Body
from pydantic import BaseModel
from caching.CacheRedis import RedisManager
from services.service_triage_category.algos.pyreason.algo_triage_basic.AlgoTriageScoreInteraction import (
    TriageScoreInteraction,
)
from services.models.Models import TriageInteractionRequest, Threshold
from services.service_triage.factory.FactoryAlgoTriage import (
    TriageAlgoName,
    TriageFactory,
)

from utils.Utils import load_env_file


class TriageRequestBody(BaseModel):
    request_id: str
    params: dict


app = FastAPI(
    title="ASU Tools Demo",
    description="Demo of using an interactive tools",
    version="0.0.1",
)


@app.post("/tools/triage", tags=["Triage"])
async def rate_response(
    request: Request, body: TriageRequestBody = Body(...)
) -> TriageInteractionRequest:
    try:
        # Step 1. Setup Caching Manager
        load_env_file("dev.env")
        caching_manager = RedisManager()
        key = f"tools-triage-{body.request_id}"

        # Create TriageInteractionRequest from request body
        triage = TriageInteractionRequest(
            request_id=body.request_id, params=body.params
        )

        # Step 2. Check for new or complete interaction request
        cached_bir_json = caching_manager.get_json(key)
        if cached_bir_json is None:
            caching_manager.save_json(key, triage.json())
        else:
            cached_bir = TriageInteractionRequest(**cached_bir_json)
            if cached_bir.complete:
                return cached_bir

        # Step 3. Interaction request is still WIP, so run the triage algorithm and cache result
        thresholds_data_algo3 = {
            "gcs": Threshold(min_value=3, max_value=15),
            "sbp": Threshold(min_value=0, max_value=219),
            "rr": Threshold(min_value=0, max_value=100),
            # Add more thresholds as necessary
        }

        bir = TriageScoreInteraction(thresholds=thresholds_data_algo3).run_triage_algo(
            triage_interaction_request=triage
        )

        # Step 4. Save the result and return it
        caching_manager.save_json(key, bir.json())
        return bir

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
