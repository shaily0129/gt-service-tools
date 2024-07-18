from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from models import Patient, PatientUpdateRequest, TriageCategory, Threshold
from typing import List
from services.service_triage_category.factory.FactoryAlgo import TriagescoreToTriagecategoryFactory, TriagescoreToTriagecategoryAlgoName

app = FastAPI()

# Initialize the thresholds data
thresholds_data = {
    'triage_score': Threshold(min_value=0, max_value=100)
}

# Sample data with physiology_record
db: List[Patient] = [
    Patient(id=uuid4(), name='Adrian Monk', triage_score=33, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Natalie Tieger', triage_score=40, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Leland Stottlemeyer', triage_score=43, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Jake Peralta', triage_score=20, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Sharona Fleming', triage_score=87, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Randy Disher', triage_score=1, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Trudy Monk', triage_score=40, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Charles Kroger', triage_score=95, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Julie Trieger', triage_score=80, physiology_record={"attribute": "value"}),
    Patient(id=uuid4(), name='Benjy Fleming', triage_score=87, physiology_record={"attribute": "value"}),
]

# Calculate initial triage categories
algo_triage_categories = TriagescoreToTriagecategoryFactory.create_triageScore_to_triageCategory_algo(
    mode=TriagescoreToTriagecategoryAlgoName.BASIC,
    thresholds=thresholds_data
)
triage_category_all_patients = algo_triage_categories.return_triage_categories(db)
for i, triage_category_patient in enumerate(triage_category_all_patients):
    db[i].triage_category = triage_category_patient.category

@app.get("/api/v1/patients", response_model=List[Patient])
async def fetch_patients():
    return db

@app.post("/api/v1/patients", response_model=UUID)
async def register_patient(patient: Patient):
    patient.id = uuid4()  
    db.append(patient)
    return patient.id

@app.delete("/api/v1/patients/{patient_id}")
async def delete_patient(patient_id: UUID):
    for patient in db:
        if patient.id == patient_id:
            db.remove(patient)
            return
    raise HTTPException(status_code=404, detail=f"Patient with id: {patient_id} does not exist")

# @app.put("/api/v1/patients/{patient_id}")
# async def update_patient(patient_update: PatientUpdateRequest, patient_id: UUID):
#     for patient in db:
#         if patient.id == patient_id:
#             if patient_update.name is not None:
#                 patient.name = patient_update.name
#             if patient_update.triage_score is not None:
#                 patient.triage_score = patient_update.triage_score
#                 # Update the triage category based on the new score
#                 updated_category = algo_triage_categories.return_triage_categories([patient])[0].category
#                 patient.triage_category = updated_category
#             if patient_update.triage_category is not None:
#                 patient.triage_category = patient_update.triage_category
#             if patient_update.physiology_record is not None:
#                 patient.physiology_record = patient_update.physiology_record
#             return
#     raise HTTPException(status_code=404, detail=f"Patient with id: {patient_id} does not exist")
