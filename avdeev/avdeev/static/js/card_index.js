"use strict"
window.addEventListener('DOMContentLoaded', () => {
    const disableExpiredCards = document.getElementById('disableExpiredCards')
    const checkExpiredCards = document.getElementById('checkExpiredCards')
    const disableCheckedCards = document.getElementById('disableCheckedCards')
    const enableCheckedCards = document.getElementById('enableCheckedCards')
    const selectAllCheckbox = document.getElementById('select-all')
    const toHistory = document.getElementById('cardHistory')
    const testButton = document.getElementById('testButton');
    const filters = document.querySelectorAll('.filter');
    const pageOf = document.querySelector('.current');
    let lastStatusFilter;
    let lastFilter = '?page=1';

    selectAllCheckbox.addEventListener('change', () => {
        const cardItems = document.querySelectorAll('.card-item');
        if (selectAllCheckbox.checked) {
            cardItems.forEach(item => {
                item.querySelector('.cardCheckbox').checked = 1
            })
        } else {
            cardItems.forEach(item => {
                item.querySelector('.cardCheckbox').checked = 0
            })
        }
    })

    function logCheckbox() {
        const cardItems = document.querySelectorAll('.card-item');
        cardItems.forEach(item => {
            const currentItemCheckbox = item.querySelector('.cardCheckbox');
            currentItemCheckbox.checked = 1
        })

    }

    testButton.addEventListener('click', logCheckbox)

    filters.forEach(item => {
        item.addEventListener('input', (e) => {
            e.preventDefault()
            const paginationHref = document.querySelectorAll('.pagination-href');
            // let href = window.location.href.split('?')[0]
            let filter = '?page=1';
            const updateFilterObj = {}
            filters.forEach(item => {
                if (item.value !== '') {
                    filter += `&${item.getAttribute("name")}=${item.value}`
                    updateFilterObj[item.getAttribute("name")] = item.value
                }
            })
            lastStatusFilter = updateFilterObj['card-status']
            lastFilter = filter
            updateFilterRequest(updateFilterObj)
            paginationHref.forEach(item => {
                item.href = item.href.split('&')[0]
                item.href = item.href + filter.split('?page=1')[1]
            })
        })
    })

    function updateFilterRequest(updateFilterObj) {
        const request = new XMLHttpRequest();
        request.open('POST', 'http://127.0.0.1:8000/cards/cardmanagement/updatefilter/');
        request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        let data = JSON.stringify(updateFilterObj);
        request.send(data);
        request.addEventListener('load', () => {
            if (request.status === 200) {
                let answ = JSON.parse(request.response)
                updateTableWithFilter(answ)
            } else {
                console.log('что то пошло не так');
            }
        });
    }

    function updateTableWithFilter(answ) {
        let obj = JSON.parse(answ)
        const cardsTableBody = document.querySelector('.cards-table')
        const maxRowCount = +cardsTableBody.getAttribute('maxRowCount')
        const cardRows = document.querySelectorAll('.card-item')
        cardRows.forEach(item => {
            item.remove()
        });
        let count = 1
        let maxPerPage = Math.ceil(obj.length / maxRowCount)
        for (let item of obj) {
            if (count <= maxRowCount) {
                let newTr = document.createElement('tr')
                newTr.classList.add('table-primary', 'card-item')
                newTr.setAttribute('id-card', item["pk"])
                newTr.innerHTML = `
                <td class="table-primary">${item["fields"]["card_series"]}</td>
                <td class="table-primary">${item["fields"]["card_number"]}</td>
                <td class="table-primary">${item["fields"]["card_create_date"]}</td>
                <td class="table-primary">${item["fields"]["card_end_date"]}</td>
                <td class="table-primary">${item["fields"]["card_last_use"]}</td>
                <td class="table-primary">${item["fields"]["card_amount"]}</td>
                <td class="table-primary">${item["fields"]["card_status"]}</td>
                <td class="table-primary"><input class="cardCheckbox" type="checkbox" 
                                            name="card-${item["pk"]}" id="card-${item["pk"]}" value="${item["pk"]}"></td>
                `;
                count += 1
                cardsTableBody.append(newTr)
            }
        }
        correctPaginationLink(maxPerPage)
    }

    function correctPaginationLink(maxPerPage) {
        const paginationBlock = document.querySelector('.step-links')
        const paginationLink = document.querySelectorAll('.pagination-href')
        paginationLink.forEach(item => {
            item.remove()
        })
        pageOf.textContent = `Page 1 of ${maxPerPage}`
        if (maxPerPage === 2) {
            const nextPage = document.createElement('a')
            nextPage.classList.add("pagination-href")
            nextPage.setAttribute("href", `?page=2${lastFilter.split('?page=1')[1]}`)
            nextPage.textContent = 'Последняя'
            paginationBlock.append(nextPage);
        } else if (maxPerPage > 2) {
            const nextPage = document.createElement('a')
            nextPage.classList.add("pagination-href")
            nextPage.setAttribute("href", `?page=2${lastFilter.split('?page=1')[1]}`)
            nextPage.textContent = '>>'
            paginationBlock.append(nextPage)
            const lastPage = document.createElement('a')
            lastPage.classList.add("pagination-href")
            lastPage.setAttribute("href", `?page=${maxPerPage}${lastFilter.split('?page=1')[1]}`)
            lastPage.textContent = '    Последняя'
            paginationBlock.append(lastPage)
        }
    }

    function checkOrDisable(action) {
        // debugger
        const request = new XMLHttpRequest();
        request.open('POST', `http://127.0.0.1:8000/cards/cardmanagement/checkexpired/${action}/`);
        request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.send();
        request.addEventListener('load', () => {
            if (request.status === 200) {
                let answ = JSON.parse(request.response)
                console.log(answ)
            } else {
                console.log('что то пошло не так');
            }
        });
    }

    disableExpiredCards.addEventListener('click', () => checkOrDisable(2))
    checkExpiredCards.addEventListener('click', () => checkOrDisable(3))
    disableCheckedCards.addEventListener('click', () => ableCheckedCards("dis"))
    enableCheckedCards.addEventListener('click', () => ableCheckedCards("en"))
    toHistory.addEventListener('click', (e) => {
        e.preventDefault()
        let listCardToHistory = []
        const cardItems = document.querySelectorAll('.card-item');
        cardItems.forEach(item => {
            const currentItemCheckbox = item.querySelector('.cardCheckbox');
            if (currentItemCheckbox.checked) listCardToHistory.push(currentItemCheckbox.value)
        })
        if (listCardToHistory.length === 0) {
            alert("Вы не выбраи ни одной карты")
        } else {
            document.cookie = `params=${listCardToHistory}`
            window.location.href = `http://127.0.0.1:8000/cards/cardmanagement/cardhistory/`
            window.location.href = `http://127.0.0.1:8000/cards/cardmanagement/cardhistory/`
        }
    })

    function ableCheckedCards(act) {
        // e.preventDefault()
        let listCardToDidable = []
        const cardItems = document.querySelectorAll('.card-item');
        cardItems.forEach(item => {
            const currentItemCheckbox = item.querySelector('.cardCheckbox');
            if (currentItemCheckbox.checked) listCardToDidable.push(currentItemCheckbox.value)
        })
        const request = new XMLHttpRequest();
        request.open('POST', `http://127.0.0.1:8000/cards/cardmanagement/${act}ablechacked/`);
        request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        let data = JSON.stringify(listCardToDidable);
        request.send(data);
        request.addEventListener('load', () => {
            if (request.status === 200) {
                let answ = JSON.parse(request.response)
                console.log(answ)
            } else {
                console.log('что то пошло не так');
            }
        });
        const reloadTimeout = setTimeout(reloadPage, 10);

        function reloadPage() {
            clearTimeout(reloadTimeout);
            location.reload()
        }
    }


});


// <a className="pagination-href" href="?page={{ page_obj.next_page_number }}&card-series={{card_series}}&card-number={{card_number}}&card-create-date={{card_create_date}}&card-end-date={{card_end_date}}&card-last-use={{card_last_use}}&card-amount={{card_amount}}&card-status={{card_status}}">>></a>
// <a className="pagination-href" href="?page={{ page_obj.paginator.num_pages }}&card-series={{card_series}}&card-number={{card_number}}&card-create-date={{card_create_date}}&card-end-date={{card_end_date}}&card-last-use={{card_last_use}}&card-amount={{card_amount}}&card-status={{card_status}}">Последняя &raquo;</a>