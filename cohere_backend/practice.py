import cohere
from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

co = cohere.Client(COHERE_API_KEY)

loader = AsyncChromiumLoader(["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"])
docs = loader.load()
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(
    docs, tags_to_extract=['p', 'li', 'div', 'a',"span"]
)

attributes = ['book_author', 'book_price', 'book_name', 'book_rating']
joined_attributes = ", ".join(attributes)


# html_content = """
# Books to Scrape (../../index.html) We love being scraped!        Home (../../index.html)    Books (../category/books_1/index.html)    Poetry (../category/books/poetry_23/index.html)   A Light in the Attic         Start of product page               A Light in the Attic  £51.77   In stock (22 available)        <small><a href="/catalogue/a-light-in-the-attic_1000/reviews/"> 0 customer reviews </a></small>  <a id="write_review" href="/catalogue/a-light-in-the-attic_1000/reviews/add/#addreview" class="btn btn-success btn-sm"> Write a review </a>   Warning! This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.  /col-sm-6  /row   Product Description   It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more   Product Information     UPC a897fe39b1053632    Product Type Books    Price (excl. tax) £51.77    Price (incl. tax) £51.77    Tax £0.00    Availability  In stock (22 available)    Number of reviews  0        End of product page
# """

html_content = docs_transformed[0].page_content
# attributes = "book_author, book_price, book_name, book_rating"

#rewrite the message variable to set the html_content variable inside

message = f"""
You are an expert data extractor. You are given partial HTML content and a set of schema/attributes. Both are delimited by triple ```. Your job is to extract the attribute values from the HTML content. The output should only contain a json dictionary of attribute key and attribute extracted value. Do not output anything else.
HTML content:
```
{html_content}
```
Attribute values:
```
{joined_attributes}
```
"""

response = co.chat(
	message=message, 
	model="command", 
	temperature=0.0
)

answer = response.text
dictionary = eval(answer)
print(type(dictionary))
print(dictionary)
