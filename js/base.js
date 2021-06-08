const div = document.createElement ('div');

div.classList.add('nav');
const ul = `
    <ul>
        <li>один</li>
        <li>два</li>
        <li>три</li>
    </ul>
`;
div.innerHTML = ul;

const body = document.body;
body.appendChild(div);


const li=document.querySelectorAll('li');
console.log (li);

for (var i=0; i<li.length;i++){
console.log ("i =", i);
if (i ==0){
li[i].setAttribute("href", "0");
}
 else if (i ==1){
li[i].setAttribute("href", "file:///home/tech-3/%D0%A0%D0%B0%D0%B1%D0%BE%D1%87%D0%B8%D0%B9%20%D1%81%D1%82%D0%BE%D0%BB/%D0%9A%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%B4%D0%B5%D1%84%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/1/index.html");
}
else if (i ==2){
li[i].setAttribute("href", "2");
}
}
a = window.location.href;
console.log(a);

console.log (div);
console.log('li0=',li[0].getAttribute('href'));

for (var i=0; i<li.length;i++){
console.log( 'li=',  li[i].getAttribute('href'));
href = li[i].getAttribute('href')
a = window.location.href;
if (href==a){
li[i].style.fontWeight = "600";
li[i].style.textDecoration =  "none";
li[i].style.color = "#ff8111";
d = document.getElementsByClassName('nav');
d.class = "nav1";

};
};

console.log(div);
