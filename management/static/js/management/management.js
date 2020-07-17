$(document).ready(function() {
  if (window.opener) {
    console.log(history.length)
    if (history.length > 1) {
      window.opener.location.reload()
      window.close()
    }
  }
})