 function shineLinks(id) {
  console.log("Айгуль, я тебя люблю!")
  console.log(urlName().nm)
          // let el = document.getElementById(id).getElementsByTagName('a');
          let el1=document.querySelector("#navbarCollapse");
          console.log(el1);
          let el = el1.getElementsByTagName('a');
          console.log(el);

          
          
          // let nav =el.substring(el.lastIndexOf("/")+1);
          // var url = document.location.href;
// console.log(el);
          for (var i = 0; i < el.length; i++) {
            let nav =el[i].href.substring(el[i].href.lastIndexOf("/")+1);

            console.log(urlName().nm);
			      console.log(`${i} = ${nav}`);

            if (urlName().nm == nav) {
				el[i].className += " active";
            };
          };
       
      };


function urlName (){
  let url  = document.location.href; // получаем href страницы
  let nm = url.match(/(?<=\/\/.+\/)\w+/); //Получаем из htef блок наименования страницы
  nm = nm[0]
  let num = url.match(/(?<=\/\/.+\/\w+\/)\d{1,}/);
  if (num == null){
    num = '0';
    }
  else {
    num = num[0]
    };
   return {nm, num}
};