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
      context.strokeRect(rect.x, rect.y, rect.width, rect.height);
      context.font = '11px Helvetica';
      context.fillStyle = "#fff";
      if (acquired_names != undefined) {
        if (acquired_names.length>1)
          {console.log(acquired_names)}
        var dists = acquired_names.map(function (n) {
          return {
            'name': n.name,
            "dist": Math.sqrt(
              Math.pow((n.dims[0] - rect.x), 2) + Math.pow((n.dims[1] - rect.y), 2)
            )
          }
        })
        var nearest = dists.reduce(function (l, e) {
          return e.dist < l.dist ? e : l;
        });
        context.fillText(nearest.name, rect.x, rect.y);
      }

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
          acquired_names = response
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