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
                Click <a href="https://nexnest.com">here</a> to join the group.
                <br><br>
                Once you've joined %s, you can chat with your group, favorite and share local rental listings.
                <br><br>
                Don't keep your friends waiting. Join now!
            </span>
            <br><br>
        </div>
    </div>
    ''' % (group.leader.name, group.name, group.name)
