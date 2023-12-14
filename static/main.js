d = document;

let kingBtn = d.getElementById("king-david-btn")
let matrixBtn = d.getElementById("matrix-david-btn")
let officeBtn = d.getElementById("office-david-btn")
let wizardBtn = d.getElementById("wizard-david-btn")
let terminatorBtn = d.getElementById("terminator-david-btn")
let fiftyvilleBtn = d.getElementById("fiftyville-david-btn")

let img_input = d.getElementById("img-input") // FORM DATA

const TERMINATOR_DAVID = "https://res.cloudinary.com/drd6awxrl/image/upload/v1702301543/terminator-david_jzwnym.jpg"
const KING_DAVID = "https://res.cloudinary.com/drd6awxrl/image/upload/v1702301543/king-david_dqwb7h.jpg"
const MATRIX_DAVID = "https://res.cloudinary.com/drd6awxrl/image/upload/v1702301543/matrix-david_adcnc0.jpg"
const OFFICE_DAVID = "https://res.cloudinary.com/drd6awxrl/image/upload/v1702301543/office-david_pufkxs.jpg"
const WIZARD_DAVID = "https://res.cloudinary.com/drd6awxrl/image/upload/v1702301542/wizard-david_x39gcx.jpg"
const FIFTYVILLE_TEAM = "https://res.cloudinary.com/drd6awxrl/image/upload/v1702507508/fiftyville-team_ug3ww1.jpg"

let imageSelected;

let randomDavid = [TERMINATOR_DAVID, KING_DAVID, MATRIX_DAVID, OFFICE_DAVID, WIZARD_DAVID, FIFTYVILLE_TEAM]

function getRandomImg() {
    //random index value
    const randomIndex = Math.floor(Math.random() * randomDavid.length);

    //get random item
    const img = randomDavid[randomIndex];

    setImgInputValue(img)
    showPreviewImg(img)
}

//onclick of IMG
function selectedImg(img){
    img_id = img.firstElementChild.id;

    if (img_id == "terminator-david"){
        imageSelected = TERMINATOR_DAVID;
        setImgInputValue(imageSelected)
        showPreviewImg(imageSelected)
        return console.log(img_input.value)
    }
    if (img_id == "wizard-david"){
        imageSelected = WIZARD_DAVID;
        setImgInputValue(imageSelected)
        showPreviewImg(imageSelected)
    }
    if (img_id == "office-david"){
        imageSelected = OFFICE_DAVID;
        setImgInputValue(imageSelected)
        showPreviewImg(imageSelected)
    }
    if (img_id == "matrix-david"){
        imageSelected = MATRIX_DAVID;
        setImgInputValue(imageSelected)
        showPreviewImg(imageSelected)
    }
    if (img_id == "king-david"){
        imageSelected = KING_DAVID;
        setImgInputValue(imageSelected)
        showPreviewImg(imageSelected)
    }
    if (img_id == "fiftyville-david"){
        imageSelected = FIFTYVILLE_TEAM;
        setImgInputValue(imageSelected)
        showPreviewImg(imageSelected)
    }

    else {
        return false; 
    }
} 

function setImgInputValue(data) {
    img_input.value = data;
}

function showPreviewImg(data) {
    let imgPreview = d.getElementById("mini-img-preview")
    imgPreview.setAttribute("src", data)
}

// checking value
if (window.location.href.match('/saythanks') != null) {
   console.log(img_input.value)
   }

function redirectSayThanks() {
    window.location = "/saythanks";
}