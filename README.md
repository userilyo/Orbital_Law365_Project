# Short project Project for Orbital

# Create a solution to extract data from a pdf file.

## 1. Setting the environment:
- Create a folder Data/Input with the given pdf "Official_Copy_Register_EGL363613.pdf"
- Create a folder  Data/Output where extracted data will be collected.
- Create a virtual environment with the requirements.txt, script has been build with python version 3.11.5;
- The file requirements-dev.txt will give a details of my python environments.

## 2. Running the script:

- The solution's script is in python and defined as main.py file.
- We need to have an "OPENAI_API_KEY" to run fully the script.

## 2. Extracting data or collecting script:

- Three main csv types of files are created after extraction:
    - 1. A table_X.csv which is an extraction of each table from each page. 
    The data of every single pdf page is extracted then save as csv file. 
    Tabula use to segregate data in columns data of the schedule of notices of leases.

    - 2. A merged csv table concatenating all merged csv table is created
    This give a clear representation of all columns data:
    •	Registration date and plan reference
    •	Property description
    •	Date of lease and term
    •	Lessee’s title
    •	Note
    
    - 3. A final table called merged_tables_chatgpt used Chatgpt to split properly all columns data is created. 
    This final table display extracted data from the pdf. We have tried to improve the split by using different prompt and different models.
    Best results was achieved with the lates chat gpt model gpt-4o and the prompt1 described in the explicative note.
 
 - An output folder containing all csv extracted after running the scripts. 
