def current_lines(eid, mtid=83, catid=133):
    cl_string = """
           {{
               currentLines(
                   eid: {eid},
                   mtid: [{mtid}],
                   marketTypeLayout: "PARTICIPANTS", 
                   catid: {catid}
               )
           }}
    """.format(eid=str(eid), mtid=str(mtid), catid=str(catid))
    cl_string = " ".join(cl_string.split())
    return cl_string
