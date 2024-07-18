from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List
from pydantic import BaseModel
from services.service_triage.factory.FactoryAlgoTriage import TriageFactory, TriageAlgoName
from models import Patient, PatientUpdateRequest, Threshold

app = FastAPI()

# Initialize database with sample patients
db: List[Patient] = [
    Patient(
        id=uuid4(),
        name="Adrian Monk",
        external_hemorrhage=3,
        tension_pneumothorax=4,
        traumatic_brain_injury=6,
        burn=2,
        gcs=10,
        sbp=60,
        rr=20,
    ),
    Patient(
        id=uuid4(), name="Natalie Tieger", splenic_laceration=6, gcs=6, sbp=100, rr=40
    ),
    Patient(
        id=uuid4(), name="Leland Stottlemeyer", external_hemorrhage=5, burn=6
    ),
    Patient(
        id=uuid4(), name="Jake Peralta", liver_hematoma=4, tension_pneumothorax=6,
        traumatic_brain_injury=4, burn=6, gcs=5, sbp=120, rr=88
    ),
    Patient(
        id=uuid4(), name="Sharona Fleming", gcs=12, sbp=120, rr=89
    ),
    Patient(
        id=uuid4(), name="Randy Disher", external_hemorrhage=5, tension_pneumothorax=6,
        traumatic_brain_injury=6, burn=2, gcs=15, sbp=80, rr=60
    ),
    Patient(
        id=uuid4(), name="Trudy Monk", splenic_laceration=6, gcs=6, sbp=100, rr=40
    ),
    Patient(
        id=uuid4(), name="Charles Kroger", external_hemorrhage=2, burn=1
    ),
    Patient(
        id=uuid4(), name="Julie Trieger", liver_hematoma=1, tension_pneumothorax=1,
        traumatic_brain_injury=1, burn=1, gcs=4, sbp=40, rr=20
    ),
    Patient(
        id=uuid4(), name="Benjy Fleming", gcs=12, sbp=120, rr=89
    )
]

# Thresholds for triage algorithm
thresholds_data_algo3 = {
    "external_hemorrhage": Threshold(min_value=1, max_value=6),
    "tension_pneumothorax": Threshold(min_value=1, max_value=6),
    "traumatic_brain_injury": Threshold(min_value=1, max_value=6),
    "concussion": Threshold(min_value=1, max_value=6),
    "cerebral_contusion": Threshold(min_value=1, max_value=6),
    "subarachnoid_hemorrhage": Threshold(min_value=1, max_value=6),
    "epidural_hematoma": Threshold(min_value=1, max_value=6),
    "nasal_fracture": Threshold(min_value=1, max_value=6),
    "orbital_fracture": Threshold(min_value=1, max_value=6),
    "le_fort_II_fracture": Threshold(min_value=1, max_value=6),
    "rib_fracture": Threshold(min_value=1, max_value=6),
    "lung_contusion": Threshold(min_value=1, max_value=6),
    "flail_chest": Threshold(min_value=1, max_value=6),
    "aortic_laceration": Threshold(min_value=1, max_value=6),
    "minor_liver_laceration": Threshold(min_value=1, max_value=6),
    "splenic_laceration": Threshold(min_value=1, max_value=6),
    "liver_hematoma": Threshold(min_value=1, max_value=6),
    "pancreatic_transection": Threshold(min_value=1, max_value=6),
    "radius_ulna_fracture": Threshold(min_value=1, max_value=6),
    "femur_fracture": Threshold(min_value=1, max_value=6),
    "knee_dislocation": Threshold(min_value=1, max_value=6),
    "traumatic_amputation_below_knee": Threshold(min_value=1, max_value=6),
    "traumatic_amputation_above_knee": Threshold(min_value=1, max_value=6),
    "burn": Threshold(min_value=1, max_value=6),
    "gcs": Threshold(min_value=3, max_value=15),
    "sbp": Threshold(min_value=0, max_value=219),
    "rr": Threshold(min_value=0, max_value=100),
}


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/api/v1/patients")
async def fetch_patients():
    return db


@app.post("/api/v1/patients")
async def register_patient(patient: Patient):
    patient.id = uuid4()
    db.append(patient)
    return {"id": patient.id}


@app.delete("/api/v1/patients/{patient_id}")
async def delete_patient(patient_id: UUID):
    for patient in db:
        if patient.id == patient_id:
            db.remove(patient)
            return
    raise HTTPException(
        status_code=404, detail=f"Patient with id:{patient_id} does not exist"
    )


@app.put("/api/v1/patients/{patient_id}")
async def update_patient(patient_update: PatientUpdateRequest, patient_id: UUID):
    for patient in db:
        if patient.id == patient_id:
            if patient_update.name is not None:
                patient.name = patient_update.name
            if patient_update.external_hemorrhage is not None:
                patient.external_hemorrhage = patient_update.external_hemorrhage
            if patient_update.tension_pneumothorax is not None:
                patient.tension_pneumothorax = patient_update.tension_pneumothorax
            if patient_update.traumatic_brain_injury is not None:
                patient.traumatic_brain_injury = patient_update.traumatic_brain_injury
            if patient_update.concussion is not None:
                patient.concussion = patient_update.concussion
            if patient_update.cerebral_contusion is not None:
                patient.cerebral_contusion = patient_update.cerebral_contusion
            if patient_update.subarachnoid_hemorrhage is not None:
                patient.subarachnoid_hemorrhage = patient_update.subarachnoid_hemorrhage
            if patient_update.epidural_hematoma is not None:
                patient.epidural_hematoma = patient_update.epidural_hematoma
            if patient_update.nasal_fracture is not None:
                patient.nasal_fracture = patient_update.nasal_fracture
            if patient_update.orbital_fracture is not None:
                patient.orbital_fracture = patient_update.orbital_fracture
            if patient_update.le_fort_II_fracture is not None:
                patient.le_fort_II_fracture = patient_update.le_fort_II_fracture
            if patient_update.rib_fracture is not None:
                patient.rib_fracture = patient_update.rib_fracture
            if patient_update.lung_contusion is not None:
                patient.lung_contusion = patient_update.lung_contusion
            if patient_update.flail_chest is not None:
                patient.flail_chest = patient_update.flail_chest
            if patient_update.aortic_laceration is not None:
                patient.aortic_laceration = patient_update.aortic_laceration
            if patient_update.minor_liver_laceration is not None:
                patient.minor_liver_laceration = patient_update.minor_liver_laceration
            if patient_update.splenic_laceration is not None:
                patient.splenic_laceration = patient_update.splenic_laceration
            if patient_update.liver_hematoma is not None:
                patient.liver_hematoma = patient_update.liver_hematoma
            if patient_update.pancreatic_transection is not None:
                patient.pancreatic_transection = patient_update.pancreatic_transection
            if patient_update.radius_ulna_fracture is not None:
                patient.radius_ulna_fracture = patient_update.radius_ulna_fracture
            if patient_update.femur_fracture is not None:
                patient.femur_fracture = patient_update.femur_fracture
            if patient_update.knee_dislocation is not None:
                patient.knee_dislocation = patient_update.knee_dislocation
            if patient_update.traumatic_amputation_below_knee is not None:
                patient.traumatic_amputation_below_knee = (
                    patient_update.traumatic_amputation_below_knee
                )
            if patient_update.traumatic_amputation_above_knee is not None:
                patient.traumatic_amputation_above_knee = (
                    patient_update.traumatic_amputation_above_knee
                )
            if patient_update.burn is not None:
                patient.burn = patient_update.burn
            if patient_update.gcs is not None:
                patient.gcs = patient_update.gcs
            if patient_update.sbp is not None:
                patient.sbp = patient_update.sbp
            if patient_update.rr is not None:
                patient.rr = patient_update.rr
            return
    raise HTTPException(
        status_code=404, detail=f"Patient with id:{patient_id} does not exist"
    )


@app.get("/api/v1/triage_scores")
async def compute_triage_scores():
    triage_algo = TriageFactory.create_triage_algo(
        TriageAlgoName.LIFE, thresholds=thresholds_data_algo3
    )
    triage_scores = triage_algo.triage(db)
    return {"triage_scores": triage_scores}


