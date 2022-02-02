let effData;
let rgbData;
let powerButton;
let mainSlide;
let speedSlide;
let powerData = 1;
let speedData = 5;
let effect = "eff-white-up-slow";
let effectName = "White Up Slow";
let row = 90;
let mainLevel = 100;
let toPost = false;
let fgColor;
let bgColor;
let fgColorPicker;
let bgColorPicker;


function setup() {
  createCanvas(800, 500);

  fgColor = color(255, 0, 0);
  bgColor = color(0, 255, 0);

  makeEffectText();
  makeMainSlider();
  makeSpeedSlider();
  makeFGColorPicker()
  makeBGColorPicker()
  
  getEffectList();
  setTimeout(() => makeButtons(), 1000);
}

function draw(){
  background('white');
  fill('black')
  makeEffectText();
  fgColor = fgColorPicker.color();
  bgColor = bgColorPicker.color();
  fill(fgColor);
  square(350, 80, 100, 25);

  fill(bgColor);
  square(475, 80, 100, 25);

  let newMain = mainSlide.value();
  if (newMain !== mainLevel) {
    mainLevel = newMain;
    toPost = true;
  }
  let newSpeed = speedSlide.value();
  if (newSpeed !== speedData) {
    speedData = newSpeed;
    toPost = true;
  }
  if(toPost) {
    toPost = false
    console.log(fgColor.levels[1])
    postData();
  }
}

function makeEffectText() {
  textSize(32);
  text('Current Effect', 10, 30);
  textSize(24);
  text(effectName, 10, 60);
}

function makeMainSlider() {
  mainSlide = createSlider(0, 100, mainLevel, 1);
  mainSlide.position(150, 80);
  mainSlide.style('width', '200px');
}

function makeSpeedSlider() {
  speedSlide = createSlider(1, 10, speedData, 1);
  speedSlide.position(150, 200);
  speedSlide.style('width', '200px');
}

function makeFGColorPicker() {
  fgColorPicker = createColorPicker(fgColor);
  fgColorPicker.position(358, 190);
  fgColorPicker.style('width', '100px');
}

function makeBGColorPicker() {
  bgColorPicker = createColorPicker(bgColor);
  bgColorPicker.position(483, 190);
  bgColorPicker.style('width', '100px');
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
  httpPost("/effect", 'json', {'power': powerData, 
                              'speed': speedData, 
                              'effect': effect, 
                              'main': mainLevel,
                              'fg_color': {'r': fgColor.levels[0],
                                          'g': fgColor.levels[1],
                                          'b': fgColor.levels[2],},
                              'bg_color': {'r': bgColor.levels[0],
                                          'g': bgColor.levels[1],
                                          'b': bgColor.levels[2],},
                            });
}

function getEffectList() {
  httpGet("/effects", "json", false, (x) => {
    effData = x['effects'];
    console.log(effData);
  })
}