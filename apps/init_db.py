from apps import create_app, db
from apps.data.tables import ChineseCalendar, Stems, Branches, Divisions, StemOrgan, BranchOrgan, CycleCalendar
from apps.config import config_dict

def init_stems_data():
    stems_data = [
        Stems(id=0, name='Kong'),
        Stems(id=1, name='Jia'),
        Stems(id=2, name='Yi'),
        Stems(id=3, name='Bing'),
        Stems(id=4, name='Ding'),
        Stems(id=5, name='Wu'),
        Stems(id=6, name='Ji'),
        Stems(id=7, name='Geng'),
        Stems(id=8, name='Xin'),
        Stems(id=9, name='Ren'),
        Stems(id=10, name='Gui')
    ]
    db.session.bulk_save_objects(stems_data)
    db.session.commit()
    print("Stems data inserted successfully")

def init_branches_data():
    branches_data = [
        Branches(id=0, name='Kong'),
        Branches(id=1, name='Zi'),
        Branches(id=2, name='Chou'),
        Branches(id=3, name='Yin'),
        Branches(id=4, name='Mao'),
        Branches(id=5, name='Chen'),
        Branches(id=6, name='Si'),
        Branches(id=7, name='Wu'),
        Branches(id=8, name='Wei'),
        Branches(id=9, name='Shen'),
        Branches(id=10, name='You'),
        Branches(id=11, name='Xu'),
        Branches(id=12, name='Hai')
    ]
    db.session.bulk_save_objects(branches_data)
    db.session.commit()
    print("Branches data inserted successfully")


def init_divisions_data():
    divisions_data = [
        Divisions(id=1, name='Shao Yin', element='Fire M.', phase='Fire'),
        Divisions(id=2, name='Tai Yin', element='Earth', phase='Earth'),
        Divisions(id=3, name='Shao Yang', element='Fire P.', phase='Fire'),
        Divisions(id=4, name='Yang Ming', element='Metal', phase='Metal'),
        Divisions(id=5, name='Tai Yang', element='Water', phase='Water'),
        Divisions(id=6, name='Jue Yin', element='Wood', phase='Wood')
    ]
    db.session.bulk_save_objects(divisions_data)
    db.session.commit()
    print("Divisions data inserted successfully")


def init_stem_organs_data():
    stem_organs_data = [
        StemOrgan(id=1, chinese_char='甲', pinyin='Jia', organ='GB'),
        StemOrgan(id=2, chinese_char='乙', pinyin='Yi', organ='LIV'),
        StemOrgan(id=3, chinese_char='丙', pinyin='Bing', organ='SI'),
        StemOrgan(id=4, chinese_char='丁', pinyin='Ding', organ='HT'),
        StemOrgan(id=5, chinese_char='戊', pinyin='Wu', organ='ST'),
        StemOrgan(id=6, chinese_char='已', pinyin='Ji', organ='SP'),
        StemOrgan(id=7, chinese_char='庚', pinyin='Geng', organ='CO'),
        StemOrgan(id=8, chinese_char='辛', pinyin='Xin', organ='LU'),
        StemOrgan(id=9, chinese_char='壬', pinyin='Ren', organ='BL'),
        StemOrgan(id=10, chinese_char='癸', pinyin='Gui', organ='KI')
    ]
    db.session.bulk_save_objects(stem_organs_data)
    db.session.commit()
    print("Stem Organs data inserted successfully")

def init_branch_organs_data():
    branch_organs_data = [
        BranchOrgan(id=1, chinese_char='子', pinyin='Zi', organ='GB'),
        BranchOrgan(id=2, chinese_char='丑', pinyin='Chou', organ='LIV'),
        BranchOrgan(id=3, chinese_char='寅', pinyin='Yin', organ='LU'),
        BranchOrgan(id=4, chinese_char='卯', pinyin='Mao', organ='CO'),
        BranchOrgan(id=5, chinese_char='辰', pinyin='Chen', organ='ST'),
        BranchOrgan(id=6, chinese_char='巳', pinyin='Si', organ='SP'),
        BranchOrgan(id=7, chinese_char='午', pinyin='Wu', organ='HT'),
        BranchOrgan(id=8, chinese_char='未', pinyin='Wei', organ='SI'),
        BranchOrgan(id=9, chinese_char='申', pinyin='Shen', organ='BL'),
        BranchOrgan(id=10, chinese_char='酉', pinyin='You', organ='KI'),
        BranchOrgan(id=11, chinese_char='戌', pinyin='Xu', organ='PC'),
        BranchOrgan(id=12, chinese_char='亥', pinyin='Hai', organ='TH')
    ]
    db.session.bulk_save_objects(branch_organs_data)
    db.session.commit()
    print("Branch Organs data inserted successfully")


def init_calendar_data():
    app = create_app(config_dict['development'])
    with app.app_context():
        # Create tables for all binds
        db.create_all()

        print(f"Using database: {app.config['SQLALCHEMY_BINDS']['data_db']}")

        # Initial data
        calendar_data = [
            ChineseCalendar(
                year=1925,
                month_1='24-1', month_2='23-2', month_3='24-3',
                month_4='23-4', month_5='21-6', month_6='21-7',
                month_7='19-8', month_8='18-9', month_9='18-10',
                month_10='16-11', month_11='16-12', month_12='14-1',
                next_year='13-2'
            ),
            ChineseCalendar(
                year=1926,
                month_1='13-2', month_2='14-3', month_3='12-4',
                month_4='12-5', month_5='10-6', month_6='10-7',
                month_7='8-8', month_8='7-9', month_9='7-10',
                month_10='5-11', month_11='5-12', month_12='4-1',
                next_year='2-2'
            )
        ]

        db.session.bulk_save_objects(calendar_data)
        db.session.commit()
        print("Calendar data inserted successfully")



def init_cycle_calendar_data():
    # create your Flask app in “development” mode (or whatever config you use)
    app = create_app(config_dict['development'])
    with app.app_context():
        # Create tables for all binds
        db.create_all()
        print(f"Using database: {app.config['SQLALCHEMY_BINDS']['data_db']}")

        # Heavenly Stems and Earthly Branches
        stems    = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
        branches = ["Zi", "Chou","Yin","Mao","Chen","Si", "Wu", "Wei","Shen","You","Xu","Hai"]

        # Clear out existing data (optional)
        CycleCalendar.query.delete()

        # Seed the 60‐year cycle
        for year_number in range(1, 61):
            stem   = stems[(year_number - 1) % 10]
            branch = branches[(year_number - 1) % 12]
            entry = CycleCalendar(
                year   = year_number,
                stem   = stem,
                branch = branch
            )
            db.session.add(entry)

        db.session.commit()
        print("✅ cycle_calendar seeded with 60 entries.")


if __name__ == '__main__':
    app = create_app(config_dict['development'])
    with app.app_context():
        db.create_all()
        # init_calendar_data()
        # init_stems_data()
        # init_branches_data()
        #init_divisions_data()
        #init_stem_organs_data()
        #init_branch_organs_data()
        init_cycle_calendar_data()
