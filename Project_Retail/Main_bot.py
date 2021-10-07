from UI_Actions import UI_Actions
import UI_Constants
from UI_Actions import login_retry

try:
    #************     UI Bot Action starts    ***************#
    uiActions = UI_Actions()

    #************     Initiate WebSite Login  ***************#
    i = 0
    while i < login_retry:
        isLoginSuccess = uiActions.login()
        if isLoginSuccess == True:
            break
        i = i+1
    else:
        uiActions.manualLogin()

    #************     Initiate Dealer Form Entry  ***************#
    uiActions.performAction()


    #************    Selecting Date and FL2 REATAIL SALE  ***************#
    uiActions.dateAndFL2reatailSelection()


    #************    BrandName,PackSize and Bottles count  ***************#
    uiActions.calling_fill()

    #************    Loging out and closing the bot  ***************#
    uiActions.logOut()

    # ************    Exception Block  ***************#
except ImportError:
    print(ImportError)

    # ************    Finally block   ***************#
finally:
    if UI_Constants.XPATH_LOG_OUT == True:
        u = UI_Actions()
        u.logOut()
    elif UI_Constants.LOGIN_URL == True:
        u = UI_Actions()
        u.close()
    else:
        print("Execution done sucessfully")


