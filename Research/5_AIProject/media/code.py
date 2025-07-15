# Notes
# All prompts can be run with separate queries or in one 'thread' -> all data is repeated if necessary for return generation
# However, Factcheck functions are most accurate when used separately, this reduces hallucination and breaks cycles of incorrect data
# Standard JSON objects are used to represent data within the AI model
# It seems easier to manipulate these objections 'server side' (aka away from the LLM) and leave the model to produce consistent results, even if less useful
# There has been a variety of prompt iteration and these were found to perform best on both: GPT4 and (if running locally) qwen2.5-14b-instruct.
# A variety of other local models were tested (Llama 3.2 1 & 3B, Gemma 2 9B, Mistral 7B v0.3, qwen2.5-14b-instruct) results below
# - Llama was occasionally better at interpreting vaguer DB scheme prompts and producing more detailed schemas but really struggled to return valid JSON data even when strictly instructed
# - Gemma (similarly to Llama) was too 'chatty' and additionally ran slower
# - Mistral faced frequent 'hallucination' and was poor at checking for detail but did seem to have a strong grasp of the required data formats
# qwen 2.5 provided a good balance of creativity whilst maintaining high accuracy (especially numerical), it relies on low operating temperature however
# I only had a few gpt4 tokens (free limit per day) however from this testing it seems to respond similarly to qwen but with even greater ability to grasp context. It should be 'plug and play' to utilise OpenAI services
# using these more accurate models fact checking rarely seemed necessary (not enough to justify multiple Api calls for every request) however these models weren't able to correctly convey their certainty meaning it will be difficult to catch truly incorrect data (and inform the user if necessary)
# -------------Demo run------------
# DB Schema prompt: Store Security system information including installers and event log.
# Result:
# ------- Installations
# id: integer
# installer: string
# location: string
# installationDate: string
# ------- SecuritySystems
# id: integer
# model: string
# serialNumber: string
# installationId: Installations.id
# ------- EventLogs
# id: integer
# securitySystem: SecuritySystems.id
# eventType: multiselect: ['alarm', 'entry', 'exit', 'maintenance']
# timestamp: string
# details: string
# record fill prompt: I have 2 security systems installed by locosecure. one is a Samsung system and the other is ubiquity. the Samsung system is at my London property and has had 2 alarms, 1 was me entering my house but the other wasn't. the other system is in America and has only triggered twice on the 27th February as it was in maintenance
# ------- Installations -------
#   id: 1
#   installer: locosecure
#   location: london property
#   installationDate: none
#   id: 2
#   installer: locosecure
#   location: america
#   installationDate: none

# ------- SecuritySystems -------
#   id: 1
#   model: samsung
#   serialNumber: none
#   installationId: 1
#   id: 2
#   model: ubiquiti
#   serialNumber: none
#   installationId: 2

# ------- EventLogs -------
#   id: 1
#   securitySystem: 1
#   eventType: ['alarm', 'entry']
#   timestamp: none
#   details: me entering my house
#   id: 2
#   securitySystem: 1
#   eventType: ['alarm']
#   timestamp: none
#   details: not specified
#   id: 3
#   securitySystem: 2
#   eventType: ['maintenance']
#   timestamp: 2024-02-27
#   details: system maintenance
  
  
import requests
import json
def aifillrecord(inputData, databaseSchema, temperature, model, api):
    
    # The URL / Ai endpoint where the local server is running / api enpoint is
    url = api
    headers = {
        "Content-Type": "application/json"
    }
    # JSON data payload
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": '''Task:
            Format the prompt into a json file strictly following this schema:
            ''' + databaseSchema + '''
            Instructions:
                •   Do not modify the schema.
                •   Return all fields for each entry.
                •   If a field is missing, input “none.”
                •   Use only accurate data from the prompt; do not create or guess information.
                •   Ignore irrelevant details.
                •   Split names logically into “First Name” and “Last Name.”
                • you may return multiple records
                •   Output the result as a json object with no extra commentary or punctuation beyond commas.
            Requirements:
                •   Every record must be complete and follow the exact format.
                •   Each variable should be a single string.
                •   Ensure response is correctly formatted in JSON.
                •   if you are completing multiple records, ensure they are grouped together under their collection name eg

            "CollectionName": [
                {
                "id": 1,
                "Customer": "1",
                "Priority": "medium",
                "IssueSummary": "Unable to Access Account"
                },
                {
                "id": 2,
                "Customer": "2",
                "Priority": "high",
                "IssueSummary": "Payment Processing Error"
                },
                {
                "id": 3,
                "Customer": "3",
                "Priority": "low",
                "IssueSummary": "Request for Invoice Copy"
                }
                ]

            '''},
            {"role": "user", "content": inputData}
        ],
        "temperature": temperature,
        "max_tokens": -1,
        "stream": False
    }
    # Making the POST request to the local server
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Checking if the request was successful
    if response.status_code == 200:
        # Printing the response content
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return(response_json["choices"][0]["message"]["content"])
        else:
            print("No content found in the response.")
    else:
        print("Failed to get response:", response.status_code, response.text)
# make a second request to the AI to fact check that the first response follows the provided structure -- unused with 'stronger' ai models
def aifactcheckrecord(structure, prompt, record, model, api):
  
    url = api
    # The headers to indicate that we are sending JSON data
    headers = {
        "Content-Type": "application/json"
    }
    # The JSON data payload
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": '''
             
            You are an AI tool for fact-checking my work. I have:
                1.  A database schema.
                2.  A prompt with data I am using to automatically populate the schema.
                3.  A prior attempt with records filled based on the prompt data.
            Please review the records I created and make any necessary corrections to ensure accuracy and consistency with the prompt data. Return only the corrected JSON object if changes are made. If no corrections are needed, return the unchanged JSON object.
            Only return the JSON object—no additional output. '''},
            {"role": "user", "content": "Database Schema: " + structure + "Data: " + prompt + "JSON record: " + record}
        ],
        "temperature": 0,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return(response_json["choices"][0]["message"]["content"])
        else:
            print("No content found in the response.")
    else:
        print("Failed to get response:", response.status_code, response.text)
# select the best version of multiple ai prompt return calls -- unused with 'stronger' ai models
def airecordselector(v1, v2, v3, prompt, model, api):
    # The api endpoint
    url = api
    headers = {
        "Content-Type": "application/json"
    }
    # The JSON data payload
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": '''respond by selecting the the best filled in database record completed from information within the data provided. ensure you return the V number of your options integer as the first digit of your response (1, 2 or 3) with no charectors before that, and then give feedback on why you made that choice. if you think suitable, you can provide a combination of data and output the most accurate JSON record object you can. However do not fabricate data and only use content from the source material'''},
            {"role": "user", "content": "the data supplied was: " + prompt + "Json objects produced - V1: " + v1 + "V2: " + v2 + "V3: " + v3}
        ],
        "temperature": 0,
        "max_tokens": -1,
        "stream": False
    }
    # POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return(response_json["choices"][0]["message"]["content"])
        else:
            print("No content found in the response.")
    else:
        print("Failed to get response:", response.status_code, response.text)
def aifillschema(inputData, temperature, model, api):
    # API endpoint
    url = api
    headers = {
        "Content-Type": "application/json"
    }
    # The JSON data payload
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": '''You are an AI assistant tasked with assisting a user in building a database system by generating multiple data collections and data fields based on the provided prompt. Present the collections response strictly in the json format below:
        "collectionName": {
            "fieldName": "type",
            "fieldName": "type",
            "fieldName": "type"
        },
           give each collection a sensible name, not collectionName
        to minimise data replication, always try to reference other collection's fields and if you want to reference other collection's fields use this format:
        "fieldname": otherCollectionName.fieldName
        aim for the minimal number of collections to produce simple outputs.
        Each field can ONLY be one of the following data types: 
        integer,
        string,
        a reference to another collection you generate in the format -
        "fieldname": otherCollectionName[fieldName]
        a multiselect containing a preset list of values you decide on in this format -
        "fieldname": "multiselect: ['option1', 'option2', 'option3']"
        you cannot use lists and arrays as field types
        
        Do not provide any additional explanations or commentary only the json object you output.
        for example:
        if the prompt was: "Track devices issued to employees"
        you might return:
        {
        "Devices": {
            "id": "integer",
            "serial": "string",
            "type": "string",
            "age": "string"
        },
        "Employees": {
            "id": "integer",
            "name": "string",
            "department": "string"
        },
        "Deployments": {
            "id": "integer",
            "device": "Devices.id",
            "employee": "Employees.id"
        }
        }
        '''},
            {"role": "user", "content": inputData}
        ],
        "temperature": temperature,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return(response_json["choices"][0]["message"]["content"])
        else:
            print("No content found in the response.")
    else:
        print("Failed to get response:", response.status_code, response.text)
        
#very unoptimal but working function to restructure AI gen JSON DB schema for manipulation
def transform_json_to_storage(json_string):
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        return "fail"
    storage = {}
    for section, fields in data.items():
        collection_name = section
        field_names = [field_name for field_name, _ in fields.items()]
        field_types = [field_type for _, field_type in fields.items()]
        storage[collection_name] = {
            "fields": {
                field_name: field_type for field_name, field_type in zip(field_names, field_types)
            },
            "references": {}
        }
    return storage
#Program logic
choice1 = input("Would you like to (U)pload database schema or (G)enerate: ")
if choice1.lower() == "u":
    databaseSchema = input("Enter your database Scheme in JSON form: ")
elif choice1.lower() == "g":
    #generate DB schema
    prompt = input("Please enter your generation prompt: ")
    databaseSchema = aifillschema(prompt, 0, 'qwen2.5-14b-instruct', 'http://localhost:1234/v1/chat/completions')
    processedDatabaseSchema = transform_json_to_storage(databaseSchema)
    print("Generated")
    print("\n")
    for collection in processedDatabaseSchema:
        print("-------", collection)
        for field, details in processedDatabaseSchema[collection]["fields"].items():
            if details == "string":
                print(f"\033[94m{field}: {details}\033[0m")  # Blue for strings
            elif details == "integer":
                print(f"\033[92m{field}: {details}\033[0m")  # Green for integers
            elif "multiselect" in details:
                print(f"\033[91m{field}: {details}\033[0m")  # Red for multiselect
            elif "." in details:
                print(f"\033[95m{field}: {details}\033[0m")  # Pink for references
            else:
                print(f"{field}: {details}")  
    print("\n")
    print("\n")
    
    choice1 = input("Would you like to view source? y/n: ")
    if choice1.lower() == 'y':
        print(databaseSchema)
continueGeneratingRecords = True
while True:
    choice2 = input("Would you like to generate records? y/n: ")
    if choice2.lower() == "y" or choice2.lower() == "n":
        break
if choice2.lower() != "y":
    continueGeneratingRecords = False
while continueGeneratingRecords == True:
    prompt = input("Please enter your record data: ")
    
    # option to read record data from file:
    # with open('software-tests-2024-10-25.txt', 'r') as file:
    #     prompt = file.read()
    records = aifillrecord(prompt, databaseSchema, 0, 'qwen2.5-14b-instruct', "http://localhost:1234/v1/chat/completions")
    recordCopy = records # to store JSON objects for export
    processedRecords = json.loads("[ " + records + " ]")
    # Define colors for each collection type
    COLORS = [
        "\033[91m",  # Red
        "\033[92m",  # Green
        "\033[94m",  # Blue
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
        "\033[93m"   # Yellow
    ]
    reset_color = "\033[0m"
    
    grouped_records = {}
    # Group records by collection type
    for item in processedRecords:
        for collection_type, records in item.items():
            if collection_type not in grouped_records:
                grouped_records[collection_type] = []
            grouped_records[collection_type].extend(records) 
    # Assign a color to each unique collection
    collection_colors = {
        collection: COLORS[i % len(COLORS)]
        for i, collection in enumerate(grouped_records.keys())
    }
    # Display grouped data
    for collection_type, records in grouped_records.items():
        color = collection_colors.get(collection_type, reset_color)
        print(f"{color}------- {collection_type} -------{reset_color}")
        
        for record in records:
            for field, value in record.items():
                print(f"{color}  {field}: {value}{reset_color}")
            print()
        print()
        
        
    choice2 = input("Would you like to view raw? y/n: ")
    if choice2.lower() == "y":
        print(recordCopy)
    choice2 = input("Would you like to continue generating records? y/n: ")
    if choice2.lower() == "n":
        continueGeneratingRecords = False