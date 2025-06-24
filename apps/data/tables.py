from apps import db

class ChineseCalendar(db.Model):
    __tablename__ = 'chinese_calendar'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month_1 = db.Column(db.String(10), nullable=False)
    month_2 = db.Column(db.String(10), nullable=False)
    month_3 = db.Column(db.String(10), nullable=False)
    month_4 = db.Column(db.String(10), nullable=False)
    month_5 = db.Column(db.String(10), nullable=False)
    month_6 = db.Column(db.String(10), nullable=False)
    month_7 = db.Column(db.String(10), nullable=False)
    month_8 = db.Column(db.String(10), nullable=False)
    month_9 = db.Column(db.String(10), nullable=False)
    month_10 = db.Column(db.String(10), nullable=False)
    month_11 = db.Column(db.String(10), nullable=False)
    month_12 = db.Column(db.String(10), nullable=False)
    next_year = db.Column(db.String(10), nullable=False)

    # Make the table read-only
    __table_args__ = {'info': {'is_read_only': True}}

    def __repr__(self):
        return f'<ChineseCalendar {self.year}>'