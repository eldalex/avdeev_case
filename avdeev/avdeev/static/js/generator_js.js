"use strict"
window.addEventListener('DOMContentLoaded', () => {
    // const buttonTable = document.querySelector('.crtable');
    const from = document.querySelector('form');
    from.addEventListener('submit', (e) => {
        e.preventDefault()
        const formData = new FormData(from);
        const data = {};
        formData.forEach(function (value, key) {
            data[key] = value;
        });
        if (data["card-series"] && data["card-count"] && data["card-create-date"] && data["optionsRadios"] && data["card-amount"]) {
            checkSeries(data)
        } else {
            alert('Вы заполнили не все поля')
        }
    });

    function checkSeries(formData) {
        let series_data = {
            "series": formData["card-series"]
        }
        const request = new XMLHttpRequest();
        request.open('POST', 'http://127.0.0.1:8000/cards/cardgenerator/checkseries/');
        request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        let data = JSON.stringify(series_data);
        request.send(data);
        request.addEventListener('load', () => {
            if (request.status === 200) {
                let answ = JSON.parse(request.response)
                if (answ["series-exist"] === 'true') {
                    alert("Такая серия существует")
                } else {
                    generateCards(formData)
                }
            } else {
                console.log('что то пошло не так');
            }
        })
    }

    function generateCards(formData) {
        const requestGenerate = new XMLHttpRequest();
        requestGenerate.open('POST', 'http://127.0.0.1:8000/cards/cardgenerator/generate/');
        requestGenerate.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        requestGenerate.setRequestHeader('X-CSRFToken', csrftoken);
        let data = JSON.stringify(formData);
        requestGenerate.send(data);
        requestGenerate.addEventListener('load', () => {
            if (requestGenerate.status === 200) {
                let answ = JSON.parse(requestGenerate.response)
                genReport(answ)
            } else {
                console.log('что то пошло не так');
            }
        });

    }

    function genReport(obj) {
        const tableP = document.createElement("p")
        const tbl = document.createElement('table')
        tbl.classList.add('table')
        const tbdy = document.createElement('tbody')
        const headTr = document.createElement('tr')
        headTr.innerHTML = `<td>#</td>
                <td>Серия карты</td>
                <td>Номер карты</td>
                <td>Дата создания</td>
                <td>Дата окончания действия</td>
                <td>Дата последнего использования</td>
                <td>Баланс карты</td>
                <td>Статус карты</td>`
        tableP.append(tbl)
        tbl.append(tbdy)
        tbdy.append(headTr)
        let num = 1
        for (let item of obj) {
            const tblTr = document.createElement('tr')
            tblTr.innerHTML = `
                <td>${num}</td>
                <td>${item["card-series"]}</td>
                <td>${item["card-number"]}</td>
                <td>${item["card-create-date"]}</td>
                <td>${item["card-end-date"]}</td>
                <td>${item["card-last-use"]}</td>
                <td>${item["card-amount"]}</td>
                <td>${item["card-status"]}</td>`;
            tbdy.append(tblTr)
            num += 1
        }
        from.append(tableP)
    }
});