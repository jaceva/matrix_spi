let colorData;
let powerButton
let powerData = 1
let speedData = 5
let fileData = 'white_mid'


function setup() {
  createCanvas(500, 500);
  background('white');
  
  powerButton = createButton(`TURN LEDS ${powerData == 1 ? 'OFF' : 'ON'}`);
  powerButton.position(50, 10);
  powerButton.mousePressed(ledPower);
  getData();
  setTimeout(makeButtons, 1000);
  
  console.log("colorData");
  console.log(colorData);
  postData()
}

function makeButtons() {
  let p = 40
  for(let f in colorData) {
    console.log(f)
    b = createButton(colorData[f]);
    b.position(50, p);
    b.mousePressed(() => {
      fileData = colorData[f]
      postData()
    });
    p += 30;
  }
}

function draw(){
  powerButton.html(`TURN LEDS ${powerData == 1 ? 'OFF' : 'ON'}`);
}

function ledPower() {
  powerData = powerData === 1 ? 0 : 1;
  console.log(powerData)
  postData();
}

function postData(d) { 
  httpPost("/effect", 'json', {'power': powerData, 'speed': speedData, 'file': fileData})
}

function getData() {
  httpGet("/effect", "json", false, (x) => {
    colorData = x;
    console.log(colorData);
  })
}