
let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
  lineNumbers: true,
  viewportMargin: Infinity,
  mode: 'python',
  indentUnit: 4,
});

editor.setSize("100%", "350px");

let python_snippet = `# These are the brackets and marginal rates used above.
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

editor.getDoc().setValue(python_snippet); 
