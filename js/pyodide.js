async function loadPyodideAndPackages(){
    await loadPyodide({ indexURL : 'https://cdn.jsdelivr.net/pyodide/v0.17.0/full/' });
    await self.pyodide.loadPackage('matplotlib');
    console.log("loadPackage is done");
    // await self.pyodide.runPython("import matplotlib")
    await self.pyodide.runPython("import matplotlib.pyplot as plt")
    console.log("pyplot from main");
    await self.pyodide.runPython("from matplotlib import ticker");
    console.log("ticker from main");
    await self.pyodide.runPython("import numpy as np");
    console.log("numpy from main");
    await self.pyodide.runPython("import io, base64");
    console.log("io, base from main");
    document.getElementById("run").classList.remove("hidden");
}

loadPyodideAndPackages()

