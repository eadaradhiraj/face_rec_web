window.onload = function () {
  var video = document.getElementById('video');
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var tracker = new tracking.ObjectTracker('face');
  tracker.setInitialScale(4);
  tracker.setStepSize(2);
  tracker.setEdgesDensity(0.1);
  tracking.track('#video', tracker, {
    camera: true
  });
  tracker.on('track', function (event) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    event.data.forEach(function (rect) {
      context.strokeStyle = '#a64ceb';
      context.strokeRect(rect.x, rect.y, rect.width, rect.height);
      context.font = '11px Helvetica';
      context.fillStyle = "#fff";
      context.fillText('x: ' + rect.x + 'px', rect.x + rect.width + 5, rect.y + 11);
      context.fillText('y: ' + rect.y + 'px', rect.x + rect.width + 5, rect.y + 22);

    });
  });

  $("#button").on('click', function () {
    var snapshotContext = snapshotCanvas.getContext('2d');
    snapshotContext.drawImage(video, 0, 0, video.width, video.height);

    var dataURI = snapshotCanvas.toDataURL('image/jpeg'); // can also use 'image/png'
    $.ajax({
      type: "POST",
      url: "/test",
      data: {
        'data': dataURI
      },
      success: function (response) {
        // console.log(response)
        var list_of_names = jQuery.map(response, function (e) {
          return e.name;
        });

        $(".prediction_results").val("Is this " + list_of_names.join(', '));
      }
    });
  })
};
