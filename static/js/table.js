window.onload = function () {
  correctWidth();
};

document.addEventListener("DOMContentLoaded", function (event) {
  window.onresize = function () {
    correctWidth();
  };
});

function correctWidth() {
   
   let body = document.querySelector("#tbl-body").offsetWidth; // получаем ширину таблицы tbl-body
  // console.log("tbody =",body);
  
  let head = document.querySelector("#tbl-head"); // получаем ширину таблицы tbl-head
  // console.log("thead =", head);
  head.style.width = body + "px"; // устанавливаем ширину таблицы tbl-head равной ширине таблицы tbl-body
   //=====================================

  //=====================================
  let thHead = document.querySelector("#tbl-head tr").querySelectorAll("th"); //берем  все колонки первого ряда таблицы tbl-head
  let countColHead = thHead.length; // считаем количество колонок ряда таблицы tbl-head
  // console.log("длина th =", countColHead);

  let tbBody = document.querySelector("#tbl-body tr").querySelectorAll("td"); //берем все колонки первого ряда таблицы tbl-body

  let countColBody = tbBody.length; // считаем количество колонок ряда таблицы tbl-body

  // console.log("длина td =", countColBody);

  if (countColBody == countColHead) {
    // если количество колонок таблицы tbl-body равно количеству колонок tbl-head

    for (var i = 0; i < countColBody; i++) {
      //перебираем количество колонок

      let tdWidth = tbBody[i].offsetWidth; //измеряем длину каждой колонки таблицы tbl-body

      thHead[i].width = tdWidth + "px"; // присваиваем значение каждой колонки таблицы tdl-body колонке того же номера таблицы tbl-head

      // console.log("col td", i, "=", tdWidth, "col th =", thHead[i].width);
    }
  }
}

const topTable = document.querySelector("#scr-01");

const bottomTable = document.querySelector("#scr-02");


bottomTable.addEventListener("scroll", () => {
  topTable.scrollLeft = bottomTable.scrollLeft;
});

