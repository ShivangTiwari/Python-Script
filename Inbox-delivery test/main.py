with open('app/common/rcpt_record.json') as f:
    data = json.load(f)

def send_mail(smtp_server, sender_email, sender_pwd, sender_port, receivers_email, subject,body,provider,unsuccess_mail):       
    list_current=[]
    message = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    status=True
    try:
        with smtplib.SMTP_SSL(smtp_server, sender_port, context=context) as smtp:
            smtp.login(sender_email, sender_pwd)
            smtp.sendmail(sender_email, receivers_email, message)
            flag=0
            for list in unsuccess_mail:
                if provider in list:
                    flag=1
            if(flag==0):
                list_current.extend((provider, "NA", "NA", 0))
                unsuccess_mail.append(list_current) 
        logging.info("mail sent successfull from:"+ sender_email+ " to " + receivers_email)
    except Exception as e:
        error_msg = " ".join(e.smtp_error.decode().split()[:4])
        logging.info(error_msg)
        flag=0
        for list in unsuccess_mail:
            if provider in list:
                #list[3] is count of unsuccess mail
                list[3]+=1
                flag=1
        if(flag==0):
            list_current.extend((provider, e.smtp_code, error_msg, 1))
            unsuccess_mail.append(list_current) 
        status= False
    return status
   
def check_imap_receive(imap_server, receivers_email, receivers_pwd, mailbox, subject,provider,lock,list_result,max_rcpt,sender_email):
    status=True
    today = date.today().strftime("%d-%b-%Y")
    try:
        with imaplib.IMAP4_SSL(imap_server)as imap:
            imap.login(receivers_email, receivers_pwd)
            bool = False
            # retry to get a response for 3 times
            for retry in range(3):
                if(bool==True):
                    break
                if(provider =='yahoo'):
                    for folder in mailbox:
                        list_current=[]
                        imap.select(mailbox[folder])
                        res,uids= imap.search(None, f'(FROM {sender_email} UNSEEN SENTON {today})')
                        var=uids[0].split()
                        if(len(var)==0):
                            flag=0
                            for list in list_result:
                                if provider in list and mailbox[folder] in list:
                                    list[3]=list[3]+0
                                    flag=1
                            if(flag==0):
                                list_current.extend((provider, mailbox[folder], max_rcpt, 0))
                                list_result.append(list_current)  
                                del list_current 
                        
                        for i in range(len(var)):
                            typ,data=imap.fetch(var[-(i+1)],'(RFC822)')
                            message=message_from_bytes(data[0][1])
                            if(message.get("subject")==subject):
                                bool = True
                                acquired=lock.acquire()
                                try:
                                    flag=0
                                    for list in list_result:
                                        if provider in list and mailbox[folder] in list:
                                            #list[3] here is count of total email_reached 
                                            list[3]=list[3]+1
                                            flag=1
                                    if(flag==0):
                                        list_current.extend((provider, mailbox[folder], max_rcpt, 1))
                                        list_result.append(list_current) 
                                finally:
                                    if acquired:
                                        lock.release()
                                break 
                            else:
                                acquired=lock.acquire()
                                try:
                                    flag=0
                                    for list in list_result:
                                        if provider in list and mailbox[folder] in list:
                                            list[3]=list[3]+0
                                            flag=1
                                    if(flag==0):
                                        list_current.extend((provider, mailbox[folder], max_rcpt, 0))
                                        list_result.append(list_current)  
                                        del list_current 
                                finally:
                                    if acquired:
                                       lock.release() 
                
                else:
                    for folder in mailbox:
                        list_current=[]
                        imap.select(mailbox[folder])
                        res,uids= imap.search(None, '(UNSEEN SUBJECT "'+ subject+ '")')
                        #if mail found
                        if (not uids[0]== b''):
                            bool = True
                            acquired=lock.acquire()
                            try:
                                flag=0
                                for list in list_result:
                                    if provider in list and mailbox[folder] in list:
                                        #list[3] here is count of total email_recahed 
                                        list[3]=list[3]+1
                                        flag=1
                                if(flag==0):
                                    list_current.extend((provider, mailbox[folder], max_rcpt, 1))
                                    list_result.append(list_current) 
       
                            finally:
                                if acquired:
                                    lock.release()
                            break 
                        else:
                            acquired=lock.acquire()
                            try:
                                flag=0
                                for list in list_result:
                                    if provider in list and mailbox[folder] in list:
                                        list[3]=list[3]+0
                                        flag=1
                                if(flag==0):
                                    list_current.extend((provider, mailbox[folder], max_rcpt, 0))
                                    list_result.append(list_current)  
                                    del list_current 
                            finally:
                                if acquired:
                                    lock.release()            
    except Exception as e:
        logging.info("Imap fail - ErrorType : {}, Error : {}".format(type(e).__name__, e))
        status=False  
    return status



def start_test(smtp_server, sender_email, sender_pwd, sender_port, receivers_email, imap_server, receivers_pwd, mailbox,provider,lock,subject,body,unsucess_dict,list_result,max_rcpt):
    #send mail
    send_mail(smtp_server, sender_email, sender_pwd, sender_port, receivers_email, subject,body,provider,unsucess_dict) 
    time.sleep(5)
    check_imap_receive(imap_server, receivers_email, receivers_pwd, mailbox, subject,provider,lock,list_result,max_rcpt,sender_email)

def ID_Test(sender_email,sender_pwd,smtp_server,sender_port,providers,max_rcpt,subject,body,unsucess_dict,list_result):
    logging.info("inbox delivery test starts")
    #thread list
    threads=[]
    for mta in providers:
        count=0
        for receivers_email, receivers_rec in data['rcpts'].items():
            if(count>= max_rcpt):
                break
            receivers_pwd=receivers_rec['pwd']
            provider= receivers_rec['provider']
            #check if provider is in the list which we want to check
            if provider == mta:
                count+=1
                mailbox=data['providers'][provider]['mailbox']
                imap_server=data['providers'][provider]['imap_host']
                #threading
                lock=threading.Lock()
                T1 = threading.Thread(target=start_test, args=(smtp_server, sender_email, sender_pwd, sender_port, receivers_email, imap_server, receivers_pwd, mailbox,provider,lock,subject,body,unsucess_dict,list_result,max_rcpt))
                T1.start()
                threads.append(T1)
                
    for t in threads:
        t.join()
    #return result list 
    return list_result
