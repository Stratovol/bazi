# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from apps import db
from datetime import datetime, timezone

from calculation.miscellaneous import get_chinese_season_by_month
from calculation.moon_phase import moon_phase
from calculation.chinese_calendar import chinese_from_fixed, fixed_from_gregorian

@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():
    return render_template('pages/index.html', segment='lunar_bazi')

@blueprint.route('/api/moon_phase')
def api_moon_phase():
    date_str = request.args.get('date')
    time_str = request.args.get('time', None)

    if not date_str:
        return jsonify({"error": "missing date"}), 400

    # build a UTC datetime
    if time_str and time_str != 'Unknown Hour':
        dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
    else:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
    dt = dt.replace(tzinfo=timezone.utc)

    # compute
    result = moon_phase(dt)
    return jsonify(result)

@blueprint.route('/api/chinese_date')
def api_chinese_date():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"error":"missing date"}), 400

    # parse date (you already have this)
    y, m, d = map(int, date_str.split('-'))
    fixed = fixed_from_gregorian(y, m, d)
    cd = chinese_from_fixed(fixed)

    # **HERE** call your new function
    season = get_chinese_season_by_month(cd.month)

    return jsonify({
      "cycle":         cd.cycle,
      "year":          cd.year,
      "month":         cd.month,
      "is_leap_month": cd.is_leap_month,
      "day":           cd.day,
      "name":          cd.name,
      "chinese_season": season   # ← new field
    })

@blueprint.route('/billing')
def billing():
    return render_template('pages/billing.html', segment='billing')

@blueprint.route('/rtl')
def rtl():
    return render_template('pages/rtl.html', segment='rtl')

@blueprint.route('/tables')
def tables():
    return render_template('pages/tables.html', segment='tables')

@blueprint.route('/virtual_reality')
def virtual_reality():
    return render_template('pages/virtual-reality.html', segment='virtual_reality')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        bio = request.form.get('bio')

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.address = address
        current_user.bio = bio

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        return redirect(url_for('home_blueprint.profile'))

    return render_template('pages/profile.html', segment='profile')


# Helper - Extract current page name from request
@blueprint.app_template_filter('replace_value')
def replace_value(value, args):
  return value.replace(args, " ").title()

def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None