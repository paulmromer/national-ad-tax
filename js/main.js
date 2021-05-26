

if (detectSafariOrMobile()) {
  console.log("yes safari");
  // document.getElementById("avg-tax-rate-calculated").src=wm.data[4]
  document.getElementById("results").classList.remove("hidden");
  document.getElementById("placeholder").classList.add("hidden");
  document.getElementById("split-1").innerHTML="$22.5";
  document.getElementById("split-2").innerHTML="$15.0";
  document.getElementById("split-diff").innerHTML="$7.5";

}
else {
  const myWorker = new Worker("./js/worker.js");
  document.getElementById("as-the-next-schedule").classList.add("hidden");
  let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: false,
    viewportMargin: Infinity,
    mode: 'python',
    indentUnit: 4,
  });

  document.getElementById("editor-div").classList.remove("hidden")

  editor.setSize("100%", "350px");
    
    let initial_editor_text = `
# These are the brackets and marginal rates used above.
#
#b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
#r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
#
# The hash at the beginning of a line marks it as a comment. If you click 
#     the Run button without making any changes, it will redo the calculations 
#     using these two un-commented lines:
# 
b = [0,    5,   10,   15,   20,   25]
r = [0, 0.10, 0.20, 0.30, 0.40, 0.50] 
#
# Uncomment the last four lines and change f to scale the rates up or down.
# 
#f = 0.5
#b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
#r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
#r = [ min(rate * f, 1.0) for rate in r]

# Or type in any other system of brackets and rates that you want to explore.` 

  editor.getDoc().setValue(initial_editor_text); 
  console.log("initial_editor_text")
  myWorker.onmessage = function(wm) {
  if (wm.data[0] == "worker is ready") {
    console.log("worker is ready msg received by main");
    document.getElementById("run").classList.remove("hidden");
    document.getElementById("placeholder").classList.add("hidden");
    document.getElementById('run').addEventListener('click', function () {
      let current_editor_text = editor.getDoc().getValue();
      myWorker.postMessage(current_editor_text);
      console.log("run clicked first time");
    });
    
  }
  else{
    try {
      // clear placeholder and any error messages from previous runs 
      document.getElementById('us_estimates_error').classList.add('hidden');
      document.getElementById('placeholder').classList.add('hidden');
      document.getElementById('editor-instructions').classList.remove('hidden');
      document.getElementById("you-clicked").classList.remove('hidden');

      document.getElementById("marginal-rate-table-calculated").innerHTML= wm.data[1];
      
      document.getElementById("rev-table-calculated").innerHTML=wm.data[2];
      document.getElementById("tax-table-calculated").innerHTML=wm.data[3];
      document.getElementById("avg-tax-rate-calculated").src=wm.data[4];
      
      // if (detectSafariOrMobile() == false ) {
      //     document.getElementById("avg-tax-rate-calculated").src=wm.data[4];
      // } 

      document.getElementById("split-1").innerHTML=wm.data[5];
      document.getElementById("split-2").innerHTML=wm.data[6];
      document.getElementById("split-diff").innerHTML=wm.data[7];
      document.getElementById("run").classList.remove("hidden");
      document.getElementById("results").classList.remove("hidden");

      document.getElementById('run').addEventListener('click', function () {
        let current_editor_text = editor.getDoc().getValue()
        myWorker.postMessage(current_editor_text);
        console.log("run clicked subsequent times");
      });
    }
    catch(err) {
      message = '<div class="mb-2">Oops! There seems to be a problem with the code you submitted. Please take a look to see if there is a line number in the error message below. If so, try editing the line and click the run button again. For example, be sure that you have not added a space before either of the variables, b and r.</div>'
      showPythonError(err, message, "us_estimates_error");
    }

    }
  } 

  myWorker.onmessageerror = function(error) {
    console.log(error);
  };
}


// function hideGraphElements() {
//   document.getElementById('avg-tax-rate-calculated').remove();
//   document.getElementById('avg-tax-rate-calculated-container').innerHTML = '<div class="error">To see a new graph based on your changes to the tax brackets and rates, please come back to this page from a desktop machine using Chrome, Firefox or Edge.</div>'
// }

function showPythonError(err, message, div_id){
  el =  document.getElementById(div_id);
  el.classList.remove('hidden');
  el.innerHTML = message + err.message;
}


function detectSafariOrMobile(){
  // get the browser
  const browser = get_browser().name.toLowerCase();  

  if (browser == 'safari') {
      return true;
  }
  
  if (detectmob()) {
      return true;
  }

  return false;
}

// detect mobile
// https://stackoverflow.com/questions/11381673/detecting-a-mobile-browser
function detectmob() { 
  if( navigator.userAgent.match(/Android/i)
  || navigator.userAgent.match(/webOS/i)
  || navigator.userAgent.match(/iPhone/i)
  || navigator.userAgent.match(/iPad/i)
  || navigator.userAgent.match(/iPod/i)
  || navigator.userAgent.match(/BlackBerry/i)
  || navigator.userAgent.match(/Windows Phone/i)
  ){
     return true;
   }
  else {
     return false;
   }
}
// get browser
// https://stackoverflow.com/questions/5916900/how-can-you-detect-the-version-of-a-browser
function get_browser() {
  var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []; 
  if(/trident/i.test(M[1])){
      tem=/\brv[ :]+(\d+)/g.exec(ua) || []; 
      return {name:'IE',version:(tem[1]||'')};
      }   
  if(M[1]==='Chrome'){
      tem=ua.match(/\bOPR|Edge\/(\d+)/)
      if(tem!=null)   {return {name:'Opera', version:tem[1]};}
      }   
  M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
  if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
  return {
    name: M[0],
    version: M[1]
  };
}

console.log("after defn of dectedSafariOrMobile");
