
from apps import create_app, db
from apps.data.tables import ChineseCalendar
from apps.config import config_dict  # Add this import

def init_calendar_data():
    # Pass the config class instead of string
    app = create_app(config_dict['development'])
    with app.app_context():
        # Create the table
        db.create_all()

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

        # Add the data
        db.session.bulk_save_objects(calendar_data)
        db.session.commit()

if __name__ == '__main__':
    init_calendar_data()