# Using a Tax on Digital Advertising to Work Toward a Less Dangerous Market for Digital Services

This repository generates a page that is deployed on a subdomain of my personal website: adtax.paulromer.net. This page takes a specification of a progressive tax schedule that could be applied to digital advertising and calculates two numbers: 

- How much tax it would collect. This is an indication of the incentive that a firm will have to switch to some other revenue model, e.g. subscriptions. 

- If the firm continues with a revenue model that relies on digital advertising, how much would the total tax bill go down if the firm were to split itself in two. 

This two measure quantify the incentives that the tax creates for a move away from the status quo with two dominant firms that rely on targeted digital advertising. See the text of the page for the reasons why I think that moving away from the status quo should be an urgent national priority. 

Reasonable people can differ. But the calculations provided here show that there is one reaction that is wrong. It is simply not true that the citizens of the United States are helpless. If they want to force a move away from our existing, pathological market for digital services, they can do it. And they can do it through their legislatures, even if unelected judges, accountable to no one, are opposed. 


# Under the hood
People who view the page using Chrome or Firefox on a desktop/laptop can provide their own tax schedule. The page uses the [Pyodide](https://pyodide.org) library to run Python in the browser that will redraw the graph of the average tax rate and recalculate the two measures of the incentive for firms to make a change. 

Because it is a challenge to get the full machinery of Python running in the browser (especially the Matplotlib library for creating graphs), this page runs Pyodide in a web worker. This means that the main page does not freeze while Pyodide is creating a full Python environment with two workhorses from the data science stack (Numpy and Matplotlib) inside the browser.

Pyodide does not yet work on mobile or Safari. People viewing the site using a mobile device or Safari on a desktop/laptop will see a static page that illustrates two possible tax schedules. 

