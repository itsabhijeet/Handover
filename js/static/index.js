window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || null;
if(!window.SpeechRecognition)
  alert("SpeechRecognition not supported by your browser.");
var recognition = new SpeechRecognition();
//recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

var result_container = document.querySelector('#results');
var start_view = document.querySelector('#start');
var stop_view = document.querySelector('#stop');

start_view.onclick = function(){
  recognition.start();
  start_view.style.backgroundColor = "#c62828"; // red
};
stop_view.onclick = function(){
  recognition.stop();
  start_view.style.backgroundColor = "#ff80ab"; // light pink
};
recognition.onspeechstart = function(){
};
recognition.onspeechend = function(){
  start_view.style.backgroundColor = "#c8e6c9";//green
};
recognition.onerror = function(){
  start_view.style.backgroundColor = "#cddc39";//yellow
};
recognition.onresult = function(event) {
  var text = event.results[0][0].transcript;
  result_container.innerText = text;
  var str = "http://127.0.0.1:5000/"  ;
  str = str + text;
  console.log(str);
  window.location.href = str;
  start_view.style.backgroundColor = "";
}