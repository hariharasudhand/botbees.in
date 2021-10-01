from UI_Actions import UI_Actions
import UI_Constants

try:
    #************     UI Bot Action starts    ***************#
    uiActions = UI_Actions()

    #************     Initiate WebSite Login  ***************#
    i = 0
    while i < UI_Constants.LOGIN_RETRY:
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
    uiActions.loginOut()

except ImportError:
    print(ImportError)    
