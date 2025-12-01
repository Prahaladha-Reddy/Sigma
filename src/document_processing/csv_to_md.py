import pandas as pd
from pathlib import Path
import os

def convert_table_to_md(table_path: str | Path) -> Path:
    """
    Convert a single table file (CSV or JSON) to Markdown in-place directory.

    - Reads the table (CSV or JSON) into a DataFrame.
    - Cleans GLYPH<216> artifacts in text columns.
    - Saves a .md file with the same name in the same folder.
    - Returns the Path to the .md file.
    """
    input_path = Path(table_path)

    if not input_path.exists():
        print(f"Error: The file {input_path} was not found.")
        return input_path.with_suffix(".md")  # dead path, but keeps type

    try:
        # Load according to extension
        if input_path.suffix.lower() == ".csv":
            df = pd.read_csv(input_path)
        elif input_path.suffix.lower() == ".json":
            df = pd.read_json(input_path)
        else:
            print(f"Skipping non-tabular file: {input_path}")
            return input_path.with_suffix(".md")

        for col in df.select_dtypes(include=["object"]).columns:
            if df[col].str.contains("GLYPH<216>").any():
                df[col] = df[col].str.replace("GLYPH<216>", "<br>• ", regex=False)
                df[col] = df[col].str.replace(r"^<br>• ", "• ", regex=True)


        output_path = input_path.with_suffix(".md")
        df.to_markdown(output_path, index=False)

        print(f"Success! Converted table:")
        print(f"  From: {input_path}")
        print(f"  To:   {output_path}")

        return output_path

    except Exception as e:
        print(f"An error occurred when converting {input_path}: {e}")
        return input_path.with_suffix(".md")