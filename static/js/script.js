let alertContainer = document.getElementById('alert')
let spinner = document.getElementById("spinner")
let downloadBtn = document.getElementById("downloadBtn")

function showToast(backgroundClass, message) {
  alertContainer.innerHTML = `<div class="toast show align-items-center text-bg-${backgroundClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            </div>`
}

function downloadVideos(videoUrls) {
  for (var i = 0; i < videoUrls.length; i++) {
    var videoUrl = videoUrls[i];
    var link = document.createElement('a');
    link.href = videoUrl;
    link.target = '_blank';
    link.click();
  }
}

let responseDataUrls = []

$("form#data").submit(function (e) {
  e.preventDefault();
  Pace.restart()
  spinner.style.display = "inline-block"
  downloadBtn.style.display = "none"
  var formData = new FormData(this);
  alertContainer.innerHTML = ""

  $.ajax({
    url: "/api",
    type: 'POST',
    data: formData,
    success: function (data) {
      let res = JSON.parse(data)
      if (res.success) {
        responseDataUrls = res.success
        showToast("success","Click the Download Button Below to Download Videos.")
        downloadBtn.style.display = "block"
      }else{
        showToast("danger",res.error)
      }
      spinner.style.display = "none"
    },
    cache: false,
    contentType: false,
    processData: false
  });
});

$(document).ajaxError(function () {
  alertContainer.innerHTML = `<div class="toast show align-items-center text-bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
          <div class="toast-body">
          No Internet Connection.
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      </div>`});


downloadBtn.onclick = function(){
  downloadVideos(responseDataUrls)
};