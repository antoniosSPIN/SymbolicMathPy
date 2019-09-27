document.addEventListener("DOMContentLoaded", (e) => {
    const forms = document.getElementsByClassName("form-answer");

    for(let i = 0; i < forms.length; i++) {
        forms.item(i).onsubmit = function (e) {
            e.preventDefault();
            const targetId = this.id.split("-")[2];
            const form = this;
            const answer = document.getElementById("answer-" + targetId).value;
            const xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    appendAnswerAndSolution(targetId, JSON.parse(this.response));
                    form.parentNode.removeChild(form);
                }
            };
            xhttp.open("POST", window.location.href, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("answer=" + encodeURIComponent(answer) + "&question_id=" + encodeURIComponent(targetId));
        };
    }
});

function appendAnswerAndSolution(targetId, response) {
    // Get question container
    const questionCont = document.getElementById("question-container-" + targetId);
    // create solution container
    const solutionCont = document.createElement("div");
    const classAnswer = response.isCorrect ? "correct" : "incorrect";
    // add necessary classes
    solutionCont.classList.add("solution", classAnswer);
    // Create solution and answer element 
    const solution = document.createElement("p");
    solution.innerText = response.solution;
    const answer = document.createElement("p");
    answer.innerText = "Correct answer: " + response.answer;
    // Append the above created elements to their places
    solutionCont.appendChild(solution);
    solutionCont.appendChild(answer);
    questionCont.appendChild(solutionCont);
};