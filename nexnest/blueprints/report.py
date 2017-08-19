from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from nexnest import db
from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.group import Group

from nexnest.models.platform_report import PlatformReport
from nexnest.models.report_listing import ReportListing
from nexnest.models.report_landlord import ReportLandlord
from nexnest.models.report_group import ReportGroup

from nexnest.utils.flash import flash_errors

from nexnest.forms import PlatformReportForm, ListingReportForm, LandlordReportForm, GroupReportForm


reports = Blueprint('reports', __name__, template_folder='../templates/reports')

session = db.session


@reports.route('/platformReport/create', methods=['GET', 'POST'])
def createPlatformReport():
    form = PlatformReportForm()

    if form.validate_on_submit():
        newPlatformReport = PlatformReport(title=form.title.data,
                                           content=form.content.data,
                                           user=current_user,
                                           sourceURL=form.sourceURL.data)

        session.add(newPlatformReport)
        session.commit()

        flash('Your report has been forwarded to NexNest Administrators!', 'success')
    else:
        flash_errors(form)

    return form.redirect()


@reports.route('/listingReport/create', methods=['GET', 'POST'])
@login_required
def createListingReport():
    form = ListingReportForm()

    if form.validate_on_submit():
        listing = Listing.query.filter_by(id=form.listing_id.data).first_or_404()

        newListingReport = ReportListing(title=form.title.data,
                                         content=form.content.data,
                                         user=current_user,
                                         sourceURL=form.sourceURL.data,
                                         listing=listing)

        session.add(newListingReport)
        session.commit()

        flash('Your report for the listing at %s has been made. NexNest Admins will be looking into it!' % listing.address, 'success')

    else:
        flash_errors(form)

    return form.redirect()


@reports.route('/landlordReport/create', methods=['GET', 'POST'])
@login_required
def createLandlordReport():
    form = LandlordReportForm()

    if form.validate_on_submit():
        landlord = Landlord.query.filter_by(user_id=form.landlord_id.data).first_or_404()

        newLandlordReport = ReportLandlord(title=form.title.data,
                                           content=form.content.data,
                                           landlord=landlord,
                                           user=current_user,
                                           sourceURL=form.sourceURL.data)

        session.add(newLandlordReport)
        session.commit()

        flash('Your report has been recieved. NexNest Admins will be looking into it!', 'success')

    else:
        flash_errors(form)

    return form.redirect()


@reports.route('/groupReport/create', methods=['GET', 'POST'])
@login_required
def createGroupReport():
    form = GroupReportForm()

    if form.validate_on_submit():
        group = Group.query.filter_by(id=form.group_id.data).first_or_404()

        newGroupReport = ReportGroup(title=form.title.data,
                                     content=form.content.data,
                                     group=group,
                                     user=current_user)
        session.add(newGroupReport)
        session.commit()

        flash('Your report has been received. NexNest Admins will be looking into it!', 'success')

    else:
        flash_errors(form)

    return form.redirect()
