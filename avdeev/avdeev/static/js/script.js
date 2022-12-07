"use strict"
window.addEventListener('DOMContentLoaded', () => {

    const form = document.querySelector('.question__form'),
        answersBlock = document.querySelector('.answers'),
        quest_number = form.querySelector('.number'),
        quest_text = form.querySelector('.question__text'),
        test_id = form.querySelector('.test_id'),
        logoutButton = document.querySelector('.logout');

    clearOldQuestion()


    function clearOldQuestion() {
        const answers = answersBlock.querySelectorAll('.answer')
        quest_number.innerHTML = '';
        quest_text.innerHTML = '';
        answers.forEach(item => {
            item.remove()
        });
    }

    function getQuestion(next = {"question_number": "1"}) {
        next["test_id"] = test_id.textContent;
        console.log(next);
        const request = new XMLHttpRequest();
        request.open('POST', 'http://127.0.0.1:8000/getquestion/');
        request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        let data = JSON.stringify(next);
        request.send(data);
        let question;
        request.addEventListener('load', () => {
            if (request.status === 200) {
                question = JSON.parse(request.response);
                if ("finish" in question) {
                    clearOldQuestion()
                    form.addEventListener('submit', (e) => {
                        window.location.href = "http://127.0.0.1:8000/"
                    })

                } else newQuestion(question);
            } else {
                console.log('что то пошло не так');
            }
        });
    }

    getQuestion();

    function newQuestion(question) {
        clearOldQuestion()
        quest_number.innerHTML = question.number
        quest_text.innerHTML = " " + question.question
        for (let i in question.answers) {
            let div = document.createElement('div')
            div.classList.add('answer')
            let ans = document.createElement('input')
            ans.setAttribute("type", "checkbox")
            ans.setAttribute("id", i)
            ans.setAttribute("name", i)
            ans.setAttribute("value", question.answers[i])

            let lbl = document.createElement('label')
            lbl.setAttribute("for", question.answers[i])
            lbl.innerText = question.answers[i]
            div.append(ans);
            div.append(lbl);
            answersBlock.append(div)
        }
    }


    form.addEventListener('submit', (e) => {
        e.preventDefault()
        const formData = new FormData(form);
        let answers = answersBlock.querySelectorAll('input[type=checkbox]');
        let obj_ans = {};
        let list_ans = [];
        answers.forEach(item => {
            if (item.checked) {
                list_ans.push(item.id)
            }
        })
        obj_ans = {
            "answers": list_ans,
            "question_number": quest_number.innerHTML
        }
        getQuestion(obj_ans)
    })

});