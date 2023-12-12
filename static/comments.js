d = document;

d.addEventListener("load", fetchMessages())

// *********************************** fetch data 
async function fetchMessages() {

    let res = await fetch('/messages/api')
    let messages = await res.json()
    console.log(messages)
    loadMessages(messages)

}

// declare variables 
let navPagination = d.getElementById("pagination-btns");
let messagesContainer = d.getElementById("messages-wrapper");

let pageIndex = 0;
let itemsPerPage = 10; 

// *********************************** load messages according to items per page limit
function loadMessages(messages) {

        html = '';

        for (let i = pageIndex*itemsPerPage; i < (pageIndex*itemsPerPage) + itemsPerPage; i++) {
            if (!messages) {
                break;
            }

            html += `
            <div key="${messages[i].id}" class="mb-2">
            <div class="comment-container d-flex flex-column align-items-start">
                <section class="align-self-center m-2 mt-4">
                    <img class="comment-img" src="${messages[i].img}" />
                </section>
                <section class="comment-text-container d-flex flex-column align-items-start p-3">
                    <div class="d-flex align-items-center justify-content-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                            <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
                        </svg>
                        <p class="mt-3 ms-2"><b>${messages[i].name}</b></p>
                    </div>
                    <p class="comment-p">${messages[i].comment}</p>
                    <p><small><i>${messages[i].date}</i></small></p>
                </section>
            </div>
        </div>`;

        messagesContainer.innerHTML = html;

        }

        //update navigation each time new page contest is loaded
        if (messages.length >= itemsPerPage) {
            loadPaginationNav(messages)
        }

}

// *********************************** load buttons according to items per page limit
function loadPaginationNav(messages) {

    html = "";

        html += `
        <div id="back-arrow">
        <button onclick="changeMsgPage(this)" class="pag-arrow-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-left-circle-fill" viewBox="0 0 16 16">
            <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.5 7.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
          </svg>
        </button>
      </div>
        <div id="btns-wrapper" class="pag-btns-wrapper"></div>
        <div id="next-arrow">
          <button onclick="changeMsgPage(this)" class="pag-arrow-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-right-circle-fill" viewBox="0 0 16 16">
              <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/>
            </svg>
          </button>
        </div>
        `
        navPagination.innerHTML = html

        const btnsWrapper = d.getElementById("btns-wrapper")

    for(let i = 0; i < (messages.length/itemsPerPage); i++) {

        //create n° of btns according to itemsPerPage
        const newBtn = d.createElement("button")
        newBtn.classList.add("page-btn")
        newBtn.innerHTML = i +1;
        newBtn.addEventListener("click", (e) => {
            pageIndex = e.target.innerHTML-1;
            console.log(pageIndex)
            loadMessages(messages)
        })
        //change style
        if (i === pageIndex) {
            newBtn.style.backgroundColor= "rgb(87, 87, 228)";
            newBtn.style.color= "white";
        }
        btnsWrapper.appendChild(newBtn)

    }

}

// *********************************** use arrows to change page
function changeMsgPage(value) {

    let pagBtns = d.getElementsByClassName("page-btn")
    console.log("******pageindex and length")
    console.log(pageIndex)
    console.log(pagBtns.length)

    if (value.parentNode.id == "back-arrow") {
        
        if (pageIndex > 0) {
            pageIndex--;
            loadMessages(arrayOfMsgs)
            return console.log(pageIndex)
        }

    }
    if (value.parentNode.id == "next-arrow") {

        if (pageIndex < pagBtns.length -1) {
            pageIndex++;
            loadMessages(arrayOfMsgs)
            return console.log(pageIndex)
        }

    }

}
