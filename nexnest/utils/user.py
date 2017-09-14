def genEmailVerificationContent(user, emailConfirmURL):
    return '''
    <div class="row">
        <div class="col-xs-1"></div>
        <div class="col-xs-10">
            <span>Hi  %s,</span>
            <br><br>
            <span>
                <strong>Welcome to the nexnest family!
                <br><br>
                In order to confirm your account and get started on nexnest please <a href="%s"> click here</a>
                <br><br>
                We're so excited to welcome you into our nest!
            </span>
            <br><br>
        </div>
    </div>
    ''' % (user.fname, emailConfirmURL)


def genEmailPasswordResetContent(user, passwordURL):
    return '''
    <div class="col-xs-1"></div>
    <div class="col-xs-10">
        <span>Hello %s,</span>
        <br><br>
        <span>
            You have requested to reset your password for your nexnest account.
            <br><br><br>
            <a href="%s">Reset my password</a>
            <br><br>
            Need help?
            Contact us at <a href="mailto:contact@nexnest.com?subject=Contact nexnest">contact@nexnest.com</a>
            <br><br>
        </span>
        <br><br>
    </div>
    ''' % (user.name, passwordURL)
