from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logging.basicConfig(filename="log.txt",level=logging.INFO)

# Load your data
popular_books = pickle.load(open("popular_top_25_book_df.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
book_title = pickle.load(open("books.pkl", "rb"))

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="./templates")

# books = popular_books.to_dict(orient="records")
books = pd.read_csv("../Book_Recommendation/dataset/Books.csv")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request, "popular_books": popular_books.to_dict(orient="records")})


def recommend(book_name):
	index = np.where(pt.index == book_name)[0][0]
	similar_items = sorted(list(enumerate(cosine_similarity(pt)[index])), key=lambda x: x[1], reverse=True)[1:6]
	data = []
	for i in similar_items:
		item = []
		temp_df = books[books['Book-Title'] == pt.index[i[0]]]
		item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
		item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
		item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
		item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
		item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
		
		data.append(item)
	return data


from pydantic import BaseModel
from typing import List

class BookRecommendation(BaseModel):
    title: str
    author: str
    year: str
    publisher: str
    image_url: str


@app.get("/recommend", response_class=HTMLResponse)
async def get_recommendation(request: Request,query: Optional[str]=Query(None)):
    logging.info(f"Recommendation for {query}")
    recommendation = recommend(query)
	# print(recommendation)
    return templates.TemplateResponse("recommend.html",  context={"request": request,"recommendation": recommendation})
