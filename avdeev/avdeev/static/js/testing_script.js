"use strict"
window.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.question__form'),
        answersBlock = document.querySelector('.answers'),
        quest_number = form.querySelector('.number'),
        quest_text = form.querySelector('.question__text'),
        test_id = form.querySelector('.test_id'),
        logoutButton = document.querySelector('.logout'),
        submitButton = document.querySelector('.submit-answer');

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

        next["test_id"] = test_id.getAttribute("testID");
        const request = new XMLHttpRequest();
        request.open('POST', '/test/getquestion/');
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
                    submitButton.innerHTML = 'Вернуться в меню'
                    form.addEventListener('submit', (e) => {
                        window.location.href=window.location.protocol+'//'+(window.location.host)+'/test/appfortests'
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
        quest_number.setAttribute("realQuestionId", question.realQuestionId)
        quest_number.setAttribute("question-number", question.number)
        quest_number.innerHTML = '<h4>Вопрос №' + question.number + '&nbsp:</h4>'
        quest_text.innerHTML = "<h4>&nbsp&nbsp" + question.question + '</h4><br>'
        for (let i in question.answers) {
            let div = document.createElement('div')
            div.classList.add('answer')
            let ans = document.createElement('input')
            ans.classList.add("form-check-input")
            ans.setAttribute("type", "checkbox")
            ans.setAttribute("id", i)
            ans.setAttribute("name", i)
            ans.setAttribute("value", question.answers[i])

            let lbl = document.createElement('label')
            lbl.classList.add("form-check-label")
            lbl.setAttribute("for", question.answers[i])
            lbl.insertAdjacentHTML('afterbegin', '<h5>' + question.answers[i] + '<h5>')
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
            "question_number": quest_number.getAttribute("question-number"),
            "realQuestionId": quest_number.getAttribute("realQuestionId")
        }
        getQuestion(obj_ans)
    })
});