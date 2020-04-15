def current_lines(eid, mtid=83, catid=133):
    string = """
           {{
               currentLines(
                   eid: {eid},
                   mtid: [{mtid}],
                   marketTypeLayout: "PARTICIPANTS", 
                   catid: {catid}
               )
           }}
    """.format(eid=str(eid), mtid=str(mtid), catid=str(catid))
    string = " ".join(string.split())
    return string

def events_by_date_by_league_group(date):
    string = """
    {
        eventsByDateByLeagueGroup( 
            es: ["in-progress", "scheduled", "complete", "suspended", "delayed", "postponed", "retired", "canceled"],
            leagueGroups: [{ mtid: 83, lid: 5, spid: 5 }],
            providerAcountOpener: 3,
            hoursRange: 25,
            showEmptyEvents: false,
            marketTypeLayout: "PARTICIPANTS",
            ic: false,
            startDate: <date>,
            timezoneOffset: -5,
            nof: true,
            hl: true,
            sort: {by: ["lid", "dt", "des"], order: ASC}
        ) {
            events {
                eid lid spid des dt es rid ic ven tvs cit cou st sta hl seid writeingame
                participants {
                    eid partid partbeid psid ih rot tr sppil sppic source {
                     ... on Team { tmid lid tmblid nam nn sn abbr cit senam imageurl } 
                     ... on ParticipantGroup {
                        partgid nam lid participants {
                            eid partid psid ih rot source {
                                ... on Player { pid fn lnam }
                                ... on Team { tmid lid nam nn sn abbr cit }
                            }
                        }
                     }
                }
            }}
        }
    }
    """
    string = " ".join(string.split())
    return string

