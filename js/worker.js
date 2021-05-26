console.log("starting worker")

loadImportRun()

async function loadImportRun() {
    await runPyodideScript();
    await loadPyodideAsync();
    await pyodide.loadPackage('matplotlib');
    console.log("matplotlib fully loaded");
    await pyodide.runPython("import io, base64, os");
    console.log("io, base64, os imported");
    await pyodide.runPython("os.environ['MPLBACKEND'] = 'AGG'");
    // await pyodide.runPython("sys.setrecursionlimit(10**6)");
    console.log("backend changed to AGG");
    await pyodide.runPython("import matplotlib");
    console.log("matplotlib imported");
    await pyodide.runPython("import matplotlib.pyplot as plt");
    console.log("pyplot imported");
    await pyodide.runPython("import numpy as np");
    await self.pyodide.runPython("from collections import namedtuple");
    await self.pyodide.runPython("from matplotlib import ticker");
    console.log("numpy, namedtuple, ticker imported")
    postMessage(
        ["worker is ready", "", "", "", "","",""]
    )
    onmessage = async function(mm) {
        pyodide.runPython(mm.data); 
        console.log("Message received from main.js");
        pyodide.runPython(await (await fetch('https://vigilant-engelbart-b5423d.netlify.app/python/tablesGraphsSplit.py')).text());
        console.log("tablesGraphsSplit.py fetched and executed")
        // pyodide.runPython(await (await fetch('http://127.0.0.1:8000/python/htmlTable.py')).text());
        // pyodide.runPython(await (await fetch('http://127.0.0.1:8000/python/graphs.py')).text());
        pyodide.runPython("check_msg = check_tax_schedule(b,r)"); 
        check_msg = pyodide.globals.get("check_msg");
        // let check_msg = ""
        if (check_msg.length > 0) {
            postMessage(
                [check_msg, "", "", "", "", "", "", ""]
            )
        }
        else {
            
            pyodide.runPython("table_marg_rates_result = table_marg_rates(b, r)");
            console.log("marg_rates")
            pyodide.runPython("table_revenue_result = table_revenue(b, r)");
            console.log("revenue")
            pyodide.runPython("table_tax_result = table_tax(b, r)"); 
            console.log("tax")   
            pyodide.runPython("us_fig_result = us_fig(b, r)");
            console.log("us_fig")
            pyodide.runPython(
                "split_1_result = '$'+format(split(50, 1, b, r), '3.1f')"
                )
            pyodide.runPython(
                "split_2_result = '$'+format(split(50, 2, b, r), '3.1f')"
                )
            pyodide.runPython(
                "split_diff_result = '$'+format(split(50, 1, b, r) - split(50, 2, b, r), '3.1f')"
                )
            // pyodide.globals.get("table_marg_rates_result"),
            // pyodide.globals.get("table_revenue_result"),
            // pyodide.globals.get("table_tax_result"),
            // pyodide.globals.get("us_fig_result"),
            split_1_result = pyodide.globals.get("split_1_result"),
            split_2_result = pyodide.globals.get("split_2_result"),
            split_diff_result = pyodide.globals.get("split_diff_result")
            console.log("split" + split_1_result + split_2_result + split_diff_result)
            postMessage(
                ["",
                pyodide.globals.get("table_marg_rates_result"),
                pyodide.globals.get("table_revenue_result"),
                pyodide.globals.get("table_tax_result"),
                pyodide.globals.get("us_fig_result"),
                pyodide.globals.get("split_1_result"),
                pyodide.globals.get("split_2_result"),
                pyodide.globals.get("split_diff_result")
                ]
            )
        };
    }
}

async function runPyodideScript() {
    importScripts('https://cdn.jsdelivr.net/pyodide/v0.17.0/full/pyodide.js');
}

async function loadPyodideAsync() {
    await loadPyodide({ indexURL : 'https://cdn.jsdelivr.net/pyodide/v0.17.0/full/' });
}

// async function loadCode(file) {
//     c = fetch(file).text();
//     return c
// }

// async function loadCode(file) {
//     return  (await (await fetch(file)).text());
// }


// function loadcode(){
//     snippet = `def valid_tax_schedule(b,r):
//     invalid = """The tax schedule you submitted fails to meet one of these requirements: \n
//     1. b[0] must equal 0
//     2. b and r must have the same length 
//     3. b must be monotonically increasing"""
//     if not len(b) == len(r):
//         return invalid

//     if not b[0] == 0:
//         return invalid

//     b_diff = [b[j+1] - b[j] for j in range(len(b)-2)]
//     for diff in b_diff:
//         if diff <= 0:
//             return invalid
//     return ""`
//     return snippet
// }




