let colorData;
let powerButton;
let speedSlide;
let powerData = 1;
let speedData = 5;
let fileData = 'white-mid';


function setup() {
  createCanvas(500, 500);
  background('white');
  
  getData();
  speedSlide = createSlider(1, 10, speedData, 1);
  speedSlide.position(10, 10);
  speedSlide.style('width', '80px');
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
    b.position(10, p);
    b.mousePressed(() => {
      fileData = colorData[f]
      postData()
    });
    p += 30;
  }
}

function draw(){
  let newSpeed = speedSlide.value();
  if (newSpeed !== speedData) {
    speedData = newSpeed;
    console.log(speedData)
    postData();
  }
  
}

// function ledPower() {
//   powerData = powerData === 1 ? 0 : 1;
//   console.log(powerData)
//   postData();
// }

function postData(d) { 
  httpPost("/effect", 'json', {'power': powerData, 'speed': speedData, 'file': fileData})
}

function getData() {
  httpGet("/effect", "json", false, (x) => {
    colorData = x;
    console.log(colorData);
  })
}