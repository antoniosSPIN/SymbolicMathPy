document.addEventListener("DOMContentLoaded", (e) => {
    const forms = document.getElementsByClassName("form-answer");

    for(let i = 0; i < forms.length; i++) {
        forms.item(i).onsubmit = function (e) {
            e.preventDefault();
            const targetId = this.id.split("-")[2];
            const form = this;
            const answer = document.getElementById("answer-" + targetId).value;
            if (validateAnswer(answer)) {
                const xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        form.parentNode.removeChild(form);
                        questionCont = document.getElementById("question-container-" + targetId);
                        const submittedAnswer = document.createElement("span");
                        submittedAnswer.innerText = "Submitted answer: " + answer;
                        questionCont.appendChild(submittedAnswer);
                    }
                };
                xhttp.open("POST", window.location.href, true);
                xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhttp.send("answer=" + encodeURIComponent(answer) + "&question_id=" + encodeURIComponent(targetId));
            }
        };
    }
});

function validateAnswer(answer) {
    const regex = /[A-Z0-9,\(\)+*^/\ \-_]+/gi
    const res = answer.match(regex);
    return res.length == 1;
}
