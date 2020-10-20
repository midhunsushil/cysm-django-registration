$(document).ready(function() {
  // Function to check if Browser supports Advanced upload
  var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
  }();

  var $form = $('form.dropzone'),
    $dropzoneBox = $form.find(".dropzone__box"),
    droppedFiles = false;

  var $input = $dropzoneBox.find('input[type="file"]'),
    $label = $dropzoneBox.find('label'),
    showFiles = function(fileList) {
      $label.text(fileList.length > 1 ? ($input.attr('data-multiple-caption') || '{count} files selected for upload.').replace('{count}', fileList.length) : fileList[0].name);

    };

    $input.change(function(e) {
      showFiles(e.target.files);
    });

  if (isAdvancedUpload) {

    $form.addClass('has-advanced-upload');
    var counter = 0;

    $dropzoneBox.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
        // e.preventDefault();
        e.stopPropagation();
        console.log('started drag'+" : "+counter);
      })

      .on('dragenter', function() {
        counter++;
        $dropzoneBox.addClass('is-dragover');
        console.log('over'+" : "+counter);
      })

      .on('dragleave drop', function() {

        counter--;
        console.log('out'+" : "+counter);
        if (counter === 0) {
          // Put your things-to-do here
          $dropzoneBox.removeClass('is-dragover');
          console.log('out'+" : "+counter);
        }
      })

      .on('drop', function(e) {
        droppedFiles = e.originalEvent.dataTransfer.files;
        $dropzoneBox.addClass("file__dropped");
        showFiles(droppedFiles);
        console.log('dropped'+" : "+counter);
      });
  }
});
