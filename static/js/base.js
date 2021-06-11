 function shineLinks(id) {
      
          var el = document.getElementById(id).getElementsByTagName('a');
          var url = document.location.href;
console.log(el);
          for (var i = 0; i < el.length; i++) {
            console.log(url);
			console.log(i,'=',el[i].href);
            if (url == el[i].href) {
				el[i].className += " active";
            };
          };
       
      };
