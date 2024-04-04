# LLM-Web-Scraping

**Python Version**:3.11


# Streamlit Frontend

The code for the streamlit frontend is available [here](https://github.com/rukshar/LLM-Web-Scraping/tree/main/streamlit_frontend/scraper_ui.py).

The frontend has 2 fields: 
- URL text input field
- Attributes list input field

Upon clicking the **Extract Attributes** button, the script sends a POST request to a FastAPI API(*ttp://127.0.0.1:8000/extract*) endpoint with the provided URL and attributes.

![frontend](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/streamlit_frontend/frontend.png)

The JSON response from the API is then displayed in the frontend. 

**Fault tolerance** is ensured by keeping the FastAPI API calling logic within try-except blocks. The script displays an error message if the API call fails and the except block handles the error.

## Running the Frontend

Create an Anaconda virtual environment with the following command:
```bash
conda create -n streamlit python=3.11
```

Activate the virtual environment with the following command:
```bash
conda activate streamlit
```

Install the required packages from the requirements.txt file with the following command:
```bash
pip install -r requirements_frontend.txt
```

To run the frontend, run the following command in the terminal:
```bash
streamlit run scraper_ui.py
```

The app runs on the address **http://127.0.0.1:8501**

# OpenAI + LangChain + FastAPI Backend

![Diagram](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/openai_backend/web_scrape_llm.jpg)


## FastAPI API

The FastAPI API(*/extract*) is a RESTful API that takes a URL and a list of attribute names as input and returns the extracted attributes from the webpage after calling a method **scrape_with_playwright** that takes input the URL, the list of attribute names and the LLM. The LLM is set to OpenAI's **gpt-3.5-turbo**. The LLM is loaded here to prevent re-initialization of the LLM in the scrape_with_playwright method.

The code for API is in [fastapi_app.py](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/openai_backend/fastapi_app.py)

## Extracting Scheme Data from Web Page

The code for extracting scheme data from the web page is in [langchain_extractor.py](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/openai_backend/langchain_extractor.py). Specifically, the code resides in the method **scrape_with_playwright**. The inputs to this method are the URL, the list of attribute names and the LLM. In this case, the LLM is OpenAI's **gpt-3.5-turbo**.

LangChain provides playwright-based **AsyncChromiumLoader** and beautiful-soup-based **BeautifulSoupTransformer** to extract the content from the web page.

A schema is constructed with the **properties** and **required** keys using the list of attribute names.

LangChain's **create_extraction_chain** method is then used to extract the information in a JSON-based format using the LLM, the schema, and the clean web page data.

**Fault tolerance** is ensured by keeping the **scrape_with_playwright** method within try-except blocks in the FastAPI API definition. The script displays an error message if the function call fails and the except block handles the error.

## Running the Backend

Create an Anaconda virtual environment with the following command:
```bash
conda create -n backend python=3.11
```

Activate the virtual environment with the following command:
```bash
conda activate backend
```

Install the required packages from the requirements.txt file with the following command:
```bash
pip install -r requirements_backend.txt
```

To run the backend, run the following command in the terminal:
```bash
uvicorn fastapi_app:app --reload
```

The API is available on the address **http://127.0.0.1:8000/extract**

