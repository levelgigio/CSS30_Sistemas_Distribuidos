window.onload = () => {
  console.log('window loaded')
  var targetContainer = document.getElementById("data");
  var eventSource = new EventSource("http://localhost:5000/stream");

  eventSource.onerror = (event, err) => {
    console.error('Error in connect SSE', event, err);
  }
  eventSource.addEventListener('message', (e) => {
    console.log('received event', e);
    targetContainer.innerHTML = e.data;
  });

  
}

//execute with -> "python -m http.server 8080"
//see logs on "localhost:8080/public"