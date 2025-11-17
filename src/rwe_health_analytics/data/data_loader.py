"""
Data Loading Module
Handles loading and basic validation of healthcare data
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthcareDataLoader:
    """Load and validate healthcare datasets"""

    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.datasets = {}

    def load_demographics(self) -> pd.DataFrame:
        """Load patient demographics data"""
        filepath = self.data_dir / "demographics.csv"
        logger.info(f"Loading demographics from {filepath}")

        df = pd.read_csv(filepath)
        df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])

        logger.info(f"Loaded {len(df)} patient records")
        self.datasets['demographics'] = df
        return df

    def load_diagnoses(self) -> pd.DataFrame:
        """Load diagnosis records"""
        filepath = self.data_dir / "diagnoses.csv"
        logger.info(f"Loading diagnoses from {filepath}")

        df = pd.read_csv(filepath)
        df['diagnosis_date'] = pd.to_datetime(df['diagnosis_date'])

        logger.info(f"Loaded {len(df)} diagnosis records")
        self.datasets['diagnoses'] = df
        return df

    def load_lab_results(self) -> pd.DataFrame:
        """Load laboratory test results"""
        filepath = self.data_dir / "lab_results.csv"
        logger.info(f"Loading lab results from {filepath}")

        df = pd.read_csv(filepath)
        df['test_date'] = pd.to_datetime(df['test_date'])

        logger.info(f"Loaded {len(df)} lab results")
        self.datasets['lab_results'] = df
        return df

    def load_medications(self) -> pd.DataFrame:
        """Load medication records"""
        filepath = self.data_dir / "medications.csv"
        logger.info(f"Loading medications from {filepath}")

        df = pd.read_csv(filepath)
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])

        logger.info(f"Loaded {len(df)} medication records")
        self.datasets['medications'] = df
        return df

    def load_outcomes(self) -> pd.DataFrame:
        """Load outcome events"""
        filepath = self.data_dir / "outcomes.csv"
        logger.info(f"Loading outcomes from {filepath}")

        df = pd.read_csv(filepath)
        df['event_date'] = pd.to_datetime(df['event_date'])

        logger.info(f"Loaded {len(df)} outcome events")
        self.datasets['outcomes'] = df
        return df

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """Load all datasets"""
        logger.info("Loading all datasets...")

        self.load_demographics()
        self.load_diagnoses()
        self.load_lab_results()
        self.load_medications()
        self.load_outcomes()

        logger.info("All datasets loaded successfully!")
        return self.datasets

    def get_patient_data(self, patient_id: str) -> Dict[str, pd.DataFrame]:
        """Get all data for a specific patient"""
        if not self.datasets:
            self.load_all()

        patient_data = {}
        for name, df in self.datasets.items():
            if 'patient_id' in df.columns:
                patient_data[name] = df[df['patient_id'] == patient_id].copy()
        return patient_data

    def validate_data_quality(self) -> Dict[str, Dict]:
        """Perform basic data quality checks"""
        if not self.datasets:
            self.load_all()

        quality_report = {}
        for name, df in self.datasets.items():
            report = {
                'n_rows': len(df),
                'n_cols': len(df.columns),
                'missing_values': df.isnull().sum().to_dict(),
                'duplicate_rows': df.duplicated().sum(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
            }
            if 'patient_id' in df.columns:
                report['unique_patients'] = df['patient_id'].nunique()

            quality_report[name] = report
        return quality_report

    def get_cohort(
        self,
        diagnosis_codes: Optional[list] = None,
        age_range: Optional[Tuple[int, int]] = None,
        gender: Optional[str] = None
    ) -> pd.DataFrame:
        """Filter patients based on criteria to create a cohort"""
        if 'demographics' not in self.datasets:
            self.load_demographics()

        cohort = self.datasets['demographics'].copy()

        if age_range:
            min_age, max_age = age_range
            cohort = cohort[(cohort['age'] >= min_age) & (cohort['age'] <= max_age)]

        if gender:
            cohort = cohort[cohort['gender'] == gender]

        if diagnosis_codes:
            if 'diagnoses' not in self.datasets:
                self.load_diagnoses()

            patients_with_dx = self.datasets['diagnoses'][
                self.datasets['diagnoses']['icd10_code'].isin(diagnosis_codes)
            ]['patient_id'].unique()

            cohort = cohort[cohort['patient_id'].isin(patients_with_dx)]

        logger.info(f"Cohort created with {len(cohort)} patients")
        return cohort


if __name__ == "__main__":
    # Example usage
    loader = HealthcareDataLoader()
    datasets = loader.load_all()

    print("\n" + "="*50)
    print("DATA LOADING SUMMARY")
    print("="*50)

    for name, df in datasets.items():
        print(f"\n{name.upper()}:")
        print(f"  Rows: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Quality report
    print("\n" + "="*50)
    print("DATA QUALITY REPORT")
    print("="*50)
    quality = loader.validate_data_quality()

    for dataset, report in quality.items():
        print(f"\n{dataset.upper()}:")
        print(f"  Unique patients: {report.get('unique_patients', 'N/A')}")
        print(f"  Duplicate rows: {report['duplicate_rows']}")
        print(f"  Missing values: {sum(report['missing_values'].values())}")
