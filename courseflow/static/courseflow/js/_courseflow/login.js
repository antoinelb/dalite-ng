import { buildReq } from "../../../../../peerinst/static/peerinst/js/ajax.js";

/*********/
/* model */
/*********/

let model;

function initModel(data) {
  model = {
    urls: {
      authenticate: data.urls.authenticate,
    },
    errorMsg: "",
  };
}

/**********/
/* update */
/**********/

async function authenticate(event) {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const req = buildReq({ username: username, password: password }, "post");
  const resp = await fetch(model.urls.authenticate, req);

  if (resp.status == 200) {
    location.reload();
  } else if (resp.status == 401) {
    const err = await resp.text();
    model.errorMsg = err;
    errorView();
  }
}

/********/
/* view */
/********/

function errorView() {
  document.getElementById("error-msg").textContent = model.errorMsg;
}

function initEventListeners() {
  event.preventDefault();
  document
    .querySelector("#lti-login form")
    .addEventListener("submit", authenticate);
}

/********/
/* init */
/********/

export function init(data) {
  initModel(data);
  errorView();
  initEventListeners();
}
