if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from collections import namedtuple
    from IPython.display import display, HTML
    import io, base64
    from htmlTable import *
    
    
base_style = {
    'figure.dpi':                   300,  # in a notebook, higher dpi makes the graph larger   
    'figure.figsize':  [3*1.6180339, 3],  # constrain the size and use the golden ratio to set the size
    'figure.facecolor':         'white',
    'figure.titlesize':               8,
    'axes.titlesize':                 8,  # the default font sizes have to be smaller bc of the higher dpi
    'axes.labelsize':                 6,
    'ytick.labelsize':                5,
    'xtick.labelsize':                5,
    'legend.fontsize':                5,
    'lines.linewidth':                1,
    'lines.markersize':               3,
    'xtick.major.size':             2.0,
    'xtick.major.width':            0.3,
    'ytick.major.size':             2.0,
    'ytick.major.width':            0.3,
}

def floating_spines(ax, axis = 'l'):
    """[summary]

    Parameters
    ----------
    ax : [type]
        [description]
    axis : str, optional
        [description], by default 'l'

    Returns
    -------
    [type]
        [description]
    """
    ax.spines['top'].set_visible(False)
    if axis == 'l':
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['left'].set_linewidth(0.2)
        ax.spines['left'].set_position(('outward', 5))
    else:
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(True)
        ax.spines['right'].set_linewidth(0.2)
        ax.spines['right'].set_position(('outward', 5))

    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_linewidth(0.2)
    ax.spines['bottom'].set_position(('outward', 5))
    return ax


def us_fig(b: list, r: list):
    """
    """
    firms, _ = us_firms()
    # avg_rate = calc_avg_rates(rev)

    names = [firm.name for firm in firms]
    rev_2021 = [firm.us_rev.yr_2021 for firm in firms]
    avg_rate_2021 = [ ar(firm.us_rev.yr_2021, b, r) for firm in firms]
    tax_paid_2021 = np.array([ar(firm.us_rev.yr_2021, b, r) * firm.us_rev.yr_2021 for firm in firms])

    rev_for_line = range(60)
    ar_for_line = [ar(x, b, r) for x in rev_for_line]
    
    adjustments = [
            (+0.5, -4, "\n $"+format(tax_paid_2021[0], "<3.1f"), 0),
            (+0.5, -4, "\n $"+format(tax_paid_2021[1], "<3.1f"), 1),
            (+0.5, -4, "\n $"+format(tax_paid_2021[2], "<3.1f"), 2),
            (+2.0, -1, ": $"+format(tax_paid_2021[3], "<3.1f"), 3),
            (+2.0, -6, "All others: " + "$"+format(tax_paid_2021[4:].sum(), "<3.1f"), 4)
        ]
    
    with plt.style.context(base_style):
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.15, 0.8, 0.75])
        ax = floating_spines(ax)
        ax.set_xlim(-1, 60)
        ax.set_ylim(-0.01, 0.5)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1.0, decimals = 0))
        ax.spines['left'].set_bounds(low = 0, high = 0.5)
        ax.spines['bottom'].set_bounds(low = 0, high = 60)
        ax.plot(rev_for_line, ar_for_line)
        ax.plot(rev_2021, avg_rate_2021, ls = '', marker = 'o', ms = 1.5)
        for j in range(len(adjustments)-1):
            ax.text(
                rev_2021[j] + adjustments[j][0], 
                avg_rate_2021[j] + adjustments[j][1]/100, 
                names[j] + adjustments[j][2], fontsize = 6
            ) 
        
        ax.set_title("Average Tax Rate, Total Revenue, and Tax Due", pad = 10)
        ax.axes.xaxis.set_label_text("Projected US Revenue for 2021 (billion USD)")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_str = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
    # if __name__ == "builtins":
    #     print("Saving png")
    #     fig.savefig("../graphs/fig-us-default.png")   
    return img_str

def ww_fig(b,r):
    """
    """
    ww_rev_for_graph = range(150)
    ww_ar_for_graph = [ar(x, b, r) for x in ww_rev_for_graph]

    ww_rev = {
        "Amazon": 26309972874.28,
        "Facebook": 107723102210.00,
        "Google": 130145195979.30,
        "IAC": 734739747.00,
        "Microsoft": 8960366731.10,
        "Reddit": 261098903.52,
        "Snapchat": 3206780000.00,
        "Spotify": 1100807642.44,
        "Twitter": 4028869581.75,
        "Verizon Media": 4589668440.03,
        "Yelp": 929364566.42,
    }

    ww_rev_l = list(ww_rev.items())
    ww_rev_sorted = sorted(ww_rev_l, key=lambda company: company[1], reverse = True)
    ww_names = [ firm[0] for firm in ww_rev_sorted ]
    ww_rev_2021 = [ company[1]/10**9 for company in ww_rev_sorted ]
    ww_avg_r = [ ar(y, b, r) for y in ww_rev_2021]
    ww_tax_paid = [ar(y, b, r) * y  for y in ww_rev_2021]
    
    adjustments = [
        (+1, -4, "\n $"+format(ww_tax_paid[0], "<3.1f"), 0),
        (+1, -4, "\n $"+format(ww_tax_paid[1], "<3.1f"), 1),
        (+1.5, -4, "\n $"+format(ww_tax_paid[2], "<3.1f"), 2),
       (+2.0, -2, "All others", 3)
    ]
    with plt.style.context(base_style):
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.15, 0.8, 0.75])
        ax = floating_spines(ax)
        ax.set_xlim(-1, 150)
        ax.set_ylim(-0.01,0.5)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1.0, decimals = 0))
        ax.spines['bottom'].set_bounds(low = 0, high = 150)
        ax.spines['left'].set_bounds(low = 0, high = 0.5)
        ax.plot(ww_rev_for_graph, ww_ar_for_graph)
        ax.plot(ww_rev_2021, ww_avg_r, ls = '', marker = 'o', ms = 1.5)
        for j in range(len(adjustments)-1):
            ax.text(
                ww_rev_2021[j] + adjustments[j][0],
                ww_avg_r[j] + adjustments[j][1]/100, 
                ww_names[j] + adjustments[j][2], 
                fontsize = 6
            ) 

        ax.set_title("Average Tax Rate, Worldwide Revenue, Tax Due", pad = 10)
        ax.axes.xaxis.set_label_text("Projected Worldwide Revenue for 2021 (billion USD)")
            
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_str = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
    # if __name__ == "builtins":
    #     print("Saving png")
    #     fig.savefig("../graphs/fig-ww-default.png")
    return