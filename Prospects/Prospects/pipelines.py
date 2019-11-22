
from sqlalchemy.orm import sessionmaker
from Prospects.models import db_connect, create_table, MetaDataDB, PlayerStatsDB

class ProspectsPipeline(object):

    def __init__(self):

        """ Initialize database connection, sessionmaker and create tables """

        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        """ Send items to database """

        session = self.Session()

        metadatadb = MetaDataDB()
        metadatadb.ep_id = item['ep_id']
        metadatadb.full_name = item['full_name']
        metadatadb.date_of_birth = item['date_of_birth']
        metadatadb.hometown = item['hometown']
        metadatadb.country = item['country']
        metadatadb.youth_team = item['youth_team']
        metadatadb.position = item['position']
        metadatadb.height = item['height']
        metadatadb.weight = item['weight']
        metadatadb.shoots = item['shoots']

        playerstatsdb = PlayerStatsDB()
        playerstatsdb.ep_id = item['ep_id']
        playerstatsdb.season = item['season']
        playerstatsdb.team = item['team']
        playerstatsdb.league = item['league']
        playerstatsdb.games_played = item['games_played']
        playerstatsdb.goals = item['goals']
        playerstatsdb.assists = item['assists']
        playerstatsdb.penalty_min = item['penalty_min']
        playerstatsdb.plus_minus = item['plus_nimuns']

        try:
            session.add(metadatadb)
            session.add(playerstatsdb)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
