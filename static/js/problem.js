document.addEventListener("DOMContentLoaded", (e) => {
    let forms = document.getElementsByClassName("form-answer")

    for(let i = 0; i < forms.length; i++) {
        forms.item(i).onsubmit = function (e) {
            e.preventDefault();
            const targetId = this.id.split("-")[1]
            const answer = document.getElementById("answer-" + targetId).value
            const xhttp = new XMLHttpRequest()
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                  console.log(this.response)
                }
            };
            xhttp.open("POST", window.location.href, true)
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("answer=" + encodeURIComponent(answer) + "&question_id=" + encodeURIComponent(targetId))
        };
    }
});