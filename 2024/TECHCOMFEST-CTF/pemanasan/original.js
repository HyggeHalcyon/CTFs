app.alert("PDF flag checker");
var userInput = app.response("Enter the flag : ", "Default Value");
var flag = String.fromCharCode(84, 67, 70, 50, 48, 50, 52, 123, 109, 97, 108, 108, 105, 99, 49, 111, 117, 115, 95, 112, 100, 102, 95, 105, 115, 95, 99, 114, 52, 122, 121, 121, 95, 101, 49, 54, 57, 53, 102, 48, 56, 53, 102, 48, 54, 57, 102, 98, 49, 101, 98, 98, 50, 100, 57, 100, 102, 49, 100, 48, 49, 51, 101, 99, 98, 125);
if (userInput == flag) {
  app.alert("Yey kamu dapet flag: " + flag);
} else {
  app.alert("Flagnya bukan " + userInput + " maaf :'( ");
}