import csv 
import sys 

def common(row):
    row['tz'] = row['Time Availability'].split('(')[0]
    rv = ''' 
<li><em>Avaialble as:</em> {ml}</li>
<li><em>Time Availability:</em> {tz}</li>
<li><em>Organizational Level:</em> {org}</li>
<li><em>Organization:</em> {Organization}</li>
'''.format(**row)
    if row['Interest in changing career track']:
        rv += '''<li><em>Interest in changing career track:</em> <b>{Interest in changing career track}</b> (1 = not interested, 5 = very interested)</li>'''.format(**row)
    if row['Interest in mentoring or learning from someone outside your own organization?']:
        rv += '''<li><em>Interest in mentoring or learning from someone outside your own organization?:</em> <b>{Interest in mentoring or learning from someone outside your own organization?}</b> (1 = prefer, 3 = rather not)</li>
'''.format(**row)
    if row['Any particular requests?']:
        rv += '''<li><em>Particular requests:</em><blockquote>{Any particular requests?}</blockquote></li>
'''.format(**row)
    return rv.strip()


def mentor(row):
    col = row['Areas of expertise'] or row['Mentors: Areas of expertise']
    row['aoe'] = '<ul>' + ''.join('<li>%s</li>' % area for area in col.split(',')) + '</ul>'
    print('''<p style="page-break-after: always;">
<div style="float: right;"><h2>Mentor</h2><br><h3>Paired With:</h3></div></h1>
<h1>{name}</h1>
<ul>
{}
<li><em>Areas of expertise:</em> {aoe}</li>
</ul></p>'''.format(common(row), **row))

def learner(row):
    col = row['Interested in improving'] or row['Learners: Interested in improving']
    row['iii'] = '<ul>' + ''.join('<li>%s</li>' % area for area in col.split(',')) + '</ul>'
    print('''<p style="page-break-after: always;">
<div style="float: right;"><h2>Learner</h2><br><h3>Paired With:</h3></div></h1>
<h1>{name}</h1>                                                                                                                                                                                                                                                                                                                
<ul>
{}
<li><em>Interested in improving</em> {iii}</li>
</ul></p>'''.format(common(row), **row))

def main():
    print("<html><body>")
    for row in csv.DictReader(sys.stdin):
        row['name'] = row['Participant full name'] or row['Email Address']
        row['ml'] = row['']
        row['org'] = row['Organizational level (i.e. P3, M2, etc.)']
        if 'Mentor' in row['ml']:
            mentor(row)
        if 'Learner' in row['ml']:
            learner(row)
    print("</body></html>")

main()
