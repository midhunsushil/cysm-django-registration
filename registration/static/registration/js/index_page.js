$(document).ready(function() {
  //jquery add active page to nav-bar
  $(".navbar-nav .nav-item.indexPage").addClass("active");

  // '#I-am-selection' button hover events
  var $active_selection = $(".form-selector .dropdown-item.school")
  update_selection($active_selection);

  $('.btn-group.dropdown').hover(function hoverIn() {

      console.log('Hover over dropdown');
      $('#i-am-selection').dropdown('show');

      // On Dropdown Item Hover
      $('.form-selector .dropdown-item').not(".disabled").hover(function() {

        console.log("Hover over : " + $(this).text());
        update_bgc_class($(this));
        $('#i-am-selection').text($(this).text());

      }, function() {

        console.log("Item Hover leave");
        console.log("Active Selection: " + $active_selection.text());
        update_selection($active_selection);

      });

      // On Dropdown Item Click
      $('.form-selector .dropdown-item').not(".disabled").click(function() {

        console.log("Clicked " + $(this).text());
        $active_selection = $(this);
        console.log("Active Selection: " + $active_selection.text());
        update_selection($active_selection);

      });

    },
    function hoverOut() {

      $('.hovercheck').mouseleave(function() {
        $('#i-am-selection').dropdown('hide');

      });

    });

// Function to update background colour
  function update_bgc_class($dropdown_item) {
    bgc_class = $dropdown_item.attr("bgc-toggle-class");
    $('#i-am-selection').removeClass("bgc-teacher bgc-school bgc-student");
    $('#i-am-selection').addClass(bgc_class);

    console.log("Updated Bg Color Class: " + bgc_class);
  }
// Function to update button text+bgc
  function update_selection($active_selection) {
    $('.form-selector .dropdown-item').removeClass('disabled');
    $active_selection.addClass("disabled");
    $('#i-am-selection').text($active_selection.text());
    update_bgc_class($active_selection)
    console.log("Updated 'I am Selection' : " + bgc_class);
  }

});
