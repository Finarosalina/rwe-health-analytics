"""
Synthetic Healthcare Data Generator
-----------------------------------
Generates EHR-like synthetic data with realistic clinical patterns.

Modules:
- Demographics
- Diagnoses
- Laboratory results
- Medications
- Outcomes
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path
from typing import Tuple

# Reproducibility
np.random.seed(42)
random.seed(42)


class HealthcareDataGenerator:
    """Generate synthetic healthcare data similar to EHR/claims."""

    def __init__(self, n_patients: int = 10000) -> None:
        self.n_patients = n_patients
        self.start_date = datetime(2018, 1, 1)
        self.end_date = datetime(2024, 12, 31)

        # ICD-10 codes for common conditions
        self.diagnosis_codes = {
            'I21': 'Acute myocardial infarction',
            'I50': 'Heart failure',
            'E11': 'Type 2 diabetes mellitus',
            'J44': 'COPD',
            'C34': 'Lung cancer',
            'C50': 'Breast cancer',
            'G35': 'Multiple sclerosis',
            'F32': 'Major depressive disorder',
            'M05': 'Rheumatoid arthritis',
            'N18': 'Chronic kidney disease'
        }

        # Common medications
        self.medications = {
            'cardiovascular': ['Metoprolol', 'Lisinopril', 'Atorvastatin', 'Aspirin', 'Warfarin'],
            'diabetes': ['Metformin', 'Insulin', 'Glipizide', 'Sitagliptin'],
            'oncology': ['Pembrolizumab', 'Nivolumab', 'Carboplatin', 'Paclitaxel'],
            'neurology': ['Interferon beta', 'Glatiramer', 'Fingolimod', 'Natalizumab'],
            'respiratory': ['Albuterol', 'Fluticasone', 'Tiotropium']
        }

    def generate_demographics(self) -> pd.DataFrame:
        """Generate patient demographics with comorbidity and socioeconomic info."""
        data = {
            'patient_id': [f'P{str(i).zfill(6)}' for i in range(self.n_patients)],
            'age': np.random.normal(55, 15, self.n_patients).clip(18, 95).astype(int),
            'gender': np.random.choice(['M', 'F'], self.n_patients, p=[0.48, 0.52]),
            'race': np.random.choice(['White', 'Black', 'Asian', 'Hispanic', 'Other'],
                                     self.n_patients, p=[0.60, 0.13, 0.06, 0.18, 0.03]),
            'bmi': np.random.normal(28, 6, self.n_patients).clip(15, 50).round(1),
            'smoking_status': np.random.choice(['Never', 'Former', 'Current'],
                                               self.n_patients, p=[0.50, 0.30, 0.20]),
            'enrollment_date': [self.start_date + timedelta(days=random.randint(0, 365))
                                for _ in range(self.n_patients)]
        }

        df = pd.DataFrame(data)
        df['charlson_score'] = np.random.poisson(2, self.n_patients).clip(0, 10)
        df['zip_code'] = np.random.randint(10000, 99999, self.n_patients)
        df['insurance_type'] = np.random.choice(['Commercial', 'Medicare', 'Medicaid', 'Uninsured'],
                                                self.n_patients, p=[0.50, 0.30, 0.15, 0.05])
        return df

    def generate_diagnoses(self, demographics_df: pd.DataFrame) -> pd.DataFrame:
        """Generate diagnosis records for each patient."""
        records = []
        for _, patient in demographics_df.iterrows():
            n_diagnoses = np.random.poisson(patient['charlson_score'] + 1)
            for _ in range(n_diagnoses):
                diagnosis_date = patient['enrollment_date'] + timedelta(days=random.randint(0, 365*5))
                icd_code = random.choice(list(self.diagnosis_codes.keys()))
                records.append({
                    'patient_id': patient['patient_id'],
                    'diagnosis_date': diagnosis_date,
                    'icd10_code': icd_code,
                    'diagnosis_desc': self.diagnosis_codes[icd_code],
                    'diagnosis_type': random.choice(['Primary', 'Secondary']),
                    'visit_type': random.choice(['Inpatient', 'Outpatient', 'Emergency'])
                })
        return pd.DataFrame(records)

    def generate_lab_results(self, demographics_df: pd.DataFrame) -> pd.DataFrame:
        """Generate laboratory test results for each patient."""
        records = []
        lab_tests = {
            'HbA1c': (5.7, 1.2, '%'),
            'Creatinine': (1.0, 0.3, 'mg/dL'),
            'eGFR': (90, 25, 'mL/min'),
            'HDL': (50, 15, 'mg/dL'),
            'LDL': (100, 30, 'mg/dL'),
            'Hemoglobin': (13.5, 2, 'g/dL'),
            'WBC': (7.5, 2.5, 'K/uL'),
            'Platelets': (250, 50, 'K/uL'),
            'ALT': (30, 20, 'U/L'),
            'AST': (28, 18, 'U/L')
        }

        for _, patient in demographics_df.iterrows():
            n_labs = random.randint(10, 30)
            for _ in range(n_labs):
                test_date = patient['enrollment_date'] + timedelta(days=random.randint(0, 365*5))
                test_name = random.choice(list(lab_tests.keys()))
                mean, std, unit = lab_tests[test_name]
                value = np.random.normal(mean * 1.2, std * 1.3) if patient['charlson_score'] > 3 else np.random.normal(mean, std)
                records.append({
                    'patient_id': patient['patient_id'],
                    'test_date': test_date,
                    'test_name': test_name,
                    'test_value': round(value, 2),
                    'unit': unit,
                    'abnormal_flag': 'Y' if random.random() < 0.3 else 'N'
                })
        return pd.DataFrame(records)

    def generate_medications(self, demographics_df: pd.DataFrame, diagnoses_df: pd.DataFrame) -> pd.DataFrame:
        """Generate medication records based on patient diagnoses."""
        records = []
        for _, patient in demographics_df.iterrows():
            patient_diagnoses = diagnoses_df[diagnoses_df['patient_id'] == patient['patient_id']]
            for _, diagnosis in patient_diagnoses.iterrows():
                if random.random() < 0.7:
                    if 'cancer' in diagnosis['diagnosis_desc'].lower():
                        med_category = 'oncology'
                    elif 'diabetes' in diagnosis['diagnosis_desc'].lower():
                        med_category = 'diabetes'
                    elif any(x in diagnosis['diagnosis_desc'].lower() for x in ['heart', 'cardio']):
                        med_category = 'cardiovascular'
                    elif 'sclerosis' in diagnosis['diagnosis_desc'].lower():
                        med_category = 'neurology'
                    else:
                        med_category = random.choice(list(self.medications.keys()))
                    medication = random.choice(self.medications[med_category])
                    start_date = diagnosis['diagnosis_date'] + timedelta(days=random.randint(0, 30))
                    duration_days = random.randint(30, 730)
                    end_date = start_date + timedelta(days=duration_days)
                    records.append({
                        'patient_id': patient['patient_id'],
                        'medication': medication,
                        'start_date': start_date,
                        'end_date': end_date,
                        'dosage': f"{random.choice([5, 10, 20, 40, 50, 100])} mg",
                        'frequency': random.choice(['QD', 'BID', 'TID', 'PRN']),
                        'prescriber_specialty': random.choice([
                            'Cardiology', 'Oncology', 'Internal Medicine', 'Endocrinology', 'Neurology'
                        ])
                    })
        return pd.DataFrame(records)

    def generate_outcomes(self, demographics_df: pd.DataFrame, diagnoses_df: pd.DataFrame) -> pd.DataFrame:
        """Generate outcome events (death, hospitalization, disease progression)."""
        records = []
        for _, patient in demographics_df.iterrows():
            patient_diagnoses = diagnoses_df[diagnoses_df['patient_id'] == patient['patient_id']]
            risk_score = (patient['charlson_score'] / 10 + (patient['age'] - 18) / 80 + (0.2 if patient['smoking_status'] == 'Current' else 0))
            
            # Death
            death_prob = risk_score * 0.15
            if random.random() < death_prob:
                last_diag = patient_diagnoses['diagnosis_date'].max() if len(patient_diagnoses) > 0 else patient['enrollment_date']
                death_date = last_diag + timedelta(days=random.randint(30, 1095))
                if death_date <= self.end_date:
                    records.append({
                        'patient_id': patient['patient_id'],
                        'event_type': 'Death',
                        'event_date': death_date,
                        'censored': 0
                    })
            
            # Hospitalizations
            n_hosp = np.random.poisson(risk_score * 3)
            for _ in range(n_hosp):
                hosp_date = patient['enrollment_date'] + timedelta(days=random.randint(0, 1825))
                if hosp_date <= self.end_date:
                    records.append({
                        'patient_id': patient['patient_id'],
                        'event_type': 'Hospitalization',
                        'event_date': hosp_date,
                        'los_days': random.randint(1, 15),
                        'censored': 0
                    })
            
            # Disease progression (for cancer)
            cancer_diag = patient_diagnoses[patient_diagnoses['diagnosis_desc'].str.contains('cancer', case=False)]
            if len(cancer_diag) > 0 and random.random() < 0.4:
                progression_date = cancer_diag['diagnosis_date'].iloc[0] + timedelta(days=random.randint(90, 730))
                if progression_date <= self.end_date:
                    records.append({
                        'patient_id': patient['patient_id'],
                        'event_type': 'Disease Progression',
                        'event_date': progression_date,
                        'censored': 0
                    })
        return pd.DataFrame(records)

    def generate_all_data(self, output_dir: str = 'data/raw') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Generate all datasets and save CSV files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print("Generating demographics...")
        demographics = self.generate_demographics()
        demographics.to_csv(output_path / 'demographics.csv', index=False)
        print(f"✓ {len(demographics)} patients generated")

        print("Generating diagnoses...")
        diagnoses = self.generate_diagnoses(demographics)
        diagnoses.to_csv(output_path / 'diagnoses.csv', index=False)
        print(f"✓ {len(diagnoses)} diagnoses generated")

        print("Generating lab results...")
        labs = self.generate_lab_results(demographics)
        labs.to_csv(output_path / 'lab_results.csv', index=False)
        print(f"✓ {len(labs)} lab results generated")

        print("Generating medications...")
        medications = self.generate_medications(demographics, diagnoses)
        medications.to_csv(output_path / 'medications.csv', index=False)
        print(f"✓ {len(medications)} medications generated")

        print("Generating outcomes...")
        outcomes = self.generate_outcomes(demographics, diagnoses)
        outcomes.to_csv(output_path / 'outcomes.csv', index=False)
        print(f"✓ {len(outcomes)} outcome events generated")

        print("\nDATA GENERATION COMPLETE!")
        return demographics, diagnoses, labs, medications, outcomes


if __name__ == "__main__":
    generator = HealthcareDataGenerator(n_patients=10000)
    generator.generate_all_data()


