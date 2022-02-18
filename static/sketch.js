let effData;
let rgbData;
let powerButton;
let mainSlide;
let speedSlide;
let powerData = 1;
let speedData = 5;
let effect = "rgb-pulse-slow";
let effectName = "Pulse Slow";
let row = 90;
let mainLevel = 100;
let toPost = false;
let fgColor;
let bgColor;
let fgColorPicker;
let bgColorPicker;
let frameCount = 0;


function setup() {
  createCanvas(1920, 1080);
  background(color(225,225,225));
  

  fgColor = color(255, 255, 255);
  bgColor = color(0, 0, 0);

  makeMainSlider(250,0);
  makeSpeedSlider(250, 100);
  makeFGColorPicker(500, 0);
  makeBGColorPicker(500, 100);
  makeTextScroll(250, 200);
  
  getEffectList();
  setTimeout(() => makeButtons(0, 100), 1000);
}

function draw(){
//   if(frameCount === 40) {
//     getEffectList();
//     setTimeout(() => makeButtons(0, 100), 1000);
//     frameCount = 0;
//   }
//   frameCount++;
  getEffectList();
  setTimeout(() => makeButtons(0, 100), 1000);
  makeEffectText(0, 0);
  mainSliderText(250, 0, 250, 100);
  speedSliderText(250, 100, 250, 100);
  fill('black')
  if(fgColor.levels[0] !== fgColorPicker.color().levels[0] ||
    fgColor.levels[1] !== fgColorPicker.color().levels[1] ||
    fgColor.levels[2] !== fgColorPicker.color().levels[2]) {

    fgColor = fgColorPicker.color();
    toPost = true;
  }
  if(bgColor.levels[0] !== bgColorPicker.color().levels[0] ||
    bgColor.levels[1] !== bgColorPicker.color().levels[1] ||
    bgColor.levels[2] !== bgColorPicker.color().levels[2]) {

    bgColor = bgColorPicker.color();
    toPost = true;
  }

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
    postData();
  }
}

function drawBorder(x, y, w, h) {
  noFill()
  rect(x+10, y+10, w-10, h-10);
}

function makeGif(x, y) {
  w = 500; 
  h = 100;
  drawBorder(x, y, w, h)
  fill(63,63,63);
  textSize(24);
  text('GIF Creation', x+20, y+35);
  textSize(12);

  text('GIF URL:', x+20, y+65);
  let gifUrl = createInput('');
  gifUrl.position(x+100, y+55);
  gifUrl.size(150);

  let textSubmit = createButton("Submit");
  textSubmit.position(x+30, y+130);
  textSubmit.style('width', '465px')
  textSubmit.style('height', '40px')
  textSubmit.mousePressed(() => {
    postGifUrl(gifUrl.value(),);
  });
}

function makeTextScroll(x, y) {
  w = 500; 
  h = 175;
  drawBorder(x, y, w, h)
  fill(63,63,63);
  textSize(24);
  text('Text Scroll Creation', x+20, y+35);
  textSize(12);

  text('Effect Name:', x+20, y+65);
  let effName = createInput('');
  effName.position(x+100, y+55);
  effName.size(150);

  text('Font:   Arial', x+250, y+65);

  text('Text Pixel Height:', x+20, y+90);
  let pixelHeight = createInput('');
  pixelHeight.position(x+123, y+80);
  pixelHeight.size(30);
  
  text('Pixels From Top:', x+150, y+90);
  let pixelTop = createInput('');
  pixelTop.position(x+250, y+80);
  pixelTop.size(30);

  text('Text:', x+20, y+115);
  let scrollText = createInput('');
  scrollText.position(x+70, y+105);
  scrollText.size(420);

  let urlSubmit = createButton("Submit");
  urlSubmit.position(x+30, y+130);
  urlSubmit.style('width', '465px')
  urlSubmit.style('height', '40px')
  urlSubmit.mousePressed(() => {
    postTextScroll(effName.value(), scrollText.value(), 
                  "DejaVuSans", pixelHeight.value(), pixelTop.value());
  });
}

function makeEffectText(x, y) {
  w = 250; 
  h = 100;
  fill(225,225,225);
  rect(x+5, y+5, w-5, h-5)
  drawBorder(x, y, w, h)
  fill(63,63,63)
  textSize(32);
  text('Current Effect', x+20, y+40);
  textSize(24);
  text(effectName, x+20, y+80);
}

function mainSliderText(x, y, w, h) {
  fill(225,225,225);
  rect(x+5, y+5, w-5, h-5)
  fill(63,63,63);
  textSize(32);
  text(`Brightness: ${mainLevel}`, x+20, y+40);
}

function makeMainSlider(x, y) {
  w = 250; 
  h = 100;
  drawBorder(x, y, w, h)
  mainSliderText(x, y, w, h)
  mainSlide = createSlider(0, 100, mainLevel, 1);
  mainSlide.position(x+20, y+80);
  mainSlide.style('width', '230px');
}

function speedSliderText(x, y, w, h) {
  fill(225,225,225);
  rect(x+5, y+5, w-5, h-5)
  fill(63,63,63);
  textSize(32);
  text(`Speed: ${speedData}`, x+20, y+40);
}

function makeSpeedSlider(x, y) {
  w = 250; 
  h = 100;
  drawBorder(x, y, w, h)
  speedSliderText(x, y, w, h)
  speedSlide = createSlider(1, 10, speedData, 1);
  speedSlide.position(x+20, y+80);
  speedSlide.style('width', '230px');
}

function makeFGColorPicker(x, y) { 
  w = 250; 
  h = 100;
  drawBorder(x, y, w, h);
  fill(63,63,63);
  textSize(24);
  text('Foreground Color', x+20, y+35);
  fgColorPicker = createColorPicker(fgColor);
  fgColorPicker.position(x+25, y+50);
  fgColorPicker.style('height', '50px');
  fgColorPicker.style('width', '230px');
}

function makeBGColorPicker(x, y) {
  w = 250; 
  h = 100;
  drawBorder(x, y, w, h);
  fill(63,63,63);
  textSize(24);
  text('Background Color', x+20, y+35);
  bgColorPicker = createColorPicker(bgColor);
  bgColorPicker.position(x+25, y+50);
  bgColorPicker.style('height', '50px');
  bgColorPicker.style('width', '230px');
}

function makeButtons(x, y) {
  w = 250
  h = 23

  for(let eff in effData) {
    b = createButton(effData[eff]);
    b.position(x+23, y+h);
    b.style('width', '230px')
    b.style('height', '25px')
    b.mousePressed(() => {
      effect = eff;
      effectName = effData[eff];
      postData()
    });
    h += 30;
  }
  drawBorder(x, y, w, h-7);
}

function postTextScroll(name, scrollText, font, height, top) {
  console.log(name)
  httpPost("/textscroll", 'json', {'name': name, 
                              'scrollText': scrollText, 
                              'font': font, 
                              'height': height,
                              'top': top,}
  )}

function postData() { 
  // console.log(effect);
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