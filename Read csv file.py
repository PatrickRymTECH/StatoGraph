"""Interactive CSV-to-chart helper.

This script guides a user through selecting a CSV file and creating a bar or pie
chart from its contents. It validates user input and provides friendly error
messages when data cannot be graphed.

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, List

import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_numeric_dtype
import tkinter as tk
from tkinter import filedialog


def select_csv_file() -> Path:
    

    Raises:
        ValueError: If the user cancels the file selection dialog.
    

    root = tk.Tk()
    root.withdraw()
    print("Please select a CSV file to load.")
    filename = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )
    root.update()
    root.destroy()

    if not filename:
        raise ValueError("No file selected. Please choose a CSV file to continue.")

    return Path(filename)


def load_dataframe(path: Path) -> pd.DataFrame:


    if not path.exists():
        raise FileNotFoundError(f"Cannot find file: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The selected CSV file is empty and cannot be graphed.")

    return df


def display_columns(df: pd.DataFrame) -> None:
    
    print("Available columns:")
    for name in df.columns:
        dtype = "numeric" if is_numeric_dtype(df[name]) else "text"
        print(f" - {name} ({dtype})")


def prompt_choice(prompt: str, options: Iterable[str]) -> str:
    

    option_list: List[str] = [opt.lower() for opt in options]
    while True:
        choice = input(prompt).strip().lower()
        if choice in option_list:
            return choice
        print(f"Please choose one of: {', '.join(option_list)}")


def prompt_column(df: pd.DataFrame, prompt: str) -> str:
    

    available = set(df.columns)
    while True:
        column = input(prompt).strip()
        if column in available:
            return column
        print("Column not found. Please pick from the columns listed above.")


def ensure_numeric_column(df: pd.DataFrame, column: str) -> None:
    
    if not is_numeric_dtype(df[column]):
        raise ValueError(
            f"Column '{column}' is not numeric. Choose a numeric column for values."
        )


def build_bar_chart(df: pd.DataFrame) -> None:
    

    display_columns(df)
    category_col = prompt_column(df, "Enter the column to use for categories: ")

    numeric_columns = [col for col in df.columns if is_numeric_dtype(df[col])]
    use_counts = True
    value_col: str | None = None

    if numeric_columns:
        answer = prompt_choice(
            "Use a numeric column for bar heights? (yes/no): ", ["yes", "no"]
        )
        use_counts = answer == "no"
        if not use_counts:
            value_col = prompt_column(df, "Enter the numeric column for bar heights: ")
            ensure_numeric_column(df, value_col)

    if use_counts:
        grouped = df[category_col].value_counts()
        if grouped.empty:
            raise ValueError("No data available to count for the selected category.")
    else:
        grouped = df.groupby(category_col)[value_col].sum()
        if grouped.empty:
            raise ValueError("No numeric data available to sum for the selected columns.")

    grouped.sort_values(ascending=False).plot(kind="bar")
    plt.title("Bar Chart")
    plt.xlabel(category_col)
    plt.ylabel("Count" if use_counts else f"Sum of {value_col}")
    plt.tight_layout()
    plt.show()


def build_pie_chart(df: pd.DataFrame) -> None:
    

    display_columns(df)
    category_col = prompt_column(df, "Enter the column to use for slice labels: ")
    value_col = prompt_column(df, "Enter the numeric column for slice sizes: ")
    ensure_numeric_column(df, value_col)

    grouped = df.groupby(category_col)[value_col].sum()
    if grouped.empty:
        raise ValueError("No numeric data available to create a pie chart.")

    grouped.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Pie Chart")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def main() -> None:
    

    try:
        csv_path = select_csv_file()
        df = load_dataframe(csv_path)
        print(f"Loaded {len(df)} rows from '{csv_path.name}'.\n")

        chart_type = prompt_choice(
            "Which chart would you like to create? (bar/pie): ", ["bar", "pie"]
        )

        if chart_type == "bar":
            build_bar_chart(df)
        else:
            build_pie_chart(df)

    except Exception as exc:  # noqa: BLE001 - broad to show clear user message
        print(f"\nUnable to create chart: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
