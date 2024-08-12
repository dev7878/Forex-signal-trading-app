function fetchSignal() {
  fetch("/check_signal")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("signal").innerText = JSON.stringify(data);
    })
    .catch((error) => console.error("Error:", error));
}
