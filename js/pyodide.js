function delay(n){
    return new Promise(function(resolve){
        setTimeout(resolve,n*1000);
    });
}

async function loadPyodideAndPackages(){
    // wait for time specified in delay 
    console.log('waiting')
    await delay(10)
    console.log('done waiting')
    // load pyodide
    await loadPyodide({ indexURL : 'https://cdn.jsdelivr.net/pyodide/v0.17.0/full/' });
   
    // import base64, io and named tupples
    await self.pyodide.runPython("import io, base64");
    await self.pyodide.runPython("from collections import namedtuple");
 
    // load matplotlib if we are not on safari  
    if ( detectSafariOrMobile() == false ) {
        await self.pyodide.loadPackage('matplotlib');
        await self.pyodide.runPython("import matplotlib.pyplot as plt")
        await self.pyodide.runPython("from matplotlib import ticker");
    }  
   
    // for safari, load numpy
    // numpy is indirectly loaded with matplotlib on other browsers
    if (detectSafariOrMobile() == true ) {
        await self.pyodide.loadPackage('numpy');   
        // hide any graph elements on safari
        hideGraphElements();
    } 

    await self.pyodide.runPython("import numpy as np");
   
    let code = await readCode("./python/adTax.py");
    let html_table = await readCode("./python/htmlTable.py")
   
    pyodide.runPython(html_table);
    pyodide.runPython(code);

    if (detectSafariOrMobile() == false ) {
        let graphs = await readCode("./python/graphs.py");
        pyodide.runPython(graphs);
    }

    document.getElementById("run").classList.remove("hidden");

}

loadPyodideAndPackages()

async function readCode(file) {
    return  (await (await fetch(file)).text());
}

function executeCode() {
    input = editor.getDoc().getValue();
    try {
        // clear placeholder and any error messages from previous runs 
        document.getElementById('us_estimates_error').classList.add('hidden');
        document.getElementById('placeholder').classList.add('hidden');
        // run python code

        pyodide.runPython(input);
        pyodide.runPython("table_marg = table_marg_rates(b, r)");
        document.getElementById("marginal-rate-table-calculated").innerHTML=pyodide.globals.get("table_marg");
        document.getElementById("results").classList.remove("hidden")

        pyodide.runPython("table_total = table_revenue_tax(b, r)");
        document.getElementById("rev-tax-table-calculated").innerHTML=pyodide.globals.get("table_total");
        
        if (detectSafariOrMobile() == false ) {
            pyodide.runPython("calculated_graph = us_fig(b,r)");
            document.getElementById("avg-tax-rate-calculated").src=pyodide.globals.get("calculated_graph");
        } 

        pyodide.runPython("split_1 = split(60, 1, b, r)");
        pyodide.runPython("split_2 = split(60, 2, b, r)");
        pyodide.runPython("split_diff = split_1 - split_2");
        pyodide.runPython("split_1_str = '$'+format(split_1, '3.1f')")
        pyodide.runPython("split_2_str = '$'+format(split_2, '3.1f')")
        pyodide.runPython("split_diff_str = '$'+format(split_diff, '3.1f')")
        document.getElementById("split-1").innerHTML=pyodide.globals.get("split_1_str");
        document.getElementById("split-2").innerHTML=pyodide.globals.get("split_2_str");
        document.getElementById("split-diff").innerHTML=pyodide.globals.get("split_diff_str");

    } catch(err) {
        message = '<div class="mb-2">Oops! There seems to be a problem with the code you submitted. Please take a look to see if there is a line number in the error message below. If so, try editing the line and click the run button again. For example, be sure that you have not added a space before either of the variables, b and r.</div>'
        showPythonError(err, message, "us_estimates_error");
    }
}

function showPythonError(err, message, div_id){
    el =  document.getElementById(div_id);
    el.classList.remove('hidden');
    el.innerHTML = message + err.message;
}

document.getElementById('run').addEventListener('click', function () {
    executeCode();
});

function hideGraphElements() {
    document.getElementById('avg-tax-rate-calculated').remove();
    document.getElementById('avg-tax-rate-calculated-container').innerHTML = '<div class="error">To see a new graph based on your changes to the tax brackets and rates, please come back to this page from a desktop machine using Chrome, Firefox or Edge.</div>'
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