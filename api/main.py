from typing import List
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

books = popular_books.to_dict(orient="records")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request, "books": books})



# def recommend(book_name):
# 	index = pt.index.get_loc(book_name)
# 	similarity_scores = list(enumerate(cosine_similarity(pt)[index]))
# 	similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
# 	similarity_scores = similarity_scores[1:6]
# 	book_indices = [i[0] for i in similarity_scores]
# 	recommended_books = pt.index[book_indices]
# 	return recommended_books

# @app.get("/recommended")
# def get_recommended(query: str = Query(..., description="Search by title, author, or genre"), Depends=Depends(recommend)):
#     """
#     Search for books by title, author, or genre and return recommendations.
#     """
#     query_lower = query.lower()
# 	books = popular_books.to_dict(orient="records")

# 	recommendations = recommend(query_lower)
#     if recommendations:
#         return {"query": query, "recommendations": recommendations}
#     return JSONResponse(
#         content={"message": "No books found for the given query.", "query": query},
#         status_code=404
#     )

# def recommend(book_name: str):
#     """
#     Recommend 5 similar books based on cosine similarity.
#     """
#     if book_name not in pt.index:
#         return []
#     index = pt.index.get_loc(book_name)
#     print(f"{index=}")
#     similarity_scores = list(enumerate(cosine_similarity(pt)[index]))
#     similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
#     similarity_scores = similarity_scores[1:6]
#     book_indices = [i[0] for i in similarity_scores]
#     recommended_books = [{"Book-Title": pt.index[i]} for i in book_indices]
#     print(recommended_books)
#     return recommended_books

# def recommend(book_name):
# 	index = np.where(pt.index == book_name)[0][0]
# 	similar_items = sorted(list(enumerate(cosine_similarity(pt)[index])), key=lambda x: x[1], reverse=True)[1:6]
# 	data = []
# 	for i in similar_items:
# 		item = []
# 		temp_df = books[books['Book-Title'] == pt.index[i[0]]]
# 		item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
# 		item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
# 		item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
# 		item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
# 		item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
		
# 		data.append(item)
# 	return data


# @app.get("/recommended", response_class=HTMLResponse)
# async def get_recommended(request: Request, query: str = Query(...)):
#     """
#     Handle search queries and return the dynamically recommended books.
#     """
#     recommendations = recommend(query)
#     print(recommendations)
#     if not recommendations:
#         return JSONResponse(
#             content={"message": "No books found for the given query.", "query": query},
#             status_code=404,
#         )
#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "books": recommendations,
#             "search_query": query,
#         },
#     )

# books = pd.read_csv('dataset/Books.csv', dtype={'column_name': 'str'}, low_memory=False)
# books = books.to_dict(orient="records")

def recommend(book_name: str):
    """
    Recommend 5 similar books based on cosine similarity.
    """
    if book_name not in pt.index:
        raise ValueError("Book not found in the database.")
    
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(cosine_similarity(pt)[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = popular_books[popular_books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        
    data.append(item)
    return data

print(recommend("Zoya"))

from pydantic import BaseModel
from typing import List

class BookRecommendation(BaseModel):
    title: str
    author: str
    year: str
    publisher: str
    image_url: str

from fastapi import HTTPException

@app.get("/recommend", response_model=List[BookRecommendation])
def recommend(book_name: str):
    """
    Recommend 5 similar books based on cosine similarity.
    """
    if book_name not in pt.index:
        raise HTTPException(status_code=404, detail="Book not found in the database.")
    
    # Get the index of the book in the pivot table
    index = np.where(pt.index == book_name)[0][0]
    
    # Compute cosine similarity and sort similar items
    similar_items = sorted(
        list(enumerate(cosine_similarity(pt)[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]  # Exclude the first item (itself)
    
    recommendations = []
    for i in similar_items:
        temp_df = popular_books[popular_books['Book-Title'] == pt.index[i[0]]]
        temp_df = temp_df.drop_duplicates('Book-Title')
        if not temp_df.empty:
            recommendation = BookRecommendation(
                title=temp_df['Book-Title'].values[0],
                author=temp_df['Book-Author'].values[0],
                year=str(temp_df['Year-Of-Publication'].values[0]),
                publisher=temp_df['Publisher'].values[0],
                image_url=temp_df['Image-URL-L'].values[0]
            )
            recommendations.append(recommendation)
    
    return recommendations
