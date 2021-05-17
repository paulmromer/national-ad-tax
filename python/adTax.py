
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from collections import namedtuple
    from IPython.display import display, HTML
    import io, base64
    from htmlTable import *

def ar(x: float, b: list, r: list):
    """
    Calculate the average tax rate

    Parameters
    ----------
    x, revenue 
    b, list of tax brackets
    r, corresponding list of tax rates 
    
    Returns
    -------
    average tax rate 
    """
    bl = b
    bu = (b[1:] + [np.inf])
    
    tp_bl = [0] + [ (bu[j]-bl[j]) * r[j] for j in range(0,len(b)-1) ]
    tp_cum = np.array(tp_bl).cumsum()

    a = 0
    for j in range(len(b)):
        if bl[j] < x and x <= bu[j]:
            a = ( (x - bl[j]) * r[j] + tp_cum[j] ) / x
    return a

def us_firms():
    """
    Returns a list and an ndarray.
    The elements of the list are namedtuples, one for each firm. Each of this has elements .name and .US_revenue.
        US_revenue is itself a namedtuple with elements "yr_2018" ... "yr_2023". For code the refers to specific years,
        the namedtuples are more readable. 

    The 13 by 6 ndarray has revenue for firms (rows) and years (columns).
    """
    us_firms_d = {
        'Amazon': [7.41, 10.32, 15.73, 20.47, 26.2, 31.97],
        'Facebook': [24.52, 31.27, 38.3, 48.48, 57.06, 65.38],
        'Google': [36.48, 41.8, 44.06, 54.93, 60.7, 66.47],
        'Hulu': [1.46, 1.95, 2.55, 3.39, 4.17, 4.98],
        'IAC': [0.5, 0.62, 0.55, 0.6, 0.64, 0.67],
        'Microsoft': [4.56, 5.29, 5.56, 6.65, 7.51, 8.3],
        'Reddit': [0.08, 0.1, 0.18, 0.25, 0.32, 0.37],
        'Roku': [0.29, 0.53, 0.83, 1.46, 2.06, 2.74],
        'Snapchat': [0.67, 0.88, 1.25, 1.82, 2.5, 3.33],
        'Spotify': [0.36, 0.45, 0.52, 0.7, 0.87, 1.03],
        'Twitter': [1.32, 1.6, 1.7, 2.21, 2.56, 2.75],
        'Verizon Media': [3.45, 3.36, 3.18, 3.44, 3.64, 3.79],
        'Yelp': [0.89, 0.96, 0.83, 0.92, 1.01, 1.07]
        }

    # namedtuple for revenue
    US_revenue = namedtuple("US_revenue", ["yr_2018", "yr_2019", "yr_2020", "yr_2021", "yr_2022", "yr_2023"])
    firms = []

    # namedtuple for a firm
    Firm_nt = namedtuple("Firm_nt", ["name", "us_rev"])
    for k, v in us_firms_d.items():
        firms.append(Firm_nt(k, US_revenue(*[rev for rev in v])))
    
    # firms_sorted is a list of namedtuples sorted by revenue in 2020
    firms_sorted:list = sorted(firms, key=lambda firm: firm.us_rev.yr_2020, reverse = True)
    rev_firm_year = np.zeros((13,6), dtype = float)
    for r in range(13):
        rev_firm_year[r] = np.array([firms_sorted[r][1]])
    return firms_sorted, rev_firm_year


def table_marg_rates(b, r):
    bl = b
    bu = (b[1:] + [np.inf])

    row_list = []
    row_list.append(f" For Revenue Between " + " " * 5 + "Marginal Tax Rate" + " " * 2)

    for j in range(len(b)):
        l = b[j]
        u = bu[j]
        t = r[j]
        if u == np.inf:
            row_list.append(" " * 6 + f"Above {l:>3} billion {t:>17.1%}" + " " * 8)
        else:
            row_list.append(" " * 5 + f" {l:>2} and {u:>2} billion {t:>17.1%}" + " " * 8)

    return h_table(row_list, font_size=12, row_margin = "4px", display_html = False, return_html = True)
    

def calc_avg_rates(rev, b, r):
    avg_rate = np.zeros((13,6), dtype = float)
    for row in range(13):
        for col in range(6):
            avg_rate[row,col] = ar(float(rev[row,col]), b, r)
    return avg_rate

def table_revenue_tax(b, r):
    _, rev = us_firms()
    total_rev_by_year = rev.sum(0)
    avg_rate = calc_avg_rates(rev, b, r)
    tax_owed = (rev * avg_rate).sum(0)
    year = "Year"
    tr = "Total Revenue   "
    td = "Tax Due"
    b = "(billion)"
    # blank = ""
    row_list = []
    row_list.append(f"{' ': ^2}{year: ^10}{tr: ^20}{td: ^10}{' ': ^3}")
    row_list.append(f"{'': ^12}{b: ^20}{b: ^12}{' ': ^2}")
    
    for j in range(6): 
        row_list.append(f"{' ': <5}{j+2018: <12d} {total_rev_by_year[j]: >6.1f} {tax_owed[j]: >14.1f}{' ': >6}")
    
    return h_table(row_list, header_rows = 2, font_size=12, row_margin = "4px", display_html = False, return_html = True)    



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

def split(s, b, r, revenue = 50):
    tax_bill = s * (ar(revenue/s, b, r)* revenue/s)
    return f"${tax_bill: <2.1f} billion"


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