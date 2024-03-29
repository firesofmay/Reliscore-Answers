import re, urllib, urllib2, cookielib, getpass, time

"""
Logs into 
"""

def main():

    """
    Inputs  : Nothing.
    Does    : Logins to Facebook. Prints Success if logged into Reliscore
    Returns : Nothing.
    """
    
    #Enter facebook credentials here.
    user='firesofmay@gmail.com'
    passw='d'


    # Initialize the needed modules
    CHandler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    browser = urllib2.build_opener(CHandler)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
    urllib2.install_opener(browser)
 
    # Initialize the cookies and get the post_form_data
    print 'Initializing..'

    #uses decorator to keep trying ten times, so that the code is robust against random errors.
    (res) = openlink(browser, 'http://m.facebook.com/index.php')    

    #find out the post form id
    mxt = re.search('name="post_form_id" value="(\w+)"', res.read())
    pfi = mxt.group(1)
    print 'Using PFI: %s' % pfi

    res.close()

    # Initialize the POST data
    data = urllib.urlencode({
        'lsd'               : '',
        'post_form_id'      : pfi,
        'charset_test'      : urllib.unquote_plus('%E2%82%AC%2C%C2%B4%2C%E2%82%AC%2C%C2%B4%2C%E6%B0%B4%2C%D0%94%2C%D0%84'),
        'email'             : user,
        'pass'              : passw
        ,'login'             : 'Log+In'
    })
 
    # Login to Facebook
    print 'Logging in to account ' + user


    #Login to facebook, if errors, retry again till 10 times
    #TODO: Unable to pass data in decorators.
    connected = False
    errval = 0
    while not connected:
        try:
            errval +=1
            res = browser.open('https://www.facebook.com/login.php?m=m&refsrc=http%3A%2F%2Fm.facebook.com%2Findex.php&refid=8', data)
            connected = True
    

        except :
            time.sleep(5)
            print "Trying to Login Again to Facebook, count = " + str(errval)

            if errval == 10:
                break;

            pass


    #If Log out value is not shown, something went wrong, check your localization of your account,
    #maybe its in some other language.
    rcode = res.code
    if not re.search('Logout', res.read()):
        print 'Login Failed'
 
        # For Debugging (when failed login)
        fh = open('debug.html', 'w')
        fh.write(res.read())
        fh.close
 
        # Exit the execution :(
        exit(2)
    res.close()

    #Logging in reliscore via facebook
    (res) = openlink(browser,'http://reliscore.com/social-auth/login/facebook/?next=')

    htmlfile = res.readlines()


    #Fetch the post form id, new permissions, and fb_dtsg (Not sure what it is)
    for line in htmlfile:
        mxt = re.search('name="post_form_id" value="(\w+)"', line)

        if mxt:
            pfi = mxt.group(1)
            print 'Using PFI: %s' % pfi

        mxt = re.search('name="new_perms" value="([\w_-]+)"', line)

        if mxt:
            new_perms = mxt.group(1)
            print 'New Permissions: %s' % new_perms

        mxt = re.search('"fb_dtsg":"(\w+)"', line)

        if mxt:
            fb_dtsg = mxt.group(1)
            print 'fb_dtsg: %s' % fb_dtsg

    try:

        # Initialize the POST data
        data = urllib.urlencode({
            'post_form_id'      : pfi,
            '_path' : 'permissions.request',
            'app_id' : '257805210926253',
            'response_type' : 'code',
            'grant_clicked' : 'Allow',
            'new_perms' : new_perms,
            'display' : 'page',
            'fbconnect' : '1',
            'from_login' : '1',
            'from_post' : '1',
            'fb_dtsg' : fb_dtsg,
            'redirect_uri' : 'http://reliscore.com/social-auth/complete/facebook/'
            
        })
    except UnboundLocalError:

        #This happens when the user already has access, and new_perms value is not found. Hence the error.
        print "You already have the Facebook OAuth authorization.\nExiting Program"
        exit(1)
    
    #Do the post request
    res = browser.open('https://www.facebook.com/dialog/permissions.request', data)

    #Check if you got Logout in the page, if yes, Success :)
    mxt = re.search('href="\/accounts\/logout\/\?next_page=\/">(\w+)<', res.read())
    if mxt.group(1) == "Logout":
        print "Login Success :D"
    else:
        print "Awww Something Went Wrong, try Again :)"

def retrythecode(f):

    def wrapped(browser, url):

        """
        Inputs  : browser object and url to fetch.
        Does    : Its a Decorator function which adds a surrounding retry code to a browser fetching a page.
                  It is required as Servers tend to throw errors randomly. It tries to fetch the given url 10 times.
                  Since I have to do this many times, I wrote a decorator to keep code clean.
        Returns : Result from the browser
        """


       #Keep trying unless you get the link to open - beta code, not sure if i should do this
        connected = False
        errval = 0
        while not connected:
            try:

                errval +=1
                return f(browser, url)        

            except :

                time.sleep(5)

                #For debugging
                print "=====" * 30
                print "Trying to fetch Again " + url
                print " count = " + str(errval)
                print "=====" * 30

                if errval == 10:
                    break;


    return wrapped

@retrythecode
def openlink(browser, url):

    """
    Inputs  : Browser object, url to fetch.
    Does    : This is the code which is being wrapped around retrythecode decorator.
    Returns : Result from browser.
    """

    res = browser.open(url)
    return res



if __name__ == '__main__':
    main()
