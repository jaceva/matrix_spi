let effData;
let rgbData;
let powerButton;
let speedSlide;
let powerData = 1;
let speedData = 5;
let effect = "eff-white-up-slow";
let effectName = "White Up Slow";
let row = 90;


function setup() {
  createCanvas(500, 500);

  makeEffectText();
  makeSlider();
  
  getEffectList();
  setTimeout(() => makeButtons(), 1000);
}

function draw(){
  background('white');
  makeEffectText();

  let newSpeed = speedSlide.value();
  if (newSpeed !== speedData) {
    speedData = newSpeed;
    console.log(speedData)
    postData();
  }
}

function makeEffectText() {
  textSize(32);
  text('Current Effect', 10, 30);
  textSize(24);
  text(effectName, 10, 60);
}

function makeSlider() {
  speedSlide = createSlider(1, 10, speedData, 1);
  speedSlide.position(10, row);
  speedSlide.style('width', '80px');
  row += 30
}

function makeButtons() {
  // let p = 40
  for(let eff in effData) {
    console.log(eff)
    b = createButton(effData[eff]);
    b.position(10, row);
    b.mousePressed(() => {
      effect = eff;
      effectName = effData[eff];
      postData()
    });
    row += 30;
  }
}

function postData() { 
  console.log(effect);
  httpPost("/effect", 'json', {'power': powerData, 'speed': speedData, 'effect': effect});
}

function getEffectList() {
  httpGet("/effects", "json", false, (x) => {
    effData = x['effects'];
    console.log(effData);
  })
}