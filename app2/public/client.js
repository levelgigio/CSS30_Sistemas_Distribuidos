window.onload = () => {
  console.log("window loaded");
  document.getElementById("rides_result").style.display = "none";
  var targetContainer = document.getElementById("data");
  var eventSource = new EventSource("http://localhost:5000/stream");

  eventSource.onerror = (event, err) => {
    console.error("Error in connect SSE", event, err);
  };
  eventSource.addEventListener("message", (e) => {
    console.log("received event", e);
    targetContainer.innerHTML = e.data;
  });
};

function toggleRides() {
  var x = document.getElementById("rides_result");
  if (x.style.display === "none") {
    get_rides()
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function offer_or_want() {
  var is_offered = document.getElementById("offered").checked;
  var from = document.getElementById("from").value;
  var to = document.getElementById("to").value;
  var date = document.getElementById("date").value;
  var passengers = document.getElementById("passengers").value;
  var username = document.getElementById("username").value;

  ride = {
    location: [from, to],
    date: date,
    passengers: passengers,
    user: username,
    offered: is_offered,
  };

  fetch("http://localhost:5000/offer_or_want_ride", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(ride),
  })
    .then((response) => {
      console.log(response);
    })
    .catch((err) => {
      console.error(err);
    });
}

function get_rides() {
  fetch("http://localhost:5000/get_rides", {
    method: "GET",
    headers: {},
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (ride_list) {

      var targetContainer = document.getElementById("response");
      response_json =
        "<pre>" + JSON.stringify(ride_list, undefined, 2) + "</pre>";

      targetContainer.innerHTML = response_json;
    })
    .catch((err) => {
      console.error(err);
    });
}

function cancel_ride() {
  var ride_id_to_cancel = document.getElementById("cancel").value;

  fetch("http://localhost:5000/cancel_ride", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: String(ride_id_to_cancel),
  })
    .then((response) => {
      console.log(response);
    })
    .catch((err) => {
      console.error(err);
    });
}
//execute with -> "python -m http.server 8080"
//see logs on "localhost:8080/public"
