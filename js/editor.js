
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
# The hash or pound sign like the one at the beginning of a line denotes a comment. 
# The code above that specifies the default values for b(the brackets) and r (the marginal rates)
#      includes extra spaces for b to indicate that these lists have to have the same length. 
# 
# To try some different values for b and r, you can edit the code above or just delete the hash 
#      from a pair of lines below. To clarify what you are doing, if you uncomment some of the
#      lines below, you could comment out the lines above or just delete them. 
# 
# Alternative 1: Set marginal rate to 40% for all revenue above $30 billion per year:
# 
# b = [0,    5,    10,   15,    20,   25,   30]
# r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.40]
# 
# Alternative 2: Specify a value for f then multiply all the rates by the factor f: 
# 
# f = 0.80
# b = [0,    5,    10,   15,    20,   25,    30,   35,    40,   50,    60]
# r = [0, 0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725]
# r = [ rate * f for rate in r]` 

editor.getDoc().setValue(python_snippet); 
