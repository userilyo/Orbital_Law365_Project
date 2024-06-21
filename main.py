import pandas as pd
import tabula
import ocrmypdf
import os
import time
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = 'XXXXXXXXXXXXXXXXXXX'  # Set your OpenAI API key here

# Initialize OpenAI client
client = OpenAI()

def pdf_to_digital(file_path, save_path):
    """
    Convert a scanned PDF to a searchable digital PDF using OCR.

    Parameters:
    file_path (str): The path to the input PDF file.
    save_path (str): The path to save the output digital PDF file.
    """
    ocrmypdf.ocr(file_path, save_path, deskew=True, force_ocr=True)

def extract_tables(pdf_path):
    """
    Extract tables from a PDF file using tabula-py.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    list of pd.DataFrame: A list of dataframes representing the extracted tables.
    """
    tables = []
    try:
        tables = tabula.read_pdf(pdf_path, multiple_tables=True, pages='all', encoding='utf-8', guess=False, lattice=False)
        # Combine tables and skip empty rows
        tables = [table.dropna(how='all') for table in tables]
    except Exception as e2:
        print(f"Tabula-py encountered an error for {pdf_path}: {e2}")
    else:
        print(f"Successfully extracted tables from {pdf_path} using tabula-py.")
    return tables

def split_the_data_csv(csv_data):
    """
    Use OpenAI API to split and structure CSV data into a formatted table.

    Parameters:
    csv_data (str): The CSV data as a string.

    Returns:
    str: The structured CSV data.
    """
    max_token_size = 2000  # Adjust as needed to avoid exceeding token limits such as as openai.RateLimitError!
    chunks = [csv_data[i:i + max_token_size] for i in range(0, len(csv_data), max_token_size)]
    structured_data = ""

    for chunk in chunks:
        prompt = f''' I have plain text tabular data, and I need help splitting it into proper columns. 
    Please extract the information and organize it into a structured table with appropriate headers. 
    Return the result as proper strongly comma-separated CSV only. We may have many tables, so split them into tables too. 
    And skip rows without the data. Do not numerate rows. Do not include any comments chatgpt response 
    except the processed data. Put the table name before the each table if possible. 
    Split the Schedule of notices of lease data into separate columns. Do not include additional columns/data at the beginning of each row.


        Data: 

        {chunk}'''

        data = ""
        stream = client.chat.completions.create(
            model="gpt-4o",
            #model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=True,
        )
        for chunk in stream:
            if not chunk.choices:
                continue

            print(chunk.choices[0].delta.content, end="")
            try:
                data += str(chunk.choices[0].delta.content)
            except:
                pass

        structured_data += data

    return structured_data

def save_tables_to_csv(extracted_tables, csv_filename):
    """
    Save extracted tables to CSV files and further process them using OpenAI API.

    Parameters:
    extracted_tables (list of pd.DataFrame): The list of extracted tables.
    csv_filename (str): The filename to save the merged tables CSV.
    """
    if extracted_tables:
        for i, table in enumerate(extracted_tables):
            print(f"\nTable {i + 1}:")
            print(table)
            table_filename = f"/Data/output/table_{i + 1}.csv"
            table.to_csv(table_filename, index=False, encoding='utf-8', sep=";")
            print(f"Table {i + 1} saved as {table_filename}")

        merged_table = pd.concat([t for t in extracted_tables if not t.empty], ignore_index=True)
        merged_table.to_csv(csv_filename, index=True, encoding='utf-8', sep=";")
        csv_data = merged_table.to_csv(index=False)
        data = split_the_data_csv(csv_data)

        
        new_data = data.replace("```csv", "").replace("```", "")
        with open(csv_filename.replace(".csv", "_chatgpt.csv"), "w") as file:
            file.write(new_data)
    else:
        print("No tables found in the PDF.")

def main():
    """
    Main function to process the PDF, extract tables, and save them to CSV files.
    """
    # Start timing the execution
    start_time = time.time()

    # Specify the PDF path
    pdf_path = "/Data/input/Official_Copy_Register_EGL363613.pdf"
    tmp_path = pdf_path.replace(".pdf", "_tmp.pdf")

    # Try to convert PDF to digital PDF
    try:
        pdf_to_digital(pdf_path, tmp_path)
    except:
        tmp_path = pdf_path

    # Extract tables
    extracted_tables = extract_tables(tmp_path)

    # Save tables to CSV
    csv_filename = "/Data/output/merged_tables.csv"
    save_tables_to_csv(extracted_tables, csv_filename)

    # Print the time taken to execute the script
    end_time = time.time()
    print(f"Time taken to execute the script: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
