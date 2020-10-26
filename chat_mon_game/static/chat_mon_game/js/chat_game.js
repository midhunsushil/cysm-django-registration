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

  var selectedChats = new Array()

  function chatInfoTemplateClone(slno, from, text) {

    console.log("Cloning chatInfo template")
    var templateContent = document.querySelector('template#chatInfo').content;
    $(templateContent).find(".newPost .content-info .accountName").text(from);
    $(templateContent).find(".newPost .content-info").attr({
      "chat_data_slno": slno
    })
    $(templateContent).find(".newPost .message").text(text);


    var targetContainer = document.querySelector('.jumbotron.chat-info');
    targetContainer.appendChild(document.importNode(templateContent, true));

  }

  function chatBubbleTemplate(text, classes) {

    var templateContent = document.querySelector('template#chatBubble').content;
    $(templateContent).find(".bubble").text(text);

    var targetContainer = document.querySelector('div.chat-container');
    targetContainer.appendChild(document.importNode(templateContent, true));
    $(targetContainer).find(".bubble").removeClass("current");
    $(targetContainer).find(".bubble:last-child").addClass(classes);

  }

  function addSelected(slno) {
    console.log("Adding selected class");
    if ($.inArray(slno, selectedChats) == -1) {
      selectedChats.push(slno);
    }
    var input_info_slno = "input[name='info'][chat_data_slno='" + slno + "' ]";
    var $bubbleElement = $('.chat-container .bubble').find(input_info_slno);
    $bubbleElement.parent().addClass("selected");
  }

  function removeSelected(slno) {
    console.log("Removing selected class");
    if ($.inArray(slno, selectedChats) == -1) {
      console.log("Unable to remove selected !");
      return 0
    } else {
      selectedChats = $.grep(selectedChats, function(value) {
        return value != slno;
      });
    }
    var input_info_slno = "input[name='info'][chat_data_slno='" + slno + "' ]";
    var $bubbleElement = $('.chat-container .bubble').find(input_info_slno);
    $bubbleElement.parent().removeClass("selected");
    return 1;
  }

  setInterval(function() {
    if (document.hasFocus()) {
      $.ajax({
        headers: {
          'X-CSRFToken': csrftoken
        },
        url: 'getchat/',
        type: 'POST',
        success: function(data) {
          if (!data.errorExist) {

            console.log(data);

            if ($.inArray(data.slno, selectedChats) == -1) {
              chatBubbleTemplate(data.chat, "current");
            } else {
              chatBubbleTemplate(data.chat, "current selected");
            }

            $('<input>').attr({
              type: 'hidden',
              name: 'info',
              'chat_data_slno': data.slno,
              'chat_data_from': data.from,
              'chat_data_text': data.chat,
              'chat_data_mod': data.moderation
            }).appendTo('.chat-container .current');

            var $chatContainer = $('.chat-container')[0]
            var chat_scrollTop = $chatContainer.scrollTop
            var chat_scrollHeight = $chatContainer.scrollHeight
            var chat_clientHeight = $chatContainer.clientHeight

            console.log("scrollTop:" + chat_scrollTop)
            console.log("scrollHeight:" + chat_scrollHeight)

            $(".chat-container").animate({
              scrollTop: $(
                '.chat-container').get(0).scrollHeight
            }, 800);

          } else {
            console.log("No data");
          }
        }
      });
    }
  }, 3000);

  $(".chat-container::-webkit-scrollbar-thumb").on("mousedown", function() {
    console.log("Pressed");
  });

  //Chat bubble clicked/selected
  $(".chat-container").on("click", ".bubble:not(.selected)", function() {

    console.log('Clicked Chat!')

    $inputInfo = $(this).children("input[name = 'info']")
    console.log($inputInfo)

    data = {
      slno: $inputInfo.attr('chat_data_slno'),
      from: $inputInfo.attr('chat_data_from'),
      text: $inputInfo.attr('chat_data_text'),
      mod: $inputInfo.attr('chat_data_mod')
    }

    addSelected(data.slno);
    chatInfoTemplateClone(data.slno, data.from, data.text);
  });
  //Chat bubble clicked/selected END

  //Close Button clicked on chatInfo
  $("div").on("click", ".newPost .nav-item .close-btn", function() {

    $container = $(this).parents("div.newPost")
    slno = $container.find(".content-info").attr("chat_data_slno");
    console.log("Close btn clicked #chatInfo slno = " + slno);
    var removed = removeSelected(slno);
    if (removed) {
      $container.remove();
    }
  });

  if ($('.chat-container')[0].scrollHeight - $('.chat-container')[0].scrollTop > 500) {
    $('.chat-container')[0].scrollTop = $('.chat-container')[0].scrollHeight
  }
});
