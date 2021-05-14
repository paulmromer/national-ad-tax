# import numpy as np 
# from IPython.display import display, HTML

flag_h = "This is flag_h."

def h_table(
    rows="",
    has_header=True,
    header_rows = 1,
    dark_header=False,
    header_color="#ffffff",
    font_size=16,
    header_border_bottom=True,
    body_border_bottom=True,
    table_title="",
    table_align="center",
    table_border_all=False,
    border_thickness="1px",
    border_color="Black",
    stripe=True,
    stripe_intensity=0.05,
    display_html=True,
    return_html=False,
    show_args=False,
):

    """
    ---------------------------------------------------------------------------
    htable() takes a list of rows, each of which is a string.

    In the typical use case, these rows will be generated by kw_format(),
        which calls kw_f1().

    The keyword arguments other than the list of rows determine the html
        formatting applied to the rows.

    htable() applies the implied CSS styles inline so the table can be included
        in an html page without knowing what styles it is using and without
        changing its styles.

    Use 'show_args = True' to see all the keyword arguments that determine the
        style of the table.

    The default value for dark_header is false. In this case, the font color
        for the header is black.

    If 'dark_header = True', the font color for the header switches to white
        and the tinted stripes start on row 2 of the body instead of row 1 of
        the body.
    ---------------------------------------------------------------------------

    """
    htable_arg_dict = {
        "has_header": has_header,
        "header_rows": header_rows,
        "dark_header": dark_header,
        "header_color": header_color,
        "font_size": font_size,
        "header_border_bottom": header_border_bottom,
        "body_border_bottom": body_border_bottom,
        "table_title": table_title,
        "table_align": table_align,
        "table_border_all": table_border_all,
        "border_thickness": border_thickness,
        "border_color": border_color,
        "stripe": stripe,
        "stripe_intensity": stripe_intensity,
        "display_html": display_html,
        "return_html": return_html,
        "show_args": show_args,
    }
    if show_args:
        print("'show_args = True' returns a dictionary of argument names and values,")
        print("    and prints the arguement names and values.")
        print()
        print("In both cases, the results reflect any supplied arguments and")
        print("    any defaults that have not been overwritten.")
        print()
        for key, value in htable_arg_dict.items():
            print(key, " = ", repr(value))
        return htable_arg_dict

    # Create strings for HTML styles
    #   If dark_header, calculate light version of header background for stripe
    if dark_header:
        header_bkgd = "background: " + header_color + ";"
        h_font_color = "color: #ffffff;"
        if stripe:
            stripe_bkgd = "background: " + tint(header_color, stripe_intensity) + "; "
        even_stripes = True

    else:  # default gray
        header_bkgd = "background: #ffffff; "
        h_font_color = "color: #000000; "
        if stripe:
            default_grey = tint("#f5f5f5", stripe_intensity / 0.05)
            stripe_bkgd = "background: " + default_grey + "; "
        even_stripes = False

    #   Font Size
    # table_style = "font-family: Menlo, Courier; "
    table_style = "font-size: " + str(font_size) + "px; "

    #   Borders
    border_style = border_thickness + " solid " + border_color

    if body_border_bottom:
        table_border_style = "border-bottom: " + border_style + "; "
        table_border_style += "border-collapse: collapse; "
    else:
        table_border_style = "border-bottom: none; "

    if table_border_all:
        table_border_style = "border: " + border_style + "; "
        table_border_style += "border-collapse: collapse; "

    table_style += table_border_style
    if table_align == "left":
        table_style += 'align="left";'
    else:
        table_style += "margin: 32px; margin-left: auto; margin-right: auto; "

    if header_border_bottom:
        header_style = "border-bottom: " + border_style + "; "
    else:
        header_style = "border-bottom: none; "

    #   Creating the table
    #       add the header row created with header_f()
    #       create header with h_row as input
    #       loop through generator to create b_row and append to b_rows
    #       run body_tags using b_rows as input
    #       run table_tags with header and body as input

    #   Defin local variables
    b_rows = ""

    #   Define functions for creating
    #       table_f -> table tags
    #       header_f -> header tags and header content
    #       body_f -> body tags
    #       body_row_f -> body row tags

    font_fam = """font-family: Menlo, "Deja Vu Sans Mono", "Roboto Mono", "Courier New", Courier, monospace; """

    def table_f(header, body):
        h = '<table style="{0}">\n'.format(table_style)
        # if len(table_caption) >0:
        #     c0_style = "text-align: center; font-size: "
        #     c1_style = str(font_size + 4) + "; "
        #     # cap_style = "{0}{1}{2}".format(font_fam, c0_style, c1_style)
        #     cap_style = "{0}{1}".format(c0_style, c1_style)
        #     # cap_style = "text-align: center; font-size:" +  + font_fam
        #     h += "<caption style='{0}'>".format(cap_style)
        #     h += table_caption + "</caption>\n"
        h += "{0}\n".format(header)
        h += "{0}\n".format(body)
        h += "</table>\n"
        return h

    def title_f():
        title_font_size = str(1.5 * font_size)
        title_style = "text-align: center; margin-bottom: " + title_font_size + "px; "
        title_style += "font-size: " + title_font_size + "px; "
        pre_style = font_fam + "{0}{1}{2}".format(
            header_bkgd, h_font_color, title_style
        )
        return pre_style

    def header_f(table_title):
        pre_style = font_fam + "{0}{1}".format(header_bkgd, h_font_color)
        h = '  <thead style="{0}">\n'.format(header_style)
        h += '    <tr style="{0}">\n'.format("")
        h += '      <th style="{0}">\n'.format(header_bkgd)
        if len(table_title) > 0:
            h += "        <pre style='{0}'>{1}</pre>\n".format(title_f(), table_title)
        for j in range(0,header_rows):
            h += "        <pre style='{0}'>{1}</pre>\n".format(pre_style, next(row_gen))
        h += "      </th>\n"
        h += "    </tr>\n"
        h += "  </thead>\n"
        return h

    def body_f(b_rows):
        h = "  <tbody>\n{0}\n".format(b_rows)
        h += "  </tbody>\n"
        return h

    def body_row_f(b_row, row_num, even_stripes):
        if even_stripes:
            if row_num % 2 == 0:
                bkgd = stripe_bkgd
            else:
                bkgd = "background: #ffffff; "
        else:
            if row_num % 2 == 0:
                bkgd = "background: #ffffff; "
            else:
                bkgd = stripe_bkgd

        pre_style = font_fam + "{0}".format(bkgd)

        h = "    <tr>\n"
        h += '      <td style="{0}">\n'.format(bkgd)
        h += "        <pre style='{0}'>{1}</pre>\n".format(pre_style, b_row)
        h += "      </td>\n"
        h += "    </tr>\n"
        return h, row_num + 1

    row_gen = (elem for elem in rows)

    #   Create a generator, build header, remove final newline
    if header_rows > 0 or len(table_title) > 0:
        header = header_f(table_title)[0:-1]
        row_num = 1
    else:
        header = ""
        row_num = 0

    # if header_rows % 2 == 0:
    #     even_stripes = False

    #   Iterate through remaining elements in the generator, create the string of body rows
    for elem in row_gen:
        h_row, row_num = body_row_f(elem, row_num, even_stripes)
        b_rows += h_row
    body = body_f(b_rows[0:-1])[0:-1]

    #   Create the table from header and body
    table1 = table_f(header, body)
    # table = '<div style="overflow-x:auto;">\n\n'
    table = "<div>\n\n"
    table += table1
    table += "\n</div>"

    if display_html:
        display(HTML(table))

    if return_html:
        return table
    else:
        return


# ===================================================================================
#  Color functions
# ===================================================================================


def shrink_dist_to_max(h, frac):
    return int(frac * h + (1 - frac) * 0xFF)


def tint(color, frac):
    """tint() takes a color as input, returns a tint that is
            only frac times the distance from white of color

       Inputs:
            color is a string in html form for hex representation
                starts w "#" followed by hex digits;
                e.g. "#0000ff" for blue
            frac is a float between 0 and 1
                closer to zero yields a lighter tint

       Return value:
            a string in the same form
            represents a tint that takes the original distance
                of color from white and reduces it to a value of size
                frac
    """
    r = shrink_dist_to_max(int(color[1:3], 16), frac)
    g = shrink_dist_to_max(int(color[3:5], 16), frac)
    b = shrink_dist_to_max(int(color[5:7], 16), frac)
    return "#" + hex((r * 0x10000) + (g * 0x100) + b)[2:]
