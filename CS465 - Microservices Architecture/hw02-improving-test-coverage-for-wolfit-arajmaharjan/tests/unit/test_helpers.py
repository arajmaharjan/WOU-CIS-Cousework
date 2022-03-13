from app.helpers import pretty_date
from datetime import datetime, timedelta

def test_now():
    assert pretty_date(datetime.utcnow()) == "just now" 

def test_about_now():
    """Tests to return just about now."""
    assert (pretty_date(datetime.utcnow() - timedelta(days=-1))) == "just about now" 

def test_seconds_ago():
    """Tests to check how many seconds ago."""
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=59))) == "59 seconds ago"

def test_minute_ago():
    """Tests to check if datetime stamp is under a minute."""
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=60))) == "a minute ago"

def test_minutes_ago():
    """checks how many minutes ago."""
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=3599))) == "59 minutes ago" 

def test_hour_ago():
    """Tests to check if datetime stamp is under an hour."""
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=3600))) == "an hour ago"

def test_hours_ago():
    """checks how many hours ago."""
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=7200))) == "2 hours ago"

def test_yesterday():
    """Tests to return yesterday."""
    assert (pretty_date(datetime.utcnow() - timedelta(days=1))) == "Yesterday" 

def test_days_ago():
    """checks how many days ago"""
    assert (pretty_date(datetime.utcnow() - timedelta(days=2))) == "2 days ago"
    assert (pretty_date(datetime.utcnow() - timedelta(days=6))) == "6 days ago"

def test_week_ago():
    """checks how many weeks ago"""
    assert (pretty_date(datetime.utcnow() - timedelta(days=7))) == "1 weeks ago" 

def test_month_ago():
    """checks how many months ago"""
    assert (pretty_date(datetime.utcnow() - timedelta(days=31))) == "1 months ago" 
    assert (pretty_date(datetime.utcnow() - timedelta(days=60))) == "2 months ago"
    assert (pretty_date(datetime.utcnow() - timedelta(days=90))) == "3 months ago" 

def test_year_ago():
    """checks how many years ago"""
    assert (pretty_date(datetime.utcnow() - timedelta(days=365))) == "1 years ago"
    assert (pretty_date(datetime.utcnow() - timedelta(days=366))) == "1 years ago" 
    assert (pretty_date(datetime.utcnow() - timedelta(days=730))) == "2 years ago" 