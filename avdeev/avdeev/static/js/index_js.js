"use strict"
window.addEventListener('DOMContentLoaded', () => {

    const statistics = document.querySelectorAll('.statistic');
    let answer;
    statistics.forEach(item => {
        let testID = item.getAttribute("testID");

        getStatistic(testID);


    });

    function getStatistic(testID) {
        let nowTest = {};
        nowTest["test_id"] = testID;
        const request = new XMLHttpRequest();
        request.open('POST', 'http://127.0.0.1:8000/test/statistics/');
        request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        let data = JSON.stringify(nowTest);
        request.send(data);

        request.addEventListener('load', () => {
            if (request.status === 200) {
                answer = JSON.parse(request.response);
                updateStatistics(testID, answer)
            } else {
                answer = {
                    "true": "0",
                    "false": "0",
                    "true_pers": "0%"
                }
                updateStatistics(testID, answer)
            }
        })
    }

    function updateStatistics(testID, answer) {
        const nowTD = document.querySelector(`td[testID="${testID}"]`)
        console.log(answer)
        nowTD.innerHTML = `Верных ответов:${answer.true}, Ошибок:${answer.false}, Процент верных ответов${answer.true_pers}`;
    }

});