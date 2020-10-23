$(document).ready(function() {

  // Acquire CSRF Token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  setInterval(function() {
    $.ajax({
      headers: {
        'X-CSRFToken': csrftoken
      },
      url: 'getchat/',
      type: 'POST',
      success: function(data) {
        if (data) {
          console.log(data);
          var $currentbubble = $('.chat-container .bubble.current');
          $bubble = $currentbubble.clone().text(data)
          $currentbubble.removeClass("current")
          $bubble.appendTo(".chat-container")

          var $chatContainer = $('.chat-container')[0]
          var chat_scrollTop = $chatContainer.scrollTop
          var chat_scrollHeight = $chatContainer.scrollHeight
          var chat_clientHeight = $chatContainer.clientHeight

          console.log("scrollTop:" + chat_scrollTop)
          console.log("scrollHeight:" + chat_scrollHeight)

          // $('.chat-container').animate({
          //   scrollTop: chat_scrollHeight - chat_clientHeight
          // }, 800);

          $(".chat-container").animate({
                    scrollTop: $(
                      '.chat-container').get(0).scrollHeight
                }, 800);

        } else {
          console.log("No data");
        }
      }
    });
  }, 3000);

  $(".chat-container::-webkit-scrollbar-thumb").on("mousedown", function() {
    console.log("Pressed");
  });
});
