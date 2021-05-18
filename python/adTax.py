def ar(y, b, r):
    """
    Calculates the average tax rate for a firm. 

    Inputs
    -----------
    y, digital advertising revenue for a firm 
    b, a list of tax brackets
    r, a corresponding list of tax rates 
    
    Output
    -------
    The average tax rate 
    """
    # ind is an index for elements in b
    ind = {}
    for m, l in enumerate(b):
        ind[l] = m

    #tbl means the tax due on revenue equal to the lower limit of a tax bracket. 
    tbl = {}
    for l in b:
        if l == 0:
            tbl[l] = 0
        else:
            tbl[l] = ( b[ind[l]] - b[ind[l]-1] ) * r[ind[l]-1] + tbl[b[ind[l]-1]]
    
    if y == 0:
        a = 0 
        
    for j in range(len(b)-1):
        if b[j] < y and y <= b[j+1]:
            a = ( (y - b[j]) * r[j] + tbl[b[j]] ) / y
    
    if  b[-1] < y:
        a = ( (y - b[-1]) * r[-1] + tbl[b[-1]] ) / y 
    
    return a

def split(y, m, b, r):
    """[summary]

    Parameters
    ----------
    y:float -- revenue of the initial firm
    m:int -- number of successor firms of equal size 
    b:float -- brackets
    r:float -- marginal rates 

    Output
    ------
    float -- total tax owed by the m successor firms 
    """
    return ar(y/m, b, r) * y

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
    import numpy as np
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
    google_rev = rev[0]
    google_tax = [ar(y, b, r)*y for y in google_rev]
    facebook_rev = rev[1]
    facebook_tax = [ar(y, b, r)*y for y in facebook_rev]
    avg_rate = calc_avg_rates(rev, b, r)
    tax_owed = (rev * avg_rate).sum(0)
    year = "Year"
    tr = "Industry"
    td = "Tax Due"
    b = "(billion)"
    # blank = ""
    row_list = []
    row_list.append(f"{' ': ^2}{year: ^10}{'Industry': ^26}{'Google': ^26}{'Facebook': ^26}{' ': ^3}")
    row_list.append(f"{'': ^12}{'Revenue': ^13}{'Tax Owed': ^13}{'Revenue': ^13}{'Tax Owed': ^13}{'Revenue': ^13}{'Tax Owed': ^13}{' ': ^2}")
    
    for j in range(6): 
        row_list.append(
            f"{' ': <3}{2018+j: ^8d}{total_rev_by_year[j]: >10.1f}{tax_owed[j]: >12.1f}{google_rev[j]: >14.1f}{google_tax[j]: >12.1f}{facebook_rev[j]: >14.1f}{facebook_tax[j]: >12.1f}{' ': >8}"
        )
                 
    return h_table(row_list, header_rows = 2, font_size=12, row_margin = "4px", display_html = False, return_html = True)  
