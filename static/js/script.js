function regAPI(api_key){

    $.ajax({
      type: "POST",
      url: "/acc/regAPI/",
      data: {
        'api_key' : api_key,
        'email': document.getElementById("email").value,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function(msg){
        // console.log(msg)
        response = JSON.parse(msg);
        document.getElementById("key").value = response['api_key'];
        location.reload();
      }
    });
}


function shortURL(){
    link = document.getElementById("link").value;
    $.ajax({
      type: "POST",
      url: "/api/v1/",
      data: {
        'link' : link,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function(msg){
        response = JSON.parse(msg);
        document.getElementById("lid").value = '/'+response['surl'];
      }
    });
  }

