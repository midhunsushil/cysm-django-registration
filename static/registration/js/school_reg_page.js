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
      if($(this).is("input")) {
        console.log($(this))
        var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({
          'name': name,
          'id': id
        }).val('').removeAttr('checked');
      }
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
      console.log("Inside delete()");
      btn.closest('.form-row').remove();
      var forms = $('.form-row');
      $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

      for (var i = 0, formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).find(':input, label').each(function() {
          // Original Code
          updateElementIndex(this, prefix, i);
          // Original Code End
          console.log($(this));

        });
      }

    }
    return false;
  }

  $(document).on("click", ".add-form-btn", function() {
    console.log("Cloning new form");
    console.log($(this).attr('class'));
    cloneMore('.form-row:last', 'class_section_set');
    return false;
  });

  $(document).on("click", ".remove-form-btn", function(e) {
    // e.preventDefault();
    console.log("Deleting form element");
    deleteForm('class_section_set', $(this));
    return false;
  });

  function initialFormButtonCustomization(form_selector, prefix, btn_selector) {
    no_of_initialForms = parseInt($('#id_' + prefix + '-INITIAL_FORMS').val());
    $initialForms = $(form_selector).slice(0,no_of_initialForms)
    $initialForms.find(btn_selector).remove()
  }
  initialFormButtonCustomization('.form-row', 'class_section_set', '.btn-clone');

});
