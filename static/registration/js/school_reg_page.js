$(document).ready(function() {

  function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
  }

  function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
      var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({
        'name': name,
        'id': id
      }).val('').removeAttr('checked');
    });

    newElement.find('label').each(function() {
      var forValue = $(this).attr('for');
      if (forValue) {

        forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');

        $(this).attr({
          'for': forValue
        });

      }
    });

    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn-clone.add-form-btn')
      .removeClass('add-form-btn').addClass('remove-form-btn');
    return false;

  }

  function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {

      btn.closest('.form-row').remove();
      var forms = $('.form-row');
      $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

      for (var i = 0, formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).find(':input').each(function() {
          updateElementIndex(this, prefix, i);
        });
      }

    }
    return false;
  }

  $(document).on("click", ".add-form-btn", function() {
    console.log("Cloning new form");
    console.log($(this).attr('class'));
    cloneMore('.form-row:last', 'form');
    return false;
  });

  $(document).on("click", ".remove-form-btn", function(e) {
    // e.preventDefault();
    console.log("Deleting form element");
    deleteForm('form', $(this));
    return false;
  });

});