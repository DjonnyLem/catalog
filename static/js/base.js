 function shineLinks(id) {
  console.log("Айгуль, я тебя люблю!")
  console.log(urlName().nm)
          let el = document.getElementById(id).getElementsByTagName('a');
          // var url = document.location.href;
// console.log(el);
          for (var i = 0; i < el.length; i++) {
            console.log(urlName().nm);
			console.log(i,'=',el[i].href);

            if (urlName().nm == el[i].href) {
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