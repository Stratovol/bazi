from apps import db

class ChineseCalendar(db.Model):
    __bind_key__ = 'data_db'  # This tells SQLAlchemy to use the data database
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


class Stems(db.Model):
    __bind_key__ = 'data_db'
    __tablename__ = 'stems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    __table_args__ = {'info': {'is_read_only': True}}

    def __repr__(self):
        return f'<Stems {self.name}>'


class Branches(db.Model):
    __bind_key__ = 'data_db'
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    __table_args__ = {'info': {'is_read_only': True}}

    def __repr__(self):
        return f'<Branches {self.name}>'


class Divisions(db.Model):
    __bind_key__ = 'data_db'
    __tablename__ = 'divisions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    element = db.Column(db.String(10), nullable=False)
    phase = db.Column(db.String(10), nullable=False)

    __table_args__ = {'info': {'is_read_only': True}}

    def __repr__(self):
        return f'<Divisions {self.name}>'


class StemOrgan(db.Model):
    __bind_key__ = 'data_db'
    __tablename__ = 'stem_organs'

    id = db.Column(db.Integer, primary_key=True)
    chinese_char = db.Column(db.String(10), nullable=False)
    pinyin = db.Column(db.String(10), nullable=False)
    organ = db.Column(db.String(10), nullable=False)

    __table_args__ = {'info': {'is_read_only': True}}

    def __repr__(self):
        return f'<StemOrgan {self.pinyin} - {self.organ}>'


class BranchOrgan(db.Model):
    __bind_key__ = 'data_db'
    __tablename__ = 'branch_organs'

    id = db.Column(db.Integer, primary_key=True)
    chinese_char = db.Column(db.String(10), nullable=False)
    pinyin = db.Column(db.String(10), nullable=False)
    organ = db.Column(db.String(10), nullable=False)

    __table_args__ = {'info': {'is_read_only': True}}

    def __repr__(self):
        return f'<BranchOrgan {self.pinyin} - {self.organ}>'

class CycleCalendar(db.Model):
    __bind_key__ = 'data_db'
    __tablename__ = 'cycle_calendar'

    id          = db.Column(db.Integer, primary_key=True)
    year        = db.Column(db.Integer, nullable=False)   # 1..60
    stem        = db.Column(db.String(10), nullable=False)
    branch      = db.Column(db.String(10), nullable=False)