# ==========================================================
# Cyber Threat Intelligence Dashboard
# Main File
# Author : Maham Farooq
# Project : Cyber Threat Intelligence Dashboard
# ==========================================================

import pandas as pd


def load_dataset(file_name):
    """
    Load the dataset from a CSV file.
    """
    try:
        df = pd.read_csv(file_name)
        print("✅ Dataset Loaded Successfully!\n")
        return df

    except FileNotFoundError:
        print("❌ Error: Dataset file not found.")
        return None

    except Exception as error:
        print("❌ Error:", error)
        return None


def main():

    print("=" * 70)
    print("        CYBER THREAT INTELLIGENCE DASHBOARD")
    print("=" * 70)

    print("\nLoading Dataset...\n")

    dataset = load_dataset("cicids2017_cleaned.csv")

    if dataset is None:
        return

    # =====================================================
    # Dataset Shape
    # =====================================================

    print("=" * 70)
    print("DATASET SHAPE")
    print("=" * 70)

    print(f"Total Rows    : {dataset.shape[0]}")
    print(f"Total Columns : {dataset.shape[1]}")

    # =====================================================
    # Column Names
    # =====================================================

    print("\n" + "=" * 70)
    print("COLUMN NAMES")
    print("=" * 70)

    for column in dataset.columns:
        print(column)

    # =====================================================
    # Dataset Information
    # =====================================================

    print("\n" + "=" * 70)
    print("DATASET INFORMATION")
    print("=" * 70)

    dataset.info()

    # =====================================================
    # Missing Values
    # =====================================================

    print("\n" + "=" * 70)
    print("MISSING VALUES")
    print("=" * 70)

    print(dataset.isnull().sum())

    # =====================================================
    # First Five Records
    # =====================================================

    print("\n" + "=" * 70)
    print("FIRST FIVE RECORDS")
    print("=" * 70)

    print(dataset.head())

    # =====================================================
    # Statistical Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("STATISTICAL SUMMARY")
    print("=" * 70)

    print(dataset.describe())

    # =====================================================
    # Attack Type Distribution
    # =====================================================

    print("\n" + "=" * 70)
    print("ATTACK TYPE DISTRIBUTION")
    print("=" * 70)

    print(dataset["Attack Type"].value_counts())

    print("\n" + "=" * 70)
    print("PROJECT ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    main()
    