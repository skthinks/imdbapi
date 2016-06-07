The given application comprises a wrapper api around imdb

It consists of 2 Parts
1. Search API 
Searches a given word on IMDb and returns the list of movies, along with links
that can be used to access the Info API and get info on desired movie

2. Info API
Gets the movie information based on movie id on IMDb. Can be used stand alone,
but requires prior knowledge of the id. The Search API accesses this API by
providing id to the desired movie

Instructions to use
1. Run Django

2. Run the Search API through
http://localhost:8000/polls/suggest/?q=($movie name)

3. Then:
Use the ID matching the movie to get the result
http://localhost:8000/polls/suggest/?q=($movie id)

