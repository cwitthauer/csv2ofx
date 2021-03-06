def export(out, mapping, grid):
    """
        path: file path to save file
        mapping: mapping for grid data
        grid: csv data
    """

    accounts = {}
    cur_parent = None
    for row in range(grid.GetNumberRows()):
        tran = dict(
            [(k, mapping[k](row, grid) ) for k in ('Date', 'Payee', 'Memo', 'Category', 'Class', 'Amount', 'Number' )])
        if not mapping['split'](row, grid):
            acct = accounts.setdefault(mapping['Account'](row, grid), {})
            acct['Account'] = mapping['Account'](row, grid)
            acct['AccountDscr'] = mapping['AccountDscr'](row, grid)
            trans = acct.setdefault('trans', [])
            trans.append(tran)
            cur_parent = tran
        else:
            splits = cur_parent.setdefault('splits', [])
            splits.append(tran)

    for a in accounts.values():
        out.write("!Account\nN%(Account)s\nD%(AccountDscr)s\n^\n!Type:Bank\n" % a)
        for t in a['trans']:
            out.write("D%(Date)s\nT%(Amount)s\nP%(Payee)s\nM%(Memo)s\nL%(Category)s/%(Class)s\n" % t)
            for s in t.get('splits', []):
                out.write("S%(Category)s/%(Class)s\nE%(Memo)s\n$%(Amount)s\n" % s)
            out.write("^\n")

    out.close()
