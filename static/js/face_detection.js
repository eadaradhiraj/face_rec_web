var video, canvas, context, tracker;
var acquired_names
window.onload = function () {
  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  context = canvas.getContext('2d');
  tracker = new tracking.ObjectTracker('face');
  track_image(tracker, canvas, context)
};

function track_image(tracker, canvas, context) {
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
      loc = acquired_names ? acquired_names.dims : acquired_names
      x = loc ? loc[3] : rect.x
      name = acquired_names ? acquired_names.name : 'not yet'
      y = loc ? loc[0] : rect.y
      w = loc ? loc[1] : rect.width
      h = loc ? loc[2] : rect.height
      context.strokeRect(rect.x, rect.y, rect.width, rect.height);
      context.font = '11px Helvetica';
      context.fillStyle = "#fff";
      context.fillText('x: ' + rect.x + 'px', rect.x + rect.width + 5, rect.y + 11);
      context.fillText(name, x , y );
      context.fillText('y: ' + rect.y + 'px', rect.x + rect.width + 5, rect.y + 22);
      // context.fillText(rect.x + rect.width + 5, rect.y + 33);

      var snapshotContext = snapshotCanvas.getContext('2d');
      //draw image to canvas. scale to target dimensions
      snapshotContext.drawImage(video, 0, 0, video.width, video.height);

      //convert to desired file format
      var dataURI = snapshotCanvas.toDataURL('image/jpeg');
      $.ajax({
        type: "POST",
        url: "/test",
        data: {
          'data': dataURI
        },
        success: function (response) {
          console.log("rect", rect, "response", response)
          acquired_names = response[0]//.dims
        }
      });

    });
  });
}

// $("#canvas").on('click', function () {
//   var snapshotContext = snapshotCanvas.getContext('2d');
//   snapshotContext.drawImage(video, 0, 0, video.width, video.height);

//   var dataURI = snapshotCanvas.toDataURL('image/jpeg'); // can also use 'image/png'
//   $.ajax({
//     type: "POST",
//     url: "/test",
//     data: {
//       'data': dataURI
//     },
//     success: function (response) {
//       var list_of_names = jQuery.map(response, function (e) {
//         return e.name;
//       });

//       $(".prediction_results").val("Is this " + list_of_names.join(', '));
//       track_image(tracker, canvas, context);
//     }
//   });
// });