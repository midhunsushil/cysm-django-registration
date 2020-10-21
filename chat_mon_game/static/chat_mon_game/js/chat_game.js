$(document).ready(function () {

setInterval(function () {
  $.ajax({
        url: 'getchat/',
        success: function (data) {
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

            console.log("scrollTop:"+chat_scrollTop)
            console.log("scrollHeight:"+chat_scrollHeight)

            $('.chat-container').animate({ scrollTop: chat_scrollHeight - chat_clientHeight}, 800);

            // if(chat_scrollHeight > 500) {
            //   console.log("Down!")
            //   $chatContainer.scrollTop = chat_scrollHeight - chat_clientHeight;
            // }
          }
          else {
            console.log("No data");
          }
        }
      });
}, 3000);

});
