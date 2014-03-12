__author__ = 'y'
def createhtmlmail(subject,html,text=None):
    import MimeWriter,mimetools,cStringIO
    if text is None:
        import htmllib,formatter
        textout = cStringIO.StringIO()
        formtext = formatter.AbstractFormatter(formatter.DumbWriter(textout))
        parser = htmllib.HTMLParser(formtext)
        parser.feed(html)
        parser.close()
        text=textout.getvalue()
        del textout,formtext,parser
    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)
    writer = MimeWriter.MimeWriter(out)
    writer.addheader("Subject",subject)
    writer.addheader("MIME-Version","1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    subpart = writer.nextpart()
    pout = subpart.startbody("text/plain",[("charset",'iso-8859-1')])
    pout.write(txtin.read())
    txtin.close()
    subpart=writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding","quoted-printable")
    pout=subpart.startbody("text/html",[("charset",'us-ascii')])
    mimetools.encode(htmlin,pout,'quoted-printable')
    htmlin.close()

    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg


if __name__=="__main__":
    import smtplib
    mail_user="norsd@163.com"
    mail_pass="FRY82chxtb"
    f=open("newsletter.html",'r')
    html = f.read()
    f.close()
    try:
        f=open("newsletter.txt",'r')
        text = f.read()
    except IOError:
        text = None
    subject = "Today's Newsletter!"
    mail_host = "smtp.163.com"
    message = createhtmlmail(subject,html,text)
    server = smtplib.SMTP()
    server.connect(mail_host)
    server.login(mail_user,mail_pass)
    server.sendmail('norsd@163.com','norsd@163.com',message)
    server.quit()