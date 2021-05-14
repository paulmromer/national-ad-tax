
let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
  lineNumbers: true,
  viewportMargin: Infinity,
  mode: 'python',
  indentUnit: 4,
});

editor.setSize("100%", "350px");

let python_snippet = `# Default
#b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
#r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
#
# The hash or pound sign at the beginning of a line denotes a comment. 
# The code here is set to run the uncommented lines for Alt #1. 
# For reference, the lines above specify the defaults used above for 
# b (the brackets) and r (the marginal rates). 
# 
# Alt 1: Set marginal rate to 40% for revenue above $30 billion:
# 
b = [0,    5,    10,   15,    20,   25,   30]
r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.40]
# 
# Alt 2: Multiply all rates by a factor f. To run, uncomment lines 29-32. 
# They run last and will overwrite values from Alt 1. 
# 
#f = 0.5
#b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
#r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
#r = [ rate * f for rate in r]` 

editor.getDoc().setValue(python_snippet); 
