console.log("starting worker")

const myInit = {
    mode: 'same-origin',
    headers: {
        'Accept': 'data'
      },
    cache: 'reload'
  };

let myRequest = new Request('https://adtax.paulromer.net/js/pyodide/matplotlib.data');

fetch(myRequest, myInit)
.then(function(response) {
  if (!response.ok) {
    console.log("second fetch")
    fetch(myRequest, myInit);
  }
  return;
}).then(loadImportRun())
    
// fetch(myRequest, myInit)
//     .then(loadImportRun())

// loadImportRun()

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

async function loadImportRun() {
    importScripts('/js/pyodide/pyodide.js');
    let pyodide = await loadPyodide({ indexURL : '/js/pyodide/' });
    await pyodide.loadPackage('matplotlib');
    await sleep(10);
    
    await pyodide.runPython("import io, base64, os");
    await pyodide.runPython("os.environ['MPLBACKEND'] = 'AGG'");
    
    await(5);
    await pyodide.runPython("import matplotlib");
    
    await sleep(5);
    await pyodide.runPython("import matplotlib.pyplot as plt");
    
    await sleep(5);
    await pyodide.runPython("import numpy as np");
    
    await sleep(5);
    await pyodide.runPython("from collections import namedtuple");
    await pyodide.runPython("from matplotlib import ticker");
    
    console.log("worker is ready")
    
    postMessage(
        ["worker is ready", "", "", "", "","",""]
    )
    onmessage = async function(mm) {
        pyodide.runPython(mm.data); 
        pyodide.runPython(await (await fetch('/python/tablesGraphsSplit.py')).text());
        pyodide.runPython("check_msg = check_tax_schedule(b,r)"); 
        check_msg = pyodide.globals.get("check_msg");
        if (check_msg.length > 0) {
            postMessage(
                [check_msg, "", "", "", "", "", "", ""]
            )
        }
        else {
            
            pyodide.runPython("table_marg_rates_result = table_marg_rates(b, r)");
            pyodide.runPython("table_revenue_result = table_revenue(b, r)");
            pyodide.runPython("table_tax_result = table_tax(b, r)"); 
            pyodide.runPython("us_fig_result = us_fig(b, r)");
            pyodide.runPython(
                "split_1_result = '$'+format(split(50, 1, b, r), '3.1f')"
                )
            pyodide.runPython(
                "split_2_result = '$'+format(split(50, 2, b, r), '3.1f')"
                )
            pyodide.runPython(
                "split_diff_result = '$'+format(split(50, 1, b, r) - split(50, 2, b, r), '3.1f')"
                )
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
