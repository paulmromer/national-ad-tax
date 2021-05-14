
let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
  lineNumbers: true,
  viewportMargin: Infinity,
  mode: 'python',
  indentUnit: 4,
});

editor.setSize("100%", "350px");

let python_snippet = `b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
#
# The hash or pound sign at the beginning of a line denotes a comment. 
# The lines of code above specify the default values for b (the brackets)
#     and r (the marginal rates). 
# 
# To try different values, you can edit those lines or delete the hash 
#      from the lines in one of the two alternatives below.
# 
# Alternative 1: Set marginal rate to 40% for revenue above $30 billion:
# 
# b = [0,    5,    10,   15,    20,   25,   30]
# r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.40]
# 
# Alternative 2: Specify a value for f; multiply all the rates by that factor: 
# 
# f = 0.80
# b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
# r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
# r = [ rate * f for rate in r]` 

editor.getDoc().setValue(python_snippet); 
