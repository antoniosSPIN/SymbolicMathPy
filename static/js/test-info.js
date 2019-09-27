document.addEventListener("DOMContentLoaded", (e) => {
    const button = document.getElementById("start-test-button");

    button.onclick = function (e) {
        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                const response = JSON.parse(this.response);
                window.location.replace(window.location.href + '/problem/' + response.start);
            }
        };
        xhttp.open("POST", window.location.href + "/start", true);
        xhttp.send();
    }
});