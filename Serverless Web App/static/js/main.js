$(document).ready(() => {
  $("#searchForm").on('submit', (e) => {
    e.preventDefault();
    let searchText = $("#searchText").val();
    getMovies(searchText);
  });
});

function getMovies(searchText){
  //make request to api using axios
  // Make a request for a user with a given ID
  axios.get("https://api.themoviedb.org/3/search/movie?api_key=98325a9d3ed3ec225e41ccc4d360c817&language=en-US&query=" + searchText)
    .then(function (response) {
      let movies = response.data.results;
      let output = '';
      $.each(movies, (index, movie) => {
        output+=`
          
        <div  style="border:10px solid RGB(30, 70, 138);">
        <br>
              <img class="center" src="https://image.tmdb.org/t/p/w500${movie.poster_path}" style="width:700;height:400;box-shadow: 5px 10px;">
              <a onclick="movieSelected('${movie.id}')"  class="btn btn-primary" href="#" target="_blank"><h2 class="active underlineHover"><b>${movie.title}</b></h2></a>
              <span id="circle">${movie.vote_average}</span>
              <br><br>
              <form method=POST action="{{url_for('movies')}}" target="dummyframe">
              <input class="fadeIn second"  type=hidden name="titleID" value=${movie.id} >
              <p>Rating:</p><br>
              <input  class="fadeIn third" type="number" name="rating" min="1" max="10"  placeholder="     0-10" >
              <br>
              <input  type='submit' class="fadeIn fourth" value="submit"  >
              </form>
              
          
        </div>
        `;
      });
      $('#movies').html(output);
    })
    .catch(function (error) {
      console.log(error);
    });
}

function movieSelected(id){
  sessionStorage.setItem('movieId', id);
  window.location = 'movie.html';
  return false;
}

function getMovie(){
  let movieId = sessionStorage.getItem('movieId');
  // Make a request for a user with a given ID
  axios.get("https://api.themoviedb.org/3/movie/" + movieId + "?api_key=98325a9d3ed3ec225e41ccc4d360c817")
    .then(function (response) {
    let movie = response.data;
    //console.log(movie);
    let output = `
        <div class="row">
          <div class="col-md-4">
            <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" class="thumbnail">
          </div>
          <div class="col-md-8">
            <h2>${movie.title}</h2>
            <ul class="list-group">
              <li class="list-group-item"><strong>Genre:</strong> ${movie.genres[0].name}, ${movie.genres[1].name}</li>
              <li class="list-group-item"><strong>Released:</strong> ${movie.release_date}</li>
              <li class="list-group-item"><strong>Rated:</strong> ${movie.vote_average}</li>
              <li class="list-group-item"><strong>Runtime:</strong> ${movie.runtime} min.</li>
              <li class="list-group-item"><strong>Production Companies:</strong> ${movie.production_companies[0].name} min.</li>
              <br>
              <h4>User Submission</h2>
              <form class = "list-group" method=POST action="http://127.0.0.1:5000/login">
              <input id="titleID" type=hidden value=${movie.id}>
              <label>Rating:</label>
              <input id="rating" class="list-group-item" type="number" id="quantity" name="quantity" min="1" max="10"><br>
              <label>Comments:</label>
              <textarea id="comment" class="list-group-item" placeholder="Optional" rows="4" cols="50"></textarea><br>
              </form>
            </ul>
          </div>
        </div>
        <div class="row">
          <div class="well">
            <h3>Plot</h3>
            ${movie.overview}
            <hr>
            <a href="http://imdb.com/title/${movie.imdb_id}" target="_blank" class="btn btn-primary">View IMDB</a>
            <a href="index.html" class="btn btn-default">Go Back To Search</a>
          </div>
        </div>
    `;
    $('#movie').html(output);
    })
    .catch(function (error) {
      console.log(error);
    });
}
