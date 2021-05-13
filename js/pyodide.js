async function loadPyodideAndPackages(){
    await loadPyodide({ indexURL : 'https://cdn.jsdelivr.net/pyodide/v0.17.0/full/' });
    await self.pyodide.loadPackage('matplotlib');
    await self.pyodide.runPython("import matplotlib.pyplot as plt")
    await self.pyodide.runPython("from matplotlib import ticker");
    await self.pyodide.runPython("import numpy as np");
    await self.pyodide.runPython("import io, base64");
    document.getElementById("run").classList.remove("hidden");
    let code = await readCode("./python/ad-tax.py");
    let html_table = await readCode("./python/html-table.py")
    pyodide.runPython(html_table);
    console.time('runcode');
    pyodide.runPython(code);
    console.timeEnd('runcode');
}

loadPyodideAndPackages()

async function readCode(file) {
    return  (await (await fetch(file)).text());
}

function executeCode() {
    input = editor.getDoc().getValue();
    pyodide.runPython(input);
    pyodide.runPython("table_marg = table_marg_rates(b, r)");
    pyodide.runPython("table_total = table_tax_paid_total(b, r)");
    document.getElementById("results").classList.remove("hidden")
    document.getElementById("marginal-rate-table-calculated").innerHTML=pyodide.globals.get("table_marg");
    document.getElementById("total-revenue-table-calculated").innerHTML=pyodide.globals.get("table_total");
    pyodide.runPython("calculated_graph = us_fig(b,r)");
    document.getElementById("avg-tax-rate-calculated").src=pyodide.globals.get("calculated_graph");
}

document.getElementById('run').addEventListener('click', function () {
    executeCode();
});
