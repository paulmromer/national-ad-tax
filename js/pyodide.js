async function loadPyodideAndPackages(){
    await loadPyodide({ indexURL : 'https://cdn.jsdelivr.net/pyodide/v0.17.0/full/' });
    await self.pyodide.loadPackage('matplotlib');
    await self.pyodide.runPython("import matplotlib.pyplot as plt")
    await self.pyodide.runPython("from matplotlib import ticker");
    await self.pyodide.runPython("import numpy as np");
    await self.pyodide.runPython("import io, base64");
    await self.pyodide.runPython("from collections import namedtuple");
    document.getElementById("run").classList.remove("hidden");
    let code = await readCode("./python/adTax.py");
    let html_table = await readCode("./python/htmlTable.py")
    pyodide.runPython(html_table);
    pyodide.runPython(code);
}

loadPyodideAndPackages()

async function readCode(file) {
    return  (await (await fetch(file)).text());
}

function executeCode() {
    input = editor.getDoc().getValue();
    pyodide.runPython(input);
    pyodide.runPython("table_marg = table_marg_rates(b, r)");
    pyodide.runPython("table_rev_tax = table_revenue_tax(b, r)");
    document.getElementById("results").classList.remove("hidden")
    document.getElementById("marginal-rate-table-calculated").innerHTML=pyodide.globals.get("table_marg");
    document.getElementById("rev-tax-table-calculated").innerHTML=pyodide.globals.get("table_rev_tax");
    pyodide.runPython("calculated_graph = us_fig(b,r)");
    document.getElementById("avg-tax-rate-calculated").src=pyodide.globals.get("calculated_graph");
    pyodide.runPython("split_1 = split(1,b,r)");
    pyodide.runPython("split_2 = split(2,b,r)");
    pyodide.runPython("split_4 = split(4,b,r)");
    document.getElementById("split-1").innerHTML=pyodide.globals.get("split_1");
    document.getElementById("split-2").innerHTML=pyodide.globals.get("split_2");
    document.getElementById("split-4").innerHTML=pyodide.globals.get("split_4");
}

document.getElementById('run').addEventListener('click', function () {
    executeCode();
});
