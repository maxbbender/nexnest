def genGroupEmailInviteNoUser(group):
    return '''
    <div class="row">
        <div class="col-xs-1"></div>
        <div class="col-xs-10">
            <span>Hello!</span>
            <br><br>
            <span>
                It looks like %s has invited you to join %s on <a href="https://nexnest.com">nexnest.com</a>.
                <br>
                Click <a href="https://nexnest.com/group/confirmEmailInvite">here</a> to join the group.
                <br><br>
                Once you've joined %s, you can chat with your group, favorite and share local rental listings.
                <br><br>
                Don't keep your friends waiting. Join now!
            </span>
            <br><br>
        </div>
    </div>
    ''' % (group.leader.name, group.name, group.name)


def genGroupEmailInviteNewUser(group):
    return '''
        <div class="row">
        <div class="col-xs-1"></div>
        <div class="col-xs-10">
            <span>Hi there!</span>
            <br><br>
            <span>
                You have been invited by %s to join the group %s on <a href="https://nexnest.com">nexnest.com</a>.
                <br>
                Please <a href="https://nexnest.com/register">sign up</a> to view your group invitation as well as the many rentals available in your area.
                <br><br>
                Once signed in, click My Groups from the top right menu bar to see your group.
                <br><br><br><br>
                If this invitation was sent to the wrong address, please disregard this email.
                Don't keey your friends waiting. Join now!
            </span>
            <br><br>
        </div>
    </div>
    ''' % (group.leader.name, group.name)
