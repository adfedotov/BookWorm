$(document).ready(function() {
  $('#dashboard-search').on('input', function(e){
    var input = $(this).val();
    $('div.card').each(function(){
      if ($(this).find('h5.card-title').text().search(new RegExp(input, "i")) < 0 && $(this).find('p.card-text').text().search(new RegExp(input, "i")) < 0) {
        $(this).fadeOut();
      } else {
        $(this).show();
      }
    });
  });
});

// Search is only by title for now
function book_request(books) {

  // This is used just to have background example of a card, should be removed
  $("div.book_content").empty();

  // Results are unsorted due to asynchronous requests
  // Also needs to be checked if name/title is undefined
  for (i = 0; i < books.length; i++) {
    $.getJSON({
      url: 'http://openlibrary.org/search.json',
      beforeSend: function(xhr){
        if (xhr.overrideMimeType){
          xhr.overrideMimeType("application/json");
        }
      },
      dataType: 'json',
      data: {q: books[i][1]},
      success: function(book_json) {
        console.log(book_json);
        var lastedition = book_json["docs"][0]["edition_key"].length - 1;
        // error is due to some results not "having" author listed
        $("div.book_content").append('<div class="card m-2" style="width: 18rem;" onclick="location.href=#"><img class="card-img-top" src="http://covers.openlibrary.org/b/olid/' + book_json["docs"][0]["edition_key"][lastedition] + '-M.jpg" alt="Card image cap"><div class="card-body"><h5 class="card-title">' + book_json["docs"][0]["title"].slice(0,40) + '</h5><p class="card-text">by ' + book_json["docs"][0]["author_name"][0] + '</p><a href="#" class="btn btn-primary btn-card">Go somewhere</a></div></div>');
      }
    });
  }
}
