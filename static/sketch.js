let state = {
  effect_id: 'rgb-test-frame',
  bright: 100,
  speed: 100,
  // fg_color: {'r': 255, 'g': 255, 'b': 255},
  // bg_color: {'r': 0, 'g': 0, 'b': 0},
  fg_color: [255, 255, 255],
  bg_color: [0, 0, 0],
};

let labels = {
  bright: 'Brightness',
  speed: 'Speed',
  fg_color: 'Foreground Color',
  bg_color: 'Background Color',
}
let effectButton;
let inp;
let slider;
// let bright = 100;
let listBox;
let controlPosition = 0;
let panePosition = 0;

const ASPECT_RATIO = 1.33;
let pageWidth;
let pageHeight;

let controls = {};
let effects = undefined;
let rev_effects = {};
let cues = [];

function setup() {
  frameRate(2);
  createCanvas(windowWidth, windowHeight);

  getEffects(drawControls);
}

function draw() {
  // displayEffects()
  // console.log(state['bright']);
}

function updateState(stateVar) {
  state[stateVar] = controls[stateVar].value();
  postState();
}

class ColorPickerControl {
  constructor(prompt, x, y, width, height, changeFunction) {
    this.prompt = prompt;
    this.colorPicker = createColorPicker(255, 255, 255);

    this.changed(changeFunction);
    this.draw(x, y, width-10, height);
  }

  remove() {
    this.colorPicker.remove();
  }

  changed(changeFunction) {
    this.colorPicker.changed(() => {
      changeFunction();
      // this.draw();
    })
    this.draw();
    console.log(this.value());
  }

  value(newValue) {
    if(newValue === undefined) {
      return color(this.colorPicker.value()).levels.slice(0,3);
    }
    this.colorPicker.value(newValue);
    this.draw();
  }

  draw(x=this.x, y=this.y, width=this.width, height=this.height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;  

    this.drawBackground();
    this.drawColorPicker();
    this.drawPrompt();
  }

  drawBackground() {
    fill("#ffffff");
    noStroke();
    rect(this.x, this.y, this.width-20, this.height)
  }

  drawPrompt() {
    let promptY = this.y + (this.height * 0.1);
    fill('#000000')
    textSize(18)
    text(`${this.prompt}: ${this.colorPicker.value()}`, this.x, promptY);
  }

  drawColorPicker() {
    let colorPickerY = this.y + (this.height * 0.25);

    this.colorPicker.position(this.x, colorPickerY);
    this.colorPicker.style('width', this.width - 10);
    this.colorPicker.style('height', this.height * 0.6);
  }
}

class SliderControl {
  constructor(prompt, x, y, width, height, changeFunction) {
    this.prompt = prompt;
    this.slider = createSlider(0, 100, 100, 1);

    this.changed(changeFunction)
    this.draw(x, y+10, width-30, height);
  }

  remove() {
    this.slider.remove();
  }

  changed(changeFunction) {
    this.slider.changed(() => {
      changeFunction()
      // this.draw()
    })
    this.draw();
    console.log(this.value());
  }

  value(newValue) {
    if(newValue === undefined) {
      return this.slider.value();
    }
    this.slider.value(newValue);
    this.draw();
  }

  draw(x=this.x, y=this.y, width=this.width, height=this.height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;  

    this.drawBackground();
    this.drawSlider();
    this.drawPrompt();
  }

  drawBackground() {
    fill("#ffffff");
    noStroke();
    rect(this.x, this.y, this.width, this.height)
  }

  drawPrompt() {
    let promptY = this.y + (this.height * 0.25);
    fill('#000000')
    textSize(18)
    text(`${this.prompt}: ${this.slider.value()}`, this.x, promptY);
  }

  drawSlider() {
    let sliderY = this.y + (this.height * 0.5);
    this.slider.position(this.x, sliderY)
    this.slider.style('width', this.width);
  }
}

// Show preview thumb(s) of effect
// how to integrate color
// class PreviewControl {
//   constructor(prompt, items, x, y, width, height, changeFunction) {
//     this.prompt = prompt;
//     this.items = items;
//     // this.listBox = createSelect();

//     this.changed(changeFunction)
//     this.draw(x, y+10, width, height);
//   }

//   remove() {
//     console.log("PreviewControl remove() - Not implemented")
//   }
  
//   updateItems(items) {
//     this.items = items;
//     this.draw();
//   }

//   changed(changeFunction) {
//     this.listBox.changed(() => {
//       changeFunction()
//       // this.draw()
//     })
//     this.draw();
//     console.log(this.value());
//   }

//   value(newValue) {
//     if(newValue === undefined) {
//       return this.listBox.value();
//     }
//     this.listBox.value(newValue);
//     this.draw();
//   }

//   draw(x=this.x, y=this.y, width=this.width, height=this.height) {
//     this.x = x;
//     this.y = y;
//     this.width = width;
//     this.height = height;  

//     this.drawBackground();
//     this.drawPreview();
//     this.drawPrompt();
//     this.drawControls();
//   }

//   drawBackground() {
//     fill("#ffffff");
//     noStroke();
//     rect(this.x, this.y, this.width, this.height)
//   }

//   drawPrompt() {
//     let promptY = this.y + (this.height * 0.05);
//     fill('#000000')
//     textSize(18)
//     // TODO: add frames and current frame
//     text(`${this.prompt}`, this.x, promptY);
//   }

//   drawPreview() {
//     let previewY = this.y + (this.height * 0.10);
//     console.log("Preview - Draw Preview Not Implemented");
//   }

//   drawControls() {
//     console.log("Preview - Draw Controls Not Implemented");
//     // enable/disable preview checkbox
//     // pause/start effect
//     // prev/next frame
//   }
// }

class ListControl {
  constructor(prompt, items, x, y, width, height, changeFunction) {
    this.prompt = prompt;
    this.items = items;
    this.listBox = createSelect();
    Object.values(this.items).forEach(element => {
      this.listBox.option(element);
    });

    this.changed(changeFunction)
    this.draw(x, y+10, width, height);
  }
  
  remove() {
    this.listBox.remove();
  }
  
  getKey(value) {
    for (const key in this.items) {
      if (this.items[key] === value) {
        return key
      }
    }
    return undefined;
  }

  updateItems(items) {
    this.items = items;
    this.draw();
  }

  changed(changeFunction) {
    // this.listBox.changed(() => {
    //   changeFunction()
    //   this.draw()
    // })
    // this.draw();
  }

  value(newValue) {
    if(newValue === undefined) {
      return rev_effects[this.listBox.value()];
    }

    // TODO test this works
    this.listBox.value(newValue);
    this.draw();
  }

  draw(x=this.x, y=this.y, width=this.width, height=this.height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;  

    this.drawBackground();
    this.drawListBox();
    this.drawPrompt();
  }

  drawBackground() {
    fill("#ffffff");
    noStroke();
    rect(this.x, this.y, this.width, this.height)
  }

  drawPrompt() {
    let promptY = this.y + (this.height * 0.05);
    fill('#000000')
    textSize(18)
    text(`${this.prompt}`, this.x, promptY);
  }

  drawListBox() {
    let listBoxY = this.y + (this.height * 0.1);
    this.listBox.position(this.x, listBoxY);
    this.listBox.style('width', this.width);
    this.listBox.style('height', this.height * 0.9);
    this.listBox.attribute('multiple', 'multiple')
  }
}

class ButtonControl {
  constructor(prompt, x, y, width, height, changeFunction) {
    this.prompt = prompt;
    this.button = createButton(this.prompt);

    this.button.mousePressed(changeFunction);
    this.draw(x, y+10, width, height);
  }
  
  remove() {
    this.button.remove();
  }

  draw(x=this.x, y=this.y, width=this.width, height=this.height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;  

    this.drawBackground();
    this.drawListBox();
    // this.drawPrompt();
  }

  drawBackground() {
    fill("#ffffff");
    noStroke();
    rect(this.x, this.y, this.width, this.height)
  }

  drawPrompt() {
    let promptY = this.y + (this.height * 0.05);
    fill('#000000')
    textSize(18)
    text(`${this.prompt}`, this.x, promptY);
  }

  drawListBox() {
    let buttonY = this.y;
    this.button.position(this.x, buttonY);
    this.button.style('width', this.width);
    this.button.style('height', this.height);
  }
}

// Line 1: Effect Name bolded center
// Line 2: fg color, bf color

class CurrentEffectControl {
  constructor(prompt, current_effect, x, y, width, height, changeFunction) {
    this.prompt = prompt;
    this.currentEffect = currentEffect;

    this.draw(x, y+10, width, height);
  }
  
  value(newValue) {
    if(newValue === undefined) {
      return this.currentEffect;
    }
    this.currentEffect = newValue;
    this.draw();
  }

  remove() {
    ;
  }

  draw(x=this.x, y=this.y, width=this.width, height=this.height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;  

    this.drawBackground();
    // this.drawListBox();
    // this.drawPrompt();
  }

  drawBackground() {
    fill("#ffffff");
    noStroke();
    rect(this.x, this.y, this.width, this.height)
  }

  drawPrompt() {
    let promptY = this.y + (this.height * 0.05);
    fill('#000000')
    textSize(18)
    text(`${this.prompt}`, this.x, promptY);
  }

  drawListBox() {
    let buttonY = this.y;
    this.button.position(this.x, buttonY);
    this.button.style('width', this.width);
    this.button.style('height', this.height);
  }
}

function setEffect() {
  state['effect_id'] = controls['effect_list'].value();
  postState();
  // controls['current_effect'].value(effect)
  
  // console.log(`${effect}: NOT IMPLEMENTED need current_effect control`);
}

function cueNext() {

  cues = [{
    effect_id: controls['effect_list'].value(),
    bright: controls['bright'].value(),
    speed: controls['speed'].value(),
    fg_color: controls['fg_color'].value(),
    bg_color: controls['bg_color'].value(),
  }, ...cues];


  console.log(cues);
  // get effect list value
  // put at top of cue list

}

function cuePosition() {
  // get effect list value
  // put at location of cue list
}

function cueLast() {
  // get effect list value
  // put at end of cue list
}

function prevCue() {
  // highlight prev cue
}

function nextCue() {
  // highlight next cue
}

function playPauseCue() {
  // stop the wall at current frame
  // POST data
}

function shiftUpCue() {
  // move selected cue up one
}

function shiftDownCue() {
  // move selected cue down one
}

function deleteCue() {
  // toggle delete cue button
}

function confirmDeleteCue() {
  // delete selected from cuelist
  // change delete cue status
}



function drawControls() {
  Object.values(controls).forEach(control => {
    control.remove();
  });
  noStroke()
  rect(0, 0, windowWidth, windowHeight)
  panePosition = 0;
  let tempWidth = windowHeight / ASPECT_RATIO;
  
  if (tempWidth > windowWidth) {
    pageWidth = windowWidth - 25;
    pageHeight = int(windowHeight * ASPECT_RATIO) -25;
  } else {
    pageWidth = int(tempWidth);
    pageHeight = int(windowHeight) - 25;
  }
  drawTopController();
  drawEffectController();
  drawCueController();
}

function drawBorder(heightPercentage) {
  fill('#ffffff');
  stroke('#000000')
  controlHeight = int(pageHeight * heightPercentage)
  // console.log(controlHeight, panePosition);
  strokeWeight(4);
  rect(0, panePosition, pageWidth, controlHeight);
  // panePosition += controlHeight;

  return controlHeight;
}

function drawTopController() {
  let heightPercentage = 0.3;
  controlHeight = drawBorder(heightPercentage);
  controlPosition = panePosition;
  panePosition += controlHeight;

  brightHeight = int(controlHeight * 0.25)
  speedHeight = int(controlHeight * 0.25)
  colorHeight = int(controlHeight * 0.5)
  
  controls['bright'] = new SliderControl(labels['bright'], 20, controlPosition, pageWidth, brightHeight, () => updateState('bright'));
  controlPosition += brightHeight;
  controls['speed'] = new SliderControl(labels['speed'], 20, controlPosition, pageWidth, speedHeight, () => updateState('speed'));
  controlPosition += speedHeight;
  controls['fg_color'] = new ColorPickerControl(labels['fg_color'], 20, controlPosition, pageWidth/2, colorHeight, () => updateState('fg_color'));
  controls['bg_color'] = new ColorPickerControl(labels['bg_color'], pageWidth/2, controlPosition, pageWidth/2, colorHeight, () => updateState('bg_color'));

  // return controlPosition;
}

function drawEffectController() {
  let heightPercentage = 0.35;

  controlWidth = pageWidth;
  controlHeight = drawBorder(heightPercentage);
  controlPosition = panePosition;
  panePosition += controlHeight;
  
  listWidth = int(controlWidth * 0.33);
  listHeight = int(controlHeight * 0.7);

  previewWidth = int(controlWidth * 0.67);
  previewHeight = int(controlHeight * 0.7);

  buttonWidth = int(controlWidth / 4.15);
  buttonHeight = int(controlHeight * 0.25);
  

  controls['effect_list'] = new ListControl('Effects', effects, 20, controlPosition, listWidth, listHeight, () => {console.log("List Changed!")});
  
  controlPosition += listHeight;
  controls['set_effect'] = new ButtonControl('Set Effect', (0 * buttonWidth) + 20, controlPosition + 5, buttonWidth, buttonHeight, setEffect);
  controls['cue_next'] = new ButtonControl('Cue Next', (1 * buttonWidth) + 20, controlPosition + 5, buttonWidth, buttonHeight, cueNext);
  controls['cue_position'] = new ButtonControl('Cue Position', (2 * buttonWidth) + 20, controlPosition + 5, buttonWidth, buttonHeight, () => {console.log("Set Now")});
  controls['cue_last'] = new ButtonControl('Cue Last', (3 * buttonWidth) + 20, controlPosition + 5, buttonWidth, buttonHeight, () => {console.log("Set Now")});


  // drawEffectPreview();
  // drawEffectController();

  // return controlPosition;
}

function drawCueController() {
  let heightPercentage = 0.35;

  controlWidth = pageWidth;
  controlHeight = drawBorder(heightPercentage);
  controlPosition = panePosition;
  panePosition += controlHeight;
  
  listWidth = int(controlWidth * 0.33);
  listHeight = int(controlHeight * 0.95);


  effectWidth = int(controlWidth * 0.67);
  effectHeight = int(controlHeight * 0.25);

  buttonWidth = int((controlWidth * 0.66) / 3.15);
  shortButtonHeight = int(controlHeight * 0.23);
  tallButtonHeight = int(controlHeight * 0.46);

  controls['cue_list'] = new ListControl('Cue List', cues, 20, controlPosition, listWidth, listHeight, () => {console.log("List Changed!")});
  // controls['current_effect']
  controlPosition += effectHeight;
  controls['prev'] = new ButtonControl('<<<', listWidth + (0 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
  controls['next'] = new ButtonControl('>>>', listWidth + (1 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
  controls['play_pause'] = new ButtonControl('Play/Pause', listWidth + (2 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
  
  controlPosition += shortButtonHeight;
  controls['shift_up'] = new ButtonControl('Shift Up', listWidth + (0 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
  controls['delete'] = new ButtonControl('Delete', listWidth + (1 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
  controls['go'] = new ButtonControl('GO', listWidth + (2 * buttonWidth) + 20, controlPosition + 5, buttonWidth, tallButtonHeight, () => {console.log("Set Now")});
  
  controlPosition += shortButtonHeight;
  controls['shift_down'] = new ButtonControl('Shift Down', listWidth + (0 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
  controls['confirm_delete'] = new ButtonControl('CONFIRM DELETE', listWidth + (1 * buttonWidth) + 20, controlPosition + 5, buttonWidth, shortButtonHeight, () => {console.log("Set Now")});
 

}

function windowResized() {
  // console.log(windowWidth, windowHeight);
  
  //createCanvas(windowWidth, windowHeight);
  drawControls();
}

function getEffects(afterFunction = () => {}) {
  httpGet("/effects", "json", false, (e) => {
    effects = {...e['effects']};
    for(let key in effects) {
      rev_effects[effects[key]] = key;
    }

    // console.log(effects);
    // console.log(Object.values(effects));
    afterFunction()
  })
}

// function getState() {
//   httpGet("/state", "json", false, (s) => {
//     state = s;
//     console.log(state);
//   })
// }

function postState() {
  // updateState()
  httpPost("/state", "json", state, (response) => {
    state = response['state']
    console.log(state)
  })
}
