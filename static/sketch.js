let colorData;
let powerButton
let powerData = false
let speedData = 5
let fileData = im-white_low

function setup() {
  createCanvas(500, 500);
  background('white');

  powerButton = createButton("Turn On");
  powerButton.position(50, 10);
  powerButton.mousePressed(ledPower);
  // console.log(colorData);
}


function draw(){
  powerButton.html(`TURN LEDS ${powerData ? 'OFF' : 'ON'}`);
}

function ledPower() {
  powerData = powerData === 1 ? 0 : 1;
  postData();
}

function postData() { 
  httpPost("/effect", 'json', {'power': powerData, 'speed': speedData, 'file': fileData})
}

function getColorData() {
  httpGet("/effect", "json", false, (x) => {
    colorData = x;
  }).then( () => {console.log("Waiting")})
}