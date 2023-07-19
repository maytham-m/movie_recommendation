
from flask import Flask, render_template, request
import openai
import os
import requests


app = Flask(__name__)

openai.api_key = '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'

TMDB_API_KEY = 'e535cf0cf528b193b4a5e09d78bc68f0'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'

OMDB_API_KEY = '9d4828d8'

@app.route('/')
def home():
    return render_template('index.html')





@app.route('/recommend', methods=['POST'])
def recommend():

    movies = request.form['movies']
    movies = [movie.strip() for movie in movies.split(',')]

    prompt = f"I have recently watched these movies: {', '.join(movies)}. Based on these, can you recommend some other movies I might enjoy?"

    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=100
    )

    recommendations = response.choices[0].text.strip().split(',')
    print(recommendations)
    recommendations = [rec.split('\n') for rec in recommendations][0][:5]
    print(recommendations)
    # ... existing code ...

    # Get movie posters, overviews, and IMDb ratings
    recommendations_with_details = []
    for rec in recommendations:
        response = requests.get(
            f'{TMDB_BASE_URL}/search/movie',
            params={
                'api_key': TMDB_API_KEY,
                'query': rec[3:-7],
            }
        )
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            overview = data['results'][0]['overview']

            # Get IMDb rating from OMDb API
            response = requests.get(
                'http://www.omdbapi.com/',
                params={
                    'apikey': OMDB_API_KEY,
                    't': rec[3:-7],
                }
            )
            data = response.json()
            imdb_rating = data.get('imdbRating', 'No IMDb rating found')

            recommendations_with_details.append((rec, TMDB_IMAGE_URL + poster_path, overview, imdb_rating))
        else:
            recommendations_with_details.append((rec, 'No poster found', 'No overview found', 'No IMDb rating found'))

    return render_template('recommendations.html', recommendations=recommendations_with_details)





if __name__ == '__main__':
    app.run(debug=True)
