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

  //Global Variables
  const csrftoken = getCookie('csrftoken');
  var selectedChats = new Array();
  var answers = {};
  var isScrolling = false;

  // Scroll Function
  $('.scrollbar-macosx').scrollbar({
    "autoUpdate": true
  });

  // Scroll-fix: Auto scroll disable on user scroll
  $('.chat-container.scroll-content').scroll(function() {

    // console.log("Change detected")
    var $chatContainer = $('.chat-container.scroll-content')[0]
    var chat_scrollTop = $chatContainer.scrollTop
    var chat_scrollHeight = $chatContainer.scrollHeight
    var chat_clientHeight = $chatContainer.clientHeight
    var dispacement = chat_scrollHeight - chat_scrollTop - chat_clientHeight

    // console.log("Scroll dist. from bottom: " + dispacement)
    //Sets status as scrolling and pause auto scroll
    if (dispacement > 200) {
      isScrolling = true;
      // console.log("is scrolling !!");
    }
    //Sets status as NOT scrolling and resume auto scroll
    if (dispacement <= 1 && isScrolling) {
      isScrolling = false;
      // console.log("not scrolling !!");
    }
  });

  // ADD chatInfo block on chatBubble clicked
  function chatInfoTemplateClone(slno, from, text, answered = null) {

    console.log("Cloning chatInfo template")

    var templateContent = document.querySelector('template#chatInfo').content;
    $(templateContent).find(".newPost .content-info .accountName").text(from);
    $(templateContent).find(".newPost .content-info").attr({
      "chat_data_slno": slno
    });
    $(templateContent).find(".newPost .message").text(text);

    var targetContainer = document.querySelector('.jumbotron.chat-info');
    targetContainer.appendChild(document.importNode(templateContent, true));
    if (answered) {
      var $addedTemp = $(targetContainer).find(".newPost:last-child")
      var targetBtn = ".nav-item .nav-link." + answered + "-btn"
      $addedTemp.find(targetBtn).addClass("selected")
    }
  }

  // ADD incoming chat in CHAT BUBBLE
  function chatBubbleTemplate(text, classes) {

    var templateContent = document.querySelector('template#chatBubble').content;
    $(templateContent).find(".bubble").text(text);

    var targetContainer = document.querySelector('div.chat-container.scroll-content');
    targetContainer.appendChild(document.importNode(templateContent, true));
    $(targetContainer).find(".bubble").removeClass("current");
    $(targetContainer).find(".bubble:last-child").addClass(classes);

  }

  function addBubbleClass(slno, classList) {
    var input_info_slno = "input[name='info'][chat_data_slno='" + slno + "' ]";
    var $bubbleElement = $('.chat-container .bubble').find(input_info_slno);
    $bubbleElement.parent().addClass(classList);
  }

  function removeBubbleClass(slno, classList) {
    var input_info_slno = "input[name='info'][chat_data_slno='" + slno + "' ]";
    var $bubbleElement = $('.chat-container .bubble').find(input_info_slno);
    $bubbleElement.parent().removeClass(classList);
  }

  // ADD SELECTED CLASS on bubble-chat clicked
  function addSelected(slno) {
    console.log("Adding selected class");
    if ($.inArray(slno, selectedChats) == -1) {
      selectedChats.push(slno);
    }
    addBubbleClass(slno, "selected")
  }

  // REMOVE selected chats on close-btn clicked
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
    removeBubbleClass(slno, "selected");
    return 1;
  }

  // ADD ANSWER and update chatBubble class
  function addAnswer(slno, answer) {
    answers[slno] = answer
    addBubbleClass(slno, "answered");
  }

  //REMOVE ANSWER and update chatBubble class
  function removeAnswer(slno, answer) {
    delete answers[slno]
    removeBubbleClass(slno, "answered");
  }

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
    //Selecting answered chat
    if (answers[data.slno]) {
      // console.log("Selecting answered chat")
      chatInfoTemplateClone(data.slno, data.from, data.text, answers[data.slno]);
    } else {
      chatInfoTemplateClone(data.slno, data.from, data.text);
    }
  });

  // Function to CLOSE chatInfo container
  function closeContainer(object) {
    $container = $(object).parents("div.newPost")
    slno = $container.find(".content-info").attr("chat_data_slno");
    console.log("Close btn clicked #chatInfo; slno = " + slno);
    var removed = removeSelected(slno);
    if (removed) {
      $container.remove();
    }
  }

  //Close Button clicked on chatInfo
  $("div").on("click", ".newPost .nav-item .close-btn", function() {
    closeContainer(this);
  });

  //Moderation option/answer click trigger function
  function moderationBtnClicked(object, answer) {
    $container = $(object).parents("div.newPost")
    slno = $container.find(".content-info").attr("chat_data_slno");
    if ($(object).is(".selected")) {
      $(object).removeClass("selected")
      removeAnswer(slno, answer);
      console.log("Removed selection")
    } else {
      $container.find(".nav-item .btn").removeClass("selected")
      $(object).addClass("selected")
      addAnswer(slno, answer)
      console.log("Added selection")
    }
    console.log("Updated ans")
    console.log(JSON.stringify(answers))
    updateServerAnswer();
  }

  //Moderation options clicked
  $(document).on("click", ".newPost .nav-item .offensive-btn", function() {
    moderationBtnClicked(this, "offensive");
    closeContainer(this);
  });

  $(document).on("click", ".newPost .nav-item .suspicious-btn", function() {
    moderationBtnClicked(this, "suspicious");
    closeContainer(this);
  });

  $(document).on("click", ".newPost .nav-item .moderate-btn", function() {
    moderationBtnClicked(this, "moderate")
    closeContainer(this);
  });

  $(document).on("click", ".testBtn", function() {

    console.log("hasClass: " + $(this).is(".selected"))
    if ($(this).is(".selected")) {
      $(this).removeClass("selected")
      console.log("removed selection")
    } else {
      $(".newPost .nav-item .btn").removeClass("selected")
      $(this).addClass("selected")
      console.log("selection added")
    }
  });

  // AJAX Request
  setInterval(function() {
    if (document.hasFocus()) {
      $.ajax({
        headers: {
          'X-CSRFToken': csrftoken
        },
        url: $("#url_getChat").attr("data-url"),
        type: 'POST',
        //AJAX request on success function
        success: function(data) {
          if (!data.errorExist) {

            // console.log(data);
            classToAdd = "current"
            if ($.inArray(data.slno, selectedChats) != -1) {
              classToAdd = classToAdd + " selected";
            }
            if (answers[data.slno]) {
              classToAdd = classToAdd + " answered"
            }
            // console.log(classToAdd)
            chatBubbleTemplate(data.chat, classToAdd);

            $('<input>').attr({
              type: 'hidden',
              name: 'info',
              'chat_data_slno': data.slno,
              'chat_data_from': data.from,
              'chat_data_text': data.chat,
              'chat_data_mod': data.moderation
            }).appendTo('.chat-container .current');

            var $chatContainer = $('.chat-container.scroll-content')[0]
            var chat_scrollTop = $chatContainer.scrollTop
            var chat_scrollHeight = $chatContainer.scrollHeight
            var chat_clientHeight = $chatContainer.clientHeight

            // console.log("scrollTop:" + chat_scrollTop)
            // console.log("scrollHeight:" + chat_scrollHeight)

            if (!isScrolling) {
              $(".chat-container.scroll-content").animate({
                scrollTop: $chatContainer.scrollHeight -
                  chat_clientHeight
              }, 800);
            }

          } else {
            console.log("No data");
          }
        }
      });
    }
  }, 3000);

  $.ajax({
    headers: {
      'X-CSRFToken': csrftoken
    },
    url: '',
    type: 'POST',
    success: function(data) {
      if (!data.errorExist) {
        console.log("answers recieved!")
        answers = data
      }
      else {
        console.log("Answers does not exist!")
      }
    }
  });

  $('.timer').startTimer({
    elementContainer: "span",
    onComplete: function () {
      submitAnswer()
    }
  });

  function submitAnswer() {
    // delay(1000);
    $.ajax({
      headers: {
        'X-CSRFToken': csrftoken
      },
      url: $("#url_submitTest").attr("data-url"),
      type: 'POST',
      data: answers,
      success: function(data) {
        if (data.status == 1) {
          console.log("+score:" + data.score_plus)
          console.log("-score:" + data.score_minus)
          urlhead = $("#url_testSubmitted").attr("data-url")
          url = urlhead + data.score_plus + "/" + data.score_minus
          window.location.replace(url);
        }
      }
    });
  }

  function updateServerAnswer() {
    $.ajax({
      headers: {
        'X-CSRFToken': csrftoken
      },
      url: $("#url_updateAnswer").attr("data-url"),
      type: 'POST',
      data: answers,
      success: function(data) {
        console.log(data)
      }
    });
  }

});
